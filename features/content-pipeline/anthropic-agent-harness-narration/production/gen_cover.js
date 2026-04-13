const { chromium } = require('playwright');
const path = require('path');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
    const htmlPath = path.join(__dirname, 'cover.html');
    await page.goto(`file://${htmlPath}`);
    await page.waitForTimeout(500);
    const shotPath = path.join(__dirname, 'videos', 'cover.png');
    await page.screenshot({ path: shotPath, type: 'png' });
    console.log(`竖版封面已生成: ${shotPath}`);
    await browser.close();
})();
