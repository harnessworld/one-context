from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aiws.context import build_workspace_context
from aiws.profiles import load_profiles
from aiws.repos import load_repos
from aiws.workspaces import load_workspaces


@dataclass
class DoctorResult:
    errors: list[str]
    warnings: list[str]


def doctor(root: Path) -> DoctorResult:
    """
    Cross-check meta/repos.yaml, meta/workspaces.yaml, and meta/profiles.yaml.

    Also emits warnings for expected local paths that are missing or not git repos.
    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        repo_entries, _ = load_repos(root)
    except Exception as e:
        return DoctorResult(errors=[str(e)], warnings=[])

    repo_ids: set[str] = {e["id"] for e in repo_entries}

    try:
        workspaces, _ = load_workspaces(root)
    except Exception as e:
        errors.append(str(e))
        workspaces = []

    try:
        profiles, _ = load_profiles(root)
    except Exception as e:
        errors.append(str(e))
        profiles = []

    profile_ids = {p["id"] for p in profiles}

    for ws in workspaces:
        wid = ws.get("id", "?")
        raw_repos = ws.get("repos")
        if raw_repos is not None:
            if not isinstance(raw_repos, list):
                errors.append(f"workspace {wid!r}: 'repos' must be a list")
            else:
                for rid in raw_repos:
                    if not isinstance(rid, str) or not rid.strip():
                        errors.append(f"workspace {wid!r}: invalid repo id in repos list")
                        continue
                    rid = rid.strip()
                    if rid not in repo_ids:
                        errors.append(
                            f"workspace {wid!r}: unknown repo id {rid!r} "
                            f"(not in meta/repos.yaml)"
                        )

        raw_prof = ws.get("profiles")
        if raw_prof is None:
            continue
        if not isinstance(raw_prof, list):
            errors.append(f"workspace {wid!r}: 'profiles' must be a list")
            continue
        for pid in raw_prof:
            if not isinstance(pid, str) or not pid.strip():
                errors.append(f"workspace {wid!r}: invalid profile id in profiles list")
                continue
            pid = pid.strip()
            if pid not in profile_ids:
                errors.append(
                    f"workspace {wid!r}: unknown profile id {pid!r} "
                    f"(not in meta/profiles.yaml)"
                )

    for entry in repo_entries:
        target = (root / entry["path"]).resolve()
        label = entry["id"]
        if not target.exists():
            warnings.append(f"repo {label}: local path missing {target}")
        elif not (target / ".git").is_dir():
            warnings.append(
                f"repo {label}: path exists but is not a git repo: {target}"
            )

    return DoctorResult(errors=errors, warnings=warnings)


def workspace_context_summary(root: Path, workspace_id: str) -> dict[str, Any]:
    """Return resolved workspace entry plus repo paths for tooling."""
    data = build_workspace_context(root, workspace_id)
    repos_out = [
        {
            "id": repo["id"],
            "path": repo["path"],
            "url": repo["url"],
        }
        for repo in data["repos"]
    ]
    return {"workspace": data["workspace"], "repos": repos_out}
