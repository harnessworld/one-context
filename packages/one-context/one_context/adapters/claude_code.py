"""Claude Code adapter — generates ``.claude/adapters/`` and root ``CLAUDE.md``."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from one_context.adapters import AdapterBase, GeneratedFile, register
from one_context.adapters._rules import FieldRule, match_rules, render_rules_by_section
from one_context.agents import resolve_agent_knowledge


PROFILE_RULES: list[FieldRule] = [
    # -- behavior --
    FieldRule(
        "behavior.plan_first", True,
        "Always create a plan and get approval before making changes.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.plan_first", False,
        "You may edit code directly without creating a formal plan first.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.safety_level", "conservative",
        "Take a conservative approach: prefer minimal, reversible changes. "
        "Review each change for unintended side effects.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.safety_level", "standard",
        "Follow standard safety practices when making changes.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.change_scope", "broad",
        "Consider cross-cutting concerns — changes may span multiple files and modules.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.change_scope", "focused",
        "Keep changes focused and scoped to the immediate task.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.test_expectation", "targeted",
        "Write targeted tests for the specific changes you make.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.test_expectation", "advisory",
        "Suggest testing strategies but do not require tests for every change.",
        section="Behavior",
    ),
    # -- output_style --
    FieldRule(
        "output_style.tone", "minimal",
        "Default to minimal output (文言极简 / caveman-style): modern language, "
        "shortest useful phrasing, no filler or pleasantries, do not restate the "
        "user's question—lead with the answer. Unless the user explicitly requests "
        "a different style, length, format, or language, keep replies short.",
        section="Output Style",
    ),
    FieldRule(
        "output_style.tone", "concise",
        "Keep responses concise and to the point.",
        section="Output Style",
    ),
    FieldRule(
        "output_style.tone", "structured",
        "Use structured output with clear headings and sections.",
        section="Output Style",
    ),
    FieldRule(
        "output_style.include_verification", True,
        "Include verification steps (e.g. test commands) after making changes.",
        section="Output Style",
    ),
    FieldRule(
        "output_style.include_verification", False,
        "Verification steps are optional — focus on the design and rationale.",
        section="Output Style",
    ),
]


@register("claude_code")
class ClaudeCodeAdapter(AdapterBase):
    """Generate per-workspace adapter files and project-root ``CLAUDE.md``."""

    supports_file_ref = True

    def generate(
        self,
        root: Path,
        workspace: dict[str, Any],
        context: dict[str, Any],
    ) -> list[GeneratedFile]:
        ws_id = workspace.get("id", "unknown")
        parts: list[str] = [
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

        # Profile rules
        for profile in context.get("profiles") or []:
            matched = match_rules(profile, PROFILE_RULES)
            if matched:
                pname = profile.get("name", profile.get("id", ""))
                parts.append(f"## Profile: {pname}")
                parts.append("")
                desc = profile.get("description", "")
                if desc:
                    parts.append(f"_{desc}_")
                    parts.append("")
                parts.append(render_rules_by_section(matched, heading_level=3))

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

            parts: list[str] = [f"# {name}", ""]
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
                    if matched:
                        pname = profile.get("name", profile.get("id", ""))
                        parts.append(f"## Profile: {pname}")
                        parts.append("")
                        parts.append(render_rules_by_section(matched, heading_level=3))

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

    def generate_project_artifacts(
        self,
        root: Path,
        workspace_ids: list[str],
        agents: list[dict[str, Any]],
    ) -> list[GeneratedFile]:
        """Generate root ``CLAUDE.md`` with ``@`` refs to adapters + agents."""
        del root  # paths are repo-relative for @-references
        lines = [
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

        content = "\n".join(lines).rstrip() + "\n"
        return [
            GeneratedFile(
                rel_path="CLAUDE.md",
                content=content,
                description="Claude Code project root CLAUDE.md (generated)",
            ),
        ]
