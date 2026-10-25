# PETE Python Log Reader

A well log interpretation tool: reads LAS well logs, computes shale volume,
porosity and water saturation, flags pay zones and estimates oil in place.

Status: reads and plots logs, computes shale volume, porosity and water saturation,
flags pay zones, and estimates oil in place (OOIP).

## Method

- Pay cutoffs: shale volume ≤ 0.4, porosity ≥ 0.08, water saturation ≤ 0.5
  (typical values for a conventional sandstone).
- Missing data is never counted as pay. Affected depths are listed in the output.
- Average water saturation over the pay is weighted by pore volume.
- OOIP = 7758 × A × h × φ × (1 − Sw) / Bo. Drainage area (A) and Bo are not in
  the log, so they are assumed values.

## Setup (Ubuntu / WSL)

```bash
python3 -m venv ~/.venvs/well-log
source ~/.venvs/well-log/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The log plot is saved to `output/raw_logs.png`.

## Data

`data/sample.las` is a small synthetic well for testing, not real data.
