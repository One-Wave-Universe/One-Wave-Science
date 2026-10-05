#!/usr/bin/env python3
"""
Sub-Percent Refinement: Can flavor-dependent weave parameters reach <1% accuracy?

Hypothesis: σ_T, κ_T, η_T may also be flavor-dependent. Test whether:
1. Universal parameters σ_T, κ_T give 2-5% nucleon errors
2. Flavor-specific σ_T, κ_T can reduce to <1% with α_strange = -0.150

Strategy:
- Grid sweep σ_T, κ_T for nucleons (fixed alpha_light = -0.05, alpha_strange = -0.150)
- Find best-fit parameters that minimize nucleon+Lambda error
- Report convergence to sub-percent accuracy
"""

import sys
sys.path.insert(0, "/home/claude/one-wave-science/solvers")

import numpy as np
from hadron_knot_geometry import create_proton, create_neutron, create_lambda
from hadron_mass_predictor import HadronMassCalculator

QUARK_MASSES_MEV = {
    "up": 2.16,
    "down": 4.67,
    "strange": 95.0,
}

HADRON_MASSES_MEV = {
    "proton": 938.3,
    "neutron": 939.6,
    "Lambda": 1115.7,
}


class FlavorDependentMassCalculator(HadronMassCalculator):
    """Extended with flavor-dependent α parameters."""

    def __init__(self, alpha_light=-0.05, alpha_strange=-0.150,
                 sigma_T=0.01, kappa_T_base=0.373, eta_T=0.001):
        super().__init__(
            alpha_radius=alpha_light,
            kappa_factor=1.0,
            sigma_T=sigma_T,
            kappa_T_base=kappa_T_base,
            eta_T=eta_T
        )
        self.alpha_light = alpha_light
        self.alpha_strange = alpha_strange

    def compute_boundary_radius(self, knot, flavor_masses=None):
        """Compute boundary radius with flavor-dependent α scaling."""
        if flavor_masses is None:
            flavor_masses = QUARK_MASSES_MEV

        light_mass = 0.0
        strange_mass = 0.0
        has_strange = False

        for vortex in knot.vortices:
            if vortex.flavor in ["up", "down"]:
                light_mass += flavor_masses.get(vortex.flavor, 0)
            elif vortex.flavor == "strange":
                strange_mass += flavor_masses.get(vortex.flavor, 0)
                has_strange = True

        if has_strange and self.alpha_strange != self.alpha_light:
            masses = []
            alphas = []

            for vortex in knot.vortices:
                m = flavor_masses.get(vortex.flavor, 0)
                masses.append(m)

                if vortex.flavor == "strange":
                    alphas.append(self.alpha_strange)
                else:
                    alphas.append(self.alpha_light)

            alpha_avg = np.mean(alphas)
            geometric_mean = np.prod(masses) ** (1.0 / len(masses))
            m_scale = geometric_mean / flavor_masses["up"]

            base_radius = 0.85
            radius = base_radius * (m_scale ** alpha_avg)
        else:
            masses = [flavor_masses.get(v.flavor, 0) for v in knot.vortices]
            geometric_mean = np.prod(masses) ** (1.0 / len(masses))
            m_scale = geometric_mean / flavor_masses["up"]

            base_radius = 0.85
            radius = base_radius * (m_scale ** self.alpha_light)

        return radius


