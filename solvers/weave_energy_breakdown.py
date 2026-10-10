#!/usr/bin/env python3
"""
Weave Energy Breakdown Diagnostic

Analyze the phase-locking energy contributions by pair type for each hadron.
This reveals why Neutron's weave energy is higher than Proton's and why Lambda
is underpredicted.

Key Questions:
1. Why does Neutron have higher weave energy than Proton?
2. Are symmetric pairs (same mass) correctly getting full coupling?
3. Are asymmetric pairs (different mass) correctly getting reduced coupling?
4. Does the Phase 5 κ_T scaling (κ_T = κ_T_base × √m_scale) introduce an asymmetry?
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from hadron_knot_geometry import (
    QUARK_MASSES_MEV, WeaveDensity, WeavingEnergyCalculator,
    create_proton, create_neutron, create_lambda
)

def analyze_phase_locking_by_pair(hadron_name, knot, kappa_T_base=0.297, sigma_T=0.01):
    """Detailed breakdown of phase-locking energy by pair type."""

    print(f"\n{'='*80}")
    print(f"HADRON: {hadron_name.upper()}")
    print(f"{'='*80}")

    # Extract vortex information
    vortices = knot.vortices
    masses = [QUARK_MASSES_MEV.get(v.flavor, 0.0) for v in vortices]
    flavors = [v.flavor for v in vortices]

    print(f"\nQuark composition:")
    for i, (flavor, mass) in enumerate(zip(flavors, masses)):
        print(f"  q{i}: {flavor:8s}  mass = {mass:8.2f} MeV")

    # Compute oscillation frequencies
    omegas = [kappa_T_base / m if m > 0 else 0.0 for m in masses]

    print(f"\nOscillation frequencies (ω = κ_T_base / m):")
    print(f"  κ_T_base = {kappa_T_base:.3f} GeV = {kappa_T_base*1000:.1f} MeV")
    for i, (flavor, omega) in enumerate(zip(flavors, omegas)):
        print(f"  q{i} ({flavor:8s}): ω = {omega:.6f}")

    # Compute Phase 5 κ_T scaling
    geometric_mean = np.prod(masses) ** (1.0 / len(masses))
    m_scale = geometric_mean / QUARK_MASSES_MEV["up"]
    kappa_T_scaled = kappa_T_base * np.sqrt(m_scale)

    print(f"\nPhase 5 κ_T scaling:")
    print(f"  Geometric mean of masses: {geometric_mean:.2f} MeV")
    print(f"  m_scale = geom_mean / m_up = {m_scale:.4f}")
    print(f"  κ_T_scaled = κ_T_base × √m_scale = {kappa_T_base:.3f} × {np.sqrt(m_scale):.4f}")
    print(f"              = {kappa_T_scaled:.4f} GeV")

    # Now analyze each pair
    print(f"\n{'Pair':<10} {'Masses':<20} {'ω_ratio':<10} {'Coherence':<12} {'κ_T_ij':<12} {'Type':<15}")
    print("-" * 80)

    pair_energies = []
    for i in range(len(vortices)):
        for j in range(i+1, len(vortices)):
            m_i, m_j = masses[i], masses[j]
            f_i, f_j = flavors[i], flavors[j]
            omega_i, omega_j = omegas[i], omegas[j]

            # Coherence factor
            if omega_i > 0 and omega_j > 0:
                omega_ratio = max(omega_i, omega_j) / min(omega_i, omega_j)
                if omega_ratio <= 1.0:
                    coherence = 1.0
                else:
                    coherence = 1.0 / (1.0 + np.log(omega_ratio))
            else:
                omega_ratio = 1.0
                coherence = 1.0

            # κ_T for this pair (using original κ_T_base, not scaled)
            kappa_T_ij = kappa_T_base * coherence

            # Determine pair type
            if abs(m_i - m_j) < 0.1:  # Same mass (within 0.1 MeV)
                pair_type = "SYMMETRIC"
            else:
                pair_type = "ASYMMETRIC"

            pair_label = f"q{i}-q{j}"
            masses_str = f"{m_i:.1f}-{m_j:.1f}"

            print(f"{pair_label:<10} {masses_str:<20} {omega_ratio:<10.4f} {coherence:<12.4f} "
                  f"{kappa_T_ij:<12.4f} {pair_type:<15}")

            pair_energies.append({
                "pair": pair_label,
                "type": pair_type,
                "coherence": coherence,
                "kappa_T_ij": kappa_T_ij,
                "m_i": m_i,
                "m_j": m_j,
                "omega_ratio": omega_ratio,
            })

    # Summary statistics
    print(f"\n{'SUMMARY':<80}")
    print(f"-" * 80)

    symmetric_pairs = [p for p in pair_energies if p["type"] == "SYMMETRIC"]
    asymmetric_pairs = [p for p in pair_energies if p["type"] == "ASYMMETRIC"]

    if symmetric_pairs:
        avg_sym_coherence = np.mean([p["coherence"] for p in symmetric_pairs])
        avg_sym_kappa = np.mean([p["kappa_T_ij"] for p in symmetric_pairs])
        print(f"Symmetric pairs ({len(symmetric_pairs)}):")
        print(f"  Average coherence: {avg_sym_coherence:.4f}")
        print(f"  Average κ_T_ij:    {avg_sym_kappa:.4f} GeV")

    if asymmetric_pairs:
        avg_asym_coherence = np.mean([p["coherence"] for p in asymmetric_pairs])
        avg_asym_kappa = np.mean([p["kappa_T_ij"] for p in asymmetric_pairs])
        print(f"Asymmetric pairs ({len(asymmetric_pairs)}):")
        print(f"  Average coherence: {avg_asym_coherence:.4f}")
        print(f"  Average κ_T_ij:    {avg_asym_kappa:.4f} GeV")

    # Compute actual weave energy with pair-wise breakdown
    weave = WeaveDensity(
        sigma_T=sigma_T,
        kappa_T=kappa_T_base,  # Use base, not scaled
        eta_T=0.01,
        neck_radius=0.1,
        break_threshold=5.0
    )

    weave_calc = WeavingEnergyCalculator(weave)

    # Monte Carlo sampling to get actual energy distribution
    np.random.seed(42)
    num_samples = 100
    boundary_radius = knot.boundary_radius

    # Dictionary to track energy per pair type
    energy_by_pair = {p["pair"]: 0.0 for p in pair_energies}
    total_energy_sampled = 0.0

    for sample_idx in range(num_samples):
        # Random point inside sphere
        r = boundary_radius * np.random.uniform(0, 1)**(1/3)
        theta = np.arccos(np.random.uniform(-1, 1))
        phi = np.random.uniform(0, 2*np.pi)

        # Pairwise contributions - use nested loops to match pair order
        pair_idx = 0
        for i in range(len(vortices)):
            for j in range(i+1, len(vortices)):
                pair_info = pair_energies[pair_idx]

                psi_i = vortices[i].spherical_harmonic(theta, phi)
                psi_j = vortices[j].spherical_harmonic(theta, phi)
                phase_diff = abs(psi_i - psi_j)**2

                # Apply pair-specific κ_T
                kappa_T_ij = pair_info["kappa_T_ij"]
                energy_contribution = kappa_T_ij * phase_diff

                energy_by_pair[pair_info["pair"]] += energy_contribution
                total_energy_sampled += energy_contribution

                pair_idx += 1

    # Normalize by volume
    volume = (4/3) * np.pi * boundary_radius**3
    for pair_label in energy_by_pair:
        energy_by_pair[pair_label] *= volume / num_samples
    total_energy_sampled *= volume / num_samples

    # Report per-pair energies
    print(f"\nPhase-locking energy contribution by pair:")
    print(f"{'Pair':<10} {'Type':<15} {'Energy (MeV)':<15} {'% of Total':<12}")
    print(f"-" * 52)

    for pair_info in pair_energies:
        pair_label = pair_info["pair"]
        pair_type = pair_info["type"]
        energy_mev = energy_by_pair[pair_label] * 1000
        percent = (energy_by_pair[pair_label] / total_energy_sampled * 100) if total_energy_sampled > 0 else 0

        print(f"{pair_label:<10} {pair_type:<15} {energy_mev:>13.1f} {percent:>10.1f}%")

    print(f"-" * 52)
    print(f"{'TOTAL':<10} {'':<15} {total_energy_sampled*1000:>13.1f} {'100.0%':>10}")

    return {
        "hadron": hadron_name,
        "total_phase_energy": total_energy_sampled,
        "energy_by_pair": energy_by_pair,
        "pair_info": pair_energies,
        "symmetric_count": len(symmetric_pairs),
        "asymmetric_count": len(asymmetric_pairs),
    }


def main():
    print("="*80)
    print("WEAVE ENERGY BREAKDOWN DIAGNOSTIC")
    print("="*80)

    # Build hadrons
    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    # Use Phase 5 calibrated parameters
    kappa_T_base = 0.297  # GeV
    sigma_T = 0.01       # GeV/fm²

    print(f"\nPhase 5 Parameters:")
    print(f"  κ_T_base: {kappa_T_base} GeV")
    print(f"  σ_T: {sigma_T} GeV/fm²")

    results = []
    for hadron_name, knot in hadrons:
        result = analyze_phase_locking_by_pair(hadron_name, knot, kappa_T_base, sigma_T)
        results.append(result)

    # Cross-hadron comparison
    print(f"\n\n{'='*80}")
    print("CROSS-HADRON COMPARISON")
    print(f"{'='*80}\n")

    print(f"{'Hadron':<12} {'Phase Energy (MeV)':<20} {'Symmetric Pairs':<18} {'Asymmetric Pairs':<18}")
    print("-" * 70)

    for r in results:
        phase_energy_mev = r["total_phase_energy"] * 1000
        print(f"{r['hadron']:<12} {phase_energy_mev:>18.1f} {r['symmetric_count']:>16} {r['asymmetric_count']:>16}")

    # Analysis
    print(f"\n{'='*80}")
    print("KEY FINDINGS")
    print(f"{'='*80}\n")

    proton_result = [r for r in results if r['hadron'] == 'proton'][0]
    neutron_result = [r for r in results if r['hadron'] == 'neutron'][0]
    lambda_result = [r for r in results if r['hadron'] == 'Lambda'][0]

    proton_energy = proton_result["total_phase_energy"] * 1000
    neutron_energy = neutron_result["total_phase_energy"] * 1000
    lambda_energy = lambda_result["total_phase_energy"] * 1000

    energy_diff = neutron_energy - proton_energy

    print(f"1. Neutron vs Proton Phase-Locking Energy:")
    print(f"   Proton:  {proton_energy:>8.1f} MeV")
    print(f"   Neutron: {neutron_energy:>8.1f} MeV")
    print(f"   Difference: {energy_diff:>+6.1f} MeV (neutron is {'HIGHER' if energy_diff > 0 else 'LOWER'})")
    print()

    if abs(energy_diff) > 50:
        print(f"   ⚠️  ISSUE: Neutron energy is {abs(energy_diff):.0f} MeV higher than Proton!")
        print(f"       This is OPPOSITE of expectation (Proton should be slightly higher)")
        print(f"       Likely cause: Phase 5 κ_T scaling introduces asymmetry")
        print()

    print(f"2. Lambda Phase-Locking Energy:")
    print(f"   Lambda:  {lambda_energy:>8.1f} MeV")
    print(f"   (All asymmetric pairs, no symmetric anchor)")
    print()

    print(f"3. Pair Type Composition:")
    print(f"   Proton:  {proton_result['symmetric_count']} symmetric, {proton_result['asymmetric_count']} asymmetric")
    print(f"   Neutron: {neutron_result['symmetric_count']} symmetric, {neutron_result['asymmetric_count']} asymmetric")
    print(f"   Lambda:  {lambda_result['symmetric_count']} symmetric, {lambda_result['asymmetric_count']} asymmetric")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
