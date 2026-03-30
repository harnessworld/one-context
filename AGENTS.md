# AGENTS.md — AI Tool Usage Guide

This file provides guidance for AI coding tools (Cursor, Claude Code, Codex, etc.) working in this repository.

## Workspace Layout

- **`meta/repos.yaml`**: repository registry (URL, local path, `id` / `alias`, description)
- **`meta/workspaces.yaml`**: task- or theme-oriented workspace definitions
- **`meta/profiles.yaml`**: shared AI/runtime profiles
- **`knowledge/`**: canonical standards, playbooks, and prompt fragments (tool-neutral)
- **`features/`**: umbrella-level feature specs; see `features/README.md` and `features/INDEX.md`
- **`docs/`**: architecture docs and contributor templates

## Features / Umbrella Requirements

Cross-repository or product-level requirement documents live in **`features/`**. Before creating, editing, or implementing such requirements, read **`features/README.md`**; index table at **`features/INDEX.md`**. When linking code to features, use the repository **`id`** from `meta/repos.yaml` (do not guess paths).

Playbook: `knowledge/playbooks/add-umbrella-feature.md`.

## Conventions

- When answering questions or editing code in this umbrella repo, use the manifests above; do not guess remotes or paths.
- For deeper structure, see `docs/architecture.md`.
- After editing manifests, validate with: `aiws doctor` (or `python -m aiws doctor`)
- Do not run destructive commands without asking.

## Agent Templates

The `docs/templates/` directory contains template files (SOUL.md, USER.md, etc.) that demonstrate how to configure personal AI agent behavior. These are **examples**, not active configuration.
