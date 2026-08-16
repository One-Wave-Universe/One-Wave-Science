# ONE-WAVE FRAMEWORK
## Book 1 — Micro
## Chapter 10: Time at Micro Scale — Counted Updates and Damping

Version: 4.0
Date: July 22, 2026
Class: B — Applied Layer
Spine: Gray / 2D / 3D / Mathematics / Predictions / Yellow Audit / Future Work / Closing Thoughts

Dependencies: A-109 Inertial Memory, A-111 Recursion, C-309 Friction Limit, C-313 Lorentz Invariance Conflict, F-608 Attenuation, C-314 Three Frames of Reference (Doppler shift explicitly distinguished from clock-rate slowing below — do not conflate)
Status: GREEN (time ontology and relativistic interpretation) / YELLOW (counted-step and damping mathematics)

---

## Gray — Standard Physics Reference

In established physics, time is a coordinate in spacetime. Special and general relativity predict time dilation, and those predictions are experimentally confirmed. Quantum mechanics usually treats time as a parameter rather than an observable operator. The thermodynamic arrow of time is associated with entropy increase.

One-Wave does not yet derive the measured relativistic formulas from its lattice update rule. Those formulas remain comparison targets, not accomplishments of this chapter.

---

## 2D One-Wave Interpretation

The lattice evolves through ordered updates:

\[
\psi^{n-1}\rightarrow\psi^n\rightarrow\psi^{n+1}.
\]

The index `n` counts updates. If one update has duration `Delta t`, the elapsed lattice time after `N` updates is

\[
t=N\Delta t.
\]

Time count and state-change magnitude are not the same variable. Damping and coupling determine how much the state changes during a tick; they do not determine how many ticks have elapsed.

---

## 3D One-Wave Interpretation

The canonical update rule is

\[
\psi_i^{n+1}=\psi_i^n+(1-\gamma)(\psi_i^n-\psi_i^{n-1})+\beta_i(\langle\psi_j^n\rangle-\psi_i^n).
\]

`gamma` suppresses inertial carry-forward. `beta` controls neighbor coupling. Neither coefficient alone is “time.”

The continuum damping rate is

\[
\mu=\frac{\gamma}{\Delta t}.
\]

The damping relaxation time is

\[
\tau_d=\frac{1}{\mu}=\frac{\Delta t}{\gamma}.
\]

This is distinct from elapsed time:

\[
\boxed{t=N\Delta t\neq\frac{N}{\gamma}}.
\]

The earlier `t=N/gamma` expression conflated elapsed update count with damping relaxation.

## Arrow of Time

The notation `n -> n+1` establishes update order, but order notation alone does not prove physical irreversibility. The canonical continuum equation contains

\[
\mu\psi_t,
\]

which damps recoverable motion and selects a preferred time direction when `mu>0`. In the ideal `mu=0` limit, the wave equation can be time-reversal symmetric. Therefore the One-Wave arrow-of-time hypothesis depends on real damping or information loss, not merely on numbering the updates forward.

This creates the explicit C-313 tension: a damped preferred-frame equation is not exactly Lorentz invariant.

## Motion and Gravitational Clock Rates

The current One-Wave hypothesis is that propagation, coupling, and internal change compete for finite update capacity. A moving or strongly coupled mode may therefore complete less internal change per external lattice tick.

That is still a Green mechanism sketch. The repository has not derived

\[
t'=t\sqrt{1-v^2/c^2}
\]

or

\[
t'=t\sqrt{1-2GM/(rc^2)}
\]

from the canonical update rule. These remain required comparison targets. No ad hoc `gamma_eff` formula is retained as though it were a derivation.

