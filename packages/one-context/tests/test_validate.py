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


class TestDoctorInheritance:
    """Doctor checks for extends / mixins validation."""

    def test_extends_unknown_profile(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                profiles:
                  - id: child
                    name: Child
                    extends: nonexistent
            """),
            encoding="utf-8",
        )
        result = doctor(tmp_root)
        assert any("extends unknown profile" in e for e in result.errors)

    def test_multi_layer_extends(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                profiles:
                  - id: grandparent
                    name: GP
                  - id: parent
                    name: Parent
                    extends: grandparent
                  - id: child
                    name: Child
                    extends: parent
            """),
            encoding="utf-8",
        )
        result = doctor(tmp_root)
        assert any("multi-layer inheritance" in e for e in result.errors)

    def test_parent_with_mixins(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                mixins:
                  - id: mx
                    name: MX
                profiles:
                  - id: parent
                    name: Parent
                    mixins:
                      - mx
                  - id: child
                    name: Child
                    extends: parent
            """),
            encoding="utf-8",
        )
        result = doctor(tmp_root)
        assert any("must not have 'mixins'" in e for e in result.errors)

    def test_unknown_mixin_reference(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                profiles:
                  - id: p1
                    name: P1
                    mixins:
                      - nonexistent
            """),
            encoding="utf-8",
        )
        result = doctor(tmp_root)
        assert any("unknown mixin" in e for e in result.errors)

    def test_mixin_with_extends_is_error(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                mixins:
                  - id: bad-mixin
                    name: Bad
                    extends: something
                profiles:
                  - id: p1
                    name: P1
            """),
            encoding="utf-8",
        )
        result = doctor(tmp_root)
        assert any("mixins must not have 'extends'" in e for e in result.errors)

    def test_mixin_with_mixins_is_error(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                mixins:
                  - id: bad-mixin
                    name: Bad
                    mixins:
                      - something
                profiles:
                  - id: p1
                    name: P1
            """),
            encoding="utf-8",
        )
        result = doctor(tmp_root)
        assert any("mixins must not have 'mixins'" in e for e in result.errors)

    def test_valid_inheritance_no_errors(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                mixins:
                  - id: strict
                    name: Strict
                    behavior:
                      safety_level: conservative
                profiles:
                  - id: base
                    name: Base
                    behavior:
                      plan_first: false
                  - id: child
                    name: Child
                    extends: base
                    mixins:
                      - strict
            """),
            encoding="utf-8",
        )
        result = doctor(tmp_root)
        assert result.errors == []
