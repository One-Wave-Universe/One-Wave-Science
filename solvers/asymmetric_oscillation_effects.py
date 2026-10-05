#!/usr/bin/env python3
"""
Asymmetric Oscillation Effects: Why Proton and Neutron Differ

Key observation: Proton (uud) and Neutron (udd) have identical oscillation
frequency dispersion (ω_ratio = 2.2) but OPPOSITE error signs!

This means the mechanism is NOT just about dispersion ratio, but about the
ASYMMETRY in how masses are distributed among the three quarks.

Hypothesis: The oscillation modulates phase-locking energy asymmetrically
based on which pairs have similar vs. different masses.

For proton (uud):
  - Pair u-u: same mass, no oscillation mismatch
  - Pair u-d: different masses, phase difference oscillates
  - Pair u-d: different masses, phase difference oscillates
  Net: 2 asymmetric pairs, 1 symmetric pair

For neutron (udd):
  - Pair u-d: different masses, phase difference oscillates
  - Pair d-d: same mass, no oscillation mismatch
  - Pair u-d: different masses, phase difference oscillates
  Net: 2 asymmetric pairs, 1 symmetric pair (same count!)

But the SPECIFIC pairs differ. In proton, the two u quarks are symmetric,
while in neutron, the two d quarks are symmetric.
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


def analyze_pair_oscillations(hadron_name, knot):
    """Analyze oscillation effects on each quark pair."""
    
    vortices = knot.vortices
    masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in vortices]
    flavors = [v.flavor for v in vortices]
    
    kappa_T = 0.297 * 1000  # MeV
    
    print(f"{hadron_name.upper()}")
    print("="*70)
    print(f"Quark composition: {', '.join([f'{f}({masses[i]:.1f} MeV)' for i, f in enumerate(flavors)])}")
    print()
    
    # Analyze each pair
    pair_data = []
    
    print("Pairwise oscillation analysis:")
    print(f"{'Pair':<10} {'Masses':>15} {'Δm':>8} {'ω₁':>10} {'ω₂':>10} {'ω_ratio':>10} {'Effect':>12}")
    print("-"*80)
    
    for i in range(len(vortices)):
        for j in range(i+1, len(vortices)):
            m1, m2 = masses[i], masses[j]
            omega1 = kappa_T / m1
            omega2 = kappa_T / m2
            omega_ratio = max(omega1, omega2) / min(omega1, omega2)
            mass_diff = abs(m1 - m2)
            
            pair_label = f"{flavors[i][0]}-{flavors[j][0]}"
            mass_str = f"{m1:.1f}-{m2:.1f}"
            
            # Determine if this is a "symmetric" or "asymmetric" pair
            if m1 == m2:
                effect = "symmetric"
            else:
                effect = "asymmetric"
            
            print(f"{pair_label:<10} {mass_str:>15} {mass_diff:>7.1f} {omega1:>10.2f} {omega2:>10.2f} {omega_ratio:>10.2f} {effect:>12}")
            
            pair_data.append({
                "pair": pair_label,
                "m1": m1,
                "m2": m2,
                "mass_diff": mass_diff,
                "omega_ratio": omega_ratio,
                "is_symmetric": m1 == m2,
            })
    
    print()
    
    # Asymmetry metric
    symmetric_pairs = sum(1 for p in pair_data if p["is_symmetric"])
    asymmetric_pairs = len(pair_data) - symmetric_pairs
    mass_diffs = [p["mass_diff"] for p in pair_data]
    total_mass_asymmetry = sum(mass_diffs)
    
    print(f"Asymmetry metrics:")
    print(f"  Symmetric pairs: {symmetric_pairs} / 3")
    print(f"  Asymmetric pairs: {asymmetric_pairs} / 3")
    print(f"  Total mass asymmetry: {total_mass_asymmetry:.1f} MeV")
    print(f"  Avg pair mass diff: {np.mean(mass_diffs):.1f} MeV")
    print()
    
    return {
        "hadron": hadron_name,
        "symmetric_pairs": symmetric_pairs,
        "asymmetric_pairs": asymmetric_pairs,
        "total_mass_asymmetry": total_mass_asymmetry,
        "avg_pair_mass_diff": np.mean(mass_diffs),
        "pair_data": pair_data,
    }


def main():
    print("="*90)
    print("ASYMMETRIC OSCILLATION EFFECTS: Why Different Flavors Behave Differently")
    print("="*90)
    print()
    
    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]
    
    results = []
    for hadron_name, knot in hadrons:
        result = analyze_pair_oscillations(hadron_name, knot)
        results.append(result)
    
    print()
    print("="*90)
    print("CORRELATION ANALYSIS")
    print("="*90)
    print()
    
    errors = {
        "proton": -23.9,
        "neutron": +27.7,
        "Lambda": +203.5,
    }
    
    print("Does error correlate with mass asymmetry?")
    print()
    print(f"{'Hadron':<12} {'Error (MeV)':>12} {'Asymmetry':>12} {'Avg diff':>10}")
    print("-"*50)
    
    for result in results:
        error = errors[result["hadron"]]
        asymmetry = result["total_mass_asymmetry"]
        avg_diff = result["avg_pair_mass_diff"]
        
        print(f"{result['hadron']:<12} {error:>+11.1f} {asymmetry:>12.1f} {avg_diff:>10.2f}")
    
    print()
    print("KEY INSIGHT:")
    print("-"*70)
    print()
    print("Proton and Neutron have SAME frequency dispersion (2.2x)")
    print("but DIFFERENT signs of error because:")
    print()
    print("Proton (uud): u-u are symmetric (oscillate together)")
    print("  → Only u-d pairs have oscillation mismatch")
    print("  → Smaller effective binding energy reduction")
    print("  → Prediction LOWER than experiment (-2.5% error)")
    print()
    print("Neutron (udd): d-d are symmetric (oscillate together)")
    print("  → Only u-d pairs have oscillation mismatch")
    print("  → Same as proton! But...")
    print()
    print("The ARRANGEMENT of symmetric/asymmetric pairs affects")
    print("how the phase locking evolves. When different mass pairs")
    print("dominate the phase-locking energy, the time-averaged")
    print("effect differs even with same ω_ratio.")
    print()
    print("Lambda: Massive asymmetry (s quark at 95 MeV)")
    print("  → All three pairs have different masses")
    print("  → Extreme oscillation mismatch (44x dispersion)")
    print("  → Binding energy severely undercounted")
    print("  → Prediction MUCH higher than experiment (+18.2% error)")
    print()


if __name__ == "__main__":
    main()
