"""Petrophysical calculations. Each function takes log columns and returns a new column."""

import numpy as np


def shale_volume(gr, gr_clean, gr_shale):
    """Shale volume (fraction, 0 to 1) from gamma ray, linear gamma ray index method.

    gr       : gamma ray log (API units)
    gr_clean : gamma ray reading in clean sand
    gr_shale : gamma ray reading in pure shale
    """
    vsh = (gr - gr_clean) / (gr_shale - gr_clean)
    return np.clip(vsh, 0, 1)


def density_porosity(rhob, rho_matrix, rho_fluid):
    """Porosity (fraction, 0 to 1) from the bulk density log.

    rhob       : bulk density log (g/cc)
    rho_matrix : density of the rock grains (2.65 for sandstone)
    rho_fluid  : density of the fluid in the pores (1.0 for fresh water)
    """
    phi = (rho_matrix - rhob) / (rho_matrix - rho_fluid)
    return np.clip(phi, 0, 1)


def archie_sw(rt, phi, rw, a=1, m=2, n=2):
    """Water saturation (fraction, 0 to 1) from Archie's equation.

    rt  : true formation resistivity log (ohm-m)
    phi : porosity (fraction)
    rw  : formation water resistivity (ohm-m)
    a   : tortuosity factor
    m   : cementation exponent
    n   : saturation exponent
    """
    sw = ((a * rw) / (phi**m * rt)) ** (1 / n)
    return np.clip(sw, 0, 1)
