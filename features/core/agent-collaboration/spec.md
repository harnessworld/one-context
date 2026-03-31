---
id: agent-collaboration
title: "Agent Collaboration — 智能体协作增强"
status: draft
category: core
primary_repo_id: one-context
owner: architect
updated: "2026-03-31"
---

# 概述

agent-framework 建立了 6 个标准智能体和产物所有权模型，但智能体之间的协作仍依赖隐式的文件传递——没有状态可查、没有决策边界、知识加载是静态的、生成文件缺乏保护。

本 feature 在不引入重依赖的前提下，为智能体协作补充五项增强能力，使其从"配置对象"向"可协作的工作主体"演进。

---

# 目标与非目标

## 目标

1. **轻量状态流转** — 在 feature 目录下引入 `status.yaml`，记录当前阶段和历史，不做硬校验
2. **决策手册** — 为每个 Agent 在 `knowledge/playbooks/` 下创建决策矩阵，明确常见场景的行为边界
3. **Knowledge 条件加载** — `agents.yaml` 的 `knowledge` 字段支持基于 workspace tags 的条件引用
4. **生成文件保护** — adapt 产物带 checksum 标记，重复生成时检测手动修改并提示
5. **Knowledge-Keeper 触发策略** — 明确触发时机和漂移检测的最简规则

## 非目标

- 消息队列、事件总线等重量级通信机制
- 状态流转的硬性校验或自动调度（保持 local-first、人工驱动）
- Knowledge-Keeper 的 AI 驱动漂移检测（先用基于规则的版本）

---

# 用户与场景

**场景 A — 状态可见性**
开发者中途接手一个 feature，运行 `onecxt feature status agent-framework`，立即看到当前处于 `implementing` 阶段，由 dev agent 负责，上一步是 architect 在 3/29 完成 design。不需要翻阅多个文件推断进度。

**场景 B — 决策边界**
Dev Agent 发现 tech_design.md 缺少数据库 schema 定义。根据决策手册，它不会自行补充，而是将 status 回退到 `design_ready` 并在 status.yaml 中注明原因，等待 architect 补全。

**场景 C — 条件知识加载**
前端 workspace（tags: [frontend]）中的 dev agent 自动获得 `frontend-conventions.md`；后端 workspace 中的同一 dev agent 获得 `api-design.md`。无需维护两套 agent 定义。

**场景 D — 安全的 adapt 重跑**
用户手动修改了 `.cursor/rules/agent-dev.mdc` 增加了自定义规则。下次 `onecxt adapt` 时，CLI 检测到 checksum 不匹配，提示"agent-dev.mdc 已被手动修改，使用 --force 覆盖或 --merge 保留"。

**场景 E — Knowledge-Keeper 触发**
feature 部署完成后，用户运行 `onecxt agent run knowledge-keeper --feature agent-framework`。Knowledge-Keeper 扫描该 feature 下的 tech_design 和 mr_report，发现"adapter 必须实现 generate_agents 方法"这一约定未记录在 standards 中，生成更新建议。

---

# 验收标准

## 轻量状态流转

- [ ] `features/_template/status.yaml` 模板存在，包含 `feature_id`、`current_phase`、`history` 字段
- [ ] 预置 phase：`draft` → `spec_ready` → `design_ready` → `implementing` → `review_ready` → `deployed`
- [ ] 支持自定义 phase：用户可在 `status.yaml` 的 `custom_phases` 字段扩展阶段，doctor 校验 `current_phase` 在预置 + 自定义范围内
- [ ] `onecxt doctor` 校验 status.yaml 格式正确性（字段存在、phase 值合法）
- [ ] Agent instructions 中包含何时更新 status.yaml 的指引

## 决策手册

- [ ] `knowledge/playbooks/` 下存在 `pm-decisions.md`、`architect-decisions.md`、`dev-decisions.md`、`qa-decisions.md`、`sre-decisions.md`、`knowledge-keeper-decisions.md`
- [ ] 每个决策手册包含至少 5 条"场景 → 行为 → 原因"条目
- [ ] `meta/agents.yaml` 中各 agent 的 `knowledge` 字段引用对应的决策手册

