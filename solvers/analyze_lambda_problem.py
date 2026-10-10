#!/usr/bin/env python3
"""
Analyze why Lambda is severely underpredicted.

Lambda (u,d,s) has:
- No symmetric pair (all three quarks different masses)
- Extreme frequency dispersion (44× with strange quark)
- Very low average coherence (0.341)

The problem: With no symmetric pair, binding_correction = 0.0
So Lambda gets no binding energy adjustment.

Expected mass: 1115.7 MeV
Current prediction with κ_T_base=0.40, no scaling: 636.6 MeV (underpredicted by 479.1 MeV)

Where should this energy come from?
- Constituent mass: 101.8 MeV (from quarks themselves)
- Weave energy: 542.8 MeV (from boundary-tension weave)
- Binding energy: -8.0 MeV (from confinement)
- Total: 636.6 MeV ← missing 479.1 MeV!

The missing energy must come from either:
1. Increased weave energy (by reducing coherence penalty)
2. Increased binding energy (different formula for hyperons)
3. A new physics mechanism for strange quark binding
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from hadron_knot_geometry import (
    QUARK_MASSES_MEV, WeaveDensity, WeavingEnergyCalculator,
    create_lambda
)

def analyze_lambda_energetics():
    """Break down where Lambda's energy comes from."""

    print("="*90)
    print("LAMBDA ENERGETICS ANALYSIS")
    print("="*90)
    print()

    lambda_hadron = create_lambda()
    vortices = lambda_hadron.vortices
    flavors = [v.flavor for v in vortices]
    masses = [QUARK_MASSES_MEV.get(f, 0) for f in flavors]

    print("Lambda composition: u, d, s")
    print(f"  Masses: {masses[0]:.2f} (u), {masses[1]:.2f} (d), {masses[2]:.2f} (s) MeV")
    print()

    # Current calculation with κ_T_base = 0.40, no scaling
    kappa_T_base = 0.40  # GeV

    # Build weave with constant κ_T
    weave = WeaveDensity(
        sigma_T=0.01,
        kappa_T=kappa_T_base,
        eta_T=0.01,
        neck_radius=0.1,
        break_threshold=5.0
    )

    weave_calc = WeavingEnergyCalculator(weave)

    # Compute energy components
    E_skin = weave_calc.surface_energy(lambda_hadron.boundary_area)
    E_phase = weave_calc.phase_locking_energy(vortices, lambda_hadron.boundary_radius)
    E_twist = weave_calc.twist_energy(vortices, lambda_hadron.boundary_radius)

    print(f"Energy breakdown (κ_T_base = {kappa_T_base} GeV, no scaling):")
    print(f"  Surface energy (E_skin):     {E_skin*1000:>8.1f} MeV")
    print(f"  Phase-locking energy (E_phase): {E_phase*1000:>8.1f} MeV")
    print(f"  Twist energy (E_twist):     {E_twist*1000:>8.1f} MeV")
    print(f"  Binding energy (assumed):   {-8.0:>8.1f} MeV")
    print(f"  Constituent masses:         {sum(masses):>8.1f} MeV")
    print(f"  {'─'*50}")

    constituent = sum(masses)
    weave_total = (E_skin + E_phase + E_twist) * 1000
    binding = -8.0
    total = constituent + weave_total + binding

    print(f"  Total predicted:            {total:>8.1f} MeV")
    print()

    actual_mass = 1115.7
    missing = actual_mass - total

    print(f"Expected (PDG):              {actual_mass:>8.1f} MeV")
    print(f"MISSING:                     {missing:>8.1f} MeV ({missing/actual_mass*100:.1f}%)")
    print()

    # Analysis
    print("="*90)
    print("DIAGNOSIS")
    print("="*90)
    print()

    # Compute coherence factors for Lambda
    kappa_T_base_mev = kappa_T_base * 1000
    omegas = [kappa_T_base / m if m > 0 else 0 for m in masses]

    print("Oscillation frequency analysis:")
    print(f"  κ_T_base = {kappa_T_base_mev:.0f} MeV")
    print(f"  ω (u) = {omegas[0]:.6f}")
    print(f"  ω (d) = {omegas[1]:.6f}")
    print(f"  ω (s) = {omegas[2]:.6f}")
    print()

    # Compute coherence for each pair
    print("Pair coherence factors:")
    coherences = []
    for i in range(len(vortices)):
        for j in range(i+1, len(vortices)):
            if omegas[i] > 0 and omegas[j] > 0:
                omega_ratio = max(omegas[i], omegas[j]) / min(omegas[i], omegas[j])
                coherence = 1.0 / (1.0 + np.log(omega_ratio)) if omega_ratio > 1.0 else 1.0
                coherences.append(coherence)
                print(f"  Pair {i}-{j} ({flavors[i]}-{flavors[j]}): ω_ratio={omega_ratio:.2f}, coherence={coherence:.4f}")

    avg_coherence = np.mean(coherences) if coherences else 1.0
    print(f"  Average coherence: {avg_coherence:.4f}")
    print()

    # What happens if we increase κ_T_base for Lambda specifically?
    print("="*90)
    print("SCENARIO: What if Lambda needs HIGHER κ_T_base?")
    print("="*90)
    print()

    # Compute required κ_T_base to reach actual mass
    required_weave_mev = actual_mass - constituent - binding
    phase_ratio = E_phase / E_skin if E_skin > 0 else 1.0  # How much of weave comes from phase

    # If we scale κ_T, phase-locking scales linearly
    current_E_phase_mev = E_phase * 1000
    required_E_phase_mev = required_weave_mev - E_skin*1000 - E_twist*1000
    scale_factor = required_E_phase_mev / current_E_phase_mev if current_E_phase_mev > 0 else 1.0
    required_kappa_T = kappa_T_base * scale_factor

    print(f"Current phase-locking energy:  {current_E_phase_mev:.1f} MeV")
    print(f"Required phase-locking energy: {required_E_phase_mev:.1f} MeV")
    print(f"Scale factor needed: {scale_factor:.2f}×")
    print(f"Required κ_T_base: {required_kappa_T:.3f} GeV")
    print()

    # But this would break Proton and Neutron!
    print("⚠️  Problem: Using κ_T_base = {:.3f} GeV would break nucleons:".format(required_kappa_T))

    weave_proton = WeaveDensity(
        sigma_T=0.01,
        kappa_T=required_kappa_T,
        eta_T=0.01,
        neck_radius=0.1,
        break_threshold=5.0
    )
    weave_calc_scaled = WeavingEnergyCalculator(weave_proton)

    from hadron_knot_geometry import create_proton, create_neutron
    proton = create_proton()
    neutron = create_neutron()

    p_phase = weave_calc_scaled.phase_locking_energy(proton.vortices, proton.boundary_radius)
    n_phase = weave_calc_scaled.phase_locking_energy(neutron.vortices, neutron.boundary_radius)

    p_mass = sum(QUARK_MASSES_MEV.get(v.flavor, 0) for v in proton.vortices) + p_phase*1000 - 5.5
    n_mass = sum(QUARK_MASSES_MEV.get(v.flavor, 0) for v in neutron.vortices) + n_phase*1000 - 10.5

    print(f"  Proton would be:  {p_mass:.1f} MeV (error: {(p_mass-938.3)/938.3*100:+.1f}%)")
    print(f"  Neutron would be: {n_mass:.1f} MeV (error: {(n_mass-939.6)/939.6*100:+.1f}%)")
    print()

    print("="*90)
    print("CONCLUSION")
    print("="*90)
    print()
    print("The problem: Lambda has NO symmetric pair for binding reference frame.")
    print()
    print("Options to fix Lambda:")
    print("1. Add a default binding correction for hadrons with no symmetric pair")
    print("   (but what should the correction value be?)")
    print("2. Use a different binding formula for hyperons (s-quark special handling)")
    print("3. Modify the coherence formula to be less aggressive on frequency dispersion")
    print("4. Add a 'hyperon binding constant' that applies to hadrons with strange quarks")
    print()
    print("Current status:")
    print(f"  Nucleons (Proton, Neutron): Excellent (~2-10% error) ✓")
    print(f"  Hyperons (Lambda): Poor (~43% error) ✗")
    print()


if __name__ == "__main__":
    try:
        analyze_lambda_energetics()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
