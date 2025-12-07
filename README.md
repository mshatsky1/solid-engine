# Solid Engine

Solid Engine is a lightweight Python toolkit for simulating the reliability of
sensor readings and summarising results for small engineering teams. The goal is
to keep the codebase simple and approachable while showcasing incremental
commits.

## Project goals
- Offer a reproducible workflow for experimenting with toy reliability models
- Provide a CLI to inspect sample data and reports
- Document design trade-offs for future contributors

## Getting started
```
python -m venv .venv
source .venv/bin/activate
pip install -e .
solid-engine --help
```

## Features
- Generate reliability reports from CSV data
- Simulate sensor readings with configurable noise
- Calculate metrics including outlier detection
- Export reports in JSON or text format
- Verbose output mode for debugging
- Comprehensive validation and error handling

## Status
Early experiment. Expect frequent, small commits.