**A specific trap to name, not fall into (added after C-314's Medium/Anchor-Frame work):** C-314's addendum derives a real, closed-form result that a moving Focal Point measures a shifted frequency,

\[
\omega'=\omega\left(1-\frac{u}{v_{\rm phase}}\right),
\]

and it is tempting to read this as "motion reduces measured internal rate, therefore this is the mechanism behind time dilation." **It is not, and treating it as such would be exactly the kind of unearned derivation this chapter has repeatedly refused to write down.** Three concrete differences:

1. C-314's shift is a **signal-propagation-delay effect** — how the spacing between wave crests arriving at a moving receiver changes — not a change in the rate of any internal process. It says nothing about whether the source's own internal update cycle actually ran slower.
2. It is **first-order and direction-dependent**: `ω' = ω(1 ∓ u/v_phase)` depending on whether the detector moves with or against propagation (blueshift one way, redshift the other). Measured time dilation is symmetric in the sign of `v` and second-order, `∝v²/c²` — it does not flip sign or vanish for perpendicular motion the way ordinary Doppler does.
3. Nothing in the canonical update rule (`ψ_i^{n+1}=ψ_i^n+(1-γ)(ψ_i^n-ψ_i^{n-1})+β(⟨ψ_j^n⟩-ψ_i^n)`) currently takes a mode's own translational speed `u` as an input at all — `u` is an emergent property of how a localized pattern's centroid moves across sites, not a per-site variable the update rule can condition `γ` or `β` on. A real derivation of clock-rate slowing would need to show how translation and internal cycling draw on the same finite per-tick update capacity (this chapter's own hypothesis, above) — and specifically produce a symmetric, second-order effect — which is a materially harder, still-open problem, not a relabeling of the Doppler result.

The closest existing rigorous treatment of this general kind of question — wave-like excitations in a compressible superfluid medium with a maximum signal speed, and what moving inhomogeneities do to them — is the analogue-gravity literature (Unruh 1981; Barceló, Liberati & Visser, *Living Reviews in Relativity*), where phonons in a moving Bose-Einstein condensate obey an effective relativistic-like wave equation with the local sound speed playing the role of `c`, and genuine horizon/redshift-like effects are derived from the condensate's own equations of motion rather than inserted by hand. This framework's own language (superfluid, compression, friction limit) sits close to that program; engaging with it directly is a more promising path to an actual derivation here than inventing a new `gamma_eff(u)` — but that engagement has not been done in this repository, and this paragraph is a pointer, not a result.

## Minimum Tick

If the lattice has a physical spatial step `Delta x` and maximum propagation speed `c`, a candidate minimum tick is

\[
\Delta t_{\min}=\frac{\Delta x}{c}.
\]

Identifying this with Planck time requires an independently derived `Delta x`; it is not established here.

---

## Mathematics

### Elapsed time

\[
t_N=N\Delta t.
\]

### Damping rate and relaxation

\[
\mu=\frac{\gamma}{\Delta t},\qquad\tau_d=\frac{1}{\mu}=\frac{\Delta t}{\gamma}.
\]

### Finite continuum scaling

For a fixed physical damping rate as the timestep is refined:

\[
\gamma=\mu\Delta t+O(\Delta t^2).
\]

### Damped propagation

\[
\psi_{tt}+\mu\psi_t-c_{\mathrm{eff}}^2\nabla^2\psi=0.
\]

For a Fourier mode:

\[
\omega=-\frac{i\mu}{2}\pm\sqrt{c_{\mathrm{eff}}^2k^2-\frac{\mu^2}{4}}.
\]

This separates propagating, critical, and overdamped regimes. See C-313.

### Attenuation comparison

F-608 uses the provisional spatial law

\[
A(x)=A_0e^{-\eta x}.
\]

Its attenuation coefficient `eta` has not yet been derived from `gamma`, `beta`, and frequency. Spatial attenuation and temporal damping must not be silently treated as identical.

---

## Predictions and Tests

1. If time is counted updates, any physical minimum tick requires a measurable or derivable lattice step.
2. If damping supplies the arrow of time, reducing `mu` should increase reversibility and memory recovery in simulations.
3. The weak-damping ratio `epsilon=mu/(c_eff k)` should control when propagation appears nearly undamped.
4. Relativistic time dilation must be derived from the same canonical variables without inserting the known square-root formulas by hand.
5. A successful model must distinguish elapsed tick count, damping relaxation, propagation phase, and internal clock change.
6. A successful model must also be symmetric and second-order in speed (matching Gray's `v²/c²` behavior), which rules out C-314's Doppler shift — asymmetric and first-order — as a candidate mechanism, however tempting the surface resemblance.

---

## Yellow Audit

Completed:

- obsolete physics I-05 citation removed; real dependencies identified,
- legacy Friction Limit citation repointed to C-309,
- elapsed time separated from damping time,
- finite continuum scaling stated,
- arrow-of-time claim narrowed to damping/information loss.

Still open:

- derivation of special-relativistic time dilation,
- derivation of gravitational time dilation,
- physical calibration of `Delta t`, `Delta x`, `mu`, and `beta`,
- derivation linking temporal damping to spatial attenuation,
- experimental test of a preferred lattice frame,
- a mechanism giving the update rule's gamma or beta any dependence on a mode's own translational speed `u` at all — u is not currently a per-site input variable, which is the concrete reason "finite update capacity" above is still a sketch and not yet math.

Newly clarified (not closed): C-314's derived Doppler shift is confirmed NOT to be a candidate derivation of clock-rate slowing — wrong order in u, wrong symmetry, and a propagation-delay effect rather than an internal-rate effect. See "A specific trap to name" above.

---

## Closing Thoughts

One-Wave's useful claim is not that `gamma` is time. It is that ordered recursive updates provide a count, while resistance and coupling determine how much change can occur during each count.

```text
time count = number of updates
damping time = loss/recovery timescale
clock rate = internal change per update
```

Those quantities may interact, but they are not interchangeable.

---

END OF BOOK 1 CHAPTER 10
