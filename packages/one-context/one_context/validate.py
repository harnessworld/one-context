from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from one_context.agents import load_agents
from one_context.context import build_workspace_context
from one_context.profiles import load_mixins, load_profiles
from one_context.repos import load_repos
from one_context.workspaces import load_workspaces

VALID_ROLES = {"pm", "architect", "dev", "qa", "sre", "knowledge-keeper"}


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
        profiles, profiles_by_id = load_profiles(root)
    except Exception as e:
        errors.append(str(e))
        profiles = []
        profiles_by_id = {}

    try:
        mixins, mixins_by_id = load_mixins(root)
    except Exception as e:
        errors.append(str(e))
        mixins = []
        mixins_by_id = {}

    profile_ids = {p["id"] for p in profiles}

    # --- Inheritance & mixin validation ---
    for p in profiles:
        pid = p["id"]
        parent_id = p.get("extends")
        if parent_id:
            plk = parent_id.casefold()
            if plk not in profiles_by_id:
                errors.append(
                    f"profile {pid!r}: extends unknown profile {parent_id!r}"
                )
            else:
                parent = profiles_by_id[plk]
                if parent.get("extends"):
                    errors.append(
                        f"profile {pid!r}: multi-layer inheritance not allowed "
                        f"(parent {parent_id!r} also has 'extends')"
                    )
                if parent.get("mixins"):
                    errors.append(
                        f"profile {pid!r}: parent {parent_id!r} must not have 'mixins'"
                    )

        mixin_refs = p.get("mixins") or []
        for mid in mixin_refs:
            mlk = mid.casefold()
            if mlk not in mixins_by_id:
                errors.append(
                    f"profile {pid!r}: references unknown mixin {mid!r}"
                )

    for m in mixins:
        mid = m["id"]
        if m.get("extends"):
            errors.append(f"mixin {mid!r}: mixins must not have 'extends'")
        if m.get("mixins"):
            errors.append(f"mixin {mid!r}: mixins must not have 'mixins'")

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

    # --- Agents validation ---
    try:
        agents, agents_by_id = load_agents(root)
    except Exception as e:
        errors.append(str(e))
        agents = []
        agents_by_id = {}

    for agent in agents:
        aid = agent.get("id", "?")

        # Validate role
        role = agent.get("role")
        if not role:
            errors.append(f"agent {aid!r}: missing required 'role' field")
        elif role not in VALID_ROLES:
            errors.append(
                f"agent {aid!r}: invalid role {role!r}. "
                f"Must be one of: {', '.join(sorted(VALID_ROLES))}"
            )

        # Validate profile reference
        profile_ref = agent.get("profile")
        if profile_ref:
            plk = profile_ref.casefold()
            if plk not in profiles_by_id:
                errors.append(
                    f"agent {aid!r}: references unknown profile {profile_ref!r}"
                )

        # Validate knowledge paths (warn only)
        knowledge_paths = agent.get("knowledge") or []
        for kp in knowledge_paths:
            if not isinstance(kp, str) or not kp.strip():
                continue
            target = (root / kp.strip()).resolve()
            if not target.exists():
                warnings.append(
                    f"agent {aid!r}: knowledge path not found: {kp}"
                )

        # Validate worktree config (dev agent)
        wt = agent.get("worktree")
        if wt:
            if role and role != "dev":
                warnings.append(
                    f"agent {aid!r}: 'worktree' config is intended for "
                    f"role=dev, but agent has role={role!r}"
                )
            if isinstance(wt, dict):
                for req_key in ("branch_pattern", "path_pattern"):
                    if not wt.get(req_key):
                        errors.append(
                            f"agent {aid!r}: worktree.{req_key} is required"
                        )
                bp = wt.get("branch_pattern", "")
                pp = wt.get("path_pattern", "")
                if bp and "{feature_id}" not in bp:
                    warnings.append(
                        f"agent {aid!r}: worktree.branch_pattern should "
                        "contain {{feature_id}} placeholder"
                    )
                if pp and ("{repo_id}" not in pp or "{feature_id}" not in pp):
                    warnings.append(
                        f"agent {aid!r}: worktree.path_pattern should "
                        "contain {{repo_id}} and {{feature_id}} placeholders"
                    )
            else:
                errors.append(
                    f"agent {aid!r}: 'worktree' must be a mapping"
                )

    # --- deploy.yaml validation (per-repo) ---
    sre_agent = next(
        (a for a in agents if a.get("role") == "sre"), None
    )
    deploy_filename = (
        sre_agent.get("deploy_manifest", "deploy.yaml") if sre_agent else None
    )
    if deploy_filename:
        for entry in repo_entries:
            repo_path = (root / entry["path"]).resolve()
            deploy_path = repo_path / deploy_filename
            if deploy_path.is_file():
                from one_context.deploy import validate_deploy_yaml

                d_errors, d_warnings = validate_deploy_yaml(deploy_path)
                for e in d_errors:
                    errors.append(
                        f"repo {entry['id']!r} {deploy_filename}: {e}"
                    )
                for w in d_warnings:
                    warnings.append(
                        f"repo {entry['id']!r} {deploy_filename}: {w}"
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
