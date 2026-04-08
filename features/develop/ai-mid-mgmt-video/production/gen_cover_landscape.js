/**
 * 横版封面（与 gen-cover SKILL 竖版 1080×1920 配套；SKILL 未写横版像素，此处固定 2560×1440 / 16:9）
 * 当前目录需有 cover-horizontal.html
 *   node gen_cover_landscape.js
 * 输出：videos/cover-horizontal.png
 */

const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

async function main() {
    const projectDir = process.cwd();
    const coverHtml = path.join(projectDir, 'cover-horizontal.html');
    const videosDir = path.join(projectDir, 'videos');
    const outputPath = path.join(videosDir, 'cover-horizontal.png');

    if (!fs.existsSync(coverHtml)) {
        console.error('未找到 cover-horizontal.html');
        process.exit(1);
    }
    if (!fs.existsSync(videosDir)) fs.mkdirSync(videosDir, { recursive: true });

    const fileUrl = 'file:///' + coverHtml.replace(/\\/g, '/');
    console.log('横版截图…');
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.setViewportSize({ width: 2560, height: 1440 });
    await page.goto(fileUrl);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(400);
    await page.screenshot({ path: outputPath, type: 'png' });
    await browser.close();

    const kb = Math.round(fs.statSync(outputPath).size / 1024);
    console.log(`已生成 ${outputPath} (${kb} KB)`);
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
