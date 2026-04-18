# 开源图标库索引

> 来源：综合整理自各图标库官方站点（Lucide、Heroicons、Phosphor、Tabler、Remix Icon 等）
> 作者：one-context 项目组
> 发布日期：2026-04
> 收录日期：2026-04-12
>
> 图标库选型指南。完整库在官方站点查看，本文仅提供链接与对比。

**使用原则**：
- 优先 SVG 内嵌（无依赖、无加载延迟）
- 避免图标字体（加载慢、渲染问题）
- 保持风格统一（一个项目用一套）

---

## 推荐方案（SVG 内嵌）

| 库 | 图标数 | 风格 | 许可证 | 链接 | 适用场景 |
|---|--------|------|--------|------|----------|
| **Lucide** | 1400+ | 线条、现代 | MIT | https://lucide.dev | 首选，风格统一 |
| **Heroicons** | 300+ | 线条/实心 | MIT | https://heroicons.com | Tailwind 生态 |
| **Phosphor** | 900+ | 6 种粗细 | MIT | https://phosphoricons.com | 需要粗细变体 |
| **Tabler** | 5200+ | 线条 | MIT | https://tabler-icons.io | 覆盖面广 |
| **Remix Icon** | 2800+ | 线条/实心 | Apache 2.0 | https://remixicon.com | 设计师友好 |

### 对比

| 维度 | Lucide | Heroicons | Phosphor | Tabler |
|------|--------|-----------|----------|--------|
| 风格一致性 | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ |
| 数量 | 中等 | 中等 | 中等 | 最多 |
| 线条粗细 | 单一 | 单一 | 6 种 | 单一 |
| 搜索体验 | 优 | 优 | 优 | 良 |
| React 组件 | ✓ | ✓ | ✓ | ✓ |
| 推荐 | **首选** | 备选 | 需粗细变体时 | 找冷门图标时 |

---

## 插画素材库

| 库 | 内容 | 许可证 | 链接 | 用途 |
|---|------|--------|------|------|
| **unDraw** | 人物/场景插画 | MIT | https://undraw.co | 装饰插图，可改色 |
| **Humaaans** | 人物组件库 | CC BY | https://humaaans.com | 流程图人物 |
| **Open Peeps** | 手绘人物 | CC0 | https://openpeeps.com | 轻松风格 |
| **Storyset** | 场景插画 | Freepik | https://storyset.com | 商业需署名 |
| **Alibaba Paper Illustration** | 纸质感插画 | — | `assets/alibaba-paper-illustration.jpg` | 装饰插图、PPT 背景 |

---

## 背景/纹理生成

| 工具 | 功能 | 链接 |
|------|------|------|
| **Haikei** | SVG 背景、波浪、网格、渐变 | https://haikei.app |
| **SVG Backgrounds** | 可调参数 SVG 纹理 | https://svgbackgrounds.com |
| **Pattern.css** | 纯 CSS 图案 | https://bansal.io/pattern-css |
| **CSS Gradient** | 渐变生成器 | https://cssgradient.io |

---

## Emoji 源

| 来源 | 说明 | 链接 |
|------|------|------|
| **Emojipedia** | 查询 Unicode、版本 | https://emojipedia.org |
| **OpenMoji** | 开源 emoji SVG（可改色）| https://openmoji.org |
| **Noto Emoji** | Google 官方 SVG | https://github.com/googlefonts/noto-emoji |

---

## 使用方式

### 方式一：直接内嵌 SVG（推荐）

```html
<!-- 从 Lucide/Heroicons 复制 SVG 代码 -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <rect x="3" y="3" width="18" height="18" rx="2"/>
  <path d="M3 9h18"/>
  <path d="M9 21V9"/>
</svg>
```

**优点**：无依赖、无加载、可 CSS 控制颜色

### 方式二：SVG Sprite

```html
<!-- 页面顶部定义 -->
<svg style="display:none">
  <symbol id="icon-grid" viewBox="0 0 24 24">
    <rect x="3" y="3" width="7" height="7"/>
    <rect x="14" y="3" width="7" height="7"/>
    <rect x="14" y="14" width="7" height="7"/>
    <rect x="3" y="14" width="7" height="7"/>
  </symbol>
</svg>

<!-- 使用时引用 -->
<svg width="24" height="24"><use href="#icon-grid"/></svg>
```

**优点**：复用、减少 DOM 体积

### 方式三：Emoji（零依赖）

```html
<span style="font-size:84px">🏗️</span>
```

**优点**：零成本、移动端原生渲染
**缺点**：不同系统渲染差异、不可改色

---

## 版权与许可证

| 许可证 | 商用 | 修改 | 署名 |
|--------|------|------|------|
| MIT | ✓ | ✓ | ✗ |
| Apache 2.0 | ✓ | ✓ | ✗ |
| CC BY | ✓ | ✓ | ✓ |
| CC0 | ✓ | ✓ | ✗ |

本索引所列图标库均为开放许可，但仍需遵守各自条款。使用前请查阅官方许可证说明。

---

## 本仓库集成

| 需求 | 使用方案 | 来源 |
|------|----------|------|
| 幻灯功能图标 | SVG 片段库 | `skills/html-deck-layout/svg-snippets.md` |
| 快速表达 | Emoji 速查 | `skills/html-deck-layout/emoji-guide.md` |
| 装饰背景 | Haikei 生成 + 手调 | 幻灯 inline 样式 |

---

*最后更新：2026-04*