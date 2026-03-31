"""Tests for one_context.dotenv — quote handling, export prefix, no-override."""

from __future__ import annotations

from pathlib import Path

import pytest

from one_context.dotenv import load_dotenv


class TestLoadDotenv:
    def test_basic_key_value(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        env_file = tmp_path / ".env"
        env_file.write_text("MY_TEST_KEY_1=hello\n", encoding="utf-8")
        monkeypatch.delenv("MY_TEST_KEY_1", raising=False)
        load_dotenv(env_file)
        import os
        assert os.environ["MY_TEST_KEY_1"] == "hello"

    def test_double_quotes_stripped(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        env_file = tmp_path / ".env"
        env_file.write_text('MY_TEST_KEY_2="quoted value"\n', encoding="utf-8")
        monkeypatch.delenv("MY_TEST_KEY_2", raising=False)
        load_dotenv(env_file)
        import os
        assert os.environ["MY_TEST_KEY_2"] == "quoted value"

    def test_single_quotes_stripped(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        env_file = tmp_path / ".env"
        env_file.write_text("MY_TEST_KEY_3='single'\n", encoding="utf-8")
        monkeypatch.delenv("MY_TEST_KEY_3", raising=False)
        load_dotenv(env_file)
        import os
        assert os.environ["MY_TEST_KEY_3"] == "single"

    def test_export_prefix(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        env_file = tmp_path / ".env"
        env_file.write_text("export MY_TEST_KEY_4=exported\n", encoding="utf-8")
        monkeypatch.delenv("MY_TEST_KEY_4", raising=False)
        load_dotenv(env_file)
        import os
        assert os.environ["MY_TEST_KEY_4"] == "exported"

    def test_no_override_existing(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        env_file = tmp_path / ".env"
        env_file.write_text("MY_TEST_KEY_5=new\n", encoding="utf-8")
        monkeypatch.setenv("MY_TEST_KEY_5", "original")
        load_dotenv(env_file)
        import os
        assert os.environ["MY_TEST_KEY_5"] == "original"

    def test_missing_file_no_error(self, tmp_path: Path):
        load_dotenv(tmp_path / "nonexistent.env")

    def test_comments_and_blanks_skipped(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        env_file = tmp_path / ".env"
        env_file.write_text(
            "# comment\n\n  \nMY_TEST_KEY_6=val\n", encoding="utf-8"
        )
        monkeypatch.delenv("MY_TEST_KEY_6", raising=False)
        load_dotenv(env_file)
        import os
        assert os.environ["MY_TEST_KEY_6"] == "val"
