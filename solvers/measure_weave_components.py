#!/usr/bin/env python3
"""
Measure Weave Energy Components: Trace C-317 Formula Step-by-Step

Objective: Decompose E_weave into its constituent parts for each hadron
and extract the exact error pattern.

C-317 (Boundary-Tension Weave):
  E_weave = σ_T·A + κ_T·ΔΨ² + η_T·∇×v

where:
  σ_T = surface tension coefficient (~0.01 GeV/fm²)
  κ_T = phase-locking coefficient (~0.373 GeV)
  η_T = twist coefficient (~0.001 GeV)

For a 3-vortex baryon knot with boundary radius R:
  A = surface area = 4πR² (sphere)
  ΔΨ² = phase difference energy ∝ Σ(φᵢ - φⱼ)²
  ∇×v = vorticity energy from phase circulation

Method: Compute each term separately, identify which term dominates the error.
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

HADRON_MASSES_MEV = {
    "proton": 938.3,
    "neutron": 939.6,
    "Lambda": 1115.7,
}

# Current predictions from the calibrated model
PREDICTED_STATIC = {
    "proton": 913.5,
    "neutron": 990.6,
    "Lambda": 1262.7,
}


def compute_boundary_radius(knot, alpha_light=-0.05, alpha_strange=-0.150):
    """Compute boundary radius using flavor-dependent α scaling."""
    masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in knot.vortices]

    # Get alpha values for each vortex
    alphas = []
    for vortex in knot.vortices:
        if vortex.flavor == "strange":
            alphas.append(alpha_strange)
        else:
            alphas.append(alpha_light)

    alpha_avg = np.mean(alphas)

    # Geometric mean of constituent masses
    geometric_mean = np.prod(masses) ** (1.0 / len(masses))
    m_scale = geometric_mean / QUARK_MASSES_MEV["up"]

    base_radius = 0.85
    radius = base_radius * (m_scale ** alpha_avg)

    return radius, m_scale, alpha_avg


def compute_phase_differences(knot):
    """Compute phase differences between all vortex pairs."""
    phases = [v.phase_offset for v in knot.vortices]

    # Pairwise phase differences
    phase_diffs = []
    for i in range(len(phases)):
        for j in range(i+1, len(phases)):
            diff = abs(phases[i] - phases[j])
            # Normalize to [0, π]
            diff = min(diff, 2*np.pi - diff)
            phase_diffs.append(diff)

    return np.array(phase_diffs) if phase_diffs else np.array([0.0])


def measure_weave_components(hadron_name, knot, R_base=0.85,
                             sigma_T=0.01, kappa_T_base=1.5, eta_T=0.01):
    """
    Measure each component of E_weave = σ_T·A + κ_T·ΔΨ² + η_T·∇×v

    KEY: κ_T scales with √m_scale, not constant!
    κ_T = κ_T_base × √m_scale
    """

    # Get radius
    R, m_scale, alpha_avg = compute_boundary_radius(knot)

    # κ_T scales with square root of mass scale
    kappa_T = kappa_T_base * np.sqrt(m_scale)

    # Surface area term: σ_T·A
    surface_area = 4 * np.pi * R**2
    E_surface = sigma_T * surface_area

    # Phase difference term: κ_T·ΔΨ²
    phase_diffs = compute_phase_differences(knot)
    phase_diff_squared = np.sum(phase_diffs**2)
    E_phase = kappa_T * phase_diff_squared

    # Twist term: η_T·∇×v
    # Vorticity ∝ (number of vortices) / (boundary circumference)
    # For 3-vortex configuration with circulation
    n_vortex = len(knot.vortices)
    circumference = 2 * np.pi * R
    # Rough estimate: vorticity energy scales with vortex count and phase density
    vorticity = n_vortex / circumference
    E_twist = eta_T * vorticity**2 * (R**3)  # Volume-weighted twist

    # Total weave energy
    E_weave_total = E_surface + E_phase + E_twist

    # Get constituent mass sum
    const_mass = sum(QUARK_MASSES_MEV.get(v.flavor, 0) for v in knot.vortices)

    # Total predicted mass
    predicted_mass = const_mass + E_weave_total

    # Experimental mass
    expt_mass = HADRON_MASSES_MEV[hadron_name]
    error_mev = predicted_mass - expt_mass
    error_pct = 100 * error_mev / expt_mass

    return {
        "hadron": hadron_name,
        "R": R,
        "m_scale": m_scale,
        "alpha_avg": alpha_avg,
        "kappa_T": kappa_T,
        "E_surface": E_surface,
        "E_phase": E_phase,
        "E_twist": E_twist,
        "E_weave_total": E_weave_total,
        "const_mass": const_mass,
        "predicted_mass": predicted_mass,
        "expt_mass": expt_mass,
        "error_mev": error_mev,
        "error_pct": error_pct,
        "n_vortex": n_vortex,
        "max_phase_diff": np.max(phase_diffs),
        "phase_diffs": phase_diffs,
    }


def analyze_weave_components():
    """Decompose E_weave for each hadron and find error patterns."""

    print("="*90)
    print("WEAVE COMPONENT DECOMPOSITION: Trace C-317 Formula Step-by-Step")
    print("="*90)
    print()

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    results = []
    for hadron_name, knot in hadrons:
        result = measure_weave_components(hadron_name, knot,
                                         sigma_T=0.01, kappa_T_base=1.5, eta_T=0.01)
        results.append(result)

    # Display detailed decomposition
    print("INDIVIDUAL DECOMPOSITION:")
    print("-" * 90)
    print()

    for r in results:
        print(f"{r['hadron'].upper()}")
        print(f"  Boundary radius R = {r['R']:.4f} fm (m_scale={r['m_scale']:.3f}, α={r['alpha_avg']:.3f})")
        print(f"  Constituent mass: {r['const_mass']:.1f} MeV")
        print(f"  κ_T (phase-locking): {r['kappa_T']:.3f} GeV (from κ_T_base × √m_scale)")
        print()
        print(f"  E_weave Components:")
        print(f"    Surface term (σ_T·A):    {r['E_surface']:>8.2f} MeV")
        print(f"    Phase term (κ_T·ΔΨ²):    {r['E_phase']:>8.2f} MeV")
        print(f"    Twist term (η_T·∇×v):    {r['E_twist']:>8.2f} MeV")
        print(f"    Total E_weave:           {r['E_weave_total']:>8.2f} MeV")
        print()
        print(f"  Total predicted: {r['const_mass']:.1f} + {r['E_weave_total']:.1f} = {r['predicted_mass']:.1f} MeV")
        print(f"  Experimental:    {r['expt_mass']:.1f} MeV")
        print(f"  Error:           {r['error_mev']:>+.1f} MeV ({r['error_pct']:>+.1f}%)")
        print(f"  Phase geometry:  max_diff={r['max_phase_diff']:.3f} rad, n_vortex={r['n_vortex']}")
        print()

    # Pattern analysis
    print("="*90)
    print("PATTERN ANALYSIS: Extract Error Scaling")
    print("="*90)
    print()

    # Sort by error magnitude
    sorted_results = sorted(results, key=lambda r: abs(r['error_mev']))

    print("Errors by magnitude:")
    for r in sorted_results:
        print(f"  {r['hadron']:<12} error={r['error_mev']:>+7.1f} MeV ({r['error_pct']:>+6.1f}%), E_phase={r['E_phase']:>6.1f} MeV")

    print()
    print("Key observations:")
    print()

    # Check if error correlates with phase energy
    print("1. PHASE ENERGY CORRELATION:")
    for r in results:
        phase_pct_of_weave = 100 * r['E_phase'] / r['E_weave_total']
        print(f"   {r['hadron']}: E_phase = {r['E_phase']:.1f} MeV ({phase_pct_of_weave:.0f}% of weave)")

    print()
    print("2. ERROR vs SURFACE AREA:")
    for r in results:
        surface_pct = 100 * r['E_surface'] / r['E_weave_total']
        print(f"   {r['hadron']}: E_surface = {r['E_surface']:.1f} MeV ({surface_pct:.0f}% of weave)")

    print()
    print("3. VORTEX COUNT DEPENDENCE:")
    for r in results:
        print(f"   {r['hadron']}: n_vortex={r['n_vortex']}, error={r['error_mev']:>+.1f} MeV")

    print()
    print("4. CONSTITUENT MASS DEPENDENCE:")
    for r in results:
        m_avg = r['const_mass'] / r['n_vortex']
        error_per_mev = r['error_mev'] / r['const_mass'] if r['const_mass'] > 0 else 0
        print(f"   {r['hadron']}: m_const={r['const_mass']:.1f} MeV (m_avg={m_avg:.2f}), error/m={error_per_mev:.4f}")

    print()
    print("="*90)
    print("HYPOTHESIS TESTING")
    print("="*90)
    print()

    # Test: does error scale with E_phase?
    print("H1: Error ∝ E_phase (phase overcounting)?")
    phase_errors = [(r['E_phase'], abs(r['error_mev'])) for r in results]
    print("   E_phase (MeV)  |  |Error| (MeV)")
    print("   " + "-" * 35)
    for e_phase, err_mag in phase_errors:
        print(f"   {e_phase:>13.1f}  |  {err_mag:>11.1f}")

    if len(phase_errors) > 1:
        correlation = np.corrcoef([p[0] for p in phase_errors], [p[1] for p in phase_errors])[0,1]
        print(f"   Correlation coefficient: {correlation:.3f}")
        if abs(correlation) > 0.8:
            print("   ✓ STRONG CORRELATION: Error likely from phase energy term!")
        elif abs(correlation) > 0.5:
            print("   ⚠ MODERATE CORRELATION: Phase may be part of mechanism")
        else:
            print("   ✗ WEAK CORRELATION: Phase not the main error source")

    print()
    print("H2: Error ∝ n_vortex (3-body vs 2-body)?")
    print("   n_vortex  |  |Error| (MeV)")
    print("   " + "-" * 25)
    for r in results:
        print(f"   {r['n_vortex']:>8}  |  {abs(r['error_mev']):>11.1f}")

    print()
    print("="*90)
    print("CONCLUSION")
    print("="*90)
    print()
    print("To achieve zero-error accuracy, we need to identify:")
    print()
    print("1. Which term (σ_T·A, κ_T·ΔΨ², η_T·∇×v) is over-predicted?")
    print("2. What is the correct scaling (e.g., factor of 2/3 for phase?)")
    print("3. Does correction depend on n_vortex, m_const, or flavor?")
    print()
    print("Next action: Use error pattern to propose corrected formula.")
    print()


if __name__ == "__main__":
    try:
        analyze_weave_components()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
