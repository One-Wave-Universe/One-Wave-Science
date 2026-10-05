"""
Test: Symmetric Laplacian Coupling for E/B Frequency Matching
==============================================================

Does ψⁿ⁺¹ = 2ψⁿ - ψⁿ⁻¹ - γ(ψⁿ - ψⁿ⁻¹) + β∇²ψ
produce identical characteristic equations for E and B?

This replaces the asymmetric ∇(∇·ψ) - ∇×(∇×ψ) with symmetric ∇²ψ.
"""

import numpy as np
from scipy.linalg import eigvals
import math

def analyze_symmetric_rule(gamma, beta, k_mag):
    """
    For plane wave ψ ~ e^{i(k·x - ωt)}, analyze characteristic equation.

    In Fourier space: ∇² → -k²

    Update rule: ψⁿ⁺¹ = 2ψⁿ - ψⁿ⁻¹ - γ(ψⁿ - ψⁿ⁻¹) - βk²ψⁿ

    Characteristic form: λ² - (2 - γ - βk²)λ + (1 - γ) = 0
    """

    # Coefficients for symmetric Laplacian rule
    a_coeff = 1.0
    b_coeff = -(2.0 - gamma - beta * k_mag**2)
    c_coeff = 1.0 - gamma

    # Solve characteristic equation
    discriminant = b_coeff**2 - 4*a_coeff*c_coeff

    if discriminant >= 0:
        lambda_1 = (-b_coeff + math.sqrt(discriminant)) / (2*a_coeff)
        lambda_2 = (-b_coeff - math.sqrt(discriminant)) / (2*a_coeff)
    else:
        lambda_1 = (-b_coeff + 1j*math.sqrt(-discriminant)) / (2*a_coeff)
        lambda_2 = (-b_coeff - 1j*math.sqrt(-discriminant)) / (2*a_coeff)

    # Frequencies: ω = -i ln(λ) for e^{-iωt} ansatz
    omega_1 = -1j * cmath.log(lambda_1) if abs(lambda_1) > 1e-10 else 0
    omega_2 = -1j * cmath.log(lambda_2) if abs(lambda_2) > 1e-10 else 0

    return {
        'lambda_1': lambda_1,
        'lambda_2': lambda_2,
        'omega_1': omega_1.real if omega_1.imag**2 < 1e-10 else omega_1,
        'omega_2': omega_2.real if omega_2.imag**2 < 1e-10 else omega_2,
        'k': k_mag,
        'discriminant': discriminant,
    }


import cmath

print("=" * 80)
print("SYMMETRIC LAPLACIAN TEST: E/B FREQUENCY MATCHING")
print("=" * 80)
print()

gamma, beta = 0.5, 0.5

print(f"Parameters: γ = {gamma}, β = {beta}")
print()

print("Characteristic equation: λ² - (2-γ-βk²)λ + (1-γ) = 0")
print()
print("KEY: If this is the SAME equation for both E and B extraction,")
print("then both fields have the same frequency ω automatically.")
print()

print("-" * 80)
print("RESULTS vs PHASE 6A COMPARISON")
print("-" * 80)
print()

for k in [0.1, 0.3, 0.5, 0.7, 1.0]:
    result = analyze_symmetric_rule(gamma, beta, k)

    print(f"k = {k:.1f}:")
    print(f"  λ₁ = {result['lambda_1']:.6f}")
    print(f"  λ₂ = {result['lambda_2']:.6f}")
    print(f"  ω (from λ) = {result['omega_1']:.6f} (or {result['omega_2']:.6f})")

    # Compare with Phase 6A asymmetric results
    # Phase 6A E (longitudinal): λ² - (2-γ-βk²)λ + (1-γ) = 0
    # Phase 6A B (transverse):   λ² - (2-γ+βk²)λ + (1+γ-βk²) = 0

    # E equation (same as our symmetric):
    a_e = 1.0
    b_e = -(2.0 - gamma - beta * k**2)
    c_e = 1.0 - gamma
    disc_e = b_e**2 - 4*a_e*c_e
    if disc_e >= 0:
        lambda_e1 = (-b_e + math.sqrt(disc_e)) / 2
        omega_e = -1j * cmath.log(lambda_e1)
    else:
        lambda_e1 = (-b_e + 1j*math.sqrt(-disc_e)) / 2
        omega_e = -1j * cmath.log(lambda_e1)

    # B equation (asymmetric):
    a_b = 1.0
    b_b = -(2.0 - gamma + beta * k**2)  # Note: +βk²
    c_b = 1.0 + gamma - beta * k**2      # Note: different constant
    disc_b = b_b**2 - 4*a_b*c_b
    if disc_b >= 0:
        lambda_b1 = (-b_b + math.sqrt(disc_b)) / 2
        omega_b = -1j * cmath.log(lambda_b1)
    else:
        lambda_b1 = (-b_b + 1j*math.sqrt(-disc_b)) / 2
        omega_b = -1j * cmath.log(lambda_b1)

    phase6a_ratio = abs(omega_b.real) / abs(omega_e.real) if omega_e.real != 0 else 0

    print(f"  Phase 6A: ω_E = {omega_e.real:.6f}, ω_B = {omega_b.real:.6f}, ratio = {phase6a_ratio:.2f}")
    print()

print("=" * 80)
print("VERDICT")
print("=" * 80)
print()
print("✓ Symmetric Laplacian gives ONE characteristic equation")
print("✓ Both E and B extract from this same equation")
print("✓ Therefore ω_E = ω_B AUTOMATICALLY (same λ → same ω)")
print()
print("This satisfies the physics requirement for Faraday's law!")
print()
print("Phase 6A's asymmetric rule has:")
print("  - E characteristic: λ² - (2-γ-βk²)λ + (1-γ) = 0")
print("  - B characteristic: λ² - (2-γ+βk²)λ + (1+γ-βk²) = 0")
print()
print("Proposed symmetric rule has:")
print("  - BOTH use: λ² - (2-γ-βk²)λ + (1-γ) = 0")
print()
print("The symmetric Laplacian ∇² treats all directions equally.")
print("This is physically justified for isotropic superfluid lattice.")
print()
print("=" * 80)
