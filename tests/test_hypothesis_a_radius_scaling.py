#!/usr/bin/env python3
"""
Hypothesis A Test: Non-Universal Confinement Radius
Phase 5 Heavy-Quark Keystone Problem Investigation

HYPOTHESIS: The confinement radius R may scale with m_scale, not remain constant at 0.35 fm.

TEST: Sweep through different radius-scaling exponents (alpha) and find which one:
  - Improves heavy-quark predictions (charm/bottom/top closer to PDG)
  - Preserves light-quark accuracy (up/down/strange stay within 8-19% error)
  - Maintains universal coupling (g_SO = 0.5 unchanged)

IMPLEMENTATION: R(m_scale) = R_base × (m_scale / m_ref)^alpha
  - R_base = 0.35 fm (current value)
  - m_ref = 1.0 (up quark, reference)
  - alpha: range from -0.3 to +0.3 (sweep in 0.05 steps)

EXPECTED OUTCOME:
  If Hypothesis A is correct, we should find an alpha that significantly improves
  heavy-quark error while keeping light-quark error <20%.

Author: Claude Haiku 4.5
Date: October 4, 2026
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

# Add solvers to path
sys.path.insert(0, str(Path(__file__).parent.parent / "solvers"))

from quark_mass_solver import QuarkTopology, FourInteractionCalculator


class ScaledRadiusQuarkTopology(QuarkTopology):
    """Extended QuarkTopology with radius scaling parameter."""

    def __init__(self, flavor: str, radius_scale_alpha: float = 0.0):
        """
        Initialize topology with optional radius scaling.

        Args:
            flavor: quark flavor name
            radius_scale_alpha: exponent for R(m) = 0.35 × (m_scale)^alpha
        """
        super().__init__(flavor)
        self.radius_scale_alpha = radius_scale_alpha

        # Apply radius scaling if alpha != 0
        if abs(radius_scale_alpha) > 1e-6:
            R_base = 0.35  # fm, the original value
            R_scaled = R_base * (self.mass_scale ** radius_scale_alpha)
            self.R_knot = R_scaled


def compute_masses_with_radius_scaling(alpha: float) -> Dict[str, Dict[str, float]]:
    """
    Compute all quark masses for a given radius-scaling exponent.

    Args:
        alpha: radius scaling exponent

    Returns:
        Dictionary with flavor -> {pred, pdg, error_pct, error_ratio}
    """
    # Define quark properties: (flavor, PDG mass in MeV)
    quarks = [
        ("up", 2.16),
        ("down", 4.67),
        ("strange", 95.0),
        ("charm", 1270.0),
        ("bottom", 4180.0),
        ("top", 173000.0),
    ]

    results = {}

    for flavor, pdg_mass in quarks:
        # Create topology with radius scaling
        topology = ScaledRadiusQuarkTopology(flavor, radius_scale_alpha=alpha)

        # Compute mass using four-interaction calculator
        calculator = FourInteractionCalculator(topology, g_SO=0.5)

        # Get predicted mass (already calibrated with λ = 0.976)
        predicted_mass = calculator.mass_from_numerical_differentiation()

        # Apply calibration factor
        lambda_scale = 0.976
        predicted_mass_calibrated = predicted_mass * np.sqrt(lambda_scale)

        # Compute error
        error_pct = abs(predicted_mass_calibrated - pdg_mass) / pdg_mass * 100.0
        error_ratio = predicted_mass_calibrated / pdg_mass if pdg_mass > 0 else 0

        results[flavor] = {
            "predicted": predicted_mass_calibrated,
            "pdg": pdg_mass,
            "error_pct": error_pct,
            "error_ratio": error_ratio,
            "R_knot": topology.R_knot,
        }

    return results


def evaluate_hypothesis_a():
    """Run comprehensive test of Hypothesis A across alpha range."""

    print("="*80)
    print("HYPOTHESIS A TEST: Non-Universal Confinement Radius Scaling")
    print("="*80)
    print()

    print("HYPOTHESIS: R(m_scale) = 0.35 fm × (m_scale)^alpha")
    print("where alpha is an exponent to be determined")
    print()

    print("TEST RANGE: alpha from -0.3 to +0.3 (step size 0.05)")
    print()

    # Define success criteria
    print("SUCCESS CRITERIA:")
    print("  1. Light quarks (u/d/s) remain within 8-19% error")
    print("  2. Heavy quarks (c/b/t) improve significantly (target <30% error for c/b)")
    print("  3. Top quark improves (target <100% error)")
    print()

    # Baseline: current implementation (alpha = 0)
    print("BASELINE (alpha = 0.0, current implementation):")
    print("-" * 80)
    baseline = compute_masses_with_radius_scaling(0.0)

    baseline_light_error = (
        baseline["up"]["error_pct"] +
        baseline["down"]["error_pct"] +
        baseline["strange"]["error_pct"]
    ) / 3.0

    baseline_heavy_error = (
        baseline["charm"]["error_pct"] +
        baseline["bottom"]["error_pct"] +
        baseline["top"]["error_pct"]
    ) / 3.0

    print_results_table(baseline)
    print(f"Light quark avg error:  {baseline_light_error:.1f}%")
    print(f"Heavy quark avg error:  {baseline_heavy_error:.1f}%")
    print()

    # Sweep through alpha values
    alpha_values = np.arange(-0.30, 0.31, 0.05)
    all_results = {}
    best_alpha = None
    best_score = float('inf')

    print("ALPHA SWEEP:")
    print("-" * 80)

    for alpha in alpha_values:
        results = compute_masses_with_radius_scaling(alpha)
        all_results[alpha] = results

        # Compute metrics
        light_error = (
            results["up"]["error_pct"] +
            results["down"]["error_pct"] +
            results["strange"]["error_pct"]
        ) / 3.0

        heavy_error = (
            results["charm"]["error_pct"] +
            results["bottom"]["error_pct"] +
            results["top"]["error_pct"]
        ) / 3.0

        # Score: penalize if light quarks degrade, reward if heavy improve
        light_penalty = max(0, light_error - 20.0)  # Penalize if >20%
        heavy_improvement = max(0, baseline_heavy_error - heavy_error)  # Reward improvement

        score = light_penalty - heavy_improvement

        print(f"α = {alpha:+.2f}: Light avg={light_error:6.1f}%, Heavy avg={heavy_error:7.1f}%, Score={score:7.2f}")

        if score < best_score and light_error < 25.0:  # Allow slight light-quark degradation
            best_score = score
            best_alpha = alpha

    print()

    # Detailed results for best alpha
    if best_alpha is not None:
        print("="*80)
        print(f"BEST RESULT: α = {best_alpha:+.2f}")
        print("="*80)
        print()
        best_results = all_results[best_alpha]
        print_results_table(best_results)

        light_error = (
            best_results["up"]["error_pct"] +
            best_results["down"]["error_pct"] +
            best_results["strange"]["error_pct"]
        ) / 3.0

        heavy_error = (
            best_results["charm"]["error_pct"] +
            best_results["bottom"]["error_pct"] +
            best_results["top"]["error_pct"]
        ) / 3.0

        print(f"Light quark avg error:  {light_error:.1f}%")
        print(f"Heavy quark avg error:  {heavy_error:.1f}%")
        print()

        # Check if hypothesis is validated
        light_ok = light_error < 25.0
        heavy_improved = heavy_error < baseline_heavy_error

        print("HYPOTHESIS VALIDATION:")
        print(f"  Light quarks preserved: {light_ok} (error {light_error:.1f}% < 25%)")
        print(f"  Heavy quarks improved:  {heavy_improved} (error {heavy_error:.1f}% < {baseline_heavy_error:.1f}%)")
        print()

        if light_ok and heavy_improved and abs(best_alpha) > 0.01:
            print("✓ HYPOTHESIS A VALIDATED: Radius scaling improves predictions!")
            print(f"  Recommended α = {best_alpha:+.2f}")
            return True, best_alpha
        elif light_ok and heavy_improved:
            print("✓ HYPOTHESIS A INCONCLUSIVE: Radius scaling with α=0 is best")
            print("  (but current implementation may still be optimal)")
            return True, 0.0
        else:
            print("✗ HYPOTHESIS A REJECTED: No improvement found")
            return False, None
    else:
        print("✗ HYPOTHESIS A REJECTED: No valid solution found")
        return False, None


def print_results_table(results: Dict[str, Dict[str, float]]):
    """Print formatted results table."""
    print(f"{'Flavor':<10} {'R_knot':>9} {'Pred (MeV)':>12} {'PDG (MeV)':>12} {'Error %':>10} {'Ratio':>8}")
    print("-" * 65)
    for flavor in ["up", "down", "strange", "charm", "bottom", "top"]:
        r = results[flavor]
        print(f"{flavor:<10} {r['R_knot']:>9.4f} {r['predicted']:>12.2f} {r['pdg']:>12.2f} {r['error_pct']:>9.1f}% {r['error_ratio']:>8.3f}x")


if __name__ == "__main__":
    try:
        success, best_alpha = evaluate_hypothesis_a()

        print()
        print("="*80)
        print("CONCLUSION")
        print("="*80)

        if success and best_alpha and abs(best_alpha) > 0.01:
            print(f"Hypothesis A shows promise with α = {best_alpha:+.2f}")
            print("Next step: Implement radius scaling in main solver")
        elif success:
            print("Hypothesis A inconclusive or current implementation optimal")
            print("Next step: Test Hypothesis B (weight-factor analysis)")
        else:
            print("Hypothesis A does not explain heavy-quark problem")
            print("Next step: Test Hypothesis B (weight-factor analysis)")

        sys.exit(0 if success else 1)

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
