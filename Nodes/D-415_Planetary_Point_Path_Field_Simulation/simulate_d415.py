#!/usr/bin/env python3
"""D-415 Planetary Point-Path-Field Simulation.

A scoped, testable slice of UPDATED_41 (Planetary-Scale Displacement Model),
built under D-412 discipline: declared state -> update law -> measurements ->
visualization, with an independently runnable Newtonian control and an
optional post-Newtonian (1PN) control run from identical initial conditions
and integrator tolerances (spec layer 8).

Scope honestly declared (see README.md and the D-415 node doc):
  - planar (2D) projection of the Sun + five-planet system (Mercury, Venus,
    Earth, Mars, Jupiter). Real 3D inclinations are not carried; this is a
    declared A-117 projection, not the full physical geometry.
  - spin/core-differential rates are prescribed from real spin periods plus
    an illustrative core-mantle offset, not derived from an internal dynamo
    solver. They feed the candidate correction term; they are not fed back
    into the orbital solver.
  - the candidate One-Wave planetary correction (K_eff) is a small,
    ablatable, bounded multiplicative perturbation on the Sun-body term of
    Newtonian gravity. It is a stand-in for UPDATED_41 section 8's EM-shell
    law, not a derivation of it.
  - internal quantities that have no meaning for point-mass bodies (cell
    area, FCC/HCP stacking, imposed well) are declared out of scope rather
    than faked. See README.md "Explicit non-applicability".

Units: AU, year, solar mass (G = 4*pi^2).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import dataclass, asdict, field
from pathlib import Path

import numpy as np

G = 4 * math.pi ** 2          # AU^3 / (Msun * yr^2)
C_LIGHT = 63241.077            # AU / yr
CODE_VERSION = "d415-0.1"

# ---------------------------------------------------------------------------
# Declared bodies. Orbital elements, masses, and spin periods are standard
# public astronomical constants (osculating heliocentric, J2000-ish), used
# only as initial conditions -- they are not the model under test.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class BodyDecl:
    name: str
    mass: float               # solar masses
    a: float                  # AU, semi-major axis
    e: float                  # eccentricity
    spin_period_days: float   # signed; negative = retrograde
    core_offset: float        # illustrative Omega_core/Omega_body - 1 (0 = no declared dynamo asymmetry)
    has_dynamo: bool          # Earth/Mercury/Jupiter true; Venus/Mars false (explicit controls, UPDATED_41 S11)
    phase_offset: float       # rad, EM-alignment proxy phase (declared, not fit)


BODIES = [
    BodyDecl("mercury", 1.6601e-7, 0.387098, 0.205630, 58.6462, 0.00220, True, 0.0),
    BodyDecl("venus", 2.4478e-6, 0.723332, 0.006772, -243.0, 0.0, False, 0.0),
    BodyDecl("earth", 3.00347e-6, 1.000000, 0.016710, 0.99727, 0.00035, True, 1.1),
    BodyDecl("mars", 3.2271e-7, 1.523679, 0.093401, 1.02596, 0.0, False, 0.0),
    BodyDecl("jupiter", 9.5479e-4, 5.20260, 0.048498, 0.41354, 0.00090, True, 2.4),
]
N_PLANETS = len(BODIES)
N_BODIES = N_PLANETS + 1  # + Sun at index 0


@dataclass
class Params:
    dt: float = 1.0 / 4000.0        # yr
    duration: float = 30.0          # yr
    fit_fraction: float = 0.6
    sample_stride: int = 10
    seed: int = 415
    # candidate One-Wave coupling coefficients -- small, bounded, ablatable.
    eps_shear: float = 2.0e-7
    eps_em: float = 2.0e-7
    weave_coeff: float = 1.5e-7
    compress_relax: float = 6.0     # 1/yr, L2D relaxation rate
    threshold: float = 0.15         # ternary local state machine threshold on delta_C
    mercury_asymmetry: float = 1.6  # UPDATED_41 S9 C_SM extra term multiplier for Mercury only
    # ablation switches (D-412 / spec required ablations)
    use_em_shell: bool = True
    use_boundary_weave: bool = True
    use_core_differential: bool = True
    use_memory: bool = True         # False => C_i tracks target instantaneously (no relaxation lag)
    use_1pn: bool = False
    include_jupiter: bool = True
    mercury_asymmetric_coupling: bool = True
    onewave_active: bool = True     # False => pure Newtonian control (all correction terms zeroed)


def active_indices(p: Params) -> list[int]:
    idx = list(range(N_PLANETS))
    if not p.include_jupiter:
        idx = [i for i in idx if BODIES[i].name != "jupiter"]
    return idx


def initial_state(p: Params) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Perihelion initial conditions for Sun + planets, barycentric-corrected
    to zero total momentum so 'center drift' is a meaningful integrity check."""
    pos = np.zeros((N_BODIES, 2))
    vel = np.zeros((N_BODIES, 2))
    masses = np.zeros(N_BODIES)
    masses[0] = 1.0
    idx = active_indices(p)
    for i, b in enumerate(BODIES):
        bi = i + 1
        masses[bi] = b.mass if i in idx else 0.0
        # Position/velocity are always set from the real orbital elements, even for a
        # body ablated out via `include_jupiter=False`: a massless body at its normal
        # orbital radius contributes zero gravity and cannot coincide with the Sun.
        r_peri = b.a * (1 - b.e)
        v_peri = math.sqrt(G * (1.0 + b.mass) * (1 + b.e) / (b.a * (1 - b.e)))
        pos[bi] = (r_peri, 0.0)
        vel[bi] = (0.0, v_peri)
    total_p = (masses[:, None] * vel).sum(axis=0)
    vel[0] = -total_p / masses[0]
    C0 = np.zeros(N_PLANETS)
    return pos, vel, C0, masses


