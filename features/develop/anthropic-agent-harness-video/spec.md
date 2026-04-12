---
id: anthropic-agent-harness-video
title: Anthropic Agent Harness 哲学口播视频
status: draft
category: develop
primary_repo_id: one-context
owner: ""
updated: "2026-04-11"
---

# 概述

面向 B站 / 抖音 / 视频号的一条 **约 5~8 分钟** 深度解析口播视频，拆解 Anthropic 的 Agent Harness 哲学——即「LLM + 工具 + 循环」的最小智能体架构范式。内容源自 Anthropic 官博 "Building Effective Agents"（2024.12）、Claude Computer Use、Claude Code 开源实践，以及社区解读。口播脚本与幻灯文案落在 `production/`。

# 核心内容骨架

1. **什么是 Harness**：LLM 不是 Agent；套上「循环 + 工具 + 安全边界」的壳才是——这就是 Harness。
2. **Agentic Loop**：think → act（tool call）→ observe → repeat；与一次性推理的本质区别。
3. **Workflow vs Agent**：编排式（5 种模式：链式 / 路由 / 并行 / 编排-工人 / 评审-优化）vs 自主循环；何时用哪个。
4. **工具设计哲学**：工具即 API 契约——清晰的 schema、原子性操作、幂等优先；Claude Code 的 Bash/Read/Write/Glob 为范例。
5. **安全 Harness**：沙箱、权限审批、超时、上下文压缩——没有安全边界的 Agent 是生产灾难。
6. **一句话总结**：Keep it simple → 简单到只需 harness，复杂到能处理一切。

# 目标与非目标

## 目标

- 产出可执行的口播脚本（含时间轴、分镜提示）。
- 幻灯文案与口播逐段对齐，支持 `skills/html-video-from-slides` 的 wav-auto 流程。
- 技术引用有据可查（标注来源：Anthropic 官博 / Claude Code 源码 / 社区解读）。

## 非目标

- 不做动画或录屏演示（纯口播 + 幻灯成片）。
- 不覆盖多 Agent 编排（MCP / A2A 等），留作后续选题。

# 用户与场景

- AI 开发者 / 架构师 / 技术管理者，想理解「为什么 Anthropic 选择 harness 而非 planning-based agent」。
- 视频可作为 one-context 的 Agent Framework 知识层配套内容。

# 验收标准

- [ ] `production/` 内含口播脚本（voiceover-script.md）、时间轴、幻灯文案。
- [ ] 技术事实点已与 Anthropic 官方来源核对。
- [ ] `features/INDEX.md` 已登记本需求。
- [ ] 口播时长控制在 5~8 分钟（约 1200~2000 字中文口播稿）。

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: one-context
- **分支 / PR**: —
- **主要路径或模块**: `features/develop/anthropic-agent-harness-video/production/`

# 关联

- **Workspace**: —
- **其他需求目录**: 与 `features/develop/claudecode-source-analysis/` 同源参考；与 `features/develop/one-context-intro-short-video/` 共用成片流水线 `skills/html-video-from-slides/`。

# 开放问题

- 口播语言：全中文 / 是否保留英文术语原词（如 harness, agentic loop, tool call）。
- 是否需要先出一版文字版博客再改口播脚本（降低事实错误风险）。