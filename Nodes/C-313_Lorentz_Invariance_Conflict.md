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

## Yellow Audit

- Finite-damping continuum scaling is now explicit.
- Propagating, critical, and overdamped regimes are derived.
- Approximate weak-damping wave behavior is identified.
- Frame-transformation behavior of the damped medium is not derived.
- No empirical bound on `mu`, `epsilon`, or their scale dependence exists.

## Future Work

1. Derive `mu(k,s)` or show why it is constant.
2. Test whether `epsilon << 1` reproduces measured relativistic behavior within known precision.
3. State explicitly whether the lattice ground is a physical preferred frame.
4. Do not adopt an exact Lorentz-invariant replacement equation until it reproduces A-109 memory, Chapter 11 damping, and observed propagation with the same variables.
