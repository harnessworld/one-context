"""Cursor adapter — generates ``.cursor/rules/onecxt-{id}.mdc`` files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from one_context.adapters import AdapterBase, GeneratedFile, register
from one_context.adapters._rules import (
    AdapterOverride,
    FieldRule,
    collect_top_rules,
    match_rules,
    render_rules_by_section,
    resolve_rule_placement,
)
from one_context.agents import resolve_agent_knowledge

_ADAPTER_NAME = "cursor"


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
        "output_style.tone", "minimal",
        "Default to minimal output (文言极简 / caveman-style): modern language, "
        "shortest useful phrasing, no filler or pleasantries, do not restate the "
        "user's question—lead with the answer. Unless the user explicitly requests "
        "a different style, length, format, or language, keep replies short.",
        section="Output Style",
        adapter_overrides={
            _ADAPTER_NAME: AdapterOverride(
                output="Respond in ≤2 lines maximum. No pleasantries. "
                "No restating user input. Lead with the answer.",
                placement="top",
            ),
        },
    ),
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
        f"description: one-context rules for workspace {ws_id}",
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
    """Generate ``.cursor/rules/onecxt-{id}.mdc`` for Cursor."""

    supports_file_ref = False

    def __init__(self) -> None:
        self._top_rules: list[str] = []

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

        # Profile rules — inline only; top-placement rules are collected separately
        for profile in context.get("profiles") or []:
            matched = match_rules(profile, PROFILE_RULES)
            self._top_rules.extend(collect_top_rules(matched, _ADAPTER_NAME))
            # Render only inline rules
            inline = [r for r in matched if resolve_rule_placement(r, _ADAPTER_NAME) != "top"]
            if inline:
                pname = profile.get("name", profile.get("id", ""))
                parts.append(f"## Profile: {pname}")
                parts.append("")
                parts.append(render_rules_by_section(inline, heading_level=3, adapter_name=_ADAPTER_NAME))

        # Knowledge — inline content
        knowledge = context.get("knowledge") or []
        inlined = _inline_knowledge(root, knowledge)
        if inlined:
            parts.append("## Project Knowledge")
            parts.append("")
            parts.append(inlined)
            parts.append("")

        files: list[GeneratedFile] = [
            GeneratedFile(
                rel_path=f".cursor/rules/onecxt-{ws_id}.mdc",
                content="\n".join(parts),
                description=f"Cursor rules for workspace {ws_id}",
            ),
        ]

        return files

    def generate_agents(
        self,
        root: Path,
        agents: list,
        profiles_by_id: dict,
    ) -> list[GeneratedFile]:
        """Generate ``.cursor/rules/agent-{id}.mdc`` for each agent.

        Each file uses ``alwaysApply: false`` with globs derived from the
        agent's ``owns`` patterns, so Cursor auto-activates the right agent
        when the user opens a matching file — no manual @ references needed.
        """
        files: list[GeneratedFile] = []

        for agent in agents:
            agent_id = agent.get("id", "unknown")
            name = agent.get("name", agent_id)
            description = agent.get("description", "")
            instructions = (agent.get("instructions") or "").strip()
            owns: list[str] = agent.get("owns") or []
            profile_id: str | None = agent.get("profile")

            # Frontmatter — globs come from owns so Cursor activates contextually
            fm_lines = [
                "---",
                f"description: \"{name}\" — {description}",
            ]
            if owns:
                fm_lines.append("globs:")
                for p in owns:
                    fm_lines.append(f"  - \"{p}\"")
            fm_lines.append("alwaysApply: false")
            fm_lines.append("---")

            parts: list[str] = ["\n".join(fm_lines), "", f"# {name}", ""]

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
                    inline = [r for r in matched if resolve_rule_placement(r, _ADAPTER_NAME) != "top"]
                    if inline:
                        pname = profile.get("name", profile.get("id", ""))
                        parts.append(f"## Profile: {pname}")
                        parts.append("")
                        parts.append(render_rules_by_section(inline, heading_level=3, adapter_name=_ADAPTER_NAME))

            knowledge = resolve_agent_knowledge(root, agent)
            inlined = _inline_knowledge(root, knowledge)
            if inlined:
                parts.append("## Knowledge")
                parts.append("")
                parts.append(inlined)
                parts.append("")

            files.append(
                GeneratedFile(
                    rel_path=f".cursor/rules/agent-{agent_id}.mdc",
                    content="\n".join(parts),
                    description=f"Cursor rules for agent {agent_id}",
                )
            )

        # Emit hard-rules file after all agents are processed
        # (top rules may also come from generate(), so always check)
        seen: set[str] = set()
        unique_top: list[str] = []
        for rule_text in self._top_rules:
            if rule_text not in seen:
                seen.add(rule_text)
                unique_top.append(rule_text)

        if unique_top:
            hard_content = (
                "---\n"
                "description: Hard rules (top-priority)\n"
                "globs:\n"
                "alwaysApply: true\n"
                "---\n\n"
                + "\n".join(unique_top)
                + "\n"
            )
            files.append(
                GeneratedFile(
                    rel_path=".cursor/rules/onecxt-hard-rules.mdc",
                    content=hard_content,
                    description="Hard rules for Cursor (top-priority, alwaysApply)",
                )
            )
            self._top_rules = []

        return files
