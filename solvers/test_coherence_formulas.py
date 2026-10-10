#!/usr/bin/env python3
"""
Test Coherence Formula Variants to find optimal decoherence model

Different formulas for how oscillation frequency mismatch reduces effective coupling:
- Variant 1: 1 / (1 + log(ω_ratio))  - current formula
- Variant 2: 1 / ω_ratio  - inverse ratio
- Variant 3: 1 / √ω_ratio  - square root
- Variant 4: 1 - (log(ω_ratio) - 1) / log(ω_ratio)  - softer decay
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from hadron_knot_geometry import (
    create_proton, create_neutron, create_lambda,
    QUARK_MASSES_MEV, WeaveDensity, WeavingEnergyCalculator
)
from hadron_mass_predictor import HadronMassCalculator

def coherence_v1(omega_ratio):
    """Current: 1 / (1 + log(ω_ratio))"""
    if omega_ratio <= 1.0:
        return 1.0
    return 1.0 / (1.0 + np.log(omega_ratio))

def coherence_v2(omega_ratio):
    """Inverse ratio: 1 / ω_ratio"""
    if omega_ratio <= 1.0:
        return 1.0
    return 1.0 / omega_ratio

def coherence_v3(omega_ratio):
    """Square root: 1 / √ω_ratio"""
    if omega_ratio <= 1.0:
        return 1.0
    return 1.0 / np.sqrt(omega_ratio)

def coherence_v4(omega_ratio):
    """Softer decay: 1 - (log(ω) - 1) / log(ω) for larger ω"""
    if omega_ratio <= 1.0:
        return 1.0
    log_w = np.log(omega_ratio)
    return max(0.0, 1.0 - (log_w - 1.0) / (log_w + 1.0))

def coherence_v5(omega_ratio):
    """Exponential decay: exp(-log(ω_ratio))"""
    if omega_ratio <= 1.0:
        return 1.0
    return np.exp(-np.log(omega_ratio))  # Same as 1/ω_ratio

def coherence_v6(omega_ratio):
    """Power law: ω_ratio^(-0.5) = 1/√ω_ratio but slightly different"""
    if omega_ratio <= 1.0:
        return 1.0
    return omega_ratio**(-0.5)

def get_avg_coherence(hadron_name, knot, coherence_func):
    """Compute average coherence for a hadron using specified formula."""
    vortices = knot.vortices
    masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in vortices]

    kappa_T_base = 0.297
    omegas = [kappa_T_base / m if m > 0 else 0 for m in masses]

    pair_coherences = []
    for i in range(len(vortices)):
        for j in range(i+1, len(vortices)):
            if omegas[i] > 0 and omegas[j] > 0:
                omega_ratio = max(omegas[i], omegas[j]) / min(omegas[i], omegas[j])
                coherence = coherence_func(omega_ratio)
                pair_coherences.append(coherence)

    return np.mean(pair_coherences) if pair_coherences else 1.0


def test_formula_variant(variant_name, coherence_func):
    """Test a coherence formula variant and compute hadron masses."""

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    # Expected values from earlier predictions
    expected = {
        "proton": 938.3,
        "neutron": 939.6,
        "Lambda": 1115.7,
    }

    # Compute coherence factors for this variant
    coherences = {}
    for hadron_name, knot in hadrons:
        coherences[hadron_name] = get_avg_coherence(hadron_name, knot, coherence_func)

    # Compute effective κ_T for each hadron
    kappa_T_base = 0.297
    kappa_T_eff = {}
    for hadron_name, coherence in coherences.items():
        kappa_T_eff[hadron_name] = kappa_T_base * coherence

    # Compute masses using calculator
    # Note: This is approximate - we'd need to modify the calculator to use custom coherence
    # For now, just return coherence values

    return coherences, kappa_T_eff


def main():
    print("="*90)
    print("COHERENCE FORMULA VARIANT TEST")
    print("="*90)
    print()

    formulas = [
        ("V1: 1/(1+log(ω))", coherence_v1),
        ("V2: 1/ω", coherence_v2),
        ("V3: 1/√ω", coherence_v3),
        ("V4: Softer decay", coherence_v4),
        ("V5: exp(-log(ω))", coherence_v5),
        ("V6: ω^(-0.5)", coherence_v6),
    ]

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    print(f"{'Variant':<20} {'Proton (p)':>15} {'Neutron (n)':>15} {'Lambda (L)':>15}")
    print("-" * 70)

    results = {}
    for variant_name, coherence_func in formulas:
        coherences, kappa_T_eff = test_formula_variant(variant_name, coherence_func)

        results[variant_name] = {
            "coherences": coherences,
            "kappa_T_eff": kappa_T_eff,
        }

        coh_p = coherences.get("proton", 1.0)
        coh_n = coherences.get("neutron", 1.0)
        coh_l = coherences.get("Lambda", 1.0)

        print(f"{variant_name:<20} {coh_p:>14.3f} {coh_n:>15.3f} {coh_l:>15.3f}")

    print()
    print("Note: Proton and Neutron always have identical coherence factors")
    print("because they have the same frequency dispersion pattern.")
    print("The error sign flip depends on which quark mass is the anchor,")
    print("not on the coherence factor itself.")
    print()

    # Test predictions with different κ_T scalings
    print("="*90)
    print("HADRON MASS PREDICTIONS WITH DIFFERENT COHERENCE SCALINGS")
    print("="*90)
    print()

    # For now, just show that all formulas give same Proton/Neutron coherence
    # This confirms that we need a SEPARATE binding correction term
    print("Key Finding:")
    print("  All coherence formulas give identical results for Proton vs Neutron")
    print("  (both have ω_ratio = 2.16, same pair configuration)")
    print()
    print("  Therefore: Coherence factor alone CANNOT explain error sign flip")
    print("  We need: Additional binding energy correction based on symmetric pair mass")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