## Knowledge 条件加载

- [ ] `meta/workspaces.yaml` schema 支持 `tags` 字段（字符串数组）
- [ ] `meta/agents.yaml` 的 `knowledge` 条目支持 `{path, when: {workspace_tags: [...]}}` 格式
- [ ] `agents.py` 加载时根据当前 workspace 的 tags 过滤 knowledge 列表
- [ ] 无 `when` 条件的条目始终加载（向后兼容）
- [ ] `onecxt doctor` 校验条件引用的路径存在

## 生成文件保护

- [ ] adapt 生成的所有文件包含 checksum 注释头（格式：`<!-- ONE-CONTEXT GENERATED | checksum: <sha256-prefix-8> -->`）
- [ ] `onecxt adapt` 检测到 checksum 不匹配时中断报错，输出具体文件列表和建议操作（`--force` 覆盖 / 手动合并 / `git diff` 查看差异）
- [ ] `onecxt adapt --force` 强制覆盖所有文件（忽略 checksum 校验）
- [ ] `onecxt adapt --diff` 预览将产生的变更

## Knowledge-Keeper 触发

- [ ] `onecxt agent run knowledge-keeper --feature <id>` 命令可用
- [ ] 扫描指定 feature 目录下的 `tech_design.md`、`test_report.md`、`mr_report.md`
- [ ] 输出"建议更新"列表（哪些约定应该提取到 `knowledge/standards/`）
- [ ] 不自动修改文件，仅输出建议（用户决定是否采纳）

---

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: `one-context`
- **分支 / PR**: `feature/agent-collaboration`
- **主要路径或模块**:
  - `features/_template/status.yaml` — 状态文件模板
  - `knowledge/playbooks/*-decisions.md` — 各角色决策手册
  - `meta/agents.yaml` — knowledge 条件加载语法
  - `meta/workspaces.yaml` — tags 字段扩展
  - `packages/one-context/one_context/agents.py` — 条件 knowledge 过滤逻辑
  - `packages/one-context/one_context/adapters/__init__.py` — checksum 生成与校验
  - `packages/one-context/one_context/cli.py` — `adapt --force/--diff`、`agent run`

---

# 关联

- **前置 Feature**: `agent-framework`（本 feature 基于其数据模型扩展）
- **Workspace**（`meta/workspaces.yaml` id）: —
- **规范文档**: `knowledge/standards/agent-framework.md`（需同步更新）

---

# 实现分阶段建议

## Phase 1 — 状态流转 + 决策手册（纯文档，零代码）
- [ ] 创建 `status.yaml` 模板
- [ ] 撰写 6 份决策手册
- [ ] 更新 `agents.yaml` 引用决策手册
- [ ] 更新 Agent instructions 中关于 status.yaml 的指引

## Phase 2 — Knowledge 条件加载
- [ ] `workspaces.yaml` schema 增加 `tags`
- [ ] `agents.yaml` knowledge 条件语法实现
- [ ] `agents.py` 过滤逻辑
- [ ] `doctor` 校验扩展

## Phase 3 — 生成文件保护
- [ ] Adapter 基类增加 checksum 注入
- [ ] `adapt` 命令增加 `--force`、`--diff` 选项
- [ ] checksum 校验逻辑

## Phase 4 — Knowledge-Keeper 触发
- [ ] `agent run` CLI 子命令
- [ ] 漂移扫描基础实现（关键词提取 + 对比）
- [ ] 建议输出格式化

---

# 开放问题

1. ~~status.yaml 是否需要支持自定义 phase？~~ **已决定：支持自定义，预置 6 阶段 + `custom_phases` 扩展**
2. 决策手册的格式是否需要结构化（YAML 表格），还是纯 Markdown 表格即可？
3. ~~Knowledge 条件加载的 `when` 是否需要支持 AND/OR 组合？~~ **已决定：只做 tags 包含匹配（any match），不做 AND/OR**
4. ~~checksum 校验失败时的默认行为？~~ **已决定：中断报错 + 给用户建议操作**
