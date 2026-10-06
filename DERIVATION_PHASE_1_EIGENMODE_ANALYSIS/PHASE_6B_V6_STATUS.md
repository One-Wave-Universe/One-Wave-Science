# Phase 6B V6: Poisson extraction — measured, not adopted

**Date:** 2026-10-06
**Script:** `discrete_maxwell_solver_v6_poisson.py`
**Status:** The V5 recommendation failed. Faraday error got worse.

V5 said the remaining Faraday error (~2.4) was a bad extraction, and that solving

    lap(φ) = ∇·ψ,   E = ∇φ
    lap(A) = ∇×ψ,   B = ∇×(A k̂)

would take the error to numerical zero. That solve was built with the same div and grad the lattice already uses.

## What the solve did

The Poisson residual is numerical noise. The Laplacian has rank N−1. The only kernel is the constant. The solve is not the bug.

| Disk | Sites | V5 max | V5 mean | V6 max | V6 mean | Poisson residual |
|---|---|---|---|---|---|---|
| radius 2 | 19 | 2.36 | 0.230 | 13.07 | 1.45 | 1e-15 |
| radius 3 | 37 | 2.22 | 0.173 | 11.24 | 1.46 | 2e-15 |

Same wave, same symmetric update, same Faraday test: |∇×E + ∂B/∂t|.

## What that means

A best-scale fit of ∇×E against ∂B/∂t on the radius-2 run does not line them up. Relative RMS after the fit is 0.95. This is not a missed sign and not a missed factor of β or ω.

The Helmholtz parts of ψ do not obey Faraday under this update. V5 looked better because it tested the second derivatives, ∇(∇·ψ) and −∇×(∇×ψ), which are a different object. That closer number is not a solved Faraday law.

## Not claimed

No continuum limit. No publication threshold. The next useful step is to write the relation this update actually preserves, and test that, instead of expecting Faraday to appear once the potential is solved.
