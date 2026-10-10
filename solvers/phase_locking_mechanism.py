#!/usr/bin/env python3
"""
Phase-Locking Mechanism: How Field Connection Creates Binding

Central insight from One-Wave framework:
- Hadron mass emerges from a bounded recurring wave pattern (knot)
- The pattern is held together by phase-locking: vortex phases align and reinforce
- κ_T (phase-locking coupling) quantifies the field connection strength
- Binding energy = energy cost to disrupt the phase-locked configuration

This is NOT about collisions. It's about how field patterns self-stabilize.

Key question: Why do current predictions overshoot by 25-150 MeV for baryons?

Hypothesis: The phase-locking calculation assumes static, evenly-spaced phases.
But real phases might oscillate or shift based on quark flavor/mass, changing the
effective phase separation and thus the phase-locking energy.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

PREDICTED = {
    "proton": 913.5,
    "neutron": 990.6,
    "Lambda": 1262.7,
}


def analyze_phase_locking_mechanism():
    """
    Extract the phase-locking mechanism from the error pattern.

    Strategy: Use the actual HadronMassCalculator to get the binding energy
    it computed, then reverse-engineer what corrections are needed.
    """

    print("="*90)
    print("PHASE-LOCKING MECHANISM ANALYSIS")
    print("="*90)
    print()

    calc = HadronMassCalculator(
        alpha_radius=-0.05,
        kappa_factor=1.0,
        sigma_T=0.01,
        kappa_T_base=0.297,  # Calibrated value
        eta_T=0.01
    )

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    print("ACTUAL CALCULATION RESULTS:")
    print("-" * 90)
    print()

    results = []
    for hadron_name, knot in hadrons:
        result = calc.compute_hadron_mass(hadron_name, knot)
        results.append((hadron_name, result))

        # Extract components
        const_mass = result["constituent_mass_MeV"]
        weave_energy = result["weave_energy_MeV"]
        binding_energy = result["binding_energy_MeV"]
        predicted = result["predicted_mass_MeV"]
        expt = result["experimental_mass_MeV"]
        error_mev = predicted - expt
        error_pct = 100 * error_mev / expt

        print(f"{hadron_name.upper()}")
        print(f"  Constituent mass:     {const_mass:>8.1f} MeV")
        print(f"  Weave energy:         {weave_energy:>8.1f} MeV  (from phase-locking + surface + twist)")
        print(f"  Binding energy:       {binding_energy:>8.1f} MeV  (empirical)")
        print(f"  Predicted:            {predicted:>8.1f} MeV  (= {const_mass:.1f} + {weave_energy:.1f} + {binding_energy:.1f})")
        print(f"  Experimental:         {expt:>8.1f} MeV")
        print(f"  Error:                {error_mev:>+8.1f} MeV ({error_pct:>+6.1f}%)")
        print()

    print("="*90)
    print("PHASE-LOCKING DISSECTION")
    print("="*90)
    print()

    print("The weave energy includes THREE components:")
    print("  1. Surface term (σ_T·A): field energy at boundary")
    print("  2. Phase-locking (κ_T·Σ|ψ_i-ψ_j|²): coupling between vortex phases")
    print("  3. Twist term (η_T·∇×v): vorticity from phase circulation")
    print()
    print("The phase-locking term is the DOMINANT contribution (~95% of weave).")
    print()

    # Extract knot-level information
    print("VORTEX CONFIGURATION ANALYSIS:")
    print("-" * 90)
    print()

    for hadron_name, knot in hadrons:
        # Phase offset geometry
        phases = np.array([v.phase_offset for v in knot.vortices])
        phases_deg = np.degrees(phases)

        # Phase differences (pairwise)
        phase_diffs = []
        for i in range(len(phases)):
            for j in range(i+1, len(phases)):
                diff = abs(phases[i] - phases[j])
                diff = min(diff, 2*np.pi - diff)  # Normalize to [0, π]
                phase_diffs.append(diff)

        phase_diffs = np.array(phase_diffs)
        phase_diffs_deg = np.degrees(phase_diffs)

        print(f"{hadron_name.upper()}: {len(knot.vortices)} vortices")
        print(f"  Phase offsets (degrees): {phase_diffs_deg}")
        print(f"  Phase differences (degrees): min={np.min(phase_diffs_deg):.1f}°, max={np.max(phase_diffs_deg):.1f}°")
        print(f"  Σ(phase_diff)²: {np.sum(phase_diffs**2):.3f} rad²")
        print()

    print("="*90)
    print("MECHANISM HYPOTHESIS: Phase Configuration Sensitivity")
    print("="*90)
    print()

    print("Observation: Error sign differs by flavor")
    print("  Proton (uud):  -25 MeV  (2 up, 1 down → lighter)")
    print("  Neutron (udd): +51 MeV  (1 up, 2 down → asymmetric)")
    print("  Lambda (uds):  +147 MeV (1 up, 1 down, 1 strange → massive)")
    print()

    print("Hypothesis: The evenly-spaced phase configuration (0°, 120°, 240°)")
    print("is NOT the true equilibrium for different flavor combinations.")
    print()
    print("Instead, the phases shift based on:")
    print("  - Constituent quark masses (heavier quarks → different phase geometry)")
    print("  - Flavor mixing (mass differences between u, d, s)")
    print("  - Center-of-mass dynamics (internal oscillations)")
    print()

    print("Effect on phase-locking energy:")
    print("  If phases shift away from 120° spacing, the phase differences change.")
    print("  Different spacing → different κ_T·Σ(phase_diff)² → different binding energy.")
    print()

    # Extract error vs constituent mass correlation
    print("="*90)
    print("ERROR CORRELATION WITH CONSTITUENT MASS")
    print("="*90)
    print()

    const_masses = []
    errors_mev = []
    for hadron_name, result in results:
        const_mass = result["constituent_mass_MeV"]
        error = result["predicted_mass_MeV"] - result["experimental_mass_MeV"]
        const_masses.append(const_mass)
        errors_mev.append(error)
        print(f"{hadron_name}: m_const={const_mass:>6.1f} MeV, error={error:>+7.1f} MeV")

    print()

    # Try to find scaling pattern
    if len(const_masses) > 1:
        # Check if error scales with constituent mass
        m_avg = np.mean(const_masses)
        err_avg = np.mean(errors_mev)

        # Normalize
        m_norm = np.array(const_masses) - m_avg
        err_norm = np.array(errors_mev) - err_avg

        if np.std(m_norm) > 0:
            correlation = np.dot(m_norm, err_norm) / (np.std(m_norm) * np.std(err_norm) * len(m_norm))
            print(f"Correlation (error vs const_mass): {correlation:.3f}")

            if abs(correlation) > 0.5:
                print("✓ Error CORRELATES with constituent mass")
                print("  → Heavier quark composition → larger error")
            else:
                print("✗ Error does NOT correlate with constituent mass")
                print("  → Pattern is flavor-specific, not mass-specific")

    print()
    print("="*90)
    print("NEXT STEP: Measure Actual Phase Geometry")
    print("="*90)
    print()
    print("To fix the mechanism, we need to:")
    print()
    print("1. Determine the TRUE equilibrium phase configuration for each hadron")
    print("   (not just assume 0°, 120°, 240°)")
    print()
    print("2. Compute how the phases shift based on:")
    print("   - Constituent mass distribution")
    print("   - Flavor composition")
    print("   - Boundary radius R")
    print()
    print("3. Use the shifted phases to recompute κ_T·Σ(phase_diff)²")
    print()
    print("4. This should explain the 25-150 MeV discrepancies")
    print()


if __name__ == "__main__":
    try:
        analyze_phase_locking_mechanism()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
