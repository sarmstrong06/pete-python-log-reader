# PETE Python Log Reader

A well log interpretation tool: reads LAS well logs, computes shale volume,
porosity and water saturation, flags pay zones and estimates oil in place.

Status: reads and plots raw logs. Petrophysical calculations are in progress.

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
