import numpy as np
import pytest

from welllog.volumetrics import net_pay_summary, ooip


def test_net_pay_summary():
    depth = np.arange(5000, 5005, 0.5)          # 10 samples, 0.5 ft step
    pay = np.array([0, 1, 1, 1, 1, 0, 0, 0, 0, 0], dtype=bool)
    phi = np.array([0.05, 0.10, 0.20, 0.10, 0.20, 0, 0, 0, 0, 0])
    sw = np.array([0.9, 0.40, 0.25, 0.40, 0.25, 1, 1, 1, 1, 1])
    s = net_pay_summary(depth, pay, phi, sw)

    assert s["gross_ft"] == pytest.approx(5.0)
    assert s["net_pay_ft"] == pytest.approx(2.0)
    assert s["net_to_gross"] == pytest.approx(0.4)
    assert s["avg_phi"] == pytest.approx(0.15)
    # Pore-volume weighted: (0.1*0.4*2 + 0.2*0.25*2) / (0.6) = 0.30, not the plain mean 0.325
    assert s["avg_sw"] == pytest.approx(0.30)


def test_net_pay_summary_no_pay():
    depth = np.arange(0, 3, 1.0)
    s = net_pay_summary(depth, np.zeros(3, bool), np.full(3, 0.1), np.full(3, 0.3))
    assert s["net_pay_ft"] == 0
    assert np.isnan(s["avg_phi"]) and np.isnan(s["avg_sw"])


def test_ooip_hand_calculation():
    # 7758 * 40 * 10 * 0.2 * 0.7 / 1.2 = 362,040 STB
    assert ooip(40, 10, 0.2, 0.3, 1.2) == pytest.approx(362_040)
