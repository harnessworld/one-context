# Features index

在新建或归档需求时更新本表。`id` 建议与目录名 `features/<category>/<feature-id>/` 中的 `<feature-id>` 一致（或与 `spec.md` frontmatter 的 `id` 一致）。


| id                            | title                                                 | category | status | path                                              | primary_repo_id |
| ----------------------------- | ----------------------------------------------------- | -------- | ------ | ------------------------------------------------- | --------------- |
| agent-framework               | 智能体框架 — meta/agents.yaml + 适配器扩展 + worktree/deploy 约定 | core     | done   | `features/core/agent-framework/`                  | one-context     |
| auto-context-compression      | 自动上下文压缩 — 定时扫描 knowledge/features 等，去重与去陈旧            | core     | draft  | `features/core/auto-context-compression/`         | one-context     |
| agent-collaboration           | 智能体协作增强 — 状态流转、决策手册、条件知识、生成保护                         | core     | draft  | `features/core/agent-collaboration/`              | one-context     |
| profile-inheritance           | Profile 继承与 Mixin 机制                                  | core     | draft  | `features/core/profile-inheritance/`              | one-context     |
| claudecode-source-analysis    | Claude Code 源码解析知识整理                                  | develop  | done   | `features/develop/claudecode-source-analysis/`    | one-context     |
| openclaw-source-analysis      | OpenClaw 源码解析知识整理                                     | develop  | done   | `features/develop/openclaw-source-analysis/`      | one-context     |
| claude-caveman-mode           | 用穴居人模式让 Claude 省 Token                                | develop  | done   | `features/develop/claude-caveman-mode/`           | one-context     |
| math-teacher-ai-platform      | 数学教师 AI 工作台 — Phase 1 可视化资产化与 AI 出题 MVP          | develop  | draft  | `features/develop/math-teacher-ai-platform/`      | FunctionCanvas  |
| one-context-intro-short-video | one-context 中视频介绍（爆款口播框架）                             | develop  | draft  | `features/develop/one-context-intro-short-video/` | one-context     |
| skill-windows-c-drive-cleanup | Windows C 盘空间清理 — 仓库内 Agent Skill                     | core     | done   | `features/core/skill-windows-c-drive-cleanup/`    | one-context     |


**Columns**

- **primary_repo_id**: `meta/repos.yaml` 里条目的 `id`（或主实现仓库）；无则填 `—`。
- **path**: 相对 one-context 根目录的路径，用反引号包起来便于复制。

