---
id: unified-adapter-rules
title: "统一适配器规则源 — 声明式 manifest，消除 PROFILE_RULES 重复"
status: draft
category: core
primary_repo_id: one-context
owner: ""
updated: "2026-04-10"
---

# 产品设想（用户原话整理）

1. **唯一真相（single truth）**：Claude Code、Cursor、OpenClaw 侧都能明确：**规则应写到唯一权威来源**，而不是在各自界面里长期分叉维护。
2. **正向生成**：从唯一真相 **生成** 各平台可用的规则文件（格式、路径因工具而异）。
3. **反向同步**：若用户 **直接在某一平台上** 改了规则，该平台应能 **感知变更**，并把内容 **补回 / 合并进唯一真相**（具体是全自动、半自动还是提示人工合并，待设计）。
4. **已有文件与冲突**：执行「生成到各平台」时，若目标路径 **已存在** 规则或用户本地改过，需要明确的 **冲突处理策略**（覆盖、三路合并、仅写入带标记区块、dry-run 报告等）。
5. **OpenClaw 多配置文件**：OpenClaw 侧配置文件较多、结构复杂，**生成时如何映射、拆文件、命名**，尚未想清；本需求先 **记录问题**，在技术设计中分阶段收敛。

以上第 2 点与当前 `onecxt adapt` 方向一致；第 3、4、5 点为 **增量能力**，复杂度高，允许分阶段交付。

---

# 概述

today：`meta/profiles.yaml` 存放 **结构化 profile**（`behavior`、`output_style` 等），但「字段值 → 各工具可见的自然语言规则」写在 `packages/one-context/one_context/adapters/` 下 **`PROFILE_RULES` 的 Python 列表**里，且在 **`claude_code.py` / `cursor.py` / `openclaw.py` 各维护一份相同逻辑**，与架构文档「Write shared meaning once. Adapt it many times.」存在落差。

本需求：引入 **单一权威、人类可编辑的规则 manifest**（或等价声明式来源），由 `onecxt adapt`（及测试）加载，再生成 Cursor / Claude Code / OpenClaw 产物；适配器只负责 **渲染与路径**，不再作为规则文案的分散来源。远期叠加 **反向同步、冲突策略、OpenClaw 多文件布局**（见上节）。

---

# 目标与非目标

## 目标

- **单一真相**：profile 字段与 `FieldRule` 语义（含 `adapter_overrides`、placement）有一份 **可版本化、可 diff** 的来源（优先仓库内 YAML/JSON，与 `meta/` 并列或置于其下）。
- **DRY**：三适配器 **共享同一套规则定义**，删除或收敛重复的 `PROFILE_RULES` 常量。
- **可校验**：`onecxt doctor` 或专用子命令能校验 manifest 与 `profiles.yaml` 字段路径一致、无遗漏、无冲突。
- **行为不变（迁移期）**：默认生成物与当前适配器输出 **字节级或语义级等价**（测试覆盖），再允许迭代文案。
- **文档**：`docs/architecture.md` 或 `packages/one-context/README.md` 中明确「规则 manifest」与 `profiles.yaml`、`knowledge/` 的分工。
- **（阶段可拆分）正向生成 + 冲突策略**：导出到各平台时，对 **已存在目标文件** 的行为有文档化、可测试的规则。
- **（阶段可拆分）反向同步**：平台侧编辑能回流唯一真相；实现形态（CLI、`watch`、钩子、CI）待定。

## 非目标

- 重写整个 profile 继承 / mixin 语义（沿用现有 `meta/profiles.yaml` 合并逻辑即可）。
- 一次性把 `knowledge/` 全文并入 manifest（长文仍走 knowledge 层；manifest 只管 **profile 字段 → 短规则句** 的映射）。
- 规定 OpenClaw/Cursor 上游产品格式变化（仍通过现有适配器输出）。
- **第一版未必**解决「所有编辑器内实时监听」——可与工具能力对齐后分阶段做。

---

# 用户与场景

- **维护者**：改一条「minimal 输出」说明时只编辑 **一处**，不必同步改三个 `.py`。
- **贡献者**：Code Review 能清楚看到规则 diff，而不是在三份 Python 里找茬。
- **多工具用户**：继续 `onecxt adapt`，但心里确信规则来自同一 manifest。

