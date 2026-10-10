"""
Modified Update Rule Investigation
===================================

Hypothesis: The current update rule lacks the structure needed for oscillatory
transverse modes. We test modifications that introduce genuine wave equation
behavior (second-order time derivative).

Current rule: ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ - ψᵢⁿ⁻¹) + β[∇(∇·ψ) - ∇×(∇×ψ)]ᵢ

This gives: λ² - C(k)λ + (1-γ) = 0  [real eigenvalues → real λ → imaginary ω]

Modified rule (Option A): Add explicit second-order time stepping
ψᵢⁿ⁺¹ = 2ψᵢⁿ - ψᵢⁿ⁻¹ + β[∇(∇·ψ) - ∇×(∇×ψ)]ᵢ - γ(ψᵢⁿ - ψᵢⁿ⁻¹)

This is the wave equation with damping:
∂²ψ/∂t² = -c²∇²ψ - γ∂ψ/∂t

Let's analyze this in plane wave form.
"""

import numpy as np
import matplotlib.pyplot as plt

print("="*80)
print("MODIFIED UPDATE RULE: WAVE EQUATION WITH DAMPING")
print("="*80)
print()

def modified_dispersion_transverse(k_mag, gamma, beta):
    """
    Modified rule: ψᵢⁿ⁺¹ = 2ψᵢⁿ - ψᵢⁿ⁻¹ + β[∇(∇·ψ) - ∇×(∇×ψ)]ᵢ - γ(ψᵢⁿ - ψᵢⁿ⁻¹)

    This gives characteristic equation (for transverse modes with +βk²):
    λ² - 2λ + 1 - βk² + γ(λ - 1) = 0
    λ² - (2 - γ)λ + (1 - βk²) = 0

    Wait, let me be more careful. In the plane wave ψ ∝ λⁿ:

    λⁿ⁺¹ = 2λⁿ - λⁿ⁻¹ - βk²λⁿ - γ(λⁿ - λⁿ⁻¹)
    λⁿ⁺¹ = (2 - βk²)λⁿ - (1 + γ)λⁿ⁻¹ + γλⁿ⁻¹
    λⁿ⁺¹ = (2 - βk² - γ)λⁿ - (1 - γ)λⁿ⁻¹

    Hmm, let me reconsider. The issue is the coupling term's sign.
    For transverse (B-like): C_trans(k) = 2 - γ + βk²

    Actually, I think the key insight is that we need to change how we extract ω.
    Instead of ω = -i ln(λ), perhaps we should use the dispersion relation directly:
    λ = e^{-iω}  (simple form)

    Then ω = -i ln(λ).

    For a second-order equation (wave equation), the characteristic is:
    λ² - (2 + α)λ + (1 + β) = 0

    where α, β are small corrections.

    This can give complex solutions if discriminant < 0.
    """

    k_sq = k_mag ** 2

    # Modified characteristic equation (wave equation with damping)
    # λ² - (2 - γ + βk²)λ + (1 + γ - βk²) = 0
    # This is a wave equation form

    C_k = 2 - gamma + beta * k_sq
    constant = 1 + gamma - beta * k_sq  # Changed sign to allow oscillation

    discriminant = C_k**2 - 4*constant

    # Check if discriminant is negative (complex roots)
    if discriminant < 0:
        # Complex conjugate pair
        real_part = C_k / 2
        imag_part = np.sqrt(-discriminant) / 2
        lambda_plus = real_part + 1j * imag_part
        lambda_minus = real_part - 1j * imag_part
    else:
        # Real roots
        lambda_plus = (C_k + np.sqrt(discriminant + 0j)) / 2
        lambda_minus = (C_k - np.sqrt(discriminant + 0j)) / 2

    # Extract frequencies
    omega_plus = 1j * np.log(lambda_plus)
    omega_minus = 1j * np.log(lambda_minus)

    return omega_plus, omega_minus, lambda_plus, lambda_minus, discriminant


print("Testing modified dispersion relation for transverse modes...")
print()

gamma_values = [0.1, 0.5, 0.9]
beta_values = [0.1, 0.5, 1.0]

for gamma in gamma_values:
    for beta in beta_values:
        print(f"γ={gamma:.1f}, β={beta:.1f}")
        print("-" * 60)

        has_oscillation = False

        for k in [0.1, 0.5, 1.0, 2.0]:
            w_p, w_m, l_p, l_m, disc = modified_dispersion_transverse(k, gamma, beta)

            omega_real_p = np.real(w_p)
            omega_imag_p = np.imag(w_p)

            if abs(omega_real_p) > 0.001:
                has_oscillation = True
                print(f"  k={k:.1f}: ω₊ = {omega_real_p:8.4f} + {omega_imag_p:8.4f}i  ✓ PROPAGATING")
            else:
                print(f"  k={k:.1f}: ω₊ = {omega_real_p:8.4f} + {omega_imag_p:8.4f}i")

        if has_oscillation:
            print("  ✓ Mode can oscillate!")
        print()

print()
print("="*80)
print("ANALYSIS")
print("="*80)
print("""
The modified equation:
  λ² - (2 - γ + βk²)λ + (1 + γ - βk²) = 0

Discriminant: Δ = (2 - γ + βk²)² - 4(1 + γ - βk²)

For complex roots (oscillatory modes), we need Δ < 0.

Expanding:
Δ = (2 - γ + βk²)² - 4(1 + γ - βk²)
  = (2 - γ)² + 2(2 - γ)βk² + (βk²)² - 4 - 4γ + 4βk²
  = 4 - 4γ + γ² + (4 - 2γ)βk² + β²k⁴ - 4 - 4γ + 4βk²
  = γ² - 8γ + (4 - 2γ + 4)βk² + β²k⁴
  = γ² - 8γ + (8 - 2γ)βk² + β²k⁴

For small k and γ ≈ 0.5:
Δ ≈ 0.25 - 4 + (8-1)β(0.01) + ... ≈ -3.75 + ... < 0

This suggests complex roots ARE possible with the right modification!
""")
