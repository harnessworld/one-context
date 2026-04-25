"""OpenClaw adapter — generates ``.openclaw/workspace-config.json``."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from one_context.adapters import AdapterBase, GeneratedFile, register
from one_context.adapters._rules import FieldRule, match_rules
from one_context.adapters._shared_rules import GENERATED_NOTICE_JSON, PROFILE_RULES
from one_context.agents import resolve_agent_knowledge
from one_context.skills import SkillMeta


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

    def __init__(self) -> None:
        self._skills: list[SkillMeta] = []

    def generate(
        self,
        root: Path,
        workspace: dict[str, Any],
        context: dict[str, Any],
    ) -> list[GeneratedFile]:
        ws_id = workspace.get("id", "unknown")
        ws_ctx = workspace.get("context") or {}

        config: dict[str, Any] = {
            "_generated": GENERATED_NOTICE_JSON,
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
                "_generated": GENERATED_NOTICE_JSON,
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

    def generate_skills(
        self,
        root: Path,
        skills: list[SkillMeta],
    ) -> list[GeneratedFile]:
        """Generate ``.openclaw/skills/<name>.json`` for each skill.

        The full SKILL.md body (stripped of frontmatter) is inlined as
        ``content`` so consumers do not need to read the source file.
        """
        from one_context.skills import strip_frontmatter

        self._skills = list(skills)
        files: list[GeneratedFile] = []

        for skill in skills:
            fm = skill.frontmatter

            # Read and inline the SKILL.md body
            skill_path = root / skill.source_path
            if skill_path.is_file():
                full_text = skill_path.read_text(encoding="utf-8")
                body = strip_frontmatter(full_text).strip()
            else:
                body = skill.body.strip() if skill.body else ""

            config: dict[str, Any] = {
                "_generated": GENERATED_NOTICE_JSON,
                "skill_id": skill.dir_name,
                "name": skill.name,
                "description": fm.get("description", ""),
                "source": skill.source_path,
                "trigger_phrases": fm.get("triggers", []),
                "content": body,
            }

            openclaw_meta = fm.get("openclaw")
            if openclaw_meta:
                config["openclaw"] = openclaw_meta

            if fm.get("type"):
                config["type"] = fm["type"]
            if fm.get("tags"):
                config["tags"] = fm["tags"]
            if fm.get("version"):
                config["version"] = fm["version"]
            if fm.get("author"):
                config["author"] = fm["author"]

            files.append(GeneratedFile(
                rel_path=f".openclaw/skills/{skill.dir_name}.json",
                content=json.dumps(config, indent=2, ensure_ascii=False) + "\n",
                description=f"OpenClaw skill config for {skill.name}",
            ))

        return files

    def generate_project_artifacts(
        self,
        root: Path,
        workspace_ids: list[str],
        agents: list[dict[str, Any]],
    ) -> list[GeneratedFile]:
        """Generate ``.openclaw/onecxt-project.json`` listing workspace + agent configs."""
        del root
        payload: dict[str, Any] = {
            "_generated": GENERATED_NOTICE_JSON,
            "one_context": {
                "version": 1,
                "description": (
                    "OpenClaw project manifest — generated by `onecxt adapt`. "
                    "Load the JSON files listed under `workspaces` and `agents`."
                ),
                "workspaces": [
                    {"id": wid, "path": f".openclaw/onecxt-{wid}.json"}
                    for wid in workspace_ids
                ],
                "agents": [
                    {
                        "id": a.get("id", ""),
                        "path": f".openclaw/agents/{a.get('id', '')}.json",
                    }
                    for a in sorted(agents, key=lambda x: str(x.get("id", "")))
                ],
                "skills": [
                    {"id": s.dir_name, "path": f".openclaw/skills/{s.dir_name}.json"}
                    for s in sorted(self._skills, key=lambda s: s.dir_name)
                ],
            }
        }
        content = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

        # Reset cached skills
        self._skills = []

        return [
            GeneratedFile(
                rel_path=".openclaw/onecxt-project.json",
                content=content,
                description="OpenClaw project manifest (workspace + agent + skill paths)",
            ),
        ]
