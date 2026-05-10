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
const { prepareSrtForBurn } = require('./srt_postprocess');
const { resolvePath, ensureDir } = require('./path_resolver');
const { DEFAULT_SUBTITLE_STYLE } = require('./ass_colours');

/** 1080p 成片烧录：过小字号手机端不可读；可被 subtitle.allowBelowRecommendedFontSize 关闭钳制 */
const MIN_RECOMMENDED_BURN_FONT_PX = 42;

async function extractSlideTexts(projectRoot) {
  const html = resolvePath(projectRoot, 'slides', 'presentation.html');
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
  const result = await page.evaluate(() => {
    const primary = document.querySelectorAll('#P > .slide, .deck > .slide');
    const slides =
      primary.length > 0
        ? primary
        : document.querySelectorAll('.s.slide, section.slide');
    return Array.from(slides).map((s) => {
      const wa = s.querySelector('.wa');
      const anchor = wa ? (wa.textContent || '').replace(/\r/g, '\n').trim() : '';
      const full = (s.innerText || '').replace(/\r/g, '\n').trim();
      return { anchor, full };
    });
  });
  await browser.close();
  if (result.length === 0) {
    throw new Error('HTML 中未找到 slide 元素');
  }
  // slides 数组：优先用 .wa 锚文字（更短、更贴近口播），无则用整页 innerText
  const slides = result.map((r) => r.anchor || r.full);
  const anchors = result.map((r) => !!r.anchor);
  return { slides, anchors };
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
  const inputPath = resolvePath(projectRoot, 'timing', 'video-input.json');
  let wavExplicit = null;
  let whisperModel = 'medium';
  let outputFile = 'final_auto.mp4';
  let burnSubtitles = false;
  let subtitleCfg = {};
  let externalSrt = null; // 用户提供的已审校 SRT（跳过 Whisper SRT 输出）
  let vadFilter = false; // 默认关闭：与 align_wav_slides.py 一致，减少片头/轻声被裁导致的字幕大段空白
  let strictSubtitles = false;
  let maxSubtitleGapSec = 2.5;
  /** @type {string | null} null = 不传参，Python 用 skill 默认 0.85 */
  let noSpeechThresholdArg = null;
  let fillSrtGaps = true;
  let whisperHotwords = '';
  /** @type {unknown[]} */
  let srtReplacements = [];
  let wrapSubtitles = true;

  if (fs.existsSync(inputPath)) {
    const j = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
    wavExplicit = j.wavFile || null;
    whisperModel = j.whisperModel || whisperModel;
    outputFile = j.outputFile || outputFile;
    burnSubtitles = j.burnSubtitles === true;
    subtitleCfg = j.subtitle || {};
    if (j.vadFilter === true) vadFilter = true;
    if (j.strictSubtitles === true) strictSubtitles = true;
    if (typeof j.maxSubtitleGapSec === 'number' && j.maxSubtitleGapSec > 0) {
      maxSubtitleGapSec = j.maxSubtitleGapSec;
    }
    if (j.noSpeechThreshold === null) {
      noSpeechThresholdArg = 'none';
    } else if (typeof j.noSpeechThreshold === 'number') {
      noSpeechThresholdArg = String(j.noSpeechThreshold);
    }
    if (j.fillSrtGaps === false) {
      fillSrtGaps = false;
    }
    if (typeof j.whisperHotwords === 'string') {
      whisperHotwords = j.whisperHotwords;
    }
    if (Array.isArray(j.srtReplacements)) {
      srtReplacements = j.srtReplacements;
    }
    if (j.wrapSubtitles === false) {
      wrapSubtitles = false;
    }
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

  // 先叠 skill 默认字幕（避免 video-input 只写 partial 时落到错误的硬编码小字号），再叠 timing/wav-durations.json 里的 subtitle（管线预先写好时可固定成片样式）
  subtitleCfg = { ...DEFAULT_SUBTITLE_STYLE, ...subtitleCfg };
  const wdPath = resolvePath(projectRoot, 'timing', 'wav-durations.json');
  if (fs.existsSync(wdPath)) {
    try {
      const wd = JSON.parse(fs.readFileSync(wdPath, 'utf-8'));
      if (wd.subtitle && typeof wd.subtitle === 'object') {
        subtitleCfg = { ...subtitleCfg, ...wd.subtitle };
      }
    } catch (_) {
      /* ignore */
    }
  }

  if (
    typeof subtitleCfg.fontSize === 'number' &&
    subtitleCfg.fontSize > 0 &&
    subtitleCfg.fontSize < MIN_RECOMMENDED_BURN_FONT_PX &&
    subtitleCfg.allowBelowRecommendedFontSize !== true
  ) {
    console.warn(
      `ℹ️  subtitle.fontSize=${subtitleCfg.fontSize} 低于 1080p 成片推荐下限 ${MIN_RECOMMENDED_BURN_FONT_PX}px，已提升到 ${MIN_RECOMMENDED_BURN_FONT_PX}（设置 subtitle.allowBelowRecommendedFontSize=true 可保留小字号）`
    );
    subtitleCfg.fontSize = MIN_RECOMMENDED_BURN_FONT_PX;
  }

  const wavAbs = path.resolve(findWavPath(projectRoot, wavExplicit));
  const wavRel = path.basename(wavAbs);

  console.log('\n╔══════════════════════════════════════════╗');
  console.log('║  wav-auto：HTML + WAV → 自动对齐 → MP4   ║');
  console.log('╚══════════════════════════════════════════╝\n');
  console.log(`   项目: ${projectRoot}`);
  console.log(`   WAV:  ${wavRel}`);
  console.log(`   Whisper 模型: ${whisperModel}`);
  console.log(`   烧录字幕: ${burnSubtitles ? '✅' : '❌'}`);
  console.log(`   VAD 裁切: ${vadFilter ? '开启（可能丢轻声/片头）' : '关闭（默认，字幕更完整）'}`);
  console.log(
    `   字幕缺口: 超过 ${maxSubtitleGapSec}s 会告警${strictSubtitles ? '；strict 模式将中止成片' : ''}`
  );
  if (noSpeechThresholdArg !== null) {
    console.log(
      `   no_speech 阈值: ${noSpeechThresholdArg === 'none' ? '关闭（不传 no_speech_threshold）' : noSpeechThresholdArg}（仅当 no_speech_prob 大于该值时跳过整段）\n`
    );
  } else {
    console.log(
      `   no_speech 阈值: 0.85（skill 默认；faster-whisper 库默认 0.6 易误跳过清晰人声，见 SKILL.md）\n`
    );
  }
  if (whisperHotwords) {
    console.log(`   Whisper hotwords: ${whisperHotwords.slice(0, 80)}${whisperHotwords.length > 80 ? '…' : ''}`);
  }
  if (srtReplacements.length) {
    console.log(`   烧录前字幕替换: ${srtReplacements.length} 组`);
  }
  const cpl = subtitleCfg.charsPerLine ?? 28;
  console.log(
    `   字幕样式: 字号 ${subtitleCfg.fontSize}px；折行: ${wrapSubtitles ? `每行≤${cpl} 字` : '关闭（整段一行）'}\n`
  );

  const { slides, anchors } = await extractSlideTexts(projectRoot);
  const anchorCount = anchors.filter(Boolean).length;
  console.log(`✅ 从 HTML 提取 ${slides.length} 页文案（${anchorCount} 页有 .wa 锚文字，${slides.length - anchorCount} 页用全文）\n`);

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

  const py = path.join(skillDir, 'scripts', 'align_wav_slides.py');
  const env = { ...process.env };
  if (ffmpegStatic) {
    env.FFMPEG_PATH = ffmpegStatic;
  }
  // 禁用 Xet Storage 写入（写入不稳定易导致 bin 文件损坏），优先走 hf-mirror.com
  env.HF_ENDPOINT = 'https://hf-mirror.com';
  env.HF_HUB_DISABLE_XET = '1';
  // Windows 控制台默认 GBK，align_wav_slides.py 含中文/emoji 的 print 会 UnicodeEncodeError
  env.PYTHONUTF8 = '1';

  const pythonExe = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
  const pyArgv = [
    py,
    '--wav',
    wavAbs,
    '--slides-json',
    slidesJson,
    '--out-json',
    alignOut,
    '--model',
    whisperModel,
    '--max-subtitle-gap-sec',
    String(maxSubtitleGapSec),
    ...(strictSubtitles ? ['--strict-subtitles'] : []),
    ...(vadFilter ? ['--vad-filter'] : []),
    ...(noSpeechThresholdArg !== null
      ? ['--no-speech-threshold', noSpeechThresholdArg]
      : []),
    ...(!fillSrtGaps ? ['--no-fill-srt-gaps'] : []),
    ...(whisperHotwords.trim()
      ? ['--hotwords', whisperHotwords.trim()]
      : []),
    // 与口播对齐的 SRT 始终生成（除非用户指定外部 srtFile），便于缺口检测；仅 burnSubtitles 时拷贝到项目根
    ...(!externalSrt ? ['--srt-out', srtOut] : []),
  ];
  const spawnOpts = { encoding: 'utf-8', env, maxBuffer: 50 * 1024 * 1024 };
  let r = spawnSync(pythonExe, pyArgv, spawnOpts);
  const outComb = `${r.stderr || ''}${r.stdout || ''}`;
  const pythonLaunchFailed =
    process.platform === 'win32' &&
    !process.env.PYTHON &&
    ((r.error &&
      (r.error.code === 'ENOENT' || r.error.errno === -4058)) ||
      r.status === 9009 ||
      /not recognized as an internal or external command|'python' was not found/i.test(outComb));
  if (pythonLaunchFailed) {
    r = spawnSync('py', ['-3', ...pyArgv], spawnOpts);
  }

  if (r.status !== 0) {
    console.error(r.stderr || r.stdout);
    if (r.status === 4) {
      throw new Error(
        'align_wav_slides.py：strict-subtitles 检测到超长无字幕区间，已中止。请编辑 sub.srt 补全缺口后重跑，或在 video-input.json 关闭 strictSubtitles / 调整 maxSubtitleGapSec。'
      );
    }
    throw new Error(
      'align_wav_slides.py 失败。请确认已执行: pip install faster-whisper huggingface_hub（可选 opencc-python-reimplemented 用于简体字幕）'
    );
  }

  const aligned = JSON.parse(fs.readFileSync(alignOut, 'utf-8'));
  if (aligned.warnings && aligned.warnings.length) {
    aligned.warnings.forEach((w) => console.warn('⚠️ ', w));
  }
  if (aligned.method === 'whisper_align_partial') {
    console.warn(
      '\n⚠️  幻灯与口播仅部分匹配（whisper_align_partial）。若成片翻页与讲解不同步：\n' +
        '   让每页 .slide 可见文字更贴近真实口播，或改用更大的 whisperModel，或改用 wav 模式手写 slideDurationsSec。\n'
    );
  }
  console.log(`\n✅ 对齐方式: ${aligned.method || 'unknown'}`);
  console.log(
    `   slideDurationsSec: [${(aligned.slideDurationsSec || [])
      .map((x) => x.toFixed(2))
      .join(', ')}]\n`
  );

  const cfg = {
    // 须传绝对路径：wavFile 指向 Downloads 等目录时 basename 在项目根不存在
    wavFile: wavAbs,
    slideDurationsSec: aligned.slideDurationsSec,
    outputFile,
    burnSubtitles,
    // 优先用用户提供的已审校 SRT，否则仅在 burn 时用 Whisper 生成的临时 SRT 烧录
    srtFile: externalSrt || (burnSubtitles ? srtOut : undefined),
    subtitle: subtitleCfg,
    srtReplacements,
    wrapSubtitles,
  };

  await runWav(projectRoot, skillDir, { cfg });

  const wdPersistPath = resolvePath(projectRoot, 'timing', 'wav-durations.json');
  ensureDir(wdPersistPath);
  const wavRelPersist =
    wavExplicit || path.relative(projectRoot, wavAbs).replace(/\\/g, '/');
  fs.writeFileSync(
    wdPersistPath,
    JSON.stringify(
      {
        wavFile: wavRelPersist,
        slideDurationsSec: aligned.slideDurationsSec,
        outputFile,
        burnSubtitles,
        ...(burnSubtitles ? { srtFile: 'subtitles/sub.srt' } : {}),
        subtitle: subtitleCfg,
      },
      null,
      2
    ) + '\n',
    'utf-8'
  );
  console.log(`\n📄 已更新 timing/wav-durations.json（与本次 wav-auto 对齐一致）\n`);

  // 无外部 srtFile 时，把 Whisper 生成的 SRT 拷到项目根，便于校对文案、保留时间轴（未 burn 也会复制供审阅）
  if (!externalSrt && fs.existsSync(srtOut)) {
    const dest = path.join(projectRoot, 'subtitles', 'sub.srt');
    ensureDir(dest);
    try {
      fs.copyFileSync(srtOut, dest);
      if (srtReplacements.length > 0 || wrapSubtitles) {
        prepareSrtForBurn(dest, dest, {
          charsPerLine:
            subtitleCfg.charsPerLine > 0 ? subtitleCfg.charsPerLine : undefined,
          fontSize:
            subtitleCfg.fontSize ?? DEFAULT_SUBTITLE_STYLE.fontSize,
          replacements: srtReplacements,
          wrap: wrapSubtitles,
        });
        console.log(
          '\n📄 已对项目 sub.srt 做与烧录相同的折行/替换，便于与成片对照改字。'
        );
      }
      console.log(
        `\n📄 已写入 ${burnSubtitles ? '对齐用字幕' : 'Whisper 初稿字幕'}：${dest}\n`
      );
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
