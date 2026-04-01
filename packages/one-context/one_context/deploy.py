"""Load and validate deploy.yaml manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from one_context.errors import ManifestError

VALID_STRATEGIES = {"docker-compose", "helm", "raw-script", "manual", "none"}


def load_deploy_yaml(path: Path) -> dict[str, Any]:
    """Parse a deploy.yaml file and return a dict.

    Raises ``ManifestError`` for structural issues.
    """
    if not path.is_file():
        raise ManifestError(f"deploy manifest not found: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ManifestError(f"deploy.yaml root must be a mapping: {path}")
    return data


def validate_deploy_yaml(path: Path) -> tuple[list[str], list[str]]:
    """Validate a deploy.yaml file.

    Returns ``(errors, warnings)`` lists.
    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        data = load_deploy_yaml(path)
    except ManifestError as e:
        return [e.message], []

    # version
    version = data.get("version")
    if version != "1":
        errors.append(f"expected version '1', got {version!r}")

    # name
    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("missing or empty 'name' field")

    # strategy
    strategy = data.get("strategy")
    if not strategy or strategy not in VALID_STRATEGIES:
        errors.append(
            f"invalid strategy {strategy!r}. "
            f"Must be one of: {', '.join(sorted(VALID_STRATEGIES))}"
        )

    # stages
    stages = data.get("stages")
    if not stages or not isinstance(stages, list):
        errors.append("'stages' must be a non-empty list")
    else:
        seen_ids: set[str] = set()
        has_health_check = False
        for i, stage in enumerate(stages):
            if not isinstance(stage, dict):
                errors.append(f"stages[{i}] must be a mapping")
                continue

            sid = stage.get("id")
            if not sid or not isinstance(sid, str) or not sid.strip():
                errors.append(f"stages[{i}]: missing or empty 'id'")
            else:
                sid = sid.strip()
                if sid in seen_ids:
                    errors.append(f"stages[{i}]: duplicate stage id {sid!r}")
                seen_ids.add(sid)

            cmd = stage.get("cmd")
            if not cmd or not isinstance(cmd, str) or not cmd.strip():
                errors.append(f"stages[{i}]: missing or empty 'cmd'")

            if stage.get("health_check"):
                has_health_check = True

        if not has_health_check:
            warnings.append("no stage has a 'health_check' defined")

    # rollback
    rollback = data.get("rollback")
    if strategy and strategy not in ("none", "manual"):
        if not rollback or not isinstance(rollback, dict) or not rollback.get("cmd"):
            warnings.append("no 'rollback.cmd' defined for active deployment strategy")

    return errors, warnings
