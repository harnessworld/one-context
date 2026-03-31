"""Tests for one_context.context — build_workspace_context + render."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from one_context.context import (
    build_workspace_context,
    render_workspace_context,
    render_workspace_context_markdown,
)


class TestBuildWorkspaceContext:
    def test_basic_build(self, tmp_root_with_workspaces: Path):
        ctx = build_workspace_context(tmp_root_with_workspaces, "dev")
        assert ctx["kind"] == "one-context"
        assert ctx["version"] == 1
        assert len(ctx["repos"]) == 2
        assert len(ctx["profiles"]) == 1

    def test_unknown_workspace_raises(self, tmp_root_with_workspaces: Path):
        with pytest.raises(ValueError, match="Unknown workspace id"):
            build_workspace_context(tmp_root_with_workspaces, "nonexistent")

    def test_no_workspaces_raises(self, tmp_root: Path):
        with pytest.raises(ValueError, match="No workspaces"):
            build_workspace_context(tmp_root, "anything")

    def test_unresolved_repo(self, tmp_root: Path):
        (tmp_root / "meta" / "workspaces.yaml").write_text(
            textwrap.dedent("""\
                workspaces:
                  - id: ws1
                    repos:
                      - alpha
                      - ghost-repo
            """),
            encoding="utf-8",
        )
        ctx = build_workspace_context(tmp_root, "ws1")
        assert "ghost-repo" in ctx["unresolved"]["repos"]

    def test_unresolved_profile(self, tmp_root_with_workspaces: Path):
        (tmp_root_with_workspaces / "meta" / "workspaces.yaml").write_text(
            textwrap.dedent("""\
                workspaces:
                  - id: dev
                    repos:
                      - alpha
                    profiles:
                      - default
                      - ghost-profile
            """),
            encoding="utf-8",
        )
        ctx = build_workspace_context(tmp_root_with_workspaces, "dev")
        assert "ghost-profile" in ctx["unresolved"]["profiles"]

    def test_knowledge_paths(self, tmp_root_with_workspaces: Path):
        knowledge_dir = tmp_root_with_workspaces / "knowledge"
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        (knowledge_dir / "test.md").write_text("# Test", encoding="utf-8")

        (tmp_root_with_workspaces / "meta" / "workspaces.yaml").write_text(
            textwrap.dedent("""\
                workspaces:
                  - id: dev
                    repos:
                      - alpha
                    context:
                      knowledge:
                        - knowledge/test.md
                        - knowledge/missing.md
            """),
            encoding="utf-8",
        )
        ctx = build_workspace_context(tmp_root_with_workspaces, "dev")
        assert len(ctx["knowledge"]) == 2
        assert ctx["knowledge"][0]["exists"] is True
        assert ctx["knowledge"][1]["exists"] is False

    def test_summary_counts(self, tmp_root_with_workspaces: Path):
        ctx = build_workspace_context(tmp_root_with_workspaces, "dev")
        assert ctx["summary"]["repo_count"] == 2
        assert ctx["summary"]["profile_count"] == 1

    def test_case_insensitive_workspace_id(self, tmp_root_with_workspaces: Path):
        ctx = build_workspace_context(tmp_root_with_workspaces, "DEV")
        assert ctx["workspace"]["id"] == "dev"


class TestRenderContext:
    def test_json_format(self, tmp_root_with_workspaces: Path):
        ctx = build_workspace_context(tmp_root_with_workspaces, "dev")
        rendered = render_workspace_context(ctx, "json")
        parsed = json.loads(rendered)
        assert parsed["kind"] == "one-context"

    def test_markdown_format(self, tmp_root_with_workspaces: Path):
        ctx = build_workspace_context(tmp_root_with_workspaces, "dev")
        rendered = render_workspace_context(ctx, "markdown")
        assert "# one-context Context Export" in rendered
        assert "## Repositories" in rendered

    def test_unsupported_format_raises(self, tmp_root_with_workspaces: Path):
        ctx = build_workspace_context(tmp_root_with_workspaces, "dev")
        with pytest.raises(ValueError, match="Unsupported"):
            render_workspace_context(ctx, "xml")


class TestRenderMarkdown:
    def test_contains_workspace_info(self, tmp_root_with_workspaces: Path):
        ctx = build_workspace_context(tmp_root_with_workspaces, "dev")
        md = render_workspace_context_markdown(ctx)
        assert "`dev`" in md
        assert "Development" in md

    def test_contains_repo_section(self, tmp_root_with_workspaces: Path):
        ctx = build_workspace_context(tmp_root_with_workspaces, "dev")
        md = render_workspace_context_markdown(ctx)
        assert "`alpha`" in md

    def test_unresolved_section(self, tmp_root: Path):
        (tmp_root / "meta" / "workspaces.yaml").write_text(
            textwrap.dedent("""\
                workspaces:
                  - id: ws1
                    repos:
                      - ghost
            """),
            encoding="utf-8",
        )
        ctx = build_workspace_context(tmp_root, "ws1")
        md = render_workspace_context_markdown(ctx)
        assert "## Unresolved References" in md
        assert "`ghost`" in md
