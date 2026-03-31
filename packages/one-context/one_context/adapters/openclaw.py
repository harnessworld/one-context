"""OpenClaw adapter — generates ``.openclaw/workspace-config.json``."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from one_context.adapters import AdapterBase, GeneratedFile, register
from one_context.adapters._rules import FieldRule, match_rules
from one_context.agents import resolve_agent_knowledge


PROFILE_RULES: list[FieldRule] = [
    # -- behavior --
    FieldRule("behavior.plan_first", True, "Always create a plan before making changes.", section="behavior"),
    FieldRule("behavior.plan_first", False, "Edit code directly without a formal plan.", section="behavior"),
    FieldRule("behavior.safety_level", "conservative", "Prefer minimal, reversible changes.", section="behavior"),
    FieldRule("behavior.safety_level", "standard", "Follow standard safety practices.", section="behavior"),
    FieldRule("behavior.change_scope", "broad", "Consider cross-cutting concerns across files.", section="behavior"),
    FieldRule("behavior.change_scope", "focused", "Keep changes focused on the immediate task.", section="behavior"),
    FieldRule("behavior.test_expectation", "targeted", "Write targeted tests for changes.", section="behavior"),
    FieldRule("behavior.test_expectation", "advisory", "Suggest testing strategies when appropriate.", section="behavior"),
    # -- output_style --
    FieldRule("output_style.tone", "concise", "Be concise.", section="output_style"),
    FieldRule("output_style.tone", "structured", "Use structured output.", section="output_style"),
    FieldRule("output_style.include_verification", True, "Include verification steps.", section="output_style"),
    FieldRule("output_style.include_verification", False, "Focus on design over verification.", section="output_style"),
]


def _collect_instructions(profiles: list[dict[str, Any]]) -> list[str]:
    """Collect all matching rule outputs across profiles."""
    instructions: list[str] = []
    for profile in profiles:
        matched = match_rules(profile, PROFILE_RULES)
        for rule in matched:
            instructions.append(rule.output)
    return instructions


def _inline_knowledge_text(root: Path, knowledge: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Read knowledge files and return as structured entries."""
    entries: list[dict[str, str]] = []
    for item in knowledge:
        if not item.get("exists"):
            continue
        abs_path = Path(item["absolute_path"])
        if abs_path.is_file():
            content = abs_path.read_text(encoding="utf-8").rstrip()
            entries.append({"source": item["path"], "content": content})
        elif abs_path.is_dir():
            for child in sorted(abs_path.rglob("*.md")):
                child_rel = child.relative_to(root).as_posix()
                content = child.read_text(encoding="utf-8").rstrip()
                entries.append({"source": child_rel, "content": content})
    return entries


@register("openclaw")
class OpenClawAdapter(AdapterBase):
    """Generate ``.openclaw/workspace-config.json`` for OpenClaw."""

    supports_file_ref = False

    def generate(
        self,
        root: Path,
        workspace: dict[str, Any],
        context: dict[str, Any],
    ) -> list[GeneratedFile]:
        ws_id = workspace.get("id", "unknown")
        ws_ctx = workspace.get("context") or {}

        config: dict[str, Any] = {
            "workspace_id": ws_id,
            "name": workspace.get("name", ""),
            "description": workspace.get("description", ""),
        }

        # Context / focus
        if ws_ctx.get("summary"):
            config["summary"] = ws_ctx["summary"]
        if ws_ctx.get("focus"):
            config["focus"] = ws_ctx["focus"]

        # Profile instructions
        profiles = context.get("profiles") or []
        instructions = _collect_instructions(profiles)
        if instructions:
            config["instructions"] = instructions

        # Profile metadata
        if profiles:
            config["profiles"] = [
                {
                    "id": p.get("id", ""),
                    "name": p.get("name", ""),
                    "mode": p.get("mode", ""),
                }
                for p in profiles
            ]

        # Knowledge — inline
        knowledge = context.get("knowledge") or []
        knowledge_entries = _inline_knowledge_text(root, knowledge)
        if knowledge_entries:
            config["knowledge"] = knowledge_entries

        content = json.dumps(config, indent=2, ensure_ascii=False) + "\n"
        return [
            GeneratedFile(
                rel_path=f".openclaw/onecxt-{ws_id}.json",
                content=content,
                description=f"OpenClaw config for workspace {ws_id}",
            ),
        ]

    def generate_agents(
        self,
        root: Path,
        agents: list,
        profiles_by_id: dict,
    ) -> list[GeneratedFile]:
        """Generate ``.openclaw/agents/{id}.json`` for each agent."""
        files: list[GeneratedFile] = []

        for agent in agents:
            agent_id = agent.get("id", "unknown")
            name = agent.get("name", agent_id)
            description = agent.get("description", "")
            instructions = (agent.get("instructions") or "").strip()
            owns: list[str] = agent.get("owns") or []
            profile_id: str | None = agent.get("profile")

            config: dict[str, Any] = {
                "agent_id": agent_id,
                "name": name,
                "role": agent.get("role", ""),
                "description": description,
            }

            if instructions:
                config["instructions"] = instructions

            if owns:
                config["owns"] = owns

            worktree = agent.get("worktree")
            if worktree:
                config["worktree"] = worktree

            deploy_manifest = agent.get("deploy_manifest")
            if deploy_manifest:
                config["deploy_manifest"] = deploy_manifest

            if profile_id:
                profile = profiles_by_id.get(profile_id.casefold())
                if profile:
                    matched = match_rules(profile, PROFILE_RULES)
                    if matched:
                        config["behavior_rules"] = [r.output for r in matched]

            knowledge = resolve_agent_knowledge(root, agent)
            knowledge_entries = _inline_knowledge_text(root, knowledge)
            if knowledge_entries:
                config["knowledge"] = knowledge_entries

            files.append(
                GeneratedFile(
                    rel_path=f".openclaw/agents/{agent_id}.json",
                    content=json.dumps(config, indent=2, ensure_ascii=False) + "\n",
                    description=f"OpenClaw agent config for {agent_id}",
                )
            )

        return files