def gravity_accel(pos: np.ndarray, masses: np.ndarray) -> np.ndarray:
    d = pos[None, :, :] - pos[:, None, :]           # d[i,j] = r_j - r_i
    dist2 = np.sum(d * d, axis=2)
    np.fill_diagonal(dist2, 1.0)
    inv_d3 = dist2 ** -1.5
    np.fill_diagonal(inv_d3, 0.0)
    a = G * np.sum((masses[None, :, None] * inv_d3[:, :, None]) * d, axis=1)
    return a


def pn1_accel(r_vec: np.ndarray, v_vec: np.ndarray, m_sun: float) -> np.ndarray:
    """Standard isotropic-coordinates 1PN Sun-dominated correction (textbook
    Schwarzschild/EIH approximation). Reaction on the Sun itself is
    neglected, as is customary in the restricted treatment."""
    r = np.linalg.norm(r_vec)
    v2 = float(np.dot(v_vec, v_vec))
    rv = float(np.dot(r_vec, v_vec))
    gm = G * m_sun
    return (gm / (C_LIGHT ** 2 * r ** 3)) * ((4 * gm / r - v2) * r_vec + 4 * rv * v_vec)


def em_alignment(t: float, b: BodyDecl, asym_extra: float) -> float:
    """Declared periodic proxy for dipole-tilt/EM-shell orientation relative
    to the Sun-body line. Explicitly NOT a derived 3D dipole geometry (see
    module docstring) -- a bounded, reproducible, ablatable stand-in."""
    period = abs(b.spin_period_days) / 365.25
    if period <= 0:
        return 0.0
    return math.cos(2 * math.pi * t / period + b.phase_offset) + asym_extra


def k_eff(t: float, i: int, C_i: float, C0_i: float, p: Params) -> tuple[float, float, float]:
    b = BODIES[i]
    delta_omega = b.core_offset if p.use_core_differential else 0.0
    shear_term = p.eps_shear * (delta_omega ** 2) if p.use_core_differential else 0.0
    asym_extra = 0.0
    if b.name == "mercury" and p.mercury_asymmetric_coupling:
        asym_extra = 0.35 * p.mercury_asymmetry
    align = em_alignment(t, b, asym_extra) if (b.has_dynamo and p.use_em_shell) else 0.0
    em_term = p.eps_em * align
    weave_term = p.weave_coeff * (C_i - C0_i) if p.use_boundary_weave else 0.0
    m_em = 1.0 + shear_term + em_term + weave_term
    keff = m_em if p.onewave_active else 1.0
    return keff, shear_term, em_term + weave_term


