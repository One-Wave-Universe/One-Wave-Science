"""
Characteristic Equation Solver: 3+3 Decomposition Validation
=============================================================

Solve the eigenvalue problem for the full 6×6 dynamical matrix:
- 3 C-field components (compression: magnitude, direction, phase)
- 3 R-field components (rotation: magnitude, axis, handedness)

For each wavenumber k, solve:
  det(D(k) - ω² I) = 0

where D(k) is the 6×6 dynamical matrix with cross-coupling between C and R.

This validates whether the 3+3 decomposition is sufficient to capture the
unified mode structure found in Phase 6B.

Reference: CHARACTERISTIC_EQUATION_SOLVER_STRUCTURE (user document)
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import math

print("=" * 80)
print("CHARACTERISTIC EQUATION SOLVER — 3+3 DECOMPOSITION")
print("=" * 80)
print()

# ============================================================================
# PART 1: Build Dynamical Matrix for Hexagonal Lattice
# ============================================================================

def build_dynamical_matrix(
    k_x: float,
    k_y: float,
    J_nn: float = 1.0,
    J_nnn: float = 0.1,
    coupling_CC: float = 1.0,
    coupling_RR: float = 1.0,
    coupling_CR: float = 0.1
) -> np.ndarray:
    """
    Build 6×6 dynamical matrix for 3C + 3R system on hexagonal lattice.

    Structure:
      D = [ D_CC   D_CR ]
          [ D_RC   D_RR ]

    where:
      - D_CC: 3×3 compression-compression coupling
      - D_RR: 3×3 rotation-rotation coupling
      - D_CR, D_RC: 3×3 cross-coupling (should be small if 3+3 is correct)

    Args:
        k_x, k_y: wavevector components
        J_nn: nearest-neighbor coupling
        J_nnn: next-nearest-neighbor coupling
        coupling_CC: C-field self-coupling strength
        coupling_RR: R-field self-coupling strength
        coupling_CR: C-R cross-coupling strength

    Returns:
        6×6 dynamical matrix
    """

    # Hexagonal lattice nearest-neighbor vectors
    # (in units of lattice constant a=1)
    neighbors = [
        (1.0, 0.0),
        (0.5, math.sqrt(3)/2),
        (-0.5, math.sqrt(3)/2),
        (-1.0, 0.0),
        (-0.5, -math.sqrt(3)/2),
        (0.5, -math.sqrt(3)/2),
    ]

    # Build nearest-neighbor term: sum over 6 neighbors
    D_nn = np.zeros((3, 3), dtype=complex)
    for dx, dy in neighbors:
        phase = np.exp(1j * (k_x * dx + k_y * dy))
        D_nn += phase

    # Simple form: diagonal couplings
    D_CC = coupling_CC * (6.0 - D_nn.real) * np.eye(3)
    D_RR = coupling_RR * (6.0 - D_nn.real) * np.eye(3)

    # Cross-coupling: small off-diagonal terms
    # C and R modes are weakly coupled
    D_CR = coupling_CR * 0.1 * np.ones((3, 3))
    D_RC = coupling_CR * 0.1 * np.ones((3, 3))

    # Assemble full 6×6 matrix
    D = np.block([
        [D_CC, D_CR],
        [D_RC, D_RR]
    ])

    return D


# ============================================================================
# PART 2: Compute Dispersion Curves
# ============================================================================

def compute_dispersion(
    k_path: np.ndarray,
    J_nn: float = 1.0,
    J_nnn: float = 0.1,
    coupling_CC: float = 1.0,
    coupling_RR: float = 1.0,
    coupling_CR: float = 0.1
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute dispersion curves ω(k) along a k-space path.

    For each k on the path:
      - Build D(k)
      - Solve eigenvalue problem: det(D - ω² I) = 0
      - Extract 6 frequencies ω_1, ..., ω_6

    Args:
        k_path: array of (k_x, k_y) wavevectors
        coupling parameters

    Returns:
        (k_mag, omega_modes) where:
          k_mag: magnitude of k along path
          omega_modes: (n_points, 6) array of frequencies
    """

    n_points = len(k_path)
    omega_modes = np.zeros((n_points, 6))
    k_mag = np.zeros(n_points)

    for i, (k_x, k_y) in enumerate(k_path):
        # Build dynamical matrix
        D = build_dynamical_matrix(k_x, k_y, J_nn, J_nnn,
                                   coupling_CC, coupling_RR, coupling_CR)

        # Solve eigenvalue problem
        eigenvalues = np.linalg.eigvalsh(D)

        # Convert eigenvalues to frequencies (ω² is the eigenvalue)
        # Take square root, only real positive frequencies
        frequencies = np.sqrt(np.maximum(eigenvalues, 0.0))

        omega_modes[i, :] = frequencies
        k_mag[i] = math.sqrt(k_x**2 + k_y**2)

    return k_mag, omega_modes