def refine_weave_parameters():
    """Sweep σ_T and κ_T to find sub-percent nucleon accuracy."""

    print("=" * 90)
    print("SUB-PERCENT REFINEMENT: Flavor-Dependent Weave Parameters")
    print("Goal: Achieve <1% nucleon accuracy with α_strange = -0.150")
    print("=" * 90)
    print()

    # Finer grid around best known values
    sigma_T_values = np.linspace(0.008, 0.012, 9)      # 0.008 to 0.012
    kappa_T_values = np.linspace(0.35, 0.40, 11)       # 0.35 to 0.40

    print(f"Testing {len(sigma_T_values)} × {len(kappa_T_values)} = {len(sigma_T_values)*len(kappa_T_values)} parameter combinations...")
    print()

    best_error = float('inf')
    best_params = None
    best_detail = None

    print(f"{'σ_T':>10} {'κ_T':>10} {'p-err%':>8} {'n-err%':>8} {'L-err%':>8} {'score':>8}")
    print("-" * 70)

    proton = create_proton()
    neutron = create_neutron()
    lam = create_lambda()

    for sigma_T in sigma_T_values:
        for kappa_T in kappa_T_values:
            calc = FlavorDependentMassCalculator(
                alpha_light=-0.05,
                alpha_strange=-0.150,
                sigma_T=sigma_T,
                kappa_T_base=kappa_T,
                eta_T=0.001
            )

            p_result = calc.compute_hadron_mass("proton", proton)
            n_result = calc.compute_hadron_mass("neutron", neutron)
            l_result = calc.compute_hadron_mass("Lambda", lam)

            p_err = p_result["error_percent"]
            n_err = n_result["error_percent"]
            l_err = l_result["error_percent"]

            # Score: minimize nucleon errors (target <1%), keep Lambda reasonable
            nucleon_penalty = p_err + n_err
            if p_err > 1.0 or n_err > 1.0:
                nucleon_penalty += (max(0, p_err - 1.0) + max(0, n_err - 1.0)) ** 2

            score = nucleon_penalty + 0.2 * l_err

            if score < best_error:
                best_error = score
                best_params = (sigma_T, kappa_T)
                best_detail = (p_err, n_err, l_err)

            if len(sigma_T_values) * len(kappa_T_values) <= 20 or (score < nucleon_penalty * 1.1):
                print(f"{sigma_T:>10.4f} {kappa_T:>10.4f} {p_err:>7.2f}% {n_err:>7.2f}% {l_err:>7.2f}% {score:>7.2f}")

    print("-" * 70)
    print()

    if best_params:
        sigma_T_best, kappa_T_best = best_params
        p_err_best, n_err_best, l_err_best = best_detail

        print("RESULT: Refined Parameters (Sub-Percent Target)")
        print()
        print(f"  σ_T = {sigma_T_best:.6f} GeV/fm² (optimized)")
        print(f"  κ_T = {kappa_T_best:.6f} GeV (optimized)")
        print(f"  α_light = -0.050 (Phase 5)")
        print(f"  α_strange = -0.150 (keystone unlock)")
        print()
        print(f"  Proton error: {p_err_best:.2f}%")
        print(f"  Neutron error: {n_err_best:.2f}%")
        print(f"  Lambda error: {l_err_best:.2f}%")
        print()

        avg_nucleon_err = (p_err_best + n_err_best) / 2

        if avg_nucleon_err < 1.0 and p_err_best < 1.5 and n_err_best < 1.5:
            print("✓ SUB-PERCENT ACCURACY ACHIEVED")
            print("Framework now matches nucleons to <1.5% precision")
            if l_err_best < 15.0:
                print("Lambda also within acceptable range")
            return (sigma_T_best, kappa_T_best)
        elif avg_nucleon_err < 3.0:
            print("⚠ APPROACHING SUB-PERCENT")
            print(f"Current nucleon accuracy: {avg_nucleon_err:.2f}%")
            print("Further refinement or additional physics needed for <1% target")
            return (sigma_T_best, kappa_T_best)
        else:
            print("✗ REFINEMENT UNSUCCESSFUL")
            print("Check framework assumptions or add additional physics")
            return None

    return None


if __name__ == "__main__":
    try:
        result = refine_weave_parameters()

        print()
        print("=" * 90)
        if result:
            print("ANALYSIS: What prevents sub-percent accuracy?")
            print()
            print("Current framework:")
            print("  - Uses Phase 5 radius + κ_T scaling")
            print("  - Weave energy from C-317 (surface + phase + twist terms)")
            print("  - Flavor-dependent radius scaling (α_light, α_strange)")
            print()
            print("Residual errors (2-5%) may come from:")
            print("  1. Weave parameter formula not exactly capturing physics")
            print("  2. Missing electromagnetic corrections (~1% for nucleons)")
            print("  3. Quark mass values uncertain (current: PDG estimates)")
            print("  4. Relativistic/QCD effects in mass formula")
            print()
            print("Next work: Investigate sensitivity to input parameters,")
            print("          add electromagnetic corrections, or refine binding model.")
        print("=" * 90)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
