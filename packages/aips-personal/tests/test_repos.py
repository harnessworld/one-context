"""Tests for aiws.repos — YAML parsing, URL inference, alias handling."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from aiws.errors import ManifestError
from aiws.repos import _normalize_aliases, _repo_name_from_url, load_repos


# --- _repo_name_from_url ---

class TestRepoNameFromUrl:
    def test_simple_https(self):
        assert _repo_name_from_url("git@test.local:org/my-repo.git") == "my-repo"

    def test_no_git_suffix(self):
        assert _repo_name_from_url("git@test.local:org/my-repo") == "my-repo"

    def test_trailing_slash(self):
        assert _repo_name_from_url("git@test.local:org/my-repo/") == "my-repo"

    def test_ssh_style(self):
        # urlparse treats git@... as a path, last segment still works
        assert _repo_name_from_url("git@test.local:org/sub/repo-name.git") == "repo-name"

    def test_empty_path_raises(self):
        with pytest.raises(ManifestError, match="Cannot infer repo name"):
            _repo_name_from_url("git@test.local:")

    def test_whitespace_stripped(self):
        assert _repo_name_from_url("  git@test.local:o/r.git  ") == "r"


# --- _normalize_aliases ---

class TestNormalizeAliases:
    def test_none_returns_empty(self):
        assert _normalize_aliases(None) == []

    def test_string(self):
        assert _normalize_aliases("foo") == ["foo"]

    def test_empty_string(self):
        assert _normalize_aliases("  ") == []

    def test_list_of_strings(self):
        assert _normalize_aliases(["a", " b "]) == ["a", "b"]

    def test_list_filters_blanks(self):
        assert _normalize_aliases(["a", "", "  ", "b"]) == ["a", "b"]

    def test_invalid_type_raises(self):
        with pytest.raises(ManifestError, match="alias must be string or list"):
            _normalize_aliases(42)


# --- load_repos ---

class TestLoadRepos:
    def test_basic_load(self, tmp_root: Path):
        entries, by_key = load_repos(tmp_root)
        assert len(entries) == 2
        assert entries[0]["id"] == "alpha"
        assert entries[1]["id"] == "beta"
        assert "alpha" in by_key
        assert "b" in by_key  # alias

    def test_url_inferred_name(self, tmp_root: Path):
        entries, _ = load_repos(tmp_root)
        # id defaults to repo name extracted from URL
        assert entries[0]["id"] == "alpha"

    def test_path_from_category(self, tmp_root: Path):
        entries, _ = load_repos(tmp_root)
        assert entries[0]["path"] == Path("repos/develop/alpha")
        assert entries[1]["path"] == Path("repos/research/beta")

    def test_explicit_id(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text(
            textwrap.dedent("""\
                repos:
                  - url: git@test.local:x/y.git
                    id: custom-id
                    path: repos/custom
            """),
            encoding="utf-8",
        )
        entries, by_key = load_repos(tmp_path)
        assert entries[0]["id"] == "custom-id"
        assert "custom-id" in by_key

    def test_explicit_path(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text(
            textwrap.dedent("""\
                repos:
                  - url: git@test.local:x/y.git
                    path: my/custom/path
            """),
            encoding="utf-8",
        )
        entries, _ = load_repos(tmp_path)
        assert entries[0]["path"] == Path("my/custom/path")

    def test_missing_manifest_raises(self, tmp_path: Path):
        with pytest.raises(ManifestError, match="Manifest not found"):
            load_repos(tmp_path)

    def test_bad_root_type_raises(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text("- just a list\n", encoding="utf-8")
        with pytest.raises(ManifestError, match="root must be a mapping"):
            load_repos(tmp_path)

    def test_missing_repos_key_raises(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text("other: true\n", encoding="utf-8")
        with pytest.raises(ManifestError, match="must contain a 'repos' list"):
            load_repos(tmp_path)

    def test_duplicate_id_raises(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text(
            textwrap.dedent("""\
                repos:
                  - url: git@test.local:x/dup.git
                    category: a
                  - url: git@test.local:y/dup.git
                    category: b
            """),
            encoding="utf-8",
        )
        with pytest.raises(ManifestError, match="Duplicate id/alias"):
            load_repos(tmp_path)

    def test_case_insensitive_lookup(self, tmp_root: Path):
        _, by_key = load_repos(tmp_root)
        assert by_key.get("ALPHA".casefold()) is not None
        assert by_key.get("Alpha".casefold()) is not None

    def test_missing_url_raises(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text(
            textwrap.dedent("""\
                repos:
                  - category: dev
            """),
            encoding="utf-8",
        )
        with pytest.raises(ManifestError, match="needs a string 'url'"):
            load_repos(tmp_path)

    def test_no_category_no_path_raises(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text(
            textwrap.dedent("""\
                repos:
                  - url: git@test.local:x/y.git
            """),
            encoding="utf-8",
        )
        with pytest.raises(ManifestError, match="needs 'category'"):
            load_repos(tmp_path)

    def test_aliases_field(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text(
            textwrap.dedent("""\
                repos:
                  - url: git@test.local:x/y.git
                    path: repos/y
                    aliases:
                      - yy
                      - yyy
            """),
            encoding="utf-8",
        )
        entries, by_key = load_repos(tmp_path)
        assert "yy" in by_key
        assert "yyy" in by_key

    def test_description_stored(self, tmp_path: Path):
        meta = tmp_path / "meta"
        meta.mkdir()
        (meta / "repos.yaml").write_text(
            textwrap.dedent("""\
                repos:
                  - url: git@test.local:x/y.git
                    path: repos/y
                    description: My cool repo
            """),
            encoding="utf-8",
        )
        entries, _ = load_repos(tmp_path)
        assert entries[0]["description"] == "My cool repo"
