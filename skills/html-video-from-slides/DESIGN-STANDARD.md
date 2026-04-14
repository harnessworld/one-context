# Presentation Design Standard

> 配合 `SKILL.md`（html-video-from-slides）使用。本文档定义所有口播视频 presentation.html 的**视觉规范与主题系统**。

**姊妹约束（不重复全文）**：若幻灯以 **大量 inline 样式** 自包含排版（`slide-main`、`fill-deck`、整页 flex 等），**版式操作级**说明见 `skills/html-deck-layout/SKILL.md`（防空白、示意图区、与本文字号下限对齐）。

## 适用场景

面向**短视频手机横屏观看**（1920×1080 截图合成 MP4），需要：
- 路演 / CEO 汇报级视觉效果（绚丽，非普通 PPT）
- 手机屏幕可读（字号够大）
- 画面充实（无大面积空白）
- 酷炫图形图表（非纯文字）
- 无动画（Playwright 截图，静态即可）
- 主题可切换（不同话题用不同风格）

---

## 硬性约束（与 SKILL.md 对齐）

| 项目 | 规定 |
|------|------|
| 画布尺寸 | **1920 × 1080 px**（`#P` 固定宽高） |
| Slide 类名 | `.s`，激活态加 `.on` |
| Slide 内边距 | **`padding:32px 48px`**（四周留呼吸空间，内容不顶边） |
| 导航 JS | `go(i)` 函数，键盘 + 点击左右分区 |
| 字幕对齐 | 每张 slide 必须含 `.wa`（Whisper 隐藏锚文字），见下文 |

---

## 信息密度原则

1. **每张 slide ≤ 3 个信息块**（标题算 1 块，不计装饰/图形）
2. **画面覆盖率 ≥ 85%**：卡片/图形/文字填满视觉区域，禁止大块留白
3. **每张 slide 至少含 1 个图形元素**：SVG 图表、架构图、数据可视化、装饰性 SVG 均可
4. 封面 / 总结页可适度留白（作为视觉呼吸节点）

---

## 字号规范（最小值，手机横屏安全线）

> **换算说明**：1920px 画布在 1400px 宽浏览器窗口中缩放比约 0.73，
> 40px CSS → ~29px 实际显示，是可接受的最小正文尺寸。

| 用途 | 最小 CSS 字号 | 实际显示（@1400px窗口） |
|------|--------------|------------------------|
| 英雄大标题（t1） | **124px** | ~91px |
| 页面主标题（t2） | **88px** | ~64px |
| 副标题（t3） | **60px** | ~44px |
| 正文 / 要点（t4） | **42px** | ~31px ← 绝对最小值 |
| 注释 / 说明（t5） | **32px** | ~23px |
| 卡片标题（Grid 内） | **52px** | ~38px |
| 卡片正文（Grid 内） | **42px** | ~31px |
| Cover Pill 标题 | **40px** | ~29px |
| Cover Pill 副说明 | **32px** | ~23px |
| 数据统计数字（ts） | **170px** | ~124px |
| 统计指标名 | **34px** | ~25px |
| 统计解释文字 | **36px** | ~26px |
| 卡片 emoji | **84px** | ~61px |

### ⚠️ 常见错误

- ❌ 在 Grid 卡片内使用 `.t4`（40px）作为卡片标题 — 太小
- ❌ 在任何说明文字里用低于 32px — 手机看不清
- ❌ Cover Pill 副说明低于 32px — 在手机上变成蚂蚁字
- ✅ Grid 卡片的内容直接写 `font-size:52px`（标题）和 `font-size:42px`（说明）
- ✅ 全屏 2×2 Grid 不需要页面标题行；卡片自身 emoji+标题就是视觉锚点

---

## Whisper 锚文字规范

每张 slide 首行放隐藏文字，供 wav-auto 对齐：

```html
<div class="wa">该页口播的关键词 逐字还原核心内容 不需要完整句子 关键词够用</div>
```

CSS：

```css
.wa {
  position: absolute;
  left: -9999px;
  top: 0;
  font-size: 1px;
  opacity: 0;
  pointer-events: none;
  width: 1px;
  overflow: hidden;
  white-space: nowrap;
}
```

