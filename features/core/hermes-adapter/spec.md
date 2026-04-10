---
id: "hermes-adapter"
title: "Hermes Adapter — one-context 支持 Hermes Agent CLI"
status: draft
category: core
primary_repo_id: one-context
owner: ""
updated: "2026-04-10"
---

# 概述

one-context 目前有 cursor、claude_code、openclaw 三个 adapter，缺少对 Hermes Agent CLI 的支持。

Hermes 的项目上下文加载机制：
1. `.hermes.md` / `HERMES.md`（优先级最高，walk 到 git root）
2. `AGENTS.md`（cwd only）
3. `CLAUDE.md`（cwd only）
4. `SOUL.md`（全局，从 `~/.hermes/` 加载，用于 agent identity/人设）

**关键发现**：Hermes 有 `.hermes.md` 这个一等公民入口，优先级高于 AGENTS.md。适配器应写 `.hermes.md` 到项目根目录，Hermes 启动即自动发现，零手动配置。

# 目标与非目标

## 目标

- 新增 `hermes` adapter，`onecxt adapt --adapter hermes` 后 Hermes 直接可用
- 生成项目根 `.hermes.md`（Hermes 自动发现，无需用户手动引用）
- 将 workspace context + profile rules + knowledge 内联到 `.hermes.md`
- `output_style.tone: minimal` 增加 hermes 特定的 `AdapterOverride`（placement=top）
- 支持 agents（per-agent 内容也内联到 `.hermes.md`，或写辅助 `.hermes/agents/*.md` 并在主文件引用）
- 补充测试用例
- **润物细无声**：adapt 完 Hermes 什么都不用配就能工作

## 非目标

- 不生成 `~/.hermes/config.yaml`（含 API key / provider，用户自管）
- 不生成 `.env`
- 不写入 `~/.hermes/SOUL.md`（那是全局人设，属于用户私人配置）
- 初版不转 `~/.hermes/skills/` 格式（knowledge 内联够用，后续可迭代）

# 用户与场景

**场景 1**：用户在 one-context 伞仓维护统一知识/profile，同时用 Hermes 作为 Agent CLI。`onecxt adapt --adapter hermes` 后，在项目目录启动 `hermes`，自动加载 `.hermes.md` 中的全部上下文，行为与 profile 一致。

**场景 2**：团队统一 cursor + claude_code + hermes 三种工具的上下文，one-context 为唯一来源。

# 验收标准

- [ ] `onecxt adapt --adapter hermes` 成功执行，无报错
- [ ] 生成项目根 `.hermes.md`（Hermes 最高优先级自动发现）
- [ ] `.hermes.md` 包含：workspace summary、focus、profile rules（含 hermes 专属 override）、内联 knowledge
- [ ] agents 内容生成到 `.hermes/agents/{id}.md`，在 `.hermes.md` 中以 markdown 引用方式聚合（Hermes 不支持 @file，但 `.hermes.md` 整体被加载，所以需要内联或合并）
- [ ] `output_style.tone: minimal` 有 hermes adapter_override（placement=top）
- [ ] `onecxt doctor` 对 hermes adapter 校验通过
- [ ] 测试覆盖：`TestHermesAdapter` 全部通过
- [ ] 零手动步骤：adapt 后在此目录运行 `hermes` 即自动加载全部上下文

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: one-context（packages/one-context/）
- **分支 / PR**: 待定
- **主要路径或模块**:
  - `packages/one-context/one_context/adapters/hermes.py`（新建，~180 行）
  - `packages/one-context/one_context/adapters/_shared_rules.py`（修改，加 hermes override）
  - `packages/one-context/tests/test_adapters.py`（修改，加 TestHermesAdapter）

# 技术要点

## Hermes 上下文发现机制

```
优先级（first match wins）:
1. .hermes.md / HERMES.md  → walk to git root  ← 我们用这个
2. AGENTS.md / agents.md   → cwd only
3. CLAUDE.md / claude.md   → cwd only
4. .cursorrules            → cwd only

SOUL.md → 全局，~/.hermes/SOUL.md，独立于项目上下文，用作 agent identity
```

## Adapter 输出结构

```
项目根/
├── .hermes.md                    # 主文件：workspace context + profile rules + 内联 knowledge + agents 摘要
└── .hermes/
    └── agents/
        └── {agent_id}.md         # 详细 agent 定义（知识内联）
```

为什么不把 agents 也放 `.hermes.md` 里：文件会太大，且 Hermes 单文件有 20000 字符截断。`.hermes.md` 放全局指引 + 用户故事级摘要，详细内容放 agents/ 目录各自文件。

**问题**：Hermes 只自动加载 `.hermes.md`，不自动扫描 `.hermes/agents/` 目录。需要在 `.hermes.md` 中内联 agents 的关键内容，或全部合并到一个 `.hermes.md`。

**方案 A（推荐）**：全部合并到单个 `.hermes.md`，靠 `_truncate_content` 截断前用户需控制总量。简单粗暴但保证 100% 自动加载。

**方案 B**：`.hermes.md` 放全局信息 + agents 摘要行，详细内容放 agents/，但 Hermes 不自动加载子目录 = 需用户手动引用 = 违反润物细无声。

选方案 A。

## 与现有 adapter 的关系

| 特性 | claude_code | openclaw | hermes（新） |
|------|-------------|----------|-------------|
| 主文件 | CLAUDE.md | .openclaw/onecxt-*.json | .hermes.md |
| @file 引用 | 支持 | 不支持 | 不支持 |
| Knowledge | @file 引用 | 内联 | 内联 |
| 格式 | Markdown | JSON | Markdown |

# 关联

- **Workspace**（`meta/workspaces.yaml` id，如有）: —
- **其他需求目录**: `features/core/unified-adapter-rules/`（adapter 规则体系）

# 开放问题

1. **20000 字符截断风险**：`_truncate_content` 对单个 context source 上限 20000 字符。实际 workspace + knowledge + agents 总量需评估。如超限会被截断丢内容。缓解方案：
   - 初版先合入 `.hermes.md`，监控实际大小
   - 超限时考虑方案 B：把 knowledge 转为 Hermes skills（`~/.hermes/skills/onecxt-xxx/SKILL.md`），skills 无单文件截断，Hermes 自动发现。缺点是走出项目目录、全局生效。
   - 另一思路：给 Hermes 提 PR 支持加载 `.hermes/` 子目录下多个 md 文件

2. **与 AGENTS.md 共存**：当前项目根已有 AGENTS.md（给 OpenClaw 用）。Hermes 发现 `.hermes.md` 后走自己的优先级，不会加载 AGENTS.md，两者互不干扰。