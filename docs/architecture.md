# Architecture overview

The Solid Engine project intentionally keeps a tiny footprint. The modules are
organised as follows:

- `models.py` contains dataclasses shared by the rest of the package.
- `metrics.py` offers a pure function-style API for computing stats.
- `simulation.py` creates synthetic readings to aid demos.
- `report.py` converts batches of readings into human-readable lines.
- `cli.py` wires the modules together using Click.

No persistence layer or background workers exist; everything happens in memory
so that contributors can reason about behaviour quickly.
