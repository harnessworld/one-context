"""
Tool-specific adapters (Cursor, Claude Code, OpenClaw, ...).

Canonical rules, skills, and context live under the repo ``knowledge/`` tree
and ``meta/*.yaml``.  Adapters translate that shared intent into formats each
tool understands.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GeneratedFile:
    """One file produced by an adapter."""

    rel_path: str
    """Path relative to the aips-personal root."""

    content: str
    """Full file content."""

    description: str
    """Human-readable explanation (shown in dry-run output)."""


class AdapterBase(ABC):
    """Base class for all tool adapters."""

    name: str = ""
    """Short machine-readable adapter name, e.g. ``cursor``."""

    supports_file_ref: bool = False
    """True if the tool can follow ``@file`` references at runtime."""

    @abstractmethod
    def generate(
        self,
        root: Path,
        workspace: dict[str, Any],
        context: dict[str, Any],
    ) -> list[GeneratedFile]:
        """Produce tool-specific configuration files.

        Parameters
        ----------
        root:
            aips-personal root directory.
        workspace:
            The raw workspace dict from ``meta/workspaces.yaml``.
        context:
            The full context dict returned by
            ``aiws.context.build_workspace_context``.
        """
        ...


# ---------------------------------------------------------------------------
# Adapter registry
# ---------------------------------------------------------------------------

ADAPTERS: dict[str, type[AdapterBase]] = {}


def register(name: str):
    """Class decorator that registers an adapter under *name*."""

    def decorator(cls: type[AdapterBase]) -> type[AdapterBase]:
        cls.name = name
        ADAPTERS[name] = cls
        return cls

    return decorator


def get_adapter(name: str) -> AdapterBase:
    """Instantiate a registered adapter by name."""
    cls = ADAPTERS.get(name)
    if cls is None:
        raise ValueError(
            f"Unknown adapter: {name!r}. "
            f"Available: {', '.join(sorted(ADAPTERS))}"
        )
    return cls()


def list_adapters() -> list[str]:
    """Return sorted list of registered adapter names."""
    return sorted(ADAPTERS)
