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

    @property
    def relative_error(self) -> float:
        """Relative error as a percentage of expected value."""
        if self.expected == 0:
            return 0.0
        return (self.delta / self.expected) * 100.0

    def is_outlier(self, threshold: float = 5.0) -> bool:
        """Check if reading is an outlier based on absolute delta threshold."""
        return abs(self.delta) >= threshold


@dataclass(frozen=True)
class ReadingBatch:
    """Collection wrapper to make downstream logic more explicit."""

    source: str
    readings: List[SensorReading]

    @classmethod
    def from_iterable(cls, source: str, iterable: Iterable[SensorReading]) -> "ReadingBatch":
        return cls(source=source, readings=list(iterable))

    def filter_by_sensor(self, sensor_id: str) -> "ReadingBatch":
        """Create a new batch filtered by sensor ID."""
        filtered = [r for r in self.readings if r.sensor_id == sensor_id]
        return ReadingBatch(source=f"{self.source}:{sensor_id}", readings=filtered)

    def count(self) -> int:
        """Return the number of readings in this batch."""
        return len(self.readings)
