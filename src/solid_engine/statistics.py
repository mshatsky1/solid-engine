"""Statistical aggregation functions for Solid Engine."""

from __future__ import annotations

from statistics import median, stdev
from typing import Iterable

from .models import SensorReading


def calculate_median_delta(readings: Iterable[SensorReading]) -> float:
    """Calculate the median delta across readings."""
    deltas = [r.delta for r in readings]
    if not deltas:
        return 0.0
    return median(deltas)


def calculate_sample_std_dev(readings: Iterable[SensorReading]) -> float:
    """Calculate sample standard deviation of deltas."""
    deltas = [r.delta for r in readings]
    if len(deltas) < 2:
        return 0.0
    return stdev(deltas)


def calculate_range(readings: Iterable[SensorReading]) -> tuple[float, float]:
    """Calculate min and max delta values."""
    deltas = [r.delta for r in readings]
    if not deltas:
        return (0.0, 0.0)
    return (min(deltas), max(deltas))

