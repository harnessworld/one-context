#!/usr/bin/env node
'use strict';

/**
 * 单入口：不复制到各视频项目；在素材目录执行，或传 --project。
 *
 *   node cli.js tts [--project <dir>]
 *   node cli.js wav [--project <dir>]
 *   node cli.js wav-auto [--project <dir>]   # 仅 HTML + 单个 WAV，自动对齐（需 faster-whisper）
 *   node cli.js srt-map [--project <dir>]    # SRT→Slide 映射（Whisper 对齐失败时用）
 *   node cli.js timing-check [--project <dir>] [--json] [--audit-cue-starts]
 *   node cli.js cover [--project <dir>]       # 封面截图
 */

const path = require('path');
const { run: runTts } = require('./lib/tts_pipeline');
const { run: runWav } = require('./lib/wav_pipeline');
const { run: runWavAuto } = require('./lib/wav_auto');
const { run: runSrtMap } = require('./lib/srt_map');
const { run: runCover } = require('./lib/cover_gen');
const {
  runProjectTimingCheck,
  printReport: printTimingReport,
} = require('./lib/timing_boundary_check');

function parseArgs() {
  const argv = process.argv.slice(2);
  const forceWhisperSrt = argv.includes('--whisper-srt');
  const horizontal = argv.includes('--horizontal');
  const skipTimingCheck = argv.includes('--skip-timing-check');
  const timingCheckJson = argv.includes('--json');
  const auditCueStarts = argv.includes('--audit-cue-starts');
  const rest = argv.filter(
    (x) =>
      x !== '--whisper-srt' &&
      x !== '--horizontal' &&
      x !== '--skip-timing-check' &&
      x !== '--json' &&
      x !== '--audit-cue-starts'
  );
  let project = process.cwd();
  let boundaries = '';
  const pi = rest.indexOf('--project');
  if (pi >= 0 && rest[pi + 1]) {
    project = path.resolve(rest[pi + 1]);
    rest.splice(pi, 2);
  }
  const bi = rest.indexOf('--boundaries');
  if (bi >= 0 && rest[bi + 1]) {
    boundaries = rest[bi + 1];
    rest.splice(bi, 2);
  }
  return {
    cmd: rest[0],
    project,
    forceWhisperSrt,
    horizontal,
    boundaries,
    skipTimingCheck,
    timingCheckJson,
    auditCueStarts,
  };
}

function usage() {
  console.log(`
html-video-from-slides（one-context 内置技能）

用法:
  node "${path.join(__dirname, 'cli.js')}" tts [--project <素材目录>]
  node "${path.join(__dirname, 'cli.js')}" wav [--project <素材目录>]
  node "${path.join(__dirname, 'cli.js')}" wav-auto [--project <素材目录>] [--whisper-srt]
  node "${path.join(__dirname, 'cli.js')}" srt-map [--project <素材目录>] [--boundaries <映射>]
  node "${path.join(__dirname, 'cli.js')}" timing-check [--project <素材目录>] [--json]
  node "${path.join(__dirname, 'cli.js')}" cover [--project <素材目录>] [--horizontal]

  tts       presentation.html、讲稿.md、可选 config.json
  wav       presentation.html、wav-durations.json、.wav（默认先做 timing-check；--skip-timing-check 跳过）
  wav-auto  presentation.html、目录内单个 .wav（可选 video-input.json）
            video-input 可选：whisperModel、vadFilter（默认 false）、strictSubtitles、maxSubtitleGapSec
            --whisper-srt  忽略 video-input.json 里的 srtFile，强制用 Whisper
                           转写生成与口播同源时间轴的 sub.srt
  srt-map   解析 sub.srt + presentation.html，输出 SRT 条目与幻灯片对照表
            --boundaries  "0:0-0,1:1-2,2:3-5,..."  生成 wav-durations.json
  timing-check  默认只报「下一页 .wa 句起点」高危对齐；--audit-cue-starts 列出全部「翻页≈字幕起点」
            --json    输出 JSON（退出码 2 表示存在高危 WARN）
  cover     截图 cover.html → videos/cover.png (1080×1920)
            --horizontal  截图 cover_h.html → videos/cover_h.png (1440×1080)

  --project  含上述文件的目录；默认当前工作目录。

依赖:
  cd skills/html-video-from-slides && npm install && npx playwright install chromium
  pip install edge-tts
  pip install faster-whisper   # 仅 wav-auto；首次会下载模型

下载失败时先在当前终端设置 HTTPS_PROXY/HTTP_PROXY（与仓库 README 代理说明一致），见 SKILL.md。
`);
}

async function main() {
  const {
    cmd,
    project,
    forceWhisperSrt,
    horizontal,
    boundaries,
    skipTimingCheck,
    timingCheckJson,
    auditCueStarts,
  } = parseArgs();
  if (
    cmd !== 'tts' &&
    cmd !== 'wav' &&
    cmd !== 'wav-auto' &&
    cmd !== 'srt-map' &&
    cmd !== 'timing-check' &&
    cmd !== 'cover'
  ) {
    usage();
    process.exit(cmd ? 1 : 0);
  }

  const skillDir = path.join(__dirname);
  if (cmd === 'tts') await runTts(project, skillDir);
  else if (cmd === 'wav')
    await runWav(project, skillDir, { skipTimingCheck });
  else if (cmd === 'wav-auto') await runWavAuto(project, skillDir, { forceWhisperSrt });
  else if (cmd === 'srt-map') runSrtMap(project, { boundaries });
  else if (cmd === 'timing-check') {
    const r = runProjectTimingCheck(project, { auditCueStarts });
    printTimingReport(r, timingCheckJson);
    if (!r.skipped && r.warnings && r.warnings.length) process.exitCode = 2;
  } else if (cmd === 'cover') await runCover(project, { horizontal });
}

main().catch((err) => {
  console.error('\n❌', err.message || err);
  process.exit(1);
});
