from __future__ import annotations

import os
from pathlib import Path

from aiws.errors import ManifestError


def find_root(start: Path | None = None) -> Path:
    """
    Return the aips-personal root directory containing meta/repos.yaml.

    Order:
    1. AIWS_ROOT environment variable (must contain meta/repos.yaml)
    2. Walk parents from start (default: cwd) looking for meta/repos.yaml
    """
    if env := os.environ.get("AIWS_ROOT", "").strip():
        root = Path(env).expanduser().resolve()
        if not (root / "meta" / "repos.yaml").is_file():
            raise ManifestError(
                f"AIWS_ROOT is set to {root!s} but meta/repos.yaml is missing"
            )
        return root

    cur = (start or Path.cwd()).resolve()
    for p in [cur, *cur.parents]:
        if (p / "meta" / "repos.yaml").is_file():
            return p

    raise ManifestError(
        "Could not find meta/repos.yaml in the current directory or any parent. "
        "Set AIWS_ROOT or run from inside the aips-personal workspace."
    )
