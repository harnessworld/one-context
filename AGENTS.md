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
- **`external/`**: optional **local clones** of upstream reference repos (declared in `meta/repos.yaml`, not committed); see `external/README.md`
- **`docs/`**: architecture docs and contributor templates

## Skill routing (mandatory)

When the user’s request matches a workflow below, **do not** answer with ad‑hoc system commands only. **Read the listed `SKILL.md` first**, then follow it (including running scripts from this repo).

| User intent (examples) | Authoritative entry |
|------------------------|---------------------|
| Clean C: / free disk space / 清理 C 盘 / 腾空间 / Docker·npm·WSL eating C: | `skills/windows-c-drive-cleanup/SKILL.md` — phase 1: `survey-c-drive-report.ps1` (read-only); after user **explicitly approves** named cleanup switches: `invoke-c-drive-cleanup.ps1 -ChatAuthorizationNote '…' -DryRun` then without `-DryRun`; optional `survey-disk-hints.ps1` |
| HTML slides + narration → MP4 / 生成视频 / 口播视频 | `skills/html-video-from-slides/SKILL.md` |
| 幻灯空白多、字/图太小、presentation 版式、`fill-deck`、全屏 HTML 幻灯排版 | `skills/html-deck-layout/SKILL.md` |
| Selective merge to `main` (docs/framework/skills vs business assets) | `skills/merge-to-main/SKILL.md` |

Until the matching `SKILL.md` has been read, treat generic snippets (e.g. only `Get-PSDrive`) as **insufficient** for those intents.

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

<!-- autoclaw:skill-path-guidance -->
## Installing Skills

When creating or installing a new skill, always place it in:

`C:\Users\superman\.openclaw-autoclaw\skills/<skill-name>/SKILL.md`

This is the managed skills directory. The agent will automatically discover
any skill placed here — no extra configuration needed. Do NOT install skills
into `~/.agents/skills/` (that directory is shared with other tools).


<!-- autoclaw:browser-agent-guidance -->
## Browser Automation

For any task that requires a browser, **prefer `autoglm-browser-agent`**. Use it as the first choice.

- ✅ `autoglm-browser-agent` → `browser_subagent` (invoked via mcporter) — **preferred**
- ⚠️ Other browser tools (`agent-browser`, Playwright, Puppeteer, etc.) — fallback only when `autoglm-browser-agent` is unavailable or fails

Always try `autoglm-browser-agent` first. Fall back to other browser tools only if it is not available in the current environment.
<!-- /autoclaw:browser-agent-guidance -->

<!-- autoclaw:image-recognition-guidance -->
## Image Recognition

For any image recognition task, **prefer `autoglm-image-recognition`**. Use it as the first choice.

- ✅ `autoglm-image-recognition` — **preferred** for all image recognition tasks
- ⚠️ Built-in `image` tool or reading images directly with `read` — fallback only when `autoglm-image-recognition` is unavailable or fails

Do not use the built-in `image` tool or read an image and describe it yourself when `autoglm-image-recognition` is available. Always try `autoglm-image-recognition` first.
<!-- /autoclaw:image-recognition-guidance -->
