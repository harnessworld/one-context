'use strict';

/**
 * SRT → Slide duration mapper (two-phase workflow).
 *
 * Phase 1 (analyze):  node cli.js srt-map --project <dir>
 *   Parses sub.srt, counts slides in presentation.html, outputs both.
 *   AI reads output, determines entry→slide boundaries.
 *
 * Phase 2 (generate): node cli.js srt-map --project <dir> --boundaries "0:0-5,1:6-12,..."
 *   Accepts boundaries, generates wav-durations.json.
 */

const fs = require('fs');
const path = require('path');
const { resolvePath } = require('./path_resolver');

// ── SRT parser ──────────────────────────────────────────────

function parseSrt(srtPath) {
  let text = fs.readFileSync(srtPath, 'utf-8').replace(/^\uFEFF/, '');
  // Normalize line endings to \n
  text = text.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  const regex = /(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})\n([\s\S]*?)(?=\n\n|\n\d+\n|$)/g;
  const entries = [];
  let m;
  while ((m = regex.exec(text)) !== null) {
    const start = +m[1] * 3600 + +m[2] * 60 + +m[3] + +m[4] / 1000;
    const end = +m[5] * 3600 + +m[6] * 60 + +m[7] + +m[8] / 1000;
    entries.push({
      i: entries.length,
      start: Math.round(start * 1000) / 1000,
      end: Math.round(end * 1000) / 1000,
      text: m[9].trim().replace(/\n/g, ' '),
    });
  }
  return entries;
}

// ── Slide counter ───────────────────────────────────────────

function countSlides(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf-8');
  const classMatches = html.match(/class=["'][^"']*\bslide\b[^"']*["']/g);
  const goMatches = html.match(/\bgo\s*\(\s*\d+\s*\)/g);
  return {
    byClass: classMatches ? classMatches.length : 0,
    byGo: goMatches ? goMatches.length : 0,
  };
}

function extractSlideTexts(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf-8');
  const slides = [];
  const regex = /<(?:div|section)[^>]*class=["'][^"']*\bslide\b[^"']*["'][^>]*>([\s\S]*?)<\/(?:div|section)>\s*(?=<(?:div|section)\b[^>]*class=["'][^"']*\bslide|<\/body)/gi;
  let m;
  while ((m = regex.exec(html)) !== null) {
    const text = m[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 140);
    if (text) slides.push(text);
  }
  return slides;
}

// ── Format helpers ──────────────────────────────────────────

function fmtTime(sec) {
  const m = Math.floor(sec / 60);
  const s = (sec % 60).toFixed(1);
  return `${m}:${s.padStart(4, '0')}`;
}

function pad3(n) { return String(n).padStart(3); }

// ── Phase 1: Analyze ────────────────────────────────────────

function analyze(srtPath, htmlPath) {
  const entries = parseSrt(srtPath);
  if (!entries.length) {
    console.error('❌ No SRT entries found in', srtPath);
    process.exit(1);
  }

  console.log(`\n📄 SRT: ${entries.length} entries  (${fmtTime(entries[0].start)} → ${fmtTime(entries[entries.length - 1].end)})`);

  let slideCount = 0;
  let slideTexts = [];
  if (fs.existsSync(htmlPath)) {
    const info = countSlides(htmlPath);
    slideCount = Math.max(info.byClass, info.byGo);
    slideTexts = extractSlideTexts(htmlPath);
    console.log(`📊 Slides: ${slideCount}  (by class: ${info.byClass}, by go(): ${info.byGo})`);
  } else {
    console.log('⚠️  presentation.html not found — slide count unknown');
  }

  console.log('\n── SRT entries ──');
  for (const e of entries) {
    console.log(`[${pad3(e.i)}] ${fmtTime(e.start)} → ${fmtTime(e.end)}  ${e.text.slice(0, 80)}`);
  }

  if (slideTexts.length) {
    console.log('\n── Slides ──');
    slideTexts.forEach((t, i) => {
      console.log(`[Slide ${i}] ${t}`);
    });
  }

  console.log(`\n✏️  Next: provide boundaries as "0:0-0,1:1-2,..." (slide_idx:first_entry-last_entry)`);
  console.log(`   node cli.js srt-map --project <dir> --boundaries "0:0-0,1:1-2,..."`);
}

// ── Phase 2: Generate wav-durations.json ────────────────────

function generate(projectDir, entries, boundariesStr) {
  const parts = boundariesStr.split(',').map(s => s.trim()).filter(Boolean);
  const durations = [];
  let totalDur = 0;

  for (const part of parts) {
    const [slideStr, rangeStr] = part.split(':');
    if (slideStr === undefined || rangeStr === undefined) {
      console.error(`❌ Invalid boundary part: "${part}" (expected "slide_idx:first-last")`);
      process.exit(1);
    }
    const slideIdx = parseInt(slideStr, 10);
    const [first, last] = rangeStr.split('-').map(Number);
    if (isNaN(slideIdx) || isNaN(first) || isNaN(last)) {
      console.error(`❌ Invalid numbers in: "${part}"`);
      process.exit(1);
    }

    const start = entries[first] ? entries[first].start : 0;
    const nextEntry = entries[last + 1];
    const end = nextEntry ? nextEntry.start : (entries[last] ? entries[last].end : start);
    const dur = Math.max(0, Math.round((end - start) * 100) / 100);

    durations[slideIdx] = dur;
    totalDur += dur;
  }

  // Fill gaps with 5s default
  for (let i = 0; i < durations.length; i++) {
    if (durations[i] === undefined) durations[i] = 5;
  }

  // Find WAV file
  const wavFiles = fs.readdirSync(projectDir).filter(f => f.endsWith('.wav'));
  const wavFile = wavFiles[0] || 'audio.wav';

  const wavDurations = {
    outputFile: 'final_auto.mp4',
    slideDurationsSec: durations,
    wavFile: wavFile,
    totalDurationSec: Math.round(totalDur * 100) / 100,
  };

  const outPath = path.join(projectDir, 'timing', 'wav-durations.json');
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(wavDurations, null, 2), 'utf-8');
  console.log(`\n✅ ${outPath}`);
  console.log(`   ${durations.length} slides, total ${Math.round(totalDur * 100) / 100}s (${(totalDur / 60).toFixed(1)} min)`);
  for (let i = 0; i < durations.length; i++) {
    console.log(`   Slide ${String(i).padStart(2)}: ${durations[i]}s`);
  }
}

// ── Main ────────────────────────────────────────────────────

function run(projectDir, { boundaries }) {
  const srtPath = resolvePath(projectDir, 'subtitles', 'sub.srt');
  const htmlPath = resolvePath(projectDir, 'slides', 'presentation.html');

  if (!fs.existsSync(srtPath)) {
    console.error('❌ sub.srt not found in', projectDir);
    process.exit(1);
  }

  if (boundaries) {
    const entries = parseSrt(srtPath);
    generate(projectDir, entries, boundaries);
  } else {
    analyze(srtPath, htmlPath);
  }
}

module.exports = { run };
