# Diagram Examples - 1:1 Replication Prompts

基于 diagram-examples 下的 6 张参考图片生成的 1:1 复刻提示词。
重点复刻图片的结构、样式、配色、组件和视觉元素。

---

## 图1: exemplar-ai-colleague-to-skill-pipeline

```
Create a horizontal left-to-right process flow diagram with a hand-drawn sketch aesthetic.

LAYOUT: White background, flow moves horizontally from left to center to right.
COLOR PALETTE: Teal/cyan (#3CB9B2) as primary accent, dark gray text, light gray subtitles.

TOP SECTION:
- Large bold black Chinese title (32px equivalent)
- Gray subtitle with arrow symbols: "信息收集 → 双线抽象 → Skill 装配"
- Small sticky note label "高层流程总览" with curved arrow pointer top-right

LEFT BLOCK (Input):
- Heading "输入同事信息" with curved arrow
- Upper box: Person icon + text fields "姓名/岗位/职级", hand-drawn box corners
- Middle box: Brain icon + "MBTI/标签/主观印象"
- Lower element: Stack of 3 document icons with chat bubbles (blue checkmark)
- Source label at bottom: "飞书/钉钉/邮件/PDF/聊天记录" with icons

CENTER BLOCK (Processing):
- Large central rounded rectangle "同事蒸馏流程" with gear icon
- Curved arrow from bottom pointing up with text "把零散材料变成结构化规则"
- Incoming teal arrows from all three left elements

RIGHT BLOCK (Output):
- Heading "双线抽象"
- Two document boxes stacked vertically:
  - Top: "work.md" with document icon, text "工作方法/技术规范/流程经验"
  - Bottom: "persona.md" with document icon, text "表达风格/决策模式/人际行为"
- Teal arrows flowing from center to documents
- Final element: Highlighted file icon "SKILL.md" with path "colleagues/{slug}/" in glowing teal/orange border
- Label "可直接调用的电子同事" with arrow

ARROWS: Thick organic teal arrows with slight curves, dual-lined in places, showing flow direction.

BOTTOM SECTION:
- Three-phase timeline: "先收集" → (teal arrow) → "再抽象" → (teal arrow) → "后运行"
- Each phase in bold black text

STYLE NOTES: Slightly tilted elements (2-3 degrees), sketchy hand-drawn borders, subtle shadows, organic curved connectors, professional infographic feel.
```

---

## 图2: exemplar-codex-agent-loop-part3-sse-tool-flow

```
Create a vertically stacked technical architecture diagram with 3 main horizontal sections.

LAYOUT: Vertical stack, full-width sections, purple/magenta color scheme.
COLOR PALETTE: Pink to purple gradient (#E87EAD to #9B59B6), deep purple backgrounds (#2D1B4E), white text, black terminal boxes.

TOP BANNER:
- Full-width gradient background (pink to purple)
- Large white Chinese title: "执行流：从 SSE 到工具调用"
- English subtitle: "Unrolling the Codex Agent Loop - Part 3/4"

SECTION 1 - SSE FLOW:
- Light purple/lavender background
- Title: "Server-Sent Events (SSE) 实时流"
- Left: Server rack icon "Model Server" with horizontal magenta gradient bar flowing right
- Three branching data streams:
  1) Upper: "output_text.delta text chunks" → flowing to "Codex Client UI" window (purple header, macOS dots)
  2) Middle: "reasoning_summary reasoning" → flowing to database icon "后台记录 (Encrypted)"
  3) Lower: "output_item.done completion signal" → purple button "触发下一步"
- Magenta flow arrows with particle effects

SECTION 2 - CONTINUITY:
- Dark purple background section
- Title: "保持思维连续性"
- Horizontal flow: Model icon → reasoning_summary_text document → Client icon → encrypted_content document
- Circular loop arrow marked "A" throughout
- Label boxes: "type=reasoning", "encrypted_content (Saved)"
- Bottom loop: Next Round Model receives saved content (arrow marked "a")
- Text box: "让模型'记得'之前的思考过程，同时保持零数据保留(ZDR)合规。"

SECTION 3 - TOOL CALL:
- Light background
- Title: "Tool Call Loop"
- Circular numbered flow (1→2→3→4→1):
  1. "Trigger" - Model + terminal snippet "function_call event received"
  2. "Execute" - Dark terminal window showing "ls -la" command and output
  3. "Backfill" - Terminal showing JSON output with "Format & Append" arrow
  4. "Recurse" - "New HTTP Request" badge with Chinese subtitle
- Connecting arrows with directional flow

BOTTOM NAVIGATION:
- Four items: "1. 核心机制 | 2. Prompt 构建 | 3. 执行流 | 4. 性能优化"
- Item 3 highlighted with purple background and white text
```

---

## 图3: exemplar-codex-agent-loop-part4-cache-compression

