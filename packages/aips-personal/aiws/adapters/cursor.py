"""Cursor adapter — generates ``.cursor/rules/aiws-{id}.mdc`` files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aiws.adapters import AdapterBase, GeneratedFile, register
from aiws.adapters._rules import FieldRule, match_rules, render_rules_by_section


PROFILE_RULES: list[FieldRule] = [
    # -- behavior --
    FieldRule(
        "behavior.plan_first", True,
        "Always create a plan before making changes. Ask for approval first.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.plan_first", False,
        "You may edit code directly without a formal plan.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.safety_level", "conservative",
        "Be conservative: prefer minimal, reversible changes.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.safety_level", "standard",
        "Follow standard safety practices.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.change_scope", "broad",
        "Changes may span multiple files — consider cross-cutting concerns.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.change_scope", "focused",
        "Keep changes focused on the immediate task.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.test_expectation", "targeted",
        "Write targeted tests for changes.",
        section="Behavior",
    ),
    FieldRule(
        "behavior.test_expectation", "advisory",
        "Suggest testing strategies when appropriate.",
        section="Behavior",
    ),
    # -- output_style --
    FieldRule(
        "output_style.tone", "concise",
        "Be concise.",
        section="Output Style",
    ),
    FieldRule(
        "output_style.tone", "structured",
        "Use structured output with clear headings.",
        section="Output Style",
    ),
    FieldRule(
        "output_style.include_verification", True,
        "Include verification steps after changes.",
        section="Output Style",
    ),
    FieldRule(
        "output_style.include_verification", False,
        "Focus on design and rationale over verification.",
        section="Output Style",
    ),
]


def _build_mdc_frontmatter(workspace: dict[str, Any]) -> str:
    """Build the MDC YAML frontmatter block."""
    ws_id = workspace.get("id", "unknown")
    lines = [
        "---",
        f"description: aips-personal rules for workspace {ws_id}",
        "globs:",
        "alwaysApply: true",
        "---",
    ]
    return "\n".join(lines)


def _inline_knowledge(root: Path, knowledge: list[dict[str, Any]]) -> str:
    """Read and inline knowledge files (Cursor doesn't support @file refs)."""
    sections: list[str] = []
    for entry in knowledge:
        if not entry.get("exists"):
            continue
        abs_path = Path(entry["absolute_path"])
        rel_path = entry["path"]
        if abs_path.is_file():
            content = abs_path.read_text(encoding="utf-8").rstrip()
            sections.append(f"<!-- source: {rel_path} -->")
            sections.append(content)
        elif abs_path.is_dir():
            for child in sorted(abs_path.rglob("*.md")):
                child_rel = child.relative_to(root).as_posix()
                content = child.read_text(encoding="utf-8").rstrip()
                sections.append(f"<!-- source: {child_rel} -->")
                sections.append(content)
    return "\n\n".join(sections)


@register("cursor")
class CursorAdapter(AdapterBase):
    """Generate ``.cursor/rules/aiws-{id}.mdc`` for Cursor."""

    supports_file_ref = False

    def generate(
        self,
        root: Path,
        workspace: dict[str, Any],
        context: dict[str, Any],
    ) -> list[GeneratedFile]:
        ws_id = workspace.get("id", "unknown")
        parts: list[str] = [_build_mdc_frontmatter(workspace), ""]

        # Workspace summary
        ws_ctx = workspace.get("context") or {}
        summary = ws_ctx.get("summary", "")
        if summary:
            parts.append(f"# Workspace: {ws_id}")
            parts.append("")
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
                parts.append(render_rules_by_section(matched, heading_level=3))

        # Knowledge — inline content
        knowledge = context.get("knowledge") or []
        inlined = _inline_knowledge(root, knowledge)
        if inlined:
            parts.append("## Project Knowledge")
            parts.append("")
            parts.append(inlined)
            parts.append("")

        content = "\n".join(parts)
        return [
            GeneratedFile(
                rel_path=f".cursor/rules/aiws-{ws_id}.mdc",
                content=content,
                description=f"Cursor rules for workspace {ws_id}",
            ),
        ]
