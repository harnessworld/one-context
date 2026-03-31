"""Tests for one_context.profiles — loading, inheritance, mixin, and resolution."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from one_context.errors import ManifestError
from one_context.profiles import (
    _deep_merge,
    load_mixins,
    load_profiles,
    resolve_profile,
)


# ---------------------------------------------------------------------------
# deep_merge
# ---------------------------------------------------------------------------

class TestDeepMerge:
    def test_flat_override(self):
        assert _deep_merge({"a": 1}, {"a": 2}) == {"a": 2}

    def test_disjoint_keys(self):
        assert _deep_merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

    def test_nested_merge(self):
        base = {"x": {"a": 1, "b": 2}}
        over = {"x": {"b": 3, "c": 4}}
        assert _deep_merge(base, over) == {"x": {"a": 1, "b": 3, "c": 4}}

    def test_list_replaced_not_merged(self):
        base = {"items": [1, 2]}
        over = {"items": [3]}
        assert _deep_merge(base, over) == {"items": [3]}

    def test_does_not_mutate_inputs(self):
        base = {"x": {"a": 1}}
        over = {"x": {"b": 2}}
        _deep_merge(base, over)
        assert base == {"x": {"a": 1}}
        assert over == {"x": {"b": 2}}


# ---------------------------------------------------------------------------
# load_profiles (existing tests preserved)
# ---------------------------------------------------------------------------

class TestLoadProfiles:
    def test_missing_file_returns_empty(self, tmp_root: Path):
        profiles, by_id = load_profiles(tmp_root)
        assert profiles == []
        assert by_id == {}

    def test_basic_load(self, tmp_root_with_workspaces: Path):
        profiles, by_id = load_profiles(tmp_root_with_workspaces)
        assert len(profiles) == 1
        assert profiles[0]["id"] == "default"
        assert "default" in by_id

    def test_case_insensitive_lookup(self, tmp_root_with_workspaces: Path):
        _, by_id = load_profiles(tmp_root_with_workspaces)
        assert by_id.get("DEFAULT".casefold()) is not None

    def test_duplicate_id_raises(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                profiles:
                  - id: dup
                    name: First
                  - id: DUP
                    name: Second
            """),
            encoding="utf-8",
        )
        with pytest.raises(ManifestError, match="Duplicate profiles id"):
            load_profiles(tmp_root)

    def test_missing_id_raises(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                profiles:
                  - name: No ID
            """),
            encoding="utf-8",
        )
        with pytest.raises(ManifestError, match="needs a non-empty string 'id'"):
            load_profiles(tmp_root)

    def test_bad_root_type(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            "- just a list\n", encoding="utf-8"
        )
        with pytest.raises(ManifestError, match="root must be a mapping"):
            load_profiles(tmp_root)

    def test_null_profiles_key(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            "profiles:\n", encoding="utf-8"
        )
        profiles, by_id = load_profiles(tmp_root)
        assert profiles == []

    def test_non_mapping_item_raises(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                profiles:
                  - just a string
            """),
            encoding="utf-8",
        )
        with pytest.raises(ManifestError, match="must be a mapping"):
            load_profiles(tmp_root)


# ---------------------------------------------------------------------------
# load_mixins
# ---------------------------------------------------------------------------

class TestLoadMixins:
    def test_missing_file_returns_empty(self, tmp_root: Path):
        mixins, by_id = load_mixins(tmp_root)
        assert mixins == []
        assert by_id == {}

    def test_no_mixins_key(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            "profiles:\n  - id: p1\n    name: P1\n",
            encoding="utf-8",
        )
        mixins, _ = load_mixins(tmp_root)
        assert mixins == []

    def test_basic_load(self, tmp_root: Path):
        (tmp_root / "meta" / "profiles.yaml").write_text(
            textwrap.dedent("""\
                mixins:
                  - id: strict
                    name: Strict
                    behavior:
                      safety_level: conservative
                profiles:
                  - id: base
                    name: Base
            """),
            encoding="utf-8",
        )
        mixins, by_id = load_mixins(tmp_root)
        assert len(mixins) == 1
        assert "strict" in by_id


# ---------------------------------------------------------------------------
# resolve_profile
# ---------------------------------------------------------------------------

