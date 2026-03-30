#!/usr/bin/env python3
"""
Clone or update sub-repositories declared in meta/repos.yaml (cross-platform).

Prefer the unified CLI after installing the package:

  pip install -e ./packages/aips-personal
  aiws sync

This script remains for convenience; it always uses the aips-personal根目录 that
contains this `scripts/` directory (not cwd discovery).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_PKG = _ROOT / "packages" / "aips-personal"
if _PKG.is_dir():
    sys.path.insert(0, str(_PKG))

try:
    from aiws.dotenv import load_dotenv
    from aiws.sync import sync_repositories
except ImportError:
    print(
        "Missing aiws package. Run: pip install -e ./packages/aips-personal",
        file=sys.stderr,
    )
    sys.exit(1)


def main() -> None:
    load_dotenv(_ROOT / ".env")

    parser = argparse.ArgumentParser(
        description="Sync sub-repos from meta/repos.yaml (legacy script)"
    )
    parser.add_argument(
        "select",
        nargs="*",
        metavar="ID_OR_ALIAS",
        help="If set, only these ids or aliases (case-insensitive)",
    )
    args = parser.parse_args()

    sync_repositories(_ROOT, args.select if args.select else None)


if __name__ == "__main__":
    main()
