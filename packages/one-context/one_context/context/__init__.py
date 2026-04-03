"""
Assemble tool-neutral context exports from canonical one-context manifests.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from one_context.profiles import load_profiles
from one_context.repos import load_repos
from one_context.workspaces import load_workspaces


def _collect_knowledge_entries(root: Path, workspace: dict[str, Any]) -> list[dict[str, Any]]:
    context = workspace.get("context")
    if not isinstance(context, dict):
        return []

    raw_paths = context.get("knowledge")
    if not isinstance(raw_paths, list):
        return []

    out: list[dict[str, Any]] = []
    for item in raw_paths:
        if not isinstance(item, str) or not item.strip():
            continue
        rel = Path(item.strip())
        target = (root / rel).resolve()
        if target.is_dir():
            target_type = "directory"
        elif target.is_file():
            target_type = "file"
        else:
            target_type = "missing"
        out.append(
            {
                "path": rel.as_posix(),
                "absolute_path": str(target),
                "exists": target.exists(),
                "type": target_type,
            }
        )
    return out


def build_workspace_context(root: Path, workspace_id: str) -> dict[str, Any]:
    """Build a minimal tool-neutral context export for one workspace."""
    _, ws_by_id = load_workspaces(root)
    if not ws_by_id:
        raise ValueError("No workspaces.yaml or empty workspaces list")

    workspace = ws_by_id.get(workspace_id.casefold())
    if not workspace:
        raise ValueError(f"Unknown workspace id: {workspace_id!r}")

    repo_entries, _ = load_repos(root)
    profile_entries, _ = load_profiles(root)

    repos_by_id = {entry["id"]: entry for entry in repo_entries}
    profiles_by_id = {entry["id"]: entry for entry in profile_entries}

    repos_out: list[dict[str, Any]] = []
    unresolved_repo_ids: list[str] = []
    for raw_repo_id in workspace.get("repos") or []:
        if not isinstance(raw_repo_id, str) or not raw_repo_id.strip():
            continue
        repo_id = raw_repo_id.strip()
        entry = repos_by_id.get(repo_id)
        if not entry:
            unresolved_repo_ids.append(repo_id)
            continue
        repos_out.append(
            {
                "id": entry["id"],
                "url": entry["url"],
                "path": str((root / entry["path"]).resolve()),
                "relative_path": entry["path"].as_posix(),
                "description": entry.get("description") or "",
                "aliases": list(entry.get("aliases") or []),
            }
        )

    profiles_out: list[dict[str, Any]] = []
    unresolved_profile_ids: list[str] = []
    for raw_profile_id in workspace.get("profiles") or []:
        if not isinstance(raw_profile_id, str) or not raw_profile_id.strip():
            continue
        profile_id = raw_profile_id.strip()
        entry = profiles_by_id.get(profile_id)
        if not entry:
            unresolved_profile_ids.append(profile_id)
            continue
        profiles_out.append(entry)

    knowledge_out = _collect_knowledge_entries(root, workspace)

    return {
        "kind": "one-context",
        "version": 1,
        "root": str(root),
        "workspace": workspace,
        "repos": repos_out,
        "profiles": profiles_out,
        "knowledge": knowledge_out,
        "summary": {
            "repo_count": len(repos_out),
            "profile_count": len(profiles_out),
            "knowledge_count": len(knowledge_out),
        },
        "unresolved": {
            "repos": unresolved_repo_ids,
            "profiles": unresolved_profile_ids,
        },
    }


# ---------------------------------------------------------------------------
# Markdown renderer — split into composable helpers
# ---------------------------------------------------------------------------

def _render_header(data: dict[str, Any]) -> list[str]:
    workspace = data.get("workspace") or {}
    workspace_id = workspace.get("id", "")
    workspace_name = workspace.get("name", "")
    description = workspace.get("description", "")

    lines = [
        "# one-context Context Export",
        "",
        f"- Workspace: `{workspace_id}`" + (f" ({workspace_name})" if workspace_name else ""),
        f"- Root: `{data.get('root', '')}`",
        f"- Repositories: {data.get('summary', {}).get('repo_count', 0)}",
        f"- Profiles: {data.get('summary', {}).get('profile_count', 0)}",
        f"- Knowledge Paths: {data.get('summary', {}).get('knowledge_count', 0)}",
    ]
    if description:
        lines.append(f"- Description: {description}")
    return lines


def _render_repos_section(data: dict[str, Any]) -> list[str]:
    lines = ["", "## Repositories", ""]
    repos = data.get("repos") or []
    if repos:
        for repo in repos:
            lines.append(
                f"- `{repo['id']}`: `{repo['relative_path']}` <- {repo['url']}"
            )
            repo_description = repo.get("description")
            if repo_description:
                lines.append(f"  - {repo_description}")
    else:
        lines.append("- None")
    return lines


def _render_profiles_section(data: dict[str, Any]) -> list[str]:
    lines = ["", "## Profiles", ""]
    profiles = data.get("profiles") or []
    if profiles:
        for profile in profiles:
            label = profile.get("id", "")
            name = profile.get("name")
            description = profile.get("description")
            title = f"`{label}`" + (f" ({name})" if name else "")
            if description:
                title += f": {description}"
            lines.append(f"- {title}")
    else:
        lines.append("- None")
    return lines


def _render_knowledge_section(data: dict[str, Any]) -> list[str]:
    lines = ["", "## Knowledge", ""]
    knowledge = data.get("knowledge") or []
    if knowledge:
        for item in knowledge:
            status = "present" if item.get("exists") else "missing"
            lines.append(
                f"- `{item['path']}` ({item.get('type', 'missing')}, {status})"
            )
    else:
        lines.append("- None")
    return lines


def _render_unresolved_section(data: dict[str, Any]) -> list[str]:
    unresolved = data.get("unresolved") or {}
    if not unresolved.get("repos") and not unresolved.get("profiles"):
        return []
    lines = ["", "## Unresolved References", ""]
    for repo_id in unresolved.get("repos") or []:
        lines.append(f"- Missing repo reference: `{repo_id}`")
    for profile_id in unresolved.get("profiles") or []:
        lines.append(f"- Missing profile reference: `{profile_id}`")
    return lines


def render_workspace_context_markdown(data: dict[str, Any]) -> str:
    """Render a human-readable Markdown export for one workspace context."""
    lines: list[str] = []
    lines.extend(_render_header(data))
    lines.extend(_render_repos_section(data))
    lines.extend(_render_profiles_section(data))
    lines.extend(_render_knowledge_section(data))
    lines.extend(_render_unresolved_section(data))
    return "\n".join(lines) + "\n"


def render_workspace_context(data: dict[str, Any], fmt: str) -> str:
    """Render a workspace context in the requested output format."""
    if fmt == "json":
        return json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if fmt == "markdown":
        return render_workspace_context_markdown(data)
    raise ValueError(f"Unsupported context export format: {fmt}")


def apply_context_compression(
    text: str,
    *,
    compress: bool = False,
    target_tokens: int | None = None,
    default_budget_tokens: int = 24_000,
) -> str:
    """
    Enforce an approximate token budget on exported context (lossy).

    Uses a rough heuristic (~4 characters per token). When only *compress* is
    True, *default_budget_tokens* applies. Smarter structured compression can
    replace this without changing the CLI contract.
    """
    if not compress and target_tokens is None:
        return text

    budget = target_tokens if target_tokens is not None else default_budget_tokens
    # Honor small explicit --target-tokens; default path keeps a floor so tiny
    # exports are not over-truncated by accident.
    if target_tokens is not None:
        max_chars = max(64, budget * 4)
    else:
        max_chars = max(512, budget * 4)
    if len(text) <= max_chars:
        return text

    note = (
        "\n\n---\n\n"
        "*[one-context: context truncated to approximate token budget; "
        "adjust with --target-tokens.]*\n"
    )
    # Ensure slice length is non-negative (small budgets vs. long footer).
    take = max(0, min(len(text), max_chars - len(note)))
    return text[:take] + note
