"""Extract six recursive stability gates from measured trajectories."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np


class Gate(str, Enum):
    BEGIN = "Begin"
    COHERENT_BUILD = "Coherent Build"
    HOLD = "Hold"
    UNSTABLE_BUILD = "Unstable Build"
    BREAK = "Break"
    LOOP = "Loop"
    UNCLASSIFIED = "Unclassified"


@dataclass(frozen=True)
class GateReceipt:
    index: int
    time: float
    gate: Gate
    energy_rate: float
    center_crossing: bool
    outward: bool


def extract_six_gates(
    time,
    x,
    v,
    energy,
    coherence,
    heat,
    *,
    center_band: float,
    speed_tol: float,
    begin_energy_max: float,
    hold_energy_min: float,
    energy_rate_tol: float,
    break_rate_min: float,
    coherence_min: float,
    heat_max: float,
    boundary: float,
) -> tuple[GateReceipt, ...]:
    arrays = [np.asarray(a, dtype=float) for a in (time, x, v, energy, coherence, heat)]
    time, x, v, energy, coherence, heat = arrays
    if any(a.ndim != 1 or a.shape != time.shape for a in arrays):
        raise ValueError("all trajectory inputs must be equal-length one-dimensional arrays")
    if time.size < 2 or not all(np.isfinite(a).all() for a in arrays):
        raise ValueError("trajectory must contain at least two finite samples")
    if not np.all(np.diff(time) > 0):
        raise ValueError("time must be strictly increasing")
    if np.any((coherence < 0) | (coherence > 1)) or np.any(heat < 0):
        raise ValueError("coherence must be in [0,1] and heat must be nonnegative")
    if not (0 <= center_band < boundary and speed_tol >= 0 and energy_rate_tol >= 0
            and break_rate_min > energy_rate_tol and 0 <= coherence_min <= 1
            and heat_max >= 0):
        raise ValueError("invalid gate thresholds")

    rates = np.empty_like(energy)
    rates[0] = 0.0
    rates[1:] = np.diff(energy) / np.diff(time)
    receipts = []
    break_seen = False

    for i in range(time.size):
        crossing = i > 0 and x[i - 1] * x[i] < 0
        outward = x[i] * v[i] > 0
        low_motion = abs(v[i]) <= speed_tol
        at_center = abs(x[i]) <= center_band

        if crossing and break_seen:
            gate = Gate.LOOP
            break_seen = False
        elif rates[i] <= -break_rate_min or (abs(x[i]) >= boundary and outward):
            gate = Gate.BREAK
            break_seen = True
        elif (
            at_center
            and low_motion
            and energy[i] <= begin_energy_max
            and abs(rates[i]) <= energy_rate_tol
        ):
            gate = Gate.BEGIN
        elif rates[i] > energy_rate_tol and coherence[i] >= coherence_min and heat[i] <= heat_max:
            gate = Gate.COHERENT_BUILD
        elif rates[i] > energy_rate_tol and (coherence[i] < coherence_min or heat[i] > heat_max):
            gate = Gate.UNSTABLE_BUILD
        elif abs(rates[i]) <= energy_rate_tol and low_motion and energy[i] >= hold_energy_min:
            gate = Gate.HOLD
        else:
            gate = Gate.UNCLASSIFIED

        receipts.append(GateReceipt(
            index=i,
            time=float(time[i]),
            gate=gate,
            energy_rate=float(rates[i]),
            center_crossing=bool(crossing),
            outward=bool(outward),
        ))

    return tuple(receipts)
