"""Tests for aiws.root — AIWS_ROOT env var, parent traversal, error on miss."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from aiws.errors import ManifestError
from aiws.root import find_root


class TestFindRoot:
    def test_env_var(self, tmp_root: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("AIWS_ROOT", str(tmp_root))
        assert find_root() == tmp_root

    def test_env_var_missing_manifest(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("AIWS_ROOT", str(tmp_path))
        with pytest.raises(ManifestError, match="AIWS_ROOT is set"):
            find_root()

    def test_walk_parents(self, tmp_root: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("AIWS_ROOT", raising=False)
        child = tmp_root / "sub" / "deep"
        child.mkdir(parents=True)
        assert find_root(start=child) == tmp_root

    def test_not_found_raises(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("AIWS_ROOT", raising=False)
        with pytest.raises(ManifestError, match="Could not find"):
            find_root(start=tmp_path)

    def test_start_is_root(self, tmp_root: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("AIWS_ROOT", raising=False)
        assert find_root(start=tmp_root) == tmp_root
