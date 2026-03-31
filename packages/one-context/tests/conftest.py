"""Shared pytest fixtures for one-context tests."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest


@pytest.fixture()
def tmp_root(tmp_path: Path) -> Path:
    """Create a minimal one-context directory with meta/repos.yaml."""
    meta = tmp_path / "meta"
    meta.mkdir()
    (meta / "repos.yaml").write_text(
        textwrap.dedent("""\
            repos:
              - url: git@test.local:acme/alpha.git
                category: develop
              - url: git@test.local:acme/beta.git
                category: research
                alias: b
        """),
        encoding="utf-8",
    )
    return tmp_path


@pytest.fixture()
def tmp_root_with_workspaces(tmp_root: Path) -> Path:
    """tmp_root extended with workspaces.yaml and profiles.yaml."""
    meta = tmp_root / "meta"
    (meta / "workspaces.yaml").write_text(
        textwrap.dedent("""\
            workspaces:
              - id: dev
                name: Development
                repos:
                  - alpha
                  - beta
                profiles:
                  - default
        """),
        encoding="utf-8",
    )
    (meta / "profiles.yaml").write_text(
        textwrap.dedent("""\
            profiles:
              - id: default
                name: Default Profile
                description: The default profile
        """),
        encoding="utf-8",
    )
    return tmp_root
