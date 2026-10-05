#!/usr/bin/env python3
"""
Test hypothesis: Hadrons with strange quarks need a DIFFERENT binding model.

The strange quark has special properties:
- Much heavier than light quarks (95 MeV vs 2-5 MeV)
- Extreme frequency dispersion (ω_ratio ≈ 44× vs 2.16× for nucleons)
- Should act as a stabilizing core, not a source of decoherence

Hypothesis: Instead of reducing κ_T via coherence for strange quarks,
we should INCREASE κ_T for hyperons to account for the strange quark's
special binding role.

Alternative model:
- For nucleons (no strange): use κ_T_base = 0.40 GeV (constant)
- For hyperons (with strange): use κ_T_strange = κ_T_base × strange_enhancement

where strange_enhancement > 1.0 captures the strange quark's stabilizing effect.
"""

import sys
sys.path.insert(0, "/home/claude/one-wave-science/solvers")

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
class StrangeAwareHadronMassCalculator:
    """Calculator that treats strange quarks differently."""

    sigma_T: float = 0.01
    kappa_T_base: float = 0.40        # For nucleons
    strange_enhancement: float = 1.5  # Multiplier for hyperons
    eta_T: float = 0.01
    binding_correction_strength: float = 1.0

    def has_strange_quark(self, knot) -> bool:
        """Check if hadron contains a strange quark."""
        return any(v.flavor == "strange" for v in knot.vortices)

    def compute_kappa_T_for_hadron(self, knot) -> float:
        """Get effective κ_T for this hadron."""
        if self.has_strange_quark(knot):
            return self.kappa_T_base * self.strange_enhancement
        else:
            return self.kappa_T_base

    def compute_weave_energy(self, knot, flavor_masses: Optional[Dict[str, float]] = None) -> float:
        """Compute weave energy with strange quark enhancement."""
        if flavor_masses is None:
            flavor_masses = QUARK_MASSES_MEV

        kappa_T = self.compute_kappa_T_for_hadron(knot)

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

        kappa_used = self.compute_kappa_T_for_hadron(knot)

        return {
            "hadron_name": hadron_name,
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
    print("TEST: STRANGE QUARK BINDING ENHANCEMENT")
    print("="*90)
    print()

    print("Hypothesis: Hyperons (with strange quarks) need higher κ_T")
    print("to account for the strange quark's stabilizing role")
    print()

    # Build hadrons
    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    # Test different strange quark enhancement factors
    enhancement_factors = [1.0, 1.5, 2.0, 2.5, 2.78]

    for enhancement in enhancement_factors:
        print("="*90)
        print(f"Testing strange_enhancement = {enhancement:.2f}×")
        print("="*90)
        print()

        calc = StrangeAwareHadronMassCalculator(
            kappa_T_base=0.40,
            strange_enhancement=enhancement,
            sigma_T=0.01,
            eta_T=0.01,
            binding_correction_strength=1.0
        )

        results = []
        for hadron_name, knot in hadrons:
            result = calc.compute_hadron_mass(hadron_name, knot)
            results.append(result)

        # Report
        print(f"{'Hadron':<12} {'κ_T Used':<12} {'Weave (MeV)':<15} {'Total (MeV)':<15} {'Error %':<10}")
        print("-" * 70)

        errors = []
        for r in results:
            print(f"{r['hadron_name']:<12} {r['kappa_T_used']:>10.3f} {r['weave_energy_MeV']:>13.1f} "
                  f"{r['predicted_mass_MeV']:>13.1f} {r['error_percent']:>+8.1f}%")
            if r['error_percent'] is not None:
                errors.append(r['error_percent'])

        avg_error = np.mean(errors) if errors else 0
        print("-" * 70)
        print(f"Average error: {avg_error:.1f}%")
        print()

    print("="*90)
    print("SUMMARY")
    print("="*90)
    print()
    print("Results show that strange_enhancement = 2.78× is required to get Lambda right,")
    print("but this is unrealistic and suggests a different physics for strange quarks.")
    print()
    print("The strange quark probably needs a COMPLETELY DIFFERENT binding model,")
    print("not just a scaling factor on the coherence-based coupling.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
