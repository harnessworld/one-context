# Knowledge

This directory is the canonical, tool-neutral knowledge layer for `one-context`.

Its purpose is to store guidance once, then let different AI tools consume or adapt that guidance without rewriting the same intent in multiple vendor-specific formats.

## Principles

- Keep core guidance human-readable.
- Keep canonical meaning independent from any single editor or AI tool.
- Treat provider-specific config as an adapter output, not the source of truth.
- Prefer reusable standards, playbooks, and prompt fragments over duplicated rules.

## Layout

| Directory | Purpose |
|-----------|---------|
| `standards/` | Normative conventions — engineering policies, schema definitions, interface contracts |
| `playbooks/` | Step-by-step operating procedures for common tasks |
| `prompts/` | Reusable text prompt and context fragments for AI tooling |
| `references/` | Analytical documents and curated external indexes (architecture analysis, design references, example collections) |
| `tools/` | Tool-related reference docs (CLI usage, configuration, integration notes) |

Umbrella-level feature specs (not sub-repo issues) live at repo root **`features/`** — see `features/README.md` and playbook `playbooks/add-umbrella-feature.md`.

Executable, tool-agnostic pipelines (Node scripts, single CLI entry) live at repo root **`skills/`** — see `skills/README.md`.

## Classification guide

| Question | Goes in |
|----------|---------|
| "What is the rule / policy / schema?" | `standards/` |
| "How do I do X step by step?" | `playbooks/` |
| "What reusable prompt can I inject?" | `prompts/` |
| "How does system Y work? What articles exist?" | `references/` |
| "How do I use tool Z's CLI?" | `tools/` |

## Language policy

- **README files**: English (stable index, tool-consumable).
- **Content files**: author's choice (Chinese or English). Title format: `English Name — 中文副标题` for Chinese documents, to keep directory indexes scannable.
- **No vendor / platform lock-in**: avoid hard-coding specific platforms (e.g. "语雀") in titles or descriptions; use generic terms (e.g. "PlantUML-compatible platforms").

## Adapter Model

1. Canonical guidance is written here.
2. Workspace and profile metadata decide what guidance applies.
3. Tool adapters convert the relevant guidance into formats understood by Cursor, Claude Code, Codex, OpenClaw, or future tools.

This keeps `knowledge/` stable even when tools change.