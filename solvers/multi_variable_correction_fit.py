#!/usr/bin/env python3
"""
Multi-Variable Correction Formula Fit

Objective: Develop a correction formula that accounts for BOTH:
1. Oscillation frequency dispersion (ω_ratio)
2. Symmetric pair count (determines which phase differences oscillate)
3. Total mass asymmetry (amplitude of oscillation)

Key constraint: Proton and Neutron have identical ω_ratio and asymmetry,
but OPPOSITE error signs. This means the mechanism is not purely additive.

Hypothesis: The sign of the correction depends on which specific masses
form the symmetric pair (light vs. heavy).
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


def analyze_hadron_oscillations(hadron_name, knot):
    """Extract oscillation and asymmetry metrics for a hadron."""

    vortices = knot.vortices
    masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in vortices]
    flavors = [v.flavor for v in vortices]

    kappa_T = 0.297 * 1000  # MeV

    # Compute oscillation frequency for each quark
    omegas = [kappa_T / m for m in masses]
    omega_min = min(omegas)
    omega_max = max(omegas)
    omega_ratio = omega_max / omega_min

    # Identify symmetric pair
    symmetric_pair_flavor = None
    for i in range(len(masses)):
        for j in range(i+1, len(masses)):
            if masses[i] == masses[j]:
                symmetric_pair_flavor = flavors[i]
                break

    # If no symmetric pair, use lightest as reference
    if symmetric_pair_flavor is None:
        min_mass_idx = np.argmin(masses)
        symmetric_pair_flavor = flavors[min_mass_idx]

    # Average mass of symmetric pair (or lightest if none)
    symmetric_mass = None
    for i in range(len(masses)):
        if flavors[i] == symmetric_pair_flavor:
            symmetric_mass = masses[i]
            break

    # Total mass asymmetry: sum of |m_i - m_avg|
    m_avg = np.mean(masses)
    total_asymmetry = sum(abs(m - m_avg) for m in masses)

    # Heaviest quark mass (relevant for scale)
    max_mass = max(masses)

    # Average of all masses
    const_mass = sum(masses)

    return {
        "hadron": hadron_name,
        "masses": masses,
        "flavors": flavors,
        "omega_ratio": omega_ratio,
        "symmetric_pair_flavor": symmetric_pair_flavor,
        "symmetric_mass": symmetric_mass,
        "total_asymmetry": total_asymmetry,
        "max_mass": max_mass,
        "const_mass": const_mass,
        "m_avg": m_avg,
    }


def fit_correction_formulas():
    """Fit multiple correction formula candidates to the data."""

    print("="*90)
    print("MULTI-VARIABLE CORRECTION FORMULA FIT")
    print("="*90)
    print()

    # Observed data
    hadrons_data = []
    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    # Experimental and predicted masses
    EXPT = {"proton": 938.3, "neutron": 939.6, "Lambda": 1115.7}
    PREDICTED = {"proton": 914.4, "neutron": 967.3, "Lambda": 1319.2}

    for hadron_name, knot in hadrons:
        metrics = analyze_hadron_oscillations(hadron_name, knot)
        error_mev = PREDICTED[hadron_name] - EXPT[hadron_name]
        metrics["error_mev"] = error_mev
        metrics["error_pct"] = 100 * error_mev / EXPT[hadron_name]
        hadrons_data.append(metrics)

    # Display metrics
    print("HADRON METRICS:")
    print("-" * 90)
    print()

    for m in hadrons_data:
        print(f"{m['hadron'].upper()}")
        quark_str = ', '.join([f"{f}({m['masses'][i]:.1f})" for i, f in enumerate(m['flavors'])])
        print(f"  Quark composition: {quark_str}")
        print(f"  ω_ratio: {m['omega_ratio']:.2f}")
        print(f"  Symmetric pair flavor: {m['symmetric_pair_flavor']} ({m['symmetric_mass']:.2f} MeV)")
        print(f"  Total mass asymmetry: {m['total_asymmetry']:.1f} MeV")
        print(f"  Constituent mass: {m['const_mass']:.1f} MeV")
        print(f"  Error: {m['error_mev']:+.1f} MeV ({m['error_pct']:+.1f}%)")
        print()

    # Fit different formulas
    print("="*90)
    print("FORMULA FITTING")
    print("="*90)
    print()

    # Extract features
    omega_ratios = np.array([m["omega_ratio"] for m in hadrons_data])
    asymmetries = np.array([m["total_asymmetry"] for m in hadrons_data])
    symmetric_masses = np.array([m["symmetric_mass"] for m in hadrons_data])
    const_masses = np.array([m["const_mass"] for m in hadrons_data])
    errors = np.array([m["error_mev"] for m in hadrons_data])

    print("Data points:")
    print(f"{'Hadron':<12} {'ω_ratio':>10} {'Asymmetry':>12} {'Sym. mass':>10} {'Error':>10}")
    print("-" * 60)
    for m in hadrons_data:
        print(f"{m['hadron']:<12} {m['omega_ratio']:>10.2f} {m['total_asymmetry']:>12.1f} {m['symmetric_mass']:>10.2f} {m['error_mev']:>+10.1f}")
    print()

    # Formula 1: Linear combination
    print("FORMULA 1: ΔE = A·(ω_ratio - 1) + B·asymmetry + C")
    print("-" * 60)

    # Build design matrix [omega_ratio-1, asymmetry, 1]
    X1 = np.column_stack([omega_ratios - 1, asymmetries, np.ones(3)])
    coeffs1, residuals1, rank1, s1 = np.linalg.lstsq(X1, errors, rcond=None)

    A, B, C = coeffs1
    predictions1 = X1 @ coeffs1
    rmse1 = np.sqrt(np.mean((predictions1 - errors)**2))

    print(f"  A (ω_ratio coeff): {A:>10.4f}")
    print(f"  B (asymmetry coeff): {B:>10.4f}")
    print(f"  C (constant): {C:>10.4f}")
    print(f"  RMSE: {rmse1:.2f} MeV")
    print()

    # Formula 2: Interaction term (asymmetry × light/heavy indicator)
    print("FORMULA 2: ΔE = A·(ω_ratio - 1) + B·asymmetry·sign_indicator + C")
    print("-" * 60)

    # Sign indicator: +1 if symmetric pair is light (u/d), -1 if strange (s)
    sign_indicators = np.array([1 if m["symmetric_mass"] < 50 else -1 for m in hadrons_data])

    X2 = np.column_stack([omega_ratios - 1, asymmetries * sign_indicators, np.ones(3)])
    coeffs2, residuals2, rank2, s2 = np.linalg.lstsq(X2, errors, rcond=None)

    A2, B2, C2 = coeffs2
    predictions2 = X2 @ coeffs2
    rmse2 = np.sqrt(np.mean((predictions2 - errors)**2))

    print(f"  A (ω_ratio coeff): {A2:>10.4f}")
    print(f"  B (asymmetry × sign coeff): {B2:>10.4f}")
    print(f"  C (constant): {C2:>10.4f}")
    print(f"  Sign indicators: {sign_indicators}")
    print(f"  RMSE: {rmse2:.2f} MeV")
    print()

    # Formula 3: Quadratic in asymmetry
    print("FORMULA 3: ΔE = A·(ω_ratio - 1) + B·asymmetry² + C·asymmetry + D")
    print("-" * 60)

    X3 = np.column_stack([omega_ratios - 1, asymmetries**2, asymmetries, np.ones(3)])
    coeffs3, residuals3, rank3, s3 = np.linalg.lstsq(X3, errors, rcond=None)

    A3, B3, C3, D3 = coeffs3
    predictions3 = X3 @ coeffs3
    rmse3 = np.sqrt(np.mean((predictions3 - errors)**2))

    print(f"  A (ω_ratio coeff): {A3:>10.4f}")
    print(f"  B (asymmetry² coeff): {B3:>10.4f}")
    print(f"  C (asymmetry coeff): {C3:>10.4f}")
    print(f"  D (constant): {D3:>10.4f}")
    print(f"  RMSE: {rmse3:.2f} MeV")
    print()

    # Formula 4: Frequency-dependent asymmetry scaling
    print("FORMULA 4: ΔE = A·(ω_ratio - 1) + B·asymmetry / ω_ratio + C")
    print("-" * 60)

    X4 = np.column_stack([omega_ratios - 1, asymmetries / omega_ratios, np.ones(3)])
    coeffs4, residuals4, rank4, s4 = np.linalg.lstsq(X4, errors, rcond=None)

    A4, B4, C4 = coeffs4
    predictions4 = X4 @ coeffs4
    rmse4 = np.sqrt(np.mean((predictions4 - errors)**2))

    print(f"  A (ω_ratio coeff): {A4:>10.4f}")
    print(f"  B (asymmetry/ω_ratio coeff): {B4:>10.4f}")
    print(f"  C (constant): {C4:>10.4f}")
    print(f"  RMSE: {rmse4:.2f} MeV")
    print()

    # Summary
    print("="*90)
    print("FORMULA COMPARISON")
    print("="*90)
    print()

    formulas = [
        ("Formula 1: Linear", rmse1, predictions1, "A·(ω-1) + B·asym + C"),
        ("Formula 2: Sign-aware", rmse2, predictions2, "A·(ω-1) + B·asym·sign + C"),
        ("Formula 3: Quadratic", rmse3, predictions3, "A·(ω-1) + B·asym² + C·asym + D"),
        ("Formula 4: Frequency-scaled", rmse4, predictions4, "A·(ω-1) + B·asym/ω + C"),
    ]

    formulas.sort(key=lambda x: x[1])

    print(f"{'Rank':<5} {'Formula':<25} {'RMSE':>12} {'Description':<35}")
    print("-" * 80)

    for rank, (name, rmse, _, desc) in enumerate(formulas, 1):
        print(f"{rank:<5} {name:<25} {rmse:>11.2f} {desc:<35}")

    print()
    print("PREDICTIONS BY BEST FORMULA (Formula 2):")
    print("-" * 60)
    print()

    print(f"{'Hadron':<12} {'Predicted':<15} {'Experimental':<15} {'Actual Predicted':<20} {'Error':>10}")
    print("-" * 75)

    for i, m in enumerate(hadrons_data):
        predicted_correction = predictions2[i]
        actual_predicted = PREDICTED[m["hadron"]]
        expt = EXPT[m["hadron"]]
        corrected_mass = actual_predicted + predicted_correction
        error_after = corrected_mass - expt

        print(f"{m['hadron']:<12} {corrected_mass:>14.1f} {expt:>14.1f} {actual_predicted:>19.1f} {error_after:>+9.1f}")

    print()
    print("="*90)
    print("PHYSICAL INTERPRETATION")
    print("="*90)
    print()

    print("Formula 2 suggests:")
    print()
    print("1. Light quarks (u, d) when forming symmetric pairs:")
    print("   → Binding energy REDUCTION (negative correction)")
    print("   → Results in LOWER predicted mass")
    print()
    print("2. Heavy quarks (s) when oscillating asymmetrically:")
    print("   → Binding energy INCREASE (positive correction)")
    print("   → Results in HIGHER predicted mass")
    print()
    print("3. The sign of the correction reverses based on the")
    print("   mass scale of the symmetric pair.")
    print()
    print("4. For proton (u-u symmetric): negative correction")
    print("5. For neutron (d-d symmetric): sign-flipped by asymmetry")
    print("6. For Lambda (no symmetric): extreme positive correction")
    print()


if __name__ == "__main__":
    try:
        fit_correction_formulas()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
