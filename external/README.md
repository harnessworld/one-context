# External references

Optional **local git clones** of upstream repositories used as reference material (e.g. Claude Code workflow demos). They are declared in **`meta/repos.yaml`** and are **not** committed to this repository — same loose-coupling model as `repos/develop/` and `repos/research/`.

## Registered clone

| Path | Declared in | Upstream |
|------|-------------|----------|
| `claude-code-best-practice/` | `repos.yaml` → `path: external/claude-code-best-practice` | [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) |

## Get or update the clone

From the one-context root (after `pip install -e ./packages/one-context` if needed):

```text
onecxt sync claude-code-best-practice
```

Or sync everything in the manifest:

```text
onecxt sync
```

Equivalent script:

```text
python scripts/sync_repos.py claude-code-best-practice
```

## Local use

- Open `external/claude-code-best-practice` as the project root in Claude Code to run that repo’s slash commands (see its `README.md`).
- Or copy selected files from its `.claude/` into another project’s `.claude/` (watch for name conflicts).

Skip README sections that assume Slack, web-only, or team cloud features if you only use the local CLI.
