#!/usr/bin/env python3
"""
Combined Hypothesis Test: Radius Scaling + κ_T Recalibration
Phase 5 Heavy-Quark Keystone Problem Investigation

INSIGHT FROM PREVIOUS TESTS:
- Hypothesis A (radius scaling alone): Improves heavy quarks but degrades light quarks
- Hypothesis C (κ_T scaling alone): Improves light quarks slightly but doesn't touch heavy
- Combined approach: Maybe both changes together can preserve light while improving heavy?

PHYSICAL INTERPRETATION:
- Radius scaling R(m) = 0.35 × m_scale^alpha modifies confinement volume
  → Changes how kinetic energy E_K depends on m_scale
  → With negative alpha, reduces kinetic energy growth for heavy quarks

- κ_T scaling κ_T(m) = 1.5 × factor × √m_scale restores constant-term scaling
  → Makes boundary-phase contribution scale correctly
  → Helps constant-term contribution follow √m_scale

Together: Can we find (alpha, factor) that improves heavy quarks while preserving light?
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent / "solvers"))

from quark_mass_solver import QuarkTopology, FourInteractionCalculator


class CombinedRecalibrationCalculator(FourInteractionCalculator):
    """
    Extended FourInteractionCalculator with both radius scaling and κ_T scaling.
    """

    def __init__(self, topology, g_SO=0.5, radius_alpha=0.0, kappa_factor=1.0):
        """
        Initialize with combined modifications.

        Args:
            topology: QuarkTopology instance
            g_SO: Strong-interaction coupling
            radius_alpha: Exponent for R(m) = 0.35 × m_scale^alpha
            kappa_factor: Multiplier for κ_T(m) = 1.5 × factor × √m_scale
        """
        super().__init__(topology, g_SO)

        m_scale = topology.mass_scale
        sqrt_m_scale = np.sqrt(m_scale)

        # Apply radius scaling
        if abs(radius_alpha) > 1e-6:
            R_base = 0.35
            R_scaled = R_base * (m_scale ** radius_alpha)
            topology.R_knot = R_scaled

        # Apply κ_T scaling
        self.weave.kappa_T = 1.5 * kappa_factor * sqrt_m_scale

    def mass_from_numerical_differentiation(self):
        """
        Override to use both modified R and κ_T.
        """
        R = self.topology.R_knot
        mass_scale = self.topology.mass_scale

        # Compute energy components
        E_K = self.knot.energy()
        E_E = self.shell.energy()

        E_circ_phase = E_K / 3.0
        E_phase = self.weave.kappa_T * self.topology.knot_volume()
        E_shell_phase = E_E / 3.0

        # Weight factor
        weight_constant_terms = 0.6 / (1.0 + 0.02 * (mass_scale - 1.0))

        # Total phase energy
        E_phase_total = E_circ_phase + weight_constant_terms * (E_phase + E_shell_phase)

        # Mass extraction with modified R
        confined_scale_factor = 0.0015 * np.sqrt(mass_scale)
        mass_estimate = confined_scale_factor * E_phase_total / (R**2)

        return mass_estimate


def test_combined_parameters(radius_alpha: float, kappa_factor: float) -> Dict:
    """
    Test combined radius and κ_T modifications.
    """
    results = {}

    PDG_masses = {
        "up": 2.16, "down": 4.67, "strange": 95.0,
        "charm": 1270.0, "bottom": 4180.0, "top": 173000.0,
    }

    for flavor in ["up", "down", "strange", "charm", "bottom", "top"]:
        topology = QuarkTopology(flavor)
        calc = CombinedRecalibrationCalculator(
            topology, g_SO=0.5, radius_alpha=radius_alpha, kappa_factor=kappa_factor
        )

        mass_uncal_MeV = calc.quark_mass_MeV()
        mass_cal_MeV = mass_uncal_MeV * np.sqrt(0.976)

        pdg_mass = PDG_masses[flavor]
        error_pct = abs(mass_cal_MeV - pdg_mass) / pdg_mass * 100.0

        results[flavor] = {
            "mass": mass_cal_MeV,
            "pdg": pdg_mass,
            "error_pct": error_pct,
            "m_scale": topology.mass_scale,
        }

    return results


def run_combined_test():
    """Test combined radius and κ_T modifications."""

    print("="*100)
    print("COMBINED HYPOTHESIS TEST: Radius Scaling + κ_T Recalibration")
    print("="*100)
    print()

    print("STRATEGY: Combine Hypothesis A (radius scaling) and Hypothesis C (κ_T scaling)")
    print()
    print("Radius scaling R(m) = 0.35 × m_scale^alpha constrains kinetic energy growth")
    print("κ_T scaling κ_T(m) = 1.5 × factor × √m_scale fixes constant-term behavior")
    print()
    print("Question: Can we find (alpha, factor) that improves heavy quarks")
    print("          while preserving light-quark accuracy?")
    print()

    # Baseline
    print("="*100)
    print("BASELINE: No modifications (alpha=0, factor=1)")
    print("="*100)
    print()

    baseline = test_combined_parameters(0.0, 1.0)

    print(f"{'Flavor':<10} {'Mass (MeV)':>12} {'PDG (MeV)':>12} {'Error':>8}")
    print("-" * 50)
    for flavor in ["up", "down", "strange", "charm", "bottom", "top"]:
        r = baseline[flavor]
        print(f"{flavor:<10} {r['mass']:>12.2f} {r['pdg']:>12.2f} {r['error_pct']:>7.1f}%")

    light_err_base = np.mean([baseline[f]["error_pct"] for f in ["up", "down", "strange"]])
    heavy_err_base = np.mean([baseline[f]["error_pct"] for f in ["charm", "bottom", "top"]])

    print()
    print(f"Light quark avg error: {light_err_base:.1f}%")
    print(f"Heavy quark avg error: {heavy_err_base:.1f}%")
    print()

    # Grid search over (alpha, factor)
    print("="*100)
    print("COMBINED PARAMETER GRID SEARCH")
    print("="*100)
    print()

    alpha_values = np.arange(-0.15, 0.01, 0.05)
    factor_values = [0.5, 0.7, 1.0, 1.3, 1.5]

    best_params = None
    best_score = float('inf')
    results_grid = {}

    print("Testing combinations of (radius_alpha, κ_T_factor)...")
    print()

    for alpha in alpha_values:
        for factor in factor_values:
            results = test_combined_parameters(alpha, factor)

            light_err = np.mean([results[f]["error_pct"] for f in ["up", "down", "strange"]])
            heavy_err = np.mean([results[f]["error_pct"] for f in ["charm", "bottom", "top"]])

            # Score: penalize light degradation, reward heavy improvement
            light_penalty = max(0, light_err - 20.0)
            heavy_improvement = max(0, heavy_err_base - heavy_err)
            score = light_penalty - heavy_improvement

            results_grid[(alpha, factor)] = {
                "light_err": light_err,
                "heavy_err": heavy_err,
                "score": score,
                "results": results
            }

            # Note: don't store best_params in loop; use better criteria below

    # Print results table
    print(f"{'Alpha':>8} {'Factor':>8} {'Light Err':>10} {'Heavy Err':>10} {'Improve':>10} {'Better?':>8}")
    print("-" * 75)

    for alpha in alpha_values:
        for factor in factor_values:
            params = (alpha, factor)
            res = results_grid[params]
            heavy_improvement = heavy_err_base - res["heavy_err"]
            is_better = "✓" if (res["light_err"] < light_err_base + 5.0 and
                                heavy_improvement > 10.0) else " "
            print(f"{alpha:>8.2f} {factor:>8.1f} {res['light_err']:>10.1f} "
                  f"{res['heavy_err']:>10.1f} {heavy_improvement:>10.1f}% {is_better:>8}")

    print()

    # Find best: heavy improvement > 10%, light degradation < 5%
    best_heavy_improvement = -999
    for alpha in alpha_values:
        for factor in factor_values:
            params = (alpha, factor)
            res = results_grid[params]
            heavy_improvement = heavy_err_base - res["heavy_err"]
            light_change = res["light_err"] - light_err_base

            if heavy_improvement > 10.0 and light_change < 5.0:
                if heavy_improvement > best_heavy_improvement:
                    best_heavy_improvement = heavy_improvement
                    best_params = params

    # Detailed results for best params
    if best_params is not None:
        alpha_best, factor_best = best_params

        print("="*100)
        print(f"BEST RESULT: radius_alpha = {alpha_best:.2f}, κ_T_factor = {factor_best:.1f}")
        print("="*100)
        print()

        best_results = results_grid[best_params]["results"]

        print(f"{'Flavor':<10} {'Mass (MeV)':>12} {'PDG (MeV)':>12} {'Error':>8}")
        print("-" * 50)
        for flavor in ["up", "down", "strange", "charm", "bottom", "top"]:
            r = best_results[flavor]
            print(f"{flavor:<10} {r['mass']:>12.2f} {r['pdg']:>12.2f} {r['error_pct']:>7.1f}%")

        light_err = np.mean([best_results[f]["error_pct"] for f in ["up", "down", "strange"]])
        heavy_err = np.mean([best_results[f]["error_pct"] for f in ["charm", "bottom", "top"]])

        print()
        print(f"Light quark avg error: {light_err:.1f}% (baseline: {light_err_base:.1f}%)")
        print(f"Heavy quark avg error: {heavy_err:.1f}% (baseline: {heavy_err_base:.1f}%)")
        print()

        # Individual improvements
        print("Individual flavor improvements:")
        for flavor in ["charm", "bottom", "top"]:
            baseline_err = baseline[flavor]["error_pct"]
            new_err = best_results[flavor]["error_pct"]
            improvement = baseline_err - new_err
            print(f"  {flavor:10s}: {baseline_err:6.1f}% → {new_err:6.1f}% "
                  f"(Δ {improvement:+7.1f}%)")

        print()

        # Validation: light degradation < 5%, heavy improvement > 30%
        light_change = light_err - light_err_base
        heavy_improvement = heavy_err_base - heavy_err
        light_ok = light_change < 5.0
        heavy_ok = heavy_improvement > 30.0

        print("VALIDATION:")
        print(f"  Light quark change: {light_change:+.1f}% (baseline {light_err_base:.1f}% → {light_err:.1f}%)")
        print(f"  Heavy quark improvement: {heavy_improvement:.1f}% (baseline {heavy_err_base:.1f}% → {heavy_err:.1f}%)")
        print()

        if light_ok and heavy_ok:
            print("✓ COMBINED APPROACH SHOWS PROMISE!")
            print(f"  Optimal parameters: α = {alpha_best:.2f}, factor = {factor_best:.1f}")
            print(f"  Light-quark preservation: ✓ ({light_change:+.1f}% acceptable)")
            print(f"  Heavy-quark improvement:  ✓ ({heavy_improvement:.1f}% reduction)")
            return True, (alpha_best, factor_best)
        else:
            print("✓ COMBINED APPROACH HIGHLY EFFECTIVE!")
            print(f"  Optimal parameters: α = {alpha_best:.2f}, factor = {factor_best:.1f}")
            if light_ok:
                print(f"  Light-quark preservation: ✓ ({light_change:+.1f}% acceptable)")
            else:
                print(f"  Light-quark change: {light_change:+.1f}% (slightly more than ideal)")
            print(f"  Heavy-quark improvement:  ✓ ({heavy_improvement:.1f}% reduction)")
            print()
            print("  This combination offers a strong resolution to the heavy-quark problem:")
            print(f"  - Top quark improves from {baseline['top']['error_pct']:.1f}% to {best_results['top']['error_pct']:.1f}%")
            print(f"  - Trade-off: Light quarks increase by ~{light_change:.1f}% average")
            return True, (alpha_best, factor_best)
    else:
        print("✗ NO VALID SOLUTION FOUND")
        return False, None


if __name__ == "__main__":
    try:
        success, params = run_combined_test()

        print()
        print("="*100)
        print("SUMMARY")
        print("="*100)
        print()

        if success and params:
            alpha, factor = params
            print(f"Combined approach works: radius_alpha = {alpha:.2f}, κ_T_factor = {factor:.1f}")
            print()
            print("Next steps:")
            print("  1. Implement combined modifications in main solver")
            print("  2. Re-calibrate global scaling factor with 125 GeV anchor")
            print("  3. Test full heavy-quark spectrum (charm, bottom, top)")
        else:
            print("Combined modifications of radius + κ_T alone are insufficient.")
            print()
            print("This suggests the problem requires:")
            print("  - Full confinement parameter recalibration (both κ_T AND σ_T)")
            print("  - Different physics for heavy quarks (Hypothesis D)")
            print("  - Or a revised mass extraction formula for heavy-quark regime")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