```
Create a vertically stacked technical infographic with 4 main sections, warm orange/yellow color scheme.

LAYOUT: White background, horizontal section dividers, warm accent colors.
COLOR PALETTE: Orange header (#F5A623), red warnings (#E74C3C), green success (#27AE60), yellow/beige highlights.

TOP BANNER:
- Orange header bar with "720 x 714px" label top-right
- Large black title: "性能与优化：缓存与压缩"
- English subtitle: "Unrolling the Codex Agent Loop - Part 4/4"

SECTION 1 - PROMPT CACHING:
- Two side-by-side coordinate graphs:
  - Left: Red exponential curve "无缓存 O(N²)", Y-axis "处理时间(N)", X-axis "请求次数"
  - Right: Green horizontal line "有缓存 O(N)", same axes
- Yellow warning box: "⚠ 警告(WARNING): MCP 工具列表顺序必须稳定！顺序改变=缓存失效"
- Right side panel:
  - Green box: "命中率100%" with three icons (Instructions, Tools, Base Context) labeled "STATIC ZONE 静态区域"
  - Pink box: "命中率低" with three icons (User Context, History, Recent Messages) labeled "DYNAMIC ZONE 动态区域"

SECTION 2 - CONFIGURATION CHANGES:
- Title: "Configuration Changes"
- Comparison visualization:
  - WRONG (left, red X marks): Four stacked blocks (A, B, C, New C) with two error scenarios - "破坏前缀" shown
  - RIGHT (right, green ✓): Four blocks with green arrow showing append-only: "Base A → Base B → New C → New D"
  - Chinese label: "Codex 做法"

SECTION 3 - CONTEXT COMPACTION:
- Title: "Context Compaction"
- Four-step horizontal flow:
  1. "1. 超限(Overflow)" - document icon with warning "History too long 历史记录过长"
  2. "2. API 调用" - arrow to "/responses/compact"
  3. "3. 转换" - funnel icon, documents labeled "compaction object" → "encrypted state 加密状态" with lock
  4. "4. 替换" - stack showing: Instructions + Compressed Object + Latest Messages
- Formula: "New prompt = Instructions + compressed object + latest messages"

SECTION 4 - ZERO DATA RETENTION:
- Light blue/gray background section
- Title: "Zero Data Retention"
- Circular lock icon with arrows labeled "无状态设计 (Stateless)"
- Text: "encrypted_content 在客户端和服务器间往返，服务端不落盘"
- Diagram: Client ↔ encrypted_content ↔ Server (round trip with crossed-out server storage)

BOTTOM NAVIGATION:
- Four items: "1. 核心机制 | 2. Prompt 构建 | 3. 执行流 | 4. 性能优化"
- Item 4 highlighted with orange background
```

---

## 图4: exemplar-persona-md-blueprint

```
Create a hub-and-spoke radial diagram with professional blueprint styling.

LAYOUT: Central document/bus icon surrounded by 6 Layer nodes in radial pattern, blue/gray color scheme.
COLOR PALETTE: Steel blue (#4A6FA5), light blue backgrounds, white document panels, gray text.

TOP SECTION:
- Black title: "persona.md 里到底要装什么，AI 才能像一个人那样说话和反应"
- Gray subtitle explaining the concept

CENTRAL HUB:
- Large central rounded rectangle with document/person icon
- Surrounded by curving connector lines to 6 surrounding nodes
- Inner circular flow diagram showing Layer relationships

LAYER NODES (arranged radially):
Each Layer has a numbered badge and color-coded panel:
- Layer 0: "硬规则" (Hard Rules) - document icon, list items
- Layer 1: "身份信息" (Identity) - person card
- Layer 2: "表达风格" (Expression Style) - speech bubble
- Layer 3: "决策与判断" (Decision Making) - flowchart icon
- Layer 4: "人际行为" (Interpersonal) - people icons
- Layer 5: "边界与雷区" (Boundaries) - warning/fence icon
- Layer C: "Correction" - notepad with pencil

CONNECTOR LINES: Curved organic lines connecting center to each Layer, some bidirectional.

BOTTOM SECTION 1:
- Header: "[二：不同风格被抽象成什么样 - persona.md 不是空模板]"
- Four character cards in row showing different personas:
  - Left 1: "强势字节范" (Strong Byte Style)
  - Left 2: "稳健协调型" (Steady Coordinator)
  - Right 1: "白围裙型" (White Apron)
  - Right 2: "完美主义细节控" (Perfectionist)
- Each card with small avatar and bullet points

BOTTOM SECTION 2:
- Header: "[三：persona.md 如何驱动真实对话 - 不同场景会调用哪些具体风格规则]"
- Three interaction flow diagrams showing how different situations trigger different Layer combinations
- Branching decision trees with Layer callouts

STYLE: Clean professional infographic, academic paper feel, subtle shadows, rounded corners on all boxes.
```

---

## 图5: exemplar-work-md-blueprint

