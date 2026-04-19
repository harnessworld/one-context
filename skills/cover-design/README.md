# Cover Design Skill

CONFIG 驱动的独立封面模板，每期只改一个 JS 对象。

## 快速开始

1. **选主题** → `PRESETS.md`（4 种：danger / growth / tech / finance）
2. **选装饰** → `ELEMENTS.md`（5 种 SVG 图案）或使用默认手机
3. **复制模板** → `template.html` 复制为 `cover.html`
4. **填 CONFIG** → 修改顶部的 `CONFIG` 对象
5. **截图输出** → `node cli.js cover --project <dir>`

## 文件说明

| 文件 | 用途 |
|------|------|
| `template.html` | CONFIG 驱动封面模板（唯一模板文件） |
| `SKILL.md` | 核心规范、CONFIG 字段详解、工作流程 |
| `PRESETS.md` | 4 套主题色系说明 |
| `ELEMENTS.md` | 装饰 SVG 图库与自定义指南 |

## 主题速选

| 主题 | 主色 | 适用场景 |
|------|------|----------|
| danger | 红+橙 | 风险警示、安全问题、曝光类 |
| growth | 金+青 | 增长报告、职场提升、突破性进展 |
| tech | 青+紫 | 技术分享、AI/编程、产品发布 |
| finance | 金+绿 | 投资分析、理财、商业策略 |

---

被 `html-video-from-slides` 引用，封面设计以本 skill 为准。