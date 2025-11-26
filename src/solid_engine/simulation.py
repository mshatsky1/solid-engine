"""Simulation helpers that produce derived readings."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from random import Random
from typing import Iterable, List

from .models import ReadingBatch, SensorReading


@dataclass
class ScenarioSimulator:
    """Very small simulation that perturbs expected values."""

    seed: int = 42
    jitter: float = 0.5

    def generate(
        self,
        sensor_id: str,
        expected_value: float,
        *,
        count: int = 10,
        spacing_seconds: int = 60,
    ) -> ReadingBatch:
        rng = Random(self.seed)
        readings: List[SensorReading] = []
        base_time = datetime.utcnow()
        for index in range(count):
            delta = rng.uniform(-self.jitter, self.jitter)
            value = expected_value + delta
            readings.append(
                SensorReading(
                    sensor_id=sensor_id,
                    recorded_at=base_time + timedelta(seconds=index * spacing_seconds),
                    value=value,
                    expected=expected_value,
                )
            )
        return ReadingBatch(source=f"sim:{sensor_id}", readings=readings)

    def extend(self, batches: Iterable[ReadingBatch], *, offset_seconds: int = 15) -> List[ReadingBatch]:
        augmented = []
        for batch in batches:
            new_readings = []
            for reading in batch.readings:
                shifted = SensorReading(
                    sensor_id=reading.sensor_id,
                    recorded_at=reading.recorded_at + timedelta(seconds=offset_seconds),
                    value=reading.value + self.jitter / 10,
                    expected=reading.expected,
                )
                new_readings.append(shifted)
            augmented.append(ReadingBatch(source=batch.source + "+", readings=new_readings))
        return augmented
