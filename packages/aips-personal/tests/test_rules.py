"""Tests for the FieldRule matching engine."""

from __future__ import annotations

from aiws.adapters._rules import (
    FieldRule,
    _MISSING,
    _resolve,
    match_rules,
    render_rules_by_section,
)


# ---------------------------------------------------------------------------
# _resolve
# ---------------------------------------------------------------------------

class TestResolve:
    def test_simple_key(self):
        assert _resolve({"a": 1}, "a") == 1

    def test_nested_key(self):
        assert _resolve({"a": {"b": {"c": 42}}}, "a.b.c") == 42

    def test_missing_key(self):
        assert _resolve({"a": 1}, "b") is _MISSING

    def test_missing_nested(self):
        assert _resolve({"a": {"b": 1}}, "a.c") is _MISSING

    def test_non_dict_intermediate(self):
        assert _resolve({"a": "string"}, "a.b") is _MISSING

    def test_empty_dict(self):
        assert _resolve({}, "a") is _MISSING

    def test_false_value(self):
        """False is a real value, not missing."""
        assert _resolve({"a": False}, "a") is False

    def test_none_value(self):
        """None is a real value, not missing."""
        assert _resolve({"a": None}, "a") is None


# ---------------------------------------------------------------------------
# match_rules
# ---------------------------------------------------------------------------

class TestMatchRules:
    RULES = [
        FieldRule("behavior.plan_first", True, "Plan first.", section="Behavior"),
        FieldRule("behavior.plan_first", False, "No plan needed.", section="Behavior"),
        FieldRule("behavior.safety_level", "conservative", "Be careful.", section="Behavior"),
        FieldRule("output_style.tone", "concise", "Be brief.", section="Output"),
    ]

    def test_basic_matching(self):
        profile = {
            "behavior": {"plan_first": True, "safety_level": "conservative"},
            "output_style": {"tone": "concise"},
        }
        matched = match_rules(profile, self.RULES)
        outputs = [r.output for r in matched]
        assert "Plan first." in outputs
        assert "Be careful." in outputs
        assert "Be brief." in outputs
        assert "No plan needed." not in outputs

    def test_no_match(self):
        profile = {"behavior": {"plan_first": "maybe"}}
        matched = match_rules(profile, self.RULES)
        assert matched == []

    def test_missing_fields(self):
        profile = {"unrelated": True}
        matched = match_rules(profile, self.RULES)
        assert matched == []

    def test_priority_ordering(self):
        rules = [
            FieldRule("x", True, "low", priority=0),
            FieldRule("y", True, "high", priority=10),
            FieldRule("z", True, "mid", priority=5),
        ]
        profile = {"x": True, "y": True, "z": True}
        matched = match_rules(profile, rules)
        assert [r.output for r in matched] == ["high", "mid", "low"]


# ---------------------------------------------------------------------------
# render_rules_by_section
# ---------------------------------------------------------------------------

class TestRenderRulesBySection:
    def test_single_section(self):
        matched = [
            FieldRule("a", True, "Do A.", section="Behavior"),
            FieldRule("b", True, "Do B.", section="Behavior"),
        ]
        text = render_rules_by_section(matched)
        assert "## Behavior" in text
        assert "Do A." in text
        assert "Do B." in text

    def test_multiple_sections(self):
        matched = [
            FieldRule("a", True, "Do A.", section="Behavior"),
            FieldRule("b", True, "Be brief.", section="Output"),
        ]
        text = render_rules_by_section(matched)
        assert "## Behavior" in text
        assert "## Output" in text

    def test_custom_heading_level(self):
        matched = [FieldRule("a", True, "Do A.", section="Behavior")]
        text = render_rules_by_section(matched, heading_level=3)
        assert "### Behavior" in text

    def test_no_section(self):
        matched = [FieldRule("a", True, "Do A.")]
        text = render_rules_by_section(matched)
        # No heading for default section
        assert "Do A." in text
        assert "##" not in text
