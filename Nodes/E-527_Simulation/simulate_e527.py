#!/usr/bin/env python3
"""Reproducible validation for One-Wave node E-527.

Tests three distinct claims:
1. Product-only readout C=R*U under constant supply approaches a plateau.
2. Finite substrate without recharge creates one transient pulse, not a cycle.
3. Recharge + state-dependent depletion + hysteresis creates a repeatable
   relaxation oscillator whose period matches the analytic formula.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Parameters:
    R_star: float = 0.85
    P: float = 0.08
    loss: float = 0.10
    depletion: float = 0.60
    C_on: float = 0.55
    C_off: float = 0.25
    U0: float = 0.30
    dt: float = 0.001
    t_end: float = 90.0


def write_csv(path: Path, header: list[str], rows) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def case_constant_supply(p: Parameters):
    t = np.arange(0.0, 60.0 + p.dt, p.dt)
    U_eq = p.P / p.loss
    U = U_eq + (p.U0 - U_eq) * np.exp(-p.loss * t)
    C = p.R_star * U
    return t, U, C, U_eq


def case_finite_substrate(p: Parameters):
    # One finite reservoir. No recharge. Exact solution.
    kp = 0.25
    S0 = 1.0
    U0 = 0.02
    t = np.arange(0.0, 60.0 + p.dt, p.dt)
    S = S0 * np.exp(-kp * t)
    if abs(p.loss - kp) < 1e-12:
        U = np.exp(-p.loss * t) * (U0 + kp * S0 * t)
    else:
        U = U0 * np.exp(-p.loss * t) + kp * S0 * (
            np.exp(-kp * t) - np.exp(-p.loss * t)
        ) / (p.loss - kp)
    C = p.R_star * U
    return t, S, U, C, kp


def hybrid_analytic(p: Parameters):
    U_on = p.C_on / p.R_star
    U_off = p.C_off / p.R_star
    U_charge = p.P / p.loss
    U_release = p.P / (p.loss + p.depletion)

    charge_condition = U_charge > U_on
    release_condition = U_release < U_off
    if not (charge_condition and release_condition):
        return {
            "cycles": False,
            "U_on": U_on,
            "U_off": U_off,
            "U_charge_eq": U_charge,
            "U_release_eq": U_release,
            "T_charge": None,
            "T_release": None,
            "T_period": None,
        }

    T_charge = (1.0 / p.loss) * math.log(
        (U_charge - U_off) / (U_charge - U_on)
    )
    T_release = (1.0 / (p.loss + p.depletion)) * math.log(
        (U_on - U_release) / (U_off - U_release)
    )
    return {
        "cycles": True,
        "U_on": U_on,
        "U_off": U_off,
        "U_charge_eq": U_charge,
        "U_release_eq": U_release,
        "T_charge": T_charge,
        "T_release": T_release,
        "T_period": T_charge + T_release,
    }


def case_hybrid(p: Parameters):
    steps = int(round(p.t_end / p.dt)) + 1
    t = np.linspace(0.0, p.t_end, steps)
    U = np.empty(steps)
    C = np.empty(steps)
    h = np.empty(steps, dtype=int)
    U[0] = p.U0
    C[0] = p.R_star * U[0]
    h[0] = 0
    on_events: list[float] = []
    off_events: list[float] = []

    mode = 0
    for i in range(1, steps):
        rate = p.loss + p.depletion * mode
        U_eq = p.P / rate
        U[i] = U_eq + (U[i - 1] - U_eq) * math.exp(-rate * p.dt)
        C[i] = p.R_star * U[i]

        if mode == 0 and C[i] >= p.C_on:
            mode = 1
            on_events.append(t[i])
        elif mode == 1 and C[i] <= p.C_off:
            mode = 0
            off_events.append(t[i])
        h[i] = mode

    return t, U, C, h, on_events, off_events


def local_maxima_count(y: np.ndarray) -> int:
    d = np.diff(y)
    return int(np.sum((d[:-1] > 0) & (d[1:] <= 0)))


def plot_line(path: Path, x, series, title: str, xlabel: str, ylabel: str):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for y, label in series:
        ax.plot(x, y, label=label)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    if len(series) > 1:
        ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main() -> None:
    p = Parameters()

    # Case 1: plateau.
    t1, U1, C1, Ueq1 = case_constant_supply(p)
    write_csv(HERE / "case_1_constant_supply_plateau.csv", ["time", "U", "C"], zip(t1, U1, C1))
    plot_line(
        HERE / "case_1_constant_supply_plateau.png",
        t1,
        [(U1, "resource U"), (C1, "readout C=R*U")],
        "E-527 Case 1: constant supply approaches a plateau",
        "time",
        "normalized value",
    )

    # Case 2: one pulse.
    t2, S2, U2, C2, kp = case_finite_substrate(p)
    write_csv(HERE / "case_2_finite_substrate_single_pulse.csv", ["time", "S", "U", "C"], zip(t2, S2, U2, C2))
    plot_line(
        HERE / "case_2_finite_substrate_single_pulse.png",
        t2,
        [(S2, "finite substrate S"), (U2, "resource U"), (C2, "readout C=R*U")],
        "E-527 Case 2: finite substrate creates one pulse, not a cycle",
        "time",
        "normalized value",
    )

    # Case 3: hybrid relaxation oscillator.
    analytic = hybrid_analytic(p)
    t3, U3, C3, h3, on_events, off_events = case_hybrid(p)
    write_csv(HERE / "case_3_hybrid_relaxation_cycle.csv", ["time", "U", "C", "release_state"], zip(t3, U3, C3, h3))
    write_csv(
        HERE / "case_3_switch_events.csv",
        ["event", "time"],
        [("release_on", x) for x in on_events] + [("release_off", x) for x in off_events],
    )
    plot_line(
        HERE / "case_3_hybrid_relaxation_cycle.png",
        t3,
        [(U3, "resource U"), (C3, "readout C=R*U"), (h3.astype(float), "release state h")],
        "E-527 Case 3: recharge, depletion, and hysteresis produce cycles",
        "time",
        "normalized value",
    )

    periods = np.diff(np.asarray(on_events)) if len(on_events) > 1 else np.array([])
    numerical_period = float(np.mean(periods[1:])) if len(periods) > 2 else (float(np.mean(periods)) if len(periods) else None)
    period_error_pct = None
    if numerical_period is not None and analytic["T_period"] is not None:
        period_error_pct = 100.0 * abs(numerical_period - analytic["T_period"]) / analytic["T_period"]

    # Parameter sweep over R* and depletion D using the analytic inequalities.
    sweep_rows = []
    R_values = np.linspace(0.50, 1.00, 101)
    D_values = np.linspace(0.05, 1.00, 96)
    cycle_map = np.zeros((len(D_values), len(R_values)))
    period_map = np.full((len(D_values), len(R_values)), np.nan)
    for di, D in enumerate(D_values):
        for ri, R in enumerate(R_values):
            q = Parameters(R_star=float(R), depletion=float(D))
            a = hybrid_analytic(q)
            cycle = int(a["cycles"])
            cycle_map[di, ri] = cycle
            if cycle:
                period_map[di, ri] = a["T_period"]
            sweep_rows.append((R, D, cycle, a["T_period"] if cycle else ""))
    write_csv(HERE / "parameter_sweep.csv", ["R_star", "depletion_D", "cycles", "analytic_period"], sweep_rows)

    fig, ax = plt.subplots(figsize=(9, 6))
    im = ax.imshow(
        cycle_map,
        origin="lower",
        aspect="auto",
        extent=[R_values[0], R_values[-1], D_values[0], D_values[-1]],
        interpolation="nearest",
    )
    ax.set_title("E-527 analytic cycle region")
    ax.set_xlabel("settled synchronization R*")
    ax.set_ylabel("state-dependent depletion D")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("0 = no cycle, 1 = cycle")
    fig.tight_layout()
    fig.savefig(HERE / "parameter_sweep_cycle_region.png", dpi=180)
    plt.close(fig)

    # Validation assertions.
    plateau_monotonic = bool(np.all(np.diff(C1) >= -1e-12))
    plateau_error = float(abs(U1[-1] - Ueq1))
    pulse_count = local_maxima_count(C2)
    cycle_count = len(on_events)
    hybrid_bounded = bool(np.all(U3 >= -1e-12) and np.all(C3 >= -1e-12))
    period_match = period_error_pct is not None and period_error_pct < 0.5

    assert plateau_monotonic, "Constant-supply product should rise monotonically."
    assert plateau_error < 0.01, "Constant-supply case did not approach equilibrium."
    assert pulse_count == 1, f"Finite substrate should yield one pulse; got {pulse_count}."
    assert cycle_count >= 5, f"Hybrid model should yield repeated cycles; got {cycle_count}."
    assert hybrid_bounded, "Hybrid model produced an invalid negative state."
    assert period_match, f"Numerical period differs from analytic by {period_error_pct:.3f}%."

    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    summary = {
        "node": "E-527",
        "status_result": "BRONZE validation of reduced hybrid model",
        "timestamp_note": "Generated during repository update; no external data used.",
        "software": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "script_sha256": script_hash,
        "parameters": asdict(p),
        "case_1": {
            "claim": "C=R*U with constant supply approaches a plateau and does not cycle.",
            "plateau_monotonic": plateau_monotonic,
            "U_equilibrium": Ueq1,
            "U_final": float(U1[-1]),
            "absolute_equilibrium_error": plateau_error,
        },
        "case_2": {
            "claim": "Finite substrate without recharge creates one transient pulse, not repeated oscillation.",
            "substrate_decay_rate": kp,
            "pulse_count": pulse_count,
            "peak_time": float(t2[int(np.argmax(C2))]),
            "peak_C": float(np.max(C2)),
        },
        "case_3": {
            "claim": "Recharge plus state-dependent depletion and hysteresis creates a stable relaxation cycle.",
            "analytic": analytic,
            "release_on_events": on_events,
            "release_off_events": off_events,
            "cycle_count": cycle_count,
            "numerical_period": numerical_period,
            "period_error_percent": period_error_pct,
            "validation_period_error_below_0_5_percent": period_match,
        },
        "scope_limits": [
            "R* is a settled synchronization input, not a full simulated Kuramoto lattice.",
            "The model validates internal dynamics only, not a specific biological event.",
            "Thresholds and parameter values are normalized test values, not measured constants.",
        ],
    }
    (HERE / "simulation_metadata.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