---

# 验收标准

- [ ] 仓库内存在 **权威规则 manifest**（路径与格式在 `tech_design.md` 定稿），并由单一模块加载。
- [ ] `claude_code` / `cursor` / `openclaw` 适配器 **不再各自持有完整重复**的 `PROFILE_RULES` 列表（允许薄包装或 re-export）。
- [ ] 现有 `packages/one-context/tests/test_adapters.py`（及相关测试）通过；必要时增加 manifest 解析与 golden 测试。
- [ ] `onecxt doctor`（或等价校验）对 manifest 做基本完整性检查。
- [ ] `features/INDEX.md` 与本 `status` 同步更新。

---

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: **one-context**（实现位于本伞仓根目录，与既有 `agent-framework` 等一致；`packages/one-context` 为可安装包）。
- **分支 / PR**: （待填）
- **主要路径或模块**: `packages/one-context/one_context/adapters/`、`meta/`（若 manifest 放于此）、新增如 `meta/adapter-rules.yaml` 或 `knowledge/rules/…`（具体见技术设计）。

---

# 关联

- **Workspace**（`meta/workspaces.yaml` id，如有）: 无硬性绑定；全局行为。
- **其他需求目录**: 与 `features/core/profile-inheritance/`（若落地 mixin 与字段路径）可对齐；与 `features/core/agent-framework/`（适配器生成链路）衔接。

---

# 开放问题（供探讨）

## 模型与 manifest

1. **格式**：纯 YAML（字段路径为 key）vs 保留 Python 仅作 loader vs 混合（manifest + 少量代码钩子）。
2. **与 `profiles.yaml` 的关系**：manifest 是否只描述「规则模板」，profile 只提供 **触发值**；还是部分长句直接写在 profile（不推荐重复）。
3. **adapter 特化**：`AdapterOverride`（如 Claude 的 `placement: top`）是否全部进 manifest，避免代码分支。
4. **版本与迁移**：是否对 manifest 做 `version:` 字段，便于未来改 schema。
5. **生成物**：是否顺带统一 `onecxt-hard-rules` 等文件的生成策略（仍从 manifest 驱动）。

## 正向生成：已有规则与冲突

6. **检测方式**：以文件 mtime/hash、嵌入的「one-context 生成」标记、还是与上次 adapt 快照对比？
7. **策略枚举**：`--force` 覆盖；跳过未变更；只更新 fenced 区块（类似 codegen）；生成 `.bak`；打印 diff 后退出。
8. **人工编辑混合**：用户在某平台文件里加了「手写段落」，下次 adapt 是否保留、放在哪一段（需块级约定）。
9. **多 workspace / 多 agent**：同一仓库多份 `onecxt-*.mdc` 时，冲突粒度是按文件还是按规则块。

## 反向同步：平台改 → 唯一真相

10. **触发**：定时 `onecxt pull-rules`、Git pre-commit、文件监视、或各工具自带的 hook（若存在）。
11. **合并语义**：把 Cursor 改动的句子合并回 YAML 时，字段如何对应（自然语言 diff → 结构化字段是否可逆）。
12. **权威优先级**：唯一真相 vs 平台编辑冲突时，默认谁赢；是否需要交互式解决（类似 `git merge`）。

## OpenClaw 多配置文件

13. **映射表**：哪些 OpenClaw 路径由 manifest 生成（例如 `.openclaw/agents/*.json`、项目级 `onecxt-project.json`、是否包含用户目录下的 skills 等）——**范围未决**。
14. **拆分原则**：一个逻辑规则对应一个 JSON 文件 vs 聚合为少数文件；与 OpenClaw 加载顺序、合并语义的关系。
15. **与 skills / 插件**：仓库内 `skills/` 与 OpenClaw 全局 skills 目录是否纳入同一套「唯一真相」或单独约定。

---

# 备注

反向同步与冲突处理依赖 **各工具是否暴露稳定钩子、文件格式是否适合块级合并**；技术设计阶段应对 Claude Code / Cursor / OpenClaw 分别做 **能力矩阵**，再定 MVP 范围。
