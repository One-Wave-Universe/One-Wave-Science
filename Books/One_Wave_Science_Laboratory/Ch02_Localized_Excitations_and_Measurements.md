# Chapter 2 — Localized Excitations and Measurements

**Status:** tested finite nonlinear candidate; canonical physical closure remains open.  
Canonical owners: A-112, A-117, D-409, E-525 and C-318.  
[Previous](Ch01_The_Joint_Response_Laboratory.md) · [Contents](README.md) · [Next](Ch03_From_Candidate_to_Canonical_Derivation.md)

## Particles as measured excitations

The One-Wave starting point is the evolving field. An excitation is a departure from its reference state. A persistent excitation keeps a recognizable relation through successive updates. A detector produces a response to that field; a particle classification names the measured signature.

These are three connected descriptions of one experiment: evolving excitation, measured response and classification. The calculation does not add a bead that must travel through the field. It also does not identify a detector's short output record with the complete field state.

To test this interpretation, build the excitation and obtain the signal from its evolution. Drawing a desired particle shape and assigning its familiar mass would reverse that order.

## Leaving the reflecting cavity

The joint response fixture used a reflecting cavity. The bulk experiment instead uses an even-period periodic FCC lattice. Every site has the native twelve neighbors, including connections across the computational seam. There is no enclosing reflecting wall or imposed well around the excitation.

A periodic box is still finite. An excitation can interact with its periodic images, and a spreading wave can eventually recur. The experiment therefore grows the domain and reports its observation window. It does not call a periodic calculation an infinite universe.

## A declared nonlinear candidate

The implemented hypothesis uses four complex response coordinates ψ=(ψK,ψE,ψM,ψT). Its energy includes spatial coupling, relative-role phase locking, a concentrating quartic term and an amplitude-limiting sextic term. The conserved norm is

\[
N=\Delta V\sum_i\|\psi_i\|^2,\qquad \Delta V=a^3/\sqrt2.
\]

The evolution is first order,

\[
i\dot\psi_i=\frac1{\Delta V}\frac{\partial E}{\partial\psi_i^*}.
\]

This is an explicit constitutive experiment. It has not been derived from the canonical second-order memory recurrence. The coefficients and N are inputs; N is not a particle count or a measured mass. Positive saturation bounds amplitude energy but does not by itself prove a stable localized solution.

The complete energy, coefficients and code are owned by [the bulk derivation](../../solvers/BULK_EXCITATION_DERIVATION.md). The experiment preserves that uncertainty while asking a real numerical question: does the declared law admit and maintain a localized excitation?

## Finding a stationary branch

At fixed N the code optimizes real amplitude profiles and checks

\[
\left.\frac1{\Delta V}\frac{\partial E}{\partial\psi^*}\right|_{\psi=q}=\mu q.
\]

The corresponding complex excitation is ψ(t)=exp(−iμt)q. Its density remains stationary while its phase evolves. A still image would miss that recurrence.

The real-amplitude search finds a valid stationary branch; it does not enumerate vortex states or prove a global minimum over complex fields. A three-vortex knot requires phase circulation and topology that this search has not constructed.

For the published N=20 branch, the residual is below 4.38×10⁻⁸. Its energy is lower than the equal-norm uniform branch. That comparison supports localization against this control, not against every possible state.

## Persistence must be measured in time

The code evolves the candidate without per-step normalization. A normalization reset would conceal leakage or numerical drift. It measures norm, energy, spatial width, localized fraction and full-state recurrence after removing only the allowed global phase.

The published branch retains about 98% of norm within radius 2 over 100 dimensionless time units. Small random phase and amplitude perturbations retain approximately the same localized fraction at the final sample. The conservative dynamics do not damp the perturbations away; the result is finite-time persistence, not proof of asymptotic recovery.

The linear control evolves the same initial profile with the concentrating and saturating terms removed. By time 20 it retains about 8.5% within the same peak-centered region. The contrast shows that the declared nonlinearity changes localization, rather than an enclosing wall maintaining a linear cavity mode.

![Measurements from the published run](../../solvers/bulk_excitation_controls.svg)

The [raw run report](../../solvers/bulk_excitation_results.json) owns all traces, seeds, error measures and controls.

## The signal comes from the same state

For a detector window w, the experiment reports coherent amplitude and intensity:

\[
A_a(t)=\Delta V\sum_iw_i\psi_{ia}(t),\qquad
I(t)=\Delta V\sum_iw_i\sum_a|\psi_{ia}(t)|^2.
\]

A radius-1 window and a radius-2 window return different outputs from the same excitation. Global phase changes coherent amplitude while leaving intensity invariant. The measured phase slope also agrees with the stationary branch's predicted −μ. This closes a numerical loop from a state equation to a detector trace.

These windows remain passive samplers. A physical detector must have its own coupling, response and energy accounting. The reported intensity is a dimensionless sampling statistic, not calibrated energy or a quantum event count.

The detector stays at the reference origin. Localization measurements track the density maximum. That distinction matters: a localized excitation moving away can remain localized while the fixed detector signal falls. The full-state error does not recenter the excitation to hide motion.

## Failures that constrain the next solution

The strongest limitation is the coupling ablation. When cross and phase coupling are removed, localization survives but the norm concentrates almost entirely in one coordinate. The couplings preserve four-role participation; this candidate does not show that all four interactions are necessary for localization. It therefore does not establish the complete C-318 mechanism.

Halving spacing at fixed box size and volume-aware N changes the energy by roughly 15%. Enlarging the domain produces much smaller changes, so domain effects and discretization effects are different problems. Continuum convergence remains open.

A half-bond-shifted seed finds a different stationary branch. This is evidence to investigate lattice pinning and metastability, not a demonstration of freely translating excitations. At low N the search returns an extended state; localization is not automatic across all inputs.

These observations narrow the next derivation. The next law must explain why its coupled structure is necessary, select admissible excitation states without per-target inputs, and survive refinement and translation controls.

## Run and inspect

```sh
python solvers/test_bulk_excitation.py
python solvers/run_bulk_excitation.py > solvers/bulk_excitation_results.json
```

Inspect the failed and changed controls alongside the successful branch. A useful candidate contributes both a working mechanism and specific evidence about what that mechanism has not solved.
