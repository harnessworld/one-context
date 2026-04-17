"""Claude Code adapter — generates ``.claude/adapters/`` and root ``CLAUDE.md``."""

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
from one_context.skills import SkillMeta

_ADAPTER_NAME = "claude_code"


def _inline_rules(
    matched: list[FieldRule],
    adapter_name: str,
    heading_level: int = 2,
) -> str:
    """Render rules that are NOT top-placement (i.e. inline only)."""
    inline = [r for r in matched if resolve_rule_placement(r, adapter_name) != "top"]
    return render_rules_by_section(inline, heading_level=heading_level, adapter_name=adapter_name)


@register("claude_code")
class ClaudeCodeAdapter(AdapterBase):
    """Generate per-workspace adapter files and project-root ``CLAUDE.md``."""

    supports_file_ref = True

    def __init__(self) -> None:
        self._top_rules: list[str] = []
        self._skills: list[SkillMeta] = []

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

        # Profile rules — inline only; top-placement rules are collected separately
        for profile in context.get("profiles") or []:
            matched = match_rules(profile, PROFILE_RULES)
            # Collect top-placement rules across all profiles
            self._top_rules.extend(collect_top_rules(matched, _ADAPTER_NAME))
            # Render only inline rules
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

        # Knowledge — use @file references (Claude Code supports this)
        knowledge = context.get("knowledge") or []
        existing = [k for k in knowledge if k.get("exists")]
        if existing:
            parts.append("## Knowledge")
            parts.append("")
            parts.append("Read these files for project context:")
            parts.append("")
            for entry in existing:
                parts.append(f"@{entry['path']}")
            parts.append("")

        content = "\n".join(parts)
        return [
            GeneratedFile(
                rel_path=f".claude/adapters/onecxt-{ws_id}.md",
                content=content,
                description=f"Claude Code instructions for workspace {ws_id}",
            ),
        ]

    def generate_agents(
        self,
        root: Path,
        agents: list,
        profiles_by_id: dict,
    ) -> list[GeneratedFile]:
        """Generate ``.claude/agents/{id}.md`` for each agent.

        Claude Code follows ``@file`` references at runtime.  Root
        ``CLAUDE.md`` (from ``generate_project_artifacts``) pulls in these
        files so users need not maintain ``@`` lines by hand.
        """
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
                    # Collect top-placement rules from agent profiles too
                    self._top_rules.extend(collect_top_rules(matched, _ADAPTER_NAME))
                    inline_text = _inline_rules(matched, _ADAPTER_NAME, heading_level=3)
                    if inline_text.strip():
                        pname = profile.get("name", profile.get("id", ""))
                        parts.append(f"## Profile: {pname}")
                        parts.append("")
                        parts.append(inline_text)

            knowledge = resolve_agent_knowledge(root, agent)
            existing = [k for k in knowledge if k.get("exists")]
            if existing:
                parts.append("## Knowledge")
                parts.append("")
                parts.append("Read these files for context:")
                parts.append("")
                for entry in existing:
                    if entry.get("type") == "directory":
                        dir_path = Path(entry["absolute_path"])
                        for child in sorted(dir_path.rglob("*.md")):
                            rel = child.relative_to(root).as_posix()
                            parts.append(f"@{rel}")
                    else:
                        parts.append(f"@{entry['path']}")
                parts.append("")

            files.append(
                GeneratedFile(
                    rel_path=f".claude/agents/{agent_id}.md",
                    content="\n".join(parts),
                    description=f"Claude Code agent config for {agent_id}",
                )
            )

        return files

    def generate_skills(
        self,
        root: Path,
        skills: list[SkillMeta],
    ) -> list[GeneratedFile]:
        """Generate ``.claude/skills/<name>.md`` with ``@`` refs to SKILL.md."""
        self._skills = list(skills)
        files: list[GeneratedFile] = []

        for skill in skills:
            content = "\n".join([
                GENERATED_HEADER_MD,
                "",
                f"# Skill: {skill.name}",
                "",
                f"@{skill.source_path}",
                "",
            ])
            files.append(GeneratedFile(
                rel_path=f".claude/skills/{skill.dir_name}.md",
                content=content,
                description=f"Claude Code skill registration for {skill.name}",
            ))

        return files

    def generate_project_artifacts(
        self,
        root: Path,
        workspace_ids: list[str],
        agents: list[dict[str, Any]],
    ) -> list[GeneratedFile]:
        """Generate root ``CLAUDE.md`` with ``@`` refs to adapters + agents."""
        del root  # paths are repo-relative for @-references

        # Deduplicate top rules while preserving order
        seen: set[str] = set()
        unique_top: list[str] = []
        for rule_text in self._top_rules:
            if rule_text not in seen:
                seen.add(rule_text)
                unique_top.append(rule_text)

        # Prepend top-placement rules as hard constraints at the very top
        top_block = ""
        hard_rules_ref = ""
        if unique_top:
            top_block = "\n".join(unique_top) + "\n\n"
            hard_rules_ref = "@.claude/adapters/onecxt-hard-rules.md\n"

        lines = [
            GENERATED_HEADER_MD,
            "",
            "# one-context — Claude Code",
            "",
            "This file is **generated by** `onecxt adapt`. Do not edit by hand — "
            "it is overwritten on the next run.",
            "",
            "To add personal instructions, put them in `knowledge/` or a separate "
            "markdown file and add that path to `meta/workspaces.yaml` "
            "(`context.knowledge`) for the relevant workspace, then re-run adapt.",
            "",
            "## Workspaces",
            "",
            "Per-workspace context (profiles, knowledge `@` list):",
            "",
        ]

        # Hard rules reference first
        if hard_rules_ref:
            lines.append(hard_rules_ref)

        for ws_id in workspace_ids:
            lines.append(f"@.claude/adapters/onecxt-{ws_id}.md")
            lines.append("")

        if agents:
            lines.extend(
                [
                    "## Agents",
                    "",
                    "Per-role context from `meta/agents.yaml` (each file expands "
                    "templates and playbooks via `@`):",
                    "",
                ]
            )
            for agent in sorted(agents, key=lambda a: str(a.get("id", ""))):
                aid = agent.get("id", "unknown")
                lines.append(f"@.claude/agents/{aid}.md")
                lines.append("")

        if self._skills:
            lines.extend(
                [
                    "## Skills",
                    "",
                    "Per-skill context (auto-discovered from `skills/`):",
                    "",
                ]
            )
            for skill in sorted(self._skills, key=lambda s: s.dir_name):
                lines.append(f"@.claude/skills/{skill.dir_name}.md")
                lines.append("")

        content = top_block + "\n".join(lines).rstrip() + "\n"

        files: list[GeneratedFile] = [
            GeneratedFile(
                rel_path="CLAUDE.md",
                content=content,
                description="Claude Code project root CLAUDE.md (generated)",
            ),
        ]

        # Generate the hard-rules standalone file for @-reference
        if unique_top:
            files.append(
                GeneratedFile(
                    rel_path=".claude/adapters/onecxt-hard-rules.md",
                    content=GENERATED_HEADER_MD + "\n\n" + "\n".join(unique_top) + "\n",
                    description="Hard rules (top-placement) for this project",
                )
            )

        # Reset cached top rules after generating artifacts
        self._top_rules = []
        self._skills = []

        return files
