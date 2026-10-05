#!/usr/bin/env python3
"""
Coherence Factor Diagnostic: Check how oscillation decoherence affects each hadron

This script computes the coherence factors for proton, neutron, and lambda
to verify that the mechanism correctly captures the binding difference.
"""

import sys
sys.path.insert(0, "/home/claude/one-wave-science/solvers")

import numpy as np
from hadron_knot_geometry import (
    create_proton, create_neutron, create_lambda,
    QUARK_MASSES_MEV, WeaveDensity, WeavingEnergyCalculator
)

def analyze_coherence(hadron_name, knot):
    """Compute and display coherence factors for a hadron."""

    print(f"\n{'='*70}")
    print(f"HADRON: {hadron_name.upper()}")
    print(f"{'='*70}")

    # Extract masses and flavors
    vortices = knot.vortices
    masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in vortices]
    flavors = [v.flavor for v in vortices]

    print(f"\nVortex composition:")
    for flavor, mass in zip(flavors, masses):
        print(f"  {flavor}: {mass:.2f} MeV")

    # Compute oscillation frequencies
    kappa_T_base = 0.297  # GeV (0.297 * 1000 = 297 MeV)
    omegas = [kappa_T_base / m if m > 0 else 0 for m in masses]

    print(f"\nOscillation frequencies (ω = κ_T / m):")
    for flavor, omega in zip(flavors, omegas):
        print(f"  {flavor}: ω = {omega:.4f} (κ_T/m)")

    # Find symmetric pairs and compute coherence factors
    print(f"\nPair-wise coherence analysis:")

    pair_coherences = []
    for i in range(len(vortices)):
        for j in range(i+1, len(vortices)):
            m_i, m_j = masses[i], masses[j]
            f_i, f_j = flavors[i], flavors[j]
            omega_i, omega_j = omegas[i], omegas[j]

            if omega_i > 0 and omega_j > 0:
                omega_ratio = max(omega_i, omega_j) / min(omega_i, omega_j)

                # Coherence factor: 1 / (1 + log(ω_ratio))
                if omega_ratio <= 1.0:
                    coherence = 1.0
                else:
                    coherence = 1.0 / (1.0 + np.log(omega_ratio))

                pair_type = "SYMMETRIC" if m_i == m_j else "ASYMMETRIC"
                print(f"  Pair {i}-{j} ({f_i}-{f_j}): ω_ratio={omega_ratio:.2f}, "
                      f"coherence={coherence:.3f} {pair_type}")

                pair_coherences.append(coherence)

    # Average coherence
    avg_coherence = np.mean(pair_coherences) if pair_coherences else 1.0
    print(f"\nAverage coherence factor: {avg_coherence:.3f}")

    # Effective κ_T
    kappa_T_eff = kappa_T_base * avg_coherence
    print(f"κ_T_base = {kappa_T_base:.3f} GeV")
    print(f"κ_T_eff = κ_T_base × avg_coherence = {kappa_T_eff:.3f} GeV")
    print(f"Coupling reduction factor: {100 * (1 - avg_coherence):.1f}%")

    # Determine binding reference frame
    m_min = min(masses)
    symmetric_masses = []
    for i in range(len(masses)):
        for j in range(i+1, len(masses)):
            if masses[i] == masses[j]:
                symmetric_masses.append(masses[i])

    if symmetric_masses:
        sym_mass = symmetric_masses[0]
        if sym_mass == m_min:
            binding_frame = "LIGHT ANCHOR (symmetric pair is lightest)"
            expected_error_sign = "NEGATIVE"
        else:
            binding_frame = "HEAVY ANCHOR (symmetric pair is heavier)"
            expected_error_sign = "POSITIVE"
    else:
        binding_frame = "NO SYMMETRIC PAIR (all different)"
        expected_error_sign = "LARGE POSITIVE"

    print(f"\nBinding reference frame: {binding_frame}")
    print(f"Expected error sign: {expected_error_sign}")

    return {
        "hadron": hadron_name,
        "avg_coherence": avg_coherence,
        "kappa_T_eff": kappa_T_eff,
        "binding_frame": binding_frame,
    }


def main():
    print("="*70)
    print("COHERENCE FACTOR DIAGNOSTIC")
    print("="*70)

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    results = []
    for hadron_name, knot in hadrons:
        result = analyze_coherence(hadron_name, knot)
        results.append(result)

    # Summary table
    print(f"\n\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}\n")

    print(f"{'Hadron':<12} {'Avg Coherence':>15} {'κ_T_eff (GeV)':>15} {'Binding Frame':<25}")
    print("-" * 70)

    for r in results:
        print(f"{r['hadron']:<12} {r['avg_coherence']:>14.3f} {r['kappa_T_eff']:>14.3f} {r['binding_frame']:<25}")

    print()

    # Cross-check with experimental observations
    actual_errors = {
        "proton": -23.9,      # MeV (underpredicted)
        "neutron": +27.7,     # MeV (overpredicted)
        "Lambda": +203.5,     # MeV (vastly overpredicted)
    }

    print(f"{'='*70}")
    print("CROSS-CHECK WITH OBSERVED ERRORS")
    print(f"{'='*70}\n")

    print(f"{'Hadron':<12} {'Expected Sign':<20} {'Actual Error':>15} {'Match':>8}")
    print("-" * 70)

    for r in results:
        # Extract expected sign from binding frame
        if "LIGHT" in r["binding_frame"]:
            expected_sign = "NEGATIVE"
        elif "NO" in r["binding_frame"]:
            expected_sign = "POSITIVE"
        else:
            expected_sign = "POSITIVE"

        actual_error = actual_errors[r["hadron"]]
        actual_sign = "NEGATIVE" if actual_error < 0 else "POSITIVE"

        match = "✓" if expected_sign == actual_sign else "✗"

        print(f"{r['hadron']:<12} {expected_sign:<20} {actual_error:>+14.1f} {match:>8}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
