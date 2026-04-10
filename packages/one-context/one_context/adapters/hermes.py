"""Hermes adapter — generates ``.hermes.md`` for Hermes Agent CLI.

Hermes discovers project context by priority (first found wins):
  1. .hermes.md / HERMES.md  (walk to git root)  ← we use this
  2. AGENTS.md / agents.md   (cwd only)
  3. CLAUDE.md / claude.md   (cwd only)
  4. .cursorrules

Because Hermes only loads ONE project context type, all workspace rules,
profile rules, knowledge, and agent definitions must be collected into
a single ``.hermes.md`` file so that everything is automatically available
with zero manual steps.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from one_context.adapters import AdapterBase, GeneratedFile, register
from one_context.adapters._rules import (
    FieldRule,
    collect_top_rules,
    match_rules,
    render_rules_by_section,
    resolve_rule_placement,
    resolve_rule_output,
)
from one_context.adapters._shared_rules import GENERATED_HEADER_MD, PROFILE_RULES
from one_context.agents import resolve_agent_knowledge

_ADAPTER_NAME = "hermes"


def _inline_knowledge_text(root: Path, knowledge: list[dict[str, Any]]) -> list[tuple[str, str]]:
    """Read knowledge files and return (source, content) pairs."""
    entries: list[tuple[str, str]] = []
    for item in knowledge:
        if not item.get("exists"):
            continue
        abs_path = Path(item["absolute_path"])
        if abs_path.is_file():
            content = abs_path.read_text(encoding="utf-8").rstrip()
            entries.append((item["path"], content))
        elif abs_path.is_dir():
            for child in sorted(abs_path.rglob("*.md")):
                child_rel = child.relative_to(root).as_posix()
                content = child.read_text(encoding="utf-8").rstrip()
                entries.append((child_rel, content))
    return entries


def _inline_rules(
    matched: list[FieldRule],
    adapter_name: str,
    heading_level: int = 2,
) -> str:
    """Render rules that are NOT top-placement (i.e. inline only)."""
    inline = [r for r in matched if resolve_rule_placement(r, adapter_name) != "top"]
    return render_rules_by_section(inline, heading_level=heading_level, adapter_name=adapter_name)


@register("hermes")
class HermesAdapter(AdapterBase):
    """Generate ``.hermes.md`` for Hermes Agent CLI.

    All context is collected into a single ``.hermes.md`` because Hermes
    uses first-match-wins and only loads one project context file.
    """

    supports_file_ref = False

    def __init__(self) -> None:
        self._top_rules: list[str] = []
        self._workspace_contents: list[str] = []
        self._agent_contents: list[str] = []

    def generate(
        self,
        root: Path,
        workspace: dict[str, Any],
        context: dict[str, Any],
    ) -> list[GeneratedFile]:
        ws_id = workspace.get("id", "unknown")
        parts: list[str] = [
            GENERATED_HEADER_MD,
            "",
            f"# one-context — workspace `{ws_id}`",
            "",
        ]

        # Workspace summary
        ws_ctx = workspace.get("context") or {}
        summary = ws_ctx.get("summary", "")
        if summary:
            parts.append(summary)
            parts.append("")

        focus = ws_ctx.get("focus") or []
        if focus:
            parts.append("## Focus Areas")
            parts.append("")
            for item in focus:
                parts.append(f"- {item}")
            parts.append("")

        # Profile rules — inline only; top-placement rules collected separately
        for profile in context.get("profiles") or []:
            matched = match_rules(profile, PROFILE_RULES)
            self._top_rules.extend(collect_top_rules(matched, _ADAPTER_NAME))
            inline_text = _inline_rules(matched, _ADAPTER_NAME, heading_level=3)
            if inline_text.strip():
                pname = profile.get("name", profile.get("id", ""))
                parts.append(f"## Profile: {pname}")
                parts.append("")
                desc = profile.get("description", "")
                if desc:
                    parts.append(f"_{desc}_")
                    parts.append("")
                parts.append(inline_text)

        # Knowledge — inline (Hermes does not support @file references)
        knowledge = context.get("knowledge") or []
        knowledge_entries = _inline_knowledge_text(root, knowledge)
        if knowledge_entries:
            parts.append("## Knowledge")
            parts.append("")
            for source, content in knowledge_entries:
                parts.append(f"<!-- source: {source} -->")
                parts.append(content)
                parts.append("")

        content = "\n".join(parts)
        self._workspace_contents.append(content)

        return [
            GeneratedFile(
                rel_path=f".hermes/onecxt-{ws_id}.md",
                content=content,
                description=f"Hermes context for workspace {ws_id}",
            ),
        ]

    def generate_agents(
        self,
        root: Path,
        agents: list,
        profiles_by_id: dict,
    ) -> list[GeneratedFile]:
        """Generate ``.hermes/agents/{id}.md`` for each agent."""
        files: list[GeneratedFile] = []

        for agent in agents:
            agent_id = agent.get("id", "unknown")
            name = agent.get("name", agent_id)
            description = agent.get("description", "")
            instructions = (agent.get("instructions") or "").strip()
            owns: list[str] = agent.get("owns") or []
            profile_id: str | None = agent.get("profile")

            parts: list[str] = [GENERATED_HEADER_MD, "", f"# {name}", ""]
            if description:
                parts.append(f"_{description}_")
                parts.append("")

            if instructions:
                parts.append(instructions)
                parts.append("")

            if owns:
                parts.append("## Artifact Ownership")
                parts.append("")
                parts.append("This agent creates and maintains:")
                for p in owns:
                    parts.append(f"- `{p}`")
                parts.append("")

            worktree = agent.get("worktree")
            if worktree:
                parts.append("## Worktree Convention")
                parts.append("")
                parts.append(f"- Branch: `{worktree.get('branch_pattern', '')}`")
                parts.append(f"- Path: `{worktree.get('path_pattern', '')}`")
                parts.append(f"- Base branch: `{worktree.get('base_branch', 'main')}`")
                parts.append("")

            deploy_manifest = agent.get("deploy_manifest")
            if deploy_manifest:
                parts.append("## Deploy Manifest")
                parts.append("")
                parts.append(f"Look for `{deploy_manifest}` in each repo root before deploying.")
                parts.append("")

            if profile_id:
                profile = profiles_by_id.get(profile_id.casefold())
                if profile:
                    matched = match_rules(profile, PROFILE_RULES)
                    self._top_rules.extend(collect_top_rules(matched, _ADAPTER_NAME))
                    inline_text = _inline_rules(matched, _ADAPTER_NAME, heading_level=3)
                    if inline_text.strip():
                        pname = profile.get("name", profile.get("id", ""))
                        parts.append(f"## Profile: {pname}")
                        parts.append("")
                        parts.append(inline_text)

            knowledge = resolve_agent_knowledge(root, agent)
            knowledge_entries = _inline_knowledge_text(root, knowledge)
            if knowledge_entries:
                parts.append("## Knowledge")
                parts.append("")
                for source, content in knowledge_entries:
                    parts.append(f"<!-- source: {source} -->")
                    parts.append(content)
                    parts.append("")

            agent_content = "\n".join(parts)
            self._agent_contents.append(agent_content)

            files.append(
                GeneratedFile(
                    rel_path=f".hermes/agents/{agent_id}.md",
                    content=agent_content,
                    description=f"Hermes agent config for {agent_id}",
                )
            )

        return files

    def generate_project_artifacts(
        self,
        root: Path,
        workspace_ids: list[str],
        agents: list[dict[str, Any]],
    ) -> list[GeneratedFile]:
        """Generate project-root ``.hermes.md`` that aggregates everything.

        Hermes auto-discovers ``.hermes.md`` (walk to git root) and only
        loads ONE project context file.  Therefore we merge all workspace
        and agent content into a single file so nothing is missed.
        """
        del root  # paths are repo-relative

        # Deduplicate top rules while preserving order
        seen: set[str] = set()
        unique_top: list[str] = []
        for rule_text in self._top_rules:
            if rule_text not in seen:
                seen.add(rule_text)
                unique_top.append(rule_text)

        # Top-placement hard rules at the very top
        top_block = ""
        if unique_top:
            top_block = "\n".join(unique_top) + "\n\n"

        # Assemble the single .hermes.md
        body_parts: list[str] = [
            GENERATED_HEADER_MD,
            "",
            "# one-context — Hermes",
            "",
            "This file is **generated by** `onecxt adapt`. Do not edit by hand.",
            "",
        ]

        # Workspace sections
        for ws_content in self._workspace_contents:
            # Strip the generated header and top-level heading from sub-files
            # since we already have our own above
            lines = ws_content.split("\n")
            filtered = []
            skip_header = True
            for line in lines:
                if skip_header:
                    # Skip everything up to and including the first "# one-context" heading
                    if line.startswith("# one-context"):
                        skip_header = False
                    continue
                filtered.append(line)
            body_parts.extend(filtered)
            body_parts.append("")

        # Agent sections (inline all agent content)
        for agent_content in self._agent_contents:
            lines = agent_content.split("\n")
            filtered = []
            skip_header = True
            for line in lines:
                if skip_header:
                    if line.startswith("# ") and not line.startswith("# one-context"):
                        skip_header = False
                    else:
                        continue
                filtered.append(line)
            body_parts.extend(filtered)
            body_parts.append("")

        content = top_block + "\n".join(body_parts).rstrip() + "\n"

        files: list[GeneratedFile] = [
            GeneratedFile(
                rel_path=".hermes.md",
                content=content,
                description="Hermes project context (auto-discovered)",
            ),
        ]

        # Reset cached state after generating artifacts
        self._top_rules = []
        self._workspace_contents = []
        self._agent_contents = []

        return files