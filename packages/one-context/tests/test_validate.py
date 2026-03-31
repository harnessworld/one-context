"""Tests for one_context.validate — doctor() cross-checks."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from one_context.validate import DoctorResult, doctor


class TestDoctor:
    def test_clean_state(self, tmp_root_with_workspaces: Path):
        # Create repo dirs with .git so doctor sees them
        for name in ("alpha", "beta"):
            d = tmp_root_with_workspaces / "repos" / ("develop" if name == "alpha" else "research") / name
            d.mkdir(parents=True, exist_ok=True)
            (d / ".git").mkdir()
        result = doctor(tmp_root_with_workspaces)
        assert result.errors == []
        assert result.warnings == []

    def test_missing_repo_dir_warning(self, tmp_root_with_workspaces: Path):
        result = doctor(tmp_root_with_workspaces)
        assert any("local path missing" in w for w in result.warnings)

    def test_not_git_repo_warning(self, tmp_root_with_workspaces: Path):
        d = tmp_root_with_workspaces / "repos" / "develop" / "alpha"
        d.mkdir(parents=True)
        # no .git directory
        result = doctor(tmp_root_with_workspaces)
        assert any("not a git repo" in w for w in result.warnings)

    def test_unknown_repo_in_workspace(self, tmp_root: Path):
        (tmp_root / "meta" / "workspaces.yaml").write_text(
            textwrap.dedent("""\
                workspaces:
                  - id: ws1
                    repos:
                      - nonexistent-repo
            """),
            encoding="utf-8",
        )
        result = doctor(tmp_root)
        assert any("unknown repo id" in e for e in result.errors)

    def test_unknown_profile_in_workspace(self, tmp_root: Path):
        (tmp_root / "meta" / "workspaces.yaml").write_text(
            textwrap.dedent("""\
                workspaces:
                  - id: ws1
                    repos:
                      - alpha
                    profiles:
                      - nonexistent-profile
            """),
            encoding="utf-8",
        )
        result = doctor(tmp_root)
        assert any("unknown profile id" in e for e in result.errors)

    def test_bad_repos_yaml_returns_error(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text("not valid", encoding="utf-8")
        result = doctor(tmp_path)
        assert len(result.errors) > 0

    def test_bad_workspaces_yaml_error(self, tmp_root: Path):
        (tmp_root / "meta" / "workspaces.yaml").write_text(
            "- just a list\n", encoding="utf-8"
        )
        result = doctor(tmp_root)
        assert any("mapping" in e for e in result.errors)

    def test_bad_profiles_yaml_error(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            "- just a list\n", encoding="utf-8"
        )
        result = doctor(tmp_root)
        assert any("mapping" in e for e in result.errors)

    def test_workspace_repos_not_list(self, tmp_root: Path):
        (tmp_root / "meta" / "workspaces.yaml").write_text(
            textwrap.dedent("""\
                workspaces:
                  - id: ws1
                    repos: "not-a-list"
            """),
            encoding="utf-8",
        )
        result = doctor(tmp_root)
        assert any("'repos' must be a list" in e for e in result.errors)

    def test_workspace_profiles_not_list(self, tmp_root: Path):
        (tmp_root / "meta" / "workspaces.yaml").write_text(
            textwrap.dedent("""\
                workspaces:
                  - id: ws1
                    repos:
                      - alpha
                    profiles: "not-a-list"
            """),
            encoding="utf-8",
        )
        result = doctor(tmp_root)
        assert any("'profiles' must be a list" in e for e in result.errors)
