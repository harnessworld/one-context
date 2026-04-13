const { chromium } = require('playwright');
const path = require('path');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1440, height: 1080 } });
    const htmlPath = path.join(__dirname, 'cover_h.html');
    await page.goto(`file://${htmlPath}`);
    await page.waitForTimeout(500);
    const shotPath = path.join(__dirname, 'videos', 'cover_h.png');
    await page.screenshot({ path: shotPath, type: 'png' });
    console.log(`横版封面已生成: ${shotPath}`);
    await browser.close();
})();
