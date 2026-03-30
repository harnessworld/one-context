"""Claude Code adapter — generates ``CLAUDE.md`` workspace instructions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aiws.adapters import AdapterBase, GeneratedFile, register
from aiws.adapters._rules import FieldRule, match_rules, render_rules_by_section


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
    """Generate ``CLAUDE.md`` for Claude Code."""

    supports_file_ref = True

    def generate(
        self,
        root: Path,
        workspace: dict[str, Any],
        context: dict[str, Any],
    ) -> list[GeneratedFile]:
        ws_id = workspace.get("id", "unknown")
        parts: list[str] = [
            f"# aips-personal — workspace `{ws_id}`",
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
                rel_path=f".claude/adapters/aiws-{ws_id}.md",
                content=content,
                description=f"Claude Code instructions for workspace {ws_id}",
            ),
        ]
