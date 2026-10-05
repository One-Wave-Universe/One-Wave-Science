#!/usr/bin/env python3
"""
Refined Correction Formula: Including Symmetric Pair Mass Scale

The previous formula couldn't distinguish Proton from Neutron because:
- Both have same mass_range (2.5 MeV)
- Both have same ω_ratio (2.16)
- Only rank_factor differs (±1)
- But |error| differs: 23.9 vs 27.7 MeV

Missing factor: The ABSOLUTE MASS SCALE of the symmetric pair

Hypothesis: Light symmetric pair (u at 2.16) → Different correction than
heavier symmetric pair (d at 4.67), even with same mass_range.

Refined formula:
  ΔE = A × (m_max - m_min) × rank_factor × g(m_sym) / √(ω_ratio)

where g(m_sym) could be:
  - Constant (already tried, doesn't work)
  - 1 / m_sym (inverse mass: lighter → stronger correction)
  - √(1/m_sym) (gentler scaling)
  - m_avg / m_sym (aspect ratio)
"""

import sys
sys.path.insert(0, "/home/claude/one-wave-science/solvers")

import numpy as np
from hadron_knot_geometry import create_proton, create_neutron, create_lambda

QUARK_MASSES_MEV = {
    "up": 2.16,
    "down": 4.67,
    "strange": 95.0,
}


def get_full_hadron_parameters(hadron_name, knot):
    """Extract all parameters including symmetric pair mass."""

    vortices = knot.vortices
    masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in vortices]

    m_min = min(masses)
    m_max = max(masses)
    m_avg = np.mean(masses)

    # Find symmetric pair
    symmetric_mass = None
    symmetric_pair_indices = []
    for i in range(len(masses)):
        for j in range(i+1, len(masses)):
            if masses[i] == masses[j]:
                symmetric_mass = masses[i]
                symmetric_pair_indices = [i, j]
                break

    # Determine rank factor
    if symmetric_mass is not None and symmetric_mass == m_min:
        rank_factor = 1.0
    elif symmetric_mass is not None and symmetric_mass != m_min:
        rank_factor = -1.0
    else:
        rank_factor = -2.0

    # Compute frequency ratio
    kappa_T = 0.297 * 1000  # MeV
    omegas = [kappa_T / m for m in masses]
    omega_min = min(omegas)
    omega_max = max(omegas)
    omega_ratio = omega_max / omega_min

    return {
        "hadron": hadron_name,
        "m_min": m_min,
        "m_max": m_max,
        "m_avg": m_avg,
        "mass_range": m_max - m_min,
        "symmetric_mass": symmetric_mass if symmetric_mass is not None else m_min,
        "rank_factor": rank_factor,
        "omega_ratio": omega_ratio,
    }


