/**
 * 横版封面截图：在本目录执行 node gen_cover_h.js → videos/cover_h.png（1440×1080）
 * 依赖：与 gen_cover.js 相同（playwright + chromium）
 */
const path = require("path");
const fs = require("fs");
const { pathToFileURL } = require("url");

async function main() {
  const projectDir = process.cwd();
  const coverHtml = path.join(projectDir, "cover_h.html");
  const videosDir = path.join(projectDir, "videos");
  const outputPath = path.join(videosDir, "cover_h.png");

  if (!fs.existsSync(coverHtml)) {
    console.error("未找到 cover_h.html");
    process.exit(1);
  }

  let chromium;
  try {
    ({ chromium } = require(path.join(projectDir, "node_modules", "playwright")));
  } catch {
    console.error("请先在本目录执行: npm install playwright && npx playwright install chromium");
    process.exit(1);
  }

  if (!fs.existsSync(videosDir)) fs.mkdirSync(videosDir, { recursive: true });

  const fileUrl = pathToFileURL(coverHtml).href;
  console.log("横版截图中:", fileUrl);

  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1440, height: 1080 });
  await page.goto(fileUrl);
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(600);
  await page.screenshot({ path: outputPath, type: "png" });
  await browser.close();

  const kb = Math.round(fs.statSync(outputPath).size / 1024);
  console.log(`横版封面已生成: ${outputPath} (${kb} KB)`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
