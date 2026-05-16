/**
 * Resume: merge tmp/part_*.mp4 + burn subtitles when full wav already produced segments.
 * Usage: node scripts/finish-burn.js <production-dir>
 * See references/resume-burn.md
 */
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const root = path.resolve(process.argv[2] || process.cwd());
const skillRoot = path.join(__dirname, '..');
const tmp = path.join(root, 'tmp');
const merged = path.join(tmp, 'merged.mp4');
const outDefault = path.join(root, 'final_auto.mp4');
const concatList = path.join(tmp, 'concat.txt');
const assPath = path.join(tmp, 'sub_for_burn.ass');
const resultPath = path.join(root, 'build-result.txt');

const BAR_HEIGHT = 110;
const BAR_ALPHA = 0.65;

function readOutputFile() {
  const cfgPaths = [
    path.join(root, 'timing', 'wav-durations.json'),
    path.join(root, 'wav-durations.json'),
  ];
  for (const p of cfgPaths) {
    if (!fs.existsSync(p)) continue;
    try {
      const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
      if (cfg.outputFile) {
        return path.isAbsolute(cfg.outputFile)
          ? cfg.outputFile
          : path.join(root, cfg.outputFile);
      }
    } catch {
      /* ignore */
    }
  }
  return outDefault;
}

function log(lines) {
  fs.appendFileSync(resultPath, lines.join('\n') + '\n', 'utf8');
}

function findFfmpeg() {
  const w = spawnSync('where', ['ffmpeg'], { encoding: 'utf8', shell: true });
  if (w.status === 0 && w.stdout.trim()) {
    return w.stdout.trim().split(/\r?\n/)[0].trim();
  }
  const skillFf = path.join(skillRoot, 'node_modules', 'ffmpeg-static', 'ffmpeg.exe');
  if (fs.existsSync(skillFf)) return skillFf;
  throw new Error('ffmpeg not found (PATH or skills/html-video-from-slides/node_modules/ffmpeg-static)');
}

function runFfmpeg(ff, args) {
  const r = spawnSync(ff, args, { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 });
  if (r.status !== 0) {
    throw new Error(
      `ffmpeg failed (${r.status}): ${(r.stderr || r.stdout || '').slice(-4000)}`
    );
  }
}

function assFilterPath(p) {
  return p.replace(/\\/g, '/').replace(/^([A-Za-z]):/, (_, d) => `${d}\\:`);
}

function main() {
  const out = readOutputFile();
  if (fs.existsSync(resultPath)) fs.unlinkSync(resultPath);
  log([`started ${new Date().toISOString()}`, `project: ${root}`]);

  const ff = findFfmpeg();
  log([`ffmpeg: ${ff}`]);

  if (!fs.existsSync(assPath)) {
    throw new Error(`Missing ${assPath} — run full "node cli.js wav" first`);
  }

  if (!fs.existsSync(merged)) {
    if (!fs.existsSync(concatList)) {
      throw new Error(`Missing ${merged} and ${concatList}`);
    }
    log(['concat parts -> merged.mp4']);
    runFfmpeg(ff, [
      '-y',
      '-f',
      'concat',
      '-safe',
      '0',
      '-i',
      concatList,
      '-c',
      'copy',
      merged,
    ]);
  } else {
    log(['merged.mp4 already exists']);
  }

  const alphaHex = Math.max(0, Math.min(255, Math.round((1 - BAR_ALPHA) * 255)))
    .toString(16)
    .padStart(2, '0');
  const assEsc = assFilterPath(assPath);
  const drawBox = `format=rgba,drawbox=y=ih-${BAR_HEIGHT}:color=#000000${alphaHex}:width=iw:height=${BAR_HEIGHT}:t=fill,format=yuv420p,`;
  const vf = `${drawBox}ass='${assEsc}'`;

  if (fs.existsSync(out)) fs.unlinkSync(out);
  log(['burn subtitles -> ' + path.basename(out)]);
  runFfmpeg(ff, ['-y', '-i', merged, '-vf', vf, '-c:a', 'copy', out]);

  const st = fs.statSync(out);
  log([
    'SUCCESS',
    `path: ${out}`,
    `size_mb: ${(st.size / (1024 * 1024)).toFixed(2)}`,
  ]);
}

try {
  main();
} catch (e) {
  log([`ERROR: ${e.message}`]);
  process.exit(1);
}
