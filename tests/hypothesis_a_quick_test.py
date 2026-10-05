#!/usr/bin/env python3
"""
Quick Hypothesis A Test: Does confinement radius scaling improve heavy-quark predictions?

This test temporarily modifies the solver to test different radius scaling exponents.
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent / "solvers"))

from quark_mass_solver import QuarkTopology, QuarkMassSpectrum, FourInteractionCalculator


def test_radius_scaling_hypothesis():
    """Test if radius scaling R(m) = 0.35 × m_scale^alpha improves predictions."""

    print("="*80)
    print("HYPOTHESIS A QUICK TEST: Non-Universal Confinement Radius")
    print("="*80)
    print()

    print("Testing: Does R(m_scale) = 0.35 × m_scale^alpha improve quark mass predictions?")
    print()

    # Test baseline (alpha = 0, current R = 0.35 fm for all)
    print("BASELINE: alpha = 0.0 (R = 0.35 fm for all quarks)")
    print("-" * 80)

    baseline_results = {}
    for flavor in ["up", "down", "strange", "charm", "bottom", "top"]:
        topology = QuarkTopology(flavor)
        calc = FourInteractionCalculator(topology, g_SO=0.5)
        mass_uncal_MeV = calc.quark_mass_MeV()

        # Apply calibration λ = 0.976
        lambda_scale = 0.976
        mass_cal_MeV = mass_uncal_MeV * np.sqrt(lambda_scale)

        PDG_masses = {
            "up": 2.16, "down": 4.67, "strange": 95.0,
            "charm": 1270.0, "bottom": 4180.0, "top": 173000.0,
        }
        pdg_mass = PDG_masses[flavor]
        error_pct = abs(mass_cal_MeV - pdg_mass) / pdg_mass * 100.0

        baseline_results[flavor] = {
            "mass": mass_cal_MeV,
            "pdg": pdg_mass,
            "error_pct": error_pct,
            "R_knot": 0.35,
        }

        print(f"{flavor:10s}: m={mass_cal_MeV:10.2f} MeV, PDG={pdg_mass:10.2f}, error={error_pct:6.1f}%")

    light_error = np.mean([baseline_results[f]["error_pct"] for f in ["up", "down", "strange"]])
    heavy_error = np.mean([baseline_results[f]["error_pct"] for f in ["charm", "bottom", "top"]])

    print()
    print(f"Light quark avg error (u/d/s): {light_error:.1f}%")
    print(f"Heavy quark avg error (c/b/t): {heavy_error:.1f}%")
    print()

    # Now test radius scaling
    print("RADIUS SCALING TEST:")
    print("-" * 80)
    print("Testing if R(m_scale) = 0.35 × m_scale^alpha improves heavy quarks")
    print()

    alpha_values = [-0.20, -0.15, -0.10, -0.05, 0.0, 0.05, 0.10, 0.15, 0.20]

    print(f"{'α':>6} {'Light Err':>10} {'Heavy Err':>10} {'Score':>10}")
    print("-" * 40)

    best_alpha = None
    best_score = float('inf')

    for alpha in alpha_values:
        # Compute masses with modified radius
        total_light_error = 0
        total_heavy_error = 0

        for flavor in ["up", "down", "strange", "charm", "bottom", "top"]:
            topology = QuarkTopology(flavor)

            # Modify radius: R(m) = R_base × m_scale^alpha
            if abs(alpha) > 1e-6:
                R_base = 0.35
                R_scaled = R_base * (topology.mass_scale ** alpha)
                topology.R_knot = R_scaled

            calc = FourInteractionCalculator(topology, g_SO=0.5)
            mass_uncal_MeV = calc.quark_mass_MeV()
            mass_cal_MeV = mass_uncal_MeV * np.sqrt(0.976)

            PDG_masses = {
                "up": 2.16, "down": 4.67, "strange": 95.0,
                "charm": 1270.0, "bottom": 4180.0, "top": 173000.0,
            }
            pdg_mass = PDG_masses[flavor]
            error_pct = abs(mass_cal_MeV - pdg_mass) / pdg_mass * 100.0

            if flavor in ["up", "down", "strange"]:
                total_light_error += error_pct
            else:
                total_heavy_error += error_pct

        light_err = total_light_error / 3.0
        heavy_err = total_heavy_error / 3.0

        # Score: light penalty + heavy improvement
        light_penalty = max(0, light_err - 20.0)
        heavy_improvement = max(0, heavy_error - heavy_err)
        score = light_penalty - heavy_improvement

        print(f"{alpha:+6.2f} {light_err:10.1f} {heavy_err:10.1f} {score:10.2f}")

        # Track best (must preserve light quarks)
        if light_err < 25.0 and score < best_score:
            best_score = score
            best_alpha = alpha

    print()
    print("="*80)

    if best_alpha is not None and abs(best_alpha) > 0.01:
        print(f"RESULT: Best α = {best_alpha:+.2f}")
        print("Hypothesis A PARTIALLY SUPPORTED: Radius scaling shows some improvement")
        print()
        print("Next: Test if this radius scaling is physically justified")
        return True, best_alpha
    else:
        print("RESULT: No significant improvement from radius scaling")
        print("Hypothesis A REJECTED: Radius scaling does not solve heavy-quark problem")
        print()
        print("Next: Move to Hypothesis B (weight-factor analysis)")
        return False, None


if __name__ == "__main__":
    success, best_alpha = test_radius_scaling_hypothesis()
    sys.exit(0 if success else 1)
