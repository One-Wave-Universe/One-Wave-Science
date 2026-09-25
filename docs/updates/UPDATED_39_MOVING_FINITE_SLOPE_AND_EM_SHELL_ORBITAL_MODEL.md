# Updated 39 — Moving Finite-Slope and EM-Shell Orbital Model

## Purpose

This update supersedes the memory/assimilation interpretation in Updated 38 for the current planetary test architecture.

The working One-Wave hypothesis is an **instantaneous moving network of body-specific finite displacement/slope regions**. Every body moves, every body's active range moves with it, and the range is determined by that body's own potential/slope relative to the surrounding reference state. No stored wake memory, relay memory, or universal cutoff radius is assumed.

This is a canonical **test architecture**, not a claim that the physical hypothesis has been established.

## Locked architectural rules

1. Every gravitating body has its own moving potential/slope profile.
2. Every profile has a body-specific finite active range; there is no universal planetary cutoff.
3. The active range is determined by slope/potential contrast against the current surrounding reference, not by an arbitrary AU radius.
4. All active regions are recomputed at every timestep as all bodies move.
5. A planet can speed up or slow down because the instantaneous combined slope geometry changes around it.
6. Intermediate planets matter because they have their own moving slope regions and are themselves being displaced by the combined system.
7. No memory or information-relay term is added to preserve a vanished interaction.
8. Electromagnetic structure is not treated as a direct gravity-like force. The current candidate role of EM is to modify the stability/stiffness/response of the local displacement shell.
9. Mercury receives an additional Sun–Mercury EM-coupling channel because its intrinsic magnetic shell is embedded much deeper in the solar magnetic environment.
10. Mars and Venus are controls for the absence of a present intrinsic global dipole: Mars has localized crustal magnetism; Venus has an induced magnetic environment but no Earth-like intrinsic global dynamo field.

## Instantaneous moving finite-slope field

For body i, define a candidate displacement potential

`Phi_i(r,t)`

and slope

`S_i(r,t) = |grad Phi_i(r,t)|`.

Its active domain is

`Omega_i(t) = { r : DeltaS_i(r,t) remains distinguishable from the current reference }`

where

`DeltaS_i(r,t) = S_i(r,t) - S_ref(r,t)`.

The finite-range boundary `R_i(t)` is therefore an emergent boundary condition of the field state, not a common hand-set cutoff.

The exact boundary functional is still to be derived. Candidate boundary tests may use gradient contrast, curvature contrast, displacement amplitude, or a combination constrained by the underlying lattice equations.

## Orbital update

At body i's current position, form the instantaneous active slope state from every body whose current domain overlaps that location:

`S_local,i(t) = SUM_j [ I(r_i in Omega_j(t)) * S_j(r_i,t) ]`

with `I` an activity indicator or a future smooth boundary weight derived from the finite-range law.

The relational driver is

`DeltaS_i(t) = S_local,i(t) - S_ref,i(t)`.

The orbital response is then written abstractly as

`a_i(t) = -F(DeltaS_i(t), K_i_eff(t))`

where `F` must ultimately be derived from the One-Wave field dynamics rather than fitted independently for every planet.

## EM shell role

The EM hypothesis is **shell stabilization / response modulation**, not direct magnetic propulsion.

For a body with a global intrinsic magnetic shell, define

`K_i_eff(t) = K_i0 * [1 + eta * C_i(t)]`

where `K_i0` is the body's baseline displacement-shell response and `C_i(t)` is a dimensionless EM-state variable constructed from independently measurable quantities.

A candidate generic structure is

`C_i(t) = G(B_sun(r_i,t), B_i(t), alignment_i(t), shell_geometry_i(t))`.

This term changes how the displacement shell responds to the local slope; it is not added as `F_mag / M`.

## Mercury special channel

Mercury uses

`K_Me_eff(t) = K_Me0 * [1 + eta*C_Me(t) + eta_SM*C_SM(t)]`

where `C_SM` is the extra Sun–Mercury magnetic coupling state.

