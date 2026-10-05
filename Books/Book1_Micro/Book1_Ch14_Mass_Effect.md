# ONE-WAVE FRAMEWORK
## Book 1 - Micro
## Chapter 14: Mass Effect as Four-Interaction Carried-Pattern Resistance

Version: 4.1  
Date: October 4, 2026  
Class: A - Core Physics Chapter  
Status: YELLOW (mechanism form resolved; numerical derivation open)

Dependencies: C-318 Four-Interaction Mass-Effect Response, A-109 Inertial Memory,
A-112 Persistent Mode, A-115 Unified Compression Field, C-301 Mirror Gate,
C-311 Electric-Magnetic Duality, C-317 Boundary-Tension Weave, C-322 Mirror-Gate Boundary Coupling and Phase Response

---

## Gray - Standard Physics Reference

Established physics uses mass as the coefficient relating force and acceleration and uses relativistic rest-energy relations for energy bookkeeping. Particle physics also uses Higgs-field coupling language for elementary masses, while most measured proton mass is associated with strong-interaction energy.

Those are external comparison systems. One-Wave must not import a scalar potential, call it the lattice, and declare the labels changed.

---

## Permanent Assumption Correction

A previous draft treated propagation status as though it created inertia. That claim entered through a misunderstanding of C-309's transport constraint and was never derived from One-Wave primitives. It is false, erased from the canonical mechanism, and may not be revived under alternate wording.

The later attempted replacement is also removed from canonical derivation:

```text
scalar potential V(phi)
-> curvature V''(v)
-> conventional mass gap
-> localized lump
-> Mass Effect
```

That sequence describes a familiar external field-theory scaffold. It does not derive One-Wave mass from the architecture already present in the repository.

---

## The Four Interactions

A material Persistent Mode is one coupled 3D recurrence maintained by:

1. **Internal knot interaction** - Three-Vortex geometry, recursive motion, and structural resistance.
2. **Electrical-shell interaction** - the pressure/stress shell created by boundary resistance and roll-off.
3. **Mirror-Gate interaction** - compression/expression orientation resistance and restoring pressure.
4. **Boundary-Tension Weave interaction** - surface-and-volume confinement and reclosure.

These are four interactions of one field state, not four forces and not four unrelated modules.

Write the complete state as

\[
\mathbf Z
=
(\mathbf Z_K,\mathbf Z_E,\mathbf Z_M,\mathbf Z_T).
\]

Its cycle-averaged energy is

\[
\overline E_4[\mathbf Z]
=
\left\langle
E_K+E_E+E_M+E_T+E_\times
\right\rangle_{\rm cycle}.
\]

The cross term \(E_\times\) is required. It contains the changes that belong to relations between interactions rather than one isolated component.

---

## Stable Hold Before Motion

Let \(\mathbf q\) denote allowed internal deformations. A stable hold state \(\mathbf q_0\) satisfies

\[
\nabla_{\mathbf q}\overline E_4(\mathbf q_0)=0
\]

and

\[
\nabla^2_{\mathbf q}\overline E_4(\mathbf q_0)\succ0
\]

on destructive deformation directions.

It must also recur:

\[
\|\mathbf Z_{n+k}-\mathbf Z_n\|<\epsilon.
\]

A bounded object is therefore not a frozen lump. It is a relationship that keeps rebuilding itself.

---

## Why Acceleration Produces a Mass Effect

Let \(\mathbf X(t)\) be the center of the complete bounded recurrence.

Moving the mode through Ground requires every field profile to be relocated and reconstructed. For each interaction component,

\[
D_t\mathbf Z_a
=
\partial_t\mathbf Z_a
-
\dot{\mathbf X}\cdot\nabla\mathbf Z_a.
\]

Let \(\mathbf v=\dot{\mathbf X}\). Near rest, the cycle-averaged energy has the form

\[
\overline E_4(\mathbf v)
=
\overline E_4(0)
+
\frac12v_i\mathcal M_{ij}v_j
+O(|\mathbf v|^3).
\]

Define the Mass-Effect tensor:

\[
\boxed{
\mathcal M_{ij}
=
\left.
\frac{\partial^2\overline E_4}
{\partial v_i\partial v_j}
\right|_{\mathbf v=0}
}
\]

Then

\[
F_i^{\rm applied}
=
\frac{d}{dt}
\left(
\frac{\partial\overline E_4}{\partial v_i}
\right)
\approx
\mathcal M_{ij}a_j.
\]

