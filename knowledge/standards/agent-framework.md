# Agent Framework — 智能体框架规范

本文档是 one-context 智能体系统的**权威规范**。所有智能体定义、适配器生成逻辑、工作流约定均以此为准。

---

## 1. 核心概念

**智能体（Agent）** 是 one-context 的一等公民配置对象，与 `repos`、`workspaces`、`profiles` 并列，在 `meta/agents.yaml` 中注册。

一个智能体不是"带角色提示词的 profile"——它有：

- **身份（identity）**：固定的 `id`、`role`、`name`
- **知识引用（knowledge）**：关联哪些 `knowledge/` 文件注入上下文
- **产物所有权（owns）**：负责创建并维护哪些文件（glob 模式）
- **行为规格（profile）**：引用 `meta/profiles.yaml` 中的 profile id
- **工具专属指令（instructions）**：注入给 AI 工具的角色说明（tool-neutral）

适配器（Cursor / Claude Code / OpenClaw）负责将上述字段翻译成各工具原生格式，不在智能体定义里保存工具专属内容。

---

## 2. `meta/agents.yaml` 模式参考

```yaml
version: "1"

agents:
  - id: <string>               # 稳定的全局唯一 id（kebab-case）
    name: <string>             # 人类可读名称
    role: <enum>               # pm | architect | dev | qa | sre | knowledge-keeper
    profile: <profile_id>      # 引用 meta/profiles.yaml 中的 id
    description: <string>      # 简短描述，供 onecxt agent list 展示

    knowledge:                 # 加载到上下文的知识文件/目录（相对 one-context 根）
      - knowledge/path/to/file.md
      - knowledge/path/to/dir/

    owns:                      # 此智能体负责创建/维护的产物（glob，相对根）
      - "features/**/spec.md"

    instructions: |            # Tool-neutral 角色说明（注入给 AI 工具）
      ...

    # --- role=dev 专属 ---
    worktree:
      branch_pattern: "feature/{feature_id}"        # {feature_id} 占位符
      path_pattern: "repos/{repo_id}/.worktrees/{feature_id}"
      base_branch: main                             # 可在 repo 级覆盖

    # --- role=sre 专属 ---
    deploy_manifest: "deploy.yaml"  # 在每个 repo 根目录查找的文件名
```

### role 枚举说明

| role | 职责摘要 |
|------|----------|
| `pm` | 按模板创建 feature spec，管理 `features/INDEX.md` |
| `architect` | 跨仓技术决策，维护 `docs/architecture.md` 和 `tech_design.md` |
| `dev` | 设计并实现功能，以 git worktree 方式在 feature 分支工作 |
| `qa` | Review 实现，生成测试，产出 `test_report.md` / `mr_report.md` |
| `sre` | 读取各 repo 的 `deploy.yaml` 执行发布，产出 `deliver.md` |
| `reviewer` | 多智能体协作评审技术方案，产出 `review_record.md` / `issue_checklist.md` |
| `knowledge-keeper` | 维护知识层，检测知识漂移，提炼新约定 |

---

## 3. 产物所有权模型（Artifact Ownership）

每个 feature 目录下的文件**由唯一智能体负责**，形成"每步有人认领、每步有文件落盘"的可追溯流程：

```
features/<category>/<feature-id>/
  spec.md          ← pm 创建并维护
  tech_design.md   ← architect（或 dev）创建并维护
  worktrees.yaml   ← dev 创建（onecxt worktree setup 生成）
  test_report.md   ← qa 创建并维护
  mr_report.md     ← qa 创建并维护
  deliver.md       ← sre 创建并维护
```

**规则：**
- `owns` 字段中的 glob 模式决定所有权；同一文件不应被两个智能体 own（`tech_design.md` 由 architect 或 dev 选一）。
- 智能体不应修改不在自己 `owns` 范围内的文件，除非明确被要求。
- 流转由人工触发（@ 对应智能体），不要求自动状态机。

---

## 4. git Worktree 约定

Dev 智能体以 **git worktree** 方式工作，每个 feature × repo 对应一个独立工作目录：

### 目录结构

```
repos/
  <repo_id>/
    .worktrees/
      <feature_id>/   ← git worktree，分支名 feature/<feature_id>
```

### `worktrees.yaml`

Dev 智能体在开始工作前，在 feature 目录下创建 `worktrees.yaml` 记录所有 worktree 状态：

```yaml
feature_id: my-feature
branch: feature/my-feature
created_at: "2026-03-31"

worktrees:
  - repo_id: repo-a
    path: repos/repo-a/.worktrees/my-feature
    branch: feature/my-feature
    base: main
    status: active        # active | merged | abandoned

  - repo_id: repo-b
    path: repos/repo-b/.worktrees/my-feature
    branch: feature/my-feature
    base: develop
    status: active
```

