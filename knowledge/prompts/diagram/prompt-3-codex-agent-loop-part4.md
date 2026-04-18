---
prompt_id: 3
slug: codex-agent-loop-part4-cache-compression
exemplar_image: images/exemplar-codex-agent-loop-part4-cache-compression.png
tags: [技术解析(对比)]
prompt_language: en
---

# Prompt: exemplar-codex-agent-loop-part4-cache-compression

> 100% 视觉还原提示词，对应 `exemplar-codex-agent-loop-part4-cache-compression.png`

```
Create a vertical-portrait technical infographic (aspect ratio ~3:4, target resolution 1280×1714px) with four major content sections stacked vertically, using a warm orange/earth-tone color scheme on a white base background.

═══════════════════════════════════════
GLOBAL STYLE
═══════════════════════════════════════
- Canvas: white (#FFFFFF) base, 1280×1714px
- Primary accent: warm orange (#E87A3A ~ #D2691E gradient range)
- Secondary accents: red (#CC3333) for negative/warning, green (#4CAF50) for positive/success
- Lego block colors: red (#CC3333), yellow (#F5C542), green (#4CAF50), blue (#4A90D9)
- Dark text: near-black (#1A1A1A) for headings, dark gray (#333333) for body
- Light gray: #F0F0F0 for section background fills
- Dark charcoal section: #2C2C2C for the Zero Data Retention band
- Font: clean sans-serif (PingFang SC / Source Han Sans), all Chinese text with occasional English labels
- Icons: flat/filled style, monochrome dark gray or white depending on section background
- Section dividers: subtle horizontal rules or background color changes between the four main blocks
- Top-right corner annotation: "1280x1714px" in small gray text (~11px)

═══════════════════════════════════════
TOP BANNER / HEADER (占画面顶部 ~8%)
═══════════════════════════════════════
- Full-width gradient header bar: left-to-right warm orange gradient (#E8863A → #D2691E), height ~120px
- Centered large bold Chinese title: "性能与优化：缓存与压缩" in bold black (#1A1A1A), ~38px
- Below the title: italic English subtitle "Unrolling the Codex Agent Loop - Part 4/4" in dark gray, ~16px
- The orange bar has very slight rounded bottom corners
- Top-right corner: "1280x1714px" in light gray (#AAAAAA), ~10px

═══════════════════════════════════════
SECTION 1: PROMPT CACHING (占画面 ~28%)
Background: white (#FFFFFF)
═══════════════════════════════════════

Section title: "Prompt Caching" in bold black (#1A1A1A), ~26px, left-aligned.

LEFT SUB-AREA: Two Coordinate Graphs (左侧 ~55%):

CHART 1 (left):
- X-Y axis, thin black lines (~1.5px)
- Y-axis label (vertical): "(N) 回合耗时" ~11px
- X-axis label: "请求次数" ~11px
- RED curve (#CC3333, ~2.5px) exponential sweep upward
- "O(N²)" in bold red ~14px, "无缓存" in red ~12px

CHART 2 (right):
- Same axes style
- GREEN curve (#4CAF50, ~2.5px) nearly linear/sub-linear
- "O(N)" in bold green ~14px, "有缓存" in green ~12px

Between/above charts — Yellow warning box:
- Background #FFF3CD, border #E8A020 ~1.5px, rounded corners ~6px
- "⚠ 警告 (WARNING):" in bold dark text ~12px
- "MCP 工具列表顺序必须确定！" ~11px
- "顺序改变 = 缓存失效" ~11px

RIGHT SUB-AREA: Static/Dynamic Zone Panel (右侧 ~45%):

TOP BOX — STATIC ZONE:
- "命中率 100% (100% Hit Rate)" in bold green (#4CAF50) ~13px
- Light green box (#E8F5E9), rounded ~8px, green border (#4CAF50)
- "STATIC ZONE (静态区域)" bold dark text ~12px
- Three pill badges: "Instructions (指令)", "Tools (工具)", "Base Context (基础上下文)"

BOTTOM BOX — DYNAMIC ZONE:
- Light red/pink box (#FDEDEC), rounded ~8px, red border (#CC3333)
- "DYNAMIC ZONE (动态区域)" bold dark text ~12px
- Three pills: "User Context (用户上下文)", "History (历史记录)", "Recent Messages (最近消息)"
- "命中率低 (Low Hit Rate)" in red ~11px

═══════════════════════════════════════
SECTION 2: CONFIGURATION CHANGES (占画面 ~22%)
Background: very light warm gray (#F5F5F0)
═══════════════════════════════════════

Section title: "Configuration Changes" bold black, ~24px.

LEFT HALF — "错误做法 (WRONG)":
- Large red X (❌) ~30px, "错误做法 (WRONG)" bold red ~16px
- WRONG SCENARIO 1: three stacked Lego bricks (Base A=blue #4A90D9, Base B=yellow #F5C542, New C=red #CC3333)
- WRONG SCENARIO 2: New C inserted in middle, "修改之前的消息 → 破坏前缀" annotation

RIGHT HALF — "Codex 做法":
- Large green checkmark (✅) ~30px, "Codex 做法" bold green ~16px
- CORRECT SCENARIO: four bricks with "New D" appended at end, "末尾追加 → 保留前缀" annotation

LEGO BRICK STYLE:
- Each brick ~80×30px, rounded ~4px, two circular studs on top
- Slight 3D shadow (darker bottom/right edge)
- Bold white text centered inside each brick

═══════════════════════════════════════
SECTION 3: CONTEXT COMPACTION (占画面 ~24%)
Background: white (#FFFFFF)
═══════════════════════════════════════

Section title: "Context Compaction" bold black, ~24px.

Four-step horizontal flow left to right:

STEP 1 — "超限 (Overflow)":
- Orange circle with white "1." (~28px, fill #E8863A)
- "超限" bold ~16px, "(Overflow)" gray below
- Document icon with orange warning exclamation
- "History too long (历史记录过长)" gray ~10px

→ Dark gray arrow (~2px, solid) →

STEP 2 — "API 调用":
- Orange circle "2."
- "API 调用" bold ~16px
- API badge: "/responses/compact" monospace on light gray (#EEEEEE)

→ Arrow →

STEP 3 — "转换":
- Orange circle "3."
- "转换" bold ~16px
- Two icons: funnel "compaction object" → lock icon "encrypted state (加密状态)"

→ Thicker arrow (~3px) →

STEP 4 — "替换":
- Orange circle "4."
- "替换" bold ~16px
- Three stacked bars: "Instructions" (light orange #FDE8D0), "Compressed Object" (light gray #E8E8E8), "Latest Messages" (light blue #D6EAF8)
- Formula: "New prompt = instructions + compressed object + latest messages" ~10px

═══════════════════════════════════════
SECTION 4: ZERO DATA RETENTION (占画面 ~12%)
Background: dark charcoal (#2C2C2C), full-width band
═══════════════════════════════════════

"Zero Data Retention" bold white ~22px.

LEFT: circular lock icon (~60px) with green (#4CAF50) border, white lock inside, small circular arrows around it
- "无状态设计 (Stateless)" bold white ~14px
- "encrypted_content 在客户端和服务器间往返，服务端不落盘" white ~11px

RIGHT: round-trip diagram
- "Client (客户端)" rounded rect, light gray → "encrypted_content" white arrow right → "Server (服务端)" cylinder
- Return arrow: "encrypted_content response" white arrow left
- Arrows white (#FFFFFF), ~1.5px

═══════════════════════════════════════
BOTTOM NAVIGATION BAR (占画面底部 ~6%)
═══════════════════════════════════════
- Light gray background (#F0F0F0), height ~60px
- Four items centered:
  1. "1. 核心机制" — dark gray (#555555), ~14px
  2. "2. Prompt 构建" — dark gray
  3. "3. 执行流" — dark gray
  4. "4. 性能优化" — HIGHLIGHTED: orange pill (#E8863A), white text, rounded ~16px

═══════════════════════════════════════
VISUAL HIERARCHY
═══════════════════════════════════════
1. Orange header banner (warm, bold eye-catch)
2. Red vs Green curve comparison (high contrast data viz)
3. Colorful Lego bricks (playful, memorable metaphor)
4. Four-step numbered flow (clear sequential process)
5. Dark charcoal ZDR band (contrast shift, signals importance)
6. Orange-highlighted nav item (current page indicator)
7. Yellow warning box (urgency callout)
8. Green STATIC ZONE vs red DYNAMIC ZONE (semantic color coding)

═══════════════════════════════════════
DESIGN ATOMS APPLIED
═══════════════════════════════════════
色彩策略：C 暖冷对比双色（橙色 #E87A3A 主调 + 红 #CC3333/绿 #4CAF50 语义对比）+ D 主题色+深色反转带（ZDR 深色条带 #2C2C2C）
布局骨架：C 分段堆叠（四段垂直：Caching → Config → Compaction → ZDR）+ E 对比并排（Section 2 错误 vs 正确做法）
信息层级：五级标准 + 徽章编号（橙色圆圈 1-4）+ 焦点元素（红/绿曲线对比图 + 乐高积木）
连接语言：中等直线箭头=步骤流转（灰/橙 2px），颜色跟随语义（红=错误，绿=正确，橙=流程）
元素词汇：坐标图=性能对比，乐高积木=可拼装模块（比喻性），终端块=代码，警告框=注意事项，深色条带=安全/合规
情绪基调：C 技术架构风 + 教学图鉴感（严肃数据 + 趣味乐高隐喻并存）
```

## 使用说明

- **适用工具**: Claude Artifacts (SVG/HTML), DALL-E 3, Midjourney v6+
- **推荐尺寸**: 1280×1714px 或等比缩放
- **风格关键词**: warm orange, technical infographic, Lego metaphor, data visualization
- **注意事项**: 乐高积木的 3D 感（顶部圆柱凸起 + 侧面阴影）是视觉记忆点，不要简化为纯色矩形；ZDR 深色条带的反转效果是节奏变化关键
