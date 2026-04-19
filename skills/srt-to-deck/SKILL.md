---
name: srt-to-deck
description: >-
  从 SRT 字幕文件生成 presentation.html + wav-durations.json。按话题和时长自动拆页，锁定每页对应的 SRT 条目范围，输出精确翻页时长。
  使用 html-deck-layout 风格的移动端幻灯片，可直接用 html-video-from-slides 的 wav 模式成片（无需 Whisper 对齐）。
  Triggers: "SRT转PPT", "字幕转幻灯", "SRT to slides", "srt2deck", "口播转PPT", "从字幕生成幻灯片", "srt to presentation"。
---

# srt-to-deck — SRT 字幕 → 移动端幻灯片（精准翻页）

从 Whisper 转写的 SRT 文件生成 `presentation.html` + `wav-durations.json`，
可直接用于 `html-video-from-slides` 的 `wav` 模式合成视频。

**核心优势**：拆页时锁定"哪几句字幕属于哪一页"，直接从 SRT 时间戳算出翻页时长，
跳过 Whisper 二次对齐，彻底避免口播与幻灯翻页不同步的问题。

## 适用场景

- 有口播录音，已用 Whisper（或 `srt-proofread` skill）转写为 SRT
- 需要根据口播内容制作对应幻灯片
- 不想手动拆页、选布局、写 HTML
- 口播与幻灯翻页不同步是常见痛点——本 skill 从根源解决

## 典型串联工作流

```
WAV → srt-proofread → SRT → srt-to-deck → presentation.html + wav-durations.json
                                                       ↓
                                               html-video-from-slides (wav 模式) → MP4
```

**推荐用 `wav` 模式（而非 `wav-auto`）成片**：wav-durations.json 已包含精确的翻页时长，
无需再让 Whisper 猜测口播对应哪一页。

## 布局系统

本 skill **复用 `html-deck-layout`** 的完整布局系统，不自带 CSS/模板：

| 资源 | 来源 |
|------|------|
| 6 套主题 CSS | `skills/html-deck-layout/assets/themes/` |
| 7 种布局 | `skills/html-deck-layout/templates/single-page/` |
| 完整 deck 模板 | `skills/html-deck-layout/templates/full-decks/` |
| 质量基准 | `skills/html-deck-layout/examples/demo-deck/` |

生成的 HTML 引用 html-deck-layout 的 CSS（相对路径或内联均可）。

## Generation workflow (MANDATORY)

**You MUST follow these 7 steps in order. Do not skip any step.**

### Step 1: 输入确认

向用户确认四个要素：

1. **SRT 文件路径**（必须）
2. **风格偏好**（默认 `mobile-tech`；可选 `mobile-warm` / `mobile-minimal` / `mobile-dark` / `mobile-data` / `mobile-nature`）
3. **目标页数**（自适应：`roundUp(总秒数 / 40)`，上下浮动 ±2。例：8min→12页，2min→3页，20min→30页）
4. **起始模板**（默认 `mobile-generic`；可选 `mobile-tech-sharing` / `mobile-product-pitch` / `mobile-course-intro`）

如果没有明确指出风格，按内容类型推荐：

| 内容类型 | 推荐主题 | 推荐模板 |
|----------|----------|----------|
| 技术/架构/AI | `mobile-tech` | `mobile-tech-sharing` |
| 生活/亲和/小红书 | `mobile-warm` | `mobile-generic` |
| 正式汇报/学术 | `mobile-minimal` 或 `mobile-data` | `mobile-generic` |
| 赛博/活动 | `mobile-dark` | `mobile-generic` |
| 文化/教育 | `mobile-nature` | `mobile-course-intro` |

✓ Gate: 用户提供了 SRT 路径后才能继续。

### Step 2: SRT 解析与拆页

读取 SRT 文件，解析时间轴和文本，按话题拆页，**同时计算每页精确时长**。

**SRT 预处理校验**：

