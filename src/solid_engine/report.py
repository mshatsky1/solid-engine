"""Reporting utilities."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
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

    def format(self, batches: Iterable[ReadingBatch], style: str = "table") -> str:
        """Format report with different styles."""
        lines = self.build(batches)
        if style == "table":
            return self._format_table(lines)
        elif style == "compact":
            return self._format_compact(lines)
        elif style == "detailed":
            return self._format_detailed(lines)
        else:
            return "\n".join(line.as_text() for line in lines)

    def _format_table(self, lines: list[ReportLine]) -> str:
        """Format as a table with headers."""
        header = f"{'Source':>12} | {'Count':>5} | {'Avg Delta':>10} | {'Std Dev':>8} | {'Outliers':>8}"
        separator = "-" * len(header)
        rows = [header, separator] + [line.as_text() for line in lines]
        return "\n".join(rows)

    def _format_compact(self, lines: list[ReportLine]) -> str:
        """Format as compact single-line entries."""
        return "\n".join(
            f"{line.source}: {line.count} readings, "
            f"avg={line.average_delta:+.3f}, outliers={line.outlier_ratio:.1%}"
            for line in lines
        )

    def _format_detailed(self, lines: list[ReportLine]) -> str:
        """Format with detailed information."""
        result = []
        for line in lines:
            result.append(f"Source: {line.source}")
            result.append(f"  Count: {line.count}")
            result.append(f"  Average Delta: {line.average_delta:+.6f}")
            result.append(f"  Standard Deviation: {line.std_dev:.6f}")
            result.append(f"  Outlier Ratio: {line.outlier_ratio:.2%}")
            result.append("")
        return "\n".join(result)

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

    def export_to_csv(self, batches: Iterable[ReadingBatch], output_path: Path) -> None:
        """Export report data to CSV file."""
        rows = self.build(batches)
        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["source", "count", "average_delta", "std_dev", "outlier_ratio"],
            )
            writer.writeheader()
            for row in rows:
                writer.writerow(
                    {
                        "source": row.source,
                        "count": row.count,
                        "average_delta": f"{row.average_delta:.4f}",
                        "std_dev": f"{row.std_dev:.4f}",
                        "outlier_ratio": f"{row.outlier_ratio:.4f}",
                    }
                )
