"""
FieldRule dataclass and rule-matching engine.

Profile fields (e.g. ``behavior.plan_first: true``) are translated into
natural-language sentences via declarative rules.  Each adapter declares its
own rule set; the engine matches field values and assembles output text.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class FieldRule:
    """One translation rule: field + expected value -> output sentence."""

    field: str
    """Dot-separated path into the profile dict, e.g. ``behavior.plan_first``."""

    match: Any
    """Value to match (equality check)."""

    output: str
    """Sentence to emit when the rule fires."""

    priority: int = 0
    """Higher priority wins when multiple rules fire for the same field."""

    section: str = ""
    """Optional grouping label (e.g. ``Behavior``, ``Context``)."""


def _resolve(data: dict[str, Any], dotpath: str) -> Any:
    """Resolve a dot-separated key path against a nested dict.

    Returns ``_MISSING`` sentinel when any segment is absent.
    """
    current: Any = data
    for segment in dotpath.split("."):
        if not isinstance(current, dict):
            return _MISSING
        current = current.get(segment, _MISSING)
        if current is _MISSING:
            return _MISSING
    return current


_MISSING = object()


def match_rules(
    profile: dict[str, Any],
    rules: list[FieldRule],
) -> list[FieldRule]:
    """Return the subset of *rules* that match *profile*, sorted by priority desc."""
    matched: list[FieldRule] = []
    for rule in rules:
        value = _resolve(profile, rule.field)
        if value is _MISSING:
            continue
        if value == rule.match:
            matched.append(rule)
    matched.sort(key=lambda r: r.priority, reverse=True)
    return matched


def render_rules_by_section(
    matched: list[FieldRule],
    *,
    heading_level: int = 2,
) -> str:
    """Group matched rules by section and render as Markdown."""
    sections: dict[str, list[str]] = {}
    for rule in matched:
        key = rule.section or "_default"
        sections.setdefault(key, []).append(rule.output)

    prefix = "#" * heading_level
    parts: list[str] = []
    for section_key, sentences in sections.items():
        if section_key != "_default":
            parts.append(f"{prefix} {section_key}")
            parts.append("")
        for sentence in sentences:
            parts.append(sentence)
        parts.append("")

    return "\n".join(parts).rstrip("\n") + "\n"
