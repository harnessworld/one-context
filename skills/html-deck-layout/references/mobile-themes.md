---
title: Mobile Deck Themes — 主题目录
---

# Mobile Deck 主题目录

6 款移动端优化主题，覆盖深色/浅色/暖色/数据场景。每个主题覆盖 base.css 的颜色 token。

| 主题 | 文件 | 背景 | 适用场景 | 关键色 |
|------|------|------|----------|--------|
| **mobile-tech** | `assets/themes/mobile-tech.css` | 深蓝 #0f172a | 技术分享、工程内训（默认主题） | 天蓝 #38bdf8 / 靛蓝 #818cf8 |
| **mobile-warm** | `assets/themes/mobile-warm.css` | 暖黄 #fffbeb | 亲和介绍、品牌展示、生活类 | 橙 #f97316 / 红 #ef4444 |
| **mobile-minimal** | `assets/themes/mobile-minimal.css` | 白 #ffffff | 正式汇报、学术报告、企业内训 | 天蓝 #0ea5e9 / 靛蓝 #6366f1 |
| **mobile-dark** | `assets/themes/mobile-dark.css` | 纯黑 #000000 | OLED 设备、赛博风、夜间演示 | 青 #22d3ee / 粉 #f472b6 |
| **mobile-data** | `assets/themes/mobile-data.css` | 浅蓝 #eff6ff | 数据报告、季度汇报、BI 展示 | 蓝 #2563eb / 紫 #7c3aed |
| **mobile-nature** | `assets/themes/mobile-nature.css` | 浅绿 #f0fdf4 | 文化内容、教育、自然主题 | 绿 #4caf72 / 金 #d4a843 |

## 使用方式

在 `<head>` 中引入 base.css + 主题 CSS：

```html
<link rel="stylesheet" href="../../assets/base.css">
<link rel="stylesheet" href="../../assets/fonts.css">
<link rel="stylesheet" href="../../assets/mobile-layout.css">
<link rel="stylesheet" href="../../assets/themes/mobile-tech.css">
```

切换主题只需替换最后一行的主题文件路径。

## 选择建议

- **技术分享** → mobile-tech（默认最安全）
- **小红书/短内容** → mobile-warm 或 mobile-nature
- **正式汇报** → mobile-minimal 或 mobile-data
- **赛博/活动** → mobile-dark
- **不确定** → mobile-tech
