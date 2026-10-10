#!/usr/bin/env python3
"""
Calibrate Phase 5 parameters for coherence-modulated phase-locking mechanism

After implementing oscillation decoherence in phase_locking_energy(),
the energy scale has shifted. This script finds optimal σ_T, κ_T_base,
and binding_correction_strength values that minimize hadron mass errors.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from hadron_knot_geometry import create_proton, create_neutron, create_lambda
from hadron_mass_predictor import HadronMassCalculator

HADRON_MASSES_MEV = {
    "proton": 938.3,
    "neutron": 939.6,
    "Lambda": 1115.7,
}

def test_parameter_set(kappa_T_base, sigma_T, binding_correction_strength):
    """Test a parameter set and return average error."""

    calc = HadronMassCalculator(
        alpha_radius=-0.05,
        kappa_factor=1.0,
        sigma_T=sigma_T,
        kappa_T_base=kappa_T_base,
        eta_T=0.01,
        binding_correction_strength=binding_correction_strength
    )

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    errors = []
    for hadron_name, knot in hadrons:
        result = calc.compute_hadron_mass(hadron_name, knot)
        if result["error_percent"] is not None:
            errors.append(result["error_percent"])

    return np.mean(errors) if errors else 1000.0

def main():
    print("="*90)
    print("COHERENCE PARAMETER CALIBRATION")
    print("="*90)
    print()

    print("Sweeping parameter space to find optimal values...")
    print("(This may take a minute...)")
    print()

    # Parameter ranges
    kappa_T_values = np.linspace(0.15, 0.50, 8)  # GeV
    sigma_T_values = np.linspace(0.005, 0.025, 5)  # GeV/fm²
    binding_correction_values = np.linspace(0.5, 2.0, 7)  # Strength factor

    best_error = float('inf')
    best_params = None
    results = []

    print(f"{'κ_T_base':>10} {'σ_T':>10} {'Binding':>10} {'Avg Error':>10}")
    print("-" * 45)

    for kappa_T in kappa_T_values:
        for sigma_T in sigma_T_values:
            for binding_corr in binding_correction_values:
                avg_error = test_parameter_set(kappa_T, sigma_T, binding_corr)

                results.append({
                    "kappa_T_base": kappa_T,
                    "sigma_T": sigma_T,
                    "binding_correction_strength": binding_corr,
                    "avg_error": avg_error,
                })

                if avg_error < best_error:
                    best_error = avg_error
                    best_params = (kappa_T, sigma_T, binding_corr)
                    print(f"{kappa_T:>10.3f} {sigma_T:>10.5f} {binding_corr:>10.3f} {avg_error:>10.2f} *")

    print()
    print("="*90)
    print("BEST FIT")
    print("="*90)
    print()

    if best_params:
        kappa_T_best, sigma_T_best, binding_best = best_params

        print(f"Best parameters found:")
        print(f"  κ_T_base: {kappa_T_best:.4f} GeV")
        print(f"  σ_T: {sigma_T_best:.5f} GeV/fm²")
        print(f"  Binding correction strength: {binding_best:.3f}")
        print(f"  Average error: {best_error:.2f}%")
        print()

        # Show predictions with best parameters
        calc = HadronMassCalculator(
            alpha_radius=-0.05,
            kappa_factor=1.0,
            sigma_T=sigma_T_best,
            kappa_T_base=kappa_T_best,
            eta_T=0.01,
            binding_correction_strength=binding_best
        )

        hadrons = [
            ("proton", create_proton()),
            ("neutron", create_neutron()),
            ("Lambda", create_lambda()),
        ]

        print(f"{'Hadron':<12} {'Predicted':>12} {'Experimental':>15} {'Error MeV':>12} {'Error %':>10}")
        print("-" * 70)

        for hadron_name, knot in hadrons:
            result = calc.compute_hadron_mass(hadron_name, knot)
            pred = result["predicted_mass_MeV"]
            expt = result["experimental_mass_MeV"]
            err_mev = result["error_MeV"]
            err_pct = result["error_percent"]

            print(f"{hadron_name:<12} {pred:>11.1f} {expt:>15.1f} {err_mev:>+11.1f} {err_pct:>+9.2f}%")

        print()

        # Show top 10 best parameter sets
        print("="*90)
        print("TOP 10 PARAMETER SETS (ranked by error)")
        print("="*90)
        print()

        results.sort(key=lambda x: x["avg_error"])

        print(f"{'Rank':<5} {'κ_T_base':>10} {'σ_T':>10} {'Binding':>10} {'Avg Error':>10}")
        print("-" * 50)

        for i, r in enumerate(results[:10], 1):
            print(f"{i:<5} {r['kappa_T_base']:>10.3f} {r['sigma_T']:>10.5f} "
                  f"{r['binding_correction_strength']:>10.3f} {r['avg_error']:>10.2f}%")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
