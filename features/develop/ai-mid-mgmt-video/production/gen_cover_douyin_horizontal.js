/**
 * 抖音横版封面 1080×608（见 cover-douyin-horizontal.html 注释）
 *   node gen_cover_douyin_horizontal.js
 * 输出：videos/cover-douyin-horizontal.png
 */

const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

async function main() {
    const projectDir = process.cwd();
    const htmlPath = path.join(projectDir, 'cover-douyin-horizontal.html');
    const videosDir = path.join(projectDir, 'videos');
    const outputPath = path.join(videosDir, 'cover-douyin-horizontal.png');

    if (!fs.existsSync(htmlPath)) {
        console.error('未找到 cover-douyin-horizontal.html');
        process.exit(1);
    }
    if (!fs.existsSync(videosDir)) fs.mkdirSync(videosDir, { recursive: true });

    const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');
    console.log('抖音横版 1080×608 截图…');
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1080, height: 608 });
    await page.goto(fileUrl);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(800);
    await page.screenshot({ path: outputPath, type: 'png' });
    await browser.close();

    const kb = Math.round(fs.statSync(outputPath).size / 1024);
    console.log(`已生成 ${outputPath} (${kb} KB)`);
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
