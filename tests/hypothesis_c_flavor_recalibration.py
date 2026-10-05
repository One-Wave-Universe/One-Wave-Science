#!/usr/bin/env python3
"""
Hypothesis C Test: Flavor-Dependent Confinement Parameter Recalibration
Phase 5 Heavy-Quark Keystone Problem Investigation

HYPOTHESIS: The confinement parameters (κ_T, σ_T, E_T) scale with mass but are currently
fixed for all flavors. Recalibrating these per-flavor can restore octave-scaling.

ROOT CAUSE (from energy analysis):
- E_phase = κ_T × V_knot is constant for all flavors despite 80000× mass variation
- E_shell is also approximately constant
- These should scale as √m_scale to maintain octave-scaling
- Current framework assumes universal confinement (R, κ_T, σ_T same for all)

TEST STRATEGY:
Instead of universal κ_T, use κ_T(m_scale) = κ_T_base × √m_scale
This makes E_phase scale correctly: E_phase(m) = κ_T_base × √m_scale × V_knot

Test by modifying FourInteractionCalculator to accept flavor-dependent κ_T.
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict, Callable

sys.path.insert(0, str(Path(__file__).parent.parent / "solvers"))

from quark_mass_solver import QuarkTopology, FourInteractionCalculator
import quark_mass_solver


class FlavorDependentFourInteractionCalculator(FourInteractionCalculator):
    """
    Extended FourInteractionCalculator with flavor-dependent confinement parameters.

    Modifies κ_T to scale with √m_scale: κ_T(m) = κ_T_base × √m_scale
    This makes E_phase scale correctly for octave-scaling.
    """

    def __init__(self, topology, g_SO=0.5, kappa_scale_factor=1.0):
        """
        Initialize with flavor-dependent κ_T.

        Args:
            topology: QuarkTopology instance
            g_SO: Strong-interaction coupling
            kappa_scale_factor: Multiplier for κ_T scaling (1.0 = no modification)
        """
        super().__init__(topology, g_SO)
        self.kappa_scale_factor = kappa_scale_factor

        # Modify weave κ_T to scale with √m_scale
        # Original: κ_T = 1.5 for all flavors
        # Modified: κ_T = 1.5 × kappa_scale_factor × √m_scale
        m_scale = topology.mass_scale
        sqrt_m_scale = np.sqrt(m_scale)

        # Apply flavor-dependent scaling
        self.weave.kappa_T = 1.5 * kappa_scale_factor * sqrt_m_scale

    def mass_from_numerical_differentiation(self):
        """
        Override to use flavor-dependent κ_T in energy calculation.
        """
        # Get the modified κ_T (already set in __init__)
        # Rest of calculation proceeds normally with scaled κ_T

        R = self.topology.R_knot
        mass_scale = self.topology.mass_scale

        # Compute energy components with modified κ_T
        E_K = self.knot.energy()
        E_E = self.shell.energy()
        E_M = self.mirror.energy()
        E_T = self.weave.energy()

        E_circ_phase = E_K / 3.0

        # CRITICAL: E_phase now includes scaled κ_T
        E_phase = self.weave.kappa_T * self.topology.knot_volume()
        E_shell_phase = E_E / 3.0

        # Weight factor (same as before)
        weight_constant_terms = 0.6 / (1.0 + 0.02 * (mass_scale - 1.0))

        # Total phase energy (with scaled κ_T contribution)
        E_phase_total = E_circ_phase + weight_constant_terms * (E_phase + E_shell_phase)

        # Mass extraction (standard formula)
        confined_scale_factor = 0.0015 * np.sqrt(mass_scale)
        mass_estimate = confined_scale_factor * E_phase_total / (R**2)

        return mass_estimate


def test_flavor_recalibration(kappa_scale_factor: float) -> Dict:
    """
    Test flavor-dependent recalibration with given κ_T scaling.

    Args:
        kappa_scale_factor: Multiplier for κ_T × √m_scale scaling

    Returns:
        Dict with flavor -> {mass, pdg, error_pct}
    """
    results = {}

    PDG_masses = {
        "up": 2.16, "down": 4.67, "strange": 95.0,
        "charm": 1270.0, "bottom": 4180.0, "top": 173000.0,
    }

    for flavor in ["up", "down", "strange", "charm", "bottom", "top"]:
        topology = QuarkTopology(flavor)
        calc = FlavorDependentFourInteractionCalculator(
            topology, g_SO=0.5, kappa_scale_factor=kappa_scale_factor
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


def run_hypothesis_c_tests():
    """Test flavor-dependent parameter recalibration."""

    print("="*90)
    print("HYPOTHESIS C TEST: Flavor-Dependent Confinement Parameter Recalibration")
    print("="*90)
    print()

    print("HYPOTHESIS: κ_T should scale as √m_scale to make E_phase scale correctly")
    print()
    print("Current framework: κ_T = 1.5 for all flavors (universal)")
    print("Modified framework: κ_T(m) = 1.5 × factor × √m_scale")
    print()
    print("This makes E_phase scale as m_scale^0, which compounds with:")
    print("  E_phase_total = E_circ + w × (κ_T×V + E_shell)")
    print("Goal: E_phase_total scales as √m_scale across all flavors")
    print()

    # Baseline
    print("="*90)
    print("BASELINE: κ_T scale factor = 1.0 (no modification)")
    print("="*90)
    print()

    baseline = test_flavor_recalibration(1.0)

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

    # Sweep through scale factors
    print("="*90)
    print("SCALE FACTOR SWEEP: κ_T(m) = 1.5 × factor × √m_scale")
    print("="*90)
    print()

    scale_factors = [0.1, 0.3, 0.5, 0.7, 1.0, 1.3, 1.5, 2.0, 3.0]
    all_results = {}
    best_factor = None
    best_score = float('inf')

    print(f"{'Factor':>8} {'Light Err':>10} {'Heavy Err':>10} {'Score':>10}")
    print("-" * 45)

    for factor in scale_factors:
        results = test_flavor_recalibration(factor)
        all_results[factor] = results

        light_err = np.mean([results[f]["error_pct"] for f in ["up", "down", "strange"]])
        heavy_err = np.mean([results[f]["error_pct"] for f in ["charm", "bottom", "top"]])

        # Score: penalize light degradation, reward heavy improvement
        light_penalty = max(0, light_err - 20.0)
        heavy_improvement = max(0, heavy_err_base - heavy_err)
        score = light_penalty - heavy_improvement

        print(f"{factor:>8.2f} {light_err:>10.1f} {heavy_err:>10.1f} {score:>10.2f}")

        if score < best_score and light_err < 25.0:
            best_score = score
            best_factor = factor

    print()

    # Detailed results for best factor
    if best_factor is not None:
        print("="*90)
        print(f"BEST RESULT: κ_T scale factor = {best_factor:.2f}")
        print("="*90)
        print()

        best_results = all_results[best_factor]
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

        # Check hypothesis validation
        light_ok = light_err < 25.0
        heavy_improved = heavy_err < heavy_err_base
        light_preserved = light_err < light_err_base + 5.0

        print("HYPOTHESIS C VALIDATION:")
        print(f"  Light quarks preserved: {light_preserved} (error {light_err:.1f}% vs {light_err_base:.1f}%)")
        print(f"  Heavy quarks improved:  {heavy_improved} (error {heavy_err:.1f}% vs {heavy_err_base:.1f}%)")
        print()

        if heavy_improved and light_preserved and abs(best_factor - 1.0) > 0.1:
            print("✓ HYPOTHESIS C PARTIALLY VALIDATED!")
            print(f"  Flavor-dependent κ_T scaling improves predictions")
            print(f"  Recommended factor: {best_factor:.2f}")
            return True, best_factor
        else:
            print("✗ HYPOTHESIS C INCONCLUSIVE")
            print("  Simple κ_T scaling alone may not solve the problem")
            print("  May require additional parameter recalibration (σ_T, confinement radius, etc.)")
            return False, None
    else:
        print("✗ HYPOTHESIS C REJECTED: No valid solution found")
        return False, None


if __name__ == "__main__":
    try:
        success, best_factor = run_hypothesis_c_tests()

        print()
        print("="*90)
        print("ANALYSIS")
        print("="*90)
        print()

        if success and best_factor:
            print(f"Hypothesis C shows promise with κ_T scale factor = {best_factor:.2f}")
            print()
            print("Next steps:")
            print("  1. Implement flavor-dependent κ_T in main solver")
            print("  2. Test with calibrated 125 GeV anchoring")
            print("  3. Consider additional parameter recalibration (σ_T, possibly radius)")
        else:
            print("Simple κ_T scaling alone is insufficient.")
            print("The energy composition problem may require:")
            print("  - Multiple parameter recalibration (κ_T AND σ_T)")
            print("  - Different confinement radius for heavy quarks (Hypothesis A signal)")
            print("  - Additional QCD physics for heavy quarks (Hypothesis D)")
            print()
            print("Recommendation: Test combined modifications")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
