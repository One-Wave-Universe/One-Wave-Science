"""
Phase 2 Preparation: 2D Dispersion Relation on Hexagonal Lattice
==================================================================

The hexagonal lattice has 6 nearest neighbors in plane + coupling to upper/lower layers.

Goal: Derive ω(k_x, k_y) and look for radial vs rotational mode separation.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================================================
# PART 1: HEXAGONAL LATTICE GEOMETRY
# ============================================================================

def hex_neighbors_2d():
    """
    In a hexagonal lattice with lattice spacing a=1:

    Each vertex has 6 neighbors in the plane, at angles 0°, 60°, 120°, 180°, 240°, 300°.

    In Cartesian coordinates (x, y):
    - If vertex is at origin
    - Neighbors are at:
      * (1, 0)           [0°]
      * (1/2, √3/2)      [60°]
      * (-1/2, √3/2)     [120°]
      * (-1, 0)          [180°]
      * (-1/2, -√3/2)    [240°]
      * (1/2, -√3/2)     [300°]
    """
    sqrt3 = np.sqrt(3)
    neighbors = np.array([
        [1, 0],
        [0.5, sqrt3/2],
        [-0.5, sqrt3/2],
        [-1, 0],
        [-0.5, -sqrt3/2],
        [0.5, -sqrt3/2],
    ])
    return neighbors

def dispersion_2d_hex(kx, ky, gamma, beta, a=1.0):
    """
    Compute the 2D hexagonal lattice dispersion relation.

    On a hexagonal lattice, the update rule becomes:
    ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) + (β/6) Σⱼ(ψⱼⁿ - ψᵢⁿ)

    where the sum is over 6 nearest neighbors in the plane.

    For plane wave ψ(r,t) = A e^{i(k·r - ωt)}:

    The neighbor sum becomes:
    Σⱼ e^{i k·Δrⱼ} where Δrⱼ are the 6 neighbor displacements

    For hexagonal: Σⱼ e^{i k·Δrⱼ} = 2[cos(kx*a) + cos((kx/2 - √3*ky/2)*a) + cos((kx/2 + √3*ky/2)*a)]

    This simplifies for a=1:
    Σ = 2[cos(kx) + cos(kx/2 - √3*ky/2) + cos(kx/2 + √3*ky/2)]
    """

    sqrt3 = np.sqrt(3)

    # Hexagonal lattice structure factor
    term1 = np.cos(kx * a)
    term2 = np.cos((kx/2 - sqrt3*ky/2) * a)
    term3 = np.cos((kx/2 + sqrt3*ky/2) * a)

    S_hex = 2 * (term1 + term2 + term3)  # neighbor sum

    # The dispersion relation quadratic (same form as 1D):
    # λ² - C(k)·λ + (1-γ) = 0
    # where C(k) = 2 - γ + (β/6) * S_hex * (for 6 neighbors)

    # Accounting for averaging over 6 neighbors:
    C_k = 2 - gamma + (beta/6) * S_hex

    discriminant = C_k**2 - 4*(1 - gamma)

    # Two eigenvalues
    lambda_plus = (C_k + np.sqrt(discriminant + 0j)) / 2
    lambda_minus = (C_k - np.sqrt(discriminant + 0j)) / 2

    # Convert to frequency (Δt = 1)
    omega_plus = -1j * np.log(lambda_plus)
    omega_minus = -1j * np.log(lambda_minus)

    return omega_plus, omega_minus, S_hex

# ============================================================================
# PART 2: 2D DISPERSION SURFACE
# ============================================================================

gamma = 0.5
beta = 0.8

print("="*80)
print("PHASE 2: 2D HEXAGONAL LATTICE DISPERSION")
print("="*80)
print(f"\nParameters: γ = {gamma}, β = {beta}")
print()

# Create 2D k-space grid
kx_range = np.linspace(-np.pi, np.pi, 50)
ky_range = np.linspace(-np.pi, np.pi, 50)
KX, KY = np.meshgrid(kx_range, ky_range)

# Compute dispersion surfaces
Omega_plus_real = np.zeros_like(KX, dtype=float)
Omega_plus_imag = np.zeros_like(KX, dtype=float)
Omega_minus_real = np.zeros_like(KX, dtype=float)
Omega_minus_imag = np.zeros_like(KX, dtype=float)

for i in range(len(kx_range)):
    for j in range(len(ky_range)):
        omega_p, omega_m, _ = dispersion_2d_hex(KX[j,i], KY[j,i], gamma, beta)
        Omega_plus_real[j,i] = np.real(omega_p)
        Omega_plus_imag[j,i] = np.imag(omega_p)
        Omega_minus_real[j,i] = np.real(omega_m)
        Omega_minus_imag[j,i] = np.imag(omega_m)

# Plot dispersion surfaces
fig = plt.figure(figsize=(16, 12))

# ω₊ real part
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
surf1 = ax1.plot_surface(KX, KY, Omega_plus_real, cmap='RdBu', alpha=0.9)
ax1.set_xlabel('kx')
ax1.set_ylabel('ky')
ax1.set_zlabel('Re(ω₊)')
ax1.set_title('Fast Mode: Real Part', fontweight='bold')
fig.colorbar(surf1, ax=ax1, pad=0.1, shrink=0.8)

# ω₊ imaginary part
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
surf2 = ax2.plot_surface(KX, KY, Omega_plus_imag, cmap='Spectral', alpha=0.9)
ax2.set_xlabel('kx')
ax2.set_ylabel('ky')
ax2.set_zlabel('Im(ω₊)')
ax2.set_title('Fast Mode: Imaginary Part (Damping)', fontweight='bold')
fig.colorbar(surf2, ax=ax2, pad=0.1, shrink=0.8)

# ω₋ real part
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
surf3 = ax3.plot_surface(KX, KY, Omega_minus_real, cmap='RdBu', alpha=0.9)
ax3.set_xlabel('kx')
ax3.set_ylabel('ky')
ax3.set_zlabel('Re(ω₋)')
ax3.set_title('Slow Mode: Real Part', fontweight='bold')
fig.colorbar(surf3, ax=ax3, pad=0.1, shrink=0.8)

# ω₋ imaginary part
ax4 = fig.add_subplot(2, 2, 4, projection='3d')
surf4 = ax4.plot_surface(KX, KY, Omega_minus_imag, cmap='Spectral', alpha=0.9)
ax4.set_xlabel('kx')
ax4.set_ylabel('ky')
ax4.set_zlabel('Im(ω₋)')
ax4.set_title('Slow Mode: Imaginary Part (Damping)', fontweight='bold')
fig.colorbar(surf4, ax=ax4, pad=0.1, shrink=0.8)

plt.tight_layout()
plt.savefig('/tmp/claude-0/-home-claude/3b9cfc7f-c329-58d1-9355-8542cf012cd9/scratchpad/dispersion_2d_hex.png', dpi=120)
print("2D dispersion surfaces saved.")

# ============================================================================
# PART 3: CONTOUR PLOTS (Easier to Read)
# ============================================================================

fig2, axes = plt.subplots(2, 2, figsize=(14, 12))

# ω₊ real
c1 = axes[0, 0].contourf(KX, KY, Omega_plus_real, levels=20, cmap='RdBu')
axes[0, 0].contour(KX, KY, Omega_plus_real, levels=10, colors='k', alpha=0.3, linewidths=0.5)
axes[0, 0].set_xlabel('kx')
axes[0, 0].set_ylabel('ky')
axes[0, 0].set_title('Re(ω₊): Propagation', fontweight='bold')
plt.colorbar(c1, ax=axes[0, 0])

# ω₊ imag
c2 = axes[0, 1].contourf(KX, KY, Omega_plus_imag, levels=20, cmap='Spectral')
axes[0, 1].contour(KX, KY, Omega_plus_imag, levels=10, colors='k', alpha=0.3, linewidths=0.5)
axes[0, 1].set_xlabel('kx')
axes[0, 1].set_ylabel('ky')
axes[0, 1].set_title('Im(ω₊): Decay Rate', fontweight='bold')
plt.colorbar(c2, ax=axes[0, 1])

# ω₋ real
c3 = axes[1, 0].contourf(KX, KY, Omega_minus_real, levels=20, cmap='RdBu')
axes[1, 0].contour(KX, KY, Omega_minus_real, levels=10, colors='k', alpha=0.3, linewidths=0.5)
axes[1, 0].set_xlabel('kx')
axes[1, 0].set_ylabel('ky')
axes[1, 0].set_title('Re(ω₋): Propagation', fontweight='bold')
plt.colorbar(c3, ax=axes[1, 0])

# ω₋ imag
c4 = axes[1, 1].contourf(KX, KY, Omega_minus_imag, levels=20, cmap='Spectral')
axes[1, 1].contour(KX, KY, Omega_minus_imag, levels=10, colors='k', alpha=0.3, linewidths=0.5)
axes[1, 1].set_xlabel('kx')
axes[1, 1].set_ylabel('ky')
axes[1, 1].set_title('Im(ω₋): Decay Rate', fontweight='bold')
plt.colorbar(c4, ax=axes[1, 1])

plt.tight_layout()
plt.savefig('/tmp/claude-0/-home-claude/3b9cfc7f-c329-58d1-9355-8542cf012cd9/scratchpad/dispersion_2d_contours.png', dpi=120)
print("2D contour plots saved.")

# ============================================================================
# PART 4: RADIAL VS ROTATIONAL ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("SYMMETRY ANALYSIS: Looking for Radial/Rotational Structure")
print("="*80)
print()

# Sample specific k-vectors and compute gradients
test_k_vectors = [
    (0.5, 0.0, "x-direction"),
    (0.5, 0.5, "diagonal"),
    (0.0, 0.5, "y-direction"),
]

for kx, ky, label in test_k_vectors:
    omega_p, omega_m, S_hex = dispersion_2d_hex(kx, ky, gamma, beta)

    print(f"\nWave vector: k = ({kx}, {ky}) [{label}]")
    print(f"  Hex structure factor: S = {S_hex:.4f}")
    print(f"  ω₊ = {omega_p:.6f}")
    print(f"  ω₋ = {omega_m:.6f}")

    # Compute numerical gradients of ω to see if there's directionality
    dk = 0.01
    omega_p_dx, _, _ = dispersion_2d_hex(kx + dk, ky, gamma, beta)
    omega_p_dy, _, _ = dispersion_2d_hex(kx, ky + dk, gamma, beta)

    grad_omega_p_x = (omega_p_dx - omega_p) / dk
    grad_omega_p_y = (omega_p_dy - omega_p) / dk

    print(f"  Group velocity (∇ω): ({grad_omega_p_x:.4f}, {grad_omega_p_y:.4f})")

# ============================================================================
# PART 5: QUESTIONS FOR PHASE 2
# ============================================================================

print("\n" + "="*80)
print("PHASE 2 CRITICAL QUESTIONS")
print("="*80)
print("""
1. RADIAL/ROTATIONAL DECOMPOSITION:
   - Does one mode have ∂ψ/∂r structure (divergence)?
   - Does the other have ∇×ψ structure (curl)?
   - Or are they both mixed?

2. SYMMETRY:
   - Do the modes respect hexagonal symmetry (k→k+2π/3)?
   - Or do they break it?

3. WRAPPER TOPOLOGY:
   - From the 2D modes, can we derive why k-space ranges as (−π to +π)?
   - Does stacking modes explain the −6/+12 asymmetry?

4. VELOCITY ANISOTROPY:
   - Is group velocity isotropic (same in all directions)?
   - Or does hexagonal geometry produce anisotropy?

5. DECAY:
   - Do decay rates differ by mode?
   - By direction?
   - Is there a preferred propagation axis?
""")

print("\n✓ Phase 1 complete: Mode structure extracted from 1D.")
print("✓ Phase 2 in progress: 2D geometry and symmetry analysis.")
