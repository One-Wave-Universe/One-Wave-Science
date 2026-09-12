"""G-765: run G-739's six-gate extractor against a numerically integrated
trajectory of G-764's exact test-bench equation, and cross-check G-764's
derived thresholds/criteria against the trajectory.

This is the Yellow-to-Bronze promotion test G-764 sets up but does not
perform. Run with: python3 g765_validate_g764.py
Writes a JSON receipt of the actual (not hand-picked) result next to this
file.
"""

import os
import json
from collections import Counter

import numpy as np

from six_gate_extractor import extract_six_gates

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- G-764's equation and its own derived structural constants ----
# ddot(x) + gamma*dot(x) + a*x^3 - b*x - h(t) = 0,  V(x;h) = a/4 x^4 - b/2 x^2 - h x
a = 1.0
b = 1.0
gamma = 1.0  # = 2*zeta*omega0; chosen only for a clean settle, not derived by G-764

x_pm = np.sqrt(b / a)                      # G-764 Sec.2: unbiased well location
x_star = np.sqrt(b / (3 * a))              # G-764 Sec.4: bias-independent inflection
h_c = np.sqrt(4 * b**3 / (27 * a))         # G-764 Sec.5: hysteresis/bifurcation field
omega_well_h0 = np.sqrt(2 * b)             # G-764 Sec.8: ringdown freq, derived AT h=0

EPS = 1e-9


def V(x, h):
    return a / 4 * x**4 - b / 2 * x**2 - h * x


def dVdx(x, h):
    return a * x**3 - b * x - h


def sig(z):
    return 0.5 * (1 + np.tanh(z))


# Smooth (tanh-ramped, not a literal mathematical step) bias program that
# drives the equation through the full Begin->Build->Hold->Build->Break->Loop
# cycle: hold near +well under a sub-critical bias, then reverse hard past
# h_c to force an escape into the -well.
TAU = 0.2
H_HOLD = 0.3   # |H_HOLD| < h_c
H_ESC = 1.2    # |H_ESC| > h_c


def h_of_t(t):
    return (
        H_HOLD
        + (-H_ESC - H_HOLD) * sig((t - 15.0) / TAU)
        + (-H_HOLD - (-H_ESC)) * sig((t - 17.0) / TAU)
    )


def integrate():
    dt = 0.005
    T = 40.0
    n = int(T / dt) + 1
    t = np.linspace(0, T, n)
    x = np.zeros(n)
    v = np.zeros(n)
    x[0] = 0.02  # tiny perturbation off the Ground saddle (Sec.3: Ground is unstable)

    def accel(xi, vi, hi):
        return -gamma * vi - dVdx(xi, hi)

    for i in range(n - 1):
        hi = h_of_t(t[i])
        k1x = v[i]
        k1v = accel(x[i], v[i], hi)
        k2x = v[i] + dt / 2 * k1v
        k2v = accel(x[i] + dt / 2 * k1x, v[i] + dt / 2 * k1v, hi)
        k3x = v[i] + dt / 2 * k2v
        k3v = accel(x[i] + dt / 2 * k2x, v[i] + dt / 2 * k2v, hi)
        k4x = v[i] + dt * k3v
        k4v = accel(x[i] + dt * k3x, v[i] + dt * k3v, hi)
        x[i + 1] = x[i] + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        v[i + 1] = v[i] + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)

    return t, x, v, dt


def main():
    t, x, v, dt = integrate()
    h_arr = np.array([h_of_t(ti) for ti in t])

    S = -V(x, h_arr)                    # "stored/commitment" ledger fed as E_i (0 at Ground)
    E_mech = 0.5 * v**2 + V(x, h_arr)   # mechanical energy, for the Sec.7 capture criterion
    P_drive = v * h_arr
    P_damp = gamma * v**2
    heat = P_damp
    coherence = np.clip(
        np.clip(P_drive, 0, None) / (np.clip(P_drive, 0, None) + P_damp + EPS), 0, 1
    )

    # Thresholds: derived from G-764's own constants wherever G-764 derives one;
    # everything else is a declared, non-cherry-picked modeling choice.
    center_band = x_star  # G-764 Sec.4/9: "center residence" == |x| < x*
    # boundary is a structural runaway limit in G-739's extractor, NOT the same
    # thing as G-764's commitment threshold x_pm: a *biased* well's rest point
    # can sit past the unbiased x_pm, so reusing x_pm here falsely flags stable
    # committed rest as a boundary-excursion "Break". This was found by running
    # this script (first pass used boundary=x_pm) and is corrected here by
    # setting the limit safely beyond any biased rest point this program reaches.
    boundary = 2.0
    begin_energy_max = 0.1 * (b**2 / (4 * a))  # 10% of the zero-bias well depth
    hold_energy_min = 0.5 * (b**2 / (4 * a))   # 50% of the zero-bias well depth
    speed_tol = 0.05
    energy_rate_tol = 0.05
    break_rate_min = 1.0
    # NOTE: coherent-vs-unstable Build is G-739 machinery, not one of UPDATED_43's
    # six required outputs (center residence, crossing direction, partial/full
    # excursion, hysteresis, return, phase) and G-764 does not derive what
    # "coherence" or "heat" mean for this equation. coherence/heat above are this
    # script's own proxy (drive power vs damping power), and coherence_min/heat_max
    # below are a declared, un-derived modeling choice, not tuned per-outcome.
    coherence_min = 0.5
    heat_max = 0.35

    receipts = extract_six_gates(
        t, x, v, S, coherence, heat,
        center_band=center_band, speed_tol=speed_tol,
        begin_energy_max=begin_energy_max, hold_energy_min=hold_energy_min,
        energy_rate_tol=energy_rate_tol, break_rate_min=break_rate_min,
        coherence_min=coherence_min, heat_max=heat_max, boundary=boundary,
    )
    gates = [r.gate.value for r in receipts]

    collapsed = []
    for g in gates:
        if not collapsed or collapsed[-1] != g:
            collapsed.append(g)
    collapsed_no_unclassified = [g for g in collapsed if g != "Unclassified"]

    # Independent ground truth: raw x=0 crossing time after the forced escape.
    seg = np.where(t >= 15.0)[0]
    xs = x[seg]
    crossing_t = None
    for k in range(1, len(xs)):
        if xs[k - 1] * xs[k] < 0:
            crossing_t = float(t[seg[k]])
            break
    loop_t = next((float(t[i]) for i, r in enumerate(receipts) if r.gate.value == "Loop"), None)

    # Capture criterion (Sec.7) at fixed h vs after h itself changes.
    def barrier_at(i):
        return V(x_star if x[i] > 0 else -x_star, h_arr[i])

    i_hold = int(round(10.0 / dt))
    i_after_flip = int(round(16.5 / dt))
    captured_during_hold = bool(E_mech[i_hold] < barrier_at(i_hold))
    captured_after_bias_flip = bool(E_mech[i_after_flip] < barrier_at(i_after_flip))

    # Ringdown frequency: measured vs the h=0 formula vs the bias-generalized formula.
    tail = t >= 30.0
    vt, tt = v[tail], t[tail]
    sgn = np.sign(vt)
    crossings = tt[1:][(sgn[1:] * sgn[:-1] < 0)]
    measured_omega = None
    if len(crossings) >= 2:
        periods = np.diff(crossings) * 2
        measured_omega = float(2 * np.pi / np.mean(periods))

    x_well_final = float(x[tail].mean())
    Vpp_biased = 3 * a * x_well_final**2 - b
    omega_generalized = float(np.sqrt(max(Vpp_biased - (gamma / 2) ** 2, 0.0)))

    result = {
        "constants": {
            "x_pm": x_pm, "x_star": x_star, "h_c": h_c,
            "omega_well_h0_formula": omega_well_h0,
        },
        "thresholds": {
            "center_band": center_band, "boundary": boundary,
            "begin_energy_max": begin_energy_max, "hold_energy_min": hold_energy_min,
            "speed_tol": speed_tol, "energy_rate_tol": energy_rate_tol,
            "break_rate_min": break_rate_min, "coherence_min": coherence_min,
            "heat_max": heat_max,
        },
        "collapsed_gate_sequence": collapsed_no_unclassified,
        "raw_gate_counts": dict(Counter(gates)),
        "crossing_time_ground_truth": crossing_t,
        "loop_gate_detected_time": loop_t,
        "capture_criterion": {
            "captured_during_hold_t10": captured_during_hold,
            "captured_after_bias_flip_t16_5": captured_after_bias_flip,
            "note": "Sec.7's capture criterion assumes fixed h; once h(t) itself "
                    "changes the barrier V(x*;h) moves, so a previously-captured "
                    "trajectory can become uncaptured without new energy input.",
        },
        "ringdown_frequency": {
            "measured": measured_omega,
            "h0_formula_sqrt_2b": omega_well_h0,
            "bias_generalized_formula": omega_generalized,
            "x_well_final": x_well_final,
            "note": "sqrt(2b) is derived at the unbiased well x_pm. For a biased "
                    "well the rest point shifts, so the correct ringdown formula "
                    "is sqrt(V''(x_well(h)) - (gamma/2)^2), i.e. curvature at the "
                    "ACTUAL (bias-shifted) minimum with the standard damped-"
                    "oscillator correction.",
        },
    }

    with open(os.path.join(HERE, "g765_validation_receipt.json"), "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
