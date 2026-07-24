# ONE-WAVE FRAMEWORK
## Book 1 - Micro
## Chapter 14: Mass Effect as Four-Interaction Carried-Pattern Resistance

Version: 4.0  
Date: July 22, 2026  
Class: A - Core Physics Chapter  
Status: YELLOW (mechanism form resolved; numerical derivation open)

Dependencies: C-318 Four-Interaction Mass-Effect Response, A-109 Inertial Memory,
A-112 Persistent Mode, A-115 Unified Compression Field, C-301 Mirror Gate,
C-311 Electric-Magnetic Duality, C-317 Boundary-Tension Weave, C-322 Mirror-Gate 125 GeV Boundary Response

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

## Relation to the 125 GeV Mirror Gate

The Mass Effect is the local response to translation inside the stable basin.

The 125 GeV Mirror Gate is finite work required to drive the boundary to its first actual crossing into the mirrored orientation basin:

\[
E_{\rm MG}
=
\overline E_4(\mathbf q_G)-\overline E_4(\mathbf q_0).
\]

The two measurements come from the same \(\overline E_4\), but from different changes:

\[
\mathcal M_{ij}
=
\partial_{v_i}\partial_{v_j}\overline E_4\big|_0,
\]

\[
E_{\rm MG}
=
\int_{\Gamma_{0\to G}}
\nabla_{\mathbf q}\overline E_4\cdot d\mathbf q
\approx125\ {\rm GeV}.
\]

Therefore the gate energy is not every object's Mass Effect and is not divided by \(c^2\) to manufacture the mechanism.

The gate helps stabilize Mass Effect because ordinary displacement remains inside the hold basin. A much larger coupled deformation is required to force the orientation flip.

---

## Numerical Program

A valid simulation must use one fixed rule and perform two separate tests.

### Test A - Mass Effect

1. Build a stable 3D recurrent state with all four interactions active.
2. Translate it at several small velocities.
3. Measure cycle-averaged energy change.
4. Extract \(\mathcal M_{ij}\) from the quadratic response.
5. Independently accelerate the mode and verify \(\mathbf F\approx\mathcal M\mathbf a\).

### Test B - Mirror Gate

1. Start from the same hold state.
2. Follow the minimum allowed coupled deformation path.
3. Locate the first actual update that crosses into the mirrored orientation basin.
4. Integrate the signed external pressure-work required along that path.
5. Compare the derived barrier with 125 GeV only after coefficients are fixed.

---

## Energy-Scale Identifiability

Let

\[
E_{\rm physical}
=
\varepsilon_{\rm lat}\mathcal E_{\rm dimensionless}.
\]

The normalized update is unchanged under a global rescaling \(\mathsf W\to\lambda\mathsf W\), while both \(m_{\rm eff}\) and \(E_{\rm MG}\) scale by \(\lambda\). The current update can therefore predict geometry and dimensionless ratios, but not an absolute value in kilograms or GeV.

The first scale-free test is

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
5. The 125 GeV gate barrier and local Mass Effect must emerge from the same four-interaction coefficients but remain different observables.

The mechanism fails if every measured mass retunes the work metric, if each object needs an unrelated rule, or if the electrical shell, Mirror Gate, knot structure, or Boundary-Tension Weave can be omitted without consequence.

---

## Yellow Audit

Resolved:

- false transport-to-mass shortcut permanently removed;
- scalar-potential mass-gap scaffold removed from canonical derivation;
- four interactions and cross-couplings identified;
- Mass Effect defined as the second velocity response of the complete recurrent architecture;
- 125 GeV separated as finite Mirror-Gate work;
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