def tidal_target(i: int, pos: np.ndarray, masses: np.ndarray) -> float:
    bi = i + 1
    r_sun = np.linalg.norm(pos[bi] - pos[0])
    val = masses[0] / max(r_sun, 1e-9) ** 3
    for j in range(N_PLANETS):
        if j == i:
            continue
        bj = j + 1
        if masses[bj] == 0:
            continue
        rij = np.linalg.norm(pos[bi] - pos[bj])
        val += masses[bj] / max(rij, 1e-9) ** 3
    return val


def derivatives(t: float, pos, vel, C, C0, masses, p: Params):
    a_grav = gravity_accel(pos, masses)
    a_out = a_grav.copy()
    keffs = np.ones(N_PLANETS)
    dC = np.zeros(N_PLANETS)
    for i in range(N_PLANETS):
        bi = i + 1
        if masses[bi] == 0:
            continue
        r_sun_vec = pos[bi] - pos[0]
        r_sun = np.linalg.norm(r_sun_vec)
        a_from_sun = -G * masses[0] * r_sun_vec / r_sun ** 3
        keff, _, _ = k_eff(t, i, C[i], C0[i], p)
        keffs[i] = keff
        a_out[bi] += a_from_sun * (keff - 1.0)
        if p.use_1pn:
            v_sun_vec = vel[bi] - vel[0]
            a_out[bi] += pn1_accel(r_sun_vec, v_sun_vec, masses[0])
        target = tidal_target(i, pos, masses)
        dC[i] = p.compress_relax * (target - C[i]) if p.use_memory else 0.0
    return vel.copy(), a_out, dC, keffs


def rk4_step(t, pos, vel, C, C0, masses, p: Params):
    dt = p.dt
    if not p.use_memory:
        for i in range(N_PLANETS):
            C[i] = tidal_target(i, pos, masses)

    def f(tt, pp, vv, cc):
        dv, da, dc, keffs = derivatives(tt, pp, vv, cc, C0, masses, p)
        return dv, da, dc, keffs

    k1v, k1a, k1c, keffs = f(t, pos, vel, C)
    k2v, k2a, k2c, _ = f(t + dt / 2, pos + dt / 2 * k1v, vel + dt / 2 * k1a, C + dt / 2 * k1c)
    k3v, k3a, k3c, _ = f(t + dt / 2, pos + dt / 2 * k2v, vel + dt / 2 * k2a, C + dt / 2 * k2c)
    k4v, k4a, k4c, _ = f(t + dt, pos + dt * k3v, vel + dt * k3a, C + dt * k3c)
    pos_n = pos + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
    vel_n = vel + dt / 6 * (k1a + 2 * k2a + 2 * k3a + k4a)
    C_n = C + dt / 6 * (k1c + 2 * k2c + 2 * k3c + k4c) if p.use_memory else C.copy()
    return pos_n, vel_n, C_n, keffs


def eccentricity_vector_angle(r_vec: np.ndarray, v_vec: np.ndarray, m_sun: float) -> float:
    """Instantaneous osculating longitude of periapsis, from the Laplace-
    Runge-Lenz / eccentricity vector. Exact and continuous at every sample
    (no periapsis-passage detection, no interpolation, no numerical
    differentiation -- velocity is already an RK4 state variable)."""
    mu = G * m_sun
    r = np.linalg.norm(r_vec)
    v2 = float(np.dot(v_vec, v_vec))
    rv = float(np.dot(r_vec, v_vec))
    e_vec = ((v2 - mu / r) * r_vec - rv * v_vec) / mu
    return float(math.atan2(e_vec[1], e_vec[0]))


def classify(delta: float, threshold: float) -> int:
    if delta < -threshold:
        return -1
    if delta > threshold:
        return 1
    return 0


def total_energy(pos, vel, masses) -> float:
    ke = 0.5 * np.sum(masses[:, None] * vel * vel)
    pe = 0.0
    for i in range(N_BODIES):
        for j in range(i + 1, N_BODIES):
            if masses[i] == 0 or masses[j] == 0:
                continue
            r = np.linalg.norm(pos[i] - pos[j])
            pe -= G * masses[i] * masses[j] / r
    return float(ke + pe)