1. 检测时间戳重叠/倒序，若有则提示用户回到 `srt-proofread` 修整
2. 检测大段空白（>30s 无 SRT 条目），提示可能存在转写缺失
3. 检测是否含说话人标签（如 `Speaker 1:` 前缀），若有则启用多说话人模式

**拆页规则**：

1. **话题边界识别**（优先级从高到低）：
   - 明确的过渡句（如"接下来""然后我们来看""第二部分""另一方面"）
   - 阶段性总结 + 新主题引入
   - 时间间隔 >3s **且**前后内容存在语义跳变的 SRT 条目之间（纯停顿不触发）
   - 递进信号（"首先/其次/最后""第一个/第二个"）可用于切分过长段落
2. **每页时长**：30-50s 为宜；>60s 应拆分；<20s 应与相邻段合并
3. **每页 SRT 条目**：通常 5-15 条，快语速/对话类可达 25-30 条

**>60s 段落拆分策略**：

在过长段落中寻找次级分页点：
- 递进/枚举信号（"首先/其次/最后""第一/第二""一方面/另一方面"）
- 拆分后每子页不低于 20s
- 例："四条核心原则"按原则1-2 / 原则3-4 拆为两页

**<20s 段落合并策略**：

- 首页 <20s：作为封面页保留，不合并（可加 `coverExtraSec` 延长停留）
- 中间页 <20s：与话题更紧密的相邻段合并（语义相似度 > 时间相邻度）
- 末尾页 <20s（非 Thanks）：与前一页合并

**多人对话处理**：

若 SRT 含说话人标签（如 WhisperX 输出）：
- 按说话人区分，应答词归入当前主讲人的话题
- 话题切换仍以上述规则为准，不因对话方切换而拆页

若 SRT **无**说话人标签（大多数 Whisper 输出）：
- 启发式规则：连续 3 条以上长句（>20 字）的说话者推断为主讲，单字/双字应答为配合角色
- 双方均有长段输出（如播客/访谈）时，以话题边界优先，忽略说话人切换信号
- 应答词（"对""嗯""是""OK"）不单独成页，归入当前话题
- 建议用户在 `srt-proofread` 阶段手动标注说话人（可提升拆页质量）

**时长计算**：

**每页时长 = 下一页第一条 SRT 的开始时间 - 本页第一条 SRT 的开始时间。**

最后一页时长 = 音频结束时间 - 最后一页第一条 SRT 的开始时间。

> 此公式保证间隙自然落入前一页，且所有页时长之和 **严格等于音频总时长**，不会出现末尾黑屏或音频截断。

```
示例（8分钟口播）：
第1页: SRT #1-#2  → 起始 00:00:00 → 下一页起始 00:00:07 → 时长 7.0s
第2页: SRT #3-#13 → 起始 00:00:07 → 下一页起始 00:00:34 → 时长 26.7s
...
最后一页: SRT #205-#213 → 起始 07:51 → 音频结束 08:06 → 时长 15.0s
```

**音频头尾静音处理**：
- SRT 起始 >0 时，0 ~ 首条 SRT 起始的时间归入封面页（封面在静音中停留）
- SRT 结束后音频仍有内容（片尾音乐），归入 Thanks 页

**输出格式**：

| 页码 | 时间段 | 时长(s) | 主题关键词 | SRT 条目范围 | 建议布局 |
|------|--------|--------|-----------|-------------|----------|
| 1 | 0:00-0:07 | 7.0 | 封面 | 1-2 | Cover |
| 2 | 0:07-0:34 | 26.7 | 问题背景 | 3-13 | Split |
| ... | ... | ... | ... | ... | ... |
| N | 7:51-8:06 | 15.0 | 收尾 | 205-213 | Thanks |

✓ Gate: 拆页大纲完成，页数在目标范围内，每页时长已计算，时长之和 = 音频总时长。

### Step 3: 大纲确认

向用户展示拆页结果表格，等待用户确认或调整。提供两级确认：

- **快速确认**：仅展示每页的主题 + 时长 + 布局，用户一语即可通过
- **详细确认**：展示完整表格含 SRT 条目范围，供精细调整

