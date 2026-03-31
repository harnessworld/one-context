# one-context Architecture Notes

This document captures the current target architecture for `one-context`.

## Product Position

one-context is a local-first, cross-platform workspace hub for people who manage many Git repositories and want AI tools to share one common context model.

## Main Layers

### 1. Registry Layer

Files under `meta/` describe what exists.

- `repos.yaml`: repository registry
- `workspaces.yaml`: task- or theme-oriented context views
- `profiles.yaml`: shared runtime and AI behavior profiles

### 2. Working Copy Layer

`repos/` contains local clones. Repositories remain independent Git repos; one-context does not merge them into one traditional single-tree monorepo.

### 3. Knowledge Layer

`knowledge/` contains canonical human-and-AI guidance in tool-neutral form.

- `standards/`: conventions and policies
- `playbooks/`: reusable procedures
- `prompts/`: reusable context fragments
- `tools/`: optional notes about how tools consume the layer (not a second source of truth for vendor-specific config)

The tree under `knowledge/` may gain more folders over time. If this list lags, treat **`knowledge/README.md` and the repository** as authoritative.

### 4. Features Layer

`features/` holds umbrella-level requirements and delivery artifacts (spec, technical design, test and MR notes, deliverables). It complements per-repository work in `repos/`: specs here should reference registered repositories by **`id`** from `meta/repos.yaml`. Conventions: `features/README.md`; index: `features/INDEX.md`. Playbook: `knowledge/playbooks/add-umbrella-feature.md`.

### 5. Adapter Layer

Tool-specific exports should live in adapters (today: `one_context.adapters` inside `packages/one-context`; later optionally split into separate packages). Adapters are translation boundaries, not sources of truth.

### 6. Entry Layer

The `onecxt` CLI is implemented in the **`packages/one-context`** installable package (import package `one_context`). It is the user-facing entrypoint for sync, inspection, and manifest validation. Install and command examples: `packages/one-context/README.md`.

Future work: workspace selection helpers, context bundle export, and adapter-driven output for specific AI tools.

## Key Design Rule

Write shared meaning once. Adapt it many times.

The system should avoid storing the same intent separately in multiple vendor-specific configuration files whenever a canonical source can exist instead.
