"""Tests for one_context.worktree — worktree lifecycle management."""

from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path

import pytest
import yaml

from one_context.errors import ManifestError
from one_context.worktree import (
    find_feature_dir,
    load_worktrees_yaml,
    resolve_worktree_config,
    save_worktrees_yaml,
    setup_worktrees,
    status_worktrees,
    teardown_worktrees,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

AGENTS_WITH_DEV = textwrap.dedent("""\
    agents:
      - id: dev
        name: Dev Agent
        role: dev
        worktree:
          branch_pattern: "feature/{feature_id}"
          path_pattern: "repos/{repo_id}/.worktrees/{feature_id}"
          base_branch: main
""")

AGENTS_NO_DEV = textwrap.dedent("""\
    agents:
      - id: pm
        name: PM Agent
        role: pm
""")


def _init_git_repo(path: Path) -> None:
    """Create a bare-minimum git repo at *path*."""
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", str(path)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(path), "commit", "--allow-empty", "-m", "init"],
        check=True, capture_output=True,
    )


def _make_root_with_repo(tmp_path: Path) -> Path:
    """Create a one-context root with one repo that is an actual git repo."""
    root = tmp_path
    meta = root / "meta"
    meta.mkdir(parents=True)
    (meta / "repos.yaml").write_text(
        textwrap.dedent("""\
            repos:
              - url: git@test.local:acme/alpha.git
                id: alpha
                path: repos/develop/alpha
        """),
        encoding="utf-8",
    )
    (meta / "agents.yaml").write_text(AGENTS_WITH_DEV, encoding="utf-8")

    # Init real git repo
    repo_path = root / "repos" / "develop" / "alpha"
    _init_git_repo(repo_path)

    # Create feature directory
    feat = root / "features" / "core" / "my-feature"
    feat.mkdir(parents=True)
    (feat / "spec.md").write_text("---\nid: my-feature\n---\n", encoding="utf-8")

    return root


# ---------------------------------------------------------------------------
# resolve_worktree_config
# ---------------------------------------------------------------------------

