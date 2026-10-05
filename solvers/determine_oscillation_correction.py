#!/usr/bin/env python3
"""
Determine Oscillation Correction Formula

Hypothesis: The observed errors come from a correction term that depends on
oscillation frequency dispersion between quarks.

Mechanism: When quarks oscillate at very different frequencies, the effective
phase-locking configuration becomes time-dependent. The static calculation
assumes all quarks move with the same phase evolution, but if they oscillate
at 44x different frequencies (as in Lambda), the phase separation oscillates
in time. Time-averaging this produces a different effective binding energy.

Test: ΔE_correction ∝ f(ω_dispersion)
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

EXPERIMENTAL_MASSES = {
    "proton": 938.3,
    "neutron": 939.6,
    "Lambda": 1115.7,
}

PREDICTED_MASSES = {
    "proton": 914.4,
    "neutron": 967.3,
    "Lambda": 1319.2,
}

ERRORS_MEV = {
    "proton": 914.4 - 938.3,      # -23.9 MeV
    "neutron": 967.3 - 939.6,     # +27.7 MeV
    "Lambda": 1319.2 - 1115.7,    # +203.5 MeV
}


def compute_oscillation_parameters(hadron_name, knot):
    """Compute oscillation frequency dispersion for a hadron."""
    
    masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in knot.vortices]
    
    kappa_T = 0.297 * 1000  # Convert to MeV
    omegas = [kappa_T / m for m in masses]
    
    omega_ratio = max(omegas) / min(omegas) if min(omegas) > 0 else 1
    avg_mass = np.mean(masses)
    
    return {
        "hadron": hadron_name,
        "masses": masses,
        "omegas": omegas,
        "omega_ratio": omega_ratio,
        "avg_mass": avg_mass,
        "error_mev": ERRORS_MEV.get(hadron_name, 0),
    }


def fit_correction_formula():
    """Fit the oscillation correction formula to observed errors."""
    
    print("="*90)
    print("OSCILLATION CORRECTION FORMULA FITTING")
    print("="*90)
    print()
    
    # Collect data
    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]
    
    data = []
    for hadron_name, knot in hadrons:
        params = compute_oscillation_parameters(hadron_name, knot)
        data.append(params)
    
    # Display data
    print("DATA:")
    print("-"*90)
    print(f"{'Hadron':<12} {'Error (MeV)':>12} {'ω_ratio':>10} {'Avg mass (MeV)':>15}")
    print("-"*90)
    for d in data:
        print(f"{d['hadron']:<12} {d['error_mev']:>+11.1f} {d['omega_ratio']:>10.1f} {d['avg_mass']:>15.2f}")
    
    print()
    print("FITTING CANDIDATE FORMULAS:")
    print("-"*90)
    print()
    
    # Candidate 1: Error ∝ (ω_ratio - 1)
    print("1. Linear in frequency dispersion: ΔE ≈ A × (ω_ratio - 1)")
    omega_ratios = np.array([d["omega_ratio"] for d in data])
    errors = np.array([d["error_mev"] for d in data])
    
    # Fit: error = A * (omega_ratio - 1)
    # Use least squares for non-zero intercept cases
    x = omega_ratios - 1
    if np.any(x != 0):
        A_fit1 = np.average(errors / (omega_ratios - 1 + 1e-6))
        predicted1 = A_fit1 * (omega_ratios - 1)
        rmse1 = np.sqrt(np.mean((errors - predicted1)**2))
        print(f"   Coefficient A = {A_fit1:.2f}")
        print(f"   RMSE = {rmse1:.1f} MeV")
        print(f"   Predictions:")
        for i, d in enumerate(data):
            pred = A_fit1 * (d["omega_ratio"] - 1)
            print(f"     {d['hadron']}: {pred:+.1f} MeV (actual {d['error_mev']:+.1f})")
    
    print()
    
    # Candidate 2: Error ∝ (ω_ratio - 1)²
    print("2. Quadratic in frequency dispersion: ΔE ≈ B × (ω_ratio - 1)²")
    x2 = (omega_ratios - 1)**2
    if np.any(x2 != 0):
        B_fit2 = np.average(errors / (x2 + 1e-6))
        predicted2 = B_fit2 * (omega_ratios - 1)**2
        rmse2 = np.sqrt(np.mean((errors - predicted2)**2))
        print(f"   Coefficient B = {B_fit2:.2f}")
        print(f"   RMSE = {rmse2:.1f} MeV")
        print(f"   Predictions:")
        for i, d in enumerate(data):
            pred = B_fit2 * (d["omega_ratio"] - 1)**2
            print(f"     {d['hadron']}: {pred:+.1f} MeV (actual {d['error_mev']:+.1f})")
    
    print()
    
    # Candidate 3: Error ∝ (ω_ratio - 1) × avg_mass
    print("3. Dispersion × mass: ΔE ≈ C × (ω_ratio - 1) × avg_mass")
    avg_masses = np.array([d["avg_mass"] for d in data])
    x3 = (omega_ratios - 1) * avg_masses
    if np.any(x3 != 0):
        C_fit3 = np.average(errors / (x3 + 1e-6))
        predicted3 = C_fit3 * (omega_ratios - 1) * avg_masses
        rmse3 = np.sqrt(np.mean((errors - predicted3)**2))
        print(f"   Coefficient C = {C_fit3:.4f}")
        print(f"   RMSE = {rmse3:.1f} MeV")
        print(f"   Predictions:")
        for i, d in enumerate(data):
            pred = C_fit3 * (d["omega_ratio"] - 1) * d["avg_mass"]
            print(f"     {d['hadron']}: {pred:+.1f} MeV (actual {d['error_mev']:+.1f})")
    
    print()
    
    # Candidate 4: Error ∝ ln(ω_ratio)
    print("4. Logarithmic dispersion: ΔE ≈ D × ln(ω_ratio)")
    ln_ratios = np.log(omega_ratios)
    if np.any(ln_ratios != 0):
        D_fit4 = np.average(errors / (ln_ratios + 1e-6))
        predicted4 = D_fit4 * ln_ratios
        rmse4 = np.sqrt(np.mean((errors - predicted4)**2))
        print(f"   Coefficient D = {D_fit4:.2f}")
        print(f"   RMSE = {rmse4:.1f} MeV")
        print(f"   Predictions:")
        for i, d in enumerate(data):
            pred = D_fit4 * np.log(d["omega_ratio"])
            print(f"     {d['hadron']}: {pred:+.1f} MeV (actual {d['error_mev']:+.1f})")
    
    print()
    print("="*90)
    print("BEST FIT SUMMARY")
    print("="*90)
    print()
    
    fits = {
        "Linear": rmse1,
        "Quadratic": rmse2,
        "Dispersion×Mass": rmse3,
        "Logarithmic": rmse4,
    }
    
    best_fit = min(fits, key=fits.get)
    print(f"Best fit: {best_fit} (RMSE = {fits[best_fit]:.1f} MeV)")
    print()
    
    if best_fit == "Linear":
        print(f"FORMULA: ΔE_correction = {A_fit1:.2f} × (ω_ratio - 1)")
        print(f"  ω_ratio = ω_max / ω_min = (κ_T / m_min) / (κ_T / m_max) = m_max / m_min")
    elif best_fit == "Quadratic":
        print(f"FORMULA: ΔE_correction = {B_fit2:.2f} × (ω_ratio - 1)²")
    elif best_fit == "Dispersion×Mass":
        print(f"FORMULA: ΔE_correction = {C_fit3:.4f} × (ω_ratio - 1) × avg_mass")
    elif best_fit == "Logarithmic":
        print(f"FORMULA: ΔE_correction = {D_fit4:.2f} × ln(ω_ratio)")
    
    print()


if __name__ == "__main__":
    fit_correction_formula()
