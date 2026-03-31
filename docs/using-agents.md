# 智能体使用指南

本文档说明如何在 Cursor、Claude Code 和 OpenClaw 中使用 one-context 智能体系统，以及完整的 feature 开发流程。

> **框架规范**：`knowledge/standards/agent-framework.md`  
> **智能体注册表**：`meta/agents.yaml`

---

## 核心理念：配置一次，工具同步

```
meta/agents.yaml
      │
      ▼
onecxt adapt <workspace>
      │
      ├──→ .cursor/rules/agent-pm.mdc          (Cursor 自动加载)
      ├──→ .claude/agents/pm.md                (Claude Code 引用)
      └──→ .openclaw/agents/pm.json            (OpenClaw 加载)
```

你**不需要**在不同工具里重复配置智能体。`meta/agents.yaml` 是唯一的维护点，适配器负责翻译格式。

---

## 快速上手

### 第一步：维护 `meta/agents.yaml`

每个智能体的 `knowledge` 列表里已经写好了模板、playbook 等路径。这是**唯一**需要维护的智能体定义；不必再把同一批路径抄进 `workspaces.yaml`（除非你希望 workspace 规则里也带上这些内容）。

### 第二步：生成工具配置

```bash
onecxt adapt my-project
# 或：onecxt adapt --all
```

`onecxt adapt` 会做两件事：

1. **Workspace 级**：与以前一样，生成 `onecxt-<workspace>.mdc` / `onecxt-<workspace>.md` / `onecxt-<workspace>.json`。
2. **智能体级**：为 `meta/agents.yaml` 里每个智能体再生成一份文件（模板与 playbook 已按工具能力 **内联或 @ 引用**）：

| 工具 | Workspace 文件 | 每个智能体 |
|------|----------------|------------|
| Cursor | `.cursor/rules/onecxt-<id>.mdc`（`alwaysApply: true`） | `.cursor/rules/agent-<id>.mdc`（`alwaysApply: false`，globs 来自 `owns`） |
| Claude Code | `.claude/adapters/onecxt-<id>.md` | `.claude/agents/<id>.md`（内含 `@path` 知识引用） |
| OpenClaw | `.openclaw/onecxt-<id>.json` | `.openclaw/agents/<id>.json` |

### 第三步：一句话调用（各工具差异）

**Cursor**：在 `features/` 下打开或新建与 PM 职责相关的文件（例如任意 `**/spec.md`）时，`agent-pm.mdc` 会因 glob 自动参与上下文。此时只说任务即可，例如：

```
帮我创建 feature：用户登录
```

若当前对话没有命中 glob，仍可显式说一句「按 PM 智能体」或打开 `features/INDEX.md` / 某个 `spec.md` 再发任务。

**Claude Code**：在仓库根目录的 `CLAUDE.md` 里**各加一行**（一次性设置），例如：

```markdown
@.claude/agents/pm.md
```

之后同一句自然语言即可；`pm.md` 内的 `@` 会在运行时拉齐模板与 playbook。

**OpenClaw**：按该工具加载 `.openclaw/agents/*.json` 的方式挂接后，同样只需一句自然语言（具体入口以 OpenClaw 文档为准）。

其他角色（dev / qa / sre 等）同理：Cursor 靠对应 `owns` 的 glob 自动带上下文；Claude Code 可在 `CLAUDE.md` 里按需增加 `@.claude/agents/dev.md` 等。

---

## 各工具使用方式

### Cursor

运行 `onecxt adapt` 后，`.cursor/rules/agent-<id>.mdc` 已写入；其中 `globs` 来自 `meta/agents.yaml` 里该智能体的 `owns`。例如 PM 的 `owns` 含 `features/**/spec.md` 与 `features/INDEX.md` 时，编辑这些路径下的文件会自动带上 PM 的说明与内联知识。

**推荐**：在 `features/` 下打开或新建目标文件后再发任务，通常只需一句话描述需求。若当前编辑器未命中任何 agent 的 glob，可临时打开 `features/INDEX.md` 或补一句「按 PM 智能体规范执行」。

---

### Claude Code

Workspace 级：`@.claude/adapters/onecxt-<workspace>.md`（可选，与以前相同）。

智能体级（**推荐，实现「一句话」**）：在 `CLAUDE.md` 里为常用角色各加一行，例如：

```markdown
@.claude/agents/pm.md
@.claude/agents/dev.md
```

每个 `agents/<id>.md` 已包含该角色的说明，并用 `@path` 列出知识文件；Claude Code 会在需要时读取。设置一次后，对话里直接说任务即可，无需每次手动 `@` 四个文件。

**调用示例：**

```
feature: user-auth，涉及仓库 repo-a、repo-b，请创建 worktree 并更新 worktrees.yaml
```

---

### OpenClaw

OpenClaw 通过 `.openclaw/onecxt-my-project.json` 加载，与上述流程一致。调用方式同 Claude Code，直接在对话中说明角色。

---

## 完整 Feature 开发流程示例

以开发「用户登录」功能为例，展示六个智能体的协作顺序。

---

### Step 1 — PM 智能体：创建 Feature Spec

**你说：**
```
你是 pm 智能体。
请在 features/core/ 下创建名为 user-login 的 feature，
需求：支持邮箱+密码登录，JWT token，7天有效期。
使用 features/_template/spec.md 模板。
```

