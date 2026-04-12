# Prompt: knowledge-base-intro

> 知识库结构介绍信息图，基于 diagram-design-atoms 策略组合生成

```
Create a vertical-portrait infographic (aspect ratio approximately 2:3, e.g. 1200×1800px) that serves as an introduction to the "knowledge/" directory in one-context. The graphic is divided into four horizontal bands: Title Header, Radial Knowledge Map, Adapter Pipeline, and Maintenance Loop. Uses a professional teal/cyan monochrome color scheme with hand-drawn curved connectors.

═══════════════════════════════════════
GLOBAL STYLE
═══════════════════════════════════════
- Background: pure white #FFFFFF
- Primary accent: deep teal #0D6B6E
- Secondary accent: medium teal #3A9A9E
- Tertiary accent: light teal #7CC4C7
- Quaternary accent: ice teal #D6EEEF
- Card backgrounds: ice teal #EAF5F5 to #F4FAFA
- Badge/number circles: #0D6B6E fill with white #FFFFFF text
- Connector lines: hand-drawn wavy/curved style, stroke ~2px, color #3A9A9E to #0D6B6E, organic — no sharp corners
- Arrow heads: small solid triangles, same color as their line
- Border style on cards: 1px solid #B0D4D6, rounded corners 4-6px
- Drop shadows: very subtle, 1-2px offset, #00000010
- Icon style: simple line-art / outline icons in #0D6B6E or #3A9A9E
- Font: Chinese sans-serif (Source Han Sans / Noto Sans SC); Latin in rounded casual sans
- Typography hierarchy:
  T1 — Main title: bold ~22-24px, color #1A1A1A
  T2 — Subtitle: regular ~12-13px, color #4A4A4A
  T3 — Section headers ("[一：…]"): bold ~14-16px, #0D6B6E, square brackets
  T4 — Node/layer titles: bold ~12-13px, #0D6B6E
  T5 — Body text: regular ~9-11px, #3A3A3A
  T6 — Small labels: regular ~8-9px, #666666
  T7 — Badge numbers: bold ~10px, white on teal circle

═══════════════════════════════════════
BAND 1 — TITLE HEADER (0%–8% from top)
═══════════════════════════════════════
- Line 1 (T1): "knowledge/ — 一处写，处处用" centered, #1A1A1A bold
- Line 2 (T2): "工具中立的知识层：写一遍规范，由适配器翻译给 Claude Code、Cursor、OpenClaw 等所有工具" centered, #4A4A4A
- Small teal pill badge (top-right): "tool-neutral" white text on #0D6B6E, roundness 10px

═══════════════════════════════════════
BAND 2 — RADIAL KNOWLEDGE MAP (8%–55%)
"[一：knowledge/ 里装了什么]"
Background: faint ice teal (#F4FAFA)
═══════════════════════════════════════

Section title (T3): "[一：knowledge/ 里装了什么]" bold #0D6B6E, left-aligned with small book icon

CENTER HUB:
- Position: ~50% horizontal, ~34% vertical
- Rounded rectangle ~200×240px, background #EAF5F5, border 2.5px solid #0D6B6E
- Subtle inner glow: 4px spread #0D6B6E15
- Title (T4 bold, centered): "knowledge/"
- Vertical stack inside (each line with tiny icon, T5):
  - 📋 "规范知识层"
  - "single source of truth"
  - "工具中立 · 适配器翻译"
- Small tag line below (T6): "人类可读，AI 也可读"

5 SURROUNDING SATELLITE NODES (radial arrangement):
Each node: rounded rect ~170-200×90-130px, #F4FAFA background, 1px #B0D4D6 border, with:
- Teal circle badge (diameter ~24px, fill #0D6B6E, white text)
- Small line-art icon (~20px)
- Bold title (T4) + 2-4 body lines (T5)
- Color gradient: badge number depth corresponds to teal shade (1=deepest, 5=lightest)

Node positions (clock arrangement):

1. "standards/" — top-left (~12%, ~12%):
   - Badge "1" (#0D6B6E), shield/ruler icon
   - Title: "standards/"
   - Body: "工程约定 · 命名规范 · 架构模式"
   - Small inner pills: "agent-framework" "claudecode-patterns" "openclaw-arch"
   - Bottom label (T6): "P0 — 权威规范"

2. "playbooks/" — top-right (~70%, ~11%):
   - Badge "2" (#1A7E81), playbook/flag icon
   - Title: "playbooks/"
   - Body: "步骤化操作手册"
   - Small inner pills: "add-umbrella-feature"
   - Bottom label (T6): "可复用流程"

3. "references/" — right (~76%, ~32%):
   - Badge "3" (#3A9A9E), link/bookmark icon
   - Title: "references/"
   - Body: "外部资源索引 · 文章 · 文档 · 仓库"
   - Small inner pills: "diagram-examples" "source-analysis"
   - Bottom label (T6): "精选索引，非全文"

4. "prompts/" — bottom-right (~68%, ~50%):
   - Badge "4" (#5CB5B8), chat-bubble icon
   - Title: "prompts/"
   - Body: "可复用提示词片段"
   - Bottom label (T6): "待填充"

5. "tools/" — bottom-left (~10%, ~46%):
   - Badge "5" (#7CC4C7), wrench icon
   - Title: "tools/"
   - Body: "工具参考文档"
   - Bottom label (T6): "待填充"

CONNECTOR LINES:
- Hand-drawn curved lines from each node → center hub, ~2px, gradient from node badge color to #0D6B6E
- Small solid triangle arrowheads at hub end
- Light dashed lines (#B0D4D6, 1px) between adjacent nodes showing lateral relationships
- Arrow from node 1 to node 2 labeled "标准指导流程" (T6)
- Arrow from node 3 to node 4 labeled "素材变提示" (T6)

Bottom annotation in this band (~53-55%, T6, centered, gray #888888):
"每层都有 README.md 作为索引入口 · 从顶层 knowledge/README.md 开始阅读"

═══════════════════════════════════════
BAND 3 — ADAPTER PIPELINE (55%–80%)
"[二：适配器模型 — 一次写入，多工具消费]"
Background: white, separated by thin teal line (#B0D4D6, 0.5px)
═══════════════════════════════════════

Section title (T3): "[二：适配器模型 — 一次写入，多工具消费]" bold #0D6B6E, left-aligned with small plug/adapter icon

THREE-STAGE HORIZONTAL PIPELINE (~31% each column, ~3% gutters):

STAGE 1 — "源头" (left ~3%–33%):
- Rounded rectangle card ~full height of band, #F4FAFA fill, 1.5px #0D6B6E border, left accent bar 4px #0D6B6E
- Header pill (white text on #0D6B6E): "① 源头"
- Large centered icon: document with checkmark, line-art #0D6B6E
- Title (T4 bold): "knowledge/"
- Body (T5): "Markdown 格式" / "工具中立" / "人类可读"
- Small terminal block (dark #2C2C2C background, #E0E0E0 monospace text):
  "$ onecxt adapt"
- Label below (T6): "唯一真相源"

STAGE 2 — "适配器" (center ~36%–66%):
- Rounded rectangle card, #FAFAFA fill, 1.5px #B0D4D6 border
- Header pill (white text on #1A7E81): "② 适配器"
- Large centered icon: gear/plug, line-art #1A7E81
- Title (T4 bold): "one_context.adapters"
- Body (T5): "翻译而不定义" / "从源头推导" / "不自己造语义"
- Small 4-row table inside (T6):
  | 适配器 | 输出目标 |
  |--------|---------|
  | claudecode | CLAUDE.md |
  | cursor     | .cursorrules |
- Label below (T6): "适配器只翻译，不拥有语义"

STAGE 3 — "消费端" (right ~69%–97%):
- Rounded rectangle card, #FAFAFA fill, 1.5px #B0D4D6 border
- Header pill (white text on #3A9A9E): "③ 消费端"
- Title (T4 bold): "AI 工具"
- Four horizontal product pills in 2×2 grid (~44% width each):
  - "Claude Code" (#0D6B6E border, teal tint fill)
  - "Cursor" (#3A9A9E border)
  - "OpenClaw" (#5CB5B8 border)
  - "Codex / 其他" (#7CC4C7 border)
- Each pill: 8-9px text, rounded, 1px border, left-aligned icon placeholder
- Label below (T6): "工具会换，知识不会"

INTER-STAGE ARROWS:
- Stage 1 → Stage 2: thick teal arrow (#0D6B6E), 3px, solid, with label "adapt" (T6)
- Stage 2 → Stage 3: thick teal arrow (#1A7E81), 3px, solid, with label "translate" (T6)

═══════════════════════════════════════
BAND 4 — MAINTENANCE LOOP (80%–100%)
"[三：谁在维护 — knowledge-keeper 与自动压缩]"
Background: white
═══════════════════════════════════════

Section title (T3): "[三：谁在维护 — knowledge-keeper 与自动压缩]" bold #0D6B6E, left-aligned with small robot/agent icon

TWO-PART LAYOUT:

LEFT HALF (~3%–48%): knowledge-keeper Agent Card
- Rounded rectangle, #F4FAFA fill, 2px #0D6B6E border
- Header: teal pill badge "knowledge-keeper" white on #0D6B6E
- Title (T4 bold): "知识维护智能体"
- Body (T5, 3 bullets with tiny icons):
  - "🔍 检测知识漂移：代码与 knowledge/ 矛盾"
  - "📤 提炼新约定：从实践中提炼，写入 standards/"
  - "🗄️ 归档旧标准：移入 archive，不删除"
- Bottom annotation (T6): "不修改代码，只更新 knowledge/ 和 docs/"

RIGHT HALF (~52%–97%): auto-context-compression Flow
- 4-step clockwise loop (rounded rect nodes ~80×40px each, #EAF5F5 fill, 1px #B0D4D6 border):
  - Step 1 "扫描" — magnifying glass icon, scans knowledge/ + features/ + docs/
  - Step 2 "判重" — equals icon, 语义近似 + 结构重叠
  - Step 3 "判旧" — clock icon, 与 INDEX.md 状态不一致
  - Step 4 "建议" — document+star icon, 合并/归档/删除建议 (需人工审查)
- Curved arrows connecting steps clockwise, teal #3A9A9E, 2px
- Label in center of loop (T6): "onecxt compress"
- Bottom note (T6, gray): "维护者每周回顾 · 大 feature 合并后收敛 · 新人入职减少困惑"

═══════════════════════════════════════
COLOR PALETTE SUMMARY
═══════════════════════════════════════
| Role                  | Hex       |
|-----------------------|-----------|
| Background            | #FFFFFF   |
| Band 2 fill           | #F4FAFA   |
| Primary teal          | #0D6B6E   |
| Secondary teal        | #1A7E81   |
| Tertiary teal         | #3A9A9E   |
| Light teal            | #5CB5B8   |
| Ice teal              | #7CC4C7   |
| Ice teal fill         | #EAF5F5   |
| Card border           | #B0D4D6   |
| Section header        | #0D6B6E   |
| Dark text             | #1A1A1A   |
| Secondary text        | #4A4A4A   |
| Body text             | #3A3A3A   |
| Small label           | #666666   |
| Annotation            | #888888   |
| Terminal bg           | #2C2C2C   |
| Terminal text         | #E0E0E0   |
| Badge fill            | #0D6B6E   |
| Badge text            | #FFFFFF   |

═══════════════════════════════════════
DESIGN ATOMS APPLIED
═══════════════════════════════════════
色彩策略：同色系分层（teal 四级：#0D6B6E → #3A9A9E → #7CC4C7 → #D6EEEF）
布局骨架：中心放射（Band 2）+ 多栏流水线（Band 3）+ 闭环循环（Band 4 右）
信息层级：五级标准 + knowledge/ hub 为焦点元素 + 徽章编号 1-5
连接语言：粗实线=核心数据流，细虚线=弱依赖，颜色跟随起点 teal 变体，手绘曲线
元素词汇：圆角矩形=目录，终端块=CLI 命令，药丸=标签，折角文档=文件产物
情绪基调：专业蓝图风
```