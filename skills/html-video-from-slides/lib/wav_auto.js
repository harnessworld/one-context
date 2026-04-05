'use strict';

/**
 * 仅 presentation.html + 单个 WAV → 自动对齐 → MP4
 * 依赖: pip install faster-whisper；系统 PATH 有 ffmpeg（或设 FFMPEG_PATH）
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { chromium } = require('playwright');
const { pathToFileURL } = require('url');
const ffmpegStatic = require('ffmpeg-static');
const { run: runWav } = require('./wav_pipeline');

async function extractSlideTexts(projectRoot) {
  const html = path.join(projectRoot, 'presentation.html');
  if (!fs.existsSync(html)) {
    throw new Error(`找不到 presentation.html：${html}`);
  }
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();
  await page.goto(pathToFileURL(html).href);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000);
  const texts = await page.evaluate(() =>
    Array.from(document.querySelectorAll('.slide')).map((s) =>
      (s.innerText || '').replace(/\r/g, '\n').trim()
    )
  );
  await browser.close();
  if (texts.length === 0) {
    throw new Error('HTML 中未找到 .slide');
  }
  return texts;
}

function findWavPath(projectRoot, explicit) {
  if (explicit) {
    const p = path.isAbsolute(explicit)
      ? explicit
      : path.join(projectRoot, explicit);
    if (!fs.existsSync(p)) throw new Error(`找不到 WAV：${p}`);
    return p;
  }
  const files = fs
    .readdirSync(projectRoot)
    .filter((f) => f.toLowerCase().endsWith('.wav'));
  if (files.length === 0) {
    throw new Error(
      '目录内没有 .wav。请放入单个口播文件，或使用 video-input.json 指定 wavFile。'
    );
  }
  if (files.length > 1) {
    throw new Error(
      `目录内有多个 .wav：${files.join(', ')}。请只保留一个，或创建 video-input.json 指定 wavFile。`
    );
  }
  return path.join(projectRoot, files[0]);
}

async function run(projectRoot, skillDir, options = {}) {
  const forceWhisperSrt = options.forceWhisperSrt === true;
  const inputPath = path.join(projectRoot, 'video-input.json');
  let wavExplicit = null;
  let whisperModel = 'medium';
  let outputFile = 'final_auto.mp4';
  let burnSubtitles = false;
  let subtitleCfg = {};
  let externalSrt = null; // 用户提供的已审校 SRT（跳过 Whisper SRT 输出）

  if (fs.existsSync(inputPath)) {
    const j = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
    wavExplicit = j.wavFile || null;
    whisperModel = j.whisperModel || whisperModel;
    outputFile = j.outputFile || outputFile;
    burnSubtitles = j.burnSubtitles === true;
    subtitleCfg = j.subtitle || {};
    if (j.srtFile && !forceWhisperSrt) {
      // 用户提供的已审校 SRT，优先使用（时间轴可能与当前 WAV 不一致）
      externalSrt = path.isAbsolute(j.srtFile) ? j.srtFile : path.join(projectRoot, j.srtFile);
      if (!fs.existsSync(externalSrt)) {
        throw new Error(`指定的 srtFile 不存在：${externalSrt}`);
      }
    } else if (j.srtFile && forceWhisperSrt) {
      console.log(
        'ℹ️  已加 --whisper-srt：忽略 video-input.json 的 srtFile，将用 Whisper 重新生成与口播对齐的 sub.srt\n'
      );
    }
  }

  const wavAbs = findWavPath(projectRoot, wavExplicit);
  const wavRel = path.basename(wavAbs);

  console.log('\n╔══════════════════════════════════════════╗');
  console.log('║  wav-auto：HTML + WAV → 自动对齐 → MP4   ║');
  console.log('╚══════════════════════════════════════════╝\n');
  console.log(`   项目: ${projectRoot}`);
  console.log(`   WAV:  ${wavRel}`);
  console.log(`   Whisper 模型: ${whisperModel}`);
  console.log(`   烧录字幕: ${burnSubtitles ? '✅' : '❌'}\n`);

  const slides = await extractSlideTexts(projectRoot);
  console.log(`✅ 从 HTML 提取 ${slides.length} 页文案（用于与口播对齐）\n`);

  const cacheDir = path.join(skillDir, '.cache');
  fs.mkdirSync(cacheDir, { recursive: true });
  const stamp = Date.now();
  const slidesJson = path.join(cacheDir, `slides_${stamp}.json`);
  const alignOut = path.join(cacheDir, `align_${stamp}.json`);
  const srtOut = path.join(cacheDir, `whisper_${stamp}.srt`);
  fs.writeFileSync(
    slidesJson,
    JSON.stringify({ slides }, null, 0),
    'utf-8'
  );

  const py = path.join(skillDir, 'align_wav_slides.py');
  const env = { ...process.env };
  if (ffmpegStatic) {
    env.FFMPEG_PATH = ffmpegStatic;
  }
  // 禁用 Xet Storage 写入（写入不稳定易导致 bin 文件损坏），优先走 hf-mirror.com
  env.HF_ENDPOINT = 'https://hf-mirror.com';
  env.HF_HUB_DISABLE_XET = '1';

  const pythonExe = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
  const r = spawnSync(
    pythonExe,
    [
      py,
      '--wav',
      wavAbs,
      '--slides-json',
      slidesJson,
      '--out-json',
      alignOut,
      '--model',
      whisperModel,
      // 只有需要烧字幕且用户没提供外部 SRT 时，才让 Whisper 输出 SRT
      ...(burnSubtitles && !externalSrt ? ['--srt-out', srtOut] : []),
    ],
    { encoding: 'utf-8', env, maxBuffer: 50 * 1024 * 1024 }
  );

  if (r.status !== 0) {
    console.error(r.stderr || r.stdout);
    throw new Error(
      'align_wav_slides.py 失败。请确认已执行: pip install faster-whisper huggingface_hub（可选 opencc-python-reimplemented 用于简体字幕）'
    );
  }

  const aligned = JSON.parse(fs.readFileSync(alignOut, 'utf-8'));
  if (aligned.warnings && aligned.warnings.length) {
    aligned.warnings.forEach((w) => console.warn('⚠️ ', w));
  }
  console.log(`\n✅ 对齐方式: ${aligned.method || 'unknown'}`);
  console.log(
    `   slideDurationsSec: [${(aligned.slideDurationsSec || [])
      .map((x) => x.toFixed(2))
      .join(', ')}]\n`
  );

  const cfg = {
    wavFile: wavRel,
    slideDurationsSec: aligned.slideDurationsSec,
    outputFile,
    burnSubtitles,
    // 优先用用户提供的已审校 SRT，否则用 Whisper 生成的
    srtFile: externalSrt || (burnSubtitles ? srtOut : undefined),
    subtitle: subtitleCfg,
  };

  await runWav(projectRoot, skillDir, { cfg });

  // 无外部 srtFile 时，把 Whisper 生成的 SRT 拷到项目根，便于只改文案、保留时间轴
  if (burnSubtitles && !externalSrt && fs.existsSync(srtOut)) {
    const dest = path.join(projectRoot, 'sub.srt');
    try {
      fs.copyFileSync(srtOut, dest);
      console.log(`\n📄 已写入对齐用字幕（与口播同源时间轴）：${dest}\n`);
    } catch (e) {
      console.warn('⚠️  未能复制 Whisper SRT 到项目目录：', e.message);
    }
  }

  try {
    fs.unlinkSync(slidesJson);
    fs.unlinkSync(alignOut);
  } catch (_) {
    /* ignore */
  }
}

module.exports = { run };
