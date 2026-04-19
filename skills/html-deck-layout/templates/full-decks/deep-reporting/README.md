# deep-reporting

## When to use

深度汇报类模板，适用于需要高视觉一致性的演示文稿。
采用 shell 布局（每页相同结构）+ deep-blue 主题，
强制每页包含 SVG 图解，确保 AI 生成结果稳定。

推荐场景：商务汇报、分析报告、方法论讲解、战略提案。

## Shell 布局特点

- **每页结构统一**: `slide-shell > slide-topline + slide-main(hero-grid > hero-left + hero-right) + footer`
- **强制视觉**: `hero-right` 必须放 SVG 图，杜绝纯文字页
- **装饰元素固定**: `hero-ordinal`、`hero-accent-bar`、`hero-glow` 自动生成
- **AI 只需填写**: eyebrow 标签、标题、副标题、SVG 图、footer 洞见

**注意**: shell 模式下 footer 使用 `.footer` 类名（不是 `.slide-footer`），避免与 mobile-layout.css 冲突。

## Page breakdown

| # | Section | Pattern | hero-right SVG 建议 |
|---|---------|---------|-------------------|
| 1 | 封面钩子 | Shell + hero-grid | 主题相关插图 |
| 2 | 痛点/问题 | Shell + hero-grid | 衰减曲线/数据图 |
| 3 | 思维转变 | Shell + hero-grid + 对比卡片 | 对比图/流程图 |
| 4 | 核心原则 | Shell + hero-grid + 色点列表 | 2x2 卡片图 |
| 5 | 方法模式 | Shell + hero-grid | 时间线/步骤图 |
| 6 | 应对策略 | Shell + hero-grid + hashtag | 界面/交互图 |
| 7 | 关键视角 | Shell + hero-grid | notif-card 列表 |
| 8 | 真实案例 | Shell + hero-grid + A/B 摘要 | A/B 对比图 |
| 9 | 结尾金句 | Full-bleed SVG (`.slide-shell--fullbleed`) | 光线+原则卡片+引言 |

## Customization

- **主题**: 默认 `mobile-deep-blue.css`，可替换（需确保 theme 定义了 `--shell-*` 变量）
- **内容**: 修改 eyebrow / title / sub / SVG / footer-strong
- **不要**: 改变 `slide-shell` 的结构层次，这是稳定性的核心
- **hero-right 内容**: 不限于纯 SVG，可以嵌入 HTML 组件（如 `.notif-card` 列表）

## CSS 加载顺序

```html
<link rel="stylesheet" href="../../../assets/base.css">
<link rel="stylesheet" href="../../../assets/fonts.css">
<link rel="stylesheet" href="../../../assets/mobile-layout.css">
<link rel="stylesheet" href="../../../assets/shell-layout.css">
<link rel="stylesheet" href="../../../assets/themes/mobile-deep-blue.css">
<link rel="stylesheet" href="style.css">
```

## 与传统 7 布局的关系

shell 布局和传统 7 布局（Cover / Grid 2x2 / Split / Card+Diagram / Stat / Process / Thanks）是两套独立系统：

- **同一 deck 中不要混用**——选一种坚持到底
- 需要高一致性 → shell
- 需要多变版式 → 传统 7 布局