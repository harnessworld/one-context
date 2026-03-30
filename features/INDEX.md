# Features index

在新建或归档需求时更新本表。`id` 建议与目录名 `features/<category>/<feature-id>/` 中的 `<feature-id>` 一致（或与 `spec.md` frontmatter 的 `id` 一致）。

| id | title | category | status | path | primary_repo_id |
|----|-------|----------|--------|------|-----------------|
| example-feature | Example feature for demonstration | develop | draft | `features/develop/example-feature/` | — |

**Columns**

- **primary_repo_id**: `meta/repos.yaml` 里条目的 `id`（或主实现仓库）；无则填 `—`。
- **path**: 相对 aips-personal 根目录的路径，用反引号包起来便于复制。