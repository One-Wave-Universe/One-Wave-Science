# Measurement / Bell Correlation — Mathematical Backbone v1

Status: **YELLOW / OPEN**

Core-rules reference:
- Rule 1 — Reference Before Interpretation
- Rule 2 — Same Target, Different Explanation
- Rule 5 — No Reverse Fitting
- Rule 7 — Unknown Means Unknown
- Rule 10 — Every Serious Claim Gets a Kill Test
- Rule 12 — Measurement Is A Physical Interaction To Be Derived
- Rule 17 — Mathematics Is The Protected Backbone
- Rule 18 — Missing Math Blocks Promotion

Purpose: restore the mathematical chain that had fallen out of the measurement / entanglement discussion and expose exactly where the simplest One-Wave local detector model succeeds and fails.

This file does **not** establish that Bell correlations have been explained by One-Wave. It preserves the calculation showing that the simplest local sign-sampling model reaches the Bell bound but not the quantum CHSH value.

---

## 1. Common-source oscillation

Let the source carry phase

\[
\lambda \in [0,2\pi).
\]

Use a common-source opposite-phase pair:

\[
W_A = A\cos(\lambda+\delta_A),
\]

\[
W_B = A\cos(\lambda+\delta_B+\pi).
\]

If propagation offsets are equal,

\[
\delta_A=\delta_B,
\]

then

\[
W_B=-W_A.
\]

This is exact peak/trough opposition for the common-source model.

A previous chapter form used opposite signs on the source phase. That sign requires an explicit mirrored-coordinate derivation before it can be treated as equivalent. It must not be silently assumed.

---

## 2. Oriented detector response

For a polarization-style orientation with \(180^\circ\) periodicity, define local continuous detector responses

\[
x_A(\lambda,a)=\cos[2(\lambda-a)],
\]

\[
x_B(\lambda,b)=-\cos[2(\lambda-b)].
\]

Here:
- \(a\) = detector A orientation,
- \(b\) = detector B orientation,
- \(\lambda\) = common source phase.

These equations are a trial detector model, not a completed detector derivation.

---

## 3. Continuous correlation

Average over a uniform unknown source phase:

\[
\langle x_Ax_B\rangle
=
-\frac{1}{2\pi}
\int_0^{2\pi}
\cos 2(\lambda-a)\cos 2(\lambda-b)\,d\lambda.
\]

Using

\[
\cos u\cos v
=
\frac{1}{2}
\left[
\cos(u-v)+\cos(u+v)
\right],
\]

the phase-varying sum term integrates to zero and

\[
\boxed{
\langle x_Ax_B\rangle
=
-\frac12\cos 2(a-b)
}.
\]

Also,

\[
\langle x_A^2\rangle
=
\langle x_B^2\rangle
=
\frac12.
\]

Therefore the normalized continuous correlation is

\[
\rho_{AB}
=
\frac{\langle x_Ax_B\rangle}
{\sqrt{\langle x_A^2\rangle\langle x_B^2\rangle}}
=
\boxed{-\cos 2(a-b)}.
\]

Important result:

The **continuous signed wave response** naturally contains the same angular cosine shape as the polarization-correlation target.

This alone does not derive the discrete quantum outcome statistics.

---

## 4. Bare local plus/minus readout

Now reduce each local response to only its sign:

\[
A(a,\lambda)
=
\operatorname{sgn}
\{\cos[2(\lambda-a)]\},
\]

\[
B(b,\lambda)
=
-\operatorname{sgn}
\{\cos[2(\lambda-b)]\}.
\]

Let

\[
\Delta=|a-b|,
\qquad
0\le\Delta\le\frac{\pi}{2}.
\]

The resulting local sign correlation is

\[
\boxed{
E_{\text{sign}}(\Delta)
=
-1+\frac{4\Delta}{\pi}
}.
\]

The quantum polarization correlation target is

\[
\boxed{
E_{\text{QM}}(\Delta)
=
-\cos(2\Delta)
}.
\]

Selected comparisons:

