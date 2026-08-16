---
node_id: "C-313"
canonical_name: "Lorentz Invariance vs. Preferred-Frame Conflict"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Open Conflict Record — Foundational"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node C-313: Lorentz Invariance vs. Preferred-Frame Conflict

Dependencies:
Upstream: A-109 Inertial Memory, A-111 Recursion, C-309 Friction Limit, Book 1 Ch10
Downstream: C-314, C-315, E-518, all future relativistic reformulations

## Conflict

The real discrete update rule contains inertial carry-forward with damping:

\[
\psi_i^{n+1}=\psi_i^n+(1-\gamma)(\psi_i^n-\psi_i^{n-1})+\beta_i(\langle\psi_j^n\rangle-\psi_i^n).
\]

Its continuum form is a damped wave equation:

\[
\psi_{tt}+\mu\psi_t-c_{\mathrm{eff}}^2\nabla^2\psi=0,
\]

with

\[
\mu=\frac{\gamma}{\Delta t},\qquad
c_{\mathrm{eff}}^2=\frac{\beta\,\Delta x^2}{2d\,\Delta t^2}.
\]

The first-time-derivative term selects a preferred time direction. It is not exactly Lorentz invariant.

## Continuum-Scaling Correction

`γ` is a dimensionless per-step damping fraction. `μ` is the physical damping rate. A finite continuum refinement requires

\[
\gamma=\mu\Delta t+O(\Delta t^2).
\]

Holding `γ` fixed while taking `Δt -> 0` makes `μ=γ/Δt` diverge, so that is not a finite-damping continuum limit.

The damping relaxation time is

\[
\tau_d=\frac{1}{\mu}=\frac{\Delta t}{\gamma},\qquad \gamma>0.
\]

## Mode Test

For

\[
\psi\propto e^{i(\mathbf{k}\cdot\mathbf{x}-\omega t)},
\]

the dispersion relation is

\[
\omega=-\frac{i\mu}{2}\pm\sqrt{c_{\mathrm{eff}}^2k^2-\frac{\mu^2}{4}}.
\]

Therefore:

```text
c_eff k > mu/2  -> propagating damped mode
c_eff k = mu/2  -> critical transition
c_eff k < mu/2  -> overdamped non-propagating mode
```

Define the dimensionless damping ratio

\[
\epsilon=\frac{\mu}{c_{\mathrm{eff}}k}.
\]

When `epsilon << 1`, the propagating mode is approximately wave-like and the Lorentz-breaking damping is a small correction over short enough times. This supports an **emergent weak-damping approximation**, not exact fundamental Lorentz invariance.

## Resolution State

The earlier proposed test “does gamma go to zero as velocity approaches c?” is not the clean primary test. `γ` is a timestep damping fraction, not a velocity by definition. The correct next question is whether the physical damping ratio `epsilon` becomes negligible for a defined family of propagating modes and whether the same scaling survives changes of frame.

A separately proposed exact D'Alembertian equation without `mu psi_t` remains unreconciled with the canonical damped rule. It cannot replace the canonical equation unless the damping mechanism is derived as an emergent effective term or the framework explicitly abandons exact Lorentz invariance.

## Exact discrete solution for general gamma (closes a previously-open item)

A-114's discrete characteristic equation `z² - (2-γ+C)z + (1-γ) = 0`, `C = β(cos(k·Δx)-1)`, was previously solved only for small `γ` and small `k`. It is exactly solvable by the quadratic formula for any `γ, β, k` — done here, not previously carried out in this repo. Numerically verified (5+ random parameter sets, including a cross-check against the standard leapfrog-scheme dispersion relation at `γ=0`).

Write `b = 2-γ+C`, `c = 1-γ`. The discriminant simplifies exactly to

```
D = b² - 4c = (γ-C)² + 4C
```

**Propagating branch (D<0, complex-conjugate roots):** since the product of roots of any monic quadratic equals its constant term, `|z|² = c` exactly — giving

```
|z| = sqrt(1-gamma)          (exact, k-INDEPENDENT)
```

The decay rate is a flat envelope across every propagating mode, set only by `γ`, never by `k`. This matches and sharpens the continuum result (`Im(ω)=μ/2`, also k-independent) — a real cross-check, not assumed in advance.