def test_mass_scale_variants():
    """Test how symmetric pair mass affects the correction."""

    print("="*90)
    print("REFINED CORRECTION FORMULA: Role of Symmetric Pair Mass")
    print("="*90)
    print()

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    errors_obs = {
        "proton": -23.9,
        "neutron": +27.7,
        "Lambda": +203.5,
    }

    params = []
    for hadron_name, knot in hadrons:
        p = get_full_hadron_parameters(hadron_name, knot)
        p["error_obs"] = errors_obs[hadron_name]
        params.append(p)

    # Display full parameters
    print("EXTENDED PARAMETERS:")
    print("-" * 90)
    print()

    print(f"{'Hadron':<12} {'Sym Mass':<10} {'Range':<10} {'Rank':<8} {'ω_ratio':<12} {'Error':>10}")
    print("-" * 70)
    for p in params:
        print(f"{p['hadron']:<12} {p['symmetric_mass']:>8.2f} {p['mass_range']:>8.1f} {p['rank_factor']:>+6.0f} {p['omega_ratio']:>11.2f} {p['error_obs']:>+9.1f}")

    print()

    y = np.array([p["error_obs"] for p in params])

    # Variant A: Base formula (from previous)
    print("VARIANT A: ΔE = A × range × rank / √ω")
    print("-" * 60)

    X_a = np.array([[p["mass_range"] * p["rank_factor"] / np.sqrt(p["omega_ratio"])] for p in params])
    A_a = np.linalg.lstsq(X_a, y, rcond=None)[0][0]
    pred_a = X_a.flatten() * A_a
    rmse_a = np.sqrt(np.mean((pred_a - y)**2))

    print(f"  A = {A_a:.4f}")
    print(f"  RMSE = {rmse_a:.2f} MeV")
    print()

    # Variant B: Include inverse mass scaling
    print("VARIANT B: ΔE = A × range × rank × (1/m_sym) / √ω")
    print("-" * 60)

    X_b = np.array([[p["mass_range"] * p["rank_factor"] * (1.0 / p["symmetric_mass"]) / np.sqrt(p["omega_ratio"])] for p in params])
    A_b = np.linalg.lstsq(X_b, y, rcond=None)[0][0]
    pred_b = X_b.flatten() * A_b
    rmse_b = np.sqrt(np.mean((pred_b - y)**2))

    print(f"  A = {A_b:.4f}")
    print(f"  RMSE = {rmse_b:.2f} MeV")
    print()

    # Variant C: Include inverse square root mass scaling
    print("VARIANT C: ΔE = A × range × rank × (1/√m_sym) / √ω")
    print("-" * 60)

    X_c = np.array([[p["mass_range"] * p["rank_factor"] * (1.0 / np.sqrt(p["symmetric_mass"])) / np.sqrt(p["omega_ratio"])] for p in params])
    A_c = np.linalg.lstsq(X_c, y, rcond=None)[0][0]
    pred_c = X_c.flatten() * A_c
    rmse_c = np.sqrt(np.mean((pred_c - y)**2))

    print(f"  A = {A_c:.4f}")
    print(f"  RMSE = {rmse_c:.2f} MeV")
    print()

    # Variant D: Ratio of average to symmetric mass
    print("VARIANT D: ΔE = A × range × rank × (m_avg/m_sym) / √ω")
    print("-" * 60)

    X_d = np.array([[p["mass_range"] * p["rank_factor"] * (p["m_avg"] / p["symmetric_mass"]) / np.sqrt(p["omega_ratio"])] for p in params])
    A_d = np.linalg.lstsq(X_d, y, rcond=None)[0][0]
    pred_d = X_d.flatten() * A_d
    rmse_d = np.sqrt(np.mean((pred_d - y)**2))

    print(f"  A = {A_d:.4f}")
    print(f"  RMSE = {rmse_d:.2f} MeV")
    print()

    # Variant E: 2-term model with base + mass correction
    print("VARIANT E: ΔE = A₁ × range × rank / √ω + A₂ × (1/m_sym)")
    print("-" * 60)

    col1 = np.array([p["mass_range"] * p["rank_factor"] / np.sqrt(p["omega_ratio"]) for p in params])
    col2 = np.array([1.0 / p["symmetric_mass"] for p in params])
    X_e = np.column_stack([col1, col2])
    coeffs_e = np.linalg.lstsq(X_e, y, rcond=None)[0]
    A_e1, A_e2 = coeffs_e
    pred_e = X_e @ coeffs_e
    rmse_e = np.sqrt(np.mean((pred_e - y)**2))

    print(f"  A₁ = {A_e1:.4f}")
    print(f"  A₂ = {A_e2:.4f}")
    print(f"  RMSE = {rmse_e:.2f} MeV")
    print()

    # Compare all variants
    print("="*90)
    print("VARIANT COMPARISON")
    print("="*90)
    print()

    variants = [
        ("Variant A: Base", rmse_a, pred_a),
        ("Variant B: 1/m_sym", rmse_b, pred_b),
        ("Variant C: 1/√m_sym", rmse_c, pred_c),
        ("Variant D: m_avg/m_sym", rmse_d, pred_d),
        ("Variant E: Two-term", rmse_e, pred_e),
    ]

    variants.sort(key=lambda x: x[1])

    print(f"{'Rank':<5} {'Variant':<30} {'RMSE':>10}")
    print("-" * 50)
    for rank, (name, rmse, _) in enumerate(variants, 1):
        print(f"{rank:<5} {name:<30} {rmse:>9.2f}")

    print()

    # Show best variant
    best_name, best_rmse, best_pred = variants[0]
    print("="*90)
    print(f"BEST FIT: {best_name}")
    print("="*90)
    print()

    print(f"{'Hadron':<12} {'Predicted':<15} {'Observed':<15} {'Error':<12}")
    print("-" * 60)

    for i, p in enumerate(params):
        pred = best_pred[i]
        obs = p["error_obs"]
        error = pred - obs

        print(f"{p['hadron']:<12} {pred:>+13.1f} {obs:>+13.1f} {error:>+10.1f}")

    print()

    # Show corrected masses
    print("="*90)
    print("CORRECTED HADRON MASSES")
    print("="*90)
    print()

    EXPT = {"proton": 938.3, "neutron": 939.6, "Lambda": 1115.7}
    PREDICTED_BASE = {"proton": 914.4, "neutron": 967.3, "Lambda": 1319.2}

    print(f"{'Hadron':<12} {'Base Pred':<15} {'Correction':<15} {'Corrected':<15} {'Expt':<12} {'Error%':>10}")
    print("-" * 80)

    total_error_pct = 0
    for i, p in enumerate(params):
        base = PREDICTED_BASE[p['hadron']]
        correction = best_pred[i]
        corrected = base + correction
        expt = EXPT[p['hadron']]
        error_pct = 100 * (corrected - expt) / expt
        total_error_pct += abs(error_pct)

        print(f"{p['hadron']:<12} {base:>13.1f} {correction:>+13.1f} {corrected:>13.1f} {expt:>10.1f} {error_pct:>+9.2f}%")

    avg_error_pct = total_error_pct / 3

    print()
    print(f"Average absolute error: {avg_error_pct:.2f}%")

    if avg_error_pct < 1.0:
        print("✓✓✓ SUB-1% accuracy achieved!")
    elif avg_error_pct < 3.0:
        print("✓ Sub-3% accuracy - on target!")
    else:
        print(f"⚠ Average error still {avg_error_pct:.1f}% - needs refinement")

    print()


if __name__ == "__main__":
    try:
        test_mass_scale_variants()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