| \(\Delta\) | \(E_{\text{sign}}\) | \(E_{\text{QM}}\) |
|---:|---:|---:|
| \(0^\circ\) | \(-1\) | \(-1\) |
| \(22.5^\circ\) | \(-0.5\) | \(-\sqrt2/2\approx-0.70710678\) |
| \(45^\circ\) | \(0\) | \(0\) |
| \(67.5^\circ\) | \(+0.5\) | \(+\sqrt2/2\approx+0.70710678\) |
| \(90^\circ\) | \(+1\) | \(+1\) |

Thus the simple sign readout gives a triangular angular correlation rather than the required cosine between the endpoints.

---

## 5. CHSH kill test

Use

\[
a=0^\circ,
\qquad
a'=45^\circ,
\qquad
b=22.5^\circ,
\qquad
b'=-22.5^\circ.
\]

For a local factorized binary-response model of the form above,

\[
|S|\le2.
\]

The sign-sampling trial reaches the local Bell bound:

\[
\boxed{|S|=2}.
\]

The quantum target for these settings is

\[
\boxed{|S|=2\sqrt2\approx2.82842712}.
\]

### Result

\[
\boxed{\text{simple shared phase + independent local sign sampling: FAIL as complete Bell replacement}}
\]

This failure remains part of the backbone. It must not be deleted or summarized away.

---

## 6. Joint discrete target that remains to be derived

For binary results

\[
r_A,r_B\in\{-1,+1\},
\]

the target joint distribution can be written

\[
\boxed{
P(r_A,r_B|a,b)
=
\frac14
\left[
1-r_Ar_B\cos2(a-b)
\right]
}.
\]

It gives local marginals

\[
P(r_A|a)=\frac12,
\qquad
P(r_B|b)=\frac12,
\]

and correlation

\[
\sum_{r_A,r_B}
r_Ar_B
P(r_A,r_B|a,b)
=
-\cos2(a-b).
\]

The open One-Wave mathematical task is therefore:

\[
\boxed{
\text{continuous global wave}
+
\text{local physical detector coupling}
\longrightarrow
P(r_A,r_B|a,b)
}
\]

without inserting the target probability law by hand and without reverse-fitting free coefficients.

---

## 7. Phase reconstruction from a local waveform

For

\[
x=A\cos\Theta,
\]

\[
\dot{x}=-A\omega\sin\Theta,
\]

the local phase can be reconstructed, where the signal model permits both quantities to be measured, by

\[
\boxed{
\Theta
=
\operatorname{atan2}
\left(
-\frac{\dot{x}}{\omega},
x
\right)
}.
\]

For detector / receptor index \(j\),

\[
\Theta_j
=
kL_j-\omega t_j+\lambda.
\]

A source-phase estimate is then

\[
\lambda_j
=
\Theta_j-kL_j+\omega t_j.
\]

A circular weighted reconstruction can be written

\[
\boxed{
\hat{\lambda}
=
\arg
\left[
\sum_j
w_j e^{i\lambda_j}
\right]
}.
\]

This supplies a precise mathematical version of:

**local hits -> retained phase information -> reconstructed peak/trough map.**

It does not by itself solve the Bell discrete-outcome problem.

---

## 8. Current status / next derivation

PASS:
- common-source continuous oscillation can produce an exact cosine-shaped normalized continuous correlation.

FAIL:
- reducing that wave independently to a bare local \(+/-\) sign produces the wrong angular curve and only \(S=2\).

OPEN:
- derive a physical focal-point / detector boundary response that maps the continuous wave to discrete outcomes while reproducing the accepted joint statistics;
- identify what detector state variables are physically retained;
- derive rather than assume any threshold, stochastic term, or coupling coefficient;
- test no-signaling marginals;
- compare against Bell / CHSH data with explicit tolerances.

Kill condition:

If every permitted One-Wave detector law that remains local and uses the declared source state is mathematically constrained to \(|S|\le2\), then that class of One-Wave detector models cannot reproduce the Bell target and must be narrowed or rejected.