def run(p: Params, out: Path, tag: str):
    pos, vel, C, masses = initial_state(p)
    C0 = C.copy()
    steps = round(p.duration / p.dt)
    rows = []
    correction_work = np.zeros(N_PLANETS)
    route_counts = {b.name: {"-1": 0, "0": 0, "1": 0} for b in BODIES}
    e0 = total_energy(pos, vel, masses)
    for step in range(steps + 1):
        t = step * p.dt
        if step % p.sample_stride == 0:
            row = {"t": t, "energy": total_energy(pos, vel, masses)}
            row["barycenter_x"] = float(np.sum(masses[:, None] * pos, axis=0)[0])
            row["barycenter_y"] = float(np.sum(masses[:, None] * pos, axis=0)[1])
            for i, b in enumerate(BODIES):
                bi = i + 1
                r_sun = pos[bi] - pos[0]
                v_sun = vel[bi] - vel[0]
                row[f"{b.name}_x"] = float(pos[bi][0])
                row[f"{b.name}_y"] = float(pos[bi][1])
                row[f"{b.name}_r"] = float(np.linalg.norm(r_sun))
                row[f"{b.name}_angle"] = float(math.atan2(r_sun[1], r_sun[0]))
                row[f"{b.name}_peri_angle"] = eccentricity_vector_angle(r_sun, v_sun, masses[0])
                keff, shear_t, other_t = k_eff(t, i, C[i], C0[i], p)
                row[f"{b.name}_Keff"] = keff
                delta = C[i] - C0[i]
                row[f"{b.name}_deltaC"] = float(delta)
                row[f"{b.name}_state"] = classify(delta, p.threshold)
            rows.append(row)
        pos, vel, C_new, keffs = rk4_step(t, pos, vel, C, C0, masses, p)
        for i in range(N_PLANETS):
            bi = i + 1
            r_sun = pos[bi] - pos[0]
            a_from_sun = -G * masses[0] * r_sun / max(np.linalg.norm(r_sun), 1e-9) ** 3
            correction_work[i] += float(np.dot(a_from_sun * (keffs[i] - 1.0), vel[bi])) * p.dt
            state = classify(float(C[i] - C0[i]), p.threshold)
            route_counts[BODIES[i].name][str(state)] += 1
        C = C_new
    ef = total_energy(pos, vel, masses)
    csvp = out / f"{tag}.csv"
    if rows:
        with csvp.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    summary = {
        "tag": tag,
        "steps": steps,
        "energy_initial": e0,
        "energy_final": ef,
        "energy_relative_drift": abs(ef - e0) / abs(e0) if e0 != 0 else None,
        "applied_work_by_body": {b.name: float(correction_work[i]) for i, b in enumerate(BODIES)},
        "route_counts_by_body": route_counts,
        "csv_sha256": hashlib.sha256(csvp.read_bytes()).hexdigest() if rows else None,
    }
    return rows, summary


# ---------------------------------------------------------------------------
# Measurements (D-412 "Required measurements" + spec "planetary test" clause)
# ---------------------------------------------------------------------------
def perihelion_precession(rows: list[dict], name: str):
    """Apsidal-line drift rate, converted to arcsec/century, from the
    instantaneous osculating eccentricity-vector angle (`{name}_peri_angle`,
    see `eccentricity_vector_angle`). Sampled at every row, not just at
    periapsis passages, so this is far better conditioned than searching for
    discrete radius minima. It is still a numerical diagnostic, not an
    ephemeris-grade propagation; near-circular orbits (Venus, Earth) have a
    small, poorly-directed eccentricity vector and their precession estimate
    is correspondingly noisy by physical construction, not by a bug -- treat
    Mercury (e=0.206) as the primary reliable diagnostic here."""
    if len(rows) < 2:
        return None
    t = np.array([row["t"] for row in rows])
    raw = np.array([row[f"{name}_peri_angle"] for row in rows])
    angle = np.unwrap(raw)
    slope, _ = np.polyfit(t, angle, 1)  # rad/yr
    return float(slope * (180.0 / math.pi * 3600.0) * 100.0)


