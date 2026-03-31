from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from one_context.errors import ManifestError


def load_profiles(root: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """
    Parse meta/profiles.yaml if present.

    Returns ([], {}) when the file is missing.
    """
    path = root / "meta" / "profiles.yaml"
    if not path.is_file():
        return [], {}

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ManifestError("profiles.yaml root must be a mapping")

    raw_list = data.get("profiles")
    if raw_list is None:
        return [], {}
    if not isinstance(raw_list, list):
        raise ManifestError("profiles.yaml must contain a 'profiles' list")

    profiles: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}

    for i, item in enumerate(raw_list):
        if not isinstance(item, dict):
            raise ManifestError(f"profiles[{i}] must be a mapping")

        pid = item.get("id")
        if not pid or not isinstance(pid, str) or not pid.strip():
            raise ManifestError(f"profiles[{i}] needs a non-empty string 'id'")
        pid = pid.strip()

        lk = pid.casefold()
        if lk in by_id:
            raise ManifestError(f"Duplicate profile id (case-insensitive): {pid!r}")

        profiles.append(item)
        by_id[lk] = item

    return profiles, by_id
