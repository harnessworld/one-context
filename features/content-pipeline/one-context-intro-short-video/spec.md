---
id: one-context-intro-short-video
title: one-context 中视频介绍（爆款口播框架）
status: draft
category: content-pipeline
primary_repo_id: one-context
owner: ""
updated: "2026-04-02"
---

# 概述

面向抖音 / B站 / 视频号等平台的一条 **约 3 分 20 秒** 中视频，用 **老周 + 小林** 双人问答形式介绍 **one-context**：共享上下文层、多端适配、跨仓 Workspace、Agent 产物链、知识层与轻依赖 CLI。口播脚本与分镜落在同目录 `production/`。

# 目标与非目标

## 目标

- 建立可迭代的 **脚本 + 时间轴 + 镜头清单** 制作框架（见 `production/README.md`）。
- 技术表述与根目录 `README.md` 一致（如 6 个标准智能体、`onecxt adapt/sync/doctor/context export` 等）。
- 成片后可选择：仅保留 umbrella 内素材，或将工程同步到 **`repos/develop/VideoFactory`**（`meta/repos.yaml` 中 `id: VideoFactory`）做剪辑与发布流水线。

## 非目标

- 不在本需求内实现 VideoFactory 代码或自动化渲染。
- 不承诺具体发布日期与平台数据指标。

# 用户与场景

- 希望向多仓 / 多 AI 工具开发者传播 one-context 的贡献者与运营。
- 后续可出「保姆级上手」续集（口播收尾已埋钩子）。

# 验收标准

- [x] `production/` 内 brief、时间轴脚本、镜头清单、素材索引齐备且可执行。
- [ ] 口播事实点已与根 `README.md` 核对（智能体数量、命令名、定位用语）— **录前按 `01` 内核对清单走一遍**。
- [x] `features/INDEX.md` 已登记本需求。

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: `one-context`（主文案与事实来源）；可选协作仓库 `VideoFactory`（剪辑与成片）。
- **分支 / PR**: —
- **主要路径**: `features/content-pipeline/one-context-intro-short-video/production/`；成片流水线见 `skills/html-video-from-slides/`（单入口 `cli.js`，勿在子目录复制脚本）。

# 关联

- **Workspace**（如有）: —
- **对标框架**: 参考 `features/develop/claudecode-source-analysis/` 的文档风格；口播结构可参考「架构拆解」类爆款节奏（前 3 秒炸场、15 秒小高潮）。

# 开放问题

- 成片是否单独进 VideoFactory 仓库目录结构（由 `onecxt sync VideoFactory` 后约定子路径）。
- 口播语言：全程中文 / 是否穿插英文命令名屏幕字。
