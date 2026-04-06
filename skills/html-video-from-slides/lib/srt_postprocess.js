'use strict';

/**
 * 烧录前处理 Whisper 生成的 SRT：可选文案替换、按字宽换行（避免单行超出画面）。
 */

const fs = require('fs');

function escapeRegex(s) {
  return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * @param {string} text
 * @param {Array<{from?: string, to?: string, ignoreCase?: boolean} | [string, string]>} replacements
 */
function applyReplacements(text, replacements) {
  if (!replacements || !replacements.length) return text;
  let out = text;
  for (const item of replacements) {
    const from = Array.isArray(item) ? item[0] : item.from;
    const to = Array.isArray(item) ? item[1] : item.to;
    const ignoreCase = Array.isArray(item) ? false : item.ignoreCase === true;
    if (from == null || to == null) continue;
    if (ignoreCase) {
      out = out.replace(new RegExp(escapeRegex(from), 'gi'), to);
    } else {
      const parts = out.split(from);
      out = parts.join(to);
    }
  }
  return out;
}

/**
 * 按 1080p 宽度与字号估算每行安全字数（中日文为主；偏保守避免出画）。
 * 粗体/宽体字在屏上往往比「字数×字号」更宽，故上限压到约 22 字/行。
 * @param {number} fontSize
 * @param {number} [videoWidth]
 */
function suggestCharsPerLine(fontSize, videoWidth = 1920) {
  const fs = Math.max(12, Math.min(72, Number(fontSize) || 18));
  const marginPx = 320;
  const usable = Math.max(960, videoWidth - marginPx);
  const perChar = fs * 1.22;
  const n = Math.floor(usable / perChar);
  return Math.max(14, Math.min(22, n));
}

/**
 * 将一段字幕折行：优先用 Intl.Segmenter 按词界折行（避免「时候」被拆开）；
 * 不支持时再按标点与字数回退。
 * @param {string} text
 * @param {number} maxChars
 */
/**
 * 合并「的」与「时…」被误拆到两行的情况（词界切分偶发）。
 * 若合并后会超过 maxChars 则不合并，避免单行出画或与折行逻辑死循环。
 */
function mergeSplitDeShi(lines, m) {
  const maxLen = m != null ? m : 999;
  const o = [];
  for (let i = 0; i < lines.length; i++) {
    let t = lines[i];
    while (
      i + 1 < lines.length &&
      /的$/.test(t) &&
      /^时/.test(lines[i + 1])
    ) {
      const merged = t + lines[i + 1];
      if (merged.length > maxLen) break;
      t = merged;
      i++;
    }
    o.push(t);
  }
  return o;
}

/** 按词折成多行（单行 flat 文本）。 */
function segmenterWrapFlat(flat, m) {
  const seg = new Intl.Segmenter('zh-Hans', { granularity: 'word' });
  const lines = [];
  let cur = '';
  for (const { segment } of seg.segment(flat)) {
    const next = cur + segment;
    if (next.length > m && cur.length > 0) {
      lines.push(cur.trim());
      cur = segment;
    } else {
      cur = next;
    }
  }
  if (cur.trim()) lines.push(cur.trim());
  return lines;
}

/** 反复按词折行并合并「的+时」，直到各行都不超过 m（合并后若仍超长则再拆）。 */
function wrapUntilAllShort(lines, m) {
  let out = mergeSplitDeShi(lines, m);
  let guard = 0;
  while (guard++ < 10 && out.some((r) => r.length > m)) {
    const next = [];
    for (const row of out) {
      if (row.length <= m) next.push(row);
      else next.push(...segmenterWrapFlat(row, m));
    }
    out = mergeSplitDeShi(next, m);
  }
  return out;
}

function wrapSubtitleText(text, maxChars) {
  const m = Math.max(8, Math.min(42, maxChars || 28));
  const flat = String(text)
    .replace(/\r/g, '')
    .split('\n')
    .map((x) => x.trim())
    .filter(Boolean)
    .join('');
  if (flat.length <= m) return flat;

  if (typeof Intl !== 'undefined' && Intl.Segmenter) {
    try {
      const lines = segmenterWrapFlat(flat, m);
      return wrapUntilAllShort(lines, m).join('\n');
    } catch (_) {
      /* fall through */
    }
  }

  const lines = [];
  let i = 0;
  while (i < flat.length) {
    let end = Math.min(i + m, flat.length);
    if (end < flat.length) {
      const chunk = flat.slice(i, end);
      let breakAt = -1;
      for (let k = chunk.length - 1; k >= Math.floor(m * 0.35); k--) {
        const c = chunk[k];
        if ('，。！？；、：\u3000'.includes(c) || c === ' ' || c === ',') {
          breakAt = i + k + 1;
          break;
        }
      }
      if (breakAt > i) {
        end = breakAt;
      }
    }
    const line = flat.slice(i, end).trim();
    if (line) lines.push(line);
    i = end;
  }
  return wrapUntilAllShort(lines, m).join('\n');
}

/**
 * @param {string} content raw SRT
 */
function parseSrt(content) {
  const lines = content.replace(/^\ufeff/, '').replace(/\r\n/g, '\n').split('\n');
  const blocks = [];
  let i = 0;
  while (i < lines.length) {
    while (i < lines.length && !lines[i].trim()) i++;
    if (i >= lines.length) break;
    const index = lines[i++];
    if (i >= lines.length) break;
    const timeLine = lines[i++];
    const textLines = [];
    while (i < lines.length && lines[i].trim() !== '') {
      textLines.push(lines[i++]);
    }
    if (timeLine && timeLine.includes('-->')) {
      blocks.push({ index, timeLine, text: textLines.join('\n') });
    }
  }
  return blocks;
}

function serializeSrt(blocks) {
  const body = blocks
    .map((b) => `${b.index}\n${b.timeLine}\n${b.text}\n`)
    .join('\n');
  return '\ufeff' + body;
}

/**
 * @param {string} srcPath
 * @param {string} destPath
 * @param {{ charsPerLine?: number, replacements?: Array, wrap?: boolean }} opts
 */
function prepareSrtForBurn(srcPath, destPath, opts = {}) {
  const raw = fs.readFileSync(srcPath, 'utf-8');
  const blocks = parseSrt(raw);
  const reps = opts.replacements || [];
  const wrap = opts.wrap !== false;
  let cpl = opts.charsPerLine;
  if (cpl == null || cpl === 0) {
    cpl = suggestCharsPerLine(opts.fontSize ?? 18);
  }
  const wrapChars = Math.max(8, Math.min(36, Number(cpl) || 20));

  for (const b of blocks) {
    let t = applyReplacements(b.text, reps);
    if (wrap) t = wrapSubtitleText(t, wrapChars);
    b.text = t;
  }
  fs.writeFileSync(destPath, serializeSrt(blocks), 'utf-8');
}

module.exports = {
  applyReplacements,
  wrapSubtitleText,
  suggestCharsPerLine,
  parseSrt,
  serializeSrt,
  prepareSrtForBurn,
};