If damping is active, the low-speed force has two different pieces:

\[
F_i^{\rm applied}
=
\mathcal M_{ij}a_j
+
\mathcal C_{ij}v_j
+\cdots.
\]

The \(\mathcal C v\) term is drag/attenuation. It is not folded into Mass Effect. A constant-velocity drag relative to Ground would also have to survive the C-313 frame audit.

For an isotropic lowest mode,

\[
\boxed{
m_{\rm eff}=\frac13\operatorname{Tr}\mathcal M}
\]

is the measured Mass Effect after drag is separated.

The mechanism is therefore:

```text
stable four-interaction recurrence
-> external attempt to change its motion
-> knot, shell, Mirror relation, and weave must all be rebuilt asymmetrically
-> combined field reaction opposes the change
-> measured Mass Effect
```

Mass is not a substance inside the mode. It is the response of the whole bounded architecture to changed motion.

---

## Direct Lattice Form

For one update step, a center shift \(\delta\mathbf X=\mathbf v\Delta t\) changes the complete profile by

\[
\delta_v\mathbf Z_i
=
-\Delta t\,v_jD_j\mathbf Z_{0,i}+O(|\mathbf v|^2).
\]

A-109 tells the lattice to carry prior state differences forward. To turn that carried difference into measurable work, the model still needs one derived four-interaction work metric \(\mathsf W_i\):

\[
\Delta E_{\rm carry}
=
\frac{1}{2\Delta t^2}
\sum_i\Delta V\,
(\delta_v\mathbf Z_i)^{\mathsf T}\mathsf W_i(\delta_v\mathbf Z_i).
\]

Therefore

\[
\boxed{
\mathcal M_{jk}
=
\sum_i\Delta V\,
(D_j\mathbf Z_{0,i})^{\mathsf T}
\mathsf W_i
(D_k\mathbf Z_{0,i})
}.
\]

The diagonal blocks of \(\mathsf W\) belong to the four interactions; the off-diagonal blocks are their coupling costs. The update rule currently lacks this calibrated work metric, which is why it can evolve dimensionless states but cannot yet predict kilograms.

---

## Continuum Work-Metric Form

A calculable form is

\[
\mathcal M_{ij}
=
\left\langle
\int
(\partial_i\mathbf Z)^{\mathsf T}
\mathsf W(\mathbf Z)
(\partial_j\mathbf Z)
\,dV
\right\rangle_{\rm cycle}.
\]

The work metric \(\mathsf W\) contains:

- inertial memory of the internal knot;
- electrical-shell resistance;
- Mirror-Gate restoring response;
- Boundary-Tension Weave reconstruction;
- off-diagonal couplings among all four.

The diagonal pieces alone are not enough. A proton is not four independent mechanisms sharing an address.

Dimensional check:

\[
[\mathcal M]=[E]/[v]^2={\rm kg}.
\]

---

## Relation to Mirror-Gate Coupling

Mass Effect measures local translational response. C-322 measures boundary coupling and phase response: reflection, deflection, tangential roll-off and scattering. There is no forced-through boundary path. The two responses must come from the same four-interaction architecture, but neither determines the other by dividing an observed energy by a speed squared.

The proposed connection to CERN's approximately 125 GeV reconstructed invariant-mass peak remains a hypothesis requiring a forward prediction.

## Numerical Program

### Test A - Mass Effect

Build a stable native 3D recurrent state with all four interactions and cross-couplings. Translate it at several small velocities, measure cycle-averaged energy, extract the second velocity response, then independently verify acceleration response with fixed coefficients.

### Test B - Mirror Gate

Start from the same state. Derive its boundary coupling operator and phase response, sweep incident conditions without permitting geometric penetration, and close input/output/storage/loss accounting. Select response features independently of measured target values. Compare only after freezing coefficients and detector response.

## Energy-Scale Identifiability

Let

\[
E_{\rm physical}
=
\varepsilon_{\rm lat}\mathcal E_{\rm dimensionless}.
\]

The normalized update is unchanged under a global rescaling \(\mathsf W\to\lambda\mathsf W\), while both \(m_{\rm eff}\) and \(E_{\rm MG}\) scale by \(\lambda\). The current update can therefore predict geometry and dimensionless ratios, but not an absolute value in kilograms or GeV.

