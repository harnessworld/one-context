---
id: 软件中一切皆Worker
title: 软件中一切皆 Worker（口播视频）
status: 发布
category: content-pipeline
primary_repo_id: one-context
owner: ""
updated: "2026-05-17"
---

# 概述

中视频口播：从 Mike Piccolo Harness 视角讨论 Agent 后端——用 Worker、Trigger、Function 统一语义，把 Agent 与微服务、批任务做成可调度、可观测、可治理的负载。

# 目标与非目标

## 目标

- [x] 维护 `production/slides/presentation.html` 与 `production/subtitles/sub.srt`。
- [x] 维护 `production/timing/wav-durations.json`。
- [ ] 发布素材见 `production/content/05-publish-kit.md`。

## 非目标

- 不在仓库内保留幻灯生成用的一次性 Python 脚本（应走 skill 流水线）。

# 验收标准

- [ ] 幻灯、字幕、翻页配置路径符合 `features/_template/content-production/`。

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: one-context
- **分支 / PR**: —
- **主要路径或模块**: `features/content-pipeline/软件中一切皆Worker/production/`

# 关联

- **Workspace**: —
- **其他需求目录**: —

# 开放问题

- 无
