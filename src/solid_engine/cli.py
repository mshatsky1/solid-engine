"""Command line entry point for Solid Engine."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Iterable

import click

from .filters import filter_by_sensor_id, filter_by_time_range, filter_outliers
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
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output with additional details.")
def report(data_path: Path, as_json: bool, verbose: bool) -> None:
    """Generate a text report from CSV input."""

    if verbose:
        click.echo(f"Loading data from: {data_path}", err=True)
    readings = list(_load_csv(data_path))
    if verbose:
        click.echo(f"Loaded {len(readings)} readings", err=True)
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


@main.command()
@click.option("--data", "data_path", type=click.Path(path_type=Path), default=DEFAULT_DATA_PATH)
@click.option("--sensor-id", help="Filter by sensor ID")
@click.option("--remove-outliers", type=float, help="Remove outliers above threshold")
@click.option("--start-time", help="Start time (ISO format)")
@click.option("--end-time", help="End time (ISO format)")
@click.option("--output", type=click.Path(path_type=Path), help="Output file path")
def filter_data(
    data_path: Path,
    sensor_id: str | None,
    remove_outliers: float | None,
    start_time: str | None,
    end_time: str | None,
    output: Path | None,
) -> None:
    """Filter sensor readings by various criteria."""
    readings = list(_load_csv(data_path))
    
    if sensor_id:
        readings = filter_by_sensor_id(readings, sensor_id)
        click.echo(f"Filtered to sensor {sensor_id}: {len(readings)} readings", err=True)
    
    if start_time or end_time:
        start = datetime.fromisoformat(start_time) if start_time else None
        end = datetime.fromisoformat(end_time) if end_time else None
        readings = filter_by_time_range(readings, start_time=start, end_time=end)
        click.echo(f"Filtered by time range: {len(readings)} readings", err=True)
    
    if remove_outliers is not None:
        before = len(readings)
        readings = filter_outliers(readings, threshold=remove_outliers)
        after = len(readings)
        click.echo(f"Removed {before - after} outliers", err=True)
    
    if output:
        batch = ReadingBatch.from_iterable(source=data_path.name, iterable=readings)
        builder = ReportBuilder()
        builder.export_to_csv([batch], output)
        click.echo(f"Exported {len(readings)} readings to {output}")
    else:
        batch = ReadingBatch.from_iterable(source=data_path.name, iterable=readings)
        builder = ReportBuilder()
        click.echo(builder.format([batch]))


if __name__ == "__main__":
    main()