```
Create a hub-and-spoke radial diagram focused on work processes, similar structure to persona.md but with work-centric styling.

LAYOUT: Central workstation/laptop icon surrounded by 5-6 capability nodes in radial pattern, darker blue/gray than persona.md.
COLOR PALETTE: Darker steel blue (#3D5A80), navy accents, light gray backgrounds, white panels.

TOP SECTION:
- Black title: "work.md 里到底要装什么，AI 才能像一个人那样工作"
- Gray subtitle explaining work protocol concept

CENTRAL HUB:
- Large document icon representing "work.md 的工作蓝图"
- Speech bubble "这不是简历摘要，这是替代干活时要遵守的工作协议"
- Curved connectors radiating to surrounding modules

SURROUNDING MODULES:
- "职责范围" (Responsibilities) - scope definition with list items
- "工作流程" (Workflow) - process steps with checkmarks
- "技术规范" (Technical Standards) - code/gear icons with requirements
- "输出风格" (Output Style) - document formats and tone
- "经验知识库" (Knowledge Base) - stacked books/lightbulb icons
- Central connector hub

BOTTOM SECTION 1:
- Header: "[二：不同岗位被抽象成什么样 - work.md 不是空模板]"
- Four role cards in horizontal row:
  - Card 1: "前端工程师" (Frontend Engineer) - code brackets icon
  - Card 2: "产品经理" (Product Manager) - product chart icon
  - Card 3: "后端工程师" (Backend Engineer) - server icon
  - Card 4: "算法工程师" (Algorithm Engineer) - formula/icon
- Each card with specific task checklist items

BOTTOM SECTION 2:
- Header: "[三：work.md 如何驱动真实工作 - 不同任务会调用哪些具体规则]"
- Central workflow showing task triggers different module combinations
- Branching paths for different task types with module callouts
- Terminal nodes showing final outputs

STYLE: Corporate/professional aesthetic, consistent rounded panels, clean typography, workflow diagram conventions.
```

---

## 图6: exemplar-work-persona-incident-flow

```
Create a vertical three-stage process diagram with incident response workflow styling.

LAYOUT: Vertical flow with three main columns, light blue/gray color scheme with highlight accents.
COLOR PALETTE: Light blue backgrounds, navy text, yellow/gold warning accents, teal process arrows.

TOP SECTION:
- Large navy title: "线上故障来了，work.md 和 persona.md 怎么一起工作"
- Gray subtitle: "人格定入口，能力做执行，再回到人格包输出"
- Small note top-right: "重点:只解释协同结构，不展开前置来去"

MAIN DIAGRAM - THREE STAGES:
Large horizontal section with dotted border, three vertical columns:

STAGE 1 - "阶段一: Persona 定义入口":
- Light blue header banner
- Document panel labeled "Persona.md"
- Input arrow from left: "输入任务: 告警/问题/初始上下文"
- Warning triangle icon → speech bubble icon
- "人格定入口" label
- Curved teal arrow flowing to Stage 2

STAGE 2 - "阶段二: Work 执行排障":
- Central column with "Work.md" header
- Internal workflow icons (clockwise):
  - Monitor/dashboard icon "看监控"
  - Release/tag icon "查发布"
  - Network diagram "定位链路"
  - Checklist "形成建议"
- Curved teal arrow to Stage 3
- Label: "提问方向和进入姿态" + "每一段都在消费上一段的结果"

STAGE 3 - "阶段三: Persona 包装输出":
- "Persona.md" header
- Two speech bubble icons (dialog format)
- "中间结果: 诊断判断/处置建议" → "人格包输出"
- Final response arrow to right "最终响应: 像这个人说出来的结论"
- Circular stamp: "符合这个性格预设的结论在递送中被执行"

MIDDLE SECTION - DETAILED FLOW:
Horizontal branching flowchart:
- "先问变更/影响面" → branches to "先看监控/发布记录"
- → "缩小异常范围" (branches to "先问最近是否发版" and "异常集中在支付回调链路")
- → "定位链路和依赖" → "形成处置建议" (branches to "建议先回滚并观察")
- Side note: "协同并不增加步骤数量，它改变的是步骤的组织方式和表达方式"

BOTTOM SECTION - COMPARISON:
- Header: "最终效果只看一件事 - 同样的判断，为什么更像真人协作"
- Two side-by-side panels:
  LEFT: "纯 Work 输出" - technical, dry response
  RIGHT: "Work + Persona 输出" - humanized response with personality
- Arrow showing transformation from Work to Work+Persona
- Caption: "人格包输出，能力保正确"
- "先回滚，别硬顶" highlighted in both boxes

STYLE: Incident response documentation aesthetic, clear stage divisions, professional technical diagram, collaborative workflow visualization.
```

---

## 使用说明

这些提示词可直接用于 Claude、Midjourney、DALL-E 或其他 AI 绘图工具，生成与参考图片风格一致的图表。

生成建议：
1. 如果首次生成不完全匹配，可以针对性地调整配色或布局细节
2. 对于中文内容，建议使用支持中文渲染的绘图工具
3. 可适当调整内容以适应具体场景，同时保持视觉风格一致
