#!/usr/bin/env python3
"""
Boundary Condition Analysis: Revisiting R and κ_T Calibration

CRITICAL REALIZATION: Correction formulas getting RMSE ~10 MeV but still
leaving ~6-17 MeV errors means the base model is systematically off.

The user's hint: "its osscilating at middle its phase shift and conncetion.
its boundry condtions"

Key parameters that affect predictions:
1. Boundary radius R(m_scale) = base_radius × m_scale^α
   - α = -0.05 (Phase 5 calibration)
   - base_radius = 0.85 fm (fixed)

2. Phase-locking coupling κ_T(m_scale) = κ_T_base × √m_scale
   - κ_T_base = 0.297 GeV (calibrated via binary search)

3. Surface tension σ_T = 0.01 GeV/fm²
4. Twist coefficient η_T = 0.01

Questions to investigate:
1. Does boundary radius scale correctly for hadrons?
2. Is κ_T calibration truly independent of flavor?
3. Are the radius and κ_T values coupled in Phase 5?

Strategy: Trace exactly HOW R and κ_T are computed for each hadron,
and whether the Phase 5 calibration from quarks transfers to hadrons.
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


def trace_radius_and_kappa(hadron_name, knot):
    """Trace exactly how R and κ_T are computed."""

    vortices = knot.vortices
    masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in vortices]
    flavors = [v.flavor for v in vortices]

    m_min = min(masses)
    m_max = max(masses)
    m_avg = np.mean(masses)

    # Compute m_scale exactly as HadronMassCalculator does
    geometric_mean = np.prod(masses) ** (1.0 / len(masses))
    m_scale = geometric_mean / QUARK_MASSES_MEV["up"]

    # Boundary radius calculation
    base_radius = 0.85
    alpha = -0.05
    R = base_radius * (m_scale ** alpha)

    # κ_T calculation
    kappa_T_base = 0.297
    kappa_T = kappa_T_base * np.sqrt(m_scale)

    # Surface area
    surface_area = 4 * np.pi * R**2

    return {
        "hadron": hadron_name,
        "masses": masses,
        "flavors": flavors,
        "m_min": m_min,
        "m_max": m_max,
        "m_avg": m_avg,
        "geometric_mean": geometric_mean,
        "m_scale": m_scale,
        "base_radius": base_radius,
        "alpha": alpha,
        "R": R,
        "surface_area": surface_area,
        "kappa_T_base": kappa_T_base,
        "kappa_T": kappa_T,
    }


def main():
    print("="*90)
    print("BOUNDARY CONDITION ANALYSIS: R and κ_T Tracing")
    print("="*90)
    print()

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    results = []
    for hadron_name, knot in hadrons:
        result = trace_radius_and_kappa(hadron_name, knot)
        results.append(result)

    # Detailed trace
    print("DETAILED PARAMETER TRACE:")
    print("-" * 90)
    print()

    for r in results:
        print(f"{r['hadron'].upper()}")
        print(f"  Quarks: {', '.join([f'{f}({m:.2f})' for f, m in zip(r['flavors'], r['masses'])])}")
        print()
        print(f"  m_scale calculation:")
        print(f"    geometric_mean = ({' × '.join([f'{m:.2f}' for m in r['masses']])}))^(1/3)")
        print(f"                   = {r['geometric_mean']:.4f} MeV")
        print(f"    m_scale = {r['geometric_mean']:.4f} / {QUARK_MASSES_MEV['up']:.2f} = {r['m_scale']:.4f}")
        print()
        print(f"  Boundary radius R:")
        print(f"    R = {r['base_radius']} × ({r['m_scale']:.4f})^{r['alpha']}")
        print(f"      = {r['base_radius']} × {r['m_scale']**r['alpha']:.4f}")
        print(f"      = {r['R']:.4f} fm")
        print(f"    Surface area A = 4π R² = {r['surface_area']:.4f} fm²")
        print()
        print(f"  Phase-locking coupling κ_T:")
        print(f"    κ_T = {r['kappa_T_base']} × √{r['m_scale']:.4f}")
        print(f"        = {r['kappa_T_base']} × {np.sqrt(r['m_scale']):.4f}")
        print(f"        = {r['kappa_T']:.4f} GeV")
        print()

    # Comparison table
    print("="*90)
    print("PARAMETER COMPARISON TABLE")
    print("="*90)
    print()

    print(f"{'Hadron':<12} {'m_scale':>10} {'R (fm)':>10} {'A (fm²)':>12} {'κ_T (GeV)':>12}")
    print("-" * 70)

    for r in results:
        print(f"{r['hadron']:<12} {r['m_scale']:>10.4f} {r['R']:>10.4f} {r['surface_area']:>12.4f} {r['kappa_T']:>12.4f}")

    print()

    # Key observations
    print("="*90)
    print("KEY OBSERVATIONS")
    print("="*90)
    print()

    print("1. Boundary Radius Sensitivity:")
    print()
    for r in results:
        print(f"   {r['hadron']}: R = {r['R']:.4f} fm")

    print()
    print("   Proton and Neutron have nearly identical R despite different m_scale:")
    p_scale = results[0]["m_scale"]
    n_scale = results[1]["m_scale"]
    print(f"   Proton m_scale = {p_scale:.4f}, Neutron m_scale = {n_scale:.4f}")
    print(f"   Difference: {abs(p_scale - n_scale):.4f} ({100*abs(p_scale-n_scale)/p_scale:.1f}%)")
    print()

    print("2. κ_T Scaling:")
    print()
    for r in results:
        print(f"   {r['hadron']}: κ_T = {r['kappa_T']:.4f} GeV")

    print()
    lambda_kappa = results[2]["kappa_T"]
    proton_kappa = results[0]["kappa_T"]
    print(f"   Lambda κ_T / Proton κ_T = {lambda_kappa / proton_kappa:.2f}×")
    print()

    print("3. Surface Area Contribution:")
    print()
    sigma_T = 0.01
    for r in results:
        E_surface = sigma_T * r["surface_area"]
        print(f"   {r['hadron']}: E_surface = σ_T × A = {sigma_T} × {r['surface_area']:.2f} = {E_surface:.2f} MeV")

    print()

    # The critical question
    print("="*90)
    print("CRITICAL QUESTION: Is m_scale Calculation Correct?")
    print("="*90)
    print()

    print("Current approach: m_scale = (m₁ × m₂ × m₃)^(1/3) / m_up")
    print()
    print("This treats all quarks symmetrically. But:")
    print("  - In QCD, quark masses affect confinement differently")
    print("  - Flavor might matter (u/d vs s)")
    print("  - The mixing might not be purely geometric mean")
    print()

    print("ALTERNATIVE 1: Arithmetic mean")
    for r in results:
        m_scale_arith = r["m_avg"] / QUARK_MASSES_MEV["up"]
        print(f"  {r['hadron']}: m_scale = {r['m_avg']:.2f} / {QUARK_MASSES_MEV['up']:.2f} = {m_scale_arith:.4f}")

    print()

    print("ALTERNATIVE 2: Light-quark-dominated (minimum mass)")
    for r in results:
        m_scale_light = r["m_min"] / QUARK_MASSES_MEV["up"]
        print(f"  {r['hadron']}: m_scale = {r['m_min']:.2f} / {QUARK_MASSES_MEV['up']:.2f} = {m_scale_light:.4f}")

    print()

    print("ALTERNATIVE 3: Heavy-quark-dominated (maximum mass)")
    for r in results:
        m_scale_heavy = r["m_max"] / QUARK_MASSES_MEV["up"]
        print(f"  {r['hadron']}: m_scale = {r['m_max']:.2f} / {QUARK_MASSES_MEV['up']:.2f} = {m_scale_heavy:.4f}")

    print()

    print("="*90)
    print("HYPOTHESIS: m_scale Should Reflect Oscillation Dynamics")
    print("="*90)
    print()

    print("The phase-locking coupling κ_T drives oscillations.")
    print("Hadron binding depends on how quarks oscillate together.")
    print()
    print("For coherent oscillations, the LIGHTEST quark sets the fastest oscillation.")
    print("For binding, we care about how phases align despite different frequencies.")
    print()
    print("Possibility: κ_T should depend on LIGHT quark mass, not geometric mean?")
    print()

    for r in results:
        # Try using minimum mass for κ_T scaling
        m_scale_light = r["m_min"] / QUARK_MASSES_MEV["up"]
        kappa_T_light = 0.297 * np.sqrt(m_scale_light)
        kappa_T_current = r["kappa_T"]

        print(f"{r['hadron']}:")
        print(f"  Current κ_T (geometric): {kappa_T_current:.4f} GeV")
        print(f"  Alternative κ_T (light): {kappa_T_light:.4f} GeV")
        print(f"  Ratio: {kappa_T_light / kappa_T_current:.3f}×")
        print()


if __name__ == "__main__":
    main()
