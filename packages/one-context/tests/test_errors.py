"""Tests for one_context.errors — ManifestError attributes."""

from __future__ import annotations

import pytest

from one_context.errors import ManifestError


class TestManifestError:
    def test_is_exception(self):
        assert issubclass(ManifestError, Exception)

    def test_message_attribute(self):
        err = ManifestError("boom")
        assert err.message == "boom"
        assert str(err) == "boom"

    def test_can_be_raised_and_caught(self):
        with pytest.raises(ManifestError):
            raise ManifestError("test error")
