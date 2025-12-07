"""Tests for data models."""

import pytest
from datetime import datetime

from solid_engine.models import SensorReading, ReadingBatch


def test_sensor_reading_validation_rejects_empty_id() -> None:
    """Test that SensorReading rejects empty sensor_id."""
    with pytest.raises(ValueError, match="sensor_id cannot be empty"):
        SensorReading(
            sensor_id="",
            recorded_at=datetime(2025, 1, 1),
            value=10.0,
            expected=10.0,
        )


def test_sensor_reading_relative_error() -> None:
    """Test relative error calculation."""
    reading = SensorReading(
        sensor_id="sensor-1",
        recorded_at=datetime(2025, 1, 1),
        value=11.0,
        expected=10.0,
    )
    assert reading.relative_error == 10.0


def test_sensor_reading_is_outlier() -> None:
    """Test outlier detection."""
    reading1 = SensorReading(
        sensor_id="sensor-1",
        recorded_at=datetime(2025, 1, 1),
        value=15.0,
        expected=10.0,
    )
    reading2 = SensorReading(
        sensor_id="sensor-1",
        recorded_at=datetime(2025, 1, 1),
        value=10.5,
        expected=10.0,
    )
    assert reading1.is_outlier(threshold=5.0) is True
    assert reading2.is_outlier(threshold=5.0) is False


def test_reading_batch_filter_by_sensor() -> None:
    """Test filtering batch by sensor ID."""
    readings = [
        SensorReading("sensor-1", datetime(2025, 1, 1), 10.0, 10.0),
        SensorReading("sensor-2", datetime(2025, 1, 1), 11.0, 10.0),
        SensorReading("sensor-1", datetime(2025, 1, 1), 12.0, 10.0),
    ]
    batch = ReadingBatch("test", readings)
    filtered = batch.filter_by_sensor("sensor-1")
    assert filtered.count() == 2
    assert all(r.sensor_id == "sensor-1" for r in filtered.readings)

