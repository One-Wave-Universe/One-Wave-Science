"""
Phase 1: Eigenmode Analysis of the One-Wave Update Rule
========================================================

Starting from:
ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) + β(⟨ψⱼⁿ⟩-ψᵢⁿ)

Insert plane wave ansatz for a translationally symmetric lattice:
ψᵢⁿ = A e^{i(k·rᵢ - ω·n·Δt)}

Derive dispersion relation D(k, ω; γ, β) = 0 without external assumptions.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# ============================================================================
# PART 1: DISPERSION RELATION (1D, nearest-neighbor coupling)
# ============================================================================

def dispersion_1d(k, gamma, beta, lattice_spacing=1.0):
    """
    Derive the dispersion relation for 1D lattice.

    For plane wave ψᵢⁿ = A e^{i(k·i·a - ω·n·Δt)}, the update rule becomes:

    λ = 1 + (1-γ)(1 - λ⁻¹) + β(cos(k·a) - 1)

    where λ = e^{-i·ω·Δt}

    Rearranging into quadratic form:
    λ² - C(k)·λ + (1-γ) = 0

    where C(k) = 2 - γ + β(cos(k·a) - 1)

    Returns the two eigenvalues λ₊ and λ₋ as functions of k.
    This gives us ω(k).
    """

    phi = k * lattice_spacing  # phase per lattice site
    C_k = 2 - gamma + beta * (np.cos(phi) - 1)

    discriminant = C_k**2 - 4*(1 - gamma)

    # The two solutions
    lambda_plus = (C_k + np.sqrt(discriminant + 0j)) / 2
    lambda_minus = (C_k - np.sqrt(discriminant + 0j)) / 2

    # Convert λ = e^{-i·ω·Δt} back to ω
    # ω = -i · ln(λ) / Δt
    # We'll use Δt = 1 for simplicity (set time scale)

    omega_plus = 1j * np.log(lambda_plus)
    omega_minus = 1j * np.log(lambda_minus)

    return omega_plus, omega_minus, lambda_plus, lambda_minus, discriminant


# ============================================================================
# PART 2: CANONICAL PARAMETERS (from user's update rule)
# ============================================================================

# The update rule weights are given but we need to establish γ and β values
# that make physical sense. Let's start with a parameter scan.

gamma_values = [0.1, 0.5, 0.9]  # damping coefficient
beta_values = [0.1, 0.5, 1.0, 2.0]  # coupling strength

print("="*80)
print("PHASE 1: EIGENMODE ANALYSIS")
print("="*80)
print()

# Wave vector range (in units of 2π/a, so k ∈ [0, π/a])
k_range = np.linspace(0, np.pi, 100)

for gamma in gamma_values:
    for beta in beta_values:
        print(f"\n{'─'*80}")
        print(f"γ = {gamma}, β = {beta}")
        print(f"{'─'*80}")

        omega_p_list = []
        omega_m_list = []
        lambda_p_list = []
        lambda_m_list = []
        disc_list = []

        for k in k_range:
            omega_p, omega_m, lambda_p, lambda_m, disc = dispersion_1d(k, gamma, beta)
            omega_p_list.append(omega_p)
            omega_m_list.append(omega_m)
            lambda_p_list.append(lambda_p)
            lambda_m_list.append(lambda_m)
            disc_list.append(disc)

        omega_p_list = np.array(omega_p_list)
        omega_m_list = np.array(omega_m_list)

        # Long-wavelength limit (k → 0)
        omega_p_lw, omega_m_lw, _, _, _ = dispersion_1d(0.001, gamma, beta)

        # Short-wavelength limit (k → π)
        omega_p_sw, omega_m_sw, _, _, _ = dispersion_1d(np.pi - 0.001, gamma, beta)

        print(f"Long-wavelength (k→0):")
        print(f"  ω₊ ≈ {omega_p_lw:.6f}")
        print(f"  ω₋ ≈ {omega_m_lw:.6f}")
        print()
        print(f"Short-wavelength (k→π):")
        print(f"  ω₊ ≈ {omega_p_sw:.6f}")
        print(f"  ω₋ ≈ {omega_m_sw:.6f}")
        print()

        # Check stability (|λ| ≤ 1)
        lambda_p_mag = np.abs(lambda_p_list)
        lambda_m_mag = np.abs(lambda_m_list)

        stable_p = np.all(lambda_p_mag <= 1.0 + 1e-10)
        stable_m = np.all(lambda_m_mag <= 1.0 + 1e-10)

        print(f"Stability:")
        print(f"  ω₊ stable: {stable_p} (max |λ| = {np.max(lambda_p_mag):.6f})")
        print(f"  ω₋ stable: {stable_m} (max |λ| = {np.max(lambda_m_mag):.6f})")
        print()

        # Characteristic velocity (group velocity at k → 0)
        # v_g = dω/dk
        dk = 0.01
        omega_p_dk, _, _, _, _ = dispersion_1d(dk, gamma, beta)
        omega_p_0, _, _, _, _ = dispersion_1d(0.001, gamma, beta)
        v_g_p = (omega_p_dk - omega_p_0) / dk

        print(f"Group velocity (k→0):")
        print(f"  v_g₊ ≈ {v_g_p:.6f} (lattice units)")
        print()


# ============================================================================
# PART 3: VISUALIZATION
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Dispersion Relation: ω(k) for One-Wave Update Rule', fontsize=14, fontweight='bold')

test_cases = [
    (0.5, 0.5, axes[0, 0]),
    (0.5, 1.0, axes[0, 1]),
    (0.9, 0.5, axes[1, 0]),
    (0.9, 1.0, axes[1, 1]),
]

k_plot = np.linspace(0, np.pi, 200)

for gamma, beta, ax in test_cases:
    omega_p_plot = []
    omega_m_plot = []

    for k in k_plot:
        omega_p, omega_m, _, _, _ = dispersion_1d(k, gamma, beta)
        omega_p_plot.append(np.real(omega_p))
        omega_m_plot.append(np.real(omega_m))

    ax.plot(k_plot, omega_p_plot, 'r-', label='ω₊ (fast mode)', linewidth=2)
    ax.plot(k_plot, omega_m_plot, 'b-', label='ω₋ (slow mode)', linewidth=2)
    ax.set_xlabel('k (wave vector)', fontsize=11)
    ax.set_ylabel('ω (frequency)', fontsize=11)
    ax.set_title(f'γ={gamma}, β={beta}', fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9)
    ax.axhline(0, color='k', linewidth=0.5)

plt.tight_layout()
plt.savefig('/tmp/claude-0/-home-claude/3b9cfc7f-c329-58d1-9355-8542cf012cd9/scratchpad/dispersion_spectrum.png', dpi=150)
print("\n" + "="*80)
print("DISPERSION PLOTS SAVED")
print("="*80)

# ============================================================================
# PART 4: KEY QUESTIONS PHASE 1 MUST ANSWER
# ============================================================================

print("\n" + "="*80)
print("CRITICAL PHASE 1 QUESTIONS")
print("="*80)
print("""
1. MODE STRUCTURE:
   - Do ω₊ and ω₋ naturally separate into distinct families?
   - Is there a characteristic velocity scale?
   - Do long-wavelength and short-wavelength limits differ physically?

2. DISPERSION PROPERTIES:
   - Is one mode propagating (linear in k) and the other gapped?
   - Or do both disperse?
   - Are there instability regions?

3. STABILITY:
   - For which (γ, β) is the system stable?
   - What constrains these parameters?

4. SYMMETRY:
   - Does radial/rotational character emerge from mode structure?
   - Or must it be added by hand?

5. LATTICE GEOMETRY:
   - Do the modes naturally suggest why 6-fold symmetry might matter?
   - Can we see hints of wrapper topology (−6 to +12)?

These questions determine whether One-Wave generates structure or requires it.
""")

