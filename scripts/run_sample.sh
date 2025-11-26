#!/usr/bin/env bash
set -euo pipefail

python -m solid_engine.cli report --data data/sample_readings.csv
