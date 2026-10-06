"""A-115 source structure across 2D, 3D, and 4D: dimensional analysis of compression-expression wake.

Key insight: The finite-wake kernel W(r) and source form J_r must adapt to dimensionality.
- 1D: W(r) ∝ e^(-r/σ)
- 2D: W(r) ∝ e^(-r/σ)/r
- 3D: W(r) ∝ e^(-r/σ)/r
- 4D: W(r) ∝ e^(-r/σ)/r²

The compression-expression oscillation pattern depends on dimension.
Galaxy disks are ~2D; exterior response may differ from 3D spherical case.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.linalg import solve_banded
from scipy.special import erf


def source_hybrid_nd(r, dimension, sigma_core=0.5, sigma_tail=2.0, weight_tail=0.3):
    """Hybrid source adapted to dimension.

    In dimension d, the source must account for how volume scales with radius:
    - 1D: volume ∝ dr (linear)
    - 2D: volume ∝ r dr (radial measure is r)
    - 3D: volume ∝ r² dr (radial measure is r²)
    - 4D: volume ∝ r³ dr (radial measure is r³)

    The source J_r is per-unit-radial-measure, so it needs compensation.
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        # Core: power-law
        core = r / (sigma_core**2 + r**2)**1.5

        # Tail: exponential with dimension-dependent decay
        if dimension == 1:
            tail = np.exp(-r/sigma_tail)
        elif dimension == 2:
            tail = np.where(r > 1e-6, np.exp(-r/sigma_tail) / r, np.exp(0.) / 1e-6)
        elif dimension == 3:
            tail = np.where(r > 1e-6, np.exp(-r/sigma_tail) / r, np.exp(0.) / 1e-6)
        elif dimension == 4:
            tail = np.where(r > 1e-6, np.exp(-r/sigma_tail) / r**2, np.exp(0.) / 1e-6**2)
        else:
            # General n-dimensional: tail ∝ e^(-r/σ) / r^(n-2)
            n_minus_2 = max(1, dimension - 2)
            tail = np.where(r > 1e-6, np.exp(-r/sigma_tail) / r**n_minus_2,
                           np.exp(0.) / 1e-6**n_minus_2)

    combined = (1. - weight_tail) * core + weight_tail * tail
    return combined / np.max(np.abs(combined) + 1e-10)  # normalize


def solve_a115_dimensional(dimension=3, cells=256, outer_radius=4.,
                          stiffness=2., alpha=1., source_func=None):
    """Solve static A-115 in arbitrary dimension with radial symmetry.

    In dimension d with radial symmetry:
    (K_chi+S_u) d/dr[r^(d-1) d(chi)/dr] = d/dr[r^(d-1) J_r]

    This is the Laplacian in d dimensions: ∇²χ = (1/r^(d-1)) d/dr[r^(d-1) dχ/dr]
    """
    if dimension < 1 or dimension > 5:
        raise ValueError("Dimension must be 1-5")

    if source_func is None:
        source_func = lambda r: source_hybrid_nd(r, dimension)

    edges = np.linspace(0., outer_radius, cells+1)
    dr = outer_radius / cells
    radius = (edges[:-1] + edges[1:]) / 2

    # Radial weighting: r^(d-1)
    radial_weight = np.power(edges, dimension - 1)

    # Evaluate source
    source_at_edges = source_func(edges)

    # Right-hand side: d/dr[r^(d-1) J_r] / stiffness
    # Using finite difference: Δ[r^(d-1) J_r] / dr / stiffness
    flux = radial_weight * source_at_edges / stiffness

    # Weights for tridiagonal system, accounting for dimension
    weights = radial_weight / dr
    weights[-1] *= 2  # Boundary condition

    # Build tridiagonal matrix
    band = np.zeros((3, cells))
    band[1] = -(weights[:-1] + weights[1:])  # diagonal
    band[0, 1:] = weights[1:-1]              # upper
    band[2, :-1] = weights[1:-1]             # lower

    # Solve
    compression = solve_banded((1,1), band, np.diff(flux))

    # Gradient: dchi/dr at cell edges
    gradient = np.zeros(cells+1)
    gradient[1:-1] = np.diff(compression) / dr
    gradient[-1] = -compression[-1] / (dr/2)

    # Acceleration
    acceleration = -alpha * gradient

    # Displacement reconstruction
    volumes = np.diff(np.power(edges, dimension) / dimension)
    displacement = np.zeros(cells+1)
    if cells > 0 and dimension > 0:
        displacement[1:] = -np.cumsum(compression * volumes) / np.power(edges[1:], dimension-1)

    return dict(
        dimension=dimension,
        cells=cells,
        outer_radius=outer_radius,
        stiffness=stiffness,
        alpha=alpha,
        max_compression=float(np.max(np.abs(compression))),
        max_exterior_acceleration=float(np.max(np.abs(acceleration[edges > 1.]))),
        max_interior_acceleration=float(np.max(np.abs(acceleration[edges < 1.]))),
        center_compression=float(compression[0] if cells > 0 else 0.),
        outer_boundary_acceleration=float(acceleration[-1]),
        gradient_falloff_rate=float(np.abs(acceleration[-1] / max(acceleration[int(cells*0.75)], 1e-10))),
        radius_grid=edges.tolist(),
        compression_profile=compression.tolist(),
        acceleration_profile=acceleration.tolist(),
        source_profile=source_at_edges.tolist()
    )


def dimensional_comparison_study():
    """Compare compression-expression wake structure across 2D, 3D, 4D."""

    dimensions = [2, 3, 4]
    cells = 512
    outer_radius = 8.0
    stiffness = 2.0
    alpha = 1.0

    results = {}
    for d in dimensions:
        results[f"{d}D"] = solve_a115_dimensional(
            dimension=d, cells=cells, outer_radius=outer_radius,
            stiffness=stiffness, alpha=alpha,
            source_func=lambda r, dim=d: source_hybrid_nd(r, dim, sigma_core=0.5,
                                                         sigma_tail=2.0, weight_tail=0.4)
        )

    # Extract metrics
    metrics = {}
    for name, result in results.items():
        metrics[name] = {
            "dimension": result["dimension"],
            "max_interior_acceleration": result["max_interior_acceleration"],
            "max_exterior_acceleration": result["max_exterior_acceleration"],
            "exterior_to_interior_ratio": (result["max_exterior_acceleration"] /
                                          max(result["max_interior_acceleration"], 1e-10)),
            "center_compression": result["center_compression"],
            "gradient_falloff": result["gradient_falloff_rate"],
            "outer_boundary_acceleration": result["outer_boundary_acceleration"],
        }

    return results, metrics


def report():
    """Generate dimensional analysis report."""
    root = Path(__file__).resolve().parents[1]
    sources = [
        "Nodes/A-115_Unified_Compression_Field.md",
        "Nodes/E-532_Bound_Unbound_Criterion_and_Finite_Wake.md",
        "solvers/SOURCE_CONSTITUTIVE_DERIVATION.md"
    ]

    results, metrics = dimensional_comparison_study()

    return dict(
        schema_version=1,
        scope="A-115 dimensional analysis: 2D, 3D, 4D with radial symmetry",
        units="dimensionless",

        dimensional_wave_kernels={
            "1D": "W(r) ∝ e^(-r/σ) — pure exponential decay",
            "2D": "W(r) ∝ e^(-r/σ)/r — logarithmic × exponential (disk-like)",
            "3D": "W(r) ∝ e^(-r/σ)/r — 1/r × exponential (spherical)",
            "4D": "W(r) ∝ e^(-r/σ)/r² — 1/r² × exponential (hyperspherical)",
        },

        key_hypothesis=[
            "The compression-expression oscillation pattern adapts to dimensionality.",
            "Galaxy disk (~2D) may respond differently than 3D spherical prediction.",
            "4D structure reveals relativistic or cosmological implications.",
            "One-Wave universality requires consistent source structure across dimensions."
        ],

        derivation_note=(
            "Source form: J_r = (1-w)·r/(σ_core²+r²)^(3/2) + w·e^(-r/σ_tail)/r^(d-2). "
            "In d dimensions, the Laplacian includes r^(d-1) weighting from volume measure. "
            "The finite-volume discretization accounts for this dimensional scaling. "
        ),

        reference_commit="current",
        authority_sha256={
            p: hashlib.sha256((root/p).read_bytes()).hexdigest()
            for p in sources if (root/p).exists()
        },
        solver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),

        results=results,
        metrics_summary=metrics,

        critical_findings=[
            "How does exterior acceleration scale with dimension? (Inverse-power law changes)",
            "Does 2D response match galaxy disk geometry better than 3D?",
            "What is the bound/unbound transition in 2D vs 3D vs 4D?",
            "Can source amplitude and range σ be unified across dimensions?",
            "Does dimensional mismatch explain part of the 40% galaxy error?"
        ],

        next_steps=[
            "Fit 2D solution to galaxy disk data separately from 3D.",
            "Derive bound/unbound criterion (E-532) in arbitrary dimension.",
            "Test whether 2D response predicts different σ and amplitude.",
            "Investigate 4D implications for relativistic/gravitational wave behavior.",
            "Determine if One-Wave source must explicitly specify dimension or is dimension-universal."
        ]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = report()
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")

    # Print dimensional comparison
    print("\n" + "="*80)
    print("A-115 DIMENSIONAL ANALYSIS: Compression-Expression Wake Structure")
    print("="*80)
    print("\nFinite-Wave Kernels by Dimension:")
    for dim, kernel in result["dimensional_wave_kernels"].items():
        print(f"  {dim:3s} {kernel}")

    print("\n" + "-"*80)
    print("Exterior Acceleration Comparison (Hybrid Source, σ=2.0, 40% tail weight):")
    print("-"*80)
    for name, metrics in result["metrics_summary"].items():
        print(f"\n{name} (d={metrics['dimension']}):")
        print(f"  Interior peak:        {metrics['max_interior_acceleration']:12.6e}")
        print(f"  Exterior max:         {metrics['max_exterior_acceleration']:12.6e}")
        print(f"  Exterior/Interior:    {metrics['exterior_to_interior_ratio']:12.3f}")
        print(f"  Gradient falloff:     {metrics['gradient_falloff']:12.3f}")
        print(f"  Outer boundary accel: {metrics['outer_boundary_acceleration']:12.6e}")

    print("\n" + "="*80)
    print("Critical Questions:")
    for i, question in enumerate(result["critical_findings"], 1):
        print(f"{i}. {question}")
    print("="*80)
    print(f"\nFull results: {args.output}")
