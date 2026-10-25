"""Volumetrics: summarize pay over a well and estimate oil in place."""

import numpy as np

BBL_PER_ACRE_FT = 7758  # barrels in one acre-foot of space


def net_pay_summary(depth, pay, phi, sw):
    """Summarize the pay interval of a well.

    depth : depth column (ft), evenly sampled
    pay   : pay flag column (True/False), e.g. from petrophysics.pay_flag
    phi   : porosity column (fraction)
    sw    : water saturation column (fraction)

    Each sample stands for one depth step of rock. Returns a dict with:
    gross_ft       : thickness of the whole logged interval
    net_pay_ft     : thickness that passes the pay cutoffs
    net_to_gross   : net pay / gross
    avg_phi        : average porosity over the pay
    avg_sw         : average water saturation over the pay, weighted by pore
                     volume (a high-porosity foot holds more fluid, so it counts more)
    """
    depth = np.asarray(depth, dtype=float)
    pay = np.asarray(pay, dtype=bool)
    phi = np.asarray(phi, dtype=float)[pay]
    sw = np.asarray(sw, dtype=float)[pay]

    step = np.median(np.diff(depth))
    gross = len(depth) * step
    net = pay.sum() * step

    return {
        "gross_ft": gross,
        "net_pay_ft": net,
        "net_to_gross": net / gross,
        "avg_phi": phi.mean() if net else np.nan,
        "avg_sw": (phi * sw).sum() / phi.sum() if net else np.nan,
    }


def ooip(area_acres, net_pay_ft, phi, sw, bo):
    """Original oil in place (stock tank barrels), volumetric method.

    area_acres : drainage area of the well (acres)
    net_pay_ft : net pay thickness (ft)
    phi        : average porosity over the pay (fraction)
    sw         : average water saturation over the pay (fraction)
    bo         : oil formation volume factor (reservoir bbl per stock tank bbl);
                 oil shrinks as gas comes out of it at the surface
    """
    return BBL_PER_ACRE_FT * area_acres * net_pay_ft * phi * (1 - sw) / bo
