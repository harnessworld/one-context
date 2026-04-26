'use strict';

/**
 * presentation.html + 整段 WAV + wav-durations.json → final_from_wav.mp4
 */

const { chromium } = require('playwright');
const ffmpegPath = require('ffmpeg-static');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { pathToFileURL } = require('url');
const {
  hexToAssWithAlpha,
  hexToAssPrimaryColour,
  DEFAULT_SUBTITLE_STYLE,
} = require('./ass_colours');
const { prepareSrtForBurn, suggestCharsPerLine } = require('./srt_postprocess');
const { resolvePath } = require('./path_resolver');

const FPS = 60;
const VIDEO_BITRATE = '8M';
const VIDEO_PRESET = 'slow';

function ff(args) {
  execSync(`"${ffmpegPath}" ${args}`, { stdio: 'inherit' });
}

function getMediaDuration(filePath) {
  try {
    execSync(`"${ffmpegPath}" -i "${filePath}"`, { stdio: 'pipe' });
  } catch (e) {
    const output = Buffer.concat([
      e.stderr || Buffer.alloc(0),
      e.stdout || Buffer.alloc(0),
    ]).toString();
    const m = output.match(/Duration:\s*(\d+):(\d+):(\d+)\.(\d+)/);
    if (m) {
      return +m[1] * 3600 + +m[2] * 60 + +m[3] + +m[4] / 100;
    }
  }
  return 0;
}

/** SRT 时间戳 → ASS 时间戳（H:MM:SS.cc） */
function srtTimeToAss(ts) {
  const m = ts.match(/(\d+):(\d+):(\d+)[,.](\d{1,3})/);
  if (!m) return '0:00:00.00';
  const h = parseInt(m[1], 10);
  const min = m[2];
  const s = m[3];
  const cs = Math.round(parseInt(m[4].padEnd(3, '0').slice(0, 3), 10) / 10)
    .toString()
    .padStart(2, '0');
  return `${h}:${min}:${s}.${cs}`;
}

/** 将 SRT 转为 ASS 文件（ass filter 对 MarginV 支持更标准） */
function generateAssFromSrt(srtPath, assPath, style) {
  const raw = fs.readFileSync(srtPath, 'utf-8');
  const lines = raw.replace(/^\ufeff/, '').replace(/\r\n/g, '\n').split('\n');
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

  const header = `[Script Info]
ScriptType: v4.00+
PlayResX: ${style.width || 1920}
PlayResY: ${style.height || 1080}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,${style.fontName || 'Microsoft YaHei'},${style.fontSize || 18},${style.primaryAss || '&H00FFFFFF'},&H00000000,${style.outlineCol || '&H00000000'},${style.backAss || '&H00000000'},${style.bold || 0},0,0,0,100,100,0,0,${style.borderStyle || 1},${style.outlineWidth || 1},${style.shadowVal || 0},2,60,60,${style.marginV || 18},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
`;

  const dialogues = [];
  for (const b of blocks) {
    const parts = b.timeLine.split('-->');
    if (parts.length !== 2) continue;
    const start = srtTimeToAss(parts[0].trim());
    const end = srtTimeToAss(parts[1].trim());
    // 强制单行：合并所有换行
    const text = b.text.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
    if (!text) continue;
    dialogues.push(`Dialogue: 0,${start},${end},Default,,0,0,0,,${text}`);
  }

  fs.writeFileSync(assPath, '\ufeff' + header + dialogues.join('\n') + '\n', 'utf-8');
}

/**
 * @param {object} [options]
 * @param {object} [options.cfg] 内存中的配置（与 wav-durations.json 同结构）；若提供则不再读 wav-durations.json
 */
