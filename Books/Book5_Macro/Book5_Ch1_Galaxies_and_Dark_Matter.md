# ONE-WAVE FRAMEWORK
## Book 5 — Macro
## Chapter 1: Galaxies and the Extended Compression Effect / Dark-Matter Comparison

Version: 1.0 (draft)
Date: July 17, 2026
Class: B — Applied Layer
Spine: Gray / 2D / 3D / Mathematics / Predictions / Yellow Audit / Future Work / Closing Thoughts

Dependencies: A-115 Unified Compression Field, E-507 Scale-Invariant Loop,
              A-104 Gradient, A-105 Restoring Response, C-309 Friction Limit,
              Book 1 Ch12 Gravity, Book 1 Ch15 Higgs/Mirror Resonance
Status: YELLOW (field equations) / GREEN (galaxy identification and coefficient fit)

---

## Gray — Standard Model Reference

Galaxy rotation curves do not match visible mass. Stars at the edge of a galaxy orbit
faster than Newtonian gravity from visible matter alone predicts.
The standard explanation is dark matter: an unseen mass, roughly five times more
abundant than ordinary matter, interacting via gravity but not electromagnetically.
Dark matter halos are inferred from rotation curves, gravitational lensing, and
large-scale structure formation.
No dark matter particle has been directly detected despite decades of searching
(WIMPs, axions, and other candidates remain unconfirmed).
Alternative theories (MOND — Modified Newtonian Dynamics) modify gravity at low
acceleration instead of adding mass, with mixed success at different scales.

Standard Model strength: dark matter halos correctly predict rotation curves,
lensing patterns, and large-scale structure across a huge range of independent
observations.
Standard Model limitation: the dark matter particle itself has never been found.
Five decades of direct-detection experiments have returned null results.

---

## 2D One-Wave Interpretation

In 2D, a galaxy is a large vortex moving through the field.

Motion through the lattice displaces the surrounding field.
The displaced field does not simply return to rest — it forms a compression ring
around the moving structure, the same way a boat moving through water leaves a
wake.

At small scale (Book 1, Chapter 12), this compression ring is negligible —
too small to measurably add to a single mode's gradient field.
At galactic scale, the ring itself becomes large enough to matter.

The **Extended Compression Effect** is the One-Wave name for the "extra" gravity conventionally attributed to dark matter:
not an unseen particle, but the field's own displaced response to the galaxy's
motion and rotation.

---

## 3D One-Wave Interpretation

In 3D, a galaxy is a rotating field structure — many stellar-scale Persistent
Modes (Book 1) coupled together, riding inside one larger rotational pattern.

The same scale-invariance claim already stated in E-507 applies here without
modification: the same update rule governs the galaxy that governs a single
mode, with scale entering only through gamma(s) and beta(s) — a real, still-open
derivation this chapter inherits rather than solves.

The compression ring (Book 1 Ch12, A-115) scales with the moving structure's size
and speed. At galactic scale:

R_ring ~ R_gravity

rather than the R_ring << R_gravity relationship true at atomic scale.
This is not a new mechanism. It is the same displaced-field response, now large
enough to be comparable to the direct gradient force itself.

Rotation curves:
A star at the galaxy's edge feels both the direct gradient pull toward the
galactic core (A-105 Restoring Response, gradient form) and the compression-ring
contribution from the galaxy's own bulk motion and rotation. Standard Newtonian
gravity accounts only for the first. The observed "extra" velocity is the second,
previously uncounted.

No new particle is required. The ring is a field response, not a substance.

Open connection to spiral structure:
Spiral arms are the visible organization of this same rotating compression
pattern — dense regions where the ring's structure concentrates matter. This
chapter does not derive spiral arm structure; it is flagged as a natural
extension, not yet attempted.

---

## Mathematics

Compression ring contribution (from Book 1 Ch12, A-115, applied at galactic scale):

R_total = R_gravity + R_ring

R_ring ~ K_p * |nabla_psi_ring|^2 * Area

At micro scale (established, Book 1 Ch12):
R_ring << R_gravity

At galactic scale (this chapter, candidate — not yet derived from first
principles, only asserted by scale extrapolation):
R_ring ~ R_gravity

Scale dependence (inherited open problem, not solved here):
The transition from R_ring << R_gravity to R_ring ~ R_gravity depends on how
gamma(s) and beta(s) scale — the same unresolved derivation flagged in B-220
and E-507. This chapter does not derive the transition; it assumes it occurs
and describes the consequence.

