"""Well log interpretation tool - main script.

Run from the project folder with:  python main.py
"""

from pathlib import Path

import lasio
import matplotlib.pyplot as plt

from welllog.petrophysics import archie_sw, density_porosity, pay_flag, shale_volume
from welllog.plotting import plot_logs
from welllog.volumetrics import net_pay_summary, ooip

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

# 4. Pay zones
# Starting cutoffs - typical values for a conventional sandstone, still to be chosen
data["PAY"] = pay_flag(data["VSH"], data["PHI"], data["SW"],
                       vsh_max=0.4, phi_min=0.08, sw_max=0.5)
summary = net_pay_summary(data["DEPT"], data["PAY"], data["PHI"], data["SW"])

print(data.loc[data["PAY"], ["DEPT", "VSH", "PHI", "SW"]].round(2).to_string(index=False))
print(f"Gross interval : {summary['gross_ft']:.1f} ft")
print(f"Net pay        : {summary['net_pay_ft']:.1f} ft "
      f"(net-to-gross {summary['net_to_gross']:.0%})")
print(f"Avg porosity   : {summary['avg_phi']:.1%}")
print(f"Avg water sat. : {summary['avg_sw']:.1%}")

# 5. Oil in place
# Drainage area and Bo are not in the log - assumed values for now
oil = ooip(area_acres=40, net_pay_ft=summary["net_pay_ft"],
           phi=summary["avg_phi"], sw=summary["avg_sw"], bo=1.2)
print(f"OOIP (40 acres, Bo 1.2): {oil:,.0f} STB")

plt.show()
