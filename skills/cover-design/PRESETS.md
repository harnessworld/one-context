# Cover Presets — 主题色系

> 4 套开箱即用的主题色系，CONFIG 中设置 `theme` 字段一键切换。

---

## danger — 危险/警示

**主色**：红+橙  |  **氛围**：紧迫、风险、警醒

```javascript
// CONFIG 示例
theme: "danger"
```

| 色值 | 用途 |
|------|------|
| `#FF2A55` | 主强调色（accent） |
| `#FF8C00` | 辅助色（accent2） |
| `#FF6B8A` | 标签文字色 |
| 标签背景 | `rgba(255,42,85,0.12)` |
| 标签边框 | `rgba(255,42,85,0.5)` |

**适用场景**：安全问题、风险警示、紧急通知、曝光类内容

---

## growth — 增长/突破

**主色**：金+青  |  **氛围**：突破、成长、黄金机会

```javascript
// CONFIG 示例
theme: "growth"
```

| 色值 | 用途 |
|------|------|
| `#FFD700` | 主强调色（accent） |
| `#00F0FF` | 辅助色（accent2） |
| `#FFD700` | 标签文字色 |
| 标签背景 | `rgba(255,215,0,0.10)` |
| 标签边框 | `rgba(255,215,0,0.45)` |

**适用场景**：增长报告、突破性进展、职场提升、机会分析

---

## tech — 科技/技术

**主色**：青+紫  |  **氛围**：科技感、数据流、未来感

```javascript
// CONFIG 示例
theme: "tech"
```

| 色值 | 用途 |
|------|------|
| `#00F0FF` | 主强调色（accent） |
| `#8B5CF6` | 辅助色（accent2） |
| `#00D4E8` | 标签文字色 |
| 标签背景 | `rgba(0,240,255,0.08)` |
| 标签边框 | `rgba(0,240,255,0.40)` |

**适用场景**：技术分享、AI/编程、产品发布、数据报告

---

## finance — 金融/财富

**主色**：金+绿  |  **氛围**：金融、收益、价值

```javascript
// CONFIG 示例
theme: "finance"
```

| 色值 | 用途 |
|------|------|
| `#FFD700` | 主强调色（accent） |
| `#00FF88` | 辅助色（accent2） |
| `#FFD700` | 标签文字色 |
| 标签背景 | `rgba(255,215,0,0.10)` |
| 标签边框 | `rgba(255,215,0,0.45)` |

**适用场景**：投资分析、理财、商业策略、行业趋势

---

## 快速选择指南

| 内容类型 | 推荐主题 | 推荐装饰 |
|----------|----------|----------|
| 安全/风险/警示 | danger | 随意 |
| 增长/职场/突破 | growth | 火箭 |
| 技术/AI/编程 | tech | 手机（默认）、芯片 |
| 投资/金融/商业 | finance | 图表、地球 |
| 知识分享/教程 | tech | 书本 |
| 流程/方法论 | growth | 进化条风格装饰 |

---

## 自定义主题

如需自定义主题色，在 template.html 的 `THEMES` 对象中添加新条目：

```javascript
const THEMES = {
    // ... 已有主题 ...

    custom: {
        accent:     "#YOUR_COLOR",
        accent2:    "#YOUR_COLOR2",
        tagBg:      "rgba(...)",
        tagBorder:  "rgba(...)",
        tagColor:   "#YOUR_COLOR",
        glowColor:  "rgba(...)",
        glowColor2: "rgba(...)",
        dotColor:   "#YOUR_COLOR",
        bar:        "linear-gradient(90deg, transparent 2%, #COLOR1 35%, #COLOR2 70%, transparent 98%)",
        textGlow:   "0 0 80px rgba(...), 0 4px 30px rgba(0,0,0,0.9)",
        accentGrad: "linear-gradient(135deg, #COLOR1 0%, #COLOR2 100%)",
        fallbackBg: "radial-gradient(ellipse 120% 80% at 50% 30%, #BG1 0%, #BG2 40%, #BG3 100%)",
        decoGlow:   "rgba(...)",
        decoAccent: "rgba(...)",
    },
};
```

然后在 CONFIG 中设置 `theme: "custom"` 即可。