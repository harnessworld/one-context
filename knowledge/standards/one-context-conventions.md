# one-context conventions

These conventions keep `one-context` agent-agnostic and easy to extend.

## Canonical sources

- **`meta/repos.yaml`**: what repositories exist and where they live locally.
- **`meta/workspaces.yaml`**: task- or theme-oriented views that reference repo ids.
- **`meta/profiles.yaml`**: shared behavior and context policy hints for AI tooling.
- **`knowledge/`**: human- and AI-readable standards, playbooks, and prompt fragments.
- **`features/`**: umbrella-level requirements and delivery artifacts (`spec.md`, design, tests, MR notes, deliverables). Convention: `features/README.md`; index: `features/INDEX.md`. Link implementations using repo **`id`** values from `meta/repos.yaml`.
- **`skills/`**: tool-neutral, executable automation units. Each skill lives in `skills/<name>/` with a `SKILL.md` (frontmatter + instructions) as the canonical source. Skills are adapted to each tool by the adapter layer.

Do not duplicate the same intent in vendor-specific formats. If a tool needs a special file, add an **adapter** that derives it from the canonical sources.

### Skill adapter mapping

| Tool | Output path | Format |
|------|-------------|--------|
| Claude Code | `.claude/skills/<name>/` (symlink → `skills/<name>/`) | SKILL.md native |
| Cursor | `.cursor/rules/skill-<name>.mdc` | Cursor rule with frontmatter |
| OpenClaw | `.openclaw/skills/<name>.json` | JSON with openclaw requires + metadata |

## Source attribution

收录外部资料到 `knowledge/` 时，**必须**在文件头部（blockquote 或 frontmatter）标注：

| 字段 | 必填 | 说明 |
|------|------|------|
| 来源链接 | ✅ | 原文 URL |
| 作者 | ✅ | 原作者或组织 |
| 发布日期 | ✅ | 原文发布日期 |
| 收录日期 | 建议 | 写入知识库的日期 |
| SHA256 | 建议 | 源文档内容 hash（用于增量编译检测，`kb-compile` 自动填充） |

示例：

```markdown
> 来源：[Article Title](https://example.com/article)
> 作者：Author Name (Organization)
> 发布日期：2026-04-15
> 收录日期：2026-04-17
> SHA256：a1b2c3d4e5f6
```

不标注出处的外部资料不得合入 `knowledge/`。

## Tool adapters

Implementations belong under `one_context.adapters` (today: package stubs; later: concrete exporters). Adapters translate; they do not own the meaning of policies or playbooks.

## Validation

After editing manifests, run:

```bash
python -m one_context doctor
```

On some systems the `onecxt` script is not on `PATH`; `python -m one_context` is the portable form.