class TestResolveWorktreeConfig:
    def test_returns_config(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text("repos: []\n", encoding="utf-8")
        (meta / "agents.yaml").write_text(AGENTS_WITH_DEV, encoding="utf-8")

        cfg = resolve_worktree_config(tmp_path)
        assert cfg["branch_pattern"] == "feature/{feature_id}"
        assert cfg["path_pattern"] == "repos/{repo_id}/.worktrees/{feature_id}"
        assert cfg["base_branch"] == "main"

    def test_no_dev_agent_raises(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text("repos: []\n", encoding="utf-8")
        (meta / "agents.yaml").write_text(AGENTS_NO_DEV, encoding="utf-8")

        with pytest.raises(ManifestError, match="role=dev"):
            resolve_worktree_config(tmp_path)


# ---------------------------------------------------------------------------
# find_feature_dir
# ---------------------------------------------------------------------------

class TestFindFeatureDir:
    def test_found(self, tmp_path: Path):
        feat = tmp_path / "features" / "core" / "my-feature"
        feat.mkdir(parents=True)
        assert find_feature_dir(tmp_path, "my-feature") == feat

    def test_not_found(self, tmp_path: Path):
        (tmp_path / "features" / "core").mkdir(parents=True)
        assert find_feature_dir(tmp_path, "nonexistent") is None

    def test_no_features_dir(self, tmp_path: Path):
        assert find_feature_dir(tmp_path, "anything") is None

    def test_skips_template_dir(self, tmp_path: Path):
        (tmp_path / "features" / "_template" / "my-feature").mkdir(parents=True)
        assert find_feature_dir(tmp_path, "my-feature") is None


# ---------------------------------------------------------------------------
# load / save worktrees.yaml
# ---------------------------------------------------------------------------

class TestWorktreesYaml:
    def test_round_trip(self, tmp_path: Path):
        manifest = {
            "feature_id": "test",
            "branch": "feature/test",
            "created_at": "2026-01-01",
            "worktrees": [
                {
                    "repo_id": "alpha",
                    "path": "repos/alpha/.worktrees/test",
                    "branch": "feature/test",
                    "base": "main",
                    "status": "active",
                },
            ],
        }
        p = tmp_path / "worktrees.yaml"
        save_worktrees_yaml(p, manifest)
        loaded = load_worktrees_yaml(p)
        assert loaded is not None
        assert loaded["feature_id"] == "test"
        assert len(loaded["worktrees"]) == 1
        assert loaded["worktrees"][0]["repo_id"] == "alpha"

    def test_load_missing_returns_none(self, tmp_path: Path):
        assert load_worktrees_yaml(tmp_path / "worktrees.yaml") is None


# ---------------------------------------------------------------------------
# setup_worktrees (integration)
# ---------------------------------------------------------------------------

class TestSetupWorktrees:
    def test_no_repos_raises(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text("repos: []\n", encoding="utf-8")
        (meta / "agents.yaml").write_text(AGENTS_WITH_DEV, encoding="utf-8")
        feat = tmp_path / "features" / "core" / "my-feature"
        feat.mkdir(parents=True)

        with pytest.raises(ManifestError, match="No repos"):
            setup_worktrees(tmp_path, "my-feature")

    def test_feature_not_found_raises(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text(
            textwrap.dedent("""\
                repos:
                  - url: git@test.local:acme/alpha.git
                    id: alpha
                    path: repos/develop/alpha
            """),
            encoding="utf-8",
        )
        (meta / "agents.yaml").write_text(AGENTS_WITH_DEV, encoding="utf-8")

        with pytest.raises(ManifestError, match="not found"):
            setup_worktrees(tmp_path, "nonexistent")

    def test_success(self, tmp_path: Path):
        root = _make_root_with_repo(tmp_path)
        manifest = setup_worktrees(root, "my-feature")

        assert manifest["feature_id"] == "my-feature"
        assert manifest["branch"] == "feature/my-feature"
        assert len(manifest["worktrees"]) == 1

        wt = manifest["worktrees"][0]
        assert wt["repo_id"] == "alpha"
        assert wt["status"] == "active"

        # Verify worktree exists on disk
        wt_path = root / wt["path"]
        assert wt_path.is_dir()

        # Verify worktrees.yaml was written
        yaml_path = root / "features" / "core" / "my-feature" / "worktrees.yaml"
        assert yaml_path.is_file()

    def test_idempotent_rerun(self, tmp_path: Path):
        root = _make_root_with_repo(tmp_path)
        m1 = setup_worktrees(root, "my-feature")
        m2 = setup_worktrees(root, "my-feature")
        assert len(m2["worktrees"]) == len(m1["worktrees"])


# ---------------------------------------------------------------------------
# status_worktrees
# ---------------------------------------------------------------------------

class TestStatusWorktrees:
    def test_status(self, tmp_path: Path):
        root = _make_root_with_repo(tmp_path)
        setup_worktrees(root, "my-feature")
        manifest = status_worktrees(root, "my-feature")
        assert manifest["worktrees"][0]["status"] == "active"

    def test_no_worktrees_yaml_raises(self, tmp_path: Path):
        feat = tmp_path / "features" / "core" / "my-feature"
        feat.mkdir(parents=True)
        with pytest.raises(ValueError, match="No worktrees.yaml"):
            status_worktrees(tmp_path, "my-feature")

    def test_no_feature_dir_raises(self, tmp_path: Path):
        with pytest.raises(ValueError, match="not found"):
            status_worktrees(tmp_path, "nonexistent")


# ---------------------------------------------------------------------------
# teardown_worktrees (integration)
# ---------------------------------------------------------------------------

class TestTeardownWorktrees:
    def test_teardown(self, tmp_path: Path):
        root = _make_root_with_repo(tmp_path)
        setup_worktrees(root, "my-feature")

        manifest = teardown_worktrees(root, "my-feature", "merged")
        assert manifest["worktrees"][0]["status"] == "merged"

        # Verify worktree removed from disk
        wt_path = root / manifest["worktrees"][0]["path"]
        assert not wt_path.exists()

    def test_teardown_abandoned(self, tmp_path: Path):
        root = _make_root_with_repo(tmp_path)
        setup_worktrees(root, "my-feature")

        manifest = teardown_worktrees(root, "my-feature", "abandoned")
        assert manifest["worktrees"][0]["status"] == "abandoned"