**智能体产出：** `features/core/user-login/spec.md`，并自动更新 `features/INDEX.md`。

---

### Step 2 — Architect 智能体：技术方案

**你说：**
```
你是 architect 智能体。
读取 features/core/user-login/spec.md，
为以下仓库产出 tech_design.md：
- api-server（负责认证接口）
- frontend（负责登录页面）
```

**智能体产出：** `features/core/user-login/tech_design.md`，内含接口定义、数据流、依赖分析。

---

### Step 3 — Dev 智能体：创建 Worktree 并实现

**你说：**
```
你是 dev 智能体。
feature: user-login，涉及仓库：api-server、frontend。
1. 为每个仓库创建 worktree（路径和分支按约定）
2. 记录 worktrees.yaml
3. 根据 tech_design.md 开始实现 api-server 的认证接口
```

**智能体产出：**
- `features/core/user-login/worktrees.yaml`（worktree 状态记录）
- 代码在 `repos/api-server/.worktrees/user-login/` 分支 `feature/user-login`

`worktrees.yaml` 示例：
```yaml
feature_id: user-login
branch: feature/user-login
created_at: "2026-03-31"

worktrees:
  - repo_id: api-server
    path: repos/api-server/.worktrees/user-login
    branch: feature/user-login
    base: main
    status: active
  - repo_id: frontend
    path: repos/frontend/.worktrees/user-login
    branch: feature/user-login
    base: main
    status: active
```

---

### Step 4 — QA 智能体：Review 与测试报告

**你说：**
```
你是 qa 智能体。
对照 features/core/user-login/spec.md 的验收标准，
review repos/api-server/.worktrees/user-login/ 中的实现，
产出 test_report.md 和 mr_report.md。
```

**智能体产出：**
- `features/core/user-login/test_report.md`（测试范围、用例、结果）
- `features/core/user-login/mr_report.md`（review 讨论、决议、待办）

---

### Step 5 — SRE 智能体：发布

**你说：**
```
你是 sre 智能体。
feature: user-login 已通过 QA，准备发布到 staging。
请读取 api-server 和 frontend 各自的 deploy.yaml，按 staging stage 执行。
```

**智能体执行流程：**
1. 读取 `features/core/user-login/deliver.md`（或提示你先创建）
2. 读取 `repos/api-server/deploy.yaml` → 找到 `stages[staging]` → 执行命令
3. 执行 `health_check`
4. 如果 `approval_required: true`（production stage），**停下来等你确认**
5. 更新 `deliver.md` 记录发布状态

---

### Step 6 — Knowledge 智能体：沉淀约定（可选）

发布完成后，定期运行：

**你说：**
```
你是 knowledge-keeper 智能体。
扫描近期 features/core/user-login/ 下的 tech_design 和 mr_report，
提炼新的工程约定，提议更新 knowledge/standards/ 中相关内容。
```

---

## Feature 目录最终状态

```
features/core/user-login/
  spec.md          ✅ pm 产出
  tech_design.md   ✅ architect 产出
  worktrees.yaml   ✅ dev 产出（自动）
  test_report.md   ✅ qa 产出
  mr_report.md     ✅ qa 产出
  deliver.md       ✅ sre 产出
```

每一步都有文件落盘。即使中途切换工具（从 Cursor 切到 Claude Code），下一个智能体只需读取已有文件，工作流不断链。

---

## 常见问题

**Q：每次对话都要说「你是 xxx 智能体」吗？**

不一定。**Cursor**：命中 `agent-*.mdc` 的 glob 时，规则已注入，直接说任务即可。**Claude Code**：在 `CLAUDE.md` 里 `@` 过对应 `agents/<id>.md` 后，同样不必每轮自报角色。若未配置或未命中 glob，补一句角色仍有帮助。

**Q：Windows 上 `onecxt adapt ... --dry-run` 控制台乱码或报错？**

控制台编码可能是 GBK。可设置环境变量 `PYTHONIOENCODING=utf-8` 再运行；或直接去掉 `--dry-run` 写文件（文件始终为 UTF-8）。

**Q：同一个 feature 能同时用 Cursor 做 dev、用 Claude Code 做 QA 吗？**

可以，因为所有产物都是磁盘上的文件。Cursor 写完 `worktrees.yaml`，Claude Code 读取 `spec.md` 和 `worktrees.yaml` 做 review，完全互通。

**Q：不同 repo 的 deploy.yaml 格式有差异怎么办？**

`deploy.yaml` 的 `strategy` 字段声明部署类型（`docker-compose` / `helm` / `raw-script` / `manual`）。SRE 智能体根据 `strategy` 选择执行方式；`manual` 类型时智能体只输出步骤供人执行。详见 `knowledge/standards/agent-framework.md` 第 5 节。

**Q：智能体配置如何随项目演进？**

只需修改 `meta/agents.yaml` 或 `knowledge/standards/`，然后重新运行 `onecxt adapt`。所有工具的配置自动更新，不需要分别修改 `.cursorrules` / `CLAUDE.md` 等文件。

---

## 相关文档

- `knowledge/standards/agent-framework.md` — 完整框架规范（schema、产物所有权、worktree 约定）
- `meta/agents.yaml` — 智能体注册表（可直接查看各智能体的 instructions）
- `features/core/agent-framework/spec.md` — 本功能的实现路线图
- `docs/architecture.md` — 系统架构
- `features/README.md` — Feature 目录约定