class TestResolveProfile:
    @pytest.fixture()
    def profiles_and_mixins(self):
        """Return (profiles_by_id, mixins_by_id) for resolution tests."""
        profiles_by_id = {
            "base": {
                "id": "base",
                "name": "Base",
                "mode": "edit",
                "behavior": {
                    "plan_first": False,
                    "safety_level": "standard",
                    "test_expectation": "targeted",
                },
                "output_style": {"tone": "concise"},
            },
            "child": {
                "id": "child",
                "name": "Child",
                "extends": "base",
                "behavior": {
                    "test_expectation": "integration",
                },
            },
            "with-mixin": {
                "id": "with-mixin",
                "name": "With Mixin",
                "extends": "base",
                "mixins": ["strict"],
                "behavior": {
                    "test_expectation": "e2e",
                },
            },
        }
        mixins_by_id = {
            "strict": {
                "id": "strict",
                "name": "Strict",
                "behavior": {"safety_level": "conservative"},
                "output_style": {"tone": "structured"},
            },
        }
        return profiles_by_id, mixins_by_id

    def test_base_profile_resolves_to_itself(self, profiles_and_mixins):
        p_by_id, m_by_id = profiles_and_mixins
        result = resolve_profile("base", p_by_id, m_by_id)
        assert result["mode"] == "edit"
        assert result["behavior"]["plan_first"] is False

    def test_extends_inherits_parent_fields(self, profiles_and_mixins):
        p_by_id, m_by_id = profiles_and_mixins
        result = resolve_profile("child", p_by_id, m_by_id)
        # Inherited from parent
        assert result["mode"] == "edit"
        assert result["behavior"]["plan_first"] is False
        assert result["behavior"]["safety_level"] == "standard"
        # Overridden by child
        assert result["behavior"]["test_expectation"] == "integration"
        # Identity is child's
        assert result["id"] == "child"
        assert result["name"] == "Child"

    def test_mixin_applied_between_parent_and_self(self, profiles_and_mixins):
        p_by_id, m_by_id = profiles_and_mixins
        result = resolve_profile("with-mixin", p_by_id, m_by_id)
        # From parent
        assert result["mode"] == "edit"
        assert result["behavior"]["plan_first"] is False
        # From mixin (overrides parent's standard)
        assert result["behavior"]["safety_level"] == "conservative"
        assert result["output_style"]["tone"] == "structured"
        # From self (overrides parent's targeted)
        assert result["behavior"]["test_expectation"] == "e2e"

    def test_unknown_profile_raises(self, profiles_and_mixins):
        p_by_id, m_by_id = profiles_and_mixins
        with pytest.raises(ManifestError, match="Unknown profile id"):
            resolve_profile("nonexistent", p_by_id, m_by_id)

    def test_unknown_parent_raises(self):
        p = {"bad": {"id": "bad", "extends": "missing"}}
        with pytest.raises(ManifestError, match="extends unknown profile"):
            resolve_profile("bad", p)

    def test_unknown_mixin_raises(self):
        p = {"x": {"id": "x", "mixins": ["missing"]}}
        with pytest.raises(ManifestError, match="references unknown mixin"):
            resolve_profile("x", p, {})

    def test_multi_layer_inheritance_raises(self):
        p = {
            "grandparent": {"id": "grandparent"},
            "parent": {"id": "parent", "extends": "grandparent"},
            "child": {"id": "child", "extends": "parent"},
        }
        with pytest.raises(ManifestError, match="multi-layer inheritance"):
            resolve_profile("child", p)

    def test_parent_with_mixins_raises(self):
        p = {
            "parent": {"id": "parent", "mixins": ["x"]},
            "child": {"id": "child", "extends": "parent"},
        }
        with pytest.raises(ManifestError, match="must not have 'mixins'"):
            resolve_profile("child", p)

    def test_multiple_mixins_later_wins(self):
        p = {
            "target": {
                "id": "target",
                "mixins": ["m1", "m2"],
            },
        }
        m = {
            "m1": {"id": "m1", "behavior": {"level": "low", "scope": "narrow"}},
            "m2": {"id": "m2", "behavior": {"level": "high"}},
        }
        result = resolve_profile("target", p, m)
        # m2 overrides m1's level
        assert result["behavior"]["level"] == "high"
        # m1's scope preserved (m2 doesn't touch it)
        assert result["behavior"]["scope"] == "narrow"

    def test_self_fields_override_everything(self):
        p = {
            "parent": {"id": "parent", "behavior": {"x": "from-parent"}},
            "child": {
                "id": "child",
                "extends": "parent",
                "mixins": ["mx"],
                "behavior": {"x": "from-self"},
            },
        }
        m = {"mx": {"id": "mx", "behavior": {"x": "from-mixin"}}}
        result = resolve_profile("child", p, m)
        assert result["behavior"]["x"] == "from-self"
