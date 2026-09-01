# 14 - Experimental Bound on the Universal Fixed-lambda Gravity Kernel

## Claim status

**GREEN mathematical identification; external empirical constraint.**

For the universal, constant-`lambda` interpretation of the Proof-09 pair law, the potential is exactly a standard Yukawa modification with fixed strength `alpha = -1`. The 2020 Eot-Wash inverse-square-law result therefore applies directly to this specific model class and requires

\[
\boxed{\lambda < 38.6\ \mu\mathrm m\quad(95\%\ \mathrm{confidence}).}
\]

This does **not** prove or disprove the complete One-Wave substrate. It sharply constrains one particular physical identification of the gradient-curvature kernel.

---

## 1. Candidate law

The Proof-09/10 pair potential is

\[
V_{OW}(r)=-K m_1m_2\frac{1-e^{-r/\lambda}}{r}.
\]

The conventional fifth-force parametrization is

\[
V_Y(r)=-G_\infty m_1m_2\frac{1+\alpha e^{-r/\lambda}}{r}.
\]

Term-by-term comparison gives the exact identification

\[
\boxed{G_\infty=K,\qquad \alpha=-1.}
\]

The radial force relative to the far-field inverse-square force is

\[
\frac{F_{OW}}{F_{N,\infty}}
=1-(1+x)e^{-x},
\qquad x=\frac r\lambda.
\]

Therefore the magnitude of the fractional force deficit is

\[
\boxed{D(x)=(1+x)e^{-x}.}
\]

No extra Yukawa amplitude is available to tune: the regularizing Yukawa term has gravitational strength and the opposite sign.

---

## 2. Published experimental constraint

J. G. Lee, E. G. Adelberger, T. S. Cook, S. M. Fleischer, and B. R. Heckel tested the gravitational inverse-square law with detector-attractor separations from `52 micrometres` to `3.0 mm`.

Their Newtonian fit was excellent. They constrained both signs of the Yukawa strength and reported that any gravitational-strength Yukawa interaction must have

\[
\boxed{\lambda<38.6\ \mu\mathrm m}
\]

at 95% confidence.

Reference:

J. G. Lee et al., *New Test of the Gravitational 1/r^2 Law at Separations down to 52 micrometres*, Physical Review Letters **124**, 101101 (2020), DOI `10.1103/PhysRevLett.124.101101`.

Because the Proof-09 candidate maps exactly to `alpha=-1`, it lies inside the tested model class if the coupling is universal, `lambda` is one constant, and the same linear superposition law is used for the experimental bodies.

---

## 3. Far-field coupling

Since the exponential term vanishes as `r/lambda -> infinity`,

\[
V_{OW}\to -K\frac{m_1m_2}{r}.
\]

Thus `K` is the far-field gravitational coupling. Under the physical identification it must match the measured Newtonian gravitational constant.

The 2022 CODATA recommended value is

\[
G=6.67430(15)\times10^{-11}\ \mathrm{m^3\,kg^{-1}\,s^{-2}}
\]

with relative standard uncertainty `2.2e-5`.

At the largest allowed `lambda=38.6 micrometres`, the candidate correction is already approximately

- `1.51e-10` at `1 mm`;
- `8.01e-111` at `1 cm`.

So ordinary centimetre-scale measurements of `G` are effectively in this candidate's far-field limit.

---

## 4. No-retuning consequence

For the largest experimentally allowed `lambda=38.6 micrometres`, solving

\[
(1+x)e^{-x}=\epsilon
\]

gives:

| fractional force deficit | distance above which deficit is smaller |
|---:|---:|
| `1%` | `256.240 micrometres` |
| `0.1%` | `356.410 micrometres` |
| `1 ppm` | `644.173 micrometres` |
| `1 ppb` | `924.073 micrometres` |
| `1e-12` | `1.20046 mm` |

Therefore the non-Newtonian structure of the universal fixed-`lambda` candidate is confined to sub-millimetre scales.

A constant `lambda` large enough to alter planetary, stellar, or galactic dynamics is incompatible with this published inverse-square-law result under the same universal `alpha=-1` pair law.

Choosing a larger fixed `lambda` after applying this constraint would be retuning against the measurement.

---

## 5. Cross-check with Proof 13

Proof 13 found that every positive mass triple lies in the enhanced planar stability region when

\[
\frac{s}{\lambda}<1.79328213290076.
\]

Combining the exact theorem with the experimental upper bound gives

\[
\boxed{s<69.2207\ \mu\mathrm m.}
\]

Thus the genuinely modified part of the Proof-13 stability result is microscopic if `lambda` is universal and constant. At astronomical separation the theorem is forced into the inverse-square Gascheau/Routh limit.

---

## 6. What survives

The experimental bound does not invalidate the mathematics already derived for the declared operator.

The following remain valid model results:

- the Proof-09 Green-function derivation;
- the regularized point-source potential;
- the Proof-12 exact finite uniform-sphere solution;
- the Proof-10 exact equilateral three-body family;
- the Proof-13 exact planar linear-stability theorem.

What fails is a **macroscopic physical interpretation of one universal constant `lambda`**.

This distinction matters: a mathematically valid Green function can still have a physical parameter range that is experimentally restricted.

---

## 7. Honest replacement choices

There are three clean routes forward.

### A. Keep `lambda` constant

Then the gradient-curvature term is a short-range regularizer. It cannot be used as the mechanism for macroscopic gravity anomalies.

### B. Derive a running/effective `lambda`

If `lambda` depends on environment, density, source structure, field state, or scale, the constant-coefficient Proof-09 operator is no longer the complete physical equation.

The dependence must be derived rather than selected after the fact, and must be retested for:

- conservation;
- source-response reciprocity;
- composition-independent fall;
- laboratory inverse-square constraints;
- Solar-System/ephemeris constraints;
- continuity between regimes.

### C. Separate mechanisms

Keep the short-range regularizer and derive a distinct large-scale term/mechanism. That mechanism then needs its own equation and independent falsifier.

---

## 8. Executable receipt

Companion bench:

`One_Wave_Bench/gravity/fixed_lambda_yukawa_constraint_bench.py`

Tests:

`One_Wave_Bench/gravity/test_fixed_lambda_yukawa_constraint_bench.py`

The executable checks:

1. the exact `alpha=-1`, `G_inf=K` mapping;
2. monotonic decay of the force deficit;
3. inverse threshold solutions for `1%`, `ppm`, and smaller corrections;
4. sub-millimetre consequence of the published bound;
5. the Proof-13 `69.2207 micrometre` cross-scale result.

Local run: **7 tests passed**.

---

## 9. Current verdict

\[
\boxed{
\text{Universal fixed-}\lambda\text{ Proof-09 physical model: }
\lambda<38.6\ \mu\mathrm m\ (95\%).
}
\]

Therefore:

\[
\boxed{
\text{the fixed-}\lambda\text{ kernel cannot also be a macroscopic/galactic modification mechanism.}
}
\]

The next load-bearing theory question is now precise:

> **Does the proposed substrate derive a scale/environment-dependent effective `lambda`, or is the large-scale gravity mechanism a separate term?**

Until one of those is derived, the experimentally safe interpretation of Proof 09 is short-range regularization plus an inverse-square far field.

## Sources

- J. G. Lee et al., Physical Review Letters 124, 101101 (2020), DOI `10.1103/PhysRevLett.124.101101`.
- NIST/CODATA 2022 recommended Newtonian constant of gravitation: `G = 6.67430(15)e-11 m^3 kg^-1 s^-2`.
