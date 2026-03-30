# Manifest reference

This document describes the YAML files under `meta/` for `aips-personal`.

## `meta/repos.yaml`

Registers Git remotes and where they should live locally.

| Field | Required | Notes |
|-------|----------|--------|
| `url` | yes | Git remote URL |
| `category` | if `path` omitted | Subfolder under `repos/`; default local path is `repos/<category>/<repo_name>` |
| `path` | no | Override local path relative to aips-personal root |
| `id` | no | Stable id; default: repository name from URL |
| `alias` / `aliases` | no | Extra names accepted by `aiws sync` (case-insensitive) |
| `description` | no | Short human-readable summary |

## `meta/workspaces.yaml`

Task- or theme-oriented views spanning multiple repositories.

| Field | Required | Notes |
|-------|----------|--------|
| `id` | yes | Stable workspace id |
| `name` | no | Display name |
| `description` | no | Purpose of the workspace |
| `repos` | no | List of repo `id`s from `repos.yaml` |
| `profiles` | no | List of profile `id`s from `profiles.yaml` |
| `tags` | no | Labels for filtering or discovery |
| `context` | no | Tool-neutral focus areas and knowledge paths |

## `meta/profiles.yaml`

Shared, tool-neutral behavior and context policy hints for AI tooling.

| Field | Required | Notes |
|-------|----------|--------|
| `id` | yes | Stable profile id |
| `name` | no | Display name |
| `description` | no | Purpose |
| `mode` | no | High-level mode (e.g. edit, review) |
| `behavior` | no | Planning, testing, safety, scope expectations |
| `context_policy` | no | What classes of context to prefer |
| `output_style` | no | Tone and reporting preferences |

Adapters for specific AI products map these fields to their own configuration; they should not redefine intent in parallel.

## Validation

Run:

```bash
aiws doctor
```

This checks YAML consistency (e.g. workspace repo ids and profile ids exist) and warns when registered local paths are missing or not Git repositories.
