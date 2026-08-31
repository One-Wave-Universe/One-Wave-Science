# 09 — Gradient–Curvature Green-Function Gravity Bridge

## Purpose

Attack the exact gap exposed by D-413 and Proof 08:

> Can the repo produce a gravity-shaped slope from its own declared field architecture instead of imposing a Gaussian well or inserting Newton's inverse-square law as the starting rule?

A-106 already declares the candidate field energy

\[
E[\psi]=\int\left[
\frac a2|\nabla\psi|^2
+V(\psi)
+\frac b2(\nabla^2\psi)^2
\right]d^3x.
\]

This proof target adds an explicit localized source coupling and derives the field equation and Green function. The result is a mathematical theorem **under the declared functional and far-field assumptions**. It is not experimental confirmation that this functional is nature's gravitational law.

---

## 1. Declare the source instead of imposing the well

Use

\[
E[\psi]=\int\left[
\frac a2|\nabla\psi|^2
+\frac b2(\nabla^2\psi)^2
-J\psi
\right]d^3x
\]

in a region where the far-field potential derivative is zero or negligible:

\[
V'(\psi)=0.
\]

Requirements:

- `a > 0`;
- `b > 0`;
- three spatial dimensions for the Green function derived below;
- a localized source `J`;
- no nonzero quadratic far-field pinning term unless its screening consequence is explicitly intended.

The source coupling `-J psi` is a new explicit bridge requirement. A-106 did not previously specify how a gravitating source enters its field equation.

---

## 2. Variation gives the field equation

Vary the functional with respect to `psi`.

The gradient term gives

\[
\delta\int\frac a2|\nabla\psi|^2d^3x
=\int(-a\nabla^2\psi)\,\delta\psi\,d^3x
\]

up to the declared boundary term.

The curvature term gives

\[
\delta\int\frac b2(\nabla^2\psi)^2d^3x
=\int b\nabla^4\psi\,\delta\psi\,d^3x.
\]

The source term gives

\[
\delta\int(-J\psi)d^3x
=\int(-J)\delta\psi\,d^3x.
\]

Therefore stationarity requires

\[
\boxed{b\nabla^4\psi-a\nabla^2\psi=J.}
\]

This is the first non-imposed candidate slope equation in the current gravity attack chain.

---

## 3. Point-source Green function

Let

\[
J(\mathbf r)=q\,\delta^3(\mathbf r).
\]

Fourier transformation gives the denominator

\[
bk^4+ak^2=k^2(a+bk^2).
\]

Define

\[
\lambda\equiv\sqrt{\frac ba},
\qquad
m\equiv\lambda^{-1}=\sqrt{\frac ab}.
\]

Then

\[
\frac1{k^2(a+bk^2)}
=\frac1a\left(
\frac1{k^2}-\frac1{k^2+m^2}
\right).
\]

The two standard 3D transforms are a massless `1/r` mode and a Yukawa/exponential `e^{-mr}/r` mode. Therefore

\[
\boxed{
\psi(r)=\frac{q}{4\pi a r}\left(1-e^{-r/\lambda}\right).
}
\]

The solution is not an imposed Gaussian. Its profile follows from the declared gradient and curvature terms plus the localized source.

---

## 4. Derived radial slope

Differentiate:

\[
\left|\frac{d\psi}{dr}\right|
=
\frac{|q|}{4\pi a r^2}
\left[
1-\left(1+\frac r\lambda\right)e^{-r/\lambda}
\right].
\]

Define

\[
x=r/\lambda.
\]

Then the ratio to the asymptotic inverse-square slope is

\[
\boxed{
\mathcal R(x)=1-(1+x)e^{-x}.
}
\]

and the fractional curvature correction is

\[
\boxed{
\epsilon_{\rm curv}(x)=(1+x)e^{-x}.
}
\]

### Long range

As `r >> lambda`,

\[
e^{-r/\lambda}\rightarrow0
\]

so

\[
\boxed{
|\nabla\psi|\rightarrow\frac{|q|}{4\pi a r^2}.
}
\]

An inverse-square far-field slope therefore emerges from the **gradient mode** of the A-106 candidate functional. It was not inserted as the update rule in this derivation.

### Short range

As `r -> 0`,

\[
\psi(0)=\frac{q}{4\pi a\lambda}
\]

and

\[
|\nabla\psi|(0)=\frac{|q|}{8\pi a\lambda^2}.
\]

The idealized point-source potential and slope are finite in this fourth-order control, rather than diverging as `1/r` and `1/r^2` all the way to zero.

This is a mathematical regularization result, not yet a claim about real microscopic gravity.

---

## 5. The sieve boundary falls out of the correction

Proof 08 established that a finite boundary cannot mean "gravity becomes zero." The Green-function result supplies a cleaner resolution boundary.

Choose a declared resolution tolerance `epsilon` and require

\[
(1+x)e^{-x}\le\epsilon.
\]

Then

\[
r_{\rm assimilate}=\lambda x_\epsilon.
\]

The dimensionless crossing is fixed by the tolerance, while the physical scale comes entirely from

\[
\lambda=\sqrt{b/a}.
\]

Examples:

| retained curvature correction | `r/lambda` required |
|---:|---:|
| 10% | 3.889720 |
| 5% | 4.743865 |
| 1% | 6.638352 |
| 0.1% | 9.233413 |

This gives a precise version of the sieve:

`local gradient+curvature structure`
` -> exponential loss of separately resolvable curvature detail`
` -> long-range gradient mode remains`
` -> parent/far-field representation may drop the resolved curvature correction once its declared error is small enough`.

Nothing is deleted physically by the mathematics. What disappears is the need to resolve the short-range correction independently at the chosen accuracy.

---

## 6. Compression and tension now have distinct mathematical jobs

Within this candidate functional:

- the `a |grad psi|^2` term supplies the long-range massless/gradient mode;
- the `b (laplacian psi)^2` term supplies the higher-curvature mode;
- their ratio defines the structural length `lambda = sqrt(b/a)`;
- the curvature correction regularizes the core and decays exponentially;
- the gradient mode survives as the inverse-square far field.

In the user's project language, this is the closest rigorous current version of

`compression/curvature compacts local structure`

and

`tension/gradient aligns/carries the larger-scale slope`.

Those words are interpretation. The equations above are the actual mathematical content.

---

## 7. Critical pinning test

If the far-field potential contains a quadratic local pinning term

\[
V(\psi)\approx\frac{\mu^2}{2}\psi^2,
\]

then the field equation becomes

\[
b\nabla^4\psi-a\nabla^2\psi+\mu^2\psi=J
\]

and the Fourier denominator becomes

\[
bk^4+ak^2+\mu^2.
\]

For `mu^2 > 0`, the denominator no longer has the `k=0` massless pole. The unscreened `1/r` mode is therefore removed; the far field becomes screened rather than inverse-square.

### D-413 consequence

D-413 contains a local anchor/return term and an imposed Gaussian well. The mechanical anchor is not automatically identical to the continuum `mu^2 psi` term, but it has the same **pinning risk** and must not be assumed compatible with a long-range gravity field.

This explains why the new lattice-only static-response attack must keep separate ledgers for:

- local numerical stabilization/anchors;
- genuine Ground reference structure;
- physical long-range field dynamics.

An absolute-site anchor cannot silently become fundamental gravity physics.

---

## 8. What is proved here

Under the explicitly stated assumptions:

1. varying the A-106 gradient+curvature functional with localized source coupling yields a fourth-order field equation;
2. its 3D point-source Green function is `1/r - exp(-r/lambda)/r` up to normalization;
3. its radial slope approaches inverse-square at long range;
4. the curvature correction has a derived exponential resolution scale;
5. the point-source core is regularized relative to the pure `1/r` control;
6. a nonzero far-field quadratic pinning term removes the massless long-range mode.

These are mathematical results, not fitted orbital observations.

---

## 9. What is not proved

This does **not** yet prove:

- that the One-Wave Ground physically obeys the A-106 functional;
- that `q` is inertial/gravitational mass;
- the value or universality of `a` or `b`;
- the value of Newton's `G`;
- equivalence principle behavior;
- relativistic gravity;
- light bending, gravitational time dilation, or gravitational waves;
- Solar-System ephemerides;
- a new solution of the general three-body problem;
- the proposed superfluid/lattice substrate.

Mapping the asymptotic coefficient to Newtonian gravity would require

\[
\frac{\alpha q}{4\pi a}=G M
\]

if A-105's response is `R_OW=-alpha grad psi`. That normalization and the relation between source charge `q` and measured mass remain open and must be derived or independently calibrated, not assumed.

---

## 10. Executable proof receipt

Run:

```bash
python One_Wave_Bench/gravity/gradient_curvature_slope_bench.py
python One_Wave_Bench/gravity/gradient_curvature_slope_bench.py --json
cd One_Wave_Bench/gravity
python -m unittest -v test_gradient_curvature_slope_bench.py
```

The bench verifies:

- `lambda=sqrt(b/a)`;
- finite core limits;
- inverse-square far-field approach;
- monotonic exponential loss of curvature correction;
- the derived 1% assimilation radius;
- scaling of the assimilation radius with `lambda`;
- the massless-pole/pinning condition.

---

## 11. Proof chain after this attack

The gravity path is now narrower:

`A-103 Differential`
` -> A-104 Gradient`
` -> A-105 response to gradient`
` -> A-106 gradient+curvature energy`
` -> localized-source variation`
` -> fourth-order field equation`
` -> inverse-square far-field slope + finite curvature correction`
` -> Proof 08 hierarchical assimilation/compression`
` -> multi-source / three-body solver`
` -> ephemeris and relativistic controls`.

The next load-bearing question is no longer "can this architecture make an inverse-square-shaped slope?"

Under the A-106 assumptions, **yes, mathematically**.

The next load-bearing questions are:

1. Why must the actual Ground use this functional?
2. What fixes `a`, `b`, and the source coupling?
3. Can the same source normalization work for different bodies without tuning?
4. Does the resulting multi-body field reproduce known gravitational observations and conservation laws?

## Claim status

**YELLOW mathematical bridge.**

The Green-function derivation is closed under its declared assumptions. The physical identification with gravity remains unvalidated.
