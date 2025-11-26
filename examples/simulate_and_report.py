"""Run a simulation then print a report."""

from __future__ import annotations

from solid_engine.metrics import ReliabilityMetrics
from solid_engine.simulation import ScenarioSimulator


def main() -> None:
    simulator = ScenarioSimulator(seed=99)
    batch = simulator.generate(sensor_id="demo", expected_value=12.0, count=8)
    metrics = ReliabilityMetrics.from_readings(batch.readings)
    print("Demo batch metrics:", metrics.to_dict())


if __name__ == "__main__":
    main()
