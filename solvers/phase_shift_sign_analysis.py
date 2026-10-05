#!/usr/bin/env python3
"""
Phase-Shift Sign Analysis: Why Proton and Neutron Have Opposite Errors

KEY OBSERVATION: Proton and Neutron have identical ω_ratio (2.16) and
identical total asymmetry (3.3 MeV), but OPPOSITE error signs:
  - Proton: -23.9 MeV (mass UNDERPREDICTED)
  - Neutron: +27.7 MeV (mass OVERPREDICTED)

This cannot be explained by formulas based only on ω_ratio and asymmetry.
There must be a SIGN-DETERMINING factor.

Hypothesis: The sign depends on whether the symmetric pair is the
MINIMUM mass quark in the hadron.

Proton (uud): u-u symmetric, u is MINIMUM mass
  → Lightest quarks define the binding scale
  → Binding energy likely STRONGER than assumed
  → Prediction LOWER (negative error)

Neutron (udd): d-d symmetric, d is NOT minimum mass (u is)
  → Mixed mass scales for binding
  → Binding energy WEAKER than assumed
  → Prediction HIGHER (positive error)

Lambda (uds): No symmetric pair, all different masses
  → Maximum asymmetry in oscillation
  → Binding energy UNDERCOUNTED
  → Prediction MUCH HIGHER (large positive error)
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


def analyze_symmetric_pair_role(hadron_name, knot):
    """Analyze how the symmetric pair's mass rank affects binding."""

    vortices = knot.vortices
    masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in vortices]
    flavors = [v.flavor for v in vortices]

    m_min = min(masses)
    m_max = max(masses)
    m_avg = np.mean(masses)

    # Find symmetric pair
    symmetric_mass = None
    symmetric_pair_indices = []
    for i in range(len(masses)):
        for j in range(i+1, len(masses)):
            if masses[i] == masses[j]:
                symmetric_mass = masses[i]
                symmetric_pair_indices = [i, j]
                break

    # If no exact symmetric pair, find closest match
    if symmetric_mass is None:
        # Find pair with smallest mass difference
        min_diff = float('inf')
        for i in range(len(masses)):
            for j in range(i+1, len(masses)):
                diff = abs(masses[i] - masses[j])
                if diff < min_diff:
                    min_diff = diff
                    symmetric_mass = masses[i]
                    symmetric_pair_indices = [i, j]

    # Determine mass rank of symmetric pair
    if symmetric_mass == m_min:
        sym_rank = "MINIMUM"
    elif symmetric_mass == m_max:
        sym_rank = "MAXIMUM"
    else:
        sym_rank = "INTERMEDIATE"

    # The asymmetric pairs (not the symmetric pair)
    asymmetric_pairs = []
    for i in range(len(masses)):
        if i not in symmetric_pair_indices:
            # Pair with the symmetric pair members
            asym_mass = masses[i]
            asymmetric_pairs.append({
                "mass": asym_mass,
                "diff_from_sym": abs(asym_mass - symmetric_mass),
            })

    # Compute oscillation frequency dispersion within pairs
    kappa_T = 0.297 * 1000  # MeV

    # Symmetric pair frequency mismatch (if masses differ even slightly)
    sym_masses = [masses[i] for i in symmetric_pair_indices]
    if len(set(sym_masses)) > 1:
        sym_freq_ratio = max(sym_masses) / min(sym_masses)
    else:
        sym_freq_ratio = 1.0

    # Asymmetric pair frequency mismatches
    asym_freq_mismatches = []
    for i in range(len(masses)):
        if i not in symmetric_pair_indices:
            # Mismatch with symmetric pair
            for j in symmetric_pair_indices:
                if masses[i] != masses[j]:
                    freq_ratio = max(masses[i], masses[j]) / min(masses[i], masses[j])
                    asym_freq_mismatches.append(freq_ratio)

    # Average asymmetric pair frequency mismatch
    avg_asym_mismatch = np.mean(asym_freq_mismatches) if asym_freq_mismatches else 1.0

    return {
        "hadron": hadron_name,
        "masses": masses,
        "flavors": flavors,
        "m_min": m_min,
        "m_max": m_max,
        "m_avg": m_avg,
        "symmetric_mass": symmetric_mass,
        "symmetric_rank": sym_rank,
        "symmetric_pair_indices": symmetric_pair_indices,
        "sym_freq_ratio": sym_freq_ratio,
        "avg_asym_mismatch": avg_asym_mismatch,
        "num_asymmetric_pairs": len(asym_freq_mismatches),
    }


