const { chromium } = require('playwright');
const { pathToFileURL } = require('url');
const fs = require('fs');

(async () => {
  const htmlFile = '/Users/superno/Documents/code/creative/one-context/features/content-pipeline/sandbox-agent-era-mid-video/production/slides/presentation.html';
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();
  await page.goto(pathToFileURL(htmlFile).href);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);
  
  // 方法1: 正常截图 go(0)
  await page.evaluate(() => { go(0); });
  await page.waitForTimeout(200);
  await page.screenshot({ path: '/tmp/try1_0.png', type: 'png' });
  
  // 方法2: go(4) 后 element screenshot
  await page.evaluate(() => { go(4); });
  await page.waitForTimeout(200);
  const el = await page.$('div#P');
  await el.screenshot({ path: '/tmp/try1_el.png' });
  
  // 方法3: go(6) 后 clip
  await page.evaluate(() => { go(6); });
  await page.waitForTimeout(200);
  await page.screenshot({ path: '/tmp/try1_clip.png', clip: {x:0, y:0, width:1920, height:1080} });
  
  // 方法4: go(8) 后 viewport resize
  await page.evaluate(() => { go(8); });
  await page.setViewportSize({width: 1920, height: 1081});
  await page.waitForTimeout(50);
  await page.setViewportSize({width: 1920, height: 1080});
  await page.waitForTimeout(200);
  await page.screenshot({ path: '/tmp/try1_resize.png' });
  
  const s0 = fs.statSync('/tmp/try1_0.png').size;
  const se = fs.statSync('/tmp/try1_el.png').size;
  const sc = fs.statSync('/tmp/try1_clip.png').size;
  const sr = fs.statSync('/tmp/try1_resize.png').size;
  console.log('normal:', s0, 'element:', se, 'clip:', sc, 'resize:', sr);
  
  const b0 = fs.readFileSync('/tmp/try1_0.png');
  const be = fs.readFileSync('/tmp/try1_el.png');
  console.log('0==el?', b0.equals(be));
  
  await browser.close();
})();
