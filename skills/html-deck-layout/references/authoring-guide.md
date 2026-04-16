---
title: Mobile Deck Authoring Guide — 创作工作流
---

# Mobile Deck 创作指南

从大纲到成品移动端 PPT 的完整工作流。

## Step 1: 确认需求

向用户确认三件事：

1. **内容与受众**：主题、大概页数、观众是谁？
2. **风格选择**：推荐 2–3 个候选主题（见 [mobile-themes.md](mobile-themes.md)）
3. **起始模板**：用哪个 full-deck 模板打底？（见 `templates/full-decks/`）

## Step 2: 选择主题

```html
<!-- 在 <head> 中引入 -->
<link rel="stylesheet" href="../../assets/base.css">
<link rel="stylesheet" href="../../assets/fonts.css">
<link rel="stylesheet" href="../../assets/mobile-layout.css">
<link rel="stylesheet" href="../../assets/themes/mobile-tech.css">  <!-- 替换此行 -->
```

## Step 3: 规划大纲

将内容拆页，每页对应一个布局：

| 页码 | 内容 | 布局 |
|------|------|------|
| 1 | 封面 | Cover |
| 2 | 核心功能 | Grid 2×2 |
| 3 | 架构图 | Card + Diagram |
| ... | ... | ... |
| N | 致谢 | Thanks |

## Step 4: 组装 Deck

1. 复制 `templates/deck.html` 作为起始文件
2. 从 `templates/single-page/` 复制对应的布局段落
3. 替换 demo 数据为实际内容
4. 补充 SVG 示意图（参考 [svg-snippets.md](svg-snippets.md)）

## Step 5: 应用移动端约束

对每页自检：

- [ ] 使用 fill-deck（除 Cover/Thanks 外）
- [ ] 正文 ≥42px、卡片标题 ≥52px
- [ ] 画面覆盖率 ≥85%
- [ ] SVG 内文字 viewBox 坐标下 ≥18px
- [ ] 每页 ≤120 汉字、≤3 信息块
- [ ] 连续页布局有变化

详细规范见 [spec-cheatsheet.md](spec-cheatsheet.md)。

## Step 6: 产出与导出

- 完整 HTML 文件（自包含，可离线打开）
- 与 `html-video-from-slides` 联动：添加 `.wa` 锚字后可自动成片
- 用 Playwright 截图导出 PNG
