---
id: auto-context-compression
title: "自动上下文压缩 — 定时扫描与去重、去陈旧"
status: draft
category: core
primary_repo_id: one-context
owner: —
updated: "2026-04-02"
---

# 概述

随着 `knowledge/`、`features/`、`docs/` 等目录持续增长，**重复表述**与**已过时但仍保留的条文**会抬高代理与人类的认知成本，削弱 one-context 作为「控制平面」的可信度。

本需求在伞仓层面定义 **自动上下文压缩（Auto Context Compression）**：由一类专用智能体（或等价自动化任务）**按固定节奏**扫描约定范围内的文本资产，识别重复与过时内容，并产出**可审查的**合并、归档或删除建议（必要时直接落地低风险变更）。

该能力与 `features/core/agent-framework` 中的 `knowledge-keeper` 角色互补：后者偏「从 feature 产物提炼新约定」；本需求偏「**存量**上下文的瘦身与一致性维护」。

---

# 目标与非目标

## 目标

- 定义 **扫描范围**（必选与可选路径）及优先级，至少覆盖：
  - `knowledge/`（含 `standards/`、`playbooks/`）
  - `features/`（`spec.md`、`INDEX.md`、各需求目录内文档）
  - `docs/`（架构与贡献者文档，与 `README.md` 交叉引用处）
  - `meta/` 中与人类可读说明强相关的文件（如 `workspaces.yaml` 注释、`profiles.yaml` 说明性字段），**不**把机器生成的巨型清单当作首要压缩对象
- 定义 **重复** 的判定维度：同一事实多处以轻微改写重复、复制粘贴段落、可合并的表格/列表等（允许「语义近似 + 结构重叠」与「显式 duplicate 标记」两类信号）。
- 定义 **过时** 的判定维度：与 `features/INDEX.md` 中 `archived`/`done` 状态不一致的描述、被 `spec.md` 明确 supersede 的旧节、引用已删除路径或旧仓库 id、与 `meta/repos.yaml` 不一致的链接（在允许范围内提示修复）。
- 定义 **定时** 触发方式：例如 cron、CI 定时 job、或本地 `onecxt` 子命令 + 系统计划任务；具体实现可选，但 spec 要求 **可重复、可日志化**。
- 定义 **产出物**：人类可读的报告（Markdown 或 JSON）、可选的「建议补丁」或 PR 草稿；**高风险删除**必须经过显式确认策略（见验收标准）。
- 与 **`onecxt doctor`** 的边界：压缩逻辑可复用校验器获取仓库 id、路径合法性；**不**要求把全部压缩规则塞进 doctor，除非团队后续选择合并。

## 非目标

- 全自动无监督删除生产分支上的大量内容（避免误删）
- 替代 Git 历史或版本控制；压缩针对**当前工作树**与约定目录
- 对注册子仓（`repos/` 内各仓库）源码做全量语义分析（可作为未来扩展，本阶段以伞仓根目录与 `meta` 指向的文档为主）
- 实时增量压缩（秒级）；本需求以**批处理、定时**为主

---

# 用户与场景

**场景 A — 维护者每周回顾**

定时任务周五生成《上下文压缩报告》，列出 TOP 重复簇与过时条目；维护者在周末合并文档、更新 `INDEX.md` 状态。

**场景 B — 大 feature 合并后**

Release 后触发一次「定向扫描」：仅 `features/<category>/<feature-id>/` 与相关 `knowledge/` 条目，收敛重复的设计说明。

**场景 C — 新成员入职**

压缩结果减少「同一句话三份文档」带来的困惑，提高 `knowledge/` 检索效率。

---

# 验收标准

- [ ] 本仓库内存在实现该能力的**落点说明**（CLI 子命令、独立脚本或 `meta/agents.yaml` 下专用智能体 + playbook，三选一或组合），并在「实现落点」中写清路径
- [ ] **扫描范围** 以列表形式写在 `knowledge/standards/` 下一份规范中（或本 `spec.md` 的附录），并与默认配置一致
- [ ] **重复** 与 **过时** 的判定规则有文档化条目；至少包含「人工复核门槛」：何种建议可自动 PR、何种仅输出警告
- [ ] 定时运行可通过文档中的命令在本地或 CI **复现**（含示例 cron 或 workflow 片段）
- [ ] 与 `features/core/agent-framework` 的关联在「关联」节可查（若依赖 `knowledge-keeper` 则写明；若不依赖则写明独立运行理由）
- [ ] `onecxt doctor` 在相关 manifest 被修改后仍能通过，或本需求明确新增 doctor 规则并同步文档

---

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: `one-context`（伞仓本体；实现位于本仓库 `packages/one-context` 与根目录元数据）
- **分支 / PR**: —
- **主要路径或模块**（初稿，实施时可调整）:
  - `packages/one-context/one_context/` — 可选新增 `compress` 或 `context_gc` 子模块与 CLI 入口
  - `meta/agents.yaml` — 若采用智能体驱动，登记「context-compressor」或扩展现有 `knowledge-keeper` 职责
  - `knowledge/playbooks/` — 操作手册：如何运行、如何复核报告、如何回滚误合并
  - `knowledge/standards/` — `auto-context-compression.md`（或合并入现有 conventions）— 扫描范围与判定规则

---

# 关联

- **Workspace**（`meta/workspaces.yaml` id）: —
- **相关需求目录**:
  - `features/core/agent-framework/` — 智能体注册与适配器；若压缩由智能体执行，需对齐角色与产物所有权
- **其他**:
  - `features/README.md`、`meta/repos.yaml` — 链接代码与文档时遵守仓库 `id` 约定

---

# 附录：建议默认扫描路径（实施时以规范文档为准）

| 路径 | 优先级 | 说明 |
|------|--------|------|
| `knowledge/` | P0 | 标准与 playbook，重复影响面大 |
| `features/` | P0 | 需求规格与索引，易与 `INDEX.md` 漂移 |
| `docs/` | P1 | 架构文与模板 |
| `README.md`、根目录 `AGENTS.md` | P1 | 与 `docs/` 易重复 |
| `meta/*.yaml` | P2 | 仅注释与描述性字段；谨慎改写 |

---

# 开放问题

1. 压缩报告默认输出到 `features/core/auto-context-compression/reports/` 还是 `.gitignore` 的临时目录？需平衡可审计与仓库噪音。
2. 是否引入轻量「内容指纹」（hash + 段落级）即可满足 MVP，还是第一版就需要嵌入模型做语义去重？
3. 与国际化无关；若未来 `knowledge/` 多语言，重复判定是否按语言分簇？
