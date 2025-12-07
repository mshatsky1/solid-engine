"""Simulation helpers that produce derived readings."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from random import Random
from typing import Iterable, List

from .models import ReadingBatch, SensorReading


@dataclass
class ScenarioSimulator:
    """
    Very small simulation that perturbs expected values.
    
    This simulator generates synthetic sensor readings by adding noise
    to expected values. Supports both uniform and Gaussian noise distributions.
    
    Attributes:
        seed: Random seed for reproducibility
        jitter: Magnitude of noise to add (for uniform) or standard deviation (for Gaussian)
        noise_type: Type of noise distribution ("uniform" or "gaussian")
    """

    seed: int = 42
    jitter: float = 0.5
    noise_type: str = "uniform"  # "uniform" or "gaussian"

    def generate(
        self,
        sensor_id: str,
        expected_value: float,
        *,
        count: int = 10,
        spacing_seconds: int = 60,
        start_time: datetime | None = None,
        drift_rate: float = 0.0,
    ) -> ReadingBatch:
        """
        Generate a batch of synthetic sensor readings.
        
        Args:
            sensor_id: Identifier for the sensor
            expected_value: Base value to perturb
            count: Number of readings to generate
            spacing_seconds: Time interval between readings
            start_time: Starting time for readings (defaults to now)
            drift_rate: Linear drift per reading (defaults to 0.0)
            
        Returns:
            ReadingBatch containing the generated readings
        """
        rng = Random(self.seed)
        readings: List[SensorReading] = []
        base_time = start_time if start_time is not None else datetime.utcnow()
        for index in range(count):
            if self.noise_type == "gaussian":
                delta = rng.gauss(0, self.jitter / 2)
            else:  # uniform
                delta = rng.uniform(-self.jitter, self.jitter)
            drift = drift_rate * index
            value = expected_value + delta + drift
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
