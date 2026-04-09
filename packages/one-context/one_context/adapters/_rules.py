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
class AdapterOverride:
    """Per-adapter override for a FieldRule's output or placement."""

    output: str | None = None
    """Override the default output text for this adapter."""

    placement: str = "inline"
    """Where to place the rule: ``"inline"`` (default) or ``"top"``."""


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

    adapter_overrides: dict[str, AdapterOverride] | None = None
    """Per-adapter overrides for output text and placement."""


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
    adapter_name: str | None = None,
) -> str:
    """Group matched rules by section and render as Markdown.

    When *adapter_name* is provided, ``resolve_rule_output`` is used so
    per-adapter output overrides take effect.
    """
    sections: dict[str, list[str]] = {}
    for rule in matched:
        key = rule.section or "_default"
        text = resolve_rule_output(rule, adapter_name) if adapter_name else rule.output
        sections.setdefault(key, []).append(text)

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


def resolve_rule_output(rule: FieldRule, adapter_name: str | None) -> str:
    """Return the output text for *rule*, applying adapter overrides if set."""
    if adapter_name and rule.adapter_overrides:
        override = rule.adapter_overrides.get(adapter_name)
        if override and override.output is not None:
            return override.output
    return rule.output


def resolve_rule_placement(rule: FieldRule, adapter_name: str | None) -> str:
    """Return the placement for *rule*, applying adapter overrides if set."""
    if adapter_name and rule.adapter_overrides:
        override = rule.adapter_overrides.get(adapter_name)
        if override:
            return override.placement
    return "inline"


def collect_top_rules(
    matched: list[FieldRule],
    adapter_name: str,
) -> list[str]:
    """Return output texts of all top-placement rules from *matched*."""
    top: list[str] = []
    for rule in matched:
        if resolve_rule_placement(rule, adapter_name) == "top":
            top.append(resolve_rule_output(rule, adapter_name))
    return top
