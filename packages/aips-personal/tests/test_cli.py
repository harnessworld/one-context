"""CLI integration tests — exercise real argument parsing + dispatch."""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

from aiws.cli import build_parser, main


class TestBuildParser:
    def test_version_flag(self):
        parser = build_parser()
        with pytest.raises(SystemExit) as exc:
            parser.parse_args(["--version"])
        assert exc.value.code == 0

    def test_doctor_command(self):
        parser = build_parser()
        args = parser.parse_args(["doctor"])
        assert args.command == "doctor"

    def test_sync_command_no_select(self):
        parser = build_parser()
        args = parser.parse_args(["sync"])
        assert args.command == "sync"
        assert args.select == []

    def test_sync_with_select(self):
        parser = build_parser()
        args = parser.parse_args(["sync", "alpha", "beta"])
        assert args.select == ["alpha", "beta"]

    def test_sync_jobs_flag(self):
        parser = build_parser()
        args = parser.parse_args(["sync", "--jobs", "2"])
        assert args.jobs == 2

    def test_verbose_flag(self):
        parser = build_parser()
        args = parser.parse_args(["--verbose", "doctor"])
        assert args.verbose is True

    def test_repo_list(self):
        parser = build_parser()
        args = parser.parse_args(["repo", "list"])
        assert args.command == "repo"
        assert args.repo_command == "list"

    def test_workspace_show(self):
        parser = build_parser()
        args = parser.parse_args(["workspace", "show", "dev"])
        assert args.ws_command == "show"
        assert args.id == "dev"

    def test_context_export(self):
        parser = build_parser()
        args = parser.parse_args(["context", "export", "dev", "--format", "markdown"])
        assert args.context_command == "export"
        assert args.format == "markdown"


class TestMainIntegration:
    def test_doctor_on_valid_root(self, tmp_root_with_workspaces: Path, monkeypatch: pytest.MonkeyPatch):
        # Create repo dirs with .git
        for name, cat in [("alpha", "develop"), ("beta", "research")]:
            d = tmp_root_with_workspaces / "repos" / cat / name
            d.mkdir(parents=True, exist_ok=True)
            (d / ".git").mkdir()

        monkeypatch.setattr(sys, "argv", ["aiws", "--root", str(tmp_root_with_workspaces), "doctor"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0

    def test_repo_list_on_valid_root(self, tmp_root: Path, monkeypatch: pytest.MonkeyPatch, capsys):
        monkeypatch.setattr(sys, "argv", ["aiws", "--root", str(tmp_root), "repo", "list"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert "alpha" in out
        assert "beta" in out

    def test_workspace_list_no_file(self, tmp_root: Path, monkeypatch: pytest.MonkeyPatch, capsys):
        monkeypatch.setattr(sys, "argv", ["aiws", "--root", str(tmp_root), "workspace", "list"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert "no workspaces" in out.lower()

    def test_profile_list_no_file(self, tmp_root: Path, monkeypatch: pytest.MonkeyPatch, capsys):
        monkeypatch.setattr(sys, "argv", ["aiws", "--root", str(tmp_root), "profile", "list"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert "no profiles" in out.lower()

    def test_workspace_show(self, tmp_root_with_workspaces: Path, monkeypatch: pytest.MonkeyPatch, capsys):
        monkeypatch.setattr(
            sys, "argv",
            ["aiws", "--root", str(tmp_root_with_workspaces), "workspace", "show", "dev"],
        )
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert '"workspace"' in out

    def test_context_export_json(self, tmp_root_with_workspaces: Path, monkeypatch: pytest.MonkeyPatch, capsys):
        monkeypatch.setattr(
            sys, "argv",
            ["aiws", "--root", str(tmp_root_with_workspaces), "context", "export", "dev"],
        )
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert '"aiws-context"' in out

    def test_context_export_markdown(self, tmp_root_with_workspaces: Path, monkeypatch: pytest.MonkeyPatch, capsys):
        monkeypatch.setattr(
            sys, "argv",
            ["aiws", "--root", str(tmp_root_with_workspaces), "context", "export", "dev", "--format", "markdown"],
        )
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert "# aips-personal Context Export" in out

    def test_invalid_root(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(sys, "argv", ["aiws", "--root", str(tmp_path), "doctor"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1

    def test_sync_mock(self, tmp_root: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(
            sys, "argv",
            ["aiws", "--root", str(tmp_root), "sync", "--jobs", "1"],
        )
        with patch("aiws.sync.subprocess.run") as mock_run:
            from unittest.mock import MagicMock
            mock_run.return_value = MagicMock(returncode=0)
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 0

    def test_verbose_flag_enables_debug(self, tmp_root: Path, monkeypatch: pytest.MonkeyPatch):
        import logging
        monkeypatch.setattr(sys, "argv", ["aiws", "--verbose", "--root", str(tmp_root), "repo", "list"])
        with pytest.raises(SystemExit):
            main()
        logger = logging.getLogger("aiws")
        assert logger.level == logging.DEBUG
