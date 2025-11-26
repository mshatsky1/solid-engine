# Usage guide

1. Create a virtual environment and install Solid Engine in editable mode.
2. Run `solid-engine simulate --sensor sensor-123` to produce synthetic data.
3. Inspect `data/sample_readings.csv` or your own CSV and run
   `solid-engine report --data path/to/file.csv --json` for structured output
   or omit the flag for plain text.

The CLI exposes JSON-like metrics for simulations and text tables for reports.
Use the docs in `config/` to tweak defaults.
