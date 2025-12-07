"""Command line entry point for Solid Engine."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Iterable

import click

from .metrics import ReliabilityMetrics
from .models import ReadingBatch, SensorReading
from .report import ReportBuilder
from .simulation import ScenarioSimulator

DEFAULT_DATA_PATH = Path("data/sample_readings.csv")


def _load_csv(path: Path) -> Iterable[SensorReading]:
    """Load sensor readings from CSV file with error handling."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    try:
        with path.open("r", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                try:
                    yield SensorReading(
                        sensor_id=row["sensor_id"],
                        recorded_at=datetime.fromisoformat(row["recorded_at"]),
                        value=float(row["value"]),
                        expected=float(row["expected"]),
                    )
                except (KeyError, ValueError, TypeError) as e:
                    raise ValueError(f"Invalid data at row {row_num}: {e}") from e
    except IOError as e:
        raise IOError(f"Failed to read file {path}: {e}") from e


@click.group()
def main() -> None:
    """Solid Engine CLI."""


@main.command()
@click.option("--data", "data_path", type=click.Path(path_type=Path), default=DEFAULT_DATA_PATH)
@click.option("--json/--text", "as_json", default=False, help="Return JSON instead of plain text.")
def report(data_path: Path, as_json: bool) -> None:
    """Generate a text report from CSV input."""

    readings = list(_load_csv(data_path))
    batch = ReadingBatch.from_iterable(source=data_path.name, iterable=readings)
    builder = ReportBuilder()
    rows = builder.build([batch])
    if as_json:
        payload = [
            {
                "source": row.source,
                "count": row.count,
                "average_delta": row.average_delta,
                "std_dev": row.std_dev,
                "outlier_ratio": row.outlier_ratio,
            }
            for row in rows
        ]
        click.echo(json.dumps(payload, indent=2))
    else:
        click.echo(builder.format([batch]))


@main.command()
@click.option("--sensor", default="sensor-1")
@click.option("--expected", type=float, default=10.0)
@click.option("--count", type=int, default=5)
@click.option("--seed", type=int, default=42)
def simulate(sensor: str, expected: float, count: int, seed: int) -> None:
    """Generate synthetic readings and print summary metrics."""

    simulator = ScenarioSimulator(seed=seed)
    batch = simulator.generate(sensor_id=sensor, expected_value=expected, count=count)
    metrics = ReliabilityMetrics.from_readings(batch.readings)
    click.echo(metrics.to_dict())


if __name__ == "__main__":
    main()
