---
prompt_id: 13
slug: skillrouter-pipeline-architecture
exemplar_image: images/exemplar-skillrouter-pipeline-architecture.jpg
tags: [论文插图]
prompt_language: en
---

# Prompt: exemplar-skillrouter-pipeline-architecture

> 100% 视觉还原提示词，对应 `exemplar-skillrouter-pipeline-architecture.jpg`
>
> 来源: `assets/alibaba-paper-illustration.jpg` · 论文: SkillRouter (arXiv:2603.22455, Alibaba Group, 2026-03)

```
Create a clean, modern technical architecture diagram titled "Figure 2: SKILLROUTER pipeline architecture" in a soft academic paper illustration style. The diagram has three major columns arranged left-to-right, each with a colored header banner:

### Layout & Visual Style
- Background: off-white / very light warm gray (#F5F5F0) with subtle light gray rounded-rectangle containers for each column
- Style: flat design with minimal soft drop shadows, rounded corners on all boxes
- Color palette: muted olive-green tonal system — dark olive (#4A6A3A) for model boxes, medium olive (#5A7A4A to #6B8E5A) for stage banners, golden amber (#E8C84A) for highlights (e.g. "body" tag), light cream (#FFF8E0) for Task Query card, light gray (#F0F0F0) for track containers, white card surfaces
- Typography: clean sans-serif (similar to Helvetica/Arial), dark gray/black text, bold for headers
- Icons: small emoji-style icons in each column header (wrench, lightning bolt, gear)
- Arrows: thin gray or dark arrows with arrowheads connecting stages, some curved

### Column 1 — "Training" (left, ~30% width)
Header: wrench icon + "Training" in bold

**Track A: Encoder Training** (top sub-section, light blue rounded box):
- Start: "Input Queries & Skills" label at top
- Arrow down to funnel icon labeled "Hard Negative Mining"
- Below funnel: four small tags in a row: "cosine similarity", "BM25", "taxonomy", "random"
- Arrow down to filter icon labeled "3-Layer False Negative Filtering"
- Below filter: small text "name matching → body similarity → embedding cosine"
- Arrow down to a green rounded box with database icon: "SR-Emb-0.6B"
- Below: small text "InfoNCE Loss · In-batch Negatives"

**Track B: Reranker Training** (bottom sub-section, light green rounded box):
- "Input Query Groups with skill candidates" label
- Arrow right to green rounded box: "SR-Rank-0.6B"
- Below: small text "Listwise Cross-Entropy Loss"

### Column 2 — "Inference" (center, ~40% width)
Header: lightning bolt icon + "Inference" in bold

- Top: yellow sticky-note style box "Task Query" with example text "Build a video tutorial indexer that..."
- Label "Input" on arrow pointing down

**Stage 1: Bi-Encoder Retrieval** (olive-green banner box):
- Left side: "[q] → embedding →" with a small model icon labeled "0.6B"
- Right side: "~80K Skills" with a grid of small document icons labeled "pre-computed"
- Center: "Cosine Similarity" connecting query embedding to "Massive Skill Pool"
- Bottom output: "Top-20 Candidates" with arrow down, label "top-20"

**Stage 2: Cross-Encoder** (olive-green banner box):
- Left input: "Query" box
- Center: "Skill" with two fields — "name" (small tag) and "body" (small tag)
- Cross-attention visualization: dotted crossing lines between query and skill fields
- Right side: model icon "0.6B"
- Output highlights: "name", "description", "body" as colored tags (body highlighted in yellow/green)
- Bottom output: "Top-K Ranked Skills" arrow going right to column 3

### Column 3 — "Agent Application" (right, ~30% width)
Header: gear icon + "Agent Application" in bold

- Top: two small card-style elements showing skill metadata: "name" + "description" tags (0.6B label nearby)
- Center: large rounded box "LLM Agent" with a brain/gear icon
- Inside LLM Agent box:
  - "System prompt" label at top
  - "Injected Skills" section showing 3-4 small cards each with "name" and "description" fields
  - "User conversation" section at bottom
- Bottom-right: small arrow indicating output/response

### Caption (optional — may be cropped in source image)
Below the diagram: "Figure 2: SKILLROUTER pipeline architecture. Stage 1: bi-encoder retrieval reduces ~80K skills to top-20 candidates. Stage 2: cross-encoder reranking produces the final ranking. Both stages use full skill text (name + description + body)."

### Key Visual Details to Match
1. All three columns are visually balanced with equal spacing
2. Arrows flow naturally: left column feeds into center, center feeds into right
3. The "0.6B" model size badges appear as small rounded pills in olive-green near model icons
4. Stage banners use medium olive-green (#5A7A4A to #6B8E5A) with white text
5. The overall feel is clean, academic, and highly readable — not flashy
6. Subtle use of icons (funnel, filter, database, document grid, gear) to aid comprehension
7. The training column shows two parallel tracks (A and B) stacked vertically
8. Cross-attention in Stage 2 is visualized with a crossing × symbol between query and skill fields

═══════════════════════════════════════
DESIGN ATOMS APPLIED
═══════════════════════════════════════
色彩策略：B 同色系分层（olive-green 色调：#4A6A3A → #5A7A4A → #6B8E5A + 金色高亮 #E8C84A）
布局骨架：A 多栏流水线（三列左→右：Training → Inference → Agent Application）
信息层级：多级标准 + 药丸徽章（0.6B 模型大小）+ 焦点元素（Stage 1/2 为中心列视觉重心）
连接语言：细直线箭头=阶段间连接（灰/深色 1.5px），部分弧形曲线，颜色统一深灰
元素词汇：圆角矩形=流程阶段，漏斗图标=Hard Negative Mining，网格=文档池（~80K Skills），药丸=标签，stage 横幅=olive-green 白字
情绪基调：B 专业蓝图风 · 学术论文插图变体（扁平设计 + 柔和配色 + 高可读性）
```

## 使用说明

- 适用于: Claude/GPT + 图像生成工具 (如 Artifacts HTML/SVG, DALL-E, Midjourney) 或手动用 Figma/draw.io 复现
- 若用 HTML/SVG 渲染，建议画布尺寸 1200x800px，三列等分
- 配色可微调，核心是保持学术论文插图的柔和、专业风格
