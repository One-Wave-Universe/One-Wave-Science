# 10 — Exact Equilateral Three-Body Closure for the Gradient–Curvature Law

## Purpose

Take the point-source slope derived in Proof 09 and ask for a genuinely nontrivial three-body result.

This proof is deliberately narrower than "solve the general three-body problem." It asks whether the candidate law supports an **exact closed three-body motion** that is not a tautological relation between coordinate differences.

The answer is yes, under one additional physical-identification assumption that is kept explicit below.

---

## 1. Candidate pair law

Proof 09 derives the radial slope factor

\[
F(x)=1-(1+x)e^{-x},
\qquad x=r/\lambda.
\]

Assume source strength and response coupling use one common proportionality to inertial mass, so the acceleration of body `i` is

\[
\boxed{
\mathbf a_i
=K\sum_{j\ne i}
 m_j
 \frac{F(r_{ij}/\lambda)}{r_{ij}^3}
 (\mathbf r_j-\mathbf r_i).
}
\]

`K` is one common interaction normalization.

This common mass coupling is **not derived by Proof 09**. It is an explicit bridge assumption. It is what gives reciprocal pair forces and makes the corresponding pair energy symmetric.

The pair potential energy is

\[
U_{ij}(r)
=-K m_i m_j
\frac{1-e^{-r/\lambda}}{r}.
\]

Differentiation gives the pair-force magnitude

\[
\left|\frac{dU_{ij}}{dr}\right|
=K m_i m_j\frac{F(r/\lambda)}{r^2}.
\]

So the benchmark law is conservative and central.

---

## 2. Put three arbitrary masses on one equilateral triangle

Let three positive masses

\[
m_1,m_2,m_3>0
\]

occupy the vertices of an equilateral triangle with side length `s`.

Every pair separation is therefore exactly

\[
r_{ij}=s.
\]

The kernel factor is the same for every pair:

\[
F_s\equiv F(s/\lambda).
\]

Thus

\[
\mathbf a_i
=
K\frac{F_s}{s^3}
\sum_{j\ne i}m_j(\mathbf r_j-\mathbf r_i).
\]

Because the omitted `j=i` term is identically zero, it can be added back:

\[
\sum_{j\ne i}m_j(\mathbf r_j-\mathbf r_i)
=
\sum_jm_j\mathbf r_j
-\mathbf r_i\sum_jm_j.
\]

Let

\[
M=m_1+m_2+m_3
\]

and

\[
\mathbf R_{CM}=\frac1M\sum_jm_j\mathbf r_j.
\]

Then

\[
\sum_jm_j\mathbf r_j=M\mathbf R_{CM}
\]

so

\[
\boxed{
\mathbf a_i
=-K\frac{M F_s}{s^3}
(\mathbf r_i-\mathbf R_{CM}).
}
\]

This is already the rigid-rotation equation.

---

## 3. Exact angular frequency

Define

\[
\boxed{
\omega^2
=K\frac{M}{s^3}
\left[
1-\left(1+\frac{s}{\lambda}\right)e^{-s/\lambda}
\right].
}
\]

Then every body obeys

\[
\boxed{
\mathbf a_i=-\omega^2(\mathbf r_i-\mathbf R_{CM}).
}
\]

If each initial velocity is the rigid-rotation velocity

\[
\mathbf v_i
=\boldsymbol\omega\times(\mathbf r_i-\mathbf R_{CM}),
\]

all three vertices rotate with the same angular frequency while every pair distance remains `s`.

Therefore an equilateral triangle of **arbitrary positive masses** is an exact rotating solution of this candidate pair law.

The unequal masses do not destroy the shape. They shift the center of mass inside the triangle, and each body rotates at its own distance from that common center.

---

## 4. Far-field/Newtonian limit

When

\[
s\gg\lambda,
\]

then

\[
F(s/\lambda)\to1
\]

and

\[
\omega^2\to K\frac{M}{s^3}.
\]

This is the standard inverse-square equilateral/Lagrange scaling with `K` occupying the role that `G` has in the Newtonian control.

The candidate law therefore changes the short-scale frequency continuously while retaining the standard far-field form.

---

## 5. Near-scale correction

The exact frequency ratio relative to the inverse-square control at the same masses and side length is

\[
\boxed{
\frac{\omega^2}{\omega_N^2}
=F(s/\lambda)
=1-(1+s/\lambda)e^{-s/\lambda}.
}
\]

Thus the three-body benchmark makes a clean dimensionless prediction once `lambda` is specified.

Examples:

- `s/lambda = 1`: `omega^2 / omega_N^2 ~= 0.264241`;
- `s/lambda = 3`: `~= 0.800852`;
- `s/lambda = 5`: `~= 0.959572`;
- `s/lambda = 10`: `~= 0.999501`.

This is not fitted separately for the three bodies. One `lambda` controls all three pair interactions.

---

## 6. Conservation structure

Because the pair potential depends only on separation and is symmetric in `i,j`, the benchmark has the standard central-potential conservation structure.

For an isolated system:

- pair forces are equal and opposite;
- total linear momentum is conserved;
- total angular momentum is conserved;
- total energy is conserved under the time-independent pair law.

These conservation results depend on the common reciprocal mass/source coupling assumption. If different bodies receive unrelated source and response coefficients, reciprocity can fail and this proof does not apply.

---

## 7. Why this is not the old closure tautology

The identity

\[
(\mathbf r_2-\mathbf r_1)
+(\mathbf r_3-\mathbf r_2)
+(\mathbf r_1-\mathbf r_3)=0
\]

is automatic coordinate bookkeeping. It predicts no dynamics.

The result here is different. It derives a specific dynamical statement:

\[
\mathbf a_i=-\omega^2(\mathbf r_i-\mathbf R_{CM})
\]

with a specific

\[
\omega(m_1,m_2,m_3,s,\lambda,K).
\]

That equation can be integrated, measured, contradicted, or compared with the inverse-square control.

---

## 8. Executable receipt

The companion simulator is

`One_Wave_Bench/gravity/gradient_curvature_three_body_bench.py`.

Tests are in

`One_Wave_Bench/gravity/test_gradient_curvature_three_body_bench.py`.

Run:

```bash
python One_Wave_Bench/gravity/gradient_curvature_three_body_bench.py
python One_Wave_Bench/gravity/gradient_curvature_three_body_bench.py --json
cd One_Wave_Bench/gravity
python -m unittest -v test_gradient_curvature_three_body_bench.py
```

The executable checks:

1. unequal-mass analytic acceleration closes on the center-of-mass rotation equation to floating-point precision;
2. the center-of-mass frame and initial total momentum close;
3. all three pair distances are exactly equal at initialization;
4. a velocity-Verlet run preserves equilateral shape;
5. numerical energy and angular momentum drift remain near integration tolerance;
6. the kernel approaches the inverse-square control at large `s/lambda`.

A local execution of the unequal-mass `(1,2,3)` benchmark produced analytic vector residuals of order `10^-16` and a one-orbit numerical shape/invariant drift near floating-point/integrator precision with 4000 steps per period.

---

## 9. What this proves

Under the Proof-09 field kernel plus the declared common mass/source coupling:

\[
\boxed{
\text{arbitrary-mass equilateral three-body rigid rotation is an exact solution.}
}
\]

The angular frequency is

\[
\boxed{
\omega^2=
\frac{KM}{s^3}
\left[1-(1+s/\lambda)e^{-s/\lambda}\right].
}
\]

That is a real mathematical three-body closure for one nontrivial solution family.

---

## 10. What this does not prove

It does not:

- solve the general three-body problem for arbitrary initial conditions;
- prove that `K=G`;
- derive the common source-to-inertial-mass ratio;
- derive `lambda` from measured physics;
- establish the One-Wave substrate;
- establish relativity or ephemeris accuracy;
- show that real celestial systems ever operate at `s` comparable to `lambda`.

The next physical attack is therefore sharper:

> **Can one independently fixed `lambda` and one common source normalization survive two-body, three-body, and Solar-System controls without retuning?**

If yes, the candidate becomes predictive. If no, the bridge fails.

## Claim status

**YELLOW exact mathematical benchmark.**

Exact for the declared candidate pair law and coupling assumption; physical identification remains open.
