# Knowledge

This directory is the canonical, tool-neutral knowledge layer for `aips-personal`.

Its purpose is to store guidance once, then let different AI tools consume or adapt that guidance without rewriting the same intent in multiple vendor-specific formats.

## Principles

- Keep core guidance human-readable.
- Keep canonical meaning independent from any single editor or AI tool.
- Treat provider-specific config as an adapter output, not the source of truth.
- Prefer reusable standards, playbooks, and prompt fragments over duplicated rules.

## Suggested Layout

- `standards/`: engineering conventions, repository policies, naming rules
- `playbooks/`: step-by-step operating procedures for common tasks
- `prompts/`: reusable prompt/context fragments

Umbrella-level feature specs (not sub-repo issues) live at repo root **`features/`** — see `features/README.md` and playbook `playbooks/add-umbrella-feature.md`.

## Adapter Model

The long-term architecture should work like this:

1. Canonical guidance is written here.
2. Workspace and profile metadata decide what guidance applies.
3. Tool adapters convert the relevant guidance into formats understood by Cursor, Claude Code, Codex, OpenClaw, or future tools.

This keeps `knowledge/` stable even when tools change.
