---
id: anthropic-agent-harness-narration
title: Anthropic Agent Harness 哲学 — 口播稿
status: draft
category: content-pipeline
primary_repo_id: one-context
owner: ""
updated: "2026-04-11"
---

# 概述

面向**短视频 / 中视频口播**的讲稿需求：用通俗中文解释 Anthropic 工程博客中围绕 **Agent Harness（智能体束具 / 编排层）** 的核心理念——为何单靠更强模型不足以解决长程任务、Harness 承担什么职责、常见失效模式（上下文焦虑、自评偏差、过早收束）与典型结构（如规划 / 生成 / 评估分工、上下文重置与结构化交接、与 Managed Agents 等「元束具」的关系）。口播需**可独立听懂**，并在正文或附录中标注**一手参考链接**便于核对，避免二手转述失真。

**口播音频位置（约定）**：录制完成的 WAV **先落在本机「下载」目录**（Windows 一般为 `%USERPROFILE%\Downloads`，资源管理器显示为「下载」）。走 `skills/html-video-from-slides` 的 **wav-auto** 前，将目录内**用于成片的那一个** `.wav` **复制到**本需求素材目录，命名为 `production/voiceover.wav`（与同目录下 `presentation.html`、`video-input.json` 一并作为 `--project` 指向的文件夹内容）；技能要求**每个项目目录仅一个** WAV，勿在素材目录里留多个 `.wav`。

# 目标与非目标

## 目标

- [ ] 产出一份可照稿录制的口播 Markdown：路径 `production/content/01-script.md`。
- [ ] 结构包含：开场钩子（15–30s 量级）、核心概念分层（Harness 是什么 / 与模型能力的关系）、至少 2 个「失效模式 → 束具层应对」的叙事、收束金句或行动建议。
- [ ] 列明**参考来源**（Anthropic Engineering 等官方文章标题 + URL + 访问日期），口播中区分「Anthropic 公开表述」与「个人归纳」。
- [ ] 给出**预估总时长**（如 3–8 分钟档）及分段时长备注，便于后续对齐幻灯或 `skills/html-video-from-slides` 流水线。
- [ ] 术语表（中英文对照可选）：harness、context reset、handoff、evaluator、meta-harness、brain / hands / session 等。

## 非目标

- 不代表 Anthropic 官方立场；不承诺与某篇博文逐句对应。
- 不要求在本需求内完成 `presentation.html` 或导出 MP4（可与 `hermes-agent-short-video` 或独立成片需求衔接）。
- 不在仓库内长期保存「下载」目录路径下的原始文件；仅以复制进 `production/` 的 `voiceover.wav` 为成片输入。

# 用户与场景

内部知识短视频、频道口播、或对 Agent 工程同事的科普；听众可能不熟悉「Harness」一词，需从日常比喻或工程类比切入。

# 验收标准

- [ ] `narration.md`（或约定的等价路径）存在且为完整口播正文，分段清晰（可用 `##` 或小标题对应气口）。
- [ ] 参考来源章节可追溯至 Anthropic（或其他）原文；无未标注的敏感或商业机密。
- [ ] 全文无与公开资料明显矛盾的技术断言；存疑处列入「开放问题」或口播中口头免责。
- [ ] 若计划走 HTML 幻灯 + wav-auto：在 spec 或口播头注释中注明目标时长与是否需逐页对齐字幕。
- [ ] 成片输入音频：自「下载」目录复制后的 `production/voiceover.wav` 存在且为**唯一** WAV；`wav-auto` 的 `--project` 指向 `features/content-pipeline/anthropic-agent-harness-narration/production/`（或你实际使用的等价素材目录）。

# 内容要点（撰写清单，非口播正文）

撰写时可覆盖以下支柱（顺序可调，不必面面俱到）：

1. **Harness 的定位**：在模型与工具 / 环境之间的控制与编排层；假设会随模型变强而过时，因此接口与状态设计比「某一版提示词」更持久。
2. **长程任务**：多会话、多上下文窗口；compaction 与「完全重置 + 结构化交接」的取舍叙事（面向大众时避免过深，点到即可）。
3. **Anthropic 公开案例线**（按需选用，以原文为准）：长程应用开发的束具设计（如多角色分工、评估与生成分离）；Effective harnesses / initializer + 增量进展类叙述；Managed Agents 与 brain–hands–session 解耦、元束具（meta-harness）等表述。
4. **对听众的 takeaway**：例如「先量失败模式再叠架构」「评测与执行分离」「用可验证工件做交接」等可迁移结论。

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: **one-context**（口播稿与需求说明位于本伞仓 `features/`）。
- **分支 / PR**: （按需）
- **主要路径或模块**: `features/content-pipeline/anthropic-agent-harness-narration/`（口播稿与幻灯成片素材建议放在 **`production/`** 子目录：`presentation.html`、`voiceover.wav`（从**下载**目录拷入）、`video-input.json`）；成片流程见 `skills/html-video-from-slides/SKILL.md` 的 `wav-auto`。

# 关联

- **Workspace**（`meta/workspaces.yaml` id，如有）:
- **其他需求目录**（跨类别时链接主从）: `features/content-pipeline/hermes-agent-short-video/`（若同一批次短视频成片）

# 开放问题

- 成片时长与平台（抖音 / B站 / YouTube）是否已定，影响信息密度与钩子长度。
- 口播是否需英文术语口播或全中文意译，需在 `narration.md` 文首约定。
