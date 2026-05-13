'use strict';

/**
 * 翻页时刻语义校验（机制层）：捕获「句首陷阱」等可自动化发现的误判。
 *
 * 典型问题：把某条字幕的 **start** 当作「进入下一页」的时刻，但该句开场白仍在展开
 * **上一页**幻灯的主题（例如过渡语「然后它用了……」仍属于「认识 V4」口播块）。
 *
 * 默认 WARN：仅当「翻页≈字幕条起点」且该条包含**下一页 .wa** 短语（高危句首陷阱）。
 * 可选 `--audit-cue-starts`：列出所有「翻页≈字幕起点」（多为正常话题切换）。
 */

const fs = require('fs');
const path = require('path');
const { resolvePath } = require('./path_resolver');
const { parseSrt } = require('./srt_map');

const EPS_DEFAULT = 0.12;

function normTxt(s) {
  return String(s || '')
    .replace(/\s+/g, '')
    .trim();
}

/**
 * @param {string} html
 * @returns {{ wa: string }[]}
 */
function extractWaPerSlide(html) {
  const slides = [];
  const re =
    /<section\b[^>]*class=["'][^"']*\bslide\b[^"']*["'][^>]*>([\s\S]*?)<\/section>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    const inner = m[1];
    const waM = inner.match(
      /class=["'][^"']*\bwa\b[^"']*["'][^>]*>([\s\S]*?)<\/[^>\s]+>/i
    );
    let wa = '';
    if (waM) {
      wa = waM[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    }
    slides.push({ wa });
  }
  return slides;
}

/** @param {number[]} durations */
function flipTimesAfterEachSlide(durations) {
  const out = [];
  let cum = 0;
  for (let i = 0; i < durations.length - 1; i++) {
    cum += durations[i];
    out.push({
      afterSlideIndex: i,
      flipIndex1Based: i + 1,
      timeSec: Math.round(cum * 1000) / 1000,
    });
  }
  return out;
}

function findEntryStartingNear(entries, t, eps) {
  for (const e of entries) {
    if (Math.abs(e.start - t) <= eps) return e;
  }
  return null;
}

/**
 * @param {object} opts
 * @param {number[]} opts.durations
 * @param {{ start:number; end:number; i:number; text:string }[]} opts.entries
 * @param {{ wa:string }[]} [opts.waSlides]
 * @param {number} [opts.epsilonSec]
 */
function checkTimingBoundaries(opts) {
  const epsilonSec = opts.epsilonSec ?? EPS_DEFAULT;
  const auditCueStarts = Boolean(opts.auditCueStarts);
  const warnings = [];
  const infos = [];

  const flips = flipTimesAfterEachSlide(opts.durations);
  const waSlides = opts.waSlides || [];

  for (const flip of flips) {
    const hitStart = findEntryStartingNear(opts.entries, flip.timeSec, epsilonSec);
    if (!hitStart) continue;

    const base = {
      flipAfterSlide1Based: flip.flipIndex1Based,
      timeSec: flip.timeSec,
      srtIndex: hitStart.i,
      srtLine: hitStart.text.slice(0, 100),
    };

    const nextWa = waSlides[flip.afterSlideIndex + 1];
    const nw = normTxt(nextWa && nextWa.wa);
    const waInCue = nw.length >= 6 && normTxt(hitStart.text).includes(nw);

    if (waInCue) {
      warnings.push({
        code: 'FLIP_AT_NEXT_WA_SENTENCE_START',
        ...base,
        waSnippet: (nextWa.wa || '').slice(0, 48),
        message:
          '翻页落在「下一页 .wa」所在字幕条的起点（±' +
          epsilonSec +
          's）：高危句首陷阱——该句常为过渡/顺承，画面应多停留在上一页直至该段讲完；请延后累计边界到该条结束之后或下一条起点。',
      });
    } else if (auditCueStarts) {
      infos.push({
        code: 'FLIP_AT_SRT_START',
        ...base,
        message:
          '翻页与字幕条起点对齐（话题首句常见，未必错误）。若画面脱节，再人工复核。',
      });
    }
  }

  if (!warnings.length && !infos.some((x) => x.code === 'FLIP_AT_SRT_START')) {
    infos.unshift({
      code: 'OK',
      message: auditCueStarts
        ? '未发现翻页与字幕起点重合（ε=' + epsilonSec + 's）。'
        : '未发现「下一页 .wa 句起点」类高危对齐（ε=' +
          epsilonSec +
          's）。话题切换常与字幕条对齐属正常；全面列表请加 --audit-cue-starts。',
    });
  }

  return { warnings, infos, epsilonSec, auditCueStarts };
}

/**
 * @param {string} projectRoot
 * @param {{ epsilonSec?: number }} [options]
 */
function runProjectTimingCheck(projectRoot, options = {}) {
  const auditCueStarts = Boolean(options.auditCueStarts);
  const cfgPath = resolvePath(projectRoot, 'timing', 'wav-durations.json');
  const srtPath = resolvePath(projectRoot, 'subtitles', 'sub.srt');
  const htmlSlides = resolvePath(projectRoot, 'slides', 'presentation.html');
  const htmlRoot = path.join(projectRoot, 'presentation.html');
  const htmlPath = fs.existsSync(htmlRoot) ? htmlRoot : htmlSlides;

  if (!fs.existsSync(cfgPath)) {
    return { skipped: true, reason: '缺少 timing/wav-durations.json', warnings: [], infos: [] };
  }
  if (!fs.existsSync(srtPath)) {
    return { skipped: true, reason: '缺少 subtitles/sub.srt', warnings: [], infos: [] };
  }
  if (!fs.existsSync(htmlPath)) {
    return { skipped: true, reason: '缺少 presentation.html', warnings: [], infos: [] };
  }

  const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
  const durations = cfg.slideDurationsSec;
  if (!Array.isArray(durations) || durations.length < 2) {
    return {
      skipped: true,
      reason: 'slideDurationsSec 无效',
      warnings: [],
      infos: [],
    };
  }

  const entries = parseSrt(srtPath);
  const html = fs.readFileSync(htmlPath, 'utf8');
  const waSlides = extractWaPerSlide(html);

  return checkTimingBoundaries({
    durations,
    entries,
    waSlides,
    epsilonSec: options.epsilonSec,
    auditCueStarts,
  });
}

function printReport(result, jsonMode) {
  if (result.skipped) {
    const payload = { skipped: true, reason: result.reason };
    if (jsonMode) console.log(JSON.stringify(payload, null, 2));
    else console.log(`ℹ️  timing-check 跳过: ${result.reason}`);
    return;
  }
  if (jsonMode) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }
  console.log('\n── timing-check（翻页边界） ──');
  for (const w of result.warnings) {
    console.log(`\n⚠️  [${w.code}] 第 ${w.flipAfterSlide1Based} 页后翻 (${w.timeSec.toFixed(2)}s)`);
    if (w.srtIndex !== undefined) console.log(`    SRT #${w.srtIndex}: ${w.srtLine || ''}`);
    if (w.waSnippet) console.log(`    .wa 片段: ${w.waSnippet}`);
    console.log(`    ${w.message}`);
  }
  for (const i of result.infos) {
    const tag = i.code === 'FLIP_AT_SRT_START' ? 'ℹ️' : '✓';
    console.log(`\n${tag}  [${i.code || 'INFO'}] ${i.message}`);
    if (i.srtLine) console.log(`    SRT #${i.srtIndex}: ${i.srtLine}`);
  }
  console.log('');
}

module.exports = {
  checkTimingBoundaries,
  runProjectTimingCheck,
  extractWaPerSlide,
  flipTimesAfterEachSlide,
  printReport,
  EPS_DEFAULT,
};
