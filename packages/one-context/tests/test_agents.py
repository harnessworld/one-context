"""Tests for agents.yaml loading, validation, and CLI commands."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from one_context.agents import load_agents, resolve_agent_knowledge
from one_context.errors import ManifestError


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def agents_yaml_content() -> str:
    """Sample agents.yaml content."""
    return """
version: "1"

agents:
  - id: pm
    name: "PM Agent"
    role: pm
    profile: default
    description: "Create and manage feature specs"
    knowledge:
      - knowledge/playbooks/add-feature.md
    owns:
      - "features/**/spec.md"
    instructions: |
      You are the PM agent.

  - id: dev
    name: "Dev Agent"
    role: dev
    profile: coding
    description: "Implement features"
    worktree:
      branch_pattern: "feature/{feature_id}"
      path_pattern: "repos/{repo_id}/.worktrees/{feature_id}"
      base_branch: main
    instructions: |
      You are the Dev agent.
"""


@pytest.fixture
def minimal_agents_yaml() -> str:
    """Minimal valid agents.yaml."""
    return """
version: "1"
agents:
  - id: test-agent
    name: "Test Agent"
    role: dev
"""


# ---------------------------------------------------------------------------
# load_agents tests
# ---------------------------------------------------------------------------

def test_load_agents_missing_file(tmp_path: Path) -> None:
    """Returns ([], {}) when agents.yaml is missing."""
    agents, by_id = load_agents(tmp_path)
    assert agents == []
    assert by_id == {}


def test_load_agents_valid(tmp_path: Path, agents_yaml_content: str) -> None:
    """Loads a valid agents.yaml."""
    meta_dir = tmp_path / "meta"
    meta_dir.mkdir()
    (meta_dir / "agents.yaml").write_text(agents_yaml_content, encoding="utf-8")

    agents, by_id = load_agents(tmp_path)

    assert len(agents) == 2
    assert "pm" in by_id
    assert "dev" in by_id
    assert by_id["pm"]["role"] == "pm"
    assert by_id["dev"]["worktree"]["branch_pattern"] == "feature/{feature_id}"


def test_load_agents_case_insensitive_lookup(tmp_path: Path, minimal_agents_yaml: str) -> None:
    """Agent lookup keys are casefolded (lowercase)."""
    meta_dir = tmp_path / "meta"
    meta_dir.mkdir()
    (meta_dir / "agents.yaml").write_text(minimal_agents_yaml, encoding="utf-8")

    _, by_id = load_agents(tmp_path)

    # The lookup keys are casefolded, so only the lowercase version is stored
    assert "test-agent" in by_id
    # Verify case-insensitive lookup works via casefold()
    assert by_id.get("test-agent".casefold()) is not None
    assert by_id.get("TEST-AGENT".casefold()) is not None
    assert by_id.get("Test-Agent".casefold()) is not None


def test_load_agents_duplicate_id(tmp_path: Path) -> None:
    """Raises error for duplicate agent ids (case-insensitive)."""
    content = """
version: "1"
agents:
  - id: my-agent
    name: "First"
    role: dev
  - id: My-Agent
    name: "Second"
    role: qa
"""
    meta_dir = tmp_path / "meta"
    meta_dir.mkdir()
    (meta_dir / "agents.yaml").write_text(content, encoding="utf-8")

    with pytest.raises(ManifestError, match="Duplicate agent id"):
        load_agents(tmp_path)


def test_load_agents_missing_id(tmp_path: Path) -> None:
    """Raises error when agent is missing 'id'."""
    content = """
version: "1"
agents:
  - name: "No ID Agent"
    role: dev
"""
    meta_dir = tmp_path / "meta"
    meta_dir.mkdir()
    (meta_dir / "agents.yaml").write_text(content, encoding="utf-8")

    with pytest.raises(ManifestError, match="needs a non-empty string 'id'"):
        load_agents(tmp_path)


def test_load_agents_not_a_mapping(tmp_path: Path) -> None:
    """Raises error when agents entry is not a mapping."""
    content = """
version: "1"
agents:
  - "just a string"
"""
    meta_dir = tmp_path / "meta"
    meta_dir.mkdir()
    (meta_dir / "agents.yaml").write_text(content, encoding="utf-8")

    with pytest.raises(ManifestError, match="must be a mapping"):
        load_agents(tmp_path)


def test_load_agents_empty_file(tmp_path: Path) -> None:
    """Handles empty agents.yaml."""
    meta_dir = tmp_path / "meta"
    meta_dir.mkdir()
    (meta_dir / "agents.yaml").write_text("", encoding="utf-8")

    agents, by_id = load_agents(tmp_path)
    assert agents == []
    assert by_id == {}


def test_load_agents_empty_list(tmp_path: Path) -> None:
    """Handles agents.yaml with empty agents list."""
    content = """
