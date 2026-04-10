"""Tests for tool adapters (Claude Code, Cursor, OpenClaw)."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

# Trigger registration side effects
import one_context.adapters.claude_code  # noqa: F401
import one_context.adapters.cursor  # noqa: F401
import one_context.adapters.hermes  # noqa: F401
import one_context.adapters.openclaw  # noqa: F401

from one_context.adapters import ADAPTERS, GeneratedFile, get_adapter, list_adapters


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def adapter_root(tmp_path: Path) -> Path:
    """Create a minimal one-context tree with knowledge files."""
    meta = tmp_path / "meta"
    meta.mkdir()

    (meta / "repos.yaml").write_text(
        textwrap.dedent("""\
            repos:
              - url: git@test.local:acme/alpha.git
                category: develop
        """),
        encoding="utf-8",
    )
    (meta / "profiles.yaml").write_text(
        textwrap.dedent("""\
            profiles:
              - id: default-coding
                name: Default Coding
                description: Balanced editing profile.
                mode: edit
                behavior:
                  plan_first: false
                  test_expectation: targeted
                  safety_level: standard
                  change_scope: focused
                context_policy:
                  load:
                    - repo-readme
                output_style:
                  tone: concise
                  include_verification: true
        """),
        encoding="utf-8",
    )
    (meta / "workspaces.yaml").write_text(
        textwrap.dedent("""\
            workspaces:
              - id: dev
                name: Development
                repos:
                  - alpha
                profiles:
                  - default-coding
                context:
                  summary: Development workspace for daily coding.
                  focus:
                    - feature development
                    - bug fixes
                  knowledge:
                    - knowledge/standards/
        """),
        encoding="utf-8",
    )
    (meta / "agents.yaml").write_text(
        textwrap.dedent("""\
            version: "1"
            agents:
              - id: pm
                name: PM Agent
                role: pm
                profile: default-coding
                description: Test PM agent.
                knowledge:
                  - knowledge/standards/
                owns:
                  - "features/**/spec.md"
                instructions: |
                  You are the PM agent for tests.
        """),
        encoding="utf-8",
    )

    # Create knowledge files
    knowledge_dir = tmp_path / "knowledge" / "standards"
    knowledge_dir.mkdir(parents=True)
    (knowledge_dir / "conventions.md").write_text(
        "# Conventions\n\nFollow these conventions.\n",
        encoding="utf-8",
    )

    return tmp_path


@pytest.fixture()
def dev_context(adapter_root: Path) -> dict:
    """Build context for the 'dev' workspace."""
    from one_context.context import build_workspace_context
    return build_workspace_context(adapter_root, "dev")


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class TestRegistry:
    def test_all_adapters_registered(self):
        names = list_adapters()
        assert "claude_code" in names
        assert "cursor" in names
        assert "hermes" in names
        assert "openclaw" in names

    def test_get_adapter(self):
        adapter = get_adapter("claude_code")
        assert adapter.name == "claude_code"

    def test_get_unknown_adapter(self):
        with pytest.raises(ValueError, match="Unknown adapter"):
            get_adapter("nonexistent")


# ---------------------------------------------------------------------------
# Claude Code Adapter
# ---------------------------------------------------------------------------

class TestClaudeCodeAdapter:
    def test_generates_file(self, adapter_root, dev_context):
        adapter = get_adapter("claude_code")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)

        assert len(files) == 1
        gf = files[0]
        assert isinstance(gf, GeneratedFile)
        assert gf.rel_path == ".claude/adapters/onecxt-dev.md"
        assert "dev" in gf.description

    def test_content_has_workspace_header(self, adapter_root, dev_context):
        adapter = get_adapter("claude_code")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content

        assert "# one-context" in content
        assert "`dev`" in content

    def test_content_has_profile_rules(self, adapter_root, dev_context):
        adapter = get_adapter("claude_code")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content

        assert "Profile: Default Coding" in content
        # Should have the "no plan" rule since plan_first=false
        assert "without" in content.lower() or "directly" in content.lower()

    def test_content_has_knowledge_refs(self, adapter_root, dev_context):
        adapter = get_adapter("claude_code")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content

        # Claude Code uses @file references
        assert "@knowledge/" in content

    def test_supports_file_ref(self):
        adapter = get_adapter("claude_code")
        assert adapter.supports_file_ref is True

    def test_content_has_focus_areas(self, adapter_root, dev_context):
        adapter = get_adapter("claude_code")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content

        assert "Focus Areas" in content
        assert "feature development" in content

    def test_generate_project_artifacts_writes_claude_md(self, adapter_root):
        from one_context.agents import load_agents

        adapter = get_adapter("claude_code")
        agents, _ = load_agents(adapter_root)
        files = adapter.generate_project_artifacts(adapter_root, ["dev"], agents)
        assert len(files) == 1
        assert files[0].rel_path == "CLAUDE.md"
        assert "@.claude/adapters/onecxt-dev.md" in files[0].content
        assert "@.claude/agents/pm.md" in files[0].content


# ---------------------------------------------------------------------------
# Hermes Adapter
# ---------------------------------------------------------------------------

class TestHermesAdapter:
    def test_generates_file(self, adapter_root, dev_context):
        adapter = get_adapter("hermes")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)

        assert len(files) == 1
        gf = files[0]
        assert isinstance(gf, GeneratedFile)
        assert gf.rel_path == ".hermes/onecxt-dev.md"

    def test_content_has_workspace_header(self, adapter_root, dev_context):
        adapter = get_adapter("hermes")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content

        assert "# one-context" in content
        assert "`dev`" in content

    def test_content_has_profile_rules(self, adapter_root, dev_context):
        adapter = get_adapter("hermes")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content

        assert "Profile: Default Coding" in content
        assert "without" in content.lower() or "directly" in content.lower()

    def test_content_inlines_knowledge(self, adapter_root, dev_context):
        adapter = get_adapter("hermes")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content

        # Hermes inlines knowledge content
        assert "Conventions" in content
        assert "<!-- source:" in content

    def test_does_not_support_file_ref(self):
        adapter = get_adapter("hermes")
        assert adapter.supports_file_ref is False

    def test_content_has_focus_areas(self, adapter_root, dev_context):
        adapter = get_adapter("hermes")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content

        assert "Focus Areas" in content
        assert "feature development" in content

    def test_generate_project_artifacts_writes_hermes_md(self, adapter_root):
        from one_context.agents import load_agents

        adapter = get_adapter("hermes")
        ws = self._get_dev_workspace(adapter_root)
        ctx = self._get_dev_context(adapter_root)
        adapter.generate(adapter_root, ws, ctx)

        agents, _ = load_agents(adapter_root)
        adapter.generate_agents(adapter_root, agents, {})
        files = adapter.generate_project_artifacts(adapter_root, ["dev"], agents)

        hermes_md = next(f for f in files if f.rel_path == ".hermes.md")
        assert hermes_md is not None
        # Should contain workspace content
        assert "Development workspace" in hermes_md.content
        # Should contain agent content
        assert "PM Agent" in hermes_md.content

    @staticmethod
    def _get_dev_workspace(root: Path) -> dict:
        from one_context.context import build_workspace_context
        ctx = build_workspace_context(root, "dev")
        return ctx["workspace"]

    @staticmethod
    def _get_dev_context(root: Path) -> dict:
        from one_context.context import build_workspace_context
        return build_workspace_context(root, "dev")


class TestHermesTopPlacement:
    """Tests for top-placement (hard rules) when tone=minimal."""

    def test_hard_rules_prepended_to_hermes_md(self, minimal_root, minimal_context):
        from one_context.agents import load_agents

        adapter = get_adapter("hermes")
        ws = minimal_context["workspace"]
        adapter.generate(minimal_root, ws, minimal_context)

        agents, _ = load_agents(minimal_root)
        adapter.generate_agents(minimal_root, agents, {})
        files = adapter.generate_project_artifacts(minimal_root, ["dev"], agents)

        hermes_md = next(f for f in files if f.rel_path == ".hermes.md")
        assert "ALWAYS respond" in hermes_md.content
        # Hard rule should come before the title
        title_pos = hermes_md.content.index("# one-context")
        hard_pos = hermes_md.content.index("ALWAYS respond")
        assert hard_pos < title_pos

    def test_inline_rules_exclude_top_placement(self, minimal_root, minimal_context):
        adapter = get_adapter("hermes")
        ws = minimal_context["workspace"]
        files = adapter.generate(minimal_root, ws, minimal_context)
        content = files[0].content
        assert "Default to minimal output" not in content


class TestHermesGenerateAgents:
    def test_generates_agent_file(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("hermes")
        files = adapter.generate_agents(root, agents, profiles)
        assert len(files) >= 1
        assert any("pm.md" in gf.rel_path for gf in files)

    def test_content_has_instructions(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("hermes")
        files = adapter.generate_agents(root, agents, profiles)
        content = files[0].content
        assert "PM agent" in content or "PM Agent" in content

    def test_content_has_artifact_ownership(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("hermes")
        files = adapter.generate_agents(root, agents, profiles)
        content = files[0].content
        assert "Artifact Ownership" in content

    def test_content_has_profile_section(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("hermes")
        files = adapter.generate_agents(root, agents, profiles)
        content = files[0].content
        assert "Profile" in content

    def test_inlines_knowledge(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("hermes")
        files = adapter.generate_agents(root, agents, profiles)
        content = files[0].content
        assert "Conventions" in content


# ---------------------------------------------------------------------------
# Cursor Adapter
# ---------------------------------------------------------------------------

class TestCursorAdapter:
    def test_generates_mdc_file(self, adapter_root, dev_context):
        adapter = get_adapter("cursor")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)

        assert len(files) == 1
        gf = files[0]
        assert gf.rel_path == ".cursor/rules/onecxt-dev.mdc"

    def test_has_mdc_frontmatter(self, adapter_root, dev_context):
        adapter = get_adapter("cursor")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content

        assert content.startswith("---\n")
        assert "alwaysApply: true" in content

    def test_content_has_profile_rules(self, adapter_root, dev_context):
        adapter = get_adapter("cursor")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content

        assert "Profile:" in content

    def test_inlines_knowledge(self, adapter_root, dev_context):
        adapter = get_adapter("cursor")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content

        # Cursor inlines knowledge, should contain actual content
        assert "Conventions" in content
        assert "<!-- source:" in content

    def test_does_not_support_file_ref(self):
        adapter = get_adapter("cursor")
        assert adapter.supports_file_ref is False


# ---------------------------------------------------------------------------
# OpenClaw Adapter
# ---------------------------------------------------------------------------

class TestOpenClawAdapter:
    def test_generates_json_file(self, adapter_root, dev_context):
        adapter = get_adapter("openclaw")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)

        assert len(files) == 1
        gf = files[0]
        assert gf.rel_path == ".openclaw/onecxt-dev.json"

    def test_valid_json(self, adapter_root, dev_context):
        adapter = get_adapter("openclaw")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content

        data = json.loads(content)
        assert data["workspace_id"] == "dev"

    def test_has_instructions(self, adapter_root, dev_context):
        adapter = get_adapter("openclaw")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)

        data = json.loads(files[0].content)
        assert "instructions" in data
        assert len(data["instructions"]) > 0

    def test_has_knowledge(self, adapter_root, dev_context):
        adapter = get_adapter("openclaw")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)

        data = json.loads(files[0].content)
        assert "knowledge" in data
        assert len(data["knowledge"]) > 0
        assert "source" in data["knowledge"][0]
        assert "content" in data["knowledge"][0]

    def test_does_not_support_file_ref(self):
        adapter = get_adapter("openclaw")
        assert adapter.supports_file_ref is False

    def test_has_profile_metadata(self, adapter_root, dev_context):
        adapter = get_adapter("openclaw")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)

        data = json.loads(files[0].content)
        assert "profiles" in data
        assert data["profiles"][0]["id"] == "default-coding"

    def test_generate_project_artifacts_manifest(self, adapter_root):
        from one_context.agents import load_agents

        adapter = get_adapter("openclaw")
        agents, _ = load_agents(adapter_root)
        files = adapter.generate_project_artifacts(adapter_root, ["dev"], agents)
        assert len(files) == 1
        assert files[0].rel_path == ".openclaw/onecxt-project.json"
        data = json.loads(files[0].content)
        oc = data["one_context"]
        assert oc["version"] == 1
        assert oc["workspaces"][0]["path"] == ".openclaw/onecxt-dev.json"
        assert any(a["id"] == "pm" for a in oc["agents"])


# ---------------------------------------------------------------------------
# CLI adapt command (integration)
# ---------------------------------------------------------------------------

class TestAdaptCLI:
    def test_adapt_dry_run(self, adapter_root, capsys):
        from one_context.cli import build_parser, _resolve_root

        parser = build_parser()
        args = parser.parse_args(["--root", str(adapter_root), "adapt", "dev", "--dry-run"])

        from one_context.cli import _cmd_adapt
        rc = _cmd_adapt(adapter_root, args)
        assert rc == 0

        captured = capsys.readouterr()
        assert "---" in captured.out  # dry-run separators
        assert "claude_code" in captured.out.lower() or "Claude Code" in captured.out

    def test_adapt_writes_files(self, adapter_root):
        from one_context.cli import build_parser
        parser = build_parser()
        args = parser.parse_args(["--root", str(adapter_root), "adapt", "dev"])

        from one_context.cli import _cmd_adapt
        rc = _cmd_adapt(adapter_root, args)
        assert rc == 0

        # Check files were created
        assert (adapter_root / ".claude" / "adapters" / "onecxt-dev.md").is_file()
        assert (adapter_root / ".cursor" / "rules" / "onecxt-dev.mdc").is_file()
        assert (adapter_root / ".openclaw" / "onecxt-dev.json").is_file()
        assert (adapter_root / "CLAUDE.md").is_file()
        assert "@.claude/adapters/onecxt-dev.md" in (adapter_root / "CLAUDE.md").read_text(
            encoding="utf-8",
        )
        assert (adapter_root / ".openclaw" / "onecxt-project.json").is_file()
        assert (adapter_root / ".claude" / "agents" / "pm.md").is_file()
        assert (adapter_root / ".openclaw" / "agents" / "pm.json").is_file()

    def test_adapt_only_filter(self, adapter_root):
        from one_context.cli import build_parser
        parser = build_parser()
        args = parser.parse_args([
            "--root", str(adapter_root), "adapt", "dev", "--only", "cursor",
        ])

        from one_context.cli import _cmd_adapt
        rc = _cmd_adapt(adapter_root, args)
        assert rc == 0

        assert (adapter_root / ".cursor" / "rules" / "onecxt-dev.mdc").is_file()
        assert not (adapter_root / ".claude" / "adapters" / "onecxt-dev.md").is_file()

    def test_adapt_unknown_workspace(self, adapter_root, capsys):
        from one_context.cli import build_parser
        parser = build_parser()
        args = parser.parse_args(["--root", str(adapter_root), "adapt", "nonexistent"])

        from one_context.cli import _cmd_adapt
        rc = _cmd_adapt(adapter_root, args)
        assert rc == 2

    def test_adapt_no_args(self, adapter_root, capsys):
        from one_context.cli import build_parser
        parser = build_parser()
        args = parser.parse_args(["--root", str(adapter_root), "adapt"])

        from one_context.cli import _cmd_adapt
        rc = _cmd_adapt(adapter_root, args)
        assert rc == 2


# ---------------------------------------------------------------------------
# generate_agents unit tests
# ---------------------------------------------------------------------------

@pytest.fixture()
def agents_and_profiles(adapter_root: Path) -> tuple:
    """Load agents and resolved profiles from adapter_root."""
    from one_context.agents import load_agents
    from one_context.profiles import load_mixins, load_profiles, resolve_profile

    agents, _ = load_agents(adapter_root)
    _, profiles_by_id = load_profiles(adapter_root)
    _, mixins_by_id = load_mixins(adapter_root)

    resolved: dict = {}
    for pid in profiles_by_id:
        try:
            resolved[pid] = resolve_profile(pid, profiles_by_id, mixins_by_id)
        except Exception:
            resolved[pid] = profiles_by_id[pid]

    return adapter_root, agents, resolved


class TestClaudeCodeGenerateAgents:
    def test_generates_agent_file(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("claude_code")
        files = adapter.generate_agents(root, agents, profiles)
        assert len(files) >= 1
        assert any("pm.md" in gf.rel_path for gf in files)

    def test_content_has_instructions(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("claude_code")
        files = adapter.generate_agents(root, agents, profiles)
        content = files[0].content
        assert "PM agent" in content or "PM Agent" in content

    def test_content_has_artifact_ownership(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("claude_code")
        files = adapter.generate_agents(root, agents, profiles)
        content = files[0].content
        assert "Artifact Ownership" in content or "spec.md" in content

    def test_content_has_profile_section(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("claude_code")
        files = adapter.generate_agents(root, agents, profiles)
        content = files[0].content
        assert "Profile" in content

    def test_content_has_knowledge_refs(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("claude_code")
        files = adapter.generate_agents(root, agents, profiles)
        content = files[0].content
        assert "@knowledge/" in content


class TestCursorGenerateAgents:
    def test_generates_agent_mdc(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("cursor")
        files = adapter.generate_agents(root, agents, profiles)
        assert len(files) >= 1
        assert any("agent-pm.mdc" in gf.rel_path for gf in files)

    def test_has_mdc_frontmatter(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("cursor")
        files = adapter.generate_agents(root, agents, profiles)
        content = files[0].content
        assert content.startswith("---\n")
        assert "alwaysApply:" in content

    def test_content_has_instructions(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("cursor")
        files = adapter.generate_agents(root, agents, profiles)
        content = files[0].content
        assert "PM agent" in content or "PM Agent" in content

    def test_inlines_knowledge(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("cursor")
        files = adapter.generate_agents(root, agents, profiles)
        content = files[0].content
        assert "Conventions" in content


class TestOpenClawGenerateAgents:
    def test_generates_agent_json(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("openclaw")
        files = adapter.generate_agents(root, agents, profiles)
        assert len(files) >= 1
        assert any("pm.json" in gf.rel_path for gf in files)

    def test_valid_json_with_instructions(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("openclaw")
        files = adapter.generate_agents(root, agents, profiles)
        data = json.loads(files[0].content)
        assert "instructions" in data
        assert len(data["instructions"]) > 0

    def test_has_knowledge(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("openclaw")
        files = adapter.generate_agents(root, agents, profiles)
        data = json.loads(files[0].content)
        assert "knowledge" in data

    def test_has_artifact_ownership(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("openclaw")
        files = adapter.generate_agents(root, agents, profiles)
        data = json.loads(files[0].content)
        assert "owns" in data or "artifact" in json.dumps(data).lower()


# ---------------------------------------------------------------------------
# Shared rules identity test
# ---------------------------------------------------------------------------

class TestSharedRulesIdentity:
    """Verify all adapters reference the same PROFILE_RULES object."""

    def test_all_adapters_share_same_rules(self):
        from one_context.adapters._shared_rules import PROFILE_RULES as shared
        from one_context.adapters.claude_code import PROFILE_RULES as cc
        from one_context.adapters.cursor import PROFILE_RULES as cu
        from one_context.adapters.hermes import PROFILE_RULES as hm
        from one_context.adapters.openclaw import PROFILE_RULES as oc
        assert cc is shared
        assert cu is shared
        assert hm is shared
        assert oc is shared

    def test_shared_rules_count(self):
        from one_context.adapters._shared_rules import PROFILE_RULES
        assert len(PROFILE_RULES) == 13


# ---------------------------------------------------------------------------
# Golden tests — output stability after shared-rules migration
# ---------------------------------------------------------------------------

class TestGoldenOutput:
    """Verify generated output contains unified wording and GENERATED marker."""

    def test_claude_code_workspace_has_marker(self, adapter_root, dev_context):
        adapter = get_adapter("claude_code")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content
        assert "GENERATED by onecxt adapt" in content

    def test_claude_code_workspace_has_unified_rules(self, adapter_root, dev_context):
        adapter = get_adapter("claude_code")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content
        assert "You may edit code directly without creating a formal plan first." in content
        assert "Write targeted tests for the specific changes you make." in content

    def test_cursor_workspace_has_marker(self, adapter_root, dev_context):
        adapter = get_adapter("cursor")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content
        assert "GENERATED by onecxt adapt" in content

    def test_cursor_workspace_has_unified_rules(self, adapter_root, dev_context):
        adapter = get_adapter("cursor")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content
        assert "You may edit code directly without creating a formal plan first." in content

    def test_openclaw_workspace_has_marker(self, adapter_root, dev_context):
        adapter = get_adapter("openclaw")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        data = json.loads(files[0].content)
        assert "_generated" in data
        assert "GENERATED by onecxt adapt" in data["_generated"]

    def test_openclaw_workspace_has_unified_rules(self, adapter_root, dev_context):
        adapter = get_adapter("openclaw")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        data = json.loads(files[0].content)
        assert any("without creating a formal plan" in i for i in data["instructions"])
        assert any("targeted tests for the specific changes" in i for i in data["instructions"])

    def test_openclaw_agents_have_marker(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("openclaw")
        files = adapter.generate_agents(root, agents, profiles)
        data = json.loads(files[0].content)
        assert "_generated" in data

    def test_openclaw_project_manifest_has_marker(self, agents_and_profiles):
        root, agents, profiles = agents_and_profiles
        adapter = get_adapter("openclaw")
        files = adapter.generate_project_artifacts(root, ["dev"], agents)
        data = json.loads(files[0].content)
        assert "_generated" in data

    def test_hermes_workspace_has_marker(self, adapter_root, dev_context):
        adapter = get_adapter("hermes")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content
        assert "GENERATED by onecxt adapt" in content

    def test_hermes_workspace_has_unified_rules(self, adapter_root, dev_context):
        adapter = get_adapter("hermes")
        ws = dev_context["workspace"]
        files = adapter.generate(adapter_root, ws, dev_context)
        content = files[0].content
        assert "You may edit code directly without creating a formal plan first." in content
        assert "Write targeted tests for the specific changes you make." in content


# ---------------------------------------------------------------------------
# --check mode tests
# ---------------------------------------------------------------------------

class TestAdaptCheck:
    def test_check_passes_when_fresh(self, adapter_root):
        from one_context.cli import build_parser, _cmd_adapt

        parser = build_parser()
        # First generate
        args = parser.parse_args(["--root", str(adapter_root), "adapt", "dev"])
        assert _cmd_adapt(adapter_root, args) == 0
        # Then check
        args = parser.parse_args(["--root", str(adapter_root), "adapt", "dev", "--check"])
        assert _cmd_adapt(adapter_root, args) == 0

    def test_check_fails_when_stale(self, adapter_root):
        from one_context.cli import build_parser, _cmd_adapt

        parser = build_parser()
        args = parser.parse_args(["--root", str(adapter_root), "adapt", "dev"])
        assert _cmd_adapt(adapter_root, args) == 0
        # Tamper with a generated file
        (adapter_root / ".claude" / "adapters" / "onecxt-dev.md").write_text(
            "tampered", encoding="utf-8",
        )
        args = parser.parse_args(["--root", str(adapter_root), "adapt", "dev", "--check"])
        assert _cmd_adapt(adapter_root, args) == 1

    def test_check_fails_when_missing(self, adapter_root):
        from one_context.cli import build_parser, _cmd_adapt

        parser = build_parser()
        # Don't generate first — files are missing
        args = parser.parse_args(["--root", str(adapter_root), "adapt", "dev", "--check"])
        assert _cmd_adapt(adapter_root, args) == 1

    def test_check_and_dry_run_exclusive(self, adapter_root):
        from one_context.cli import build_parser, _cmd_adapt

        parser = build_parser()
        args = parser.parse_args([
            "--root", str(adapter_root), "adapt", "dev", "--check", "--dry-run",
        ])
        assert _cmd_adapt(adapter_root, args) == 2


# ---------------------------------------------------------------------------
# Dirty detection tests
# ---------------------------------------------------------------------------

class TestDirtyDetection:
    def test_dirty_warning_printed(self, adapter_root, capsys):
        from one_context.cli import build_parser, _cmd_adapt

        parser = build_parser()
        args = parser.parse_args(["--root", str(adapter_root), "adapt", "dev"])
        _cmd_adapt(adapter_root, args)
        # Tamper
        (adapter_root / ".claude" / "adapters" / "onecxt-dev.md").write_text(
            "tampered", encoding="utf-8",
        )
        # Re-run adapt (normal mode)
        _cmd_adapt(adapter_root, args)
        captured = capsys.readouterr()
        assert "dirty" in captured.out.lower()
