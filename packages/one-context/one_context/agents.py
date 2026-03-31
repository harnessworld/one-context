"""Load and validate meta/agents.yaml."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from one_context.errors import ManifestError


def load_agents(root: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """
    Parse meta/agents.yaml if present.

    Returns ([], {}) when the file is missing.
    """
    path = root / "meta" / "agents.yaml"
    if not path.is_file():
        return [], {}

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ManifestError("agents.yaml root must be a mapping")

    raw_list = data.get("agents")
    if raw_list is None:
        return [], {}
    if not isinstance(raw_list, list):
        raise ManifestError("agents.yaml must contain an 'agents' list")

    agents: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}

    for i, item in enumerate(raw_list):
        if not isinstance(item, dict):
            raise ManifestError(f"agents[{i}] must be a mapping")

        aid = item.get("id")
        if not aid or not isinstance(aid, str) or not aid.strip():
            raise ManifestError(f"agents[{i}] needs a non-empty string 'id'")
        aid = aid.strip()

        lk = aid.casefold()
        if lk in by_id:
            raise ManifestError(f"Duplicate agent id (case-insensitive): {aid!r}")

        agents.append(item)
        by_id[lk] = item

    return agents, by_id


def resolve_agent_knowledge(root: Path, agent: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Resolve the ``knowledge`` paths for an agent.

    Returns the same structure as ``context._collect_knowledge_entries`` so
    adapter helpers can reuse the same inlining / @-reference logic.
    """
    raw_paths = agent.get("knowledge") or []
    out: list[dict[str, Any]] = []
    for item in raw_paths:
        if not isinstance(item, str) or not item.strip():
            continue
        rel = Path(item.strip())
        target = (root / rel).resolve()
        if target.is_dir():
            target_type = "directory"
        elif target.is_file():
            target_type = "file"
        else:
            target_type = "missing"
        out.append(
            {
                "path": rel.as_posix(),
                "absolute_path": str(target),
                "exists": target.exists(),
                "type": target_type,
            }
        )
    return out
