# 08 — Finite-Slope Sieve Boundary and Assimilation Proof Target

## Purpose

Turn the surviving `Updated 38 -> 39 -> 40 -> 41` planetary chain into a falsifiable mathematical target.

This document does **not** claim a new law of gravity. It separates what can already be proved under the standard inverse-square control from what the One-Wave model still has to derive from its own substrate equations.

The central correction is:

> **Finite resolution is not the same thing as finite influence.**

The useful version of the sieve idea is therefore:

`explicit local structure -> derived resolution/dominance boundary -> parent-field compression -> reopen explicit structure when required by error/geometry`

not

`body field -> arbitrary radius -> zero influence outside radius`.

---

## 1. Attack the simplest finite-boundary candidate

Let a local body of mass `m` sit a distance `R` from a parent body of mass `M`.

Under the standard inverse-square control,

`g_local(r) = G m / r^2`

and the parent field magnitude at the local body's center is

`g_parent(R) = G M / R^2`.

If distinguishability is defined by equality of those **magnitudes**,

`G m / r^2 = G M / R^2`,

then

`r_absolute = R sqrt(m/M)`.

For Earth relative to the Sun this is about

`r_absolute ~= 2.59e8 m = 259,000 km`.

The Moon's mean orbital radius is about

`3.844e8 m = 384,400 km`.

Therefore the simple absolute-background crossing would place the Moon outside Earth's independently resolved domain.

### Result A

**FAIL as a general physical boundary rule.**

The reference comparison cannot simply be `local slope magnitude versus parent slope magnitude` if the boundary is supposed to track local binding/dominance structure.

---

## 2. Use the local change in the reference slope

The One-Wave architecture repeatedly uses a local-minus-reference differential. Under an inverse-square control, the first radial change of the parent field across a small local distance `r` is

`|delta g_parent| ~= 2 G M r / R^3`.

In a circular rotating-frame/Hill control, the effective linear stretching coefficient is `kappa = 3`, giving

`delta g_reference ~= kappa G M r / R^3`.

Set the local body's inward slope equal to that local reference change:

`G m / r^2 = kappa G M r / R^3`.

Cancel `G` and solve:

`r^3 = (m / (kappa M)) R^3`

so

`r_differential = R (m / (kappa M))^(1/3)`.

For Earth-Sun with `kappa = 3`,

`r_differential ~= 1.497e9 m = 1.497 million km`.

That contains the lunar orbit.

### Result B

**PASS as a derived standard-control dominance boundary.**

The cube-root boundary is not a hand-selected AU cutoff. It follows from the collision of two different scalings:

- local inverse-square slope: `~ r^-2`;
- local parent differential/tidal slope: `~ r`.

Their equality forces a finite `r^3` crossing.

This is closely related to the standard Hill/tidal-dominance construction. That connection is a strength for the control test, not evidence of new One-Wave physics.

---

## 3. Do not turn the dominance boundary into a hard influence cutoff

A Hill-like/differential boundary tells us where local structure dominates or can be treated as an independently bound subsystem. It does **not** mean the body's field becomes exactly zero outside that radius.

Jupiter's Sun-relative differential/Hill-like boundary is about `5.32e10 m` (roughly 53 million km), while the nominal difference between Jupiter's and Earth's mean orbital radii is roughly `6.29e11 m`.

A hard rule such as

`if distance > R_active: contribution = 0`

would therefore remove Jupiter's direct contribution at Earth in this simple control geometry.

That is not an acceptable representation of the standard N-body control.

### Result C

**FAIL for hard finite-influence cutoff.**

The finite boundary may be a **resolution, dominance, or state-transition boundary**, but not a disappearance boundary unless a new physical law independently derives and validates that behavior.

---

## 4. Mathematical sieve: hierarchical parent-field assimilation

There is a rigorous standard-control version of the sieve idea.

Take a source cluster with bodies `m_k` at offsets `x_k` around their center of mass `c`. Let

`a = max |x_k - c|`

be the cluster radius, and evaluate the field at a target a distance

`R = |x_target - c|`

from the cluster center, with `a < R`.

For the Newtonian potential,

`Phi(x) = -G SUM_k m_k / |x - x_k|`,

the far field admits a convergent multipole expansion in powers of `a/R`.

If the expansion origin is the center of mass, the dipole moment vanishes. The first omitted correction after the monopole is then generically quadrupolar.