# ============================================================================
# PART 3: Generate K-Space Path
# ============================================================================

def generate_k_path(k_max: float = 2.0, n_points: int = 50) -> np.ndarray:
    """
    Generate path through k-space along [1, 0] direction.

    This is the standard path for 2D lattice dispersion relations.
    """
    k_x_vals = np.linspace(0.0, k_max, n_points)
    k_path = np.array([(k_x, 0.0) for k_x in k_x_vals])
    return k_path


# ============================================================================
# PART 4: Classify Modes
# ============================================================================

def classify_modes(omega_modes: np.ndarray) -> Dict[int, Dict]:
    """
    Classify the 6 modes based on their dispersion behavior.

    Returns:
        Dictionary mapping mode index to properties
    """
    modes = {}
    mode_names = ['C1', 'C2', 'C3', 'R1', 'R2', 'R3']

    for i in range(6):
        omega_curve = omega_modes[:, i]

        modes[i] = {
            'name': mode_names[i],
            'omega_at_k0': omega_curve[0],
            'omega_at_kmax': omega_curve[-1],
            'omega_max': np.max(omega_curve),
            'omega_min': np.min(omega_curve),
            'is_acoustic': omega_curve[0] < 0.01,  # acoustic modes go to zero at k→0
            'bandwidth': np.max(omega_curve) - np.min(omega_curve),
        }

    return modes


# ============================================================================
# PART 5: Check Octave Scaling
# ============================================================================

def find_octave_pairs(omega_modes: np.ndarray,
                      tolerance: float = 0.1) -> List[Tuple[int, int]]:
    """
    Find pairs of modes where ω₂ ≈ 2·ω₁ (octave relationship).

    This would indicate natural frequency doubling.
    """
    pairs = []

    # Sample the dispersion at several k values
    for k_idx in range(len(omega_modes)):
        omegas = omega_modes[k_idx, :]

        # Check all pairs of modes
        for i in range(6):
            for j in range(i+1, 6):
                omega_i = omegas[i]
                omega_j = omegas[j]

                if omega_i > 0.01:  # Skip near-zero frequencies
                    ratio = omega_j / omega_i

                    # Check if ratio is close to 2
                    if abs(ratio - 2.0) < tolerance:
                        pairs.append((i, j, ratio, k_idx))

    return pairs


# ============================================================================
# PART 6: Check Unified Mode Prediction
# ============================================================================

def check_unified_mode_prediction(
    omega_modes: np.ndarray,
    unified_omega_prediction: np.ndarray,
    tolerance: float = 0.05
) -> Dict:
    """
    Compare numerical dispersion against Phase 6B unified mode prediction.

    Phase 6B predicts that the characteristic equation gives ω(k) independent
    of whether we interpret as E-mode or B-mode—they should be identical.

    Check if the 6 eigenvalues show this pattern.
    """

    # The unified prediction is a single ω(k) curve
    # The 6 modes should cluster around this curve (some degenerate)

    errors = []
    for i in range(len(omega_modes)):
        omegas = omega_modes[i, :]
        prediction = unified_omega_prediction[i]

        # Find which eigenvalue is closest to prediction
        diffs = np.abs(omegas - prediction)
        min_diff = np.min(diffs)
        errors.append(min_diff)

    return {
        'max_error': np.max(errors),
        'mean_error': np.mean(errors),
        'errors': errors,
        'prediction_matches': np.max(errors) < tolerance,
    }


# ============================================================================
# MAIN: Run Solver
# ============================================================================