async function run(projectRoot, skillDir, options = {}) {
  void skillDir;
  // Pipeline output lands in root; fallback to slides/ for backward compat
  const htmlRoot = path.join(projectRoot, 'presentation.html');
  const htmlSlides = resolvePath(projectRoot, 'slides', 'presentation.html');
  const HTML_FILE = fs.existsSync(htmlRoot) ? htmlRoot : htmlSlides;
  const CONFIG_FILE = resolvePath(projectRoot, 'timing', 'wav-durations.json');
  const TEMP_DIR = path.join(projectRoot, 'tmp');

  let cfg = options.cfg;
  if (!cfg) {
    if (!fs.existsSync(CONFIG_FILE)) {
      throw new Error(
        `缺少 wav-durations.json。或使用: node cli.js wav-auto --project <dir> 自动生成。`
      );
    }
    cfg = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
  }
  const wavName = cfg.wavFile || 'audio.wav';
  const WAV_FILE = path.isAbsolute(wavName)
    ? wavName
    : path.join(projectRoot, wavName);
  const slideDurations = cfg.slideDurationsSec;
  const outFile = cfg.outputFile || 'final_from_wav.mp4';
  const OUTPUT = path.isAbsolute(outFile)
    ? outFile
    : path.join(projectRoot, outFile);

  if (!Array.isArray(slideDurations) || slideDurations.length < 1) {
    throw new Error('wav-durations.json 中 slideDurationsSec 须为非空数组');
  }

  if (!fs.existsSync(WAV_FILE)) {
    throw new Error(`找不到 WAV 文件：${WAV_FILE}`);
  }
  if (!fs.existsSync(HTML_FILE)) {
    throw new Error(`找不到 presentation.html：${HTML_FILE}`);
  }

  console.log('\n╔══════════════════════════════════════════╗');
  console.log('║  HTML 幻灯 + WAV → MP4 (one-context skill) ║');
  console.log('╚══════════════════════════════════════════╝\n');
  console.log(`   项目目录: ${projectRoot}`);
  console.log(`   WAV: ${path.basename(WAV_FILE)}\n`);

  if (fs.existsSync(TEMP_DIR)) fs.rmSync(TEMP_DIR, { recursive: true, force: true });
  fs.mkdirSync(TEMP_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();
  await page.goto(pathToFileURL(HTML_FILE).href);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  // Ensure go() is exposed globally for templates that define it inside IIFE
  await page.addScriptTag({
    content: `
      (function() {
        if (typeof go === 'function' && typeof window.go !== 'function') {
          window.go = go;
        }
      })();
    `
  });
  await page.waitForTimeout(300);

  const numSlides = await page.evaluate(
    () => document.querySelectorAll('.s.slide').length
  );
  if (slideDurations.length !== numSlides) {
    await browser.close();
    throw new Error(
      `slideDurationsSec 长度 (${slideDurations.length}) 与 HTML 中 .slide 数量 (${numSlides}) 不一致`
    );
  }

  const wavDur = getMediaDuration(WAV_FILE);
  const sumDur = slideDurations.reduce((a, b) => a + b, 0);
  const scale = sumDur > 0 && Math.abs(wavDur - sumDur) > 0.05 ? wavDur / sumDur : 1;
  const scaled = slideDurations.map((d) => d * scale);

  if (scale !== 1) {
    console.log(
      `ℹ️  WAV 时长 ${wavDur.toFixed(2)}s 与配置之和 ${sumDur.toFixed(2)}s 不一致，已按比例缩放（×${scale.toFixed(4)}）。\n`
    );
  }

  const slideData = [];
  let cum = 0;

  for (let i = 0; i < numSlides; i++) {
    await page.evaluate((n) => {
      // 核心修复：直接修改 style.display 强制 Chromium headless 重排/重绘。
      // 纯 classList.toggle 在 headless 模式下不会触发合成器更新帧缓冲，
      // 导致所有截图都返回第一帧。
      const slides = document.querySelectorAll('.s.slide');
      slides.forEach((s, idx) => {
        if (idx === n) {
          s.style.display = 'flex';
          s.style.flexDirection = 'column';
          s.classList.add('is-active');
        } else {
          s.style.display = 'none';
          s.classList.remove('is-active');
        }
      });
      // 同步页面内部状态（页码、进度条等副作用）
      if (typeof go === 'function') go(n);
      else if (typeof goTo === 'function') goTo(n);
    }, i);
    await page.waitForTimeout(900);

    const imgPath = path.join(TEMP_DIR, `slide_${String(i).padStart(2, '0')}.png`);
    await page.screenshot({ path: imgPath });

    const dur = scaled[i];
    const audioSeg = path.join(TEMP_DIR, `slide_${String(i).padStart(2, '0')}.wav`);
    ff(
      `-y -ss ${cum.toFixed(3)} -i "${WAV_FILE}" -t ${dur.toFixed(3)} -c copy "${audioSeg}"`
    );
    cum += dur;

    slideData.push({ imgPath, audioSeg, duration: dur });
  }

  await browser.close();
  console.log('✅ 截图与 WAV 切片完成\n');

  for (let i = 0; i < slideData.length; i++) {
    const s = slideData[i];
    const videoPath = path.join(TEMP_DIR, `part_${String(i).padStart(2, '0')}.mp4`);
    ff(
      `-y -loop 1 -framerate ${FPS} -i "${s.imgPath}" -i "${s.audioSeg}" ` +
        `-c:v libx264 -preset ${VIDEO_PRESET} -b:v ${VIDEO_BITRATE} -maxrate 10M -bufsize 16M -pix_fmt yuv420p ` +
        `-vf "scale=1920:1080" ` +
        `-c:a aac -b:a 192k -shortest "${videoPath}"`
    );
    slideData[i].videoPath = videoPath;
    process.stdout.write(`  片段 ${i + 1}/${slideData.length} ✓\r`);
  }
  console.log('\n');

  const concatList = path.join(TEMP_DIR, 'concat.txt');
  fs.writeFileSync(
    concatList,
    slideData
      .map((s) => `file '${s.videoPath.replace(/\\/g, '/').replace(/'/g, "'\\''")}'`)
      .join('\n'),
    'utf-8'
  );

  const mergedPath = path.join(TEMP_DIR, 'merged.mp4');
  ff(`-y -f concat -safe 0 -i "${concatList}" -c copy "${mergedPath}"`);
  console.log('✅ 拼接完成\n');

  // 字幕烧录
  if (cfg.burnSubtitles) {
    const srtName = cfg.srtFile || 'subtitles.srt';
    const srtAbs = path.isAbsolute(srtName) ? srtName : path.join(projectRoot, srtName);
    if (!fs.existsSync(srtAbs)) {
      throw new Error(`字幕文件不存在: ${srtAbs}`);
    }
    const subCfg = cfg.subtitle || {};
    const fontSize = subCfg.fontSize ?? DEFAULT_SUBTITLE_STYLE.fontSize;
    const marginV = subCfg.marginV ?? DEFAULT_SUBTITLE_STYLE.marginV;
    const fontName = subCfg.fontName || 'Microsoft YaHei';
    const bold = subCfg.bold !== false ? 1 : 0;
    const srtReplacements = cfg.srtReplacements || [];
    const wrapSubtitles = cfg.wrapSubtitles !== false;
    const primaryAss = hexToAssPrimaryColour(
      subCfg.primaryColour ?? DEFAULT_SUBTITLE_STYLE.primaryColour,
      subCfg.primaryAlpha ?? DEFAULT_SUBTITLE_STYLE.primaryAlpha
    );
    const outlineWidth =
      typeof subCfg.outline === 'number' ? subCfg.outline : (DEFAULT_SUBTITLE_STYLE.outline ?? 0);
    const borderStyle =
      typeof subCfg.borderStyle === 'number' ? subCfg.borderStyle : 1;
    const backAlpha =
      typeof subCfg.backAlpha === 'number' ? subCfg.backAlpha : 255;
    const backAss = subCfg.backColour != null
      ? hexToAssWithAlpha(subCfg.backColour, backAlpha)
      : hexToAssWithAlpha('#000000', backAlpha);
    const outlineCol = borderStyle === 3 ? '&HFF000000' : '&H00000000';
    const shadowVal = typeof subCfg.shadow === 'number' ? subCfg.shadow : 0;
    const barHeight =
      typeof subCfg.barHeight === 'number'
        ? subCfg.barHeight
        : (DEFAULT_SUBTITLE_STYLE.barHeight ?? 60);
    const barAlpha =
      typeof subCfg.barAlpha === 'number'
        ? subCfg.barAlpha
        : (DEFAULT_SUBTITLE_STYLE.barAlpha ?? 0.55);

    let srtForBurn = srtAbs;
    if (wrapSubtitles || srtReplacements.length > 0) {
      const tmpSrt = path.join(TEMP_DIR, 'sub_for_burn.srt');
      prepareSrtForBurn(srtAbs, tmpSrt, {
        charsPerLine: subCfg.charsPerLine > 0 ? subCfg.charsPerLine : undefined,
        fontSize,
        replacements: srtReplacements,
        wrap: wrapSubtitles,
      });
      srtForBurn = tmpSrt;
      const effLine =
        subCfg.charsPerLine > 0
          ? subCfg.charsPerLine
          : suggestCharsPerLine(fontSize);
      console.log(
        `📝 字幕预处理: ${wrapSubtitles ? `每行≤${effLine} 字` : '不换行'}${srtReplacements.length ? `；${srtReplacements.length} 组替换` : ''}`
      );
    }

    // SRT → ASS（ass filter 对 MarginV 支持更标准）
    const assPath = path.join(TEMP_DIR, 'sub_for_burn.ass');
    generateAssFromSrt(srtForBurn, assPath, {
      width: 1920,
      height: 1080,
      fontSize,
      fontName,
      bold,
      primaryAss,
      outlineCol,
      backAss,
      outlineWidth,
      shadowVal,
      borderStyle,
      marginV,
    });
    const assFilter = assPath
      .replace(/\\/g, '/')
      .replace(/^([A-Za-z]):/, (_, d) => `${d}\\:`);

    const alphaHex = Math.max(0, Math.min(255, Math.round((1 - barAlpha) * 255)))
      .toString(16)
      .padStart(2, '0');
    const drawBox =
      barHeight > 0
        ? `format=rgba,drawbox=y=ih-${barHeight}:color=#000000${alphaHex}:width=iw:height=${barHeight}:t=fill,format=yuv420p,`
        : '';

    console.log('📝 烧录字幕...');
    ff(
      `-y -i "${mergedPath}" ` +
      `-vf "${drawBox}ass='${assFilter}'" ` +
      `-c:a copy "${OUTPUT}"`
    );
    console.log('✅ 字幕烧录完成');
  } else {
    fs.copyFileSync(mergedPath, OUTPUT);
  }

  console.log(`\n🎉 完成：${OUTPUT}`);
  console.log(`💡 中间文件: ${TEMP_DIR}\n`);
}

module.exports = { run };
