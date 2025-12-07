"""Data filtering utilities for Solid Engine."""

from __future__ import annotations

from datetime import datetime
from typing import Callable, Iterable

from .models import ReadingBatch, SensorReading


def filter_by_sensor_id(
    readings: Iterable[SensorReading], sensor_id: str
) -> list[SensorReading]:
    """Filter readings by sensor ID."""
    return [r for r in readings if r.sensor_id == sensor_id]


def filter_by_time_range(
    readings: Iterable[SensorReading],
    start_time: datetime | None = None,
    end_time: datetime | None = None,
) -> list[SensorReading]:
    """Filter readings by time range."""
    result = list(readings)
    if start_time is not None:
        result = [r for r in result if r.recorded_at >= start_time]
    if end_time is not None:
        result = [r for r in result if r.recorded_at <= end_time]
    return result


def filter_by_custom(
    readings: Iterable[SensorReading], predicate: Callable[[SensorReading], bool]
) -> list[SensorReading]:
    """Filter readings using a custom predicate function."""
    return [r for r in readings if predicate(r)]


def filter_outliers(
    readings: Iterable[SensorReading], threshold: float = 5.0
) -> list[SensorReading]:
    """Filter out outlier readings based on delta threshold."""
    return [r for r in readings if abs(r.delta) < threshold]

