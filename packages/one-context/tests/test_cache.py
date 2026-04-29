"""Tests for one_context.cache — incremental adapt content cache."""

from __future__ import annotations

from pathlib import Path

import pytest

from one_context.cache import (
    file_hash,
    load_cache,
    needs_write,
    save_cache,
    update_cache,
)


class TestFileHash:
    def test_deterministic(self):
        assert file_hash("hello") == file_hash("hello")

    def test_different_content(self):
        assert file_hash("hello") != file_hash("world")

    def test_empty_string(self):
        h = file_hash("")
        assert isinstance(h, str) and len(h) == 16

    def test_length(self):
        assert len(file_hash("any content")) == 16


class TestLoadSaveCache:
    def test_round_trip(self, tmp_path: Path):
        cache = {"a.md": "abc123", "b.md": "def456"}
        save_cache(tmp_path, cache)
        loaded = load_cache(tmp_path)
        assert loaded == cache

    def test_missing_file_returns_empty(self, tmp_path: Path):
        assert load_cache(tmp_path) == {}

    def test_invalid_json_returns_empty(self, tmp_path: Path):
        cache_file = tmp_path / ".onecxt" / "adapt-cache.json"
        cache_file.parent.mkdir(parents=True)
        cache_file.write_text("not valid json{{{", encoding="utf-8")
        assert load_cache(tmp_path) == {}

    def test_non_dict_json_returns_empty(self, tmp_path: Path):
        cache_file = tmp_path / ".onecxt" / "adapt-cache.json"
        cache_file.parent.mkdir(parents=True)
        cache_file.write_text("[1, 2, 3]", encoding="utf-8")
        assert load_cache(tmp_path) == {}

    def test_creates_directory(self, tmp_path: Path):
        save_cache(tmp_path, {"x.md": "hash1"})
        assert (tmp_path / ".onecxt" / "adapt-cache.json").is_file()

    def test_overwrites_existing(self, tmp_path: Path):
        save_cache(tmp_path, {"a.md": "old"})
        save_cache(tmp_path, {"a.md": "new", "b.md": "extra"})
        loaded = load_cache(tmp_path)
        assert loaded == {"a.md": "new", "b.md": "extra"}


class TestNeedsWrite:
    def test_new_file_needs_write(self):
        cache = {}
        assert needs_write("a.md", "content", cache) is True

    def test_unchanged_file_skipped(self):
        content = "same as before"
        cache = {"a.md": file_hash(content)}
        assert needs_write("a.md", content, cache) is False

    def test_changed_file_needs_write(self):
        cache = {"a.md": file_hash("old content")}
        assert needs_write("a.md", "new content", cache) is True


class TestUpdateCache:
    def test_adds_entry(self):
        cache = {}
        update_cache("a.md", "hello", cache)
        assert cache["a.md"] == file_hash("hello")

    def test_updates_existing(self):
        cache = {"a.md": "old_hash"}
        update_cache("a.md", "new content", cache)
        assert cache["a.md"] == file_hash("new content")