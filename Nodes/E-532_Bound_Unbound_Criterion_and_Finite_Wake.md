---
node_id: "E-532"
canonical_name: "Bound vs Unbound Criterion and Finite Wake"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Bound-State Primitive / Mass Mechanism Foundation"
claim_gate_detail: "YELLOW — criterion form tested in reduced runs; continuum limit and residual spectrum still open"
metadata_standard: "I-06"
---

# Node E-532: Bound vs Unbound Criterion and Finite Wake

**Dependencies**  
Upstream: A-107 Bounded Motion, A-108 Local Stability, E-506 Stability, E-509 Propagation Limit, C-318 Mass Mechanism  
Lateral: E-531 Dual-Harmonic Propagation (domain separation), D-408 Sixfold Lattice  
Downstream: residual channel targets, four-force core regimes (C-323), core migration dynamics

## Purpose

Define when a displacement excitation is **bound** (mass-bearing, finite wake) versus **unbound** (propagating, free), and formalize the finite-wake kernel that cuts the far field.

Mass is not continued octave scaling (E-531). Mass is a stable or quasi-stable bound-lattice excitation.

## Bound criterion

On a lattice site (or continuum patch) define local invariants of the displacement field \(\mathbf{u}\):

\[
I_1 = |\mathbf{u}|^2, \qquad I_3 = |\Delta\mathbf{u}|^2
\]

(where \(\Delta\) is the discrete or continuum Laplacian).

Bound flag:

\[
\boxed{
\mathrm{bound} \;\Leftrightarrow\; \bigl(I_3 > \tfrac12 I_1\bigr) \;\wedge\; \bigl(|\mathbf{u}| > u_{\mathrm{floor}}\bigr)
}
\]

- \(I_3 > I_1/2\) encodes sufficient local curvature relative to amplitude (the core cannot flatten into a free wave).
- \(u_{\mathrm{floor}}\) rejects numerical noise.

Only bound sites carry residual orientation density \(C_i\) and participate in rear-compression / core-migration updates.

## Finite wake

A bound core sources a displacement wake in the surrounding medium. The wake is not infinite-range by default. A minimal isotropic kernel with range parameter \(\sigma\) is

\[
W(r) = \frac{e^{-r/\sigma}}{r} \quad (r>0)
\]

(or its lattice transcription).  

- Small \(\sigma\) → short-range residual (strong-like).  
- Large \(\sigma\) → long-range (gravity-like or EM-like depending on orientation content).

The continuum stress (C-323) recovers the same regimes from bulk modulus, curvature penalty, and residual orientation without inserting a separate Yukawa field by hand.

## Residual after last bound state

After the last excitation that still satisfies the bound criterion, any remaining free displacement propagates under the dual-harmonic / free-field rules (E-531). That residual channel is the natural target for neutrino-like or other light unbound modes. Absolute mass-squared scale remains free until the frequency zero of E-531 is fixed.

## Interaction with propagation

Bound cores may source wakes. Those wakes, once outside the core, evolve as free displacement and therefore fall under E-531. The bound flag itself is not a harmonic index; it is a local stability test.

## Required tests

1. Single-core hold: bound flag stable under small perturbations.  
2. Core–core approach: wake interference and possible merger or scattering.  
3. Rear-compression: directed update moves the bound core without dissolving the flag.  
4. Range sweep: vary \(\sigma\) (or continuum \(\gamma, K\)) and recover short vs long effective forces.  
5. Null: free-field packets must not acquire a persistent bound flag under the same update laws.

## Failure / falsification

- If bound flags appear spontaneously on pure free waves under controlled zero-core runs.  
- If no choice of continuum parameters recovers both short-range and long-range limits from the same stress.  
- If residual spectrum after all bound states cannot be made light without breaking lattice energy accounting.

## Status

YELLOW. Criterion form and finite-wake idea tested in reduced 1-D / lattice runs. Continuum closure and residual spectrum still open.
