"""
Energy accounting for this batch's DC-only scope: a resistive network under
a constant DC source has constant power, so energy over a run duration is
simply power * time. (Time-varying energy integration -- for when
capacitors/inductors arrive in a later batch -- is explicitly out of scope
here; see Virtual_Breadboard/simulate.js's integrateEnergy for the
trapezoidal version this will eventually need to match in spirit.)
"""
from __future__ import annotations


def energy_from_power(power_watts: float, duration_seconds: float) -> float:
    """E = P * t, in joules."""
    if duration_seconds < 0:
        raise ValueError(f"duration_seconds must be >= 0, got {duration_seconds!r}")
    return power_watts * duration_seconds


def energy_balance(supplied_joules: float, dissipated_joules: float) -> dict:
    """No unexplained energy gain or loss: real supplied energy must equal
    real dissipated energy for a pure resistive DC network (nothing stores
    or generates energy in this batch's component set). Returns the
    absolute and relative mismatch so a caller can apply its own
    tolerance -- this function does not itself decide pass/fail."""
    mismatch = supplied_joules - dissipated_joules
    denom = max(abs(supplied_joules), 1e-15)
    return {
        "supplied_joules": supplied_joules,
        "dissipated_joules": dissipated_joules,
        "mismatch_joules": mismatch,
        "relative_mismatch": mismatch / denom,
    }
