import pytest
from datetime import datetime

from solid_engine.utils import clamp, normalize, round_to_precision, format_timestamp


def test_clamp_limits_value() -> None:
    assert clamp(5, lower=0, upper=3) == 3
    assert clamp(-1, lower=0, upper=3) == 0
    assert clamp(2, lower=0, upper=3) == 2


def test_clamp_rejects_invalid_bounds() -> None:
    with pytest.raises(ValueError):
        clamp(1, lower=5, upper=1)


def test_normalize() -> None:
    assert normalize(5, min_val=0, max_val=10) == 0.5
    assert normalize(0, min_val=0, max_val=10) == 0.0
    assert normalize(10, min_val=0, max_val=10) == 1.0
    assert normalize(5, min_val=5, max_val=5) == 0.0


def test_round_to_precision() -> None:
    assert round_to_precision(3.14159, precision=2) == 3.14
    assert round_to_precision(3.14159, precision=4) == 3.1416
    assert round_to_precision(10.0, precision=2) == 10.0


def test_format_timestamp() -> None:
    dt = datetime(2025, 1, 15, 14, 30, 45)
    assert format_timestamp(dt) == "2025-01-15 14:30:45"
    assert format_timestamp(dt, format_str="%Y-%m-%d") == "2025-01-15"
