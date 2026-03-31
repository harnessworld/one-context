---
id: profile-inheritance
title: "Profile Inheritance — Profile 继承与 Mixin 机制"
status: draft
category: core
primary_repo_id: one-context
owner: architect
updated: "2026-03-31"
---

# 概述

当前 `meta/profiles.yaml` 仅有 2 个 Profile（`default-coding`、`repo-architecture`），所有开发类 Agent 共享同一行为配置。随着使用场景扩展（前端/后端/数据/移动端等），需要 10+ 种 Profile 变体来表达行为差异。

逐一定义完整 Profile 会导致大量重复配置和维护负担。本 feature 引入 Profile 继承和 Mixin 组合机制，用最小的声明量表达差异。

---

# 目标与非目标

## 目标

1. **单层继承** — Profile 可通过 `extends` 引用一个父 Profile，仅声明差异字段
2. **Mixin 组合** — Profile 可通过 `mixins` 引用多个 Mixin 片段，叠加特定维度的行为覆盖
3. **解析确定性** — 定义明确的字段合并优先级：`自身字段 > mixin（按声明顺序后覆盖前）> extends 父级`
4. **校验与可追溯** — `onecxt doctor` 校验继承链合法性；`onecxt profile show` 输出解析后的完整 Profile

## 非目标

- 多层继承（A extends B extends C）——先限制为单层，避免复杂度爆炸
- Profile 的运行时动态切换（仍为 adapt 时静态解析）
- Mixin 冲突的自动解决（仍按声明顺序"后覆盖前"，但 doctor 会警告）

---

# 用户与场景

**场景 A — 前端/后端差异化**
```yaml
profiles:
  default-coding:
    behavior:
      plan_first: false
      safety_level: standard
      test_expectation: targeted

  frontend-coding:
    extends: default-coding
    behavior:
      test_expectation: visual+snapshot
      change_scope: component-scoped

  backend-coding:
    extends: default-coding
    behavior:
      test_expectation: integration
      safety_level: conservative
```
前端 dev agent 引用 `frontend-coding`，后端 dev agent 引用 `backend-coding`，无需重复声明 `plan_first: false`。

**场景 B — Mixin 叠加**
```yaml
mixins:
  strict-review:
    behavior:
      safety_level: conservative
      output_style:
        tone: structured

  fast-iteration:
    behavior:
      plan_first: false
      change_scope: focused

profiles:
  prototype-frontend:
    extends: frontend-coding
    mixins: [fast-iteration]
    # 结果：plan_first=false, test=visual+snapshot, scope=focused, safety=standard

  production-backend:
    extends: backend-coding
    mixins: [strict-review]
    # 结果：plan_first=false, test=integration, safety=conservative, tone=structured
```

**场景 C — 查看解析结果**
```bash
$ onecxt profile show production-backend --resolved
# 输出完整合并后的 Profile，标注每个字段的来源
behavior:
  plan_first: false              # ← default-coding
  safety_level: conservative     # ← strict-review (mixin)
  test_expectation: integration  # ← backend-coding
  change_scope: focused          # ← default-coding
  output_style:
    tone: structured             # ← strict-review (mixin)
```

---

# 验收标准

## 继承

- [ ] `profiles.yaml` 支持 `extends: <profile-id>` 字段
- [ ] 子 Profile 仅需声明差异字段，其余从父级继承
- [ ] `extends` 指向不存在的 Profile 时 `onecxt doctor` 报错
- [ ] 当前限制为单层继承：如果父 Profile 也有 `extends`，doctor 报错
- [ ] 数据结构预留多层继承扩展点：`profiles.py` 的解析逻辑使用递归 + 深度计数器（当前 max_depth=1），未来放开只需调整阈值并增加拓扑排序/循环检测

## Mixin

- [ ] `profiles.yaml` 顶层支持 `mixins` 区块，与 `profiles` 并列
- [ ] Profile 可通过 `mixins: [id1, id2]` 引用多个 Mixin
- [ ] Mixin 引用不存在的 id 时 doctor 报错
- [ ] Mixin 不能有 `extends` 或 `mixins` 字段（扁平结构）
- [ ] `onecxt doctor` 检测到两个 mixin 设置同一字段为不同值时输出警告（非阻断，但提示用户注意声明顺序）

## 合并优先级

- [ ] 字段合并顺序：`extends 父级` → `mixins（按声明顺序依次覆盖）` → `自身字段`
- [ ] 深层对象做 deep merge（如 `output_style.tone` 不覆盖同级的 `output_style.format`）
- [ ] 数组字段做替换而非合并（避免歧义）

## CLI

- [ ] `onecxt profile list` 输出所有 Profile 和 Mixin，标注类型
- [ ] `onecxt profile show <id>` 输出原始定义
- [ ] `onecxt profile show <id> --resolved` 输出完整合并结果，每个字段标注来源

## Adapter 兼容

- [ ] `_rules.py` 的 FieldRule 匹配逻辑不变——它接收的是解析后的完整 Profile
- [ ] 现有 2 个 Profile 无 `extends`/`mixins` 时行为完全不变（向后兼容）

---

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: `one-context`
- **分支 / PR**: `feature/profile-inheritance`
- **主要路径或模块**:
  - `meta/profiles.yaml` — schema 扩展（extends、mixins）
  - `packages/one-context/one_context/profiles.py` — 继承解析、mixin 合并、循环检测
  - `packages/one-context/one_context/validate.py` — doctor 校验扩展
  - `packages/one-context/one_context/cli.py` — `profile show --resolved`
  - `packages/one-context/one_context/adapters/_rules.py` — 确认兼容（可能无改动）

---

# 关联

- **前置 Feature**: `agent-framework`（Agent 引用 Profile）
- **相关 Feature**: `agent-collaboration`（条件 knowledge 加载可能与 Profile tags 联动）
- **Workspace**（`meta/workspaces.yaml` id）: —

---

# 实现分阶段建议

## Phase 1 — 单层继承
- [ ] `profiles.yaml` schema 扩展 `extends` 字段
- [ ] `profiles.py` 实现继承解析（dict deep merge）
- [ ] `validate.py` 增加继承链校验（存在性、单层限制）
- [ ] 单元测试覆盖

## Phase 2 — Mixin 机制
- [ ] `profiles.yaml` schema 扩展 `mixins` 顶层区块和 Profile 的 `mixins` 引用
- [ ] `profiles.py` 实现 mixin 合并逻辑（按声明顺序）
- [ ] 合并优先级测试（extends → mixins → self）
- [ ] `validate.py` 增加 mixin 校验

## Phase 3 — CLI 增强
- [ ] `profile show --resolved` 带来源标注
- [ ] `profile list` 展示 Profile 和 Mixin

## Phase 4 — 预置 Profile 库
- [ ] 基于 `default-coding` 扩展：`frontend-coding`、`backend-coding`、`data-coding`、`mobile-coding`
- [ ] 基于 `repo-architecture` 扩展：`strict-architecture`
- [ ] 预置 Mixin：`strict-review`、`fast-iteration`、`doc-heavy`
- [ ] 更新 `agents.yaml` 中各 Agent 引用更精确的 Profile

---

# 开放问题

1. 是否需要支持"Profile 模板变量"？例如 `test_command: "{package_manager} test"` 由 workspace 注入。还是这属于 adapter 层的职责？
2. ~~Mixin 冲突是否需要 doctor 警告？~~ **已决定：需要。doctor 检测同字段冲突并输出警告，实际合并仍按声明顺序**
3. ~~是否放开多层继承？~~ **已决定：当前单层，但预留扩展点（递归 + depth 参数），未来可平滑升级**
