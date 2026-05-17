---
id: hermes-agent-short-video
title: Hermes Agent 短视频口播成片
status: 发布
category: content-pipeline
primary_repo_id: one-context
owner: ""
updated: "2026-04-09"
---

# 概述

基于下载目录最新口播 WAV（已复制到 `production/voiceover.wav`），使用仓库技能 `skills/html-video-from-slides` 的 **wav-auto** 流程生成 1920×1080 讲解视频。幻灯文案需与口播逐段对齐，否则 Whisper 对齐可能退化为均分时长。

# 目标与非目标

## 目标

- [ ] 补全 `production/presentation.html` 各页 `.slide` 可见文字，与 `voiceover.wav` 内容一致或可前缀匹配。
- [ ] 在技能目录执行：`node cli.js wav-auto --project "…/production"`，产出 MP4（配置见 `video-input.json`）。
- [ ] 成片前按 SKILL 要求校对 `sub.srt`，必要时写入 `srtReplacements` 后重烧。

## 非目标

- 不修改 `repos/` 内业务仓库代码（本需求为内容成片）。

# 用户与场景

内部短视频口播素材快速入库 one-context，便于复用统一流水线。

# 验收标准

- [ ] `production/` 内含 `presentation.html`、`voiceover.wav`（单 wav）、`video-input.json`。
- [ ] 导出 MP4 路径与 `video-input.json` 中 `outputFile` 一致；字幕烧录策略符合配置。

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: one-context（技能与素材路径在本伞仓）
- **分支 / PR**: （按需）
- **主要路径或模块**: `features/content-pipeline/hermes-agent-short-video/production/`、`skills/html-video-from-slides/cli.js`

# 关联

- **Workspace**（`meta/workspaces.yaml` id，如有）:
- **其他需求目录**（跨类别时链接主从）:

# 开放问题

- 口播实际分段与当前占位页数是否一致；若不对齐需增删幻灯或改用 `srt-map` / 手写 `wav-durations.json`。
