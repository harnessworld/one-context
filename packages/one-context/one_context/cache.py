"""SHA256-based content cache for incremental adapt runs.

Records the hash of each generated file's content on disk.  On subsequent
runs, files whose generated content matches the cached hash are skipped
entirely — no disk write needed.  This avoids unnecessary I/O and preserves
file modification timestamps for unchanged outputs.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


CACHE_DIR = ".onecxt"
CACHE_FILE = "adapt-cache.json"


def _cache_path(root: Path) -> Path:
    return root / CACHE_DIR / CACHE_FILE


def file_hash(content: str) -> str:
    """Return a short SHA-256 hex digest of *content*."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def load_cache(root: Path) -> dict[str, str]:
    """Load the adapt cache from disk.

    Returns a dict mapping ``rel_path`` → ``hash``.  Returns an empty
    dict when the cache file does not exist or is invalid JSON.
    """
    path = _cache_path(root)
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items()}
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        pass
    return {}


def save_cache(root: Path, cache: dict[str, str]) -> None:
    """Persist the adapt cache to disk."""
    path = _cache_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def needs_write(rel_path: str, content: str, cache: dict[str, str]) -> bool:
    """Return True if *content* differs from the cached version.

    A file needs writing when:
    - It has no entry in the cache, or
    - Its content hash differs from the cached hash.
    """
    current = file_hash(content)
    return cache.get(rel_path) != current


def update_cache(rel_path: str, content: str, cache: dict[str, str]) -> None:
    """Record the current hash of *content* in *cache*."""
    cache[rel_path] = file_hash(content)