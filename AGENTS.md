# AGENTS.md — AI Tool Usage Guide

This file provides guidance for AI coding tools (Cursor, Claude Code, Codex, etc.) working in this repository.

## Workspace Layout

- **`packages/one-context/`**: installable Python package; CLI `onecxt` / module `one_context` — **implement CLI changes here**; usage in `packages/one-context/README.md`
- **`meta/repos.yaml`**: repository registry (URL, local path, `id` / `alias`, description)
- **`meta/workspaces.yaml`**: task- or theme-oriented workspace definitions
- **`meta/profiles.yaml`**: shared AI/runtime profiles
- **`knowledge/`**: canonical standards, playbooks, prompts; layout in `knowledge/README.md`
- **`skills/`**: cross-tool executable helpers (e.g. HTML slides → MP4); see `skills/README.md`
- **`features/`**: umbrella-level feature specs; see `features/README.md` and `features/INDEX.md`
- **`docs/`**: architecture docs and contributor templates

## Features / Umbrella Requirements

Cross-repository or product-level requirement documents live in **`features/`**. Before creating, editing, or implementing such requirements, read **`features/README.md`**; index table at **`features/INDEX.md`**. When linking code to features, use the repository **`id`** from `meta/repos.yaml` (do not guess paths).

Playbook: `knowledge/playbooks/add-umbrella-feature.md`.

## Default output style (minimal / 文言极简)

Unless the user **explicitly** asks for a different style, length, format, or language, agents should default to **minimal output**: modern wording, shortest useful phrasing, no pleasantries, do not restate the question—**answer first**. This reduces output tokens and matches `meta/profiles.yaml` profile **`default-coding`** (`output_style.tone: minimal`).

**Overrides:** Phrases such as “详细说明”, “展开讲”, “tutorial 口吻”, “step by step”, “in English”, “用表格”, etc. take precedence for that request.

**Lighter default:** Profile **`default-coding-lighter`** uses `tone: concise` (via mixin `output-concise`) when minimal is too aggressive for a workspace.

Canonical machine-readable policy: `meta/profiles.yaml`; tool-specific text is emitted by adapters (`one_context.adapters`).

## Conventions

- When answering questions or editing code in this umbrella repo, use the manifests above; do not guess remotes or paths.
- For deeper structure, see `docs/architecture.md`.
- After editing manifests, validate with: `onecxt doctor` (or `python -m one_context doctor`)
- Do not run destructive commands without asking.

## Agent Templates

The `docs/templates/` directory contains template files (SOUL.md, USER.md, etc.) that demonstrate how to configure personal AI agent behavior. These are **examples**, not active configuration.
