"""Configuration file loading for Solid Engine."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@dataclass
class Config:
    """Configuration settings for Solid Engine."""

    outlier_threshold: float = 5.0
    simulation_seed: int = 42
    simulation_jitter: float = 0.5
    default_dataset: str = "data/sample_readings.csv"

    @classmethod
    def from_file(cls, path: Path) -> "Config":
        """Load configuration from YAML file."""
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML is required for configuration file support")
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            data: dict[str, Any] = yaml.safe_load(f) or {}
        thresholds = data.get("thresholds", {})
        simulation = data.get("simulation", {})
        cli = data.get("CLI", {})
        return cls(
            outlier_threshold=thresholds.get("outlier", 5.0),
            simulation_seed=simulation.get("seed", 42),
            simulation_jitter=simulation.get("jitter", 0.5),
            default_dataset=cli.get("default_dataset", "data/sample_readings.csv"),
        )

    @classmethod
    def default(cls) -> "Config":
        """Return default configuration."""
        return cls()

