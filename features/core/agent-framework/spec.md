---
id: agent-framework
title: "Agent Framework — 智能体框架"
status: in_progress
category: core
primary_repo_id: one-context
owner: architect
updated: "2026-03-31"
---

# 概述

one-context 目前是一个优秀的"上下文控制平面"：它管理多仓注册表、知识层、profile、适配器。但它缺少在这个平面上运作的**工作主体**。

本 feature 为 one-context 引入**智能体（Agent）**作为新的一等公民配置对象，并建立一套跨工具（Cursor / Claude Code / OpenClaw）均可使用的框架规范。

---

# 目标与非目标

## 目标

- 在 `meta/agents.yaml` 中引入智能体注册表，与 `repos`、`workspaces`、`profiles` 并列
- 定义 6 个标准智能体：`pm`、`architect`、`dev`、`qa`、`sre`、`knowledge-keeper`
- 制定产物所有权模型（每个 feature 文件由唯一智能体负责）
- 制定 git worktree 工作约定（Dev 智能体，feature 级别隔离）
- 制定声明式 `deploy.yaml` 约定（SRE 智能体，repo 级别）
- 扩展适配器框架，支持为每个智能体生成 tool-native 配置
- 扩展 CLI：`onecxt agent list/show`、`onecxt adapt-agent`、`onecxt worktree setup/status/teardown`

## 非目标

- 智能体自动调度或状态机（流转由人工触发）
- 智能体间消息传递或 API 通信
- 云端或多人协同（local-first 原则不变）
- 替换现有 profile 系统（智能体引用 profile，不替代）

---

# 用户与场景

**场景 A — 个人多仓开发者**
使用 `@pm` 创建 feature spec，`@dev` 开发，`@qa` 验收，`@sre` 发布。每一步自动有文件落盘，回溯清晰。

**场景 B — 跨工具团队**
成员甲用 Cursor，成员乙用 Claude Code。`onecxt adapt-agent` 为两人生成各自工具原生的智能体配置，行为规格一致，无需重复维护。

**场景 C — 知识维护**
`@knowledge-keeper` 定期扫描知识漂移，从近期 feature 的 tech_design / mr_report 中提炼新约定并更新 `knowledge/standards/`。

---

# 验收标准

- [ ] `meta/agents.yaml` 可通过 `onecxt doctor` 校验（无错误）
- [ ] `onecxt agent list` 输出 6 个标准智能体
- [ ] `onecxt agent show pm` 输出完整字段（profile、knowledge、owns、instructions）
- [ ] `onecxt adapt dev` 在 Cursor / Claude Code / OpenClaw 各自目录生成 `agent-pm.mdc` / `pm.md` / `agent-pm.json`
- [ ] 生成文件内容包含：角色说明、profile 行为规格、knowledge 内容（inline 或引用）、owns 产物清单
- [ ] `onecxt worktree setup <feature-id>` 在涉及的 repo 下创建 worktree，并写入 `worktrees.yaml`
- [ ] `onecxt worktree teardown <feature-id>` 清理 worktree，更新 `worktrees.yaml` status 为 `merged` 或 `abandoned`
- [ ] `deploy.yaml` 模板文件存在于 `docs/templates/deploy.yaml`，字段通过 `onecxt doctor` 校验
- [ ] 知识规范文档 `knowledge/standards/agent-framework.md` 存在且与实现一致

---

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: `one-context`
- **分支 / PR**: `feature/agent-framework`
- **主要路径或模块**:
  - `meta/agents.yaml` — 智能体注册表
  - `knowledge/standards/agent-framework.md` — 权威规范
  - `packages/one-context/one_context/agents.py` — Agent 数据模型与加载逻辑
  - `packages/one-context/one_context/adapters/` — 各适配器扩展（生成 agent 配置）
  - `packages/one-context/one_context/cli.py` — 新增 `agent` 和 `worktree` 子命令
  - `packages/one-context/one_context/worktree.py` — Worktree 管理逻辑
  - `docs/templates/deploy.yaml` — SRE deploy manifest 模板

---

# 关联

- **Workspace**（`meta/workspaces.yaml` id）: —
- **规范文档**: `knowledge/standards/agent-framework.md`
- **相关 profile**: `meta/profiles.yaml`（智能体引用 profile id）
- **相关 feature 模板**: `features/_template/`（PM 智能体使用）

---

# 实现分阶段建议

## Phase 1 — 规范与数据层（当前）
- [x] `knowledge/standards/agent-framework.md` 框架规范落盘
- [x] `meta/agents.yaml` starter 注册表（6 个智能体）
- [ ] `onecxt doctor` 支持校验 `agents.yaml`
- [ ] `onecxt agent list / show` CLI

## Phase 2 — 适配器扩展
- [ ] 各适配器（Cursor / Claude Code / OpenClaw）支持生成 agent 配置文件
- [ ] `onecxt adapt-agent <id>` 命令

## Phase 3 — Worktree 管理
- [ ] `worktree.py` 模块
- [ ] `onecxt worktree setup / status / teardown`
- [ ] `features/.../worktrees.yaml` 自动生成与更新

## Phase 4 — SRE deploy.yaml 支持
- [ ] `deploy.yaml` schema 定义与 doctor 校验
- [ ] `docs/templates/deploy.yaml` 模板
- [ ] SRE 智能体生成配置中注入 deploy.yaml 查找逻辑

---

# 开放问题

1. `tech_design.md` 的 owns 归 `architect` 还是 `dev`？建议：架构师负责设计，开发可以追加实现细节，但 architect 是首要 owner。需在规范里明确"追加而非覆盖"的协作模式。
2. `onecxt adapt-agent` 是独立命令还是 `onecxt adapt` 的选项（`--include-agents`）？
3. `deploy.yaml` 是否需要支持多环境继承（staging extends base）？
