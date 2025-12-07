"""Utility helpers for Solid Engine."""

from __future__ import annotations

import logging
from datetime import datetime

# Configure module-level logger
logger = logging.getLogger(__name__)


def clamp(value: float, *, lower: float, upper: float) -> float:
    """Clamp a value between two bounds."""

    if lower > upper:
        raise ValueError("lower bound cannot exceed upper bound")
    return max(lower, min(upper, value))


def normalize(value: float, min_val: float, max_val: float) -> float:
    """Normalize a value to the range [0, 1]."""
    if max_val == min_val:
        return 0.0
    return (value - min_val) / (max_val - min_val)


def round_to_precision(value: float, precision: int = 2) -> float:
    """Round a float to specified decimal places."""
    return round(value, precision)


def format_timestamp(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a datetime object as a string."""
    return dt.strftime(format_str)


def show_progress(current: int, total: int, prefix: str = "Progress") -> None:
    """Display a simple progress indicator."""
    if total == 0:
        return
    percentage = (current / total) * 100
    logger.info(f"{prefix}: {current}/{total} ({percentage:.1f}%)")
