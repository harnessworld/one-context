from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml

from one_context.errors import ManifestError


# ---------------------------------------------------------------------------
# Deep merge utility
# ---------------------------------------------------------------------------

def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge *override* into a copy of *base*.

    - dict values are merged recursively.
    - All other types (lists, scalars) are replaced wholesale.
    """
    result = copy.deepcopy(base)
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = copy.deepcopy(val)
    return result


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def _parse_manifest(path: Path) -> dict[str, Any]:
    """Read and validate the top-level structure of profiles.yaml."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ManifestError("profiles.yaml root must be a mapping")
    return data


def _parse_entries(
    raw_list: list | None,
    kind: str,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Parse a list of id-bearing entries (profiles or mixins)."""
    if raw_list is None:
        return [], {}
    if not isinstance(raw_list, list):
        raise ManifestError(f"profiles.yaml must contain a '{kind}' list")

    entries: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}

    for i, item in enumerate(raw_list):
        if not isinstance(item, dict):
            raise ManifestError(f"{kind}[{i}] must be a mapping")

        eid = item.get("id")
        if not eid or not isinstance(eid, str) or not eid.strip():
            raise ManifestError(f"{kind}[{i}] needs a non-empty string 'id'")
        eid = eid.strip()

        lk = eid.casefold()
        if lk in by_id:
            raise ManifestError(f"Duplicate {kind} id (case-insensitive): {eid!r}")

        entries.append(item)
        by_id[lk] = item

    return entries, by_id


def load_profiles(root: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Parse meta/profiles.yaml → profiles section.

    Returns ([], {}) when the file is missing.
    """
    path = root / "meta" / "profiles.yaml"
    if not path.is_file():
        return [], {}
    data = _parse_manifest(path)
    return _parse_entries(data.get("profiles"), "profiles")


def load_mixins(root: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Parse meta/profiles.yaml → mixins section.

    Returns ([], {}) when the file is missing or has no mixins key.
    """
    path = root / "meta" / "profiles.yaml"
    if not path.is_file():
        return [], {}
    data = _parse_manifest(path)
    return _parse_entries(data.get("mixins"), "mixins")


# ---------------------------------------------------------------------------
# Resolution (inheritance + mixin merge)
# ---------------------------------------------------------------------------

# Fields that are metadata, not merged from parent/mixin.
_META_FIELDS = frozenset({"id", "name", "description", "extends", "mixins"})


def resolve_profile(
    profile_id: str,
    profiles_by_id: dict[str, dict[str, Any]],
    mixins_by_id: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return a fully-resolved profile with inheritance and mixins applied.

    Merge order: extends parent → mixins (declared order, later wins) → self.

    Raises ``ManifestError`` on missing references or illegal structures.
    """
    mixins_by_id = mixins_by_id or {}
    lk = profile_id.casefold()
    profile = profiles_by_id.get(lk)
    if profile is None:
        raise ManifestError(f"Unknown profile id: {profile_id!r}")

    merged: dict[str, Any] = {}

    # --- 1. extends (single-layer) ---
    parent_id = profile.get("extends")
    if parent_id:
        plk = parent_id.casefold()
        parent = profiles_by_id.get(plk)
        if parent is None:
            raise ManifestError(
                f"Profile {profile_id!r}: extends unknown profile {parent_id!r}"
            )
        if parent.get("extends"):
            raise ManifestError(
                f"Profile {profile_id!r}: multi-layer inheritance not allowed "
                f"(parent {parent_id!r} also has 'extends')"
            )
        if parent.get("mixins"):
            raise ManifestError(
                f"Profile {profile_id!r}: parent {parent_id!r} must not have 'mixins'"
            )
        # Merge parent fields (excluding meta)
        for k, v in parent.items():
            if k not in _META_FIELDS:
                merged[k] = copy.deepcopy(v)

    # --- 2. mixins (declared order, later wins) ---
    mixin_ids = profile.get("mixins") or []
    for mid in mixin_ids:
        mlk = mid.casefold()
        mixin = mixins_by_id.get(mlk)
        if mixin is None:
            raise ManifestError(
                f"Profile {profile_id!r}: references unknown mixin {mid!r}"
            )
        for k, v in mixin.items():
            if k not in _META_FIELDS:
                if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
                    merged[k] = _deep_merge(merged[k], v)
                else:
                    merged[k] = copy.deepcopy(v)

    # --- 3. self fields (highest priority) ---
    for k, v in profile.items():
        if k not in _META_FIELDS:
            if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
                merged[k] = _deep_merge(merged[k], v)
            else:
                merged[k] = copy.deepcopy(v)

    # Preserve identity fields from self
    merged["id"] = profile["id"]
    if "name" in profile:
        merged["name"] = profile["name"]
    if "description" in profile:
        merged["description"] = profile["description"]

    return merged
