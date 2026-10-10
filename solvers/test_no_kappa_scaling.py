#!/usr/bin/env python3
"""
Test hadron mass predictions WITHOUT Phase 5 κ_T scaling.

Hypothesis: The Phase 5 κ_T scaling (κ_T ∝ √m_scale) is harmful for hadrons
because it makes Neutron's coupling HIGHER than Proton's, when it should be similar.

This test uses κ_T_base = 0.297 GeV for all hadrons without scaling.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from dataclasses import dataclass
from typing import Dict, Optional
from hadron_knot_geometry import (
    QUARK_MASSES_MEV, WeaveDensity, WeavingEnergyCalculator,
    create_proton, create_neutron, create_lambda
)

HADRON_MASSES_MEV = {
    "proton": 938.3,
    "neutron": 939.6,
    "Lambda": 1115.7,
}

@dataclass
class SimpleHadronMassCalculator:
    """Simplified calculator: NO Phase 5 κ_T scaling, just pair-wise coherence."""

    sigma_T: float = 0.01              # Surface tension
    kappa_T_base: float = 0.297        # Base phase-locking coupling (GeV) - constant
    eta_T: float = 0.01                # Twist coefficient
    binding_correction_strength: float = 1.0

    def compute_weave_energy(self, knot, flavor_masses: Optional[Dict[str, float]] = None) -> float:
        """Compute weave energy WITHOUT Phase 5 κ_T scaling."""
        if flavor_masses is None:
            flavor_masses = QUARK_MASSES_MEV

        # Use constant κ_T_base (no scaling)
        weave = WeaveDensity(
            sigma_T=self.sigma_T,
            kappa_T=self.kappa_T_base,  # Constant, not scaled
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

        return {
            "hadron_name": hadron_name,
            "constituent_mass_MeV": constituent_mass,
            "weave_energy_MeV": weave_energy * 1000,
            "binding_energy_MeV": binding_energy,
            "predicted_mass_MeV": total_mass,
            "experimental_mass_MeV": experimental_mass,
            "error_MeV": error_mev,
            "error_percent": error_percent,
            "boundary_radius_fm": knot.boundary_radius,
        }


def main():
    print("="*90)
    print("TEST: HADRON MASSES WITHOUT PHASE 5 κ_T SCALING")
    print("="*90)
    print()

    print("Hypothesis: Phase 5 κ_T scaling makes Neutron coupling HIGHER than Proton")
    print("Expected: Removing scaling should improve Neutron predictions")
    print()

    # Test with different κ_T_base values
    test_values = [0.25, 0.297, 0.35, 0.40]

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    for kappa_test in test_values:
        print("="*90)
        print(f"Testing κ_T_base = {kappa_test:.3f} GeV (NO Phase 5 scaling)")
        print("="*90)
        print()

        calc = SimpleHadronMassCalculator(
            kappa_T_base=kappa_test,
            sigma_T=0.01,
            eta_T=0.01,
            binding_correction_strength=1.0
        )

        results = []
        for hadron_name, knot in hadrons:
            result = calc.compute_hadron_mass(hadron_name, knot)
            results.append(result)

        # Report
        print(f"{'Hadron':<12} {'Weave (MeV)':<15} {'Binding (MeV)':<15} {'Total (MeV)':<15} {'Error %':<10}")
        print("-" * 70)

        errors = []
        for r in results:
            print(f"{r['hadron_name']:<12} {r['weave_energy_MeV']:>13.1f} {r['binding_energy_MeV']:>13.1f} "
                  f"{r['predicted_mass_MeV']:>13.1f} {r['error_percent']:>+8.1f}%")
            if r['error_percent'] is not None:
                errors.append(r['error_percent'])

        avg_error = np.mean(errors) if errors else 0
        print("-" * 70)
        print(f"Average error: {avg_error:.1f}%")
        print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
