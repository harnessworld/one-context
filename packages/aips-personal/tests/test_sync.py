"""Tests for aiws.sync — mock subprocess, clone/pull/skip branches."""

from __future__ import annotations

import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from aiws.sync import SyncResult, sync_one, sync_repositories


class TestSyncOne:
    def test_clone_new_repo(self, tmp_root: Path):
        from aiws.repos import load_repos

        entries, _ = load_repos(tmp_root)
        entry = entries[0]

        with patch("aiws.sync.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = sync_one(entry, tmp_root)

        assert result.success is True
        assert "clone" in result.message.lower()

    def test_pull_existing_repo(self, tmp_root: Path):
        from aiws.repos import load_repos

        entries, _ = load_repos(tmp_root)
        entry = entries[0]
        target = (tmp_root / entry["path"]).resolve()
        target.mkdir(parents=True)
        (target / ".git").mkdir()

        with patch("aiws.sync.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = sync_one(entry, tmp_root)

        assert result.success is True
        assert "update" in result.message.lower()

    def test_skip_non_git_dir(self, tmp_root: Path):
        from aiws.repos import load_repos

        entries, _ = load_repos(tmp_root)
        entry = entries[0]
        target = (tmp_root / entry["path"]).resolve()
        target.mkdir(parents=True)
        # no .git directory

        result = sync_one(entry, tmp_root)
        assert result.success is False
        assert "skip" in result.message.lower()

    def test_clone_failure(self, tmp_root: Path):
        from aiws.repos import load_repos

        entries, _ = load_repos(tmp_root)
        entry = entries[0]

        with patch("aiws.sync.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=128)
            result = sync_one(entry, tmp_root)

        assert result.success is False

    def test_pull_failure(self, tmp_root: Path):
        from aiws.repos import load_repos

        entries, _ = load_repos(tmp_root)
        entry = entries[0]
        target = (tmp_root / entry["path"]).resolve()
        target.mkdir(parents=True)
        (target / ".git").mkdir()

        with patch("aiws.sync.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            result = sync_one(entry, tmp_root)

        assert result.success is False


class TestSyncRepositories:
    def test_sync_all(self, tmp_root: Path):
        with patch("aiws.sync.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            results = sync_repositories(tmp_root, select=None)

        assert len(results) == 2
        assert all(r.success for r in results)

    def test_sync_selected(self, tmp_root: Path):
        with patch("aiws.sync.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            results = sync_repositories(tmp_root, select=["alpha"])

        assert len(results) == 1

    def test_sync_by_alias(self, tmp_root: Path):
        with patch("aiws.sync.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            results = sync_repositories(tmp_root, select=["b"])

        assert len(results) == 1

    def test_unknown_id_raises(self, tmp_root: Path):
        with pytest.raises(SystemExit):
            sync_repositories(tmp_root, select=["nonexistent"])

    def test_workers_param(self, tmp_root: Path):
        with patch("aiws.sync.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            results = sync_repositories(tmp_root, select=None, workers=1)

        assert len(results) == 2

    def test_concurrent_execution(self, tmp_root: Path):
        with patch("aiws.sync.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            results = sync_repositories(tmp_root, select=None, workers=4)

        assert len(results) == 2
