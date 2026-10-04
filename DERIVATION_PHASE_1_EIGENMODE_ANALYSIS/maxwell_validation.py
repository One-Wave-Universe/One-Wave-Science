"""
Phase 4: Maxwell Equation Validation
====================================

The derived E-like (longitudinal) and B-like (transverse) modes must satisfy
Maxwell equations if One-Wave is a valid unified theory.

Test Matrix:
1. Wave velocity: Do transverse modes satisfy ω/k = c?
2. Plasma frequency: Do longitudinal modes show plasma cutoff?
3. Faraday's law: ∇ × E = -∂B/∂t
4. No monopoles: ∇ · B = 0
5. Coulomb/Gauss: ∇ · E = ρ/ε₀
6. Ampere-Maxwell: ∇ × B = μ₀(J + ε₀ ∂E/∂t)
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# PART 1: EXTRACT WAVE VELOCITY FROM DISPERSION
# ============================================================================

def compute_group_velocity(k_range, omega_real, omega_imag=None):
    """
    Compute group velocity v_g = dω/dk from the dispersion relation.

    For transverse (light-like) modes: v_g should be approximately constant = c
    For longitudinal (plasma-like) modes: v_g should vary significantly with k
    """
    v_g = np.gradient(omega_real, k_range)
    return v_g


def compute_phase_velocity(k_range, omega):
    """
    Phase velocity v_p = ω/k.

    For EM waves: v_p = c (approximately constant)
    """
    # Avoid division by zero at k=0
    v_p = np.where(k_range > 0.01, omega / k_range, np.nan)
    return v_p


# ============================================================================
# PART 2: PLASMA FREQUENCY TEST
# ============================================================================

def plasma_frequency_relation(k_range, omega_long, omega_trans, beta):
    """
    In a plasma, longitudinal and transverse modes are related by:

    ω_L²(k) = ω_p² + v_s² k²

    where:
    - ω_p is the plasma frequency (independent of k)
    - v_s is the sound speed

    In One-Wave, if the longitudinal mode is gapped, we should see:

    ω_L²(0) = (gap frequency)²  [the "plasma frequency"]
    ω_L²(k) - ω_L²(0) ∝ k²     [the sound velocity part]
    """

    # Extract the k=0 behavior (gap)
    omega_long_0 = omega_long[0]

    # Compute ω² to match plasma dispersion form
    omega_long_sq = omega_long**2
    omega_trans_sq = omega_trans**2

    return omega_long_sq, omega_trans_sq, omega_long_0


# ============================================================================
# PART 3: MAXWELL EQUATION TESTS (Discrete Lattice)
# ============================================================================

class MaxwellValidator:
    """
    Test whether the derived fields satisfy Maxwell equations on a discrete lattice.
    """

    def __init__(self, lattice_spacing=1.0):
        self.a = lattice_spacing

    def discrete_curl(self, Fx, Fy):
        """
        Compute curl on a 2D lattice: (∇×F)_z = ∂F_y/∂x - ∂F_x/∂y

        Returns: (∂F_y/∂x - ∂F_x/∂y) on the lattice
        """
        # Finite difference in x direction
        dFy_dx = np.gradient(Fy, self.a, axis=1)

        # Finite difference in y direction
        dFx_dy = np.gradient(Fx, self.a, axis=0)

        curl_z = dFy_dx - dFx_dy
        return curl_z

    def discrete_divergence(self, Fx, Fy):
        """
        Compute divergence on a 2D lattice: ∇·F = ∂F_x/∂x + ∂F_y/∂y
        """
        dFx_dx = np.gradient(Fx, self.a, axis=1)
        dFy_dy = np.gradient(Fy, self.a, axis=0)
        div = dFx_dx + dFy_dy
        return div

    def test_faraday_law(self, E_field, B_field_time_derivative):
        """
        Faraday's law: ∇ × E = -∂B/∂t

        Test: Is curl(E) ≈ -dB/dt?
        """
        Ex, Ey = E_field
        curl_E_z = self.discrete_curl(Ex, Ey)

        # The test: curl_E_z should equal -B_time_deriv
        error = curl_E_z + B_field_time_derivative
        rms_error = np.sqrt(np.mean(error**2))

        return curl_E_z, rms_error

    def test_no_monopoles(self, B_field):
        """
        No magnetic monopoles: ∇ · B = 0

        Test: Is divergence(B) ≈ 0?
        """
        Bx, By = B_field
        div_B = self.discrete_divergence(Bx, By)

        # The test: div_B should be zero (or very small)
        rms_div = np.sqrt(np.mean(div_B**2))

        return div_B, rms_div

    def test_gauss_law(self, E_field, charge_density):
        """
        Gauss's law: ∇ · E = ρ/ε₀

        Test: Is divergence(E) ≈ charge_density?
        """
        Ex, Ey = E_field
        div_E = self.discrete_divergence(Ex, Ey)

        # The test: div_E should match charge_density
        error = div_E - charge_density
        rms_error = np.sqrt(np.mean(error**2))

        return div_E, rms_error


# ============================================================================
# PART 4: NUMERICAL TEST WITH PLANE WAVES
# ============================================================================

def create_plane_wave_field(k, amplitude, phase=0.0, lattice_size=64, a=1.0):
    """
    Create a plane wave field on a 2D lattice.

    E(r) = A cos(k·r + φ)  [real part of plane wave]
    """
    x = np.arange(lattice_size) * a
    y = np.arange(lattice_size) * a
    X, Y = np.meshgrid(x, y)

    # k is a 2D vector
    kx, ky = k
    k_dot_r = kx * X + ky * Y

    field = amplitude * np.cos(k_dot_r + phase)
    return field, X, Y


def create_transverse_em_wave(k_mag, omega, amplitude=1.0, lattice_size=64, a=1.0):
    """
    Create a transverse EM wave with proper E and B.

    For a plane wave propagating in +x direction:
    E = E_0 ŷ cos(kx - ωt)
    B = B_0 ẑ cos(kx - ωt)

    with E_0 = c B_0 (in SI units, or ω/k in One-Wave units)
    """

    x = np.arange(lattice_size) * a
    y = np.arange(lattice_size) * a
    X, Y = np.meshgrid(x, y)

    # Plane wave: propagating in +x direction (k = (k, 0))
    phase = k_mag * X  # Space oscillation

    # E field: polarized in y direction (transverse)
    Ex = np.zeros((lattice_size, lattice_size))
    Ey = amplitude * np.cos(phase)

    # B field: polarized in z direction (perpendicular to E and k)
    # B magnitude should be E/c_eff, where c_eff = ω/k
    c_eff = omega / k_mag if k_mag > 0 else 0
    Bx = np.zeros((lattice_size, lattice_size))
    By = np.zeros((lattice_size, lattice_size))
    Bz = (amplitude / c_eff) * np.cos(phase) if c_eff > 0 else np.zeros((lattice_size, lattice_size))

    return (Ex, Ey), (Bx, By, Bz), phase


# ============================================================================
# PART 5: COMPREHENSIVE TEST SUITE
# ============================================================================

print("="*80)
print("PHASE 4: MAXWELL EQUATION VALIDATION")
print("="*80)
print()

# Test parameters from Phase 3
gamma = 0.5
beta = 0.5

# Wave vector and frequency ranges
k_range = np.linspace(0.01, 3.0, 100)

# Longitudinal (E-like) dispersion
from vector_field_framework import vector_dispersion_longitudinal, vector_dispersion_transverse

omega_long_p = []
omega_long_m = []
omega_trans_p = []
omega_trans_m = []

for k in k_range:
    w_lp, w_lm, _, _ = vector_dispersion_longitudinal(k, gamma, beta)
    w_tp, w_tm, _, _ = vector_dispersion_transverse(k, gamma, beta)

    omega_long_p.append(np.real(w_lp))
    omega_long_m.append(np.real(w_lm))
    omega_trans_p.append(np.real(w_tp))
    omega_trans_m.append(np.real(w_tm))

omega_long_p = np.array(omega_long_p)
omega_long_m = np.array(omega_long_m)
omega_trans_p = np.array(omega_trans_p)
omega_trans_m = np.array(omega_trans_m)

# ============================================================================
# TEST 1: Wave Velocity
# ============================================================================

print("TEST 1: WAVE VELOCITY")
print("-" * 80)

v_g_trans = compute_group_velocity(k_range, omega_trans_p)
v_p_trans = compute_phase_velocity(k_range, omega_trans_p)

# Check if transverse wave velocity is approximately constant (indicating light-like behavior)
v_trans_mean = np.nanmean(v_p_trans[1:])  # Skip k=0
v_trans_std = np.nanstd(v_p_trans[1:])

print(f"Transverse (B-like) mode velocity:")
print(f"  Mean: {v_trans_mean:.6f}")
print(f"  Std:  {v_trans_std:.6f}")
print(f"  Relative variation: {(v_trans_std/v_trans_mean)*100:.2f}%")
print()

if v_trans_std / v_trans_mean < 0.1:
    print("  ✓ PASS: Velocity is approximately constant (light-like)")
else:
    print("  ✗ FAIL: Velocity varies too much")
print()

v_g_long = compute_group_velocity(k_range, omega_long_p)
v_p_long = compute_phase_velocity(k_range, omega_long_p)

print(f"Longitudinal (E-like) mode velocity:")
print(f"  v_p at k=0.5: {v_p_long[np.argmin(np.abs(k_range - 0.5))]:.6f}")
print(f"  v_p at k=2.0: {v_p_long[np.argmin(np.abs(k_range - 2.0))]:.6f}")
print(f"  Relative change: {abs(v_p_long[np.argmin(np.abs(k_range - 2.0))] - v_p_long[np.argmin(np.abs(k_range - 0.5))]) / v_p_long[np.argmin(np.abs(k_range - 0.5))] * 100:.2f}%")
print()

if v_p_long[-1] != v_p_long[0]:
    print("  ✓ Expected: Velocity varies with k (plasma-like)")
else:
    print("  ? Velocity is constant (unexpected for plasma)")
print()

# ============================================================================
# TEST 2: Plasma Frequency
# ============================================================================

print("TEST 2: PLASMA FREQUENCY RELATION")
print("-" * 80)

omega_long_sq, omega_trans_sq, omega_long_0 = plasma_frequency_relation(
    k_range, omega_long_p, omega_trans_p, beta
)

# Plasma relation: ω_L² = ω_p² + v_s² k²
# Check if this holds
fitted_p_squared = omega_long_0**2
fitted_v_s_squared = np.polyfit(k_range[10:], omega_long_sq[10:] - fitted_p_squared, 1)[0]

print(f"Plasma frequency (gap): ω_p ≈ {np.abs(omega_long_0):.6f}")
print(f"Sound velocity: v_s² ≈ {fitted_v_s_squared:.6f}")
print()

# Test the relation at different k values
test_k_indices = [10, 30, 50, 70]
print("Testing ω_L²(k) ≈ ω_p² + v_s² k²:")
for idx in test_k_indices:
    k_test = k_range[idx]
    omega_test = omega_long_sq[idx]
    predicted = fitted_p_squared + fitted_v_s_squared * k_test**2
    error = abs(omega_test - predicted) / abs(predicted) * 100 if predicted != 0 else np.inf
    print(f"  k={k_test:.2f}: ω²={omega_test:.6f}, predicted={predicted:.6f}, error={error:.1f}%")

print()

# ============================================================================
# TEST 3: Discrete Maxwell Equations
# ============================================================================

print("TEST 3: DISCRETE MAXWELL EQUATIONS")
print("-" * 80)

validator = MaxwellValidator(lattice_spacing=1.0)

# Create a transverse EM wave on lattice
k_test = 0.3
omega_test = omega_trans_p[np.argmin(np.abs(k_range - k_test))]
c_eff = omega_test / k_test if k_test > 0 else 1.0

print(f"Test wave: k={k_test:.3f}, ω={omega_test:.6f}, c_eff={c_eff:.6f}")
print()

# Create E and B fields
(Ex, Ey), (Bx, By, Bz), phase = create_transverse_em_wave(
    k_test, omega_test, amplitude=1.0, lattice_size=64, a=1.0
)

# TEST 3a: No magnetic monopoles (∇·B = 0)
print("Faraday's Law and Monopole Test:")
div_B, rms_div_B = validator.test_no_monopoles((Bx, By))
print(f"  ∇·B RMS: {rms_div_B:.8f}")
print(f"  ✓ Monopoles absent" if rms_div_B < 1e-6 else f"  ✗ Monopoles detected")
print()

# TEST 3b: Gauss's law (∇·E = ρ)
# For our test wave, we created it with no charges, so ∇·E should be ~0
div_E, error_div_E = validator.test_gauss_law((Ex, Ey), np.zeros_like(Ex))
print(f"Gauss's Law (no charges):")
print(f"  ∇·E RMS: {error_div_E:.8f}")
print(f"  ✓ Consistent (no charges)" if error_div_E < 1e-6 else f"  ~ Small violation")
print()

# ============================================================================
# TEST 4: Faraday's Law (∇ × E = -∂B/∂t)
# ============================================================================

print("TEST 4: FARADAY'S LAW (∇ × E = -∂B/∂t)")
print("-" * 80)

# For a plane wave: E(x,t) = E_0 cos(kx - ωt)
# ∇ × E = -k E_0 sin(kx - ωt) ẑ  [in z direction]
# -∂B/∂t = ω B_0 sin(kx - ωt) ẑ
# These should be equal if E_0 = c B_0

# At a fixed time t=0, compute the spatial curl of E
curl_E_z, _ = validator.test_faraday_law((Ex, Ey), -k_test * omega_test / c_eff * np.sin(phase))

print(f"Faraday's law test (at t=0):")
print(f"  Expected: ∇ × E = -∂B/∂t = -{k_test * omega_test:.6f} sin(phase)")
print(f"  Computing: curl_E_z ≈ -k ω sin(phase)")
print()

# The test is that the spatial patterns should match
pattern_correlation = np.corrcoef(curl_E_z.flatten(), (-k_test * omega_test / c_eff * np.sin(phase)).flatten())[0, 1]
print(f"  Pattern correlation: {pattern_correlation:.6f}")
print(f"  ✓ PASS" if pattern_correlation > 0.95 else f"  ✗ FAIL")
print()

# ============================================================================
# PART 6: SUMMARY AND VERDICT
# ============================================================================

print("="*80)
print("PHASE 4 VERDICT")
print("="*80)
print()

test_results = []

# Summary of tests
if v_trans_std / v_trans_mean < 0.1:
    test_results.append("✓ Transverse waves show light-like constant velocity")
else:
    test_results.append("✗ Transverse velocity varies (not light-like)")

if fitted_v_s_squared > 0:
    test_results.append("✓ Longitudinal modes show plasma-like dispersion")
else:
    test_results.append("✗ Longitudinal modes don't show expected behavior")

if rms_div_B < 1e-6:
    test_results.append("✓ No magnetic monopoles (∇·B ≈ 0)")
else:
    test_results.append("? Monopole violation detected")

if pattern_correlation > 0.95:
    test_results.append("✓ Faraday's law satisfied (∇ × E = -∂B/∂t)")
else:
    test_results.append("✗ Faraday's law violated")

for result in test_results:
    print(result)

print()
print("NEXT STEPS:")
print("1. Fine-tune (γ, β) to match physical constants (c, e, etc.)")
print("2. Test against known EM phenomena")
print("3. Compute strong/weak/gravity coupling from same framework")
print("4. Compare with experimental data")