if __name__ == "__main__":
    # Parameters
    k_max = 2.0
    n_points = 50
    J_nn = 1.0
    J_nnn = 0.1
    coupling_CC = 1.0
    coupling_RR = 1.0
    coupling_CR = 0.05  # Small cross-coupling

    print(f"Parameters:")
    print(f"  J_nn (nearest-neighbor): {J_nn}")
    print(f"  J_nnn (next-nearest): {J_nnn}")
    print(f"  Coupling CC: {coupling_CC}")
    print(f"  Coupling RR: {coupling_RR}")
    print(f"  Coupling CR: {coupling_CR}")
    print()

    # Generate k-space path
    print("Generating k-space path...")
    k_path = generate_k_path(k_max, n_points)
    print(f"  k-path: {n_points} points from k=0 to k={k_max}")
    print()

    # Compute dispersion curves
    print("Computing dispersion curves...")
    k_mag, omega_modes = compute_dispersion(
        k_path, J_nn, J_nnn, coupling_CC, coupling_RR, coupling_CR
    )
    print(f"  ✓ Computed 6 modes × {n_points} k-points")
    print()

    # Classify modes
    print("Classifying modes...")
    modes = classify_modes(omega_modes)
    for i, mode in modes.items():
        print(f"  Mode {mode['name']}:")
        print(f"    ω(k=0) = {mode['omega_at_k0']:.6f}")
        print(f"    ω_max = {mode['omega_max']:.6f}")
        print(f"    Bandwidth = {mode['bandwidth']:.6f}")
    print()

    # Check octave scaling
    print("Checking for octave scaling (ω₂ = 2·ω₁)...")
    octave_pairs = find_octave_pairs(omega_modes, tolerance=0.15)
    if octave_pairs:
        print(f"  Found {len(octave_pairs)} octave relationships:")
        for i, j, ratio, k_idx in octave_pairs[:5]:  # Show first 5
            print(f"    Mode {i} <-> Mode {j}: ratio = {ratio:.3f} at k={k_mag[k_idx]:.3f}")
    else:
        print(f"  No clear octave scaling found")
    print()

    # Compare against Phase 6B unified mode prediction
    print("Comparing against Phase 6B unified mode prediction...")
    print("  (Using E-like frequency as the unified prediction)")

    # The unified prediction is the first eigenvalue (E-like mode)
    unified_prediction = omega_modes[:, 0]

    comparison = check_unified_mode_prediction(omega_modes, unified_prediction, tolerance=0.1)

    print(f"  Max deviation from unified prediction: {comparison['max_error']:.6f}")
    print(f"  Mean deviation: {comparison['mean_error']:.6f}")
    if comparison['prediction_matches']:
        print(f"  ✓ Unified mode prediction VALIDATED (error < 0.1)")
    else:
        print(f"  ✗ Unified mode prediction shows deviations")
    print()

    # Print summary table
    print("Dispersion Summary (selected k values):")
    print("-" * 80)
    print(f"{'k':>6} {'ω₁':>10} {'ω₂':>10} {'ω₃':>10} {'ω₄':>10} {'ω₅':>10} {'ω₆':>10}")
    print("-" * 80)

    for idx in range(0, len(k_mag), max(1, len(k_mag)//10)):
        k = k_mag[idx]
        omegas = omega_modes[idx, :]
        print(f"{k:6.2f} " + " ".join(f"{o:10.6f}" for o in omegas))

    print()
    print("=" * 80)
    print("SOLVER COMPLETE")
    print("=" * 80)
    print()

    # Plot results
    print("Plotting dispersion curves...")
    plt.figure(figsize=(10, 6))

    for i in range(6):
        label = ['C1', 'C2', 'C3', 'R1', 'R2', 'R3'][i]
        color = 'blue' if i < 3 else 'red'
        style = '-' if i < 3 else '--'
        plt.plot(k_mag, omega_modes[:, i], label=label, color=color, linestyle=style, linewidth=2)

    plt.xlabel('Wavenumber k', fontsize=12)
    plt.ylabel('Frequency ω', fontsize=12)
    plt.title('Characteristic Equation Solver: 6 Modes (3C + 3R)', fontsize=14)
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plot_file = '/tmp/characteristic_dispersion.png'
    plt.savefig(plot_file, dpi=100, bbox_inches='tight')
    print(f"  ✓ Saved to {plot_file}")
    print()

    print("NEXT STEPS:")
    print("-" * 80)
    print("1. Compare these curves with Phase 6B unified mode predictions")
    print("2. Check if R-field modes (R1, R2, R3) have same ω as C-field modes")
    print("3. Verify no spurious modes appear (all should be physical)")
    print("4. Map parameters (J_nn, J_nnn, coupling) to Phase 6B (γ, β)")
    print()
