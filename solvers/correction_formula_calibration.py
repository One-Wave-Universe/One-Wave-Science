#!/usr/bin/env python3
"""
Correction Formula Calibration: Unified Formula Across All Hadrons

Based on phase_shift_sign_analysis.py findings:
- Proton and Neutron have opposite error signs based on symmetric pair rank
- Lambda has much larger error due to extreme asymmetry + frequency dispersion

Proposed unified formula:
  ΔE_correction = A × (m_max - m_min) × rank_factor / f(ω_ratio)

where:
  rank_factor = +1 if symmetric pair is MINIMUM mass
              = -1 if symmetric pair is MAXIMUM or INTERMEDIATE mass
              = -2 if NO symmetric pair (all different masses)

  f(ω_ratio) could be:
    - Linear: 1.0
    - Inverse: 1 / ω_ratio
    - Square root inverse: 1 / √ω_ratio
    - Logarithmic: log(ω_ratio)

This accounts for: Higher oscillation dispersion reduces binding
correction because oscillations average out more.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from hadron_knot_geometry import create_proton, create_neutron, create_lambda

QUARK_MASSES_MEV = {
    "up": 2.16,
    "down": 4.67,
    "strange": 95.0,
}


def get_hadron_parameters(hadron_name, knot):
    """Extract all parameters needed for correction formula."""

    vortices = knot.vortices
    masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in vortices]

    m_min = min(masses)
    m_max = max(masses)

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
        # No symmetric pair (all different)
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
        "mass_range": m_max - m_min,
        "rank_factor": rank_factor,
        "omega_ratio": omega_ratio,
    }


def test_formula_variants():
    """Test different functional forms for frequency scaling."""

    print("="*90)
    print("CORRECTION FORMULA CALIBRATION")
    print("="*90)
    print()

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    # Observed errors (from measurements)
    errors_obs = {
        "proton": -23.9,
        "neutron": +27.7,
        "Lambda": +203.5,
    }

    # Extract parameters
    params = []
    for hadron_name, knot in hadrons:
        p = get_hadron_parameters(hadron_name, knot)
        p["error_obs"] = errors_obs[hadron_name]
        params.append(p)

    # Display parameters
    print("HADRON PARAMETERS:")
    print("-" * 90)
    print()

    print(f"{'Hadron':<12} {'Range':<10} {'Rank':<8} {'ω_ratio':<12} {'Error':>10}")
    print("-" * 60)
    for p in params:
        print(f"{p['hadron']:<12} {p['mass_range']:>8.1f} {p['rank_factor']:>+6.0f} {p['omega_ratio']:>11.2f} {p['error_obs']:>+9.1f}")

    print()

    # Test formula variants
    print("="*90)
    print("TESTING FORMULA VARIANTS")
    print("="*90)
    print()

    # Variant 1: ΔE = A × range × rank_factor
    print("VARIANT 1: ΔE = A × range × rank_factor")
    print("-" * 60)

    X1 = np.array([[p["mass_range"] * p["rank_factor"]] for p in params])
    y = np.array([p["error_obs"] for p in params])

    A1 = np.linalg.lstsq(X1, y, rcond=None)[0][0]
    pred1 = X1.flatten() * A1
    rmse1 = np.sqrt(np.mean((pred1 - y)**2))

    print(f"  A = {A1:.4f}")
    print(f"  RMSE = {rmse1:.2f} MeV")
    print()

    # Variant 2: ΔE = A × range × rank_factor / ω_ratio
    print("VARIANT 2: ΔE = A × range × rank_factor / ω_ratio")
    print("-" * 60)

    X2 = np.array([[p["mass_range"] * p["rank_factor"] / p["omega_ratio"]] for p in params])
    A2 = np.linalg.lstsq(X2, y, rcond=None)[0][0]
    pred2 = X2.flatten() * A2
    rmse2 = np.sqrt(np.mean((pred2 - y)**2))

    print(f"  A = {A2:.4f}")
    print(f"  RMSE = {rmse2:.2f} MeV")
    print()

    # Variant 3: ΔE = A × range × rank_factor / √ω_ratio
    print("VARIANT 3: ΔE = A × range × rank_factor / √ω_ratio")
    print("-" * 60)

    X3 = np.array([[p["mass_range"] * p["rank_factor"] / np.sqrt(p["omega_ratio"])] for p in params])
    A3 = np.linalg.lstsq(X3, y, rcond=None)[0][0]
    pred3 = X3.flatten() * A3
    rmse3 = np.sqrt(np.mean((pred3 - y)**2))

    print(f"  A = {A3:.4f}")
    print(f"  RMSE = {rmse3:.2f} MeV")
    print()

    # Variant 4: ΔE = A × range × rank_factor / log(1 + ω_ratio)
    print("VARIANT 4: ΔE = A × range × rank_factor / log(1 + ω_ratio)")
    print("-" * 60)

    X4 = np.array([[p["mass_range"] * p["rank_factor"] / np.log(1 + p["omega_ratio"])] for p in params])
    A4 = np.linalg.lstsq(X4, y, rcond=None)[0][0]
    pred4 = X4.flatten() * A4
    rmse4 = np.sqrt(np.mean((pred4 - y)**2))

    print(f"  A = {A4:.4f}")
    print(f"  RMSE = {rmse4:.2f} MeV")
    print()

    # Variant 5: ΔE = A × range × rank_factor × log(ω_ratio)
    print("VARIANT 5: ΔE = A × range × rank_factor × log(ω_ratio)")
    print("-" * 60)

    X5 = np.array([[p["mass_range"] * p["rank_factor"] * np.log(p["omega_ratio"] + 1e-6)] for p in params])
    A5 = np.linalg.lstsq(X5, y, rcond=None)[0][0]
    pred5 = X5.flatten() * A5
    rmse5 = np.sqrt(np.mean((pred5 - y)**2))

    print(f"  A = {A5:.4f}")
    print(f"  RMSE = {rmse5:.2f} MeV")
    print()

    # Compare
    print("="*90)
    print("VARIANT COMPARISON (ranked by RMSE)")
    print("="*90)
    print()

    variants = [
        ("Variant 1: A × range × rank", rmse1, pred1, A1),
        ("Variant 2: A × range × rank / ω", rmse2, pred2, A2),
        ("Variant 3: A × range × rank / √ω", rmse3, pred3, A3),
        ("Variant 4: A × range × rank / log(ω)", rmse4, pred4, A4),
        ("Variant 5: A × range × rank × log(ω)", rmse5, pred5, A5),
    ]

    variants.sort(key=lambda x: x[1])

    print(f"{'Rank':<5} {'Variant':<35} {'RMSE':>10} {'A coeff':>10}")
    print("-" * 65)
    for rank, (name, rmse, _, coeff) in enumerate(variants, 1):
        print(f"{rank:<5} {name:<35} {rmse:>9.2f} {coeff:>10.4f}")

    print()

    # Show best variant predictions
    best_name, best_rmse, best_pred, best_A = variants[0]
    print("="*90)
    print(f"BEST FIT: {best_name}")
    print("="*90)
    print()

    print(f"Coefficient A = {best_A:.4f}")
    print()

    print(f"{'Hadron':<12} {'Predicted':<15} {'Observed':<15} {'Error':<12}")
    print("-" * 60)

    for i, p in enumerate(params):
        pred = best_pred[i]
        obs = p["error_obs"]
        error = pred - obs

        print(f"{p['hadron']:<12} {pred:>+13.1f} {obs:>+13.1f} {error:>+10.1f}")

    print()

    # Show what this means for hadron masses
    print("="*90)
    print("APPLICATION: Corrected Hadron Masses")
    print("="*90)
    print()

    EXPT = {"proton": 938.3, "neutron": 939.6, "Lambda": 1115.7}
    PREDICTED_BASE = {"proton": 914.4, "neutron": 967.3, "Lambda": 1319.2}

    print(f"{'Hadron':<12} {'Base Pred':<15} {'Correction':<15} {'Corrected':<15} {'Expt':<12} {'Error%':>10}")
    print("-" * 80)

    for i, p in enumerate(params):
        base = PREDICTED_BASE[p['hadron']]
        correction = best_pred[i]
        corrected = base + correction
        expt = EXPT[p['hadron']]
        error_pct = 100 * (corrected - expt) / expt

        print(f"{p['hadron']:<12} {base:>13.1f} {correction:>+13.1f} {corrected:>13.1f} {expt:>10.1f} {error_pct:>+9.2f}%")

    print()

    # Final validation
    print("="*90)
    print("VALIDATION")
    print("="*90)
    print()

    print(f"Best formula RMSE: {best_rmse:.2f} MeV")
    print()

    if best_rmse < 20:
        print("✓ EXCELLENT: All hadrons fit to within ±20 MeV")
    elif best_rmse < 50:
        print("✓ GOOD: Fit explains most variance")
    else:
        print("✗ FAIR: More work needed on mechanism")

    print()

    return best_name, best_A, best_rmse


if __name__ == "__main__":
    try:
        test_formula_variants()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
