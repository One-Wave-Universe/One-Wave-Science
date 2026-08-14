# Updated 38 — Finite-Wake Three-Body Perturbation Architecture

## Purpose

This update captures the current One-Wave attack on the celestial three-body problem without promoting unproved interpretation to established physics.

The target is not merely to produce visually plausible orbits. The target is to test whether a system can be advanced from relational information alone, without requiring absolute location as a primitive, while also enforcing the One-Wave finite-wake hypothesis rather than summing independent gravitational wells to infinity.

## Claim status

- **Standard-control facts:** planetary orbital motion is perturbed by other massive bodies; Jupiter is a major source of Solar-System perturbations; Mercury is in a 3:2 spin-orbit resonance and possesses an intrinsic magnetic field/magnetosphere.
- **One-Wave hypotheses under test:** gravitational influence is a finite displacement/wake in a medium; local wakes are assimilated into larger parent fields; relational slopes can replace absolute-position primitives; Mercury's high-speed, eccentric, magnetically active environment may expose additional medium-displacement behavior.
- **Not yet established:** a finite-wake cutoff law, a non-locality theorem, a unique superfluid-chaos signature, or a derivation that outperforms standard celestial mechanics.

## Core relational rule

For a directed relation between systems i and j, use the architectural differential

`CHANGE_ij = LOCAL_SLOPE_i - REFERENCE_SLOPE_j`

or, in field notation,

`Delta_ij = grad(Phi_i) - grad(Phi_j)`

with the warning that this is currently a candidate relational update language, not yet a completed force law.

The important requirement is that the state of the system be represented by relations/edges rather than by assigning each body a privileged absolute location.

## Three-body relational graph

For Sun (S), Earth (E), and Moon (M), retain the three pair relations

- S-E
- E-M
- M-S

and require consistency around the closed relational loop.

A closure identity that follows algebraically from pair differences is only a bookkeeping identity. It is **not** evidence for new physics. Any useful three-body result must make a non-tautological prediction about evolution, stability, residuals, or a measurable boundary condition.

## Finite-wake rule

The One-Wave working hypothesis is

`local wake -> assimilation boundary -> parent reference field`

rather than

`standalone body field -> infinity`.

A body's wake therefore remains independently resolved only while its displacement/gradient/phase structure remains distinguishable from the surrounding parent field.

The missing mathematical object is an assimilation criterion. Candidate quantities include:

- displacement amplitude relative to parent background;
- gradient contrast;
- phase coherence;
- curvature contrast;
- scale ratio;
- a hysteretic combination of the above.

No cutoff radius is to be inserted ad hoc merely to fit orbital data.

## Jupiter perturbation test

The Sun-Earth-Moon system is the base relational test. Jupiter is then added as a controlled perturbing source.

Architecturally,

`Delta_SE(t) = Delta_parent(t) + delta_J(t) + delta_other(t)`

but `delta_J` is not assumed to be an infinite independent field. Under the finite-wake hypothesis it must become assimilated into the Solar reference when its independently resolvable contrast falls below the derived assimilation criterion.

### Required comparison

1. Reproduce the Sun-Earth-Moon baseline.
2. Add Jupiter using the same rule set.
3. Predict the timing and sign of Jupiter-induced changes before tuning against residuals.
4. Compare against a standard high-quality ephemeris/control solution.
5. Measure whether the finite-wake model introduces systematic errors or a distinct improvement.

Planetary speeding/slowing must be decomposed into:

- ordinary Keplerian perihelion/aphelion speed variation;
- standard multi-body perturbation;
- any additional One-Wave residual.

The model fails this test if it labels ordinary orbital variation as a new wake effect.

## Mercury stress test

Mercury is treated as a separate high-stress environment because several effects overlap strongly:

- short orbital period and high orbital speed;
- large eccentricity relative to the other major planets;
- 3:2 gravitational spin-orbit resonance;
- intrinsic magnetic field and magnetosphere;
- strong and varying solar-wind interaction.

The 3:2 lock is **not** to be relabeled as an electromagnetic lock without evidence. Standard gravitational/tidal spin-orbit resonance remains the control explanation.

The One-Wave test is instead whether Mercury shows a reproducible residual correlated with variables that a medium-displacement hypothesis specifically predicts, after standard gravitational and electromagnetic/plasma effects are removed.

Candidate decomposition:

`Observed_Mercury = orbital + spin_resonance + planetary_perturbations + solar_GR/control + EM/plasma + candidate_medium_residual`

The candidate residual must be specified before fitting.

## Test ladder

### Stage 1 — Two-body control

Sun-Earth and Earth-Moon separately. Recover ordinary bounded orbital behavior and expected speed variation.

### Stage 2 — Relational three-body system

Sun-Earth-Moon using only relational edge states plus explicitly declared scale reference. Demonstrate that no hidden absolute coordinate is required for the update.

### Stage 3 — Closure attack

Prove which closure relations are tautologies and remove them from the evidence ledger. Search for a non-tautological invariant, stability condition, or evolution constraint.

### Stage 4 — Jupiter perturbation

Add Jupiter and compare predicted phase/timing/amplitude of perturbations against ephemeris data.

### Stage 5 — Finite-wake boundary

Derive the assimilation boundary from the field equations or state-transition rules. Do not choose a cutoff radius by hand.

### Stage 6 — Mercury stress test

Run Mercury with gravitational, relativistic, spin-resonance, magnetic, and plasma controls separated. Test for a predeclared One-Wave residual.

## Non-locality theorem target

The desired theorem is stronger than a coordinate rewrite.

A successful result would show that:

1. the complete state required to advance the N-body subsystem can be represented by a finite set of relational states and nested scale-boundary variables;
2. the update law closes on those variables;
3. no privileged absolute position is required;
4. distant influence enters through finite assimilated boundary state rather than an infinite list of independently evaluated wells;
5. the formulation produces testable predictions that differ from, or compress without loss, the standard description.

If the equations merely reconstruct ordinary Cartesian N-body dynamics in disguised coordinates, that is mathematically useful but not a new physical result.

## Immediate implementation target

Build a minimal numerical bench with two simultaneous tracks:

- **Control track:** standard Newtonian/relativistic ephemeris-quality dynamics appropriate to the selected test.
- **One-Wave track:** relational edges + nested reference field + candidate finite-wake assimilation rule.

Both tracks must emit machine-readable residuals for position-equivalent relations, velocity change, phase, energy/angular-momentum bookkeeping, and boundary transitions.

No visual success criterion is sufficient.

## Current status

`relational mechanism -> candidate edge equations -> closure attack -> finite-wake law missing -> perturbation tests -> theorem target`

This update promotes the architecture and test program only. It does **not** claim the celestial three-body problem or gravitational non-locality has been solved.
