# PRINT PACKET 01 — Gravity: Closed Math and Open Physics

## Submission-safe scope

This packet is deliberately narrower than "the whole One-Wave theory is proved."

It separates four statuses:

- **geometric theorem** — follows from geometry/conservation;
- **model theorem** — exact after a stated mathematical model is assumed;
- **conditional theorem** — exact after additional coupling assumptions are imposed;
- **open physical hypothesis** — still needs derivation or measurement.

The point is to keep valid mathematics defensible even if a later physical interpretation fails.

---

## Result 1 — spherical sieve closure

For a conserved radial throughput `J` in ordinary three-dimensional space,

\[
\nabla\cdot\mathbf J=0,
\qquad
\mathbf J=J_r(r)\hat{\mathbf r}.
\]

Then

\[
\frac1{r^2}\frac{d}{dr}[r^2J_r(r)]=0
\]

and therefore

\[
\boxed{J_r(r)=\frac{Q}{4\pi r^2}}.
\]

This is the rigorous geometric content of the "sand in a sieve" picture: the same throughput distributed over spherical shell area `4 pi r^2` produces an inverse-square density.

**Status: geometric theorem.**

It does not by itself prove that gravity is literally this throughput or that matter couples to it with the required sign/strength.

---

## Result 2 — gradient-curvature Green function

Take the declared static functional

\[
E[\psi]=\int\left[
\frac a2|\nabla\psi|^2
+\frac b2(\nabla^2\psi)^2
-J\psi
\right]d^3x,
\qquad a>0,\;b>0.
\]

Variation gives

\[
\boxed{b\nabla^4\psi-a\nabla^2\psi=J.}
\]

For a point source, with

\[
\lambda=\sqrt{b/a},
\]

the exact 3-D Green function is

\[
\boxed{
\psi(r)=\frac{q}{4\pi a r}\left(1-e^{-r/\lambda}\right).
}
\]

Its radial slope contains

\[
F(x)=1-(1+x)e^{-x},
\qquad x=r/\lambda,
\]

so the far field approaches inverse square.

**Status: exact model theorem under the declared functional.**

The point-source radial magnitude is finite at small radius, but the full vector direction is not defined at exact point coincidence. Proof 12 closes that weakness with an extended source.

---

## Result 3 — finite uniform source has a smooth center

For a uniform spherical source of radius `R` and total source `q`, define

\[
\mu=1/\lambda,
\qquad z=\mu R.
\]

The exact interior solution is Coulomb minus Yukawa. Near the center,

\[
\boxed{
\frac{d\psi}{dr}
=-\frac{\rho_0}{3a}
\left[1-(1+z)e^{-z}\right]r+O(r^3).
}
\]

Therefore

\[
\boxed{d\psi/dr|_{r=0}=0.}
\]

Outside the source,

\[
\boxed{
\psi_{out}(r)=\frac{q}{4\pi a r}
\left[1-A(R/\lambda)e^{-r/\lambda}\right],
}
\]

with

\[
\boxed{
A(z)=\frac{3[z\cosh z-\sinh z]}{z^3}.
}
\]

Potential and first radial derivative match at the source boundary. As `R/lambda -> 0`, `A -> 1` and the point-source kernel is recovered.

**Status: exact model theorem for a uniform spherical source.**

Executable receipt:

`One_Wave_Bench/gravity/finite_uniform_sphere_bench.py`

---

## Result 4 — exact equilateral three-body family

Assume the reciprocal pair acceleration

\[
\mathbf a_i
=K\sum_{j\ne i}m_j
\frac{F(r_{ij}/\lambda)}{r_{ij}^3}
(\mathbf r_j-\mathbf r_i).
\]

Put any three positive masses on an equilateral triangle of side `s`. In the center-of-mass frame,

\[
\sum_jm_j\mathbf r_j=0.
\]

Because every pair separation is `s`,

\[
\sum_{j\ne i}m_j(\mathbf r_j-\mathbf r_i)
=-M_{tot}\mathbf r_i.
\]

Thus

\[
\boxed{
\mathbf a_i=-\omega^2\mathbf r_i,
\qquad
\omega^2=\frac{K M_{tot}}{s^3}F(s/\lambda).
}
\]

So the triangle can rotate rigidly with exactly fixed side length.

**Status: exact model theorem under pairwise superposition and common reciprocal mass/source coupling.**

This is a real three-body solution family, but it is not a solution of arbitrary three-body initial conditions and it does not establish perturbation stability.

Executable receipt:

`One_Wave_Bench/gravity/gradient_curvature_three_body_bench.py`

---

## Result 5 — source/response mass coupling

If source `A` creates `S_A G` and response body `B` couples with coefficient `R_B`, then pair reciprocity requires

\[
R_BS_A=R_AS_B.
\]

If universal free fall additionally imposes `R_i/m_i = beta`, then both source and response coefficients are proportional to inertial mass.

**Status: conditional theorem.**

Pairwise reciprocity is an explicit extra assumption and is stronger than total momentum conservation in a dynamical field theory where the field can carry momentum.

---

## What is closed now

1. spherical conserved throughput -> exact `1/r^2` density;
2. declared gradient-curvature functional -> exact Coulomb-minus-Yukawa Green function;
3. uniform spherical source -> exact smooth zero-slope center and exterior finite-size form factor;
4. declared reciprocal pair law -> exact arbitrary-mass equilateral rigid-rotation family;
5. pair reciprocity + universal response -> mass-proportional source/response coupling.

---

## What is still open

1. Derive why the physical Ground must use the gradient-curvature functional instead of selecting it for mathematical usefulness.
2. Fix `a`, `b`, `lambda`, and source normalization independently rather than fitting them to the same observation used as evidence.
3. Generalize the finite-source theorem to nonuniform/realistic source profiles.
4. Derive the many-body field directly and compare it with pairwise superposition.
5. Derive linear perturbation stability for the equilateral family as a function of mass ratios and `s/lambda`.
6. Build a causal dynamical theory with explicit field energy and momentum.
7. Make a held-out quantitative prediction that differs from established gravity models and test it.

---

## Attack order

The next highest-value mathematical target is the **linear stability theorem** for the regularized equilateral three-body orbit.

The next highest-value physical target is a **parameter-independent bridge** from the declared Ground/substrate model to the gradient-curvature functional.

Do not add more interpretation until one of those two load-bearing gaps is reduced.

---

## Reproducibility

Run all current gravity proof tests:

```bash
cd One_Wave_Bench/gravity
python -m unittest discover -v
```

Individual receipts:

```bash
python One_Wave_Bench/gravity/finite_slope_sieve_bench.py --json
python One_Wave_Bench/gravity/gradient_curvature_slope_bench.py --json
python One_Wave_Bench/gravity/gradient_curvature_three_body_bench.py --json
python One_Wave_Bench/gravity/finite_uniform_sphere_bench.py --json
```

The GitHub `Gravity proof bench` workflow runs the full unit-test discovery and emits these receipts on relevant changes.

## Bottom line

The strongest defensible statement is now:

> **Conserved spherical throughput forces inverse-square dilution. A declared gradient-curvature operator produces an exact regularized Green function. A uniform extended source has an exact smooth core. Under a reciprocal pair-law bridge, the same kernel possesses an exact rotating equilateral three-body family.**

That is narrower than proving an entire physical theory, but it is closed mathematics, executable, falsifiable, and ready to be turned into a formal preprint.