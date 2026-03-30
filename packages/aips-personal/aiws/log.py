"""Centralised logging setup for aiws CLI."""

from __future__ import annotations

import logging
import sys


def setup_logging(verbose: bool = False) -> None:
    """Configure the root ``aiws`` logger.

    * ``--verbose`` → DEBUG on stderr
    * default     → INFO on stderr
    """
    level = logging.DEBUG if verbose else logging.INFO
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger = logging.getLogger("aiws")
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)