**原则**：
- 包含该页口播的主要名词、动词、数字
- 不影响视觉（完全隐藏）
- 不需要完整正文，关键词锚定足够

---

## 布局模板库

### A. Hero（封面/结尾用）
- 全宽居中
- 大标题 + 副标题 + 底部 badge 行
- 背景：orb 光晕 + 动物水印

### B. Split（左文右图，主力布局）
- 左 40–44%：`justify-content:space-between` + **三段结构**（顶：badge+标题 / 中：body flex:1 / 底：总结卡）
- 右 56–60%：SVG 图表 / 架构图（`max-height:960px`）
- ❌ 禁止：左列用 `justify-content:center`（内容不足时大量浮空）
- 适用：架构说明、对比、流程

### C. Grid-2×2（四格并列）
- 4 个等宽信息卡片
- 适用：优势罗列、安全要素、总结要点

### D. Stats（数据冲击）
- 1–2 个超大数字居中
- 下方说明文字
- 适用：性能指标、数据结论

### E. Timeline（进化时间线）
- 垂直 3–4 阶段，箭头连接
- 每段：编号 + 图标 + 标题 + 描述
- 适用：历史演进、发展阶段

---

## 图形组件清单

| 组件 | 使用场景 | 实现方式 |
|------|----------|----------|
| 层级堆叠图 | 架构分层 | SVG 矩形 + 渐变 + 连接箭头 |
| 环形 / 数字环 | 百分比数据 | SVG circle + stroke-dasharray |
| 流程图 | 故障恢复流程 | SVG rect + path + marker |
| 对比两栏 | before/after | CSS grid 两列 |
| 大数字卡片 | 性能指标 | div + 渐变文字 |
| 动物水印 | 主题装饰 | `.animal-wm` + 巨型 emoji + 极低透明度 |

---

## 主题系统架构

### Base Layer（结构骨架，所有主题共用）

- 画布、slide、导航、`.wa` 规范
- 布局模板（`.s`、`.col`、`.row`、`.f1`）
- 字号 class（`.t1`–`.t5`、`.ts`）
- Card / Badge 占位 class

### Theme Skin（皮肤包，~30–50 行 CSS）

每套主题定义：

```css
:root {
  /* 背景 */
  --bg: #...;
  --bg-pattern: url(...);
  /* 主色调（3色） */
  --accent-a: #...;  /* 主强调 */
  --accent-b: #...;  /* 次强调 */
  --accent-c: #...;  /* 第三色 */
  /* 文字 */
  --cream: #...;
  --muted: #...;
  /* 卡片 */
  --card: rgba(...);
  --bdr: rgba(...);
  /* 字体 */
  --font: '...', system-ui;
}
body::before { /* 背景纹理/图案 */ }
.animal-wm { /* 主题专属装饰字符 */ }
```

---

## 官方主题定义

### 1. 动物主题（animal）

**适用话题**：架构、系统设计、工程类话题（动物隐喻）

| Token | 值 |
|-------|-----|
| `--bg` | `#0b1a0d`（深林绿黑） |
| `--accent-a` | `#d4a843`（金色阳光） |
| `--accent-b` | `#4caf72`（丛林绿） |
| `--accent-c` | `#e07a3a`（日落橙） |
| `--cream` | `#f0e8d0` |
| `--muted` | `#7a9f7a` |
| `--font` | system-ui |
| 背景纹理 | 六边形蜂巢网格（极淡金色线） |
| 水印元素 | 按页内容选用对应动物 emoji（opacity 2–3%） |

**卡片变体**：`g-hi`（金边）、`g-gn`（绿边）、`g-or`（橙边）、`g-rd`（红边）、`g-sk`（天蓝边）

**代表作**：`features/develop/anthropic-agent-harness-narration/production/presentation.html`

---

### 2. 商务主题（business）— 待实现

深海蓝 + 冷灰 + 银白；字体 Segoe UI；无动物装饰；图形偏数据图表风格。

### 3. 古文主题（wenyan）— 待实现

