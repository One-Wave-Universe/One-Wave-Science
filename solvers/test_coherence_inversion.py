#!/usr/bin/env python3
"""
Test Hypothesis: Coherence Inversion Principle

For hadrons with a symmetric pair anchor (nucleons), the binding reference frame
is set by the symmetric pair, and asymmetric pairs are decoherent.

For hadrons with NO symmetric pair anchor (hyperons with strange quark), there is
NO reference frame. All pairs are asymmetric. To maintain strong binding,
nature increases the coupling by compensating for the average decoherence.

Proposed mechanism: κ_T_effective = κ_T_base / avg_coherence

This inverts the decoherence penalty, ensuring that highly incoherent systems
still have strong binding.

Physical interpretation:
- When oscillations are well-matched (coherence ≈ 1.0): κ_T_eff ≈ κ_T_base
- When oscillations are mismatched (coherence ≈ 0.341): κ_T_eff ≈ 2.93 × κ_T_base
  This compensates for the lost energy from incoherence.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from dataclasses import dataclass
from typing import Dict, Optional
from hadron_knot_geometry import (
    QUARK_MASSES_MEV, WeaveDensity, WeavingEnergyCalculator,
    create_proton, create_neutron, create_lambda, create_pion_plus
)

HADRON_MASSES_MEV = {
    "proton": 938.3,
    "neutron": 939.6,
    "Lambda": 1115.7,
    "π⁺": 139.6,
}

@dataclass
class CoherenceInversionCalculator:
    """Calculator using coherence inversion for no-anchor hadrons."""

    sigma_T: float = 0.01
    kappa_T_base: float = 0.40        # For well-coherent systems
    eta_T: float = 0.01
    binding_correction_strength: float = 1.0

    def has_symmetric_pair(self, knot) -> bool:
        """Check if hadron has a symmetric pair (same mass quarks)."""
        masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in knot.vortices]
        for i in range(len(masses)):
            for j in range(i+1, len(masses)):
                if abs(masses[i] - masses[j]) < 0.1:  # Within 0.1 MeV
                    return True
        return False

    def compute_avg_coherence(self, knot) -> float:
        """Compute average coherence for all quark pairs."""
        masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in knot.vortices]
        kappa_T_base_mev = self.kappa_T_base * 1000
        omegas = [kappa_T_base_mev / m if m > 0 else 0 for m in masses]

        coherences = []
        for i in range(len(knot.vortices)):
            for j in range(i+1, len(knot.vortices)):
                if omegas[i] > 0 and omegas[j] > 0:
                    omega_ratio = max(omegas[i], omegas[j]) / min(omegas[i], omegas[j])
                    if omega_ratio <= 1.0:
                        coherence = 1.0
                    else:
                        coherence = 1.0 / (1.0 + np.log(omega_ratio))
                    coherences.append(coherence)

        return np.mean(coherences) if coherences else 1.0

    def compute_effective_kappa_T(self, knot) -> float:
        """Compute effective κ_T using coherence inversion for no-anchor hadrons."""
        has_anchor = self.has_symmetric_pair(knot)

        if has_anchor:
            # Nucleons: use base coupling (anchor provides reference frame)
            return self.kappa_T_base
        else:
            # Hyperons: use coherence inversion to compensate for decoherence
            avg_coherence = self.compute_avg_coherence(knot)
            return self.kappa_T_base / avg_coherence if avg_coherence > 0 else self.kappa_T_base

    def compute_weave_energy(self, knot, flavor_masses: Optional[Dict[str, float]] = None) -> float:
        """Compute weave energy with coherence inversion."""
        if flavor_masses is None:
            flavor_masses = QUARK_MASSES_MEV

        kappa_T = self.compute_effective_kappa_T(knot)

        weave = WeaveDensity(
            sigma_T=self.sigma_T,
            kappa_T=kappa_T,
            eta_T=self.eta_T,
            neck_radius=0.1,
            break_threshold=5.0
        )

        weave_calc = WeavingEnergyCalculator(weave)
        total_energy = weave_calc.total_weave_energy(knot)

        return total_energy

    def compute_binding_energy_correction(self, knot, flavor_masses: Optional[Dict[str, float]] = None) -> float:
        """Binding energy correction based on symmetric pair mass scale."""
        if flavor_masses is None:
            flavor_masses = QUARK_MASSES_MEV

        masses = []
        for vortex in knot.vortices:
            if vortex.flavor in flavor_masses:
                masses.append(flavor_masses[vortex.flavor])

        if not masses:
            return 0.0

        m_min = min(masses)
        m_max = max(masses)
        mass_range = m_max - m_min

        # Find symmetric pair
        symmetric_mass = None
        for i in range(len(masses)):
            for j in range(i+1, len(masses)):
                if masses[i] == masses[j]:
                    symmetric_mass = masses[i]
                    break

        # Determine binding correction
        if symmetric_mass is None:
            rank_factor = 0.0
        elif symmetric_mass == m_min:
            rank_factor = 1.0
        else:
            rank_factor = -1.0

        if abs(rank_factor) < 0.5:
            correction_magnitude = 0.0
        else:
            correction_magnitude = mass_range * rank_factor / 1000.0

        correction = correction_magnitude * self.binding_correction_strength

        return correction

    def compute_hadron_mass(self, hadron_name: str, knot, flavor_masses: Optional[Dict[str, float]] = None) -> Dict:
        """Compute hadron mass."""
        if flavor_masses is None:
            flavor_masses = QUARK_MASSES_MEV

        constituent_mass = sum(
            flavor_masses.get(v.flavor, 0) for v in knot.vortices
        )

        weave_energy = self.compute_weave_energy(knot, flavor_masses)

        num_vortices = knot.num_vortices
        if num_vortices == 3:
            binding_energy_base = -8.0
        elif num_vortices == 2:
            binding_energy_base = -30.0
        else:
            binding_energy_base = 0.0

        binding_correction = self.compute_binding_energy_correction(knot, flavor_masses)
        binding_energy_correction_mev = binding_correction * 1000

        binding_energy = binding_energy_base + binding_energy_correction_mev

        total_mass = constituent_mass + weave_energy * 1000 + binding_energy

        if hadron_name in HADRON_MASSES_MEV:
            experimental_mass = HADRON_MASSES_MEV[hadron_name]
            error_mev = abs(total_mass - experimental_mass)
            error_percent = (error_mev / experimental_mass) * 100
        else:
            experimental_mass = None
            error_mev = None
            error_percent = None

        kappa_used = self.compute_effective_kappa_T(knot)
        avg_coh = self.compute_avg_coherence(knot)

        return {
            "hadron_name": hadron_name,
            "has_symmetric_pair": self.has_symmetric_pair(knot),
            "avg_coherence": avg_coh,
            "kappa_T_used": kappa_used,
            "constituent_mass_MeV": constituent_mass,
            "weave_energy_MeV": weave_energy * 1000,
            "binding_energy_MeV": binding_energy,
            "predicted_mass_MeV": total_mass,
            "experimental_mass_MeV": experimental_mass,
            "error_MeV": error_mev,
            "error_percent": error_percent,
        }


def main():
    print("="*90)
    print("TEST: COHERENCE INVERSION PRINCIPLE")
    print("="*90)
    print()

    print("Hypothesis: For hadrons with NO symmetric pair anchor (like Lambda),")
    print("the binding coupling is enhanced to compensate for oscillation decoherence.")
    print()
    print("κ_T_effective = κ_T_base / avg_coherence")
    print()

    # Build hadrons
    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    calc = CoherenceInversionCalculator(
        kappa_T_base=0.40,
        sigma_T=0.01,
        eta_T=0.01,
        binding_correction_strength=1.0
    )

    results = []
    for hadron_name, knot in hadrons:
        result = calc.compute_hadron_mass(hadron_name, knot)
        results.append(result)

    # Report
    print(f"{'Hadron':<12} {'Anchor':<12} {'Coh':<8} {'κ_T':<8} {'Weave':<12} {'Total':<12} {'Error%':<10}")
    print("-" * 90)

    errors = []
    for r in results:
        anchor = "YES" if r["has_symmetric_pair"] else "NO"
        print(f"{r['hadron_name']:<12} {anchor:<12} {r['avg_coherence']:>6.3f} "
              f"{r['kappa_T_used']:>6.3f} {r['weave_energy_MeV']:>10.1f} "
              f"{r['predicted_mass_MeV']:>10.1f} {r['error_percent']:>+8.1f}%")
        if r['error_percent'] is not None:
            errors.append(r['error_percent'])

    print("-" * 90)
    avg_error = np.mean(errors) if errors else 0
    print(f"Average error: {avg_error:.1f}%")
    print()

    print("="*90)
    print("DETAILED ANALYSIS")
    print("="*90)
    print()

    for r in results:
        print(f"{r['hadron_name'].upper()}")
        print(f"  Symmetric pair anchor: {'YES ✓' if r['has_symmetric_pair'] else 'NO ✗'}")
        print(f"  Average coherence:     {r['avg_coherence']:.4f}")

        if r['has_symmetric_pair']:
            print(f"  κ_T used:              {r['kappa_T_used']:.4f} GeV (base, no inversion)")
        else:
            inversion_factor = 1.0 / r['avg_coherence'] if r['avg_coherence'] > 0 else 1.0
            print(f"  Inversion factor:      1 / {r['avg_coherence']:.4f} = {inversion_factor:.2f}×")
            print(f"  κ_T used:              {r['kappa_T_used']:.4f} GeV (base × {inversion_factor:.2f})")

        print(f"  Predicted mass:        {r['predicted_mass_MeV']:.1f} MeV")
        print(f"  Experimental mass:     {r['experimental_mass_MeV']:.1f} MeV")
        print(f"  Error:                 {r['error_percent']:+.1f}%")
        print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
