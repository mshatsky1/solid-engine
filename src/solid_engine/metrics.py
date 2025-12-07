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
    max_delta: float

    @classmethod
    def from_readings(
        cls,
        readings: Iterable[SensorReading],
        *,
        outlier_threshold: float = 5.0,
    ) -> "ReliabilityMetrics":
        if outlier_threshold < 0:
            raise ValueError("outlier_threshold must be non-negative")
        # Convert to list once for efficiency
        data = list(readings)
        if not data:
            return cls(count=0, average_delta=0.0, std_dev=0.0, outlier_ratio=0.0, max_delta=0.0)

        # Single pass through data for better performance
        deltas = []
        outliers = 0
        max_abs_delta = 0.0
        for reading in data:
            delta = reading.delta
            deltas.append(delta)
            abs_delta = abs(delta)
            if abs_delta >= outlier_threshold:
                outliers += 1
            if abs_delta > max_abs_delta:
                max_abs_delta = abs_delta

        avg = mean(deltas)
        spread = pstdev(deltas) if len(deltas) > 1 else 0.0
        ratio = outliers / len(deltas) if deltas else 0.0
        return cls(
            count=len(deltas),
            average_delta=avg,
            std_dev=spread,
            outlier_ratio=ratio,
            max_delta=max_abs_delta if deltas else 0.0,
        )

    def to_dict(self) -> dict[str, int | float]:
        """Convert metrics to dictionary format."""
        return {
            "count": self.count,
            "average_delta": round(self.average_delta, 4),
            "std_dev": round(self.std_dev, 4),
            "outlier_ratio": round(self.outlier_ratio, 4),
            "max_delta": round(self.max_delta, 4),
        }

    def summary(self) -> str:
        """Generate a human-readable summary of metrics."""
        return (
            f"Count: {self.count}, "
            f"Avg Delta: {self.average_delta:.4f}, "
            f"Std Dev: {self.std_dev:.4f}, "
            f"Outliers: {self.outlier_ratio:.2%}, "
            f"Max Delta: {self.max_delta:.4f}"
        )
