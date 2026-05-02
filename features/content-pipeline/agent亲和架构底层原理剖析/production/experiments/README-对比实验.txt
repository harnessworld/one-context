Open Design 对比实验（与当前流水线产物对照）
============================================

本目录放了从官方仓库 tmp/open-design 抽取的两份「可双击打开」的 HTML，
用于肉眼对比版式气质；内容仍是上游示例主题，不是你的「Agent 亲和架构」专稿。

A. 当前流水线（本专题正式稿）
   ../slides/presentation.html
   - html-deck-layout + mobile-tech，固定 1920×1080 手机横屏叙事
   - 与 html-video-from-slides wav 模式配套（#P 缩放、go(n)、.s.slide）

B. open-design · guizang（杂志风 + WebGL 双背景 + 横向 deck）
   open-design-guizang-magazine-demo.html
   - 由 skills/guizang-ppt/assets/template.html + example-slides.html 合并生成
   - 键盘 ← →、ESC 索引；全屏杂志排版、数据大字报、流水线布局等
   - 需联网加载 Google Fonts；含 WebGL 与 unpkg lucide

C. open-design · simple-deck（极简横向投融资风示例）
   open-design-simple-deck-sample.html
   - 横向 scroll-snap，← → 翻页；偏英文 VC deck 语汇

如何打开
--------
在资源管理器中双击上述 .html，或用浏览器「打开文件」。

若要同一选题、可发表的 OD 稿：需在本地跑 open-design（pnpm tools-dev），
选 deck 技能 + 设计体系，把你的讲稿/大纲当 brief 生成；再单独评估是否值得做
HTML → presentation.html 的适配层。