version: "1"
agents: []
"""
    meta_dir = tmp_path / "meta"
    meta_dir.mkdir()
    (meta_dir / "agents.yaml").write_text(content, encoding="utf-8")

    agents, by_id = load_agents(tmp_path)
    assert agents == []
    assert by_id == {}


# ---------------------------------------------------------------------------
# resolve_agent_knowledge tests
# ---------------------------------------------------------------------------

def test_resolve_agent_knowledge_file(tmp_path: Path) -> None:
    """Resolves knowledge paths for files."""
    # Create a knowledge file
    knowledge_dir = tmp_path / "knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "test.md").write_text("# Test", encoding="utf-8")

    agent = {
        "id": "test",
        "knowledge": ["knowledge/test.md"],
    }

    result = resolve_agent_knowledge(tmp_path, agent)

    assert len(result) == 1
    assert result[0]["path"] == "knowledge/test.md"
    assert result[0]["exists"] is True
    assert result[0]["type"] == "file"


def test_resolve_agent_knowledge_directory(tmp_path: Path) -> None:
    """Resolves knowledge paths for directories."""
    knowledge_dir = tmp_path / "knowledge" / "standards"
    knowledge_dir.mkdir(parents=True)

    agent = {
        "id": "test",
        "knowledge": ["knowledge/standards/"],
    }

    result = resolve_agent_knowledge(tmp_path, agent)

    assert len(result) == 1
    assert result[0]["type"] == "directory"
    assert result[0]["exists"] is True


def test_resolve_agent_knowledge_missing(tmp_path: Path) -> None:
    """Handles missing knowledge paths."""
    agent = {
        "id": "test",
        "knowledge": ["knowledge/nonexistent.md"],
    }

    result = resolve_agent_knowledge(tmp_path, agent)

    assert len(result) == 1
    assert result[0]["exists"] is False
    assert result[0]["type"] == "missing"


def test_resolve_agent_knowledge_empty(tmp_path: Path) -> None:
    """Handles agent without knowledge field."""
    agent = {"id": "test"}

    result = resolve_agent_knowledge(tmp_path, agent)

    assert result == []


# ---------------------------------------------------------------------------
# CLI agent list tests
# ---------------------------------------------------------------------------

def test_cli_agent_list_empty(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """agent list returns empty message when no agents."""
    from one_context.cli import build_parser

    meta_dir = tmp_path / "meta"
    meta_dir.mkdir()

    # Create minimal repos.yaml so root detection works
    (meta_dir / "repos.yaml").write_text("repos: []", encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args(["--root", str(tmp_path), "agent", "list"])
    exit_code = args.func(tmp_path, args)

    assert exit_code == 0
    captured = capsys.readouterr()
    assert "no agents" in captured.out


def test_cli_agent_list(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """agent list outputs agents in TSV format."""
    from one_context.cli import build_parser

    meta_dir = tmp_path / "meta"
    meta_dir.mkdir()

    (meta_dir / "repos.yaml").write_text("repos: []", encoding="utf-8")
    (meta_dir / "agents.yaml").write_text(
        """
version: "1"
agents:
  - id: pm
    name: "PM Agent"
    role: pm
  - id: dev
    name: "Dev Agent"
    role: dev
""",
        encoding="utf-8",
    )

    parser = build_parser()
    args = parser.parse_args(["--root", str(tmp_path), "agent", "list"])
    exit_code = args.func(tmp_path, args)

    assert exit_code == 0
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == 2
    assert "pm" in lines[0]
    assert "dev" in lines[1]


# ---------------------------------------------------------------------------
# CLI agent show tests
# ---------------------------------------------------------------------------

def test_cli_agent_show(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """agent show outputs agent as JSON."""
    from one_context.cli import build_parser

    meta_dir = tmp_path / "meta"
    meta_dir.mkdir()

    (meta_dir / "repos.yaml").write_text("repos: []", encoding="utf-8")
    (meta_dir / "agents.yaml").write_text(
        """
version: "1"
agents:
  - id: pm
    name: "PM Agent"
    role: pm
    description: "Test description"
""",
        encoding="utf-8",
    )

    parser = build_parser()
    args = parser.parse_args(["--root", str(tmp_path), "agent", "show", "pm"])
    exit_code = args.func(tmp_path, args)

    assert exit_code == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["id"] == "pm"
    assert data["name"] == "PM Agent"
    assert data["role"] == "pm"


def test_cli_agent_show_not_found(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """agent show returns error for unknown agent."""
    from one_context.cli import build_parser

    meta_dir = tmp_path / "meta"
    meta_dir.mkdir()

    (meta_dir / "repos.yaml").write_text("repos: []", encoding="utf-8")
    (meta_dir / "agents.yaml").write_text(
        """
version: "1"
agents:
  - id: pm
    name: "PM Agent"
    role: pm
""",
        encoding="utf-8",
    )

    parser = build_parser()
    args = parser.parse_args(["--root", str(tmp_path), "agent", "show", "nonexistent"])
    exit_code = args.func(tmp_path, args)

    assert exit_code == 2
    captured = capsys.readouterr()
    assert "unknown agent id" in captured.err


def test_cli_agent_show_case_insensitive(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """agent show is case-insensitive."""
    from one_context.cli import build_parser

    meta_dir = tmp_path / "meta"
    meta_dir.mkdir()

    (meta_dir / "repos.yaml").write_text("repos: []", encoding="utf-8")
    (meta_dir / "agents.yaml").write_text(
        """
version: "1"
agents:
  - id: my-agent
    name: "My Agent"
    role: dev
""",
        encoding="utf-8",
    )

    parser = build_parser()
    args = parser.parse_args(["--root", str(tmp_path), "agent", "show", "MY-AGENT"])
    exit_code = args.func(tmp_path, args)

    assert exit_code == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["id"] == "my-agent"