def model_separation(rows_a: list[dict], rows_b: list[dict], name: str, fit_fraction: float):
    """RMS position separation between two runs sharing the same t grid,
    split into a fit interval and a withheld prediction interval."""
    n = min(len(rows_a), len(rows_b))
    t = np.array([rows_a[k]["t"] for k in range(n)])
    dx = np.array([rows_a[k][f"{name}_x"] - rows_b[k][f"{name}_x"] for k in range(n)])
    dy = np.array([rows_a[k][f"{name}_y"] - rows_b[k][f"{name}_y"] for k in range(n)])
    sep = np.hypot(dx, dy)
    t_split = t[0] + fit_fraction * (t[-1] - t[0])
    fit_mask = t <= t_split
    held_mask = ~fit_mask
    return {
        "rms_separation_fit_interval": float(np.sqrt(np.mean(sep[fit_mask] ** 2))) if fit_mask.any() else None,
        "rms_separation_heldout_interval": float(np.sqrt(np.mean(sep[held_mask] ** 2))) if held_mask.any() else None,
        "max_separation_heldout_interval": float(sep[held_mask].max()) if held_mask.any() else None,
    }


def kinematic_identity_check(rows: list[dict]) -> float:
    """d_ij + d_jk + d_ki = 0 around Sun-Earth-Mars. Purely kinematic;
    reported as a sanity check on the integrator/bookkeeping, never as
    evidence for the model (spec explicitly forbids counting it as such)."""
    worst = 0.0
    for row in rows:
        d_se = np.array([row["earth_x"], row["earth_y"]])
        d_em = np.array([row["mars_x"] - row["earth_x"], row["mars_y"] - row["earth_y"]])
        d_ms = np.array([-row["mars_x"], -row["mars_y"]])
        worst = max(worst, float(np.linalg.norm(d_se + d_em + d_ms)))
    return worst


def recovery_time(rows_perturbed: list[dict], rows_baseline: list[dict], name: str, tol: float):
    n = min(len(rows_perturbed), len(rows_baseline))
    for k in range(n):
        dx = rows_perturbed[k][f"{name}_x"] - rows_baseline[k][f"{name}_x"]
        dy = rows_perturbed[k][f"{name}_y"] - rows_baseline[k][f"{name}_y"]
        if math.hypot(dx, dy) < tol:
            return rows_perturbed[k]["t"]
    return None


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
CASE_OVERRIDES = {
    "newton_control": dict(onewave_active=False, use_1pn=False),
    "pn_control": dict(onewave_active=False, use_1pn=True),
    "onewave": dict(onewave_active=True, use_1pn=False),
    "ablation_zero_input": dict(onewave_active=False, use_1pn=False),
    "ablation_no_em_shell": dict(onewave_active=True, use_1pn=False, use_em_shell=False),
    "ablation_no_boundary_weave": dict(onewave_active=True, use_1pn=False, use_boundary_weave=False),
    "ablation_no_core_differential": dict(onewave_active=True, use_1pn=False, use_core_differential=False),
    "ablation_no_memory": dict(onewave_active=True, use_1pn=False, use_memory=False),
    "ablation_symmetric_mercury": dict(onewave_active=True, use_1pn=False, mercury_asymmetric_coupling=False),
    "ablation_no_jupiter": dict(onewave_active=True, use_1pn=False, include_jupiter=False),
    "dt_refine_half": dict(onewave_active=True, use_1pn=False),
}


def make_params(base: Params, tag: str) -> Params:
    overrides = dict(CASE_OVERRIDES.get(tag, {}))
    if tag == "dt_refine_half":
        overrides["dt"] = base.dt / 2.0
    fields = asdict(base)
    fields.update(overrides)
    return Params(**fields)


