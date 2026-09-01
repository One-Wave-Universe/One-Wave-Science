# 13 - Linear Stability Theorem for the Regularized Equilateral Three-Body Orbit

## Purpose

Proof 10 established an exact rotating equilateral three-body solution for the declared pair law

\[
\mathbf a_i
=K\sum_{j\ne i}m_j\,
\frac{F(r_{ij}/\lambda)}{r_{ij}^3}
(\mathbf r_j-\mathbf r_i),
\qquad
F(x)=1-(1+x)e^{-x}.
\]

That existence theorem did **not** answer whether a small shape perturbation grows.

This proof closes that gap at the planar linear level. It derives the exact rotating-frame characteristic polynomial, recovers the classical Gascheau/Routh threshold in the inverse-square limit, and gives the modified stability boundary at finite `s/lambda`.

The result is mathematical for the declared pair law. It does not establish that the law is physically realized.

---

## 1. Exact relative equilibrium from Proof 10

Let three positive masses occupy an equilateral triangle of side `s`. Define

\[
M=m_1+m_2+m_3,
\qquad
x=\frac{s}{\lambda}.
\]

Proof 10 gives the exact angular frequency

\[
\boxed{
\omega^2
=K\frac{M}{s^3}F(x)
}.
\]

Define the pair coefficient

\[
h(r)=K\frac{F(r/\lambda)}{r^3}.
\]

Then the equilibrium relation is simply

\[
\omega^2=Mh(s).
\]

---

## 2. The one local slope parameter that controls the linearization

For a pair displacement vector `d`, with `r=|d|` and unit vector `n=d/r`,

\[
D_{\mathbf d}[h(r)\mathbf d]
=h(r)\left[I+\eta\,\mathbf n\mathbf n^T\right],
\]

where

