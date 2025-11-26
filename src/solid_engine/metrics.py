"""Reliability metrics for Solid Engine."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Iterable

from .models import SensorReading


@dataclass
class ReliabilityMetrics:
    """Aggregate metrics derived from multiple readings."""

    count: int
    average_delta: float
    std_dev: float
    outlier_ratio: float

    @classmethod
    def from_readings(
        cls,
        readings: Iterable[SensorReading],
        *,
        outlier_threshold: float = 5.0,
    ) -> "ReliabilityMetrics":
        data = list(readings)
        if not data:
            return cls(count=0, average_delta=0.0, std_dev=0.0, outlier_ratio=0.0)

        deltas = [reading.delta for reading in data]
        avg = mean(deltas)
        spread = pstdev(deltas) if len(deltas) > 1 else 0.0
        outliers = sum(1 for delta in deltas if abs(delta) >= outlier_threshold)
        ratio = outliers / len(deltas)
        return cls(count=len(deltas), average_delta=avg, std_dev=spread, outlier_ratio=ratio)

    def to_dict(self) -> dict:
        return {
            "count": self.count,
            "average_delta": round(self.average_delta, 4),
            "std_dev": round(self.std_dev, 4),
            "outlier_ratio": round(self.outlier_ratio, 4),
        }
