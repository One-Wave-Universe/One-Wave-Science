"""G-745 unit conversion for a zone-edge a0 candidate.

This is NOT a derivation of the lattice constant.
"""

from __future__ import annotations

import math
from typing import Dict

HBAR_C_MEV_FM = 197.3269804
E125_MEV = 125_000.0
FM_TO_M = 1.0e-15


def compton_like_length_fm(energy_mev: float) -> float:
    if energy_mev <= 0:
        raise ValueError("energy must be positive")
    return HBAR_C_MEV_FM / energy_mev


def zone_edge_a0_m(energy_mev: float = E125_MEV, c_eff_over_c: float = 1.0) -> float:
    if c_eff_over_c <= 0:
        raise ValueError("c_eff/c must be positive")
    return math.pi * compton_like_length_fm(energy_mev) * FM_TO_M * c_eff_over_c


def receipt(energy_mev: float = E125_MEV, c_eff_over_c: float = 1.0) -> Dict[str, object]:
    a0 = zone_edge_a0_m(energy_mev, c_eff_over_c)
    return {
        "brick": "Yellow",
        "derived": False,
        "assumptions": ("A1_energy_is_zone_edge", "A2_kmax_pi_over_a0", "A3_vg_zero_is_condensate_break", "A4_c_eff_known"),
        "E_mev": energy_mev,
        "c_eff_over_c": c_eff_over_c,
        "a0_m": a0,
        "a0_fm": a0 / FM_TO_M,
        "gray_control_c_eff_is_c": c_eff_over_c == 1.0,
        "allowed_in_blind_hoyle_test": False,
    }