\[
\boxed{
\eta
=\left.\frac{d\ln h}{d\ln r}\right|_{r=s}
=\frac{s h'(s)}{h(s)}
}.
\]

For the present kernel,

\[
F'(x)=xe^{-x},
\]

so

\[
\eta(x)
=\frac{xF'(x)}{F(x)}-3
=\frac{x^2e^{-x}}{1-(1+x)e^{-x}}-3.
\]

Multiplying numerator and denominator by `e^x` gives the useful exact form

\[
\boxed{
\eta(x)=\frac{x^2}{e^x-1-x}-3.
}
\]

Thus all short-range modification of the planar linear stability enters through one dimensionless local slope `eta(x)`.

---

## 3. Exact range and monotonicity of `eta`

Let

\[
q(x)=\eta(x)+3=\frac{x^2}{e^x-1-x}.
\]

For `x>0`, the denominator is positive, so `q>0` and therefore

\[
\eta>-3.
\]

Also

\[
e^x>1+x+\frac{x^2}{2}
\qquad (x>0),
\]

which implies

\[
q<2
\]

and therefore

\[
\eta<-1.
\]

Hence

\[
\boxed{-3<\eta(x)<-1\qquad(x>0).}
\]

The slope is strictly decreasing. Differentiating,

\[
q'(x)
=\frac{x\left[(2-x)e^x-2-x\right]}{(e^x-1-x)^2}.
\]

Define

\[
H(x)=(2-x)e^x-2-x.
\]

Then

\[
H(0)=0,
\qquad
H'(x)=(1-x)e^x-1,
\qquad
H''(x)=-xe^x<0
\]

for `x>0`. Since `H'(0)=0`, it follows that `H'(x)<0`, then `H(x)<0`, then `q'(x)<0`.

Therefore

\[
\boxed{
\eta(x)\text{ decreases strictly from }-1\text{ to }-3
\text{ as }x\text{ runs from }0^+\text{ to }\infty.
}
\]

---

## 4. Rotating-frame linearization

Normalize masses by

\[
\mu_i=\frac{m_i}{M},
\qquad
\mu_1+\mu_2+\mu_3=1,
\]

and normalize time by the exact orbital frequency,

\[
\tau=\omega t.
\]

Choose any unit-side equilateral triangle for the pair directions, for example

\[
\mathbf p_1=(0,0),\qquad
\mathbf p_2=(1,0),\qquad
\mathbf p_3=\left(\frac12,\frac{\sqrt3}{2}\right).
\]

A constant shift to the center-of-mass frame does not change any pair direction or pair Jacobian.

Let `A` be the normalized `6 x 6` acceleration Jacobian. For each pair `i,j`, define

\[
D_{ij}=I+\eta\,\mathbf n_{ij}\mathbf n_{ij}^T.
\]

The pair contributes the exact blocks

\[
A_{ii}\mathrel{-}=\mu_jD_{ij},
\qquad
A_{ij}\mathrel{+}=\mu_jD_{ij},
\]

\[
A_{jj}\mathrel{-}=\mu_iD_{ij},
\qquad
A_{ji}\mathrel{+}=\mu_iD_{ij}.
\]

In the frame rotating with angular speed `omega`, the perturbation `xi` obeys

\[
\boldsymbol\xi''+2J_6\boldsymbol\xi'
=(I_6+A)\boldsymbol\xi,
\]

where prime means `d/dtau` and `J_6` is three copies of the planar quarter-turn matrix

\[
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]

Using the modal ansatz

\[
\boldsymbol\xi=\mathbf v e^{\sigma\tau},
\]

we obtain

\[
Q(\sigma)\mathbf v=0,
\]

with

\[
Q(\sigma)
=\sigma^2I_6+2\sigma J_6-(I_6+A).
\]

---

## 5. Exact characteristic factorization

Define the standard symmetric mass parameter

\[
\boxed{
\beta
=\frac{m_1m_2+m_2m_3+m_3m_1}{(m_1+m_2+m_3)^2}.
}
\]

For positive masses,

\[
0<\beta\le\frac13,
\]

with equality only for equal masses.

Direct evaluation of the `6 x 6` determinant gives

\[
\boxed{
\det Q(\sigma)
=\sigma^2(\sigma^2+1)^2(\sigma^2+\eta+4)
\left[
\sigma^4+(\eta+4)\sigma^2+\frac34\eta^2\beta
\right].
}
\]

This is the central theorem of this proof.

The mass dependence of the nontrivial shape sector collapses completely to the single scalar `beta`; the force-law dependence collapses completely to the single local slope `eta`.

The companion executable independently reconstructs the raw pair Jacobian and numerically checks this factorization at generic complex `sigma` values. The default receipt agrees at approximately `10^-15` relative error.

---

## 6. Mode separation

The factors have a clean interpretation.

- `sigma^2` is the zero-frequency symmetry sector associated with the relative-equilibrium family.
- `(sigma^2+1)^2` is the translational symmetry sector expressed in rotating coordinates.
- `sigma^2+eta+4` is the breathing/scale sector.
- The quartic factor contains the nontrivial planar shape modes.

Because Proof 13 already established

\[
-3<\eta<-1,
\]

we have

\[
1<\eta+4<3.
\]

Therefore the breathing factor always has a purely imaginary pair

\[
\sigma=\pm i\sqrt{\eta+4}.
\]

The only possible planar exponential instability is therefore in the shape quartic.

---

## 7. Exact stability criterion

Put

\[
u=\sigma^2.
\]

The shape quartic becomes

\[
u^2+(\eta+4)u+\frac34\eta^2\beta=0.
\]

Its discriminant is

\[
\boxed{
\Delta=(\eta+4)^2-3\eta^2\beta.
}
\]

Since `eta+4>0` and `beta>0`, the two `u` roots are real and negative exactly when

\[
\Delta\ge0.
\]

Therefore the finite-scale stability boundary is

\[
\boxed{
\beta_{\rm crit}(x)
=\frac{(\eta(x)+4)^2}{3\eta(x)^2}.
}
\]

The classification is:

\[
\boxed{
\begin{aligned}
\beta&<\beta_{\rm crit}(x)
&&\Rightarrow\text{ strict spectral-stability interior for nontrivial planar modes},\\
\beta&=\beta_{\rm crit}(x)
&&\Rightarrow\text{ repeated-root marginal boundary},\\
\beta&>\beta_{\rm crit}(x)
&&\Rightarrow\text{ exponentially unstable shape mode}.
\end{aligned}
}
\]

At the equality boundary the shape frequencies coalesce. This proof does **not** promote that repeated-root boundary to bounded linear stability without a separate Jordan/normal-form analysis.

Inside the strict region the dimensionless squared shape frequencies are

\[
\boxed{
\nu_{\pm}^2
=\frac{\eta+4\pm\sqrt{\Delta}}{2},
\qquad
\sigma=\pm i\nu_+,\ \pm i\nu_-.
}
\]

---

## 8. Exact recovery of Gascheau/Routh

In the inverse-square limit

\[
x=\frac{s}{\lambda}\to\infty,
\]

we have

\[
\eta\to-3.
\]

Then

\[
\beta_{\rm crit}
\to
\frac{(-3+4)^2}{3(-3)^2}
=\frac1{27}.
\]

Thus

\[
\boxed{
\beta<\frac1{27}
}
\]

is recovered as the strict Newtonian triangular stability condition, with `beta=1/27` the limiting boundary.

This is an important external control: the new linearization does not merely produce a plausible-looking threshold; it reduces exactly to the classical result when the candidate force law reduces to inverse square.

---

## 9. A new finite-scale result: short-range regularization enlarges the stable mass region

Because `eta(x)>-3` at every finite `x`,

\[
\beta_{\rm crit}(x)>\frac1{27}
\]

for every finite `s/lambda`.

Therefore every mass triple that is strictly Newtonian-stable remains strictly stable throughout the finite-scale regularized law.

More strongly, the maximum physically possible mass parameter is

\[
\beta_{\max}=\frac13.
\]

All positive-mass triples are inside the strict stability region whenever

\[
\beta_{\rm crit}>\frac13.
\]

For `-3<eta<-1`, this is equivalent to

\[
\eta>-2.
\]

The marginal all-mass boundary is therefore determined by

\[
\eta(x_*)=-2.
\]

Using the exact `eta` formula,

\[
\frac{x_*^2}{e^{x_*}-1-x_*}=1,
\]

or

\[
\boxed{
e^{x_*}=1+x_*+x_*^2.
}
\]

The unique nonzero positive root is

\[
\boxed{
x_*=1.79328213290076\ldots}
\]

Hence

\[
\boxed{
0<\frac{s}{\lambda}<1.7932821329
\quad\Rightarrow\quad
\text{every positive mass triple is in the strict planar spectral-stability region.}
}
\]

At `s/lambda=x_*`, the equal-mass case is marginal and all unequal positive mass triples remain inside.

---

## 10. Critical scale for any mass triple

For

\[
\frac1{27}<\beta\le\frac13,
\]

the strict decrease of `eta(x)` guarantees one unique finite transition scale.

At the boundary

\[
(\eta+4)^2=3\beta\eta^2.
\]

Since `eta<0` and `eta+4>0`,

\[
\eta+4=-\eta\sqrt{3\beta},
\]

so

\[
\boxed{
\eta_{\rm crit}(\beta)
=-\frac4{1+\sqrt{3\beta}}.
}
\]

The unique `x_crit` is then defined by

\[
\boxed{
\eta(x_{\rm crit})=\eta_{\rm crit}(\beta).
}
\]

For `beta<=1/27`, no finite transition exists: the mass triple remains strictly stable for every finite `x` and approaches the Newtonian boundary/control from above only as `x->infinity` when `beta=1/27`.

---

## 11. Numerical examples and explanation of the earlier stress test

### Equal masses `1:1:1`

\[
\beta=\frac13,
\qquad
x_{\rm crit}=1.79328213290076\ldots
\]

Thus equal masses are stable at `x=1` but unstable at `x=3`.

### Earlier stress ratio `1:1.7:2.4`

\[
\beta\approx0.314494425221,
\]

and

\[
\boxed{x_{\rm crit}\approx1.859688760985.}
\]

So the previous run at

\[
x=5
\]

is analytically in the unstable region, while the same mass ratio at `x=1` is in the stable region.

This explains why tiny numerical perturbations grew over several periods even though the unperturbed equilateral orbit itself is an exact solution.

### `1:2:3`

\[
\beta=\frac{11}{36}\approx0.305555555556,
\]

with

\[
x_{\rm crit}\approx1.893093377893.
\]

### Stable stress ratio `100:1:0.5`

\[
\beta\approx0.0146084593171<\frac1{27}.
\]

Therefore it lies in the strict stability region for every finite `s/lambda`, including the earlier long-range stress run.

---

## 12. Executable receipt

Companion bench:

`One_Wave_Bench/gravity/equilateral_linear_stability_bench.py`

Tests:

`One_Wave_Bench/gravity/test_equilateral_linear_stability_bench.py`

Run:

```bash
python One_Wave_Bench/gravity/equilateral_linear_stability_bench.py
python One_Wave_Bench/gravity/equilateral_linear_stability_bench.py --json
cd One_Wave_Bench/gravity
python -m unittest -v test_equilateral_linear_stability_bench.py
```

The executable checks:

1. the exact `eta(x)` short- and long-range limits;
2. the Newtonian `1/27` control;
3. the all-positive-mass boundary `x*=1.7932821329...`;
4. classification of the earlier stable and unstable numerical stress examples;
5. the theorem that Newtonian-stable mass triples remain stable for every finite `x`;
6. the raw `6 x 6` rotating-frame Jacobian determinant against the closed characteristic factorization at generic complex probe values.

The default local receipt for masses `1:1.7:2.4` at `s/lambda=5` gives a raw-determinant/factorization relative mismatch of approximately

\[
8.3\times10^{-16}.
\]

---

## 13. What this proves

Under the exact candidate pair law and the common mass/source coupling assumption already declared in Proof 10:

\[
\boxed{
\text{the planar linear spectral-stability boundary of the exact equilateral orbit is known in closed form.}
}
\]

The boundary is

\[
\boxed{
\beta_{\rm crit}(x)
=\frac{(\eta(x)+4)^2}{3\eta(x)^2},
\qquad
\eta(x)=\frac{x^2}{e^x-1-x}-3.
}
\]

It exactly recovers the classical inverse-square `1/27` threshold and gives a specific finite-scale modification without fitting a new three-body parameter.

---

## 14. What this does not prove

It does not:

- prove nonlinear/Lyapunov stability;
- resolve the repeated-root marginal boundary by Jordan or normal-form analysis;
- solve arbitrary three-body initial conditions;
- prove that the candidate pair law is the physical law of gravity;
- derive `lambda`, `K`, or the common source/mass coupling from independent physical principles;
- establish relativistic, causal, or Solar-System accuracy;
- show that any real celestial system has `s/lambda` in the modified regime.

The next mathematical attack is no longer "is the exact triangle stable?" The linear answer is now explicit.

The next load-bearing physical attack is:

> **derive or independently constrain `lambda` and the source coupling, then test the same fixed values against two-body, three-body, and precision orbital data without retuning.**

## Claim status

**YELLOW-GREEN mathematical theorem for the declared model.**

The characteristic factorization and finite-scale stability boundary are exact for the stated pair law; physical identification of that law with gravity remains open.
