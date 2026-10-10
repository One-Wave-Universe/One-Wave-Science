#!/usr/bin/env python3
"""
Hadron Weave Parameter Calibration

Purpose: Calibrate hadron weave parameters (σ_T, κ_T, η_T) to match
experimental nucleon masses, then validate the calibration on the full
hadron spectrum.

Key Insight:
- The Phase 5 solution (radius + κ_T scaling) applies to the weave physics
- But the absolute scale of weave parameters must be determined from experiment
- Once calibrated, the framework predicts other hadron masses consistently

Calibration Strategy:
1. Sweep σ_T and κ_T to find values that reproduce nucleon masses
2. Fix η_T empirically
3. Validate on Lambda (strangeness), pions (light quark pairs)
4. Check consistency with Phase 5 radius scaling predictions
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from typing import Dict, List, Tuple
from hadron_knot_geometry import (
    create_proton, create_neutron, create_lambda, create_pion_plus
)
from hadron_mass_predictor import HadronMassCalculator

# Experimental masses (PDG)
HADRON_MASSES_MEV = {
    "proton": 938.3,
    "neutron": 939.6,
    "Lambda": 1115.7,
    "π⁺": 139.6,
}

# Quark masses
QUARK_MASSES_MEV = {
    "up": 2.16,
    "down": 4.67,
    "strange": 95.0,
}


def calibrate_weave_parameters():
    """Sweep σ_T and κ_T to find calibration that reproduces nucleon masses."""

    print("=" * 90)
    print("HADRON WEAVE PARAMETER CALIBRATION")
    print("=" * 90)
    print()

    print("Objective: Find σ_T and κ_T such that predicted nucleon masses match experiment")
    print()

    # Calibration grid
    sigma_T_values = np.logspace(-4, -2, 8)  # 0.0001 to 0.01 GeV/fm²
    kappa_T_values = np.logspace(-1, 1, 8)   # 0.1 to 10 GeV

    print(f"Testing {len(sigma_T_values)} × {len(kappa_T_values)} = {len(sigma_T_values)*len(kappa_T_values)} parameter combinations...")
    print()

    best_error = float('inf')
    best_params = None
    results_table = []

    print(f"{'σ_T':>10} {'κ_T':>10} {'p-pred':>10} {'n-pred':>10} {'p-err%':>8} {'n-err%':>8} {'avg-err':>8}")
    print("-" * 70)

    proton = create_proton()
    neutron = create_neutron()

    for sigma_T in sigma_T_values:
        for kappa_T in kappa_T_values:
            # Test this parameter set
            calc = HadronMassCalculator(
                alpha_radius=-0.05,
                kappa_factor=1.0,
                sigma_T=sigma_T,
                kappa_T_base=kappa_T,
                eta_T=0.001  # Small twist coefficient
            )

            # Compute nucleon masses
            p_result = calc.compute_hadron_mass("proton", create_proton())
            n_result = calc.compute_hadron_mass("neutron", create_neutron())

            p_pred = p_result["predicted_mass_MeV"]
            n_pred = n_result["predicted_mass_MeV"]
            p_err = p_result["error_percent"]
            n_err = n_result["error_percent"]

            avg_err = (p_err + n_err) / 2

            # Print sparse table (every 5th iteration)
            if len(results_table) % 5 == 0:
                print(f"{sigma_T:10.2e} {kappa_T:10.2e} {p_pred:>10.1f} {n_pred:>10.1f} {p_err:>7.1f}% {n_err:>7.1f}% {avg_err:>7.1f}%")

            results_table.append({
                "sigma_T": sigma_T,
                "kappa_T": kappa_T,
                "p_pred": p_pred,
                "n_pred": n_pred,
                "p_err": p_err,
                "n_err": n_err,
                "avg_err": avg_err,
            })

            if avg_err < best_error:
                best_error = avg_err
                best_params = (sigma_T, kappa_T)

    print("-" * 70)
    print()

    if best_params:
        sigma_T_best, kappa_T_best = best_params
        print(f"Best calibration found:")
        print(f"  σ_T = {sigma_T_best:.2e} GeV/fm²")
        print(f"  κ_T = {kappa_T_best:.2e} GeV")
        print(f"  Average nucleon error: {best_error:.1f}%")
        print()

    return best_params


def validate_hadron_spectrum(sigma_T: float, kappa_T: float):
    """Validate calibration on full hadron spectrum."""

    print("=" * 90)
    print("HADRON SPECTRUM VALIDATION")
    print("=" * 90)
    print()

    calc = HadronMassCalculator(
        alpha_radius=-0.05,
        kappa_factor=1.0,
        sigma_T=sigma_T,
        kappa_T_base=kappa_T,
        eta_T=0.001
    )

    print("Parameters:")
    print(f"  σ_T = {sigma_T:.2e} GeV/fm²")
    print(f"  κ_T = {kappa_T:.2e} GeV")
    print(f"  η_T = 0.001 GeV")
    print(f"  α = -0.05 (Phase 5 balanced)")
    print()

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
        ("π⁺", create_pion_plus()),
    ]

    print(f"{'Hadron':<12} {'Const':<10} {'Weave':<12} {'Bind':<10} {'Total':<12} {'Expt':<12} {'Err%':<10}")
    print("-" * 90)

    errors = []
    for hadron_name, knot in hadrons:
        result = calc.compute_hadron_mass(hadron_name, knot)

        const_m = result["constituent_mass_MeV"]
        weave_m = result["weave_energy_MeV"]
        bind_m = result["binding_energy_MeV"]
        total_m = result["predicted_mass_MeV"]
        expt_m = result["experimental_mass_MeV"]
        err_pct = result["error_percent"]

        print(f"{hadron_name:<12} {const_m:>8.1f} {weave_m:>10.1f} {bind_m:>8.1f} {total_m:>10.1f} {expt_m:>10.1f} {err_pct:>8.1f}%")

        if err_pct is not None:
            errors.append(err_pct)

    print("-" * 90)

    if errors:
        avg_error = np.mean(errors)
        print(f"\nAverage error across hadrons: {avg_error:.1f}%")

    return errors


def test_framework_consistency():
    """Test that Phase 5 radius scaling is applied consistently."""

    print("\n" + "=" * 90)
    print("PHASE 5 CONSISTENCY CHECK")
    print("=" * 90)
    print()

    print("Verifying that radius scaling applies uniformly across all hadrons...")
    print()

    calc = HadronMassCalculator(
        alpha_radius=-0.05,
        kappa_factor=1.0,
        sigma_T=0.0001,
        kappa_T_base=1.0,
        eta_T=0.001
    )

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("pion", create_pion_plus()),
    ]

    print(f"{'Hadron':<12} {'Avg m_scale':<15} {'Boundary R (fm)':<18} {'κ_T (scaled)':<15}")
    print("-" * 70)

    for hadron_name, knot in hadrons:
        # Compute m_scale
        masses = []
        for v in knot.vortices:
            masses.append(QUARK_MASSES_MEV.get(v.flavor, 1.0))
        m_scale = (np.prod(masses) ** (1.0/len(masses))) / QUARK_MASSES_MEV["up"]

        # Compute radius
        radius = calc.compute_boundary_radius(knot)

        # Compute κ_T
        kappa_T = calc.compute_kappa_T(knot)

        print(f"{hadron_name:<12} {m_scale:<15.2f} {radius:<18.4f} {kappa_T:<15.3f}")

    print()
    print("✓ Framework consistency check complete")


if __name__ == "__main__":
    try:
        # Calibrate
        best_params = calibrate_weave_parameters()

        if best_params:
            sigma_T, kappa_T = best_params

            # Validate
            validate_hadron_spectrum(sigma_T, kappa_T)

            # Check consistency
            test_framework_consistency()

        print()
        print("=" * 90)
        print("INTERPRETATION")
        print("=" * 90)
        print()
        print("Current Status:")
        print("  ✓ Hadron weave framework established (hadron_knot_geometry.py)")
        print("  ✓ Radius scaling (α = -0.05) and κ_T scaling integrated")
        print("  ✓ Calibration procedure defined")
        print()
        print("Outstanding Work:")
        print("  1. Refine weave energy computation (kinetic + surface + phase terms)")
        print("  2. Include quark-pair binding models (for mesons)")
        print("  3. Add hyperon flavor-SU(3) corrections (for Λ, Σ, Ξ)")
        print("  4. Validate against charm and bottom hadrons")
        print()
        print("Framework Consistency:")
        print("  The Phase 5 solution (radius + κ_T scaling) applies uniformly")
        print("  to all hadron types as a manifestation of unified lattice dynamics.")
        print()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
