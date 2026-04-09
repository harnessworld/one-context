"""Tests for the FieldRule matching engine."""

from __future__ import annotations

from one_context.adapters._rules import (
    AdapterOverride,
    FieldRule,
    _MISSING,
    _resolve,
    collect_top_rules,
    match_rules,
    render_rules_by_section,
    resolve_rule_output,
    resolve_rule_placement,
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

    def test_adapter_name_uses_overrides(self):
        matched = [
            FieldRule(
                "output_style.tone", "minimal",
                "Default to minimal output.",
                section="Output Style",
                adapter_overrides={
                    "claude_code": AdapterOverride(
                        output="ALWAYS be brief.",
                        placement="top",
                    ),
                },
            ),
        ]
        # With adapter_name, override output is used
        text = render_rules_by_section(matched, adapter_name="claude_code")
        assert "ALWAYS be brief." in text
        assert "Default to minimal" not in text

    def test_adapter_name_without_override(self):
        matched = [
            FieldRule(
                "output_style.tone", "minimal",
                "Default to minimal output.",
                section="Output Style",
            ),
        ]
        # Without adapter_overrides, default output is used
        text = render_rules_by_section(matched, adapter_name="claude_code")
        assert "Default to minimal output." in text


# ---------------------------------------------------------------------------
# AdapterOverride, resolve_rule_output, resolve_rule_placement
# ---------------------------------------------------------------------------

class TestAdapterOverride:
    def test_resolve_output_no_override(self):
        rule = FieldRule("x", True, "Default text.")
        assert resolve_rule_output(rule, "claude_code") == "Default text."

    def test_resolve_output_with_override(self):
        rule = FieldRule(
            "x", True, "Default text.",
            adapter_overrides={
                "claude_code": AdapterOverride(output="Hard text."),
            },
        )
        assert resolve_rule_output(rule, "claude_code") == "Hard text."

    def test_resolve_output_override_for_other_adapter(self):
        rule = FieldRule(
            "x", True, "Default text.",
            adapter_overrides={
                "cursor": AdapterOverride(output="Cursor text."),
            },
        )
        assert resolve_rule_output(rule, "claude_code") == "Default text."

    def test_resolve_output_none_adapter_name(self):
        rule = FieldRule(
            "x", True, "Default text.",
            adapter_overrides={
                "claude_code": AdapterOverride(output="Hard text."),
            },
        )
        assert resolve_rule_output(rule, None) == "Default text."

    def test_resolve_output_override_output_is_none(self):
        rule = FieldRule(
            "x", True, "Default text.",
            adapter_overrides={
                "claude_code": AdapterOverride(output=None, placement="top"),
            },
        )
        # output=None means use default
        assert resolve_rule_output(rule, "claude_code") == "Default text."

    def test_resolve_placement_no_override(self):
        rule = FieldRule("x", True, "Text.")
        assert resolve_rule_placement(rule, "claude_code") == "inline"

    def test_resolve_placement_with_override(self):
        rule = FieldRule(
            "x", True, "Text.",
            adapter_overrides={
                "claude_code": AdapterOverride(placement="top"),
            },
        )
        assert resolve_rule_placement(rule, "claude_code") == "top"

    def test_resolve_placement_override_for_other_adapter(self):
        rule = FieldRule(
            "x", True, "Text.",
            adapter_overrides={
                "cursor": AdapterOverride(placement="top"),
            },
        )
        assert resolve_rule_placement(rule, "claude_code") == "inline"


# ---------------------------------------------------------------------------
# collect_top_rules
# ---------------------------------------------------------------------------

class TestCollectTopRules:
    def test_collects_top_rules(self):
        matched = [
            FieldRule(
                "output_style.tone", "minimal", "Soft text.",
                adapter_overrides={
                    "claude_code": AdapterOverride(output="Hard text.", placement="top"),
                },
            ),
            FieldRule("behavior.plan_first", True, "Plan first."),
        ]
        top = collect_top_rules(matched, "claude_code")
        assert top == ["Hard text."]

    def test_no_top_rules(self):
        matched = [
            FieldRule("behavior.plan_first", True, "Plan first."),
        ]
        top = collect_top_rules(matched, "claude_code")
        assert top == []

    def test_uses_adapter_override_output(self):
        matched = [
            FieldRule(
                "output_style.tone", "minimal", "Soft text.",
                adapter_overrides={
                    "claude_code": AdapterOverride(output="ALWAYS be brief.", placement="top"),
                },
            ),
        ]
        top = collect_top_rules(matched, "claude_code")
        assert top == ["ALWAYS be brief."]
