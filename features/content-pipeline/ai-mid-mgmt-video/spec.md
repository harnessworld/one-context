---
id: ai-mid-mgmt-video
title: AI 中视频管理 — 素材与发布工具链
status: draft
category: content-pipeline
primary_repo_id: one-context
owner: ""
updated: "2026-04-11"
---

# 概述

AI 中视频管理—面向管理者和决策者的素材整理与发布工具链，集中管理中视频（3-15 分钟）的口播脚本、幻灯、字幕和发布素材。

# 目标与非目标

## 目标

- 整理 AI 中视频相关素材，统一放入 `production/` 目录结构。
- 发布素材（标题、简介、话题标签）在 `production/content/05-publish-kit.md` 中维护。

## 非目标

- 不在本 feature 内生成成片（成片流程走 `skills/html-video-from-slides`）。
- 不覆盖其他短视频 feature 的内容。

# 用户与场景

需要快速查找和发布 AI 相关中视频素材的内容运营者。

# 验收标准

- [ ] `production/` 目录结构符合 `features/_template/content-production/` 模板。
- [ ] `production/content/05-publish-kit.md` 包含可用的发布素材。

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: one-context
- **分支 / PR**: —
- **主要路径或模块**: `features/content-pipeline/ai-mid-mgmt-video/production/`

# 关联

- **Workspace**（`meta/workspaces.yaml` id，如有）:
- **其他需求目录**: 同类别下其他 `content-pipeline` feature 共用成片流水线。

# 开放问题