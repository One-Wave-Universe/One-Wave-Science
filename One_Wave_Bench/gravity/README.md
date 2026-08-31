# Gravity Proof Bench

This directory attacks the planetary finite-range, slope-law, and three-body logic from `UPDATED_38` through `UPDATED_41`.

The rule here is **smallest falsifiable step first**. Do not build a giant Solar-System visualizer while the field law or coupling assumptions are still undefined.

## Current proof/simulator ladder

| Bench | Question | Current result |
|---|---|---|
| `finite_slope_sieve_bench.py` | What can a finite boundary mean without deleting real long-range influence? | **Dominance/resolution boundary + hierarchical compression survive; hard cutoff fails.** |
| `gradient_curvature_slope_bench.py` | Can A-106's declared gradient+curvature energy generate a gravity-shaped slope without an imposed Gaussian well? | **Yes mathematically under declared far-field/source assumptions: finite core + inverse-square far field + exponential curvature correction.** |
| `gradient_curvature_three_body_bench.py` | Does that candidate pair law possess a nontrivial exact three-body solution? | **Yes under common mass/source coupling: arbitrary-mass equilateral rigid rotation closes exactly.** |

## 1. Finite-slope / sieve bench

This bench attacks two boundary interpretations and one compression rule.

### Boundary attack

- tests an absolute parent-slope crossing;
- tests a local differential/tidal crossing;
- checks Earth/Sun against the lunar-orbit control;
- checks whether a Hill-like boundary can be interpreted as a hard influence cutoff.

### Sieve / assimilation attack

- compares direct multi-source acceleration with a center-of-mass parent monopole;
- measures relative acceleration error against the opening ratio `a/R`;
- checks the expected quadratic far-field error when the center-of-mass dipole vanishes.

Current boundary result:

| Idea | Result |
|---|---|
| `local slope = absolute parent slope` defines finite boundary | **Rejected as general boundary** |
| `local slope = local differential/tidal reference` defines dominance boundary | **Works under inverse-square control** |
| dominance boundary means influence becomes zero | **Rejected** |
| distant explicit sources can be compressed into parent state | **Works under standard multipole control** |

For Earth relative to the Sun:

- absolute-background crossing: about `2.59e8 m`;
- lunar orbital radius: about `3.844e8 m`;
- differential/Hill-like boundary (`kappa=3`): about `1.497e9 m`.

The sieve interpretation that survives is therefore:

`explicit local structure -> compressed parent representation -> reopen children when geometry/error requires it`

not

`explicit local structure -> cutoff -> disappear`.

Proof:

`Internal_Proofs/08_Finite_Slope_Sieve_Boundary_and_Assimilation_Proof_Target.md`

## 2. Gradient-curvature slope bench

A-106 declares a candidate energy containing both gradient and curvature terms. With a localized source coupling and no nonzero far-field pinning term, variation gives

```text
b nabla^4 psi - a nabla^2 psi = J
```

with

```text
lambda = sqrt(b/a)
```

and point-source Green function

```text
psi(r) = q/(4*pi*a*r) * (1 - exp(-r/lambda)).
```

The radial slope is

```text
|grad psi| = |q|/(4*pi*a*r^2) * [1 - (1+r/lambda) exp(-r/lambda)].
```

So the short-range curvature correction dies exponentially while the long-range gradient mode approaches inverse-square.

A declared error tolerance produces a derived **resolution** radius. For example the curvature correction falls below 1% at about

```text
r = 6.638352 * lambda.
```

A nonzero quadratic far-field pinning term removes the massless mode and therefore removes the unscreened `1/r` component. This is why D-413's local anchor cannot silently be promoted into the fundamental long-range field law.

Proof:

`Internal_Proofs/09_Gradient_Curvature_Green_Function_Gravity_Bridge.md`

## 3. Exact equilateral three-body bench

Under the additional explicit assumption that source/response coupling has one common proportionality to inertial mass, the candidate acceleration law is

```text
a_i = K sum_j m_j F(r_ij/lambda) (r_j-r_i)/r_ij^3
F(x) = 1 - (1+x) exp(-x).
```

For any three positive masses on an equilateral triangle of side `s`, every pair sees the same kernel factor. The acceleration sum closes exactly on the center of mass:

```text
a_i = -omega^2 (r_i - R_CM)
```

with

```text
omega^2 = K (m1+m2+m3) F(s/lambda) / s^3.
```

The simulator verifies the analytic vector closure with unequal masses and integrates the rigid orbit with velocity Verlet while tracking shape, center of mass, momentum, angular momentum, and energy.

This is an exact solution of the declared candidate pair law. It is **not** a solution of the general three-body problem and does **not** derive the common mass/source coupling assumption.

Proof:

`Internal_Proofs/10_Exact_Equilateral_Three_Body_Closure_for_Gradient_Curvature_Law.md`

## Run everything

From the repository root:

```bash
cd One_Wave_Bench/gravity
python -m unittest discover -v
```

Individual machine-readable receipts:

```bash
python One_Wave_Bench/gravity/finite_slope_sieve_bench.py --json
python One_Wave_Bench/gravity/gradient_curvature_slope_bench.py --json
python One_Wave_Bench/gravity/gradient_curvature_three_body_bench.py --json
```

## Build contract

### Purpose

Turn the gravity architecture into a sequence of falsifiable mathematical and numerical contracts before full planetary fitting.

### Inputs

- declared field functional or control law;
- source strengths/masses;
- source/target geometry;
- common coefficients and boundary assumptions;
- explicit tolerances for compression/resolution.

### Outputs

- derived field/slope equations;
- candidate boundary radii;
- analytic closure residuals;
- numerical conservation residuals;
- direct versus compressed field residuals;
- machine-readable claim status.

### Forbidden shortcuts

- no hand-selected AU cutoff presented as derived;
- no zeroing distant influence merely because local dominance ended;
- no planet-specific tuning to rescue a failed law;
- no visual-orbit success criterion;
- no promotion of Newtonian control math to proof of a One-Wave substrate;
- no hiding source-to-inertial-mass proportionality inside an unexplained constant;
- no calling one exact three-body family a solution of the general three-body problem.

## Current load-bearing gap

The field-shape question is now partially closed mathematically under A-106's assumptions. The next hardest dependency is the **source/response coupling**:

```text
Why does a physical body source q in proportion to inertial mass,
and why does the receiving response use the same universal ratio?
```

Until that is derived or independently constrained, `K`, `q`, and measured mass cannot be identified by definition.

After that, the same fixed law must survive:

1. two-body controls;
2. exact and non-exact three-body trajectories;
3. hierarchical compression tests;
4. Solar-System ephemeris comparison;
5. relativistic controls.
