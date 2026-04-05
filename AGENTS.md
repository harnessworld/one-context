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

## Skill routing (mandatory)

When the user’s request matches a workflow below, **do not** answer with ad‑hoc system commands only. **Read the listed `SKILL.md` first**, then follow it (including running scripts from this repo).

| User intent (examples) | Authoritative entry |
|------------------------|---------------------|
| Clean C: / free disk space / 清理 C 盘 / 腾空间 / Docker·npm·WSL eating C: | `skills/windows-c-drive-cleanup/SKILL.md` — phase 1: `survey-c-drive-report.ps1` (read-only); after user **explicitly approves** named cleanup switches: `invoke-c-drive-cleanup.ps1 -ChatAuthorizationNote '…' -DryRun` then without `-DryRun`; optional `survey-disk-hints.ps1` |
| HTML slides + narration → MP4 / 生成视频 / 口播视频 | `skills/html-video-from-slides/SKILL.md` |
| Selective merge to `main` (docs/framework/skills vs business assets) | `skills/merge-to-main/SKILL.md` |

Until the matching `SKILL.md` has been read, treat generic snippets (e.g. only `Get-PSDrive`) as **insufficient** for those intents.
- **`docs/`**: architecture docs and contributor templates

## Features / Umbrella Requirements

Cross-repository or product-level requirement documents live in **`features/`**. Before creating, editing, or implementing such requirements, read **`features/README.md`**; index table at **`features/INDEX.md`**. When linking code to features, use the repository **`id`** from `meta/repos.yaml` (do not guess paths).

Playbook: `knowledge/playbooks/add-umbrella-feature.md`.

## Conventions

- When answering questions or editing code in this umbrella repo, use the manifests above; do not guess remotes or paths.
- For deeper structure, see `docs/architecture.md`.
- After editing manifests, validate with: `onecxt doctor` (or `python -m one_context doctor`)
- Do not run destructive commands without asking.

## Agent Templates

The `docs/templates/` directory contains template files (SOUL.md, USER.md, etc.) that demonstrate how to configure personal AI agent behavior. These are **examples**, not active configuration.