The real (oscillatory) part follows from `Re(z)=b/2` and `z=|z|e^{iφ}`:

```
cos(omega_R * dt) = (2-gamma+C) / (2*sqrt(1-gamma))
```

At `γ=0` this reduces exactly to `cos(ω dt) = 1+(β/2)(cos(k·Δx)-1)`, the standard numerical dispersion relation of an explicit leapfrog/central-difference wave-equation discretization — an independent, textbook cross-check, not a coincidence arranged to fit.

**New structural finding, not previously stated anywhere in this repo: a long-wavelength cutoff.** Setting `D=0` and solving for `x ≡ -C = β(1-cos(k·Δx)) ≥ 0` gives the exact propagating/overdamped boundary for any `γ`:

```
x_crit = (2-gamma) - 2*sqrt(1-gamma)
```

For any `γ>0`, `x_crit>0` — meaning sufficiently small `k` (long wavelength) is **overdamped**, not propagating, however small `γ` is. This is the mirror image of C-309's already-known high-`k` propagation ceiling: damping doesn't just decay every mode uniformly, it structurally removes propagation at the long-wavelength end entirely, leaving only an intermediate-to-high-`k` propagating band whose width shrinks as `γ→1`. Numerically verified directly against the exact quadratic (not just the boundary formula) across a k-sweep.

**What this does and does not do for the C-313 conflict:** it fully answers Future Work item 1 below (`μ(k,s)`'s k-dependence: it has none, exactly, in the propagating branch) but it does **not** resolve the Lorentz-invariance question itself, and it specifically does **not** support the hypothesis (raised independently this session, Book 1 Ch10) that `γ`/friction directly produces relativistic-style time dilation for a translating mode: `γ` enters only as a flat, k-independent decay envelope here, never as anything resembling a frequency-curvature or mass term. A translating bound state's speed is carried by its wave-packet's central `k` (via group velocity `dω_R/dk`), not by `γ`, and `γ` has no k-dependence to couple through. If an emergent, symmetric, second-order-in-`u` effect exists in this framework at all, the more promising lever is `ω_R(k)`'s own curvature — it is not linear in `k` at large `k` (it saturates near the zone edge, `cos(ω_R Δt) → 1-β` as `k·Δx→π`, unlike a true relativistic mass-shell `ω²=c²k²+m²`) — but turning "the dispersion has curvature" into an actual derivation of packet-level time dilation is a separate, substantial, still-undone piece of work (comparable to the real, open question of emergent Lorentz symmetry from lattice regularization in lattice-QFT/analogue-gravity theory), not a small next step.

## Yellow Audit

- Finite-damping continuum scaling is now explicit.
- Propagating, critical, and overdamped regimes are derived.
- Approximate weak-damping wave behavior is identified.
- General-gamma exact discrete dispersion relation: SOLVED above (was previously listed as unsolved) — `|z|=√(1-γ)` exactly, k-independent; a new long-wavelength cutoff `x_crit=(2-γ)-2√(1-γ)` identified and verified.
- Checked and found NOT to directly support the "γ = clock-slowing mechanism" hypothesis (Book 1 Ch10) — γ has no k-dependence to carry a speed-dependent effect through; flagged there and here so the two aren't later conflated.
- Frame-transformation behavior of the damped medium is not derived.
- No empirical bound on `mu`, `epsilon`, or their scale dependence exists.
- Whether `ω_R(k)`'s large-k curvature (saturation near the zone edge) could support an emergent, symmetric time-dilation-like effect for wave packets is now a sharper, well-posed open question — not attempted here.

## Future Work

1. ~~Derive `mu(k,s)` or show why it is constant.~~ DONE above: constant (k-independent) in the propagating branch, for any γ.
2. Test whether `epsilon << 1` reproduces measured relativistic behavior within known precision.
3. State explicitly whether the lattice ground is a physical preferred frame.
4. Do not adopt an exact Lorentz-invariant replacement equation until it reproduces A-109 memory, Chapter 11 damping, and observed propagation with the same variables.
5. Attempt packet-kinematics-under-translation using `ω_R(k)`'s derived large-k curvature, to test — honestly, not by assumption — whether it can produce a symmetric, second-order-in-u effect. This is the concrete next step the exact solution above actually opens up.
