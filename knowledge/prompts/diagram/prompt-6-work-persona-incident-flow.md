---
prompt_id: 6
slug: work-persona-incident-flow
exemplar_image: images/exemplar-work-persona-incident-flow.png
tags: [协作编排]
prompt_language: en
---

# Prompt: exemplar-work-persona-incident-flow

> 100% 视觉还原提示词，对应 `exemplar-work-persona-incident-flow.png`

```
Create a vertical-portrait infographic (aspect ratio approximately 3:4, e.g. 900×1200 px) illustrating how "work.md" and "persona.md" collaborate during an online incident response. Four major horizontal bands top to bottom: Title Header, Three-Phase Sequence Diagram, Horizontal Detail Flow, Bottom Comparison Panel.

═══════════════════════════════════════
GLOBAL STYLE
═══════════════════════════════════════
- Background: pure white (#FFFFFF)
- Primary accent: teal/dark cyan (#1A7A7A) for header bars, key arrows, emphasis text
- Secondary: light teal (#E8F4F4) for section background fills
- Tertiary: warm light gray (#F5F5F0) for document card backgrounds
- Border/line: medium gray (#CCCCCC)
- Text: near-black (#222222) body, white (#FFFFFF) on teal bars
- Main flow arrows: teal (#1A7A7A), stroke 2–3px, filled triangular arrowheads
- Annotation arrows: gray (#999999), 1px, dashed
- Curved connectors: teal (#1A7A7A), smooth cubic-bezier arcs, 2px
- Font: Chinese sans-serif (PingFang SC, Noto Sans SC)
- Size hierarchy: Title 28-32px bold, Subtitle 14-16px, Section headers 16-18px bold, Phase labels 13-14px bold, Body 11-12px, Annotations 10-11px gray
- Icon style: simple flat line-art, 24-32px, dark gray (#555555) stroke, no fill
- Rounded corners 4-6px. No drop shadows. Clean flat design.

═══════════════════════════════════════
BAND 1 — TITLE HEADER (top 12%)
═══════════════════════════════════════
- Line 1 (28-32px bold teal #1A7A7A, left-aligned): "线上故障来了，work.md 和 persona.md 怎么一起工作"
- Line 2 (14-16px regular gray #888888): "人格定入口，能力做执行，再回到人格包输出"
- Top-right annotation (10-11px #999999, right-aligned): "重点：只解释协同结构，不展开前置来源"

═══════════════════════════════════════
BAND 2 — THREE-PHASE SEQUENCE DIAGRAM (next 45%)
Background: faint light-teal (#EAF6F6)
═══════════════════════════════════════

Section title (16-18px bold #333333, centered): "协同运行时序：一次任务如何在三段之间流动"

THREE EQUAL COLUMNS (~30% each, ~5% gutters):

COLUMN 1 — Phase 1:
- Header bar: teal (#1A7A7A) rounded rect, white text "阶段一：Persona 定义入口" 13px bold
- Card below: #F5F5F0 fill, #CCCCCC border, "Persona.md" 14px bold
  - Body: "提问方向和进入姿态", "每一段都在消费上一段的结果", "人格定入口" in teal
- LEFT INPUT ARROW: teal 2.5px horizontal from left canvas edge
  - Label: "输入任务：告警 / 问题 / 初始上下文" 10-11px
  - Yellow warning triangle (⚠, fill #F5A623) at arrow origin

COLUMN 2 — Phase 2:
- Header bar: medium gray (#888888), white text "阶段二：Work 执行排障"
- Card: "Work.md" 14px bold
  - 2×2 grid of icon-label pairs inside:
    - 看监控 (monitor icon), 查发布 (clipboard icon)
    - 定位链路 (node graph icon), 形成建议 (document+star icon)
  - Each icon 28-32px, #555555 stroke, label 11px #444444
  - "能力做执行" 11px teal

COLUMN 3 — Phase 3:
- Header bar: teal (#1A7A7A), white text "阶段三：Persona 包装输出"
- Card: "Persona.md" 14px bold
  - "中间结果：诊断判断 / 处置建议", "人格包输出" in teal
- RIGHT OUTPUT ARROW: teal 2.5px to right canvas edge
  - "最终响应：像这个人说出来的结论" 10px gray

Inter-column arrows: teal dashed 1.5px rightward, label "同一个任务，按顺序经过三段处理"
Two teal parabolic arcs spanning full width (one above, one below columns), 2px, showing left-to-right flow.

Bottom annotation (11px #888888): "这不是两份文档并列展示，这是一次任务在运行时的三段式编排"

═══════════════════════════════════════
BAND 3 — HORIZONTAL DETAIL FLOW (next 22%)
Background: white, separated by thin gray line (#DDDDDD)
═══════════════════════════════════════

5 rounded-rectangle boxes in horizontal row (~120×36px each, 1.5px teal border, white fill, 12px bold teal text):

BOX 1: "先问变更 / 影响面"
BOX 2: "再看监控 / 发布记录"
BOX 3: "缩小异常范围"
BOX 4: "定位链路和依赖"
BOX 5: "形成处置建议" (2px border, final step emphasis)

Connecting: straight teal arrows 2px between boxes.

Sub-branches dropping down (gray dashed 1px vertical, small #FAFAFA boxes):
- Below BOX 1: "先问最近是否发版"
- Below BOX 3: "异常集中在支付回调链路"
- Below BOX 5: "建议先回滚并观察"

Right annotation (10px #888888): "协同并不增加步骤数量，它改变的是步骤的组织方式和表达方式"

═══════════════════════════════════════
BAND 4 — BOTTOM COMPARISON PANEL (bottom 21%)
═══════════════════════════════════════

Title (16-18px bold #333333): "最终效果只看一件事 - 同样的判断，为什么更像真人协作"

Two cards side by side (~42% width each, ~8% gap):

LEFT "纯 Work 输出":
- 1.5px #CCCCCC border, #FAFAFA fill
- "纯 Work 输出" 14px bold #333333
- Body: "先看监控，再查最近发布，异常主要集中在支付回调链路，建议先回滚并观察"
- Sub-label: "Work 执行排障" 10px gray

RIGHT "Work + Persona 输出":
- 1.5px teal border (#1A7A7A), #F8FCFC fill (faint teal tint)
- "Work + Persona 输出" 14px bold teal
- Body: "先别乱猜，最近是不是刚发过版？影响面先拉齐。现在看起来异常集中在支付回调链路，下游超时把错误率带上来了。先回滚，别硬顶。"

Center annotation (10px #888888): "work 决定内容正确 / persona 决定表达像本人"
Bottom label (11px teal): "人格包输出，能力保正确"

═══════════════════════════════════════
SPACING & COLOR SUMMARY
═══════════════════════════════════════
- Band 1: 0%–12%, white
- Band 2: 12%–57%, light teal (#EAF6F6)
- Band 3: 57%–79%, white
- Band 4: 79%–100%, white
- Overall: airy, spacious, teal + gray + white, single yellow ⚠ as only warm accent

═══════════════════════════════════════
DESIGN ATOMS APPLIED
═══════════════════════════════════════
色彩策略：A 单强调色 + 全灰度（teal #1A7A7A 为唯一彩色，仅一处黄色 ⚠ 作暖色点缀）
布局骨架：C 分段堆叠（四横带）+ A 多栏流水线（Band 2 三列时序图）
信息层级：多级标准 + 焦点元素（Band 2 三阶段时序图为视觉重心）
连接语言：粗实线=主流向（teal 2-3px 曲线），细虚线=注释（灰 1px），抛物线弧=跨区域流向（teal 2px）
元素词汇：圆角矩形=阶段卡片，横幅条=阶段头部（teal/gray 填充白字），对比并排卡片=效果对比
情绪基调：D 协同流程风（干净平直 + 极淡底色分区 + 清爽无衬线）
```

## 使用说明

- **适用工具**: Claude Artifacts (SVG/HTML), DALL-E 3, Midjourney v6+
- **推荐尺寸**: 900×1200px (3:4) 或等比缩放
- **风格关键词**: collaborative flow, teal accent, three-phase sequence, clean flat design
- **注意事项**: Band 4 的对比面板是全图落点 — 左侧"纯 Work"灰色边框 vs 右侧"Work + Persona"teal 边框，对比效果决定说服力
