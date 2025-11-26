import pytest

from solid_engine.utils import clamp


def test_clamp_limits_value() -> None:
    assert clamp(5, lower=0, upper=3) == 3
    assert clamp(-1, lower=0, upper=3) == 0
    assert clamp(2, lower=0, upper=3) == 2


def test_clamp_rejects_invalid_bounds() -> None:
    with pytest.raises(ValueError):
        clamp(1, lower=5, upper=1)
