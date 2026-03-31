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
    """Path relative to the one-context root."""

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
            one-context root directory.
        workspace:
            The raw workspace dict from ``meta/workspaces.yaml``.
        context:
            The full context dict returned by
            ``one_context.context.build_workspace_context``.
        """
        ...

    def generate_agents(
        self,
        root: Path,
        agents: list[dict[str, Any]],
        profiles_by_id: dict[str, dict[str, Any]],
    ) -> list[GeneratedFile]:
        """Produce per-agent tool-specific configuration files.

        Default implementation returns an empty list; adapters override this
        to emit agent-specific rule / config files that allow the AI tool to
        activate a named agent without any manual file references.

        Parameters
        ----------
        root:
            one-context root directory.
        agents:
            All agent dicts loaded from ``meta/agents.yaml``.
        profiles_by_id:
            Profile lookup dict keyed by lowercased profile id.
        """
        return []

    def generate_project_artifacts(
        self,
        root: Path,
        workspace_ids: list[str],
        agents: list[dict[str, Any]],
    ) -> list[GeneratedFile]:
        """Produce project-root integration files (e.g. ``CLAUDE.md``, OpenClaw manifest).

        Called once per ``onecxt adapt`` run after all workspace-level files
        and agent files are defined. Default: no extra files.
        """
        return []


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