def main():
    print("="*90)
    print("PHASE-SHIFT SIGN ANALYSIS: Role of Symmetric Pair Mass Rank")
    print("="*90)
    print()

    hadrons_meta = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    # Observed errors
    errors = {
        "proton": -23.9,
        "neutron": +27.7,
        "Lambda": +203.5,
    }

    results = []
    for hadron_name, knot in hadrons_meta:
        analysis = analyze_symmetric_pair_role(hadron_name, knot)
        analysis["error"] = errors[hadron_name]
        results.append(analysis)

    # Display detailed analysis
    print("INDIVIDUAL ANALYSIS:")
    print("-" * 90)
    print()

    for r in results:
        print(f"{r['hadron'].upper()}")
        mass_str = " + ".join([f"{f}({m:.1f})" for f, m in zip(r['flavors'], r['masses'])])
        print(f"  Composition: {mass_str}")
        print(f"  m_min={r['m_min']:.2f}, m_avg={r['m_avg']:.2f}, m_max={r['m_max']:.2f}")
        print()
        print(f"  Symmetric pair: mass={r['symmetric_mass']:.2f} MeV ({r['symmetric_rank']})")
        print(f"  Symmetric pair frequency ratio: {r['sym_freq_ratio']:.2f}")
        print(f"  Avg asymmetric pair frequency mismatch: {r['avg_asym_mismatch']:.2f}")
        print(f"  Number of asymmetric pairs: {r['num_asymmetric_pairs']}")
        print()
        print(f"  OBSERVED ERROR: {r['error']:+.1f} MeV")
        print()

    # Comparison
    print("="*90)
    print("COMPARATIVE ANALYSIS")
    print("="*90)
    print()

    print("KEY QUESTION: Why do Proton and Neutron have opposite errors?")
    print()
    print(f"{'Hadron':<12} {'Sym. Rank':<15} {'Sym. Mass':<12} {'Freq Ratio':<12} {'Error':>10}")
    print("-" * 65)

    for r in results:
        print(f"{r['hadron']:<12} {r['symmetric_rank']:<15} {r['symmetric_mass']:>10.2f} {r['avg_asym_mismatch']:>11.2f} {r['error']:>+9.1f}")

    print()
    print("OBSERVATION:")
    print("-" * 65)
    print()
    print("Proton:   Symmetric pair is MINIMUM mass (u at 2.16 MeV)")
    print("          → Phase differences modulated by LIGHT quark oscillations")
    print("          → Binding energy STRONGER → mass UNDERPREDICTED (-23.9 MeV)")
    print()
    print("Neutron:  Symmetric pair is NOT minimum (d at 4.67 MeV, u at 2.16 MeV)")
    print("          → Phase differences modulated by MIXED oscillations")
    print("          → Binding energy WEAKER → mass OVERPREDICTED (+27.7 MeV)")
    print()
    print("Lambda:   No symmetric pair (all different: u/d/s)")
    print("          → Phase differences maximally modulated")
    print("          → Binding energy SEVERELY undercounted → mass HUGELY OVERPREDICTED (+203.5 MeV)")
    print()

    # Proposed correction mechanism
    print("="*90)
    print("PROPOSED CORRECTION MECHANISM")
    print("="*90)
    print()

    print("ΔE_correction depends on:")
    print()
    print("1. Is there a symmetric pair? (Yes/No)")
    print("   - If YES: Symmetric pair sets the oscillation baseline")
    print("   - If NO: Maximum asymmetry in oscillations")
    print()
    print("2. Is the symmetric pair the MINIMUM mass quark? (Yes/No)")
    print("   - If YES (Proton): Light quark binding scale")
    print("     → Correction NEGATIVE (binding stronger)")
    print("   - If NO (Neutron): Mixed binding scale")
    print("     → Correction POSITIVE (binding weaker)")
    print()
    print("3. What is the total mass asymmetry? (scales magnitude)")
    print("   - Small (Proton/Neutron ~3 MeV): ~25-30 MeV correction")
    print("   - Large (Lambda ~122 MeV): ~200+ MeV correction")
    print()

    # Test correction formula
    print("="*90)
    print("TEST CORRECTION FORMULA")
    print("="*90)
    print()

    print("Proposed: ΔE = ±A × asymmetry × g(ω_ratio) × h(sym_rank)")
    print()
    print("where:")
    print("  h(sym_rank) = +1 if symmetric_pair is MINIMUM")
    print("              = -1 if symmetric_pair is NOT MINIMUM")
    print("              = -2 if NO symmetric pair (maximum asymmetry)")
    print()

    # Fit this formula
    corrections = []
    for r in results:
        if r['symmetric_rank'] == 'MINIMUM':
            rank_factor = 1.0
        else:
            rank_factor = -1.0

        # For Lambda, no symmetric pair
        if 'Lambda' in r['hadron']:
            rank_factor = -2.0

        corrections.append({
            "hadron": r['hadron'],
            "error": r['error'],
            "asymmetry": r['m_max'] - r['m_min'],  # Use max-min as asymmetry
            "rank_factor": rank_factor,
        })

    print("Asymmetry metrics:")
    print(f"{'Hadron':<12} {'Error':>10} {'Max-Min':<10} {'Rank Factor':<12}")
    print("-" * 50)
    for c in corrections:
        print(f"{c['hadron']:<12} {c['error']:>+9.1f} {c['asymmetry']:>9.1f} {c['rank_factor']:>+11.1f}")

    print()

    # Fit A parameter
    # error = A × asymmetry × rank_factor
    # A = error / (asymmetry × rank_factor)
    A_values = []
    for c in corrections:
        if c['asymmetry'] != 0:
            A = c['error'] / (c['asymmetry'] * c['rank_factor'])
            A_values.append(A)
            print(f"{c['hadron']}: A = {A:.4f}")

    print()
    if A_values:
        A_avg = np.mean(A_values)
        A_std = np.std(A_values)
        print(f"Average A: {A_avg:.4f} ± {A_std:.4f}")

    print()


if __name__ == "__main__":
    main()
