from datetime import datetime

from solid_engine.metrics import ReliabilityMetrics
from solid_engine.models import ReadingBatch, SensorReading


def _reading(delta: float) -> SensorReading:
    return SensorReading(
        sensor_id="sensor-1",
        recorded_at=datetime(2025, 1, 1),
        value=10 + delta,
        expected=10,
    )


def test_metrics_from_readings_counts_outliers() -> None:
    batch = ReadingBatch.from_iterable(
        source="test",
        iterable=[_reading(delta) for delta in (-0.5, 0.1, 5.1)],
    )

    metrics = ReliabilityMetrics.from_readings(batch.readings, outlier_threshold=5)

    assert metrics.count == 3
    assert metrics.outlier_ratio == 1 / 3


def test_metrics_empty_batch_returns_zeroes() -> None:
    metrics = ReliabilityMetrics.from_readings([], outlier_threshold=1)

    assert metrics.count == 0
    assert metrics.average_delta == 0.0
