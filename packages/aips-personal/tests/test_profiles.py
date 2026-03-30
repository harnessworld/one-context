"""Tests for aiws.profiles — optional file, parsing, duplicate detection."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from aiws.errors import ManifestError
from aiws.profiles import load_profiles


class TestLoadProfiles:
    def test_missing_file_returns_empty(self, tmp_root: Path):
        profiles, by_id = load_profiles(tmp_root)
        assert profiles == []
        assert by_id == {}

    def test_basic_load(self, tmp_root_with_workspaces: Path):
        profiles, by_id = load_profiles(tmp_root_with_workspaces)
        assert len(profiles) == 1
        assert profiles[0]["id"] == "default"
        assert "default" in by_id

    def test_case_insensitive_lookup(self, tmp_root_with_workspaces: Path):
        _, by_id = load_profiles(tmp_root_with_workspaces)
        assert by_id.get("DEFAULT".casefold()) is not None

    def test_duplicate_id_raises(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                profiles:
                  - id: dup
                    name: First
                  - id: DUP
                    name: Second
            """),
            encoding="utf-8",
        )
        with pytest.raises(ManifestError, match="Duplicate profile id"):
            load_profiles(tmp_root)

    def test_missing_id_raises(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                profiles:
                  - name: No ID
            """),
            encoding="utf-8",
        )
        with pytest.raises(ManifestError, match="needs a non-empty string 'id'"):
            load_profiles(tmp_root)

    def test_bad_root_type(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            "- just a list\n", encoding="utf-8"
        )
        with pytest.raises(ManifestError, match="root must be a mapping"):
            load_profiles(tmp_root)

    def test_null_profiles_key(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            "profiles:\n", encoding="utf-8"
        )
        profiles, by_id = load_profiles(tmp_root)
        assert profiles == []

    def test_non_mapping_item_raises(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                profiles:
                  - just a string
            """),
            encoding="utf-8",
        )
        with pytest.raises(ManifestError, match="must be a mapping"):
            load_profiles(tmp_root)
