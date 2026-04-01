"""Git worktree lifecycle management for feature branches."""

from __future__ import annotations

import logging
import subprocess
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from one_context.agents import load_agents
from one_context.errors import ManifestError
from one_context.repos import load_repos

logger = logging.getLogger("one_context.worktree")


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def resolve_worktree_config(root: Path) -> dict[str, Any]:
    """Return the ``worktree`` config block from the dev agent.

    Raises ``ManifestError`` if no dev agent or no worktree config is found.
    """
    agents, _ = load_agents(root)
    dev = next((a for a in agents if a.get("role") == "dev"), None)
    if dev is None:
        raise ManifestError("No agent with role=dev found in meta/agents.yaml")
    wt = dev.get("worktree")
    if not wt or not isinstance(wt, dict):
        raise ManifestError("Dev agent has no 'worktree' config in meta/agents.yaml")
    return wt


def find_feature_dir(root: Path, feature_id: str) -> Path | None:
    """Search ``features/*/`` for a matching *feature_id* subdirectory."""
    features_dir = root / "features"
    if not features_dir.is_dir():
        return None
    for category_dir in sorted(features_dir.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith("_"):
            continue
        candidate = category_dir / feature_id
        if candidate.is_dir():
            return candidate
    return None


# ---------------------------------------------------------------------------
# worktrees.yaml I/O
# ---------------------------------------------------------------------------

def load_worktrees_yaml(path: Path) -> dict[str, Any] | None:
    """Parse an existing ``worktrees.yaml``.  Returns *None* when missing."""
    if not path.is_file():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ManifestError(f"worktrees.yaml must be a mapping: {path}")
    return data


def save_worktrees_yaml(path: Path, manifest: dict[str, Any]) -> None:
    """Write *manifest* to ``worktrees.yaml``."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.dump(manifest, default_flow_style=False, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Lifecycle operations
# ---------------------------------------------------------------------------

def setup_worktrees(
    root: Path,
    feature_id: str,
    repo_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Create git worktrees for *feature_id* across repos.

    Returns the worktrees manifest dict that was written to disk.
    """
    wt_cfg = resolve_worktree_config(root)
    branch_pattern = wt_cfg["branch_pattern"]
    path_pattern = wt_cfg["path_pattern"]
    base_branch = wt_cfg.get("base_branch", "main")

    repo_entries, repos_by_key = load_repos(root)
    if not repo_entries:
        raise ManifestError("No repos registered in meta/repos.yaml")

    if repo_ids:
        selected = []
        for rid in repo_ids:
            entry = repos_by_key.get(rid.casefold())
            if entry is None:
                raise ManifestError(f"Unknown repo id {rid!r}")
            selected.append(entry)
        repo_entries = selected

    feature_dir = find_feature_dir(root, feature_id)
    if feature_dir is None:
        raise ManifestError(
            f"Feature directory not found for {feature_id!r}. "
            "Create the feature spec first (PM workflow)."
        )

    branch = branch_pattern.format(feature_id=feature_id)
    worktree_entries: list[dict[str, Any]] = []

    # Load existing manifest to support idempotent re-runs
    yaml_path = feature_dir / "worktrees.yaml"
    existing = load_worktrees_yaml(yaml_path)
    existing_repo_ids: set[str] = set()
    if existing:
        for e in existing.get("worktrees", []):
            existing_repo_ids.add(e.get("repo_id", "").casefold())
        worktree_entries = list(existing.get("worktrees", []))

    for entry in repo_entries:
        rid = entry["id"]
        if rid.casefold() in existing_repo_ids:
            logger.info("Worktree already exists for repo %s, skipping", rid)
            continue

        repo_path = (root / entry["path"]).resolve()
        if not repo_path.is_dir():
            raise ManifestError(
                f"Repo {rid!r} local path missing: {repo_path}. "
                "Run 'onecxt sync' first."
            )

        wt_rel = path_pattern.format(repo_id=rid, feature_id=feature_id)
        wt_abs = (root / wt_rel).resolve()

        # Try creating the worktree
        cmd = [
            "git", "-C", str(repo_path),
            "worktree", "add", str(wt_abs), "-b", branch, base_branch,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # Branch may already exist — retry without -b
            cmd_retry = [
                "git", "-C", str(repo_path),
                "worktree", "add", str(wt_abs), branch,
            ]
            result = subprocess.run(cmd_retry, capture_output=True, text=True)
            if result.returncode != 0:
                raise ManifestError(
                    f"git worktree add failed for repo {rid!r}: "
                    f"{result.stderr.strip()}"
                )

        worktree_entries.append({
            "repo_id": rid,
            "path": wt_rel,
            "branch": branch,
            "base": base_branch,
            "status": "active",
        })

    manifest: dict[str, Any] = {
        "feature_id": feature_id,
        "branch": branch,
        "created_at": existing.get("created_at", str(date.today())) if existing else str(date.today()),
        "worktrees": worktree_entries,
    }
    save_worktrees_yaml(yaml_path, manifest)
    return manifest


def status_worktrees(root: Path, feature_id: str) -> dict[str, Any]:
    """Read ``worktrees.yaml`` for *feature_id* and verify on-disk state.

    Returns the (possibly updated) manifest.
    """
    feature_dir = find_feature_dir(root, feature_id)
    if feature_dir is None:
        raise ValueError(f"Feature directory not found for {feature_id!r}")

    yaml_path = feature_dir / "worktrees.yaml"
    manifest = load_worktrees_yaml(yaml_path)
    if manifest is None:
        raise ValueError(f"No worktrees.yaml found for feature {feature_id!r}")

    for entry in manifest.get("worktrees", []):
        wt_path = root / entry.get("path", "")
        if entry.get("status") == "active" and not wt_path.is_dir():
            entry["status"] = "missing"

    return manifest


def teardown_worktrees(
    root: Path,
    feature_id: str,
    status: str = "merged",
) -> dict[str, Any]:
    """Remove git worktrees for *feature_id* and update ``worktrees.yaml``.

    *status* should be ``"merged"`` or ``"abandoned"``.
    """
    feature_dir = find_feature_dir(root, feature_id)
    if feature_dir is None:
        raise ValueError(f"Feature directory not found for {feature_id!r}")

    yaml_path = feature_dir / "worktrees.yaml"
    manifest = load_worktrees_yaml(yaml_path)
    if manifest is None:
        raise ValueError(f"No worktrees.yaml found for feature {feature_id!r}")

    repo_entries, repos_by_key = load_repos(root)

    for entry in manifest.get("worktrees", []):
        if entry.get("status") != "active":
            continue

        rid = entry.get("repo_id", "")
        repo_entry = repos_by_key.get(rid.casefold())
        if repo_entry is None:
            logger.warning("Repo %s not found in repos.yaml, skipping teardown", rid)
            entry["status"] = status
            continue

        repo_path = (root / repo_entry["path"]).resolve()
        wt_abs = (root / entry.get("path", "")).resolve()

        if wt_abs.is_dir():
            cmd = [
                "git", "-C", str(repo_path),
                "worktree", "remove", str(wt_abs),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                # Try with --force for unclean worktrees
                cmd_force = cmd + ["--force"]
                result = subprocess.run(cmd_force, capture_output=True, text=True)
                if result.returncode != 0:
                    logger.warning(
                        "Failed to remove worktree for %s: %s",
                        rid, result.stderr.strip(),
                    )
                    entry["status"] = "teardown_failed"
                    continue

        entry["status"] = status

    save_worktrees_yaml(yaml_path, manifest)
    return manifest