仿宣纸底色（暖米黄）+ 朱砂红 + 墨绿；楷体 / 宋体；印章装饰；留白感强。  
参考：`features/develop/claude-caveman-mode/production/presentation.html`

### 4. 宝宝可爱主题（kawaii）— 待实现

浅粉 / 奶蓝；圆角气泡卡片；卡通图标；大圆点装饰。

---

## 新建 Presentation 流程

1. 通读 SRT，划分话题段落，确定 slide 数量（建议 10–14 张，每张平均 30–50s）
2. 准备 CSS：复制 `base.css` + 选定主题 `theme-*.css` 到素材目录
3. **每张 slide 独立组合**：从 `TEMPLATES.md` 选布局，从 `svg-snippets.md` 选图形，从 `base.css` 选卡片/芯片配色——相邻 slide 布局不同，图形不重复
4. 编写 `.wa` 隐藏锚文字（摘自该段 SRT 关键词）
5. 每张 slide 完成后对照 `TEMPLATES.md` Minimum Fill Table 验证填充率
6. 用 `node cli.js wav-auto --project <dir>` 验证对齐效果

---

## 页面标题行策略

| 场景 | 推荐做法 |
|------|----------|
| Grid 2×2（4 卡） | **不要独立标题行**，改为 slim header（inline chip + 标题，约 70px 高）或完全去掉 |
| Grid 2×2（4 卡）内容多 | **拆成 2 页**（每页 2 个大卡，更大字体，更强视觉冲击） |
| Split 布局 | 左侧正常放 chip + 标题，占左列顶部 |
| Stats 数字页 | slim header（chip + 标题同行），其余空间给大数字 |

**拆页原则**：页数多不是问题，宁可多拆一页也不要让单页内容密度超标导致字小。

## 字数上限（每个文字块）

| 位置 | 上限 | 违规后果 |
|------|------|----------|
| 卡片 body 每行 | 18 汉字 | 超出自动换行 → 挤压行高 |
| 每张卡片 body | 5 行（不计空行） | 超出 → 拆成下一页 |
| Slim header 标题 | 12 汉字 | 超出字号被迫缩小 |
| Bottom tag / 总结行 | 20 汉字 | 超出溢出卡片边界 |
| **每张 slide 总字数** | **≤ 120 汉字** | Slide 是骨架，口播讲细节 |

## 反模式（禁止）

- ❌ 大块空白：单张 slide 空白区域 > 15% 视觉面积
- ❌ 纯文字页：没有任何图形元素（装饰水印也算）
- ❌ **字号过小：Grid 卡片标题 < 52px，卡片正文 < 42px，全局 body < 42px，Cover Pill 标题 < 40px，任何说明文字 < 32px**
- ❌ 缺少 `.wa`：任何 slide 不含 Whisper 锚文字
- ❌ 超过 3 信息块：单页信息过载
- ❌ 动画/transition 影响截图：截图时应为最终态
- ❌ Grid 2×2 同时加独立标题行：标题行 + grid 双重压缩，必然字小
- ❌ **`position:absolute` 定位内容区**：进化条、标题行、底部说明脱离文档流，产生死空间
- ❌ **`justify-content:center` + 内容不足**：内容浮在中间，上下大量空白；大卡/Split 左列必须改 `space-between`
- ❌ **`<br>` 空行当间距**：空行不贡献内容高度却消耗视觉空间，配合 `center` 会放大空洞感；改用 `margin-top` 分组或 separator div
- ❌ **Cover 内容区用 `position:absolute`**：进化条、底部来源行脱离文档流，flex 容器无法感知其高度

## HTML 模板参考

生成新 presentation 时，**必须**使用 `base.css` 的共享类名（不自己写 CSS），每张 slide 从 `TEMPLATES.md` 选布局骨架、从 `svg-snippets.md` 选图形。`reference.html` 展示了完整的 HTML 结构（CSS 引用、#P 容器、导航脚本），仅作结构参考，**不要直接复制后填空——那会千篇一律**。每页生成后对照 TEMPLATES.md 的 Minimum Fill Table 自验填充率。
