# Prompt: exemplar-codex-agent-loop-part3-sse-tool-flow

> 100% 视觉还原提示词，对应 `exemplar-codex-agent-loop-part3-sse-tool-flow.png`

```
Create a vertical-portrait infographic (roughly 3:4 aspect ratio, approx 1080×1440 px) with a clean, modern technical-diagram aesthetic combining flat illustration with subtle hand-drawn/sketch elements (wavy flowing arrows). The overall color theme is deep purple / magenta (#5B2D8E, #7B3FA0, #9B59B6) on a white background.

═══════════════════════════════════════
GLOBAL STYLE
═══════════════════════════════════════
- Background: pure white (#FFFFFF)
- Primary accent color: deep purple (#5B2D8E)
- Secondary accent: magenta-purple (#7B3FA0 to #9B59B6 gradient)
- Tertiary accent: soft lavender (#E8D5F5) for background fills
- Text color: near-black (#1A1A1A) for body, deep purple (#5B2D8E) for headings
- Dark terminal blocks: very dark gray (#1E1E2E) with green/white monospace text
- Font family: Chinese headings in bold Hei-style sans-serif (similar to PingFang SC Heavy); English in clean sans-serif (similar to Inter or Helvetica Neue); monospace (Menlo / SF Mono) for code blocks
- Font size hierarchy: main title ~36px bold, section headers ~22px bold, body labels ~13px regular, code text ~11px monospace
- Icon style: simple line-art icons in purple (#5B2D8E), ~24-32px; robot/gear/brain icons use a sketch style
- Arrow style: flowing wavy/curved arrows with purple-to-magenta gradient (#7B3FA0 → #C76DD7), stroke width ~3-4px, filled triangular arrowheads; some arrows have a hand-drawn wiggle feel
- Connector lines between nodes: thin solid lines (#5B2D8E), ~1.5px, with small filled-circle endpoints or arrowheads
- Circle nodes: white fill with purple (#5B2D8E) 2px border, ~40px diameter, containing letter labels (A, B, C) in purple bold
- Rounded rectangles for entity boxes: white fill, 1.5px purple border, ~8px corner radius
- Section dividers: horizontal lines spanning full width, thin (#D0D0D0), separating the three major content sections

═══════════════════════════════════════
TOP HEADER (占画面顶部 ~8%)
═══════════════════════════════════════
- Position: top-left aligned, full width, with ~20px left padding
- Line 1 (main title): "执行流：从 SSE 到工具调用" in bold black (#1A1A1A), ~36px font, Chinese characters, left-aligned
- Line 2 (subtitle): "Unrolling the Codex Agent Loop - Part 3/4" in regular weight, dark gray (#444444), ~16px, English, left-aligned, ~4px below title
- A thin horizontal separator line (#D0D0D0) spans below the subtitle area to delineate from the first section

═══════════════════════════════════════
SECTION 1: SERVER-SENT EVENTS (SSE) 实时流 (占画面 ~32%, from ~8% to ~40%)
═══════════════════════════════════════

Section Header:
- "Server-Sent Events (SSE) 实时流" in bold purple (#5B2D8E), ~20px, left-aligned at ~20px from left edge

Layout: Left-to-right flow diagram with three main entities

Left entity — "Model Server" (~15% from left, vertical center of section):
- A stylized server/cloud icon in purple line-art, roughly 60×50px
- Below it: label "Model Server" in purple (#5B2D8E) bold, ~13px

Center area — Three flowing arrows fanning out rightward from Model Server:

Arrow 1 (top path, curving upward then right):
- Label above arrow: "1) output_text.delta" in bold dark text (~12px), second line "text chunks" in regular gray (#666666) ~11px
- Arrow style: wavy/flowing purple gradient line (#7B3FA0 → #C76DD7), ~3px stroke, curves upward from server then sweeps right
- Arrowhead points toward the right side

Arrow 2 (middle path, slight downward curve then right):
- Label: "2) reasoning_summary" in bold (~12px), second line "reasoning" in regular gray ~11px
- Arrow flows from server in a gentle S-curve to the center-right area

Arrow 3 (connecting to step 3 on the right):
- "3) output_item.done" with subtitle "completion signal"

Center element — Database/encrypted storage icon:
- Position: center of the section, slightly below the middle path
- A cylindrical database icon in purple line-art, ~30px wide
- Label below: "后台记录" line 1, "(Encrypted)" line 2, in gray (#666666) ~11px
- A small robot icon sits near this, ~20px, purple

Right side — Terminal/UI mockup box (~60-85% from left):
- A rounded-corner rectangle (~200×80px), very light lavender fill (#F5F0FA), thin purple border
- Top text inside: "实时显示在屏幕" in small gray text ~10px
- Below: "...The execution flow" in monospace ~11px, dark text
- Label below the box: "Codex Client UI" in purple bold ~12px

Far right — Action badge:
- A rounded pill/badge shape with purple fill (#5B2D8E), white text inside: "触发下一步" (~12px bold)

Connecting flow logic:
- Arrow 1 flows from Model Server up-right to the Client UI box
- Arrow 2 flows from Model Server center-right, passing near the database icon
- Arrow 3 points toward the "触发下一步" badge

═══════════════════════════════════════
SECTION 2: 保持思维连续性 (占画面 ~25%, from ~40% to ~65%)
═══════════════════════════════════════

Section Header:
- Background: a soft lavender banner (#F0E6F6) spanning the full width, ~30px tall
- "保持思维连续性" in bold purple (#5B2D8E), ~20px, left-aligned with ~20px padding

Layout: Horizontal 3-node flow diagram (A → B → C → back to next round)

Left node — "Model" entity:
- Position: ~10% from left
- Icon: a simplified robot/AI brain icon in purple line-art (~40px)
- Label below: "Model" in purple bold ~13px

Node A (circle):
- Position: ~25% from left
- White circle, purple 2px border, ~36px diameter
- Letter "A" inside in purple bold ~14px
- Label below: "reasoning_summary_text" in dark text ~11px
- Below that: "type=reasoning" in gray italic ~10px

Flowing arrow from Model → A:
- Wavy purple gradient arrow from the Model icon rightward to circle A

Node B (circle):
- Position: ~55% from left
- Same style: white circle, purple border, "B" inside
- Label above: "Client" in purple bold ~13px (with a small monitor/screen icon)
- Label to the right: "encrypted_content" line 1, "(Saved)" line 2, in gray ~11px

Arrow A → B:
- A flowing purple arrow from A to B, horizontal, slightly wavy

Node C (circle):
- Position: ~25% from left, SECOND ROW below A (about 50px lower)
- White circle, purple border, "C" inside
- To the left: "Next Round" label with curved-arrow refresh icon
- Below: "Model" label with small robot icon
- To the right: "encrypted_content" and "(Saved)" labels in gray ~11px

Arrow B → C:
- A curved arrow going from B downward-left to C, creating a loop-back visual

Annotation box (bottom-right of this section):
- Rounded rectangle with light lavender fill (#F0E6F6), thin purple border
- Text: "让模型'记得'之前的思考过程，同时保持零数据保留 (ZDR) 合规。" ~11px, dark gray (#333333)

═══════════════════════════════════════
SECTION 3: TOOL CALL LOOP (占画面 ~30%, from ~65% to ~95%)
═══════════════════════════════════════

Section Header:
- "Tool Call Loop" in bold purple (#5B2D8E), ~22px, left-aligned

Layout: 4-step numbered flow in a rectangular clockwise cycle (1→2→3→4→back to 1)

Step 1 — "Trigger" (top-left, ~5-35% from left, ~70% from top):
- "1." in large purple bold + "Trigger" in purple bold ~16px
- Small lightning bolt icon (⚡) in purple
- Dark terminal block (rounded rect, ~180×50px, background #1E1E2E):
  - "function_call event received" in light gray/white monospace ~11px
  - "name: run_shell, args: ls -la" in green (#4EC9B0) monospace ~11px

Step 2 — "Execute" (top-right, ~55-95% from left, ~70% from top):
- "2." + "Execute" in purple bold ~16px
- Dark terminal block (~220×70px, background #1E1E2E) with macOS dots (red/yellow/green):
  - "total 8" in white monospace
  - "drwxr-xr-x  2 user  user  4096 May 20 10:00 ." etc.
  - "-rw-r--r--  1 user  user   220 May 20 18:00 file.txt"

Arrow Step 1 → Step 2: horizontal purple arrow pointing right

Step 3 — "Backfill" (bottom-right, ~55-95% from left, ~85% from top):
- "3." + "Backfill" in purple bold ~16px, "Format & Append" annotation in gray italic
- Dark terminal block (~220×60px, background #1E1E2E):
  - "function_call_output: {" + formatted ls output as JSON

Arrow Step 2 → Step 3: vertical purple arrow pointing downward

Step 4 — "Recurse" (bottom-left, ~5-35% from left, ~85% from top):
- "4." + "Recurse" in purple bold ~16px
- Circular refresh arrow icon in purple
- "New HTTP Request" pill badge, lavender fill (#F0E6F6), purple border
- Chinese text: "新请求包含旧请求作为精确前缀 → 触发缓存!"

Arrow Step 3 → Step 4: horizontal purple arrow pointing left
Arrow Step 4 → Step 1: curved purple arrow going upward (completing the loop)

═══════════════════════════════════════
BOTTOM NAVIGATION BAR (占画面底部 ~5%)
═══════════════════════════════════════
- Full-width bar, deep purple background (#3D1A5E)
- Height: ~40px
- Four items evenly spaced:
  1. "1. 核心机制" — white text, regular, ~13px
  2. "2. Prompt 构建" — white text, regular
  3. "3. 执行流" — HIGHLIGHTED: bright magenta (#E91E90) background pill, white bold text
  4. "4. 性能优化" — white text, regular

═══════════════════════════════════════
VISUAL FLOW & COMPOSITION
═══════════════════════════════════════
- Section 1 (SSE): left-to-right fan-out arrow pattern — dynamic data streaming feel
- Section 2 (Continuity): triangular A→B→C node layout — cyclic memory pattern
- Section 3 (Tool Call Loop): rectangular 4-step clockwise cycle — state machine feel
- Purple gradient wavy arrows in Section 1 vs straight/angular arrows in Section 3 create visual contrast
- Dark terminal blocks (#1E1E2E) provide strong contrast against white background
- Lavender banner (#F0E6F6) in Section 2 provides a gentle color break
```
