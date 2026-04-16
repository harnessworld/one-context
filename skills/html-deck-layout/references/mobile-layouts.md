---
title: Mobile Deck Layouts — 布局目录
---

# Mobile Deck 布局目录

7 种移动端优化布局，每种对应 `templates/single-page/` 下的模板文件。所有布局遵循 fill-deck + ≥42px 正文 + ≥85% 覆盖率约束。

| 布局 | 文件 | 结构 | 适用页 | 关键 CSS |
|------|------|------|--------|----------|
| **Cover** | `cover.html` | v-center + hero | 封面、章节首页 | `.v-center`, `.emoji-xl` |
| **Grid 2×2** | `grid-2x2.html` | fill-deck + 4 卡网格 | 功能总览、模块对比 | `.fill-deck`, `.grid-2x2` |
| **Split 50/50** | `split-50-50.html` | fill-deck + 左右对半 | 对比、前后端、优劣 | `.fill-deck`, `.split` |
| **Card + Diagram** | `card-plus-diagram.html` | fill-deck + 顶卡 + 全宽图 | 架构图、流程图、数据流 | `.fill-deck`, `.card-diagram` |
| **Stat Highlight** | `stat-highlight.html` | fill-deck + 大数字卡 | 数据展示、里程碑 | `.stat-value`, `.stat-label` |
| **Process Flow** | `process-flow.html` | fill-deck + 横向步骤 | 发布流程、决策链、时间线 | `.process-flow` |
| **Thanks** | `thanks.html` | v-center + 居中文字 | 收口、致谢、结尾 | `.v-center` (例外允许) |

## 布局选择指南

```
封面 .............. Cover
功能/模块总览 ..... Grid 2×2
A vs B 对比 ....... Split 50/50
架构/流程图 ....... Card + Diagram
关键数字 .......... Stat Highlight
步骤/流程 ......... Process Flow
结尾 .............. Thanks
```

## 版式多样性规则

- 同一 deck 中至少使用 2–3 种不同布局
- 禁止连续 3 页以上使用同一布局
- Grid 和 Split 可交替使用增加视觉变化
