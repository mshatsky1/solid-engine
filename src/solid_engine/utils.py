"""Utility helpers for Solid Engine."""

from __future__ import annotations

import logging

# Configure module-level logger
logger = logging.getLogger(__name__)


def clamp(value: float, *, lower: float, upper: float) -> float:
    """Clamp a value between two bounds."""

    if lower > upper:
        raise ValueError("lower bound cannot exceed upper bound")
    return max(lower, min(upper, value))