The extra term is allowed because Mercury's intrinsic field is directly embedded in a much stronger and more rapidly varying solar magnetic environment than Earth's. It must nevertheless be computed from measurable Sun/Mercury field geometry rather than inserted as a free constant solely to reproduce Mercury's orbit.

Mercury's 3:2 spin-orbit resonance remains a gravitational/tidal control fact. The EM-shell term is not permitted to relabel that resonance without evidence.

## Earth

Earth has a present intrinsic global field, so

`K_E_eff(t) = K_E0 * [1 + eta*C_E(t)]`.

Earth is therefore a primary magnetized-rocky-planet comparison against Mercury.

## Mars

Mars has no present Earth-like global intrinsic dipole. For the first global-shell test,

`C_Mars_global(t) = 0`.

Localized crustal magnetic structure is retained for a later anisotropic correction rather than being promoted to a global shell.

Thus the first-pass Mars orbital response is

`a_Mars(t) = -F(DeltaS_Mars(t), K_Mars0)`.

## Venus

Venus has no present intrinsic global dipole comparable to Earth. Its induced magnetic environment is kept separate from an intrinsic-shell term.

First-pass:

`C_Venus_intrinsic(t) = 0`.

This makes Venus a second rocky control against Mercury and Earth.

## Giant planets

Jupiter, Saturn, Uranus, and Neptune possess intrinsic global magnetic fields and therefore receive nonzero EM-shell state variables. Their large magnetic moments are a crucial falsification test: a correct shell-stability law must not generate absurd orbital corrections merely because a planet has a large magnetic moment.

The law must depend on the actual shell/field geometry and the body's displacement response, not on magnetic moment alone.

## What the multi-planet fit already rules out

The current exploratory calculations rule out treating the magnetic term as a simple universal extra inward acceleration proportional only to magnetic strength or magnetic moment. Such a term cannot match the secular orbital pattern across Mercury, Earth, Jupiter, and the non-dipole rocky controls simultaneously.

Therefore the candidate EM effect is assigned to **shell response/stability**, while the moving finite-slope network remains responsible for the common orbital dynamics.

This separation is now architectural:

`ORBIT = moving finite slope geometry`

`EM = modifier of local shell integrity / stiffness / response`

not

`ORBIT = gravity + arbitrary magnetic gravity-like force`.

## Required full Solar-System test

Simulate at minimum:

- Sun
- Mercury
- Venus
- Earth + Moon
- Mars
- Jupiter
- Saturn
- Uranus
- Neptune

At every timestep:

1. update every body's state and position;
2. recompute every body's potential and slope profile;
3. recompute its current finite active range from the same boundary law;
4. determine which moving regions overlap every target body;
5. form each target's relational local-minus-reference slope;
6. compute each body's EM-shell state if it has an intrinsic global field;
7. add Mercury's independently defined Sun–Mercury coupling state;
8. update orbital motion;
9. compare with a standard high-quality ephemeris control.

## Falsification requirements

The candidate model must fail if any of the following occur:

- a single arbitrary cutoff is required for all planets;
- body-specific ranges must be tuned independently merely to force an orbital match;
- an EM coefficient must be independently tuned for every magnetized planet;
- Jupiter's large magnetic field produces an unobserved giant orbital correction;
- Mars or Venus require a fictitious global intrinsic magnetic shell to fit;
- Mercury's extra coupling is defined only after inspecting the residual it is supposed to explain;
- removing absolute coordinates merely rewrites ordinary N-body dynamics without producing a distinct finite-range closure law.

## Current locked model

`moving body-specific finite slope ranges`

`+ instantaneous overlap of those moving ranges`

`+ local minus reference slope`

`+ EM-dependent displacement-shell response for magnetized bodies`

`+ extra independently measurable Sun–Mercury coupling state`

`+ no memory`

`+ no universal cutoff`

`+ Mars/Venus global-intrinsic-field controls`

`+ full Solar-System ephemeris comparison`

## Claim status

YELLOW / candidate architecture.

The architecture is locked for the next numerical attack. The finite-range boundary law and EM-to-displacement-shell coupling law are not yet derived from first principles, and no new gravitational or electromagnetic effect is claimed as experimentally established.