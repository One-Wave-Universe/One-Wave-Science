# What the symmetric update preserves

**Date:** 2026-10-06
**Script:** `symmetric_update_relation.py`
**Status:** The relation holds on an eigenmode. It does not hold on the V5 plane wave.

The step is

    ψⁿ⁺¹ = 2ψⁿ − ψⁿ⁻¹ − γ(ψⁿ − ψⁿ⁻¹) + β ∇²ψⁿ

with γ = 0.5 and β = 0.5. If ∇²v = μ v, the time factor λ = ψⁿ / ψⁿ⁻¹ obeys

    λ² − (2 − γ + β μ) λ + (1 − γ) = 0

The product of the two roots is 1 − γ = 0.5, so a propagating root has |λ| = √0.5 ≈ 0.707. The field is damped. It is not a unit-modulus Faraday wave.

## Eigenmode of this disk

The mode is the real eigenvector whose μ is closest to −0.25, which is the k² the V5 plane wave assumed. Forty steps.

| Disk | μ | \|λ\| | update residual | λ error |
|---|---|---|---|---|
| radius 2, 19 sites | −0.222222 | 0.707107 | 0 | 3×10⁻¹⁰ |
| radius 3, 37 sites | −0.241880 | 0.707107 | 0 | 1×10⁻⁹ |

The update residual is zero because the history was made by that step. The λ error is the real test. On an eigenmode the characteristic equation holds.

## Plane wave used by V5

Same disks. k = (0.5, 0). The assumed time factor is exp(−i × 0.236039 × 0.01), which has |λ| ≈ 1. That root is not a root of this update.

| | radius 2 | radius 3 |
|---|---|---|
| μ at the center | −0.1565 | −0.1565 |
| μ across the disk | −0.455 to +0.216 | −0.455 to +0.216 |
| λ from the center μ | 0.784 | 0.784 |
| λ the V5 run assumed | ≈ 1 − 0.00236 i | same |
| drift of the center λ | 0.249 | 4.95 |
| update residual | 0 | 0 |

The plane wave is not an eigenmode. Its laplacian changes sign across the disk. The update still runs, and its residual is zero, but the single frequency 0.236 is not what the lattice does.

## Not claimed

Faraday is untouched. This does not repair V5 or V6. It says which relation is real: the damped characteristic equation, and only where ∇²v = μ v.
