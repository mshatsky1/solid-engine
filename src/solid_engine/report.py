"""Reporting utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .metrics import ReliabilityMetrics
from .models import ReadingBatch


@dataclass
class ReportLine:
    source: str
    count: int
    average_delta: float
    std_dev: float
    outlier_ratio: float

    def as_text(self) -> str:
        return (
            f"{self.source:>12} | count={self.count:3d} "
            f"avg={self.average_delta:+.3f} std={self.std_dev:.3f} outliers={self.outlier_ratio:.2%}"
        )


class ReportBuilder:
    def build(self, batches: Iterable[ReadingBatch]) -> list[ReportLine]:
        output: list[ReportLine] = []
        for batch in batches:
            metrics = ReliabilityMetrics.from_readings(batch.readings)
            output.append(
                ReportLine(
                    source=batch.source,
                    count=metrics.count,
                    average_delta=metrics.average_delta,
                    std_dev=metrics.std_dev,
                    outlier_ratio=metrics.outlier_ratio,
                )
            )
        return output

    def format(self, batches: Iterable[ReadingBatch]) -> str:
        lines = [line.as_text() for line in self.build(batches)]
        return "\n".join(lines)

    def export_to_dict(self, batches: Iterable[ReadingBatch]) -> list[dict[str, str | int | float]]:
        """Export report data as a list of dictionaries."""
        rows = self.build(batches)
        return [
            {
                "source": row.source,
                "count": row.count,
                "average_delta": row.average_delta,
                "std_dev": row.std_dev,
                "outlier_ratio": row.outlier_ratio,
            }
            for row in rows
        ]