用户可能的调整：
- 合并某两页
- 拆分某一页为两页
- 更改某页的布局建议
- 修改主题关键词
- 调整某页的 SRT 条目范围（直接影响翻页时机）

**调整后必须重新计算受影响页的时长**，并验证总和仍 = 音频总时长。

✓ Gate: 用户确认大纲后才能继续。

### Step 4: 布局选择与内容映射

根据每页主题自动匹配布局，精炼 SRT 文本为幻灯内容。

**布局匹配规则**：

| 页面角色 | 布局 | 判断依据 |
|----------|------|----------|
| 视频封面 | **Cover** | 固定首页 |
| 总览/模块对比/多要点 | **Grid 2×2** | "几个方面""四大特性""三个模块" |
| 对比/前后/优劣/双视角 | **Split 50/50** | "对比""vs""一方面另一方面" |
| 架构/流程/数据流/系统 | **Card + Diagram** | "架构""流程""链路""数据流"（**必用，≥2 页**） |
| 关键数字/里程碑/指标 | **Stat Highlight** | 具体数字、百分比、排名 |
| 步骤/流程/时间线 | **Process Flow** | "第一步""然后""最后""流程" |
| 收尾/致谢 | **Thanks** | 固定末页 |

**布局多样性约束**（与 html-deck-layout 一致）：
- 最多连续 2 页使用同一种布局，不可 3 页以上连续同布局
- 整份 deck 必须 ≥3 种不同布局（Cover/Thanks 不计入）
- ≥2 页使用 Card + Diagram（含内联 SVG）

**内容精炼规则**：

1. 从该段 SRT 文本中提取核心信息，≤120 汉字/页（硬上限；各布局建议值更保守）
2. 标题提炼为 ≤15 字
3. 去除语气词（嗯、啊、呢、吧）、口头禅（就是说、对吧、然后）、重复表达；但保留嵌入长句的话语标记（如"对，而不是..."中的"对"起逻辑连接作用，不应删除）
4. 保留关键数据（数字、百分比、专有名词）
5. 每个 card/信息块 ≤40 汉字

各布局建议字数（120 为硬上限，推荐在以下范围内）：

| 布局 | 建议字数 |
|------|----------|
| Cover | ≤30 |
| Grid 2×2 | ≤80（每卡 ~20） |
| Split 50/50 | ≤60（单侧 ~30） |
| Card + Diagram | ≤70（SVG 占位较多） |
| Stat Highlight | ≤40 |
| Process Flow | ≤80 |
| Thanks | ≤30 |

**`.wa` 锚文字**：每页至少一个 `.wa` 元素，用于后续 wav-auto 模式的 Whisper 对齐后备。
选取规则：
- 优先选取该页 SRT 中唯一标识本页的一句话（含关键词/数据）
- 不选通用语（"对""接下来""我们要聊的是"）
- 不重复幻灯标题
- 写法：`<span class="wa">核心语句摘录</span>`，定位在页面底部或角落

✓ Gate: 每页布局已确定，内容已精炼，≥2 页标注了 Card + Diagram + SVG。

### Step 5: 生成 presentation.html + wav-durations.json

**极其重要：先读取质量基准**：

> ⚠️ You MUST read `skills/html-deck-layout/examples/demo-deck/index.html` as the visual
> quality baseline. Your output MUST match or exceed its richness.

**生成规则**：

1. 从 Step 1 选定的 full-deck 模板打底
2. 替换每页内容为 Step 4 的精炼文本
3. 按布局选择从 `templates/single-page/` 复制对应结构
4. 引用 html-deck-layout 的 CSS（参见下方 CSS 路径示例）
5. 添加内联 SVG 图表（Step 4 标注的 Card + Diagram 页）
6. 包含键盘导航 `<script>`，**必须包含 `function go(n)`**
7. **同时输出 `wav-durations.json`**（文件名必须与 html-video-from-slides 一致！）

**CSS 路径示例**：

素材目录通常在 `features/xxx/production/` 或独立目录，需根据实际位置调整：

