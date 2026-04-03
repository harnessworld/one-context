'use strict';

/**
 * presentation.html + 讲稿.md + Edge TTS → final.mp4
 * 临时文件：{projectRoot}/temp_video/
 */

const { chromium } = require('playwright');
const ffmpegPath = require('ffmpeg-static');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { pathToFileURL } = require('url');

function parseScript(md) {
  const blocks = md.split(/(?=^# 【)/m).filter((s) => s.trim());
  return blocks.map((block) => {
    const lines = block.split('\n');
    const header = lines[0].replace(/^# 【/, '').replace('】', '').trim();
    let start = 1;
    while (
      start < lines.length &&
      (lines[start].startsWith('时长：') || lines[start].trim() === '')
    ) {
      start++;
    }
    const contentLines = [];
    for (let i = start; i < lines.length; i++) {
      if (lines[i].trim() === '---') break;
      contentLines.push(lines[i]);
    }
    const text = contentLines
      .join('\n')
      .replace(/\*\*(.*?)\*\*/gs, '$1')
      .replace(/\*(.*?)\*/gs, '$1')
      .replace(/`+([^`]*)`+/g, '$1')
      .replace(/^#{1,6}\s*/gm, '')
      .replace(/^[-*]\s+/gm, '')
      .replace(/[①②③④⑤⑥⑦⑧⑨⑩]/g, '')
      .replace(/→/g, '，')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
    return { header, text };
  });
}

function getAudioDuration(mp3Path) {
  try {
    execSync(`"${ffmpegPath}" -i "${mp3Path}"`, { stdio: 'pipe' });
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
  return 10.0;
}

function generateSRT(slideData, outputPath, subtitleCfg) {
  const SUBTITLE_CHARS_PER_LINE = subtitleCfg.charsPerLine ?? 28;
  let srt = '';
  let idx = 1;
  let elapsed = 0;

  for (const slide of slideData) {
    const rawSentences = slide.text
      .replace(/\n+/g, '，')
      .split(/(?<=[。！？；，…])/u)
      .map((s) => s.trim())
      .filter((s) => s.length > 0);

    const chunks = [];
    for (const sent of rawSentences) {
      for (let i = 0; i < sent.length; i += SUBTITLE_CHARS_PER_LINE) {
        const chunk = sent.substring(i, i + SUBTITLE_CHARS_PER_LINE).trim();
        if (chunk) chunks.push(chunk);
      }
    }

    if (chunks.length === 0) {
      elapsed += slide.duration;
      continue;
    }

    const totalChars = chunks.reduce((s, c) => s + c.length, 0);
    let lineElapsed = elapsed;

    for (const chunk of chunks) {
      const lineDur = Math.max(0.8, (chunk.length / totalChars) * slide.duration);
      const lineEnd = Math.min(lineElapsed + lineDur, elapsed + slide.duration);

      srt += `${idx}\n`;
      srt += `${toSRTTime(lineElapsed)} --> ${toSRTTime(lineEnd)}\n`;
      srt += `${chunk}\n\n`;

      idx++;
      lineElapsed = lineEnd;
    }

    elapsed += slide.duration;
  }

  fs.writeFileSync(outputPath, '\ufeff' + srt, { encoding: 'utf-8' });
}

function toSRTTime(sec) {
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = Math.floor(sec % 60);
  const ms = Math.round((sec - Math.floor(sec)) * 1000);
  return `${p2(h)}:${p2(m)}:${p2(s)},${p3(ms)}`;
}
const p2 = (n) => String(n).padStart(2, '0');
const p3 = (n) => String(n).padStart(3, '0');

function ff(args, outputFile) {
  try {
    execSync(`"${ffmpegPath}" ${args}`, { stdio: 'pipe' });
  } catch (e) {
    if (outputFile && !fs.existsSync(outputFile)) {
      const stderr = (e.stderr || Buffer.alloc(0)).toString();
      throw new Error(`FFmpeg 失败 [${path.basename(outputFile)}]:\n${stderr.slice(-800)}`);
    }
  }
}

function generateAudio(text, outputPath, idx, voiceId, skillDir, tempDir, voiceCfg) {
  const TTS_HELPER = path.join(skillDir, 'tts_helper.py');
  const configFile = path.join(tempDir, `tts_cfg_${idx}.json`);
  fs.writeFileSync(
    configFile,
    JSON.stringify({
      text,
      voice: voiceId,
      rate: voiceCfg.rate ?? '+0%',
      pitch: voiceCfg.pitch ?? '+0Hz',
      volume: voiceCfg.volume ?? '+0%',
      output: outputPath,
    }),
    'utf-8'
  );
  try {
    execSync(`python "${TTS_HELPER}" "${configFile}"`, { stdio: 'pipe' });
  } catch (e) {
    const stderr = (e.stderr || Buffer.alloc(0)).toString();
    throw new Error(`TTS 失败 [slide ${idx}]:\n${stderr.slice(-500)}`);
  }
}

async function run(projectRoot, skillDir) {
  const CONFIG_FILE = path.join(projectRoot, 'config.json');
  const cfg = fs.existsSync(CONFIG_FILE)
    ? JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'))
    : {};

  const TEMP_DIR = path.join(projectRoot, 'temp_video');
  const HTML_FILE = path.join(projectRoot, cfg.input?.htmlFile ?? 'presentation.html');
  const SCRIPT_FILE = path.join(projectRoot, cfg.input?.scriptFile ?? '讲稿.md');
  const OUTPUT_MP4 = path.join(projectRoot, cfg.output?.file ?? 'final.mp4');
  const voiceCfg = cfg.voice ?? {};
  const VOICE_SINGLE = voiceCfg.name ?? 'zh-CN-YunxiNeural';
  const VOICE_MALE = voiceCfg.male ?? 'zh-CN-YunxiNeural';
  const VOICE_FEMALE = voiceCfg.female ?? 'zh-CN-XiaoxiaoNeural';
  const VOICE_START = voiceCfg.startWith === 'female' ? 'female' : 'male';
  const USE_VOICE_ALTERNATE =
    voiceCfg.mode === 'alternate' || voiceCfg.alternate === true;
  const FPS = cfg.video?.fps ?? 60;
  const VIDEO_BITRATE = cfg.video?.bitrate ?? '8M';
  const VIDEO_MAXRATE = cfg.video?.maxrate ?? '10M';
  const VIDEO_PRESET = cfg.video?.preset ?? 'slow';
  const SUBTITLE_ENABLE = cfg.subtitle?.enable !== false;
  const SUBTITLE_FONT_SIZE = cfg.subtitle?.fontSize ?? 24;
  const SUBTITLE_MARGIN_V = cfg.subtitle?.marginV ?? 18;
  const SUBTITLE_FONT_NAME = cfg.subtitle?.fontName ?? 'Microsoft YaHei';
  const SUBTITLE_BOLD = cfg.subtitle?.bold !== false;
  const SUBTITLE_CHARS_PER_LINE = cfg.subtitle?.charsPerLine ?? 28;

  function voiceForSlide(idx) {
    if (!USE_VOICE_ALTERNATE) return VOICE_SINGLE;
    const femaleFirst = VOICE_START === 'female';
    const isFemale = femaleFirst ? idx % 2 === 0 : idx % 2 === 1;
    return isFemale ? VOICE_FEMALE : VOICE_MALE;
  }

  console.log('\n╔══════════════════════════════════════════╗');
  console.log('║  HTML 幻灯 + TTS → MP4 (one-context skill) ║');
  console.log('╚══════════════════════════════════════════╝\n');
  console.log(`   项目目录: ${projectRoot}`);
  console.log(`   HTML: ${path.basename(HTML_FILE)}`);
  console.log(`   讲稿: ${path.basename(SCRIPT_FILE)}`);
  console.log(`   输出: ${path.basename(OUTPUT_MP4)}\n`);

  if (!fs.existsSync(SCRIPT_FILE)) {
    throw new Error(`找不到讲稿: ${SCRIPT_FILE}`);
  }
  if (!fs.existsSync(HTML_FILE)) {
    throw new Error(`找不到 HTML: ${HTML_FILE}`);
  }

  if (fs.existsSync(TEMP_DIR)) fs.rmSync(TEMP_DIR, { recursive: true, force: true });
  fs.mkdirSync(TEMP_DIR, { recursive: true });

  const slides = parseScript(fs.readFileSync(SCRIPT_FILE, 'utf-8'));
  console.log(`✅ 解析讲稿完成，共 ${slides.length} 页\n`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();

  await page.goto(pathToFileURL(HTML_FILE).href);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);

  const slideData = [];
  const slideP2 = (i) => String(i).padStart(2, '0');

  for (let i = 0; i < slides.length; i++) {
    const slide = slides[i];
    const tag = `[${String(i + 1).padStart(2)}/${slides.length}]`;
    console.log(`${tag} ${slide.header}`);

    await page.evaluate((n) => {
      if (typeof go === 'function') go(n);
    }, i);
    await page.waitForTimeout(900);

    const imgPath = path.join(TEMP_DIR, `slide_${slideP2(i)}.png`);
    await page.screenshot({ path: imgPath });
    console.log(`      📸 截图 ✓`);

    const audioPath = path.join(TEMP_DIR, `slide_${slideP2(i)}.mp3`);
    const vid = voiceForSlide(i);
    generateAudio(slide.text, audioPath, i, vid, skillDir, TEMP_DIR, voiceCfg);
    const duration = getAudioDuration(audioPath);
    console.log(`      🔊 语音 ✓  ${vid}  ${duration.toFixed(1)}s`);

    slideData.push({ ...slide, imgPath, audioPath, duration });
  }

  await browser.close();
  console.log('\n✅ 截图与语音全部生成完毕\n');

  console.log('🎞  合成各页视频片段...');
  for (let i = 0; i < slideData.length; i++) {
    const s = slideData[i];
    const videoPath = path.join(TEMP_DIR, `slide_${slideP2(i)}.mp4`);

    ff(
      `-y -loop 1 -framerate ${FPS} -i "${s.imgPath}" ` +
        `-i "${s.audioPath}" ` +
        `-c:v libx264 -preset ${VIDEO_PRESET} -b:v ${VIDEO_BITRATE} -maxrate ${VIDEO_MAXRATE} -bufsize 16M -pix_fmt yuv420p ` +
        `-vf "scale=1920:1080" ` +
        `-c:a aac -b:a 192k ` +
        `-t ${s.duration.toFixed(3)} ` +
        `-shortest "${videoPath}"`,
      videoPath
    );

    slideData[i].videoPath = videoPath;
    process.stdout.write(`  片段 ${i + 1}/${slideData.length} ✓\r`);
  }
  console.log('\n✅ 视频片段合成完毕\n');

  const concatList = path.join(TEMP_DIR, 'concat.txt');
  fs.writeFileSync(
    concatList,
    slideData
      .map((s) => `file '${s.videoPath.replace(/\\/g, '/').replace(/'/g, "'\\''")}' `)
      .join('\n'),
    'utf-8'
  );

  const mergedPath = path.join(TEMP_DIR, 'merged.mp4');
  ff(`-y -f concat -safe 0 -i "${concatList}" -c copy "${mergedPath}"`, mergedPath);
  console.log('✅ 拼接完成\n');

  if (SUBTITLE_ENABLE) {
    console.log('📝 生成字幕并烧录进视频...');
    const srtPath = path.join(TEMP_DIR, 'subtitles.srt');
    generateSRT(slideData, srtPath, {
      charsPerLine: SUBTITLE_CHARS_PER_LINE,
    });

    const srtFilter = srtPath
      .replace(/\\/g, '/')
      .replace(/^([A-Za-z]):/, (_, d) => `${d}\\:`);

    const boldVal = SUBTITLE_BOLD ? 1 : 0;
    ff(
      `-y -i "${mergedPath}" ` +
        `-vf "subtitles='${srtFilter}':charenc=UTF-8:force_style='` +
        `FontName=${SUBTITLE_FONT_NAME},` +
        `FontSize=${SUBTITLE_FONT_SIZE},` +
        `PrimaryColour=&H00FFFFFF,` +
        `OutlineColour=&H00000000,` +
        `BackColour=&H80000000,` +
        `Bold=${boldVal},Outline=2,Shadow=1,` +
        `Alignment=2,MarginV=${SUBTITLE_MARGIN_V}` +
        `'" ` +
        `-c:a copy "${OUTPUT_MP4}"`,
      OUTPUT_MP4
    );
  } else {
    fs.copyFileSync(mergedPath, OUTPUT_MP4);
  }

  const totalDuration = slideData.reduce((s, d) => s + d.duration, 0);
  console.log('\n╔══════════════════════════════════════════╗');
  console.log('║          🎉  视频生成完成！               ║');
  console.log('╚══════════════════════════════════════════╝');
  console.log(`\n📁 ${OUTPUT_MP4}`);
  console.log(`⏱  总时长：${(totalDuration / 60).toFixed(1)} 分钟`);
  console.log(`💡 临时文件: ${TEMP_DIR}\n`);
}

module.exports = { run };
