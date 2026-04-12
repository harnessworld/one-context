'use strict';

/**
 * Cover screenshot generator using Playwright.
 *
 * node cli.js cover --project <dir>              → videos/cover.png (1080×1920)
 * node cli.js cover --project <dir> --horizontal → videos/cover_h.png (1440×1080)
 */

const path = require('path');
const fs = require('fs');

const SIZES = {
  portrait:  { w: 1080, h: 1920 },
  landscape: { w: 1440, h: 1080 },
};

function pathToFileURL(p) {
  return 'file:///' + p.replace(/\\/g, '/');
}

async function run(projectDir, { horizontal }) {
  const htmlName = horizontal ? 'cover_h.html' : 'cover.html';
  const htmlPath = path.join(projectDir, htmlName);

  if (!fs.existsSync(htmlPath)) {
    console.error(`❌ ${htmlName} not found in ${projectDir}`);
    process.exit(1);
  }

  const size = horizontal ? SIZES.landscape : SIZES.portrait;
  const outDir = path.join(projectDir, 'videos');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  const outName = horizontal ? 'cover_h.png' : 'cover.png';
  const outPath = path.join(outDir, outName);

  // Load playwright-core
  let chromium;
  const skillNodeModules = path.join(__dirname, '..', 'node_modules', 'playwright-core');
  try {
    const pw = require(skillNodeModules);
    chromium = pw.chromium;
  } catch {
    try {
      const pw = require('playwright-core');
      chromium = pw.chromium;
    } catch {
      console.error('❌ playwright-core not found. Run in skill dir: npm install && npx playwright install chromium');
      process.exit(1);
    }
  }

  console.log(`📸 Rendering ${htmlName} at ${size.w}×${size.h} …`);

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: size.w, height: size.h } });

  try {
    await page.goto(pathToFileURL(htmlPath), { waitUntil: 'networkidle' });
  } catch {
    // file:// protocol may not emit networkidle; ignore
  }
  await page.waitForTimeout(1000);
  await page.screenshot({ path: outPath, fullPage: false });
  await browser.close();

  const stat = fs.statSync(outPath);
  const kb = (stat.size / 1024).toFixed(0);
  console.log(`✅ ${outPath}  (${kb} KB, ${size.w}×${size.h})`);
}

module.exports = { run };