Rotation curve candidate form (sketch — new, not previously stated anywhere
in the repo, flagged accordingly):
v(r)^2 / r = R_gravity(r)/m + R_ring(r)/m
where R_ring(r) grows relative to R_gravity(r) at large r, producing the
flattened rotation curve observed instead of the Keplerian falloff Newtonian
gravity alone predicts. This form is a plausibility sketch, not a derivation —
no functional form for R_ring(r) is given.

---


### Load-bearing A-115 formulation

A-115 replaces the dead I-09 address and makes the claim explicit:

```text
gravity = local directional response of the compression field
dark matter = extended/wake contribution of that same field
Higgs-like resistance = local boundary stiffness of that same field
```

For circular motion:

```text
v_c(r)^2 / r = |g_local(r) + g_wake(r)|
```

An ordinary gravity analysis would infer an effective extra density

```text
rho_DM,eff = -(1/(4 pi G_eff)) div(g_wake).
```

That is an observational translation, not a second One-Wave substance. The actual Yellow task is to derive `g_wake(r)` from the A-115 field equation with coefficients fixed independently of the galaxy being fit.

## Predictions

1. No dark matter particle will ever be found, because there isn't one.
Prediction: direct-detection experiments (WIMP searches, axion searches) will
continue returning null results indefinitely, because dark matter is a field
response, not a particle.

2. The ratio of "dark" to visible mass should correlate with rotational
velocity and structure size, not be a fixed universal ratio.
Prediction: galaxies with different rotation speeds or different structural
compactness should show different effective dark-to-visible mass ratios,
following from how R_ring scales with motion and size — not a constant fudge
factor. This is a real, checkable prediction against existing rotation-curve
data, not yet checked in this chapter.

3. The compression ring should be continuous with ordinary gravity, not a
separate substance with its own clustering behavior.
Prediction: dark matter "clumps" inferred from lensing should always be
co-located with a moving or rotating baryonic structure generating them — no
dark matter should exist detached from any baryonic source.

---

## Yellow Audit

- MASS-MECHANISM STATUS: C-318 permanently removes the false transport-to-mass shortcut and the substitution \(m_{\rm eff}=E_0/c^2\) as causal mechanisms. This chapter now requires one open A-115/C-318 bridge from the stable four-interaction stress profile to both the local Mass-Effect tensor and the far-field gravity-source amplitude. The galactic compression calculation cannot be promoted until that shared source mapping is closed.
- Rotation curve functional form is a plausibility sketch only — no derived
  R_ring(r), no fit to actual rotation curve data
- Transition from R_ring<<R_gravity (micro) to R_ring~R_gravity (galactic)
  is assumed, not derived — depends entirely on the still-unresolved
  gamma(s)/beta(s) scaling law shared with B-220 and E-507
- Spiral arm structure noted as a natural extension, not attempted
- No connection yet made to gravitational lensing observations specifically

---

## Future Work

Derive the A-115/C-318 mapping from one stable four-interaction recurrence to both the local Mass-Effect tensor and the far-field gravity-source amplitude before treating the chapter's gravitational Mass Effect as closed.
Derive gamma(s)/beta(s) scaling explicitly enough to justify the assumed
micro-to-galactic transition in R_ring, rather than asserting it by
extrapolation.
Fit the candidate rotation curve form against real observational data.
Extend to gravitational lensing and large-scale structure formation.
Attempt a derivation of spiral arm structure from the rotating compression
ring.

---

## Closing Thoughts

Dark matter has been searched for directly, underground, in ultra-cold
detectors, for fifty years, and found nothing. That is a real result, not
a failure of instruments. It is worth taking seriously as evidence, not
just as an inconvenience for particle physics to eventually overcome.

In One-Wave, the search comes up empty because there is nothing there to
find. The "missing mass" was never missing and never a substance — it was
the field's own displaced response to a galaxy's bulk motion, the same
compression ring that Book 1 already established at atomic scale, just
large enough at galactic scale to matter.

Whether that holds up depends entirely on whether the scale-dependence of
gamma and beta can actually be derived — not assumed, not extrapolated,
derived. That derivation does not exist yet. This chapter is a real,
structured claim sitting on top of a real, still-open problem. Both of
those things are true at once, and neither cancels the other out.

---

END OF BOOK 5 CHAPTER 1 (DRAFT)
One wave. Mirror builds.