### CLI 命令（计划）

```bash
onecxt worktree setup <feature-id> [--repos repo1,repo2]   # 创建 worktree
onecxt worktree status <feature-id>                        # 查看状态
onecxt worktree teardown <feature-id>                      # 合并后清理
```

`worktrees.yaml` 由 `onecxt worktree setup` 自动生成；智能体可在其上追加 `status` 变更。

---

## 5. deploy.yaml 约定（SRE）

每个需要 SRE 智能体参与发布的 repo 根目录下放置 `deploy.yaml`，声明该 repo 的发布方式。

```yaml
version: "1"
name: "my-service"
strategy: docker-compose   # docker-compose | helm | raw-script | manual | none

stages:
  - id: staging
    cmd: "docker-compose -f docker-compose.staging.yml up -d"
    health_check: "curl -f http://localhost:8080/health"
    approval_required: false

  - id: production
    cmd: "docker-compose -f docker-compose.prod.yml up -d"
    health_check: "curl -f http://localhost:8080/health"
    approval_required: true

rollback:
  cmd: "docker-compose -f docker-compose.prod.yml down && ..."

notes: |
  任何发布前的额外提醒，SRE 智能体在执行前必须读取。
```

SRE 智能体在工作前：
1. 读取 feature 的 `deliver.md`（内含发布范围与版本）
2. 对每个涉及的 repo 查找 `deploy.yaml`
3. 按 `stages` 顺序执行，遇到 `approval_required: true` 时暂停并等待人工确认
4. 完成后更新 `deliver.md` 中的发布状态

---

## 6. 适配器生成（Adapter Output）

`onecxt adapt <workspace>` 在现有逻辑基础上，**额外**为每个智能体生成一份 agent 配置文件，并在项目根写入工具入口文件：

| 工具 | 生成路径 |
|------|----------|
| Cursor | `.cursor/rules/agent-{id}.mdc` |
| Claude Code | `.claude/agents/{id}.md` |
| OpenClaw | `.openclaw/agents/{id}.json` |

| 工具 | 项目根 / 聚合文件 |
|------|-------------------|
| Claude Code | `CLAUDE.md` — `@` 引用本次 adapt 的全部 `onecxt-<workspace>.md` 与全部 `agents/{id}.md` |
| OpenClaw | `.openclaw/onecxt-project.json` — 列出上述 workspace JSON 与 agent JSON 的相对路径 |

每份 agent 生成文件包含：
1. 智能体身份与角色说明（来自 `instructions`）
2. 关联 profile 转译后的行为规格
3. 内联/引用的 knowledge 内容
4. `owns` 产物清单（告知 AI 工具自己负责哪些文件）
5. role 专属配置（worktree 路径模式 / deploy_manifest 位置）

（计划中的 CLI：`onecxt adapt-agent`、`onecxt agent list/show` — 当前由 `onecxt adapt` 一次性生成全部 agent 与项目根文件。）

---

## 7. 标准智能体一览

| id | role | owns | 关键知识引用 |
|----|------|------|-------------|
| `pm` | pm | `features/**/spec.md`, `features/INDEX.md` | `playbooks/add-umbrella-feature.md` |
| `architect` | architect | `features/**/tech_design.md`, `docs/architecture.md` | `docs/architecture.md`, `knowledge/standards/` |
| `dev` | dev | `features/**/worktrees.yaml` | `knowledge/standards/` |
| `qa` | qa | `features/**/test_report.md`, `features/**/mr_report.md` | `knowledge/standards/` |
| `sre` | sre | `features/**/deliver.md` | `knowledge/playbooks/` |
| `knowledge-keeper` | knowledge-keeper | `knowledge/standards/`, `knowledge/playbooks/` | 全部 knowledge |

---

## 8. 跨工具兼容原则

智能体定义本身 **tool-neutral**，不包含任何工具专属语法。具体要求：

- `instructions` 用自然语言写，不含 `@file`、`.mdc` 语法或 JSON 结构——由适配器负责翻译。
- `knowledge` 引用用相对路径，适配器决定是 inline 还是 `@file` 引用。
- 任何工具特定的覆盖（如 Cursor glob filter）通过适配器规则层表达，不写入 `agents.yaml`。

---

## 相关文档

- `meta/agents.yaml` — 智能体注册表（实例）
- `meta/profiles.yaml` — profile 定义
- `features/README.md` — feature 目录约定
- `knowledge/playbooks/add-umbrella-feature.md` — PM 智能体操作手册
- `docs/architecture.md` — 系统架构