Therefore the parent monopole representation

`M_parent = SUM_k m_k`

located at the center of mass has far-field relative error scaling as

`error = O((a/R)^2)`

for a center-of-mass-centered bounded cluster, with higher multipole moments reducing the error further.

This gives a precise meaning to assimilation:

`many locally resolved sources -> finite parent state + controlled residual`.

The source information has not vanished. It has been compressed into the moments required at the current observation scale.

### Result D

**PASS as a standard mathematical compression theorem.**

This proves that a many-body field can be represented hierarchically without evaluating every internal source as an independently resolved object at every distant location, provided the geometry and retained error tolerance permit the compression.

It does **not** prove a superfluid substrate or a new gravitational law.

---

## 5. The corrected sieve architecture

The logically consistent architecture is now:

1. **Local explicit state** — keep nearby bodies/structures explicitly resolved.
2. **Reference differential** — compare local structure to the spatial change/curvature of the surrounding reference, not merely its absolute magnitude.
3. **Derived dominance boundary** — a finite local boundary can emerge from the equations; for the inverse-square control this gives the cube-root/Hill-like scaling.
4. **Assimilation, not deletion** — outside an independent-resolution region, fold resolvable source structure into a parent representation rather than setting its influence to zero.
5. **Error-controlled reopening** — if a target is too near the source group, inside its bounding region, or requires higher accuracy, reopen the parent and resolve children/higher moments.

This is the mathematically defensible form of the "sand in a sieve" idea:

`fine structure -> sieve boundary -> coarser parent structure -> finer structure reopened when needed`.

---

## 6. What this closes in Updated 38-41

### Updated 38

The missing assimilation criterion is narrowed. Absolute slope magnitude is rejected. A local differential/tidal criterion is a valid standard-control candidate for **dominance/resolution**.

### Updated 39

The "moving body-specific finite range" must not be interpreted as a hard zero-influence radius. If Updated 39 keeps "no memory", assimilation must be instantaneous state compression/reference construction, not stored wake memory.

### Updated 40-41

Point-Path-Field and planetary displacement states can use the same hierarchy:

`explicit local P/P/F state -> parent compressed field state -> reopen children when local geometry requires it`.

This gives the recursive architecture a measurable mathematical contract instead of only a naming hierarchy.

---

## 7. One-Wave theorem still required

To upgrade this from a standard-control proof to a One-Wave physical result, the repo still needs a derived One-Wave field/update law.

That law must show, without planet-by-planet fitting:

1. the local slope law;
2. the reference-state construction;
3. why a finite resolution/state boundary exists;
4. what information crosses that boundary into the parent state;
5. an error or conservation bound for that compression;
6. how/when a compressed parent reopens into explicit child relations;
7. at least one prediction or compression property not obtained merely by rewriting Newtonian N-body dynamics.

If the derived law reduces exactly to ordinary multipole Newtonian gravity, the result is still a useful hierarchical solver/representation, but it is not new gravitational physics.

---

## 8. Executable receipt

The companion bench is:

`One_Wave_Bench/gravity/finite_slope_sieve_bench.py`

Tests:

`One_Wave_Bench/gravity/test_finite_slope_sieve_bench.py`

Run:

```bash
python One_Wave_Bench/gravity/finite_slope_sieve_bench.py
python One_Wave_Bench/gravity/finite_slope_sieve_bench.py --json
python -m unittest One_Wave_Bench/gravity/test_finite_slope_sieve_bench.py -v
```

The bench attacks both boundary interpretations and measures far-field parent-compression error.

---

## Current proof ledger

| Statement | Status |
|---|---|
| Absolute parent-slope crossing is the physical finite boundary | **FAIL** |
| Local differential/tidal balance yields a finite cube-root dominance boundary | **PASS under inverse-square standard control** |
| Hill-like boundary can be used as hard zero-influence cutoff | **FAIL** |
| Distant bounded source structure can be compressed into parent multipoles with controlled error | **PASS under Newtonian standard control** |
| One-Wave substrate independently derives the same-or-better hierarchy | **INCONCLUSIVE** |
| One-Wave gravity / three-body problem solved | **NOT CLAIMED** |

## Highest-value next attack

Derive the **local slope/update equation from the Ground/lattice model** strongly enough that the finite-boundary and parent-compression machinery can be rerun without inserting Newton's inverse-square law as the starting assumption.