```
# 素材目录在项目根下
<link rel="stylesheet" href="../../skills/html-deck-layout/assets/base.css">

# 素材目录在 features/xxx/production/
<link rel="stylesheet" href="../../../skills/html-deck-layout/assets/base.css">

# 最稳妥：内联关键 CSS 到 HTML 中（自包含，不依赖相对路径）
```

具体引用的四个 CSS：
```
base.css → fonts.css → mobile-layout.css → themes/mobile-{主题}.css
```

**wav-durations.json 格式**（文件名必须为 `wav-durations.json`，这是 html-video-from-slides 硬编码期望的文件名）：

```json
{
  "wavFile": "口播.wav",
  "slideDurationsSec": [7.0, 26.7, 54.2, 38.7, ...],
  "outputFile": "final.mp4",
  "burnSubtitles": true,
  "srtFile": "sub.srt",
  "subtitle": {
    "charsPerLine": 28,
    "fontSize": 18
  }
}
```

字段说明：
- `slideDurationsSec`：**核心字段**，数组长度 = 幻灯页数，每项 = 该页持续秒数（来自 Step 2 的时长计算），各项之和应 = 音频总时长
- `wavFile`：口播 WAV 文件名（用户需确认）
- `outputFile`：输出视频文件名
- `burnSubtitles`：是否烧录字幕（默认 true）
- `srtFile`：SRT 文件路径（用于烧录字幕）
- `subtitle`：字幕样式配置（`charsPerLine` 默认 28，与 html-video-from-slides 一致）

**HTML 骨架**（slide 结构与 html-deck-layout CSS 完全一致：`.s.slide` + `is-active` 切换）：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>视频标题</title>
<link rel="stylesheet" href="path/to/html-deck-layout/assets/base.css">
<link rel="stylesheet" href="path/to/html-deck-layout/assets/fonts.css">
<link rel="stylesheet" href="path/to/html-deck-layout/assets/mobile-layout.css">
<link rel="stylesheet" href="path/to/html-deck-layout/assets/themes/mobile-tech.css">
<style>/* 此处仅放本视频专属覆盖 */</style>
</head>
<body>
<div id="prog" style="width:0%"></div>
<div id="P">
  <section class="s slide is-active" id="s0">...</section>
  <section class="s slide" id="s1">...</section>
  ...
