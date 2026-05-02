---
id: agent亲和架构底层原理剖析
title: Agent 亲和架构底层原理剖析（口播 / 视频）
status: draft
category: content-pipeline
primary_repo_id: one-context
owner: ""
updated: "2026-04-28"
---

# 概述

围绕「Agent 亲和架构」的中视频口播：从传统架构为何难以承载 AI Agent，到推理与 GPU 调度亲和、工具 / 状态 / 安全等亲和维度。成片依赖口播 WAV、`presentation.html` 与流水线配置。

# 目标与非目标

## 目标

- [ ] 口播 WAV 置于 `production/media/`（文件名与 `timing/video-input.json` 中 `wavFile` 一致）。
- [ ] 校对字幕：`production/subtitles/sub.srt`（当前由 `Agent+亲和架构底层原理剖析.srt` 复制而来；发布前按需校对）。
- [ ] 幻灯 `production/slides/presentation.html`（html-deck-layout / srt-to-deck）。
- [ ] `timing/wav-durations.json` + `timing/video-input.json` 配置齐全后跑 `skills/html-video-from-slides`（wav 或 wav-auto）。
- [ ] 补全 `production/content/00-structure.md`、`01-script.md`、`05-publish-kit.md`。

## 非目标

- 不修改业务代码仓库；成片产出在 `production/`。

# 用户与场景

技术向听众：Agent 基础设施、推理调度与亲和架构科普。

# 验收标准

- [ ] 成片 MP4 路径与 `video-input.json` 的 `outputFile` 一致。
- [ ] 字幕时间轴与口播一致（若仅用外部 SRT，勿改时间轴除非重跑 Whisper）。

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: one-context
- **分支 / PR**: —
- **主要路径或模块**: `features/content-pipeline/agent亲和架构底层原理剖析/production/`

# 关联

- **Workspace**（`meta/workspaces.yaml` id，如有）:
- **流水线**: `skills/html-video-from-slides/SKILL.md`；可选 `skills/html-deck-layout`、`skills/srt-to-deck`。

# 开放问题

- `production/subtitles.srt` 为备用 / 旧导出（时间码格式与标准 SRT 不一致）； canonical 为 `production/subtitles/sub.srt`。确认后可删除根下重复文件以免混淆。