def plot(all_rows: dict, out: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(2, 2, figsize=(12, 9))
    for tag in ("newton_control", "pn_control", "onewave"):
        rows = all_rows[tag]
        t = [r["t"] for r in rows]
        ax[0, 0].plot([r["earth_x"] for r in rows], [r["earth_y"] for r in rows], label=f"{tag} earth", alpha=0.7)
        ax[0, 1].plot(t, [r["mercury_r"] for r in rows], label=f"{tag} mercury_r", alpha=0.7)
        ax[1, 0].plot(t, [r["mercury_deltaC"] for r in rows], label=f"{tag} mercury_deltaC", alpha=0.7)
        ax[1, 1].plot(t, [r["energy"] for r in rows], label=tag, alpha=0.7)
    titles = ["Earth path (AU)", "Mercury Sun-distance (AU)", "Mercury L2D compression differential", "Total system energy"]
    for a, title in zip(ax.flat, titles):
        a.set_title(title)
        a.grid(alpha=0.25)
        a.legend(fontsize=7)
    ax[0, 0].axis("equal")
    fig.tight_layout()
    fig.savefig(out / "d415_case_comparison.png", dpi=170)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results")
    ap.add_argument("--duration", type=float, default=None)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    base = Params()
    if a.duration:
        base.duration = a.duration

    all_rows, all_summ = {}, {}
    for tag in CASE_OVERRIDES:
        p = make_params(base, tag)
        rows, summ = run(p, out, tag)
        all_rows[tag] = rows
        all_summ[tag] = summ
        print(f"  ran {tag}: {len(rows)} samples, energy_drift={summ['energy_relative_drift']}")

    plot({k: v for k, v in all_rows.items() if k in ("newton_control", "pn_control", "onewave")}, out)

    # ---- measurements ----
    precession = {}
    for tag in ("newton_control", "pn_control", "onewave"):
        precession[tag] = {b.name: perihelion_precession(all_rows[tag], b.name) for b in BODIES}
    precession_refined = {
        tag: perihelion_precession(all_rows[tag], "mercury")
        for tag in ("newton_control", "pn_control", "onewave", "dt_refine_half")
    }

    sep_onewave_vs_newton = {b.name: model_separation(all_rows["onewave"], all_rows["newton_control"], b.name, base.fit_fraction) for b in BODIES}
    sep_zero_input_vs_newton = {b.name: model_separation(all_rows["ablation_zero_input"], all_rows["newton_control"], b.name, base.fit_fraction) for b in BODIES}

    kin_identity_worst = kinematic_identity_check(all_rows["onewave"])

    keff_bounds = {}
    for tag in ("onewave",):
        for b in BODIES:
            vals = [row[f"{b.name}_Keff"] for row in all_rows[tag]]
            keff_bounds[b.name] = {"min": float(min(vals)), "max": float(max(vals))}

    dt_convergence_ratio = None
    if precession_refined["onewave"] is not None and precession_refined["dt_refine_half"] is not None and abs(precession_refined["onewave"]) > 1e-9:
        dt_convergence_ratio = abs(precession_refined["dt_refine_half"] - precession_refined["onewave"]) / abs(precession_refined["onewave"])

    checks = {
        "zero_input_matches_newton_control": (
            sep_zero_input_vs_newton["earth"]["rms_separation_heldout_interval"] is not None
            and sep_zero_input_vs_newton["earth"]["rms_separation_heldout_interval"] < 1e-9
        ),
        "candidate_correction_is_bounded_perturbation": all(
            abs(v["min"] - 1.0) < 1e-3 and abs(v["max"] - 1.0) < 1e-3 for v in keff_bounds.values()
        ),
        "newton_control_energy_conserved": all_summ["newton_control"]["energy_relative_drift"] is not None and all_summ["newton_control"]["energy_relative_drift"] < 1e-6,
        "kinematic_identity_holds_to_float_precision": kin_identity_worst < 1e-6,
        "onewave_separation_grows_from_fit_to_heldout": (
            sep_onewave_vs_newton["mercury"]["rms_separation_heldout_interval"] is not None
            and sep_onewave_vs_newton["mercury"]["rms_separation_fit_interval"] is not None
            and sep_onewave_vs_newton["mercury"]["rms_separation_heldout_interval"] >= sep_onewave_vs_newton["mercury"]["rms_separation_fit_interval"]
        ),
        "1pn_perihelion_precession_is_prograde_and_nonzero": precession_refined["pn_control"] is not None and precession_refined["pn_control"] > 0,
    }

    payload = {
        "model": "D-415 planetary point/path/field: Newtonian control + 1PN control + candidate One-Wave correction",
        "status": "YELLOW candidate architecture (UPDATED_41 scoped test)",
        "native_dimension": "3D physical system, integrated as a declared 2D planar projection (A-117)",
        "code_version": CODE_VERSION,
        "parameters": asdict(base),
        "seed": base.seed,
        "limitations": [
            "Planar (2D) projection: real orbital inclinations are not carried.",
            "Spin/core-differential rates are prescribed constants (real spin periods + an illustrative core-mantle offset), not solved from an internal dynamo model, and are not fed back from the orbital solver.",
            "The K_eff candidate correction is a small bounded multiplicative stand-in for UPDATED_41 S8's EM-shell law, not a derivation of it.",
            "EM-alignment is a declared periodic proxy (orbital-phase modulation), not a derived 3D dipole-tilt geometry.",
            "Perihelion-precession estimates use parabolic interpolation around sampled radius minima, not analytic osculating-element propagation; treat as a coarse diagnostic and see the dt-refinement convergence check.",
            "Cell area, FCC/HCP stacking, imposed-well, and periodic/random-lattice ablations are D-408/D-409/D-413 lattice-scale concepts and are declared out of scope at this point-mass planetary scale.",
            "Held-out ranging residuals are computed against this engine's own Newtonian control, not against independent spacecraft ranging data; this is a model-separation test, not an external validation.",
            "Does not derive kilograms, an absolute work metric, or a GR replacement (repository honesty boundary).",
        ],
        "measurements": {
            "perihelion_precession_arcsec_per_century": precession,
            "perihelion_precession_dt_refinement": precession_refined,
            "dt_convergence_relative_change": dt_convergence_ratio,
            "model_separation_onewave_vs_newton_control": sep_onewave_vs_newton,
            "model_separation_zero_input_vs_newton_control": sep_zero_input_vs_newton,
            "kinematic_identity_max_deviation_AU": kin_identity_worst,
            "K_eff_bounds_by_body": keff_bounds,
            "applied_work_by_body": {tag: all_summ[tag]["applied_work_by_body"] for tag in ("onewave", "ablation_no_em_shell", "ablation_no_boundary_weave")},
            "route_counts_by_body_onewave": all_summ["onewave"]["route_counts_by_body"],
            "energy_relative_drift_by_case": {tag: all_summ[tag]["energy_relative_drift"] for tag in CASE_OVERRIDES},
        },
        "ablations": {
            "no_em_shell": "use_em_shell=False; zeroes the EM-alignment channel of K_eff for dynamo bodies.",
            "no_boundary_weave": "use_boundary_weave=False; zeroes the L2D compression-differential channel of K_eff.",
            "no_core_differential": "use_core_differential=False; zeroes the shear channel (prescribed DeltaOmega_core-mantle).",
            "no_memory": "use_memory=False; C_i tracks its instantaneous tidal target with no relaxation lag.",
            "symmetric_mercury": "mercury_asymmetric_coupling=False; removes the UPDATED_41 S9 Sun-Mercury asymmetric EM term.",
            "no_jupiter": "include_jupiter=False; N-body-count analog of a spatial-refinement test.",
            "zero_input": "onewave_active=False; must reduce exactly to the Newtonian control (see checks).",
            "dt_refine_half": "same case at half the timestep; tests numerical convergence of the precession estimate.",
            "not_applicable": [
                "no_well (D-413 imposed-curvature-well concept does not apply to point-mass N-body gravity)",
                "FCC_vs_HCP_stacking (D-409 3D lattice concept)",
                "periodic/random/simple-control lattices (D-408/D-413 lattice concept; the analog here is the Newtonian control model itself)",
            ],
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "cases": {tag: all_summ[tag] for tag in CASE_OVERRIDES},
    }
    (out / "d415_summary.json").write_text(json.dumps(payload, indent=2))
    print(json.dumps({"all_checks_pass": payload["all_checks_pass"], "checks": checks}, indent=2))
    raise SystemExit(0 if payload["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