A conditional scale-free test, once a boundary-response energy is defined and computed, is

\[
\mathcal R_G
=
\frac{E_{\rm MG}}{m_{\rm eff}v_{\rm lat}^2}
=
\frac{\Delta\mathcal E_G}{\widetilde m}.
\]

Then the model must choose one route: calibrate \(\varepsilon_{\rm lat}\) from another microscopic observable and predict 125 GeV, or use 125 GeV as the calibration anchor and predict the rest of the spectrum without refitting.

---

## Predictions and Failure Tests

1. Every bounded material mode with nonzero Mass Effect must require coupled reconstruction under translation.
2. A traveling light mode must retain zero rest Mass Effect under the same update law.
3. Removing any one of the four interactions must change or destroy the derived Mass Effect.
4. One response law must generate more than one measured Mass Effect without per-object fitting.
5. A proposed boundary-response feature and local Mass Effect must emerge from the same four-interaction coefficients but remain different observables.

The mechanism fails if every measured mass retunes the work metric, if each object needs an unrelated rule, or if the electrical shell, Mirror Gate, knot structure, or Boundary-Tension Weave can be omitted without consequence.

---

## Reproduced Solver Limitation

The existing Phase 5 solvers do not yet execute Tests A and B. They insert measured mass ratios and select the compression endpoint at 125 GeV. Their outputs cannot establish independent predictions. The [reproduction audit](../../Internal_Proofs/Boundary_Coupling_and_Phase5_Audit.md) supplies commands and the corrections recorded in C-318.

## Yellow Audit

Resolved:

- false transport-to-mass shortcut permanently removed;
- scalar-potential mass-gap scaffold removed from canonical derivation;
- four interactions and cross-couplings identified;
- Mass Effect defined as the second velocity response of the complete recurrent architecture;
- measured collider energy separated from an unproved gate identification;
- dimensions close;
- inertial response is separated from velocity drag.

Open:

- stable 3D four-interaction profile;
- four-interaction work metric from the discrete update rule;
- explicit independent-calibration or 125-GeV-calibration route;
- measured Mass-Effect spectrum;
- gapless traveling-light branch under the same fixed law;
- separate damping tensor and C-313 frame consistency.

---

## Closing

It is what the field does when a bounded recurrence refuses to have only one part moved at a time.

The knot, shell, Mirror relation, and weave must all move together. Their coupled resistance is what gets measured.

END OF BOOK 1 CHAPTER 14

## Executable joint-response replacement (2026-10-04)

The four-interaction calculation now runs on D-409's native twelve-neighbor 3D FCC shell. See [the derivation](../../solvers/JOINT_RESPONSE_DERIVATION.md), [solver](../../solvers/joint_boundary_response.py) and [complete results](../../solvers/joint_response_results.json).

One declared joint operator computes exact discrete energy, passive coupling and phase response, boundary-coordinate inertia and carried-profile energy curvature. Eleven tests pass. The 500-step relative energy drift is below 9.38e-14; the maximum lossless power-ledger error is below 1.34e-15. Cross-coupling removal eliminates interaction-port transfer. No measured mass or 125 GeV target is an input.

Refinement from 13 to 55 to 177 sites changes the first spatial frequency from 0.459660896 to 0.632761487 to 0.683984404. These are dimensionless candidate-cavity results. A self-held knot, constitutive coefficients, physical amplitude, absolute units and observable channel mapping remain required before a particle-mass claim. The imposed reflecting cavity is a conservation control, not demonstrated confinement. Boundary ports currently describe interaction coordinates rather than angular bounce, roll-off or spatial scattering distributions.

## Bulk excitation follow-up (2026-10-04)

[The nonlinear bulk experiment](../../solvers/BULK_EXCITATION_DERIVATION.md) tests particles as measured signatures of field excitations: evolve the native 3D field, then sample specified detector windows. It supplies a localized candidate without an enclosing reflecting wall and publishes stationary residuals, 100-time-unit perturbation traces, linear and uniform controls, domain growth, spacing refinement and coupling ablations.

This is an additive hypothetical first-order closure, not a derivation from the canonical memory update or an established four-interaction mass mechanism. Coupling-off localization survives; spacing changes energy about 15%; a shifted seed finds a distinct pinned branch. These results are retained as constraints on the next physical derivation. No particle mass target or forced Mirror penetration enters the experiment.
