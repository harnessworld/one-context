from __future__ import annotations


class ManifestError(Exception):
    """Invalid or inconsistent YAML manifests under meta/."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
