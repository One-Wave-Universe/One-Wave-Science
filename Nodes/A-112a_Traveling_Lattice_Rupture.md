---
node_id: "A-112a"
canonical_name: "Traveling Lattice Rupture"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Scale-Specific Persistent-Mode Formalization"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node A-112a: Traveling Lattice Rupture

Dependencies:
Upstream: A-112 Persistent Mode, A-102 Displacement, A-104 Gradient,
A-105 Restoring Response, B-203 Expression, B-204 Compression,
B-209 Break Condition, E-509 Propagation Limit
Downstream: Book 5 Ch4 Black Holes and Quasars, future lattice-defect simulation,
future moving-boundary measurements

## Scope

This node formalizes one narrow claim:

> A localized rupture can relocate through the lattice without creating an
> indefinitely lengthening permanent tear, provided rupture content is
> transported forward while the previous location re-closes.

This is a kinematic Yellow model. It does not yet derive black-hole motion from
first-principles One-Wave field dynamics.

## State Variable

For lattice site `i` and discrete step `n`, define

```text
r_i^n in [0,1]
```

as local rupture occupancy:

- `r=0` intact closure,
- `0<r<1` strained or partially open,
- `r=1` fully active rupture in the normalized model.

Let lattice spacing be `Delta x` and step duration be `Delta t`.

## Conservative Relocation Rule

For right-moving transport, define rupture flux

```text
J_(i+1/2)^n = nu_n r_i^n
```

and update by flux balance:

```text
r_i^(n+1) = r_i^n + J_(i-1/2)^n - J_(i+1/2)^n
          = r_i^n - nu_n(r_i^n-r_(i-1)^n).
```

Here

```text
nu_n = v_n Delta t / Delta x
```

is the dimensionless transport number.

For left-moving transport, reverse the upwind direction.

## Stability Bound

The first-order transport update remains a convex combination

```text
r_i^(n+1) = (1-nu)r_i^n + nu r_(i-1)^n
```

when

```text
0 <= nu <= 1.
```

Therefore the update preserves `0 <= r <= 1` without generating new extrema.
The bound is the discrete propagation condition for this minimal model.

At `nu=1`, the profile shifts exactly one site per step:

```text
r_i^(n+1) = r_(i-1)^n.
```

The defect shape and width are exactly preserved in that ideal shift case.

## Rupture Conservation

Define total rupture content

```text
R_n = sum_i r_i^n.
```

Under periodic boundaries or zero net boundary flux:

```text
R_(n+1)-R_n
= sum_i (J_(i-1/2)-J_(i+1/2))
= 0.
```

The flux terms telescope. Therefore

```text
R_(n+1) = R_n.
```

This is the mathematical form of

```text
the rupture relocates; it does not accumulate.
```

## Opening Ahead and Reclosure Behind

Define positive opening and closing rates:

```text
O_i^n = [r_i^(n+1)-r_i^n]_+
C_i^n = [r_i^n-r_i^(n+1)]_+.
```

For a right-moving localized profile:

- `O_i` is concentrated at the forward edge,
- `C_i` is concentrated at the rear edge.

Because total rupture is conserved:

```text
sum_i O_i^n = sum_i C_i^n
```

for each closed-system step. The amount opened ahead equals the amount reclosed
behind.

## Velocity and Acceleration

For a defect with nonzero total rupture, define center of rupture

```text
x_c^n = Delta x * (sum_i i r_i^n) / R_n.
```

Measured velocity is

```text
v_n = (x_c^(n+1)-x_c^n) / Delta t.
```

Constant `nu` gives constant nominal velocity. Acceleration requires changing
`nu_n`:

```text
a_n = (v_(n+1)-v_n) / Delta t.
```

The physical law that determines `nu_n` from pressure asymmetry remains open.

## Permanent Scar Variable

Rupture occupancy and irreversible damage are separate variables. Define

```text
d_i^n in [0,1]
```

as persistent structural damage, with update

```text
d_i^(n+1) = clip(
  d_i^n
  + kappa_d [r_i^n-r_damage]_+ (1-d_i^n)
  - lambda_d d_i^n,
  0,1).
```

Interpretation:

- `r_damage` = damage threshold above ordinary transported rupture,
- `kappa_d` = scar-formation rate,
- `lambda_d` = repair rate.

Behind a passing defect where `r -> 0`:

```text
d_i^(n+1) = (1-lambda_d)d_i^n.
```

Thus:

- `lambda_d > 0` gives repair and decay of damage,
- `lambda_d = 0` preserves any scar permanently,
- ordinary travel creates no scar when `r < r_damage`.

This distinguishes a traveling rupture from a propagating fracture.

## Width and Wake Measures

For occupancy threshold `r_c`, define defect width

```text
W_n = Delta x * count{i : r_i^n >= r_c}.
```

Define scar length

```text
L_scar^n = Delta x * count{i : d_i^n >= d_c}.
```

A stable traveling rupture should satisfy approximately

```text
R_n constant,
W_n bounded,
L_scar^n not growing.
```

A propagating fracture is identified by sustained growth of `L_scar`.

## Boundary Conditions

The conservation proof holds for:

1. periodic boundaries, or
2. closed boundaries with zero rupture flux.

Open boundaries allow rupture content to enter or leave and must report the net
flux explicitly.

## Internal Consistency Checks Completed

1. **Bounded state:** `0<=nu<=1` preserves normalized occupancy bounds.
2. **Conservation:** total rupture is constant under closed boundaries.
3. **Simultaneous exchange:** opening ahead equals closure behind.
4. **No automatic scar:** damage is a separate thresholded variable.
5. **Constant speed:** fixed `nu` produces fixed nominal transport speed.
6. **Acceleration:** changing `nu` changes the defect velocity rather than its
   required total rupture.

These results promote the relocation claim from Green description to Yellow
mathematical model.

## Falsification Conditions for the Yellow Model

The current model fails its own intended purpose if a later implementation shows
any of the following under the stated conditions:

- total rupture grows with distance despite closed boundaries,
- opening and reclosure do not balance,
- bounded initial data generate values outside `[0,1]` for `0<=nu<=1`,
- a permanent scar grows when the damage threshold is never crossed,
- the measured center does not move at the transport velocity.

## Yellow Audit

- The transport number `nu` is prescribed, not derived from One-Wave pressure
  and restoring-response equations.
- First-order transport introduces numerical diffusion for `0<nu<1`; a Bronze
  implementation should compare exact-shift, higher-order, and conservative
  schemes.
- The rupture field has not been tied to measured black-hole quantities.
- The structural-damage law is a candidate model requiring calibration.
- Bronze requires reproducible simulation code, metadata, parameter sweeps,
  graphs, and recorded failures.
