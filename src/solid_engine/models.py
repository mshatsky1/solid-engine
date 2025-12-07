"""Typed data models used across Solid Engine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List


@dataclass(frozen=True)
class SensorReading:
    """Single measurement captured by a sensor."""

    sensor_id: str
    recorded_at: datetime
    value: float
    expected: float

    def __post_init__(self) -> None:
        """Validate reading data after initialization."""
        if not self.sensor_id:
            raise ValueError("sensor_id cannot be empty")
        if not isinstance(self.value, (int, float)):
            raise TypeError("value must be numeric")
        if not isinstance(self.expected, (int, float)):
            raise TypeError("expected must be numeric")

    @property
    def delta(self) -> float:
        """Difference between measurement and expected value."""

        return self.value - self.expected


@dataclass(frozen=True)
class ReadingBatch:
    """Collection wrapper to make downstream logic more explicit."""

    source: str
    readings: List[SensorReading]

    @classmethod
    def from_iterable(cls, source: str, iterable: Iterable[SensorReading]) -> "ReadingBatch":
        return cls(source=source, readings=list(iterable))
