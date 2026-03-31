"""Tests for one_context.root — ONECXT_ROOT, parent traversal, error on miss."""

from __future__ import annotations

from pathlib import Path

import pytest

from one_context.errors import ManifestError
from one_context.root import find_root


def _clear_root_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ONECXT_ROOT", raising=False)


class TestFindRoot:
    def test_env_var_onecxt(self, tmp_root: Path, monkeypatch: pytest.MonkeyPatch):
        _clear_root_env(monkeypatch)
        monkeypatch.setenv("ONECXT_ROOT", str(tmp_root))
        assert find_root() == tmp_root

    def test_env_var_missing_manifest(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _clear_root_env(monkeypatch)
        monkeypatch.setenv("ONECXT_ROOT", str(tmp_path))
        with pytest.raises(ManifestError, match="ONECXT_ROOT is set"):
            find_root()

    def test_walk_parents(self, tmp_root: Path, monkeypatch: pytest.MonkeyPatch):
        _clear_root_env(monkeypatch)
        child = tmp_root / "sub" / "deep"
        child.mkdir(parents=True)
        assert find_root(start=child) == tmp_root

    def test_not_found_raises(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _clear_root_env(monkeypatch)
        with pytest.raises(ManifestError, match="Could not find"):
            find_root(start=tmp_path)

    def test_start_is_root(self, tmp_root: Path, monkeypatch: pytest.MonkeyPatch):
        _clear_root_env(monkeypatch)
        assert find_root(start=tmp_root) == tmp_root
