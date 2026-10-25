"""Well log interpretation tool - main script.

Run from the project folder with:  python main.py
"""

from pathlib import Path

import lasio
import matplotlib.pyplot as plt

from welllog.petrophysics import archie_sw, density_porosity, shale_volume
from welllog.plotting import plot_logs

ROOT = Path(__file__).parent
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

# 1. Load a well
las = lasio.read(ROOT / "data" / "sample.las")
data = las.df().reset_index()  # depth becomes a normal column
units = {curve.mnemonic: curve.unit for curve in las.curves}

print(las.well)
print(data.head())

# 2. Quick look at the raw logs
fig = plot_logs(data, ["GR", "RHOB", "NPHI", "RT"], units=units, title=las.well.WELL.value)
fig.savefig(OUTPUT / "raw_logs.png", dpi=150)
print(f"Saved {OUTPUT / 'raw_logs.png'}")

# 3. Petrophysics
data["VSH"] = shale_volume(data["GR"], gr_clean=25, gr_shale=110)
data["PHI"] = density_porosity(data["RHOB"], rho_matrix=2.65, rho_fluid=1.0)
data["SW"] = archie_sw(data["RT"], data["PHI"], rw=0.05)

print(data[["DEPT", "VSH", "PHI", "SW"]].round(2).to_string(index=False))

fig = plot_logs(data, ["GR", "VSH", "PHI", "SW"], units=units, title=las.well.WELL.value)
fig.savefig(OUTPUT / "petrophysics.png", dpi=150)
print(f"Saved {OUTPUT / 'petrophysics.png'}")

plt.show()
