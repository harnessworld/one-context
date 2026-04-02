# Features index

在新建或归档需求时更新本表。`id` 建议与目录名 `features/<category>/<feature-id>/` 中的 `<feature-id>` 一致（或与 `spec.md` frontmatter 的 `id` 一致）。

| id | title | category | status | path | primary_repo_id |
|----|-------|----------|--------|------|-----------------|
| agent-framework | 智能体框架 — meta/agents.yaml + 适配器扩展 + worktree/deploy 约定 | core | in_progress | `features/core/agent-framework/` | one-context |
| agent-collaboration | 智能体协作增强 — 状态流转、决策手册、条件知识、生成保护 | core | draft | `features/core/agent-collaboration/` | one-context |
| profile-inheritance | Profile 继承与 Mixin 机制 | core | draft | `features/core/profile-inheritance/` | one-context |
| claudecode-source-analysis | Claude Code 源码解析知识整理 | develop | done | `features/develop/claudecode-source-analysis/` | one-context |
| openclaw-source-analysis | OpenClaw 源码解析知识整理 | develop | done | `features/develop/openclaw-source-analysis/` | one-context |

**Columns**

- **primary_repo_id**: `meta/repos.yaml` 里条目的 `id`（或主实现仓库）；无则填 `—`。
- **path**: 相对 one-context 根目录的路径，用反引号包起来便于复制。