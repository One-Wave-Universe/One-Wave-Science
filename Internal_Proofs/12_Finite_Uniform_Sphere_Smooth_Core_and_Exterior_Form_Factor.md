# 12 — Finite Uniform-Sphere Smooth Core and Exterior Form Factor

## Purpose

Close the exact point-source weakness left by Proof 09 without hiding it.

Proof 09 derives the point-source Green kernel

\[
G(r)=\frac{1}{4\pi a}\left(\frac1r-\frac{e^{-r/\lambda}}r\right),
\qquad \lambda=\sqrt{b/a}.
\]

Its radial magnitude is finite as `r -> 0`, but a point source still has no unique force direction at exact coincidence because `r=|x|` is not differentiable as a Cartesian scalar at the origin.

The correct attack is therefore not to call the point source smooth. Replace the ideal point with an extended source and solve it exactly.

---

## 1. Uniform spherical source

Let a sphere of radius `R` have uniform source density `rho0` and total source

\[
q=\frac{4\pi R^3}{3}\rho_0.
\]

The static field is the convolution

\[
\psi(r)=\frac{1}{4\pi a}\,[P(r)-Y(r)],
\]

where `P` is the ordinary Coulomb convolution and `Y` is the Yukawa convolution.

Define

\[
\mu=\lambda^{-1},\qquad z=\mu R,\qquad y=\mu r.
\]

---

## 2. Exact interior solution

For `0 <= r <= R`, spherical integration gives

\[
P_{in}(r)=2\pi\rho_0\left(R^2-\frac{r^2}{3}\right).
\]

The regular solution of the Yukawa equation inside the constant-density sphere is

\[
Y_{in}(r)=\frac{4\pi\rho_0}{\mu^2}
\left[1-(1+z)e^{-z}\frac{\sinh y}{y}\right].
\]

Use

\[
\frac{\sinh y}{y}=1+\frac{y^2}{6}+O(y^4).
\]

Both interior pieces are even analytic functions of `r` near the center. Therefore

\[
\boxed{\left.\frac{d\psi}{dr}\right|_{r=0}=0.}
\]

More precisely,

\[
\boxed{
\frac{d\psi}{dr}
=-\frac{\rho_0}{3a}
\left[1-(1+z)e^{-z}\right]r+O(r^3).
}
\]

### Result A

**PASS — the finite uniform source has a genuinely smooth zero-slope center.**

This closes the point-source directional cusp for this explicit extended-source model.

---

## 3. Exact exterior solution

For `r >= R`, the Coulomb part is exactly

\[
P_{out}(r)=\frac{q}{r}.
\]

The Yukawa convolution is

\[
Y_{out}(r)=q A(z)\frac{e^{-\mu r}}{r},
\]

with the dimensionless source-size form factor

\[
\boxed{
A(z)=\frac{3[z\cosh z-\sinh z]}{z^3}.
}
\]

Therefore

\[
\boxed{
\psi_{out}(r)=\frac{q}{4\pi a r}
\left[1-A(R/\lambda)e^{-r/\lambda}\right].
}
\]

The long-range `1/r` mode is unchanged. Finite source size changes only the short-range Yukawa correction amplitude.

As `R/lambda -> 0`,

\[
A(R/\lambda)\to1,
\]

so the point-source Green function is recovered.

### Result B

**PASS — finite source size produces a derived exterior form factor, not an ad hoc core patch.**

---

## 4. Boundary matching

The interior and exterior expressions are obtained from the same convolution, so `psi` and its first radial derivative are continuous at `r=R`.

The companion executable independently evaluates the two sides with a small epsilon offset and checks this numerically.

For the default benchmark `R/lambda=1.5`, it reports approximately:

- potential boundary relative mismatch `< 9e-9`;
- radial-slope boundary relative mismatch `< 1e-9`;
- center slope exactly `0` in the analytic implementation;
- center linear-coefficient analytic/numeric mismatch about `1e-13`;
- tiny-source recovery of the point-source law at the few-`1e-9` level;
- far-field recovery of inverse-square behavior at the few-`1e-8` level for the chosen finite test radius.

These are consistency checks of the formulas, not empirical gravity measurements.

---

## 5. Theorem

### Uniform-sphere smooth-core closure

Under the declared Proof-09 gradient-curvature operator and a uniform spherical source:

1. the center potential is finite;
2. the center radial slope is exactly zero;
3. the interior slope is analytic and linear to leading order near the center;
4. potential and first radial derivative match continuously at the source boundary;
5. the exterior field is exactly Coulomb minus Yukawa with source-size form factor `A(R/lambda)`;
6. the point-source kernel is recovered as `R/lambda -> 0`;
7. the unscreened inverse-square far field remains intact.

This is an exact mathematical model theorem.

---

## 6. What this closes

Proof 09 no longer needs to treat the finite point-source radial magnitude as if that alone made the full vector field smooth.

The corrected chain is:

`point-source Green function`
` -> finite radial-magnitude limit but directional cusp at exact coincidence`
` -> explicit extended source`
` -> exact smooth center`
` -> exact exterior finite-size form factor`
` -> point-source and inverse-square limits recovered`.

This is a stronger result because the weak point is solved instead of renamed.

---

## 7. What remains open

This theorem does **not** prove:

- that real gravitating bodies have uniform source density;
- that the Proof-09 operator is the physical law of gravity;
- what physical quantity supplies the source density;
- the value of `lambda`, `a`, or the common coupling;
- the validity of pairwise superposition for the complete many-body field;
- relativistic behavior.

The next source attack is to generalize the convolution to nonuniform spherical profiles and identify which source moments control the Yukawa correction.

The next three-body attack remains the perturbation stability theorem for Proof 10.

---

## 8. Executable receipt

Companion bench:

`One_Wave_Bench/gravity/finite_uniform_sphere_bench.py`

Tests:

`One_Wave_Bench/gravity/test_finite_uniform_sphere_bench.py`

Run:

```bash
python One_Wave_Bench/gravity/finite_uniform_sphere_bench.py --json
cd One_Wave_Bench/gravity
python -m unittest -v test_finite_uniform_sphere_bench.py
```

## Claim status

**YELLOW exact mathematical model theorem.**

The finite-source smooth-core result is closed for the declared operator and uniform spherical source. Physical identification remains unvalidated.