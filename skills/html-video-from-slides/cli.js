#!/usr/bin/env node
'use strict';

/**
 * 单入口：不复制到各视频项目；在素材目录执行，或传 --project。
 *
 *   node cli.js tts [--project <dir>]
 *   node cli.js wav [--project <dir>]
 *   node cli.js wav-auto [--project <dir>]   # 仅 HTML + 单个 WAV，自动对齐（需 faster-whisper）
 */

const path = require('path');
const { run: runTts } = require('./lib/tts_pipeline');
const { run: runWav } = require('./lib/wav_pipeline');
const { run: runWavAuto } = require('./lib/wav_auto');

function parseArgs() {
  const argv = process.argv.slice(2);
  const forceWhisperSrt = argv.includes('--whisper-srt');
  const rest = argv.filter((x) => x !== '--whisper-srt');
  let project = process.cwd();
  const pi = rest.indexOf('--project');
  if (pi >= 0 && rest[pi + 1]) {
    project = path.resolve(rest[pi + 1]);
    const next = rest.slice();
    next.splice(pi, 2);
    return { cmd: next[0], project, forceWhisperSrt };
  }
  return { cmd: rest[0], project, forceWhisperSrt };
}

function usage() {
  console.log(`
html-video-from-slides（one-context 内置技能）

用法:
  node "${path.join(__dirname, 'cli.js')}" tts [--project <素材目录>]
  node "${path.join(__dirname, 'cli.js')}" wav [--project <素材目录>]
  node "${path.join(__dirname, 'cli.js')}" wav-auto [--project <素材目录>] [--whisper-srt]

  tts      presentation.html、讲稿.md、可选 config.json
  wav      presentation.html、wav-durations.json、.wav
  wav-auto presentation.html、目录内单个 .wav（可选 video-input.json）
           video-input 可选：whisperModel、vadFilter（默认 false）、strictSubtitles、maxSubtitleGapSec
           --whisper-srt  忽略 video-input.json 里的 srtFile，强制用 Whisper
                          转写生成与口播同源时间轴的 sub.srt（解决字幕与语音不对齐）

  --project  含上述文件的目录；默认当前工作目录。

依赖:
  cd skills/html-video-from-slides && npm install && npx playwright install chromium
  pip install edge-tts
  pip install faster-whisper   # 仅 wav-auto；首次会下载模型

下载失败时先在当前终端设置 HTTPS_PROXY/HTTP_PROXY（与仓库 README 代理说明一致），见 SKILL.md。
`);
}

async function main() {
  const { cmd, project, forceWhisperSrt } = parseArgs();
  if (cmd !== 'tts' && cmd !== 'wav' && cmd !== 'wav-auto') {
    usage();
    process.exit(cmd ? 1 : 0);
  }

  const skillDir = path.join(__dirname);
  if (cmd === 'tts') await runTts(project, skillDir);
  else if (cmd === 'wav') await runWav(project, skillDir);
  else await runWavAuto(project, skillDir, { forceWhisperSrt });
}

main().catch((err) => {
  console.error('\n❌', err.message || err);
  process.exit(1);
});