</div>
<div id="pn"></div>
<script>
(function(){
var PW=1920,PH=1080;
function fit(){var el=document.getElementById('P'),r=Math.min(window.innerWidth/PW,window.innerHeight/PH),x=(window.innerWidth-PW*r)/2,y=(window.innerHeight-PH*r)/2;el.style.transform='scale('+r+')';el.style.transformOrigin='0 0';el.style.left=x+'px';el.style.top=y+'px'}
window.addEventListener('resize',fit);fit();
var slides=document.querySelectorAll('.s.slide'),total=slides.length,cur=0;
function ui(){document.getElementById('pn').textContent=(cur+1)+' / '+total;var b=document.getElementById('prog');if(b)b.style.width=(cur/(total-1)*100)+'%'}
function go(i){if(i<0||i>=total)return;slides[cur].classList.remove('is-active');cur=i;slides[cur].classList.add('is-active');ui()}
document.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key==='ArrowDown'||e.key===' '){e.preventDefault();go(cur+1)}else if(e.key==='ArrowLeft'||e.key==='ArrowUp'){e.preventDefault();go(cur-1)}});
document.addEventListener('click',function(e){if(e.clientX>window.innerWidth*0.3)go(cur+1);else go(cur-1)});
ui();
})();
</script>
</body>
</html>
```

✓ Gate: HTML 结构完整，包含 go(n) 函数，wav-durations.json 已生成，CSS 路径可用。

### Step 5.5: 成片指引

向用户说明如何使用产出物合成视频：

**推荐方式：wav 模式（精准翻页）**

```bash
node skills/html-video-from-slides/cli.js wav --project <素材目录>
```

此模式直接读取 `wav-durations.json` 中的 `slideDurationsSec`，按精确时长翻页，
**无需 Whisper 二次对齐**，口播与画面天然同步。

**不推荐：wav-auto 模式**

```bash
# ⚠️ 不推荐用于 srt-to-deck 产出的幻灯
node skills/html-video-from-slides/cli.js wav-auto --project <素材目录>
```

wav-auto 的对齐原理是用 **Whisper 识别音频中的语音，再匹配幻灯可见文字** 来判断翻页时机。
但 srt-to-deck 已将口播内容精炼为骨架（≤120 字），与原始口播差异很大，
Whisper 匹配成功率极低，大概率降级为"均分音频"，翻页与讲解彻底脱节。
**除非你打算放弃精确翻页、让 Whisper 完全接管，否则不要使用 wav-auto。**

✓ Gate: 用户清楚两种成片方式的区别和适用场景。

### Step 6: 自检

**复用 html-deck-layout 全部硬约束**（约束值来自 html-deck-layout Visual richness rules，如有冲突以 html-deck-layout 为准）：

- [ ] fill-deck on all content pages（除 Cover/Thanks）
- [ ] Body text ≥42px, card title ≥52px
- [ ] Coverage ≥85%, ≤120 汉字/页
- [ ] SVG 内文字 viewBox 坐标下 ≥24px（标注），≥28px（关键文字）
- [ ] 每页 ≤3 info blocks
- [ ] Layout variety: ≥3 types total, no 3+ consecutive same layout
- [ ] ≥2 pages with card-diagram + inline SVG

**额外自检**：

- [ ] `wav-durations.json` 的 `slideDurationsSec` 数组长度 = HTML slide 数量
- [ ] `slideDurationsSec` 各项之和 = 音频总时长（误差 ≤1s；校验基准是 WAV 文件时长，而非 SRT 最后一条时间）
- [ ] 每页有 `.wa` 锚文字（后备对齐用）
- [ ] 总页数在目标范围内
- [ ] `function go(n)` 存在且可调用
- [ ] CSS 引用路径正确（在浏览器中打开 HTML 可正常显示，slide 可见且可翻页）
- [ ] slide 使用 `<section class="s slide">` + `is-active` 切换，与 html-deck-layout CSS 兼容

✓ Gate: 全部勾选通过。

## 与现有 skill 的关系

| | srt-to-deck | html-deck-layout | html-video-from-slides | srt-proofread |
|---|---|---|---|---|
| 输入 | SRT 文件 | 用户 prompt | HTML + 音频 | WAV |
| 输出 | presentation.html + wav-durations.json | presentation.html | MP4 | 校对后 SRT |
| 布局系统 | 复用 html-deck-layout | 自有 | 不涉及 | 不涉及 |
| 对齐方式 | SRT 时间戳直接算时长 | 不涉及 | Whisper 或 slideDurationsSec | 不涉及 |
| 关系 | 上游：SRT→HTML+时长 | 上游：prompt→HTML | 下游：HTML+音频→视频 | 前置：SRT 校对 |

- **srt-to-deck 复用 html-deck-layout 的所有视觉规范**（主题、布局、SVG、fill-deck），不自带 CSS/模板
- **srt-to-deck 输出的 wav-durations.json 让 html-video-from-slides 的 wav 模式直接可用**，无需 Whisper 对齐
- **srt-proofread 是前置步骤**：先用 srt-proofread 校对 SRT，再用 srt-to-deck 生成幻灯

## 反模式

- 不要把 SRT 原文逐条照搬到幻灯片上——幻灯是骨架，细节靠口播
- 不要跳过大纲确认直接生成 HTML——拆页结果需要人工审核
- 不要自创布局或 CSS——统一使用 html-deck-layout 的布局系统
- 不要省略 wav-durations.json——这是精准翻页的关键，缺了就只能靠 Whisper 猜
- 不要在同一页堆砌 >120 汉字——手机屏幕放不下
- 不要修改 wav-durations.json 的时间轴而不重新校验 SRT 对应关系——改一处可能影响全局
- 不要对 srt-to-deck 产出的精炼幻灯使用 wav-auto 模式——匹配成功率极低，大概率翻页脱节