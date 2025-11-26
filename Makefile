.PHONY: install test lint sample

install:
	python -m venv .venv && . .venv/bin/activate && pip install -e .[dev]

test:
	pytest -q

sample:
	solid-engine report --data data/sample_readings.csv
