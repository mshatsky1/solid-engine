from datetime import datetime

from solid_engine.models import ReadingBatch, SensorReading
from solid_engine.report import ReportBuilder


def _reading(value: float) -> SensorReading:
    return SensorReading(
        sensor_id="sensor-1",
        recorded_at=datetime(2025, 1, 1),
        value=value,
        expected=10,
    )


def test_report_format_includes_source() -> None:
    batch = ReadingBatch.from_iterable("csv", [_reading(10.2), _reading(9.8)])

    text = ReportBuilder().format([batch])

    assert "csv" in text
    assert "avg" in text
