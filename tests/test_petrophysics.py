import numpy as np
import pytest

from welllog.petrophysics import archie_sw, density_porosity, pay_flag, shale_volume


def test_shale_volume_linear_and_clipped():
    gr = np.array([10, 20, 70, 120, 200])
    vsh = shale_volume(gr, gr_clean=20, gr_shale=120)
    assert vsh == pytest.approx([0, 0, 0.5, 1, 1])


def test_density_porosity_sandstone():
    # (2.65 - 2.32) / (2.65 - 1.0) = 0.20
    assert density_porosity(2.32, 2.65, 1.0) == pytest.approx(0.20)


def test_density_porosity_clipped():
    phi = density_porosity(np.array([2.80, 0.5]), 2.65, 1.0)
    assert phi == pytest.approx([0, 1])


def test_archie_sw_hand_calculation():
    # Sw = sqrt(0.05 / (0.2^2 * 20)) = sqrt(0.0625) = 0.25
    assert archie_sw(rt=20, phi=0.2, rw=0.05) == pytest.approx(0.25)


def test_archie_sw_clipped_at_one():
    assert archie_sw(rt=0.5, phi=0.05, rw=0.1) == pytest.approx(1.0)


def test_pay_flag_cutoffs_are_inclusive():
    flag = pay_flag(np.array([0.4, 0.41]), np.array([0.08, 0.2]), np.array([0.5, 0.2]),
                    vsh_max=0.4, phi_min=0.08, sw_max=0.5)
    assert flag.tolist() == [True, False]


def test_pay_flag_missing_data_is_never_pay():
    nan = np.nan
    flag = pay_flag(np.array([nan, 0.1, 0.1]), np.array([0.2, nan, 0.2]), np.array([0.2, 0.2, nan]),
                    vsh_max=0.4, phi_min=0.08, sw_max=0.5)
    assert not flag.any()
