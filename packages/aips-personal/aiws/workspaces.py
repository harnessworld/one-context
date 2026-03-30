from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from aiws.errors import ManifestError


def load_workspaces(root: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """
    Parse meta/workspaces.yaml if present.

    Returns ([], {}) when the file is missing (optional in minimal setups).
    """
    path = root / "meta" / "workspaces.yaml"
    if not path.is_file():
        return [], {}

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ManifestError("workspaces.yaml root must be a mapping")

    raw_list = data.get("workspaces")
    if raw_list is None:
        return [], {}
    if not isinstance(raw_list, list):
        raise ManifestError("workspaces.yaml must contain a 'workspaces' list")

    workspaces: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}

    for i, item in enumerate(raw_list):
        if not isinstance(item, dict):
            raise ManifestError(f"workspaces[{i}] must be a mapping")

        wid = item.get("id")
        if not wid or not isinstance(wid, str) or not wid.strip():
            raise ManifestError(f"workspaces[{i}] needs a non-empty string 'id'")
        wid = wid.strip()

        lk = wid.casefold()
        if lk in by_id:
            raise ManifestError(f"Duplicate workspace id (case-insensitive): {wid!r}")

        workspaces.append(item)
        by_id[lk] = item

    return workspaces, by_id
