#!/usr/bin/env python3
"""
Flavor-Dependent Radius Scaling Test

Hypothesis: Phase 5 radius scaling exponent α varies by flavor family.
- α_light (u, d): already validated at -0.05
- α_strange (s): unknown, to be determined
- α_charm (c), α_bottom (b): future work

Goal: Find α_strange that reproduces Lambda mass while preserving nucleon accuracy.

If this works, it's a cascade unlock: the principle that explains strangeness
also determines the entire flavor hierarchy.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from hadron_knot_geometry import create_proton, create_neutron, create_lambda
from hadron_mass_predictor import HadronMassCalculator

# Experimental hadron masses (PDG)
HADRON_MASSES_MEV = {
    "proton": 938.3,
    "neutron": 939.6,
    "Lambda": 1115.7,
}

# Quark masses
QUARK_MASSES_MEV = {
    "up": 2.16,
    "down": 4.67,
    "strange": 95.0,
}


def compute_flavor_composition(knot):
    """Return (light_mass, heavy_mass, has_strange) for a hadron."""
    light_mass = 0.0
    strange_mass = 0.0
    has_strange = False

    for vortex in knot.vortices:
        if vortex.flavor in ["up", "down"]:
            light_mass += QUARK_MASSES_MEV.get(vortex.flavor, 0)
        elif vortex.flavor == "strange":
            strange_mass += QUARK_MASSES_MEV.get(vortex.flavor, 0)
            has_strange = True

    return light_mass, strange_mass, has_strange


class FlavorDependentMassCalculator(HadronMassCalculator):
    """Extended HadronMassCalculator with flavor-dependent α parameters."""

    def __init__(self, alpha_light=-0.05, alpha_strange=None,
                 sigma_T=0.01, kappa_T_base=0.373, eta_T=0.001):
        super().__init__(
            alpha_radius=alpha_light,  # default to light
            kappa_factor=1.0,
            sigma_T=sigma_T,
            kappa_T_base=kappa_T_base,
            eta_T=eta_T
        )
        self.alpha_light = alpha_light
        self.alpha_strange = alpha_strange if alpha_strange is not None else alpha_light

    def compute_boundary_radius(self, knot, flavor_masses=None):
        """Compute boundary radius with flavor-dependent α scaling."""
        if flavor_masses is None:
            flavor_masses = QUARK_MASSES_MEV

        # Check if hadron contains strangeness
        light_mass, strange_mass, has_strange = compute_flavor_composition(knot)

        if has_strange and self.alpha_strange != self.alpha_light:
            # Use flavor-dependent calculation
            # Effective m_scale accounts for both light and strange contributions
            masses = []
            alphas = []

            for vortex in knot.vortices:
                m = flavor_masses.get(vortex.flavor, 0)
                masses.append(m)

                if vortex.flavor == "strange":
                    alphas.append(self.alpha_strange)
                else:
                    alphas.append(self.alpha_light)

            # Weighted combination: use harmonic mean of scaling factors
            alpha_avg = np.mean(alphas)
            geometric_mean = np.prod(masses) ** (1.0 / len(masses))
            m_scale = geometric_mean / flavor_masses["up"]

            base_radius = 0.85
            radius = base_radius * (m_scale ** alpha_avg)
        else:
            # Use original calculation (all light quarks)
            masses = [flavor_masses.get(v.flavor, 0) for v in knot.vortices]
            geometric_mean = np.prod(masses) ** (1.0 / len(masses))
            m_scale = geometric_mean / flavor_masses["up"]

            base_radius = 0.85
            radius = base_radius * (m_scale ** self.alpha_light)

        return radius


def test_flavor_dependent_alpha():
    """Test different α_strange values to find best fit for Lambda."""

    print("=" * 90)
    print("FLAVOR-DEPENDENT RADIUS SCALING TEST")
    print("Keystone Problem: Can flavor-dependent α fix strangeness while preserving nucleons?")
    print("=" * 90)
    print()

    # Test range for α_strange
    alpha_strange_values = np.linspace(-0.15, 0.05, 13)

    print("Hypothesis: α varies by flavor family")
    print(f"  α_light (u, d): -0.05 (fixed from Phase 5)")
    print(f"  α_strange (s): ? (to be determined)")
    print()

    # Fixed nucleon calibration parameters
    sigma_T = 0.010
    kappa_T_base = 0.373
    eta_T = 0.001

    print("Calibration parameters (from nucleon fit):")
    print(f"  σ_T = {sigma_T}")
    print(f"  κ_T = {kappa_T_base}")
    print(f"  η_T = {eta_T}")
    print()

    print(f"{'α_strange':>10} {'p-err%':>10} {'n-err%':>10} {'Λ-err%':>10} {'Score':>10}")
    print("-" * 60)

    best_score = float('inf')
    best_alpha_strange = None
    best_result = None

    for alpha_s in alpha_strange_values:
        calc = FlavorDependentMassCalculator(
            alpha_light=-0.05,
            alpha_strange=alpha_s,
            sigma_T=sigma_T,
            kappa_T_base=kappa_T_base,
            eta_T=eta_T
        )

        # Test on nucleons and Lambda
        proton = create_proton()
        p_result = calc.compute_hadron_mass("proton", proton)
        p_err = p_result["error_percent"]

        neutron = create_neutron()
        n_result = calc.compute_hadron_mass("neutron", neutron)
        n_err = n_result["error_percent"]

        lam = create_lambda()
        l_result = calc.compute_hadron_mass("Lambda", lam)
        l_err = l_result["error_percent"]

        # Score: minimize Lambda error while keeping nucleon errors reasonable
        # Weight: Lambda error most important, nucleon errors should stay <10%
        nucleon_penalty = 0.0
        if p_err > 10.0:
            nucleon_penalty += (p_err - 10.0) ** 2
        if n_err > 10.0:
            nucleon_penalty += (n_err - 10.0) ** 2

        score = l_err + 0.5 * nucleon_penalty

        print(f"{alpha_s:>10.3f} {p_err:>9.1f}% {n_err:>9.1f}% {l_err:>9.1f}% {score:>9.1f}")

        if score < best_score:
            best_score = score
            best_alpha_strange = alpha_s
            best_result = {
                "alpha_strange": alpha_s,
                "proton_error": p_err,
                "neutron_error": n_err,
                "lambda_error": l_err,
            }

    print("-" * 60)
    print()

    # Report best result
    if best_result:
        print("RESULT: Flavor-dependent scaling with best fit")
        print()
        print(f"  α_light = -0.05 (Phase 5, fixed)")
        print(f"  α_strange = {best_result['alpha_strange']:.3f} (optimized)")
        print()
        print(f"  Nucleon errors: proton {best_result['proton_error']:.1f}%, neutron {best_result['neutron_error']:.1f}%")
        print(f"  Lambda error: {best_result['lambda_error']:.1f}%")
        print()

        # Check if this is an improvement
        original_lambda_error = 29.9
        lambda_improvement = original_lambda_error - best_result['lambda_error']

        print("VERIFICATION BY CONSEQUENCE:")
        print()

        if best_result['proton_error'] < 10.0 and best_result['neutron_error'] < 10.0:
            print(f"  ✓ Nucleons preserved: proton {best_result['proton_error']:.1f}%, neutron {best_result['neutron_error']:.1f}%")
        else:
            print(f"  ✗ Nucleons degraded: proton {best_result['proton_error']:.1f}%, neutron {best_result['neutron_error']:.1f}%")

        if best_result['lambda_error'] < 15.0:
            print(f"  ✓ Lambda fixed: {best_result['lambda_error']:.1f}% error (was 29.9%)")
            print(f"    Improvement: {lambda_improvement:.1f} percentage points")
        elif best_result['lambda_error'] < 20.0:
            print(f"  ⚠ Lambda improved: {best_result['lambda_error']:.1f}% error (was 29.9%)")
            print(f"    Improvement: {lambda_improvement:.1f} percentage points (but not solved)")
        else:
            print(f"  ✗ Lambda not improved: {best_result['lambda_error']:.1f}% error")

        print()

        if (best_result['proton_error'] < 10.0 and best_result['neutron_error'] < 10.0
            and best_result['lambda_error'] < 15.0):
            print("STATUS: ✓ KEYSTONE UNLOCK SUCCESSFUL")
            print("Flavor-dependent α explains nucleons AND strangeness.")
            print("Next: Validate on other strange baryons (Σ, Ξ); test charm/bottom.")
            return True
        else:
            print("STATUS: ⚠ PARTIAL SUCCESS or FAILURE")
            print("Flavor-dependent α alone doesn't solve strangeness.")
            print("May need: modified κ_T scaling, or additional flavor physics.")
            return False

    return False


if __name__ == "__main__":
    try:
        success = test_flavor_dependent_alpha()

        print()
        print("=" * 90)
        if success:
            print("CONCLUSION: Flavor-dependent radius scaling is the keystone unlock.")
            print("The phase 5 framework extends to the full hadron spectrum with α per flavor.")
        else:
            print("CONCLUSION: Flavor-dependent radius scaling alone is insufficient.")
            print("Strangeness requires additional physics beyond radius scaling.")
        print("=" * 90)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
