.PHONY: install test lint sample example

install:
	python -m venv .venv && . .venv/bin/activate && pip install -e .[dev]

test:
	pytest -q

sample:
	solid-engine report --data data/sample_readings.csv

example:
	python examples/simulate_and_report.py
