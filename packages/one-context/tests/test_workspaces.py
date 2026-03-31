"""Tests for one_context.workspaces — optional file, parsing, duplicate detection."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from one_context.errors import ManifestError
from one_context.workspaces import load_workspaces


class TestLoadWorkspaces:
    def test_missing_file_returns_empty(self, tmp_root: Path):
        # tmp_root has repos.yaml but no workspaces.yaml
        workspaces, by_id = load_workspaces(tmp_root)
        assert workspaces == []
        assert by_id == {}

    def test_basic_load(self, tmp_root_with_workspaces: Path):
        workspaces, by_id = load_workspaces(tmp_root_with_workspaces)
        assert len(workspaces) == 1
        assert workspaces[0]["id"] == "dev"
        assert "dev" in by_id

    def test_case_insensitive_lookup(self, tmp_root_with_workspaces: Path):
        _, by_id = load_workspaces(tmp_root_with_workspaces)
        assert by_id.get("DEV".casefold()) is not None

    def test_duplicate_id_raises(self, tmp_root: Path):
        (tmp_root / "meta" / "workspaces.yaml").write_text(
            textwrap.dedent("""\
                workspaces:
                  - id: dup
                    name: First
                  - id: DUP
                    name: Second
            """),
            encoding="utf-8",
        )
        with pytest.raises(ManifestError, match="Duplicate workspace id"):
            load_workspaces(tmp_root)

    def test_missing_id_raises(self, tmp_root: Path):
        (tmp_root / "meta" / "workspaces.yaml").write_text(
            textwrap.dedent("""\
                workspaces:
                  - name: No ID
            """),
            encoding="utf-8",
        )
        with pytest.raises(ManifestError, match="needs a non-empty string 'id'"):
            load_workspaces(tmp_root)

    def test_bad_root_type(self, tmp_root: Path):
        (tmp_root / "meta" / "workspaces.yaml").write_text(
            "- just a list\n", encoding="utf-8"
        )
        with pytest.raises(ManifestError, match="root must be a mapping"):
            load_workspaces(tmp_root)

    def test_null_workspaces_key(self, tmp_root: Path):
        (tmp_root / "meta" / "workspaces.yaml").write_text(
            "workspaces:\n", encoding="utf-8"
        )
        workspaces, by_id = load_workspaces(tmp_root)
        assert workspaces == []

    def test_non_mapping_item_raises(self, tmp_root: Path):
        (tmp_root / "meta" / "workspaces.yaml").write_text(
            textwrap.dedent("""\
                workspaces:
                  - just a string
            """),
            encoding="utf-8",
        )
        with pytest.raises(ManifestError, match="must be a mapping"):
            load_workspaces(tmp_root)
