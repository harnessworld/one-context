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

/**
 * @param {object} [options]
 * @param {object} [options.cfg] 内存中的配置（与 wav-durations.json 同结构）；若提供则不再读 wav-durations.json
 */
async function run(projectRoot, skillDir, options = {}) {
  void skillDir;
  const HTML_FILE = path.join(projectRoot, 'presentation.html');
  const CONFIG_FILE = path.join(projectRoot, 'wav-durations.json');
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

  const numSlides = await page.evaluate(
    () => document.querySelectorAll('.slide').length
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
    const fontSizeEff = fontSize;
    const primaryAss = hexToAssPrimaryColour(
      subCfg.primaryColour ?? DEFAULT_SUBTITLE_STYLE.primaryColour,
      subCfg.primaryAlpha ?? DEFAULT_SUBTITLE_STYLE.primaryAlpha
    );
    const outlineWidth =
      typeof subCfg.outline === 'number' ? subCfg.outline : 2;
    const borderStyle =
      typeof subCfg.borderStyle === 'number' ? subCfg.borderStyle : 1;
    const opaqueBar = borderStyle === 3;
    const backAlpha =
      typeof subCfg.backAlpha === 'number' ? subCfg.backAlpha : 255;
    const backAss =
      subCfg.backColour != null
        ? hexToAssWithAlpha(subCfg.backColour, backAlpha)
        : opaqueBar
          ? '&HFF000000'
          : '&H80000000';
    const outlineCol = opaqueBar ? '&HFF000000' : '&H00000000';
    const shadowVal = opaqueBar ? 0 : 1;

    let srtForBurn = srtAbs;
    if (wrapSubtitles || srtReplacements.length > 0) {
      const tmpSrt = path.join(TEMP_DIR, 'sub_for_burn.srt');
      prepareSrtForBurn(srtAbs, tmpSrt, {
        charsPerLine: subCfg.charsPerLine > 0 ? subCfg.charsPerLine : undefined,
        fontSize: fontSizeEff,
        replacements: srtReplacements,
        wrap: wrapSubtitles,
      });
      srtForBurn = tmpSrt;
      const effLine =
        subCfg.charsPerLine > 0
          ? subCfg.charsPerLine
          : suggestCharsPerLine(fontSizeEff);
      console.log(
        `📝 字幕预处理: ${wrapSubtitles ? `每行≤${effLine} 字` : '不换行'}${srtReplacements.length ? `；${srtReplacements.length} 组替换` : ''}`
      );
    }

    const srtFilter = srtForBurn
      .replace(/\\/g, '/')
      .replace(/^([A-Za-z]):/, (_, d) => `${d}\\:`);

    console.log('📝 烧录字幕...');
    ff(
      `-y -i "${mergedPath}" ` +
      `-vf "subtitles='${srtFilter}':charenc=UTF-8:force_style='` +
      `FontName=${fontName},` +
      `FontSize=${fontSize},` +
      `PrimaryColour=${primaryAss},` +
      `OutlineColour=${outlineCol},` +
      `BackColour=${backAss},` +
      `Bold=${bold},` +
      `BorderStyle=${borderStyle},` +
      `Outline=${outlineWidth},` +
      `Shadow=${shadowVal},` +
      `Alignment=2,MarginV=${marginV},WrapStyle=0,MarginL=120,MarginR=120` +
      `'" ` +
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
