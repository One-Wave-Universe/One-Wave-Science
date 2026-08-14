# Updated 41 — Planetary-Scale Displacement Model

## Purpose

This update supersedes the narrower orbital framing of Updated 39/40. The working One-Wave planetary hypothesis is that a planet is a **planetary-scale displacement structure**, analogous in architecture to the lower-scale displacement structures used elsewhere in the framework. Orbit, gravity-like response, field range, spin behavior, tides, EM-shell behavior, internal stress, and stability are treated as outputs of the same coupled displacement state rather than as separate mechanisms patched together afterward.

This is a canonical **test architecture**, not an experimentally established replacement for standard planetary physics.

## Core rule

A planet is not represented by mass plus an orbit. Its state is the current interaction of internal compression, recursive rotation, EM circulation, density/phase structure, neighboring displacement fields, and the surrounding reference field.

Define the planetary displacement state

`D_planetary,i(t) = F[L2D_i, P_i(P,Pa,F), Pa_i(P,Pa,F), F_i(P,Pa,F), rho_i(r), phase_i(r), EM_i, neighbors_i, S_ref_i]`

where Point, Path, and Field are each recursively Point–Path–Field.

The external observables are derived from this state:

`D_planetary -> active range / slope profile / orbital response / spin response / tidal response / EM-shell behavior / internal stress / stability`

No single variable is the cause by itself. The physical state is the interaction pattern.

## 1. Two-dimensional bound/compressed layer

The planetary state begins with the compressed/bound lattice layer rather than with a point-mass orbit.

Define

`L2D_i = {C_i, T_i, gamma_i, Q_i, Omega_i}`

where:

- `C_i` = local compression/binding state;
- `T_i` = effective lattice tension/stiffness;
- `gamma_i` = damping/shear/friction state;
- `Q_i` = integrity/bound-state variable;
- `Omega_i` = circulation/rotation state of the bound structure.

The working hypothesis is that the bound/compressed state produces and constrains the higher-dimensional rotating displacement structure.

A generic coupling form is

`dL2D_i/dt = G(compression, shear, internal flow, EM state, neighboring gradients, reference state)`.

This layer must not be replaced by an arbitrary scalar gravity parameter.

## 2. Recursive Point–Path–Field state

Every planetary scale carries the full nested 3 x 3 Point–Path–Field structure:

- `PP` — point within point
- `PPa` — path within point
- `PF` — field within point
- `PaP` — point within path
- `PaPa` — path within path
- `PaF` — field within path
- `FP` — point within field
- `FPa` — path within field
- `FF` — field within field

These are not nine independent corrections. They are coupled views/states of one displacement system.

### POINT(P,Pa,F)

The planetary POINT includes the actual internal structure of the body:

- density profile;
- solid and liquid layers;
- inner core / outer core where applicable;
- mantle or deep-fluid circulation;
- whole-body rotation;
- differential rotation between layers;
- conducting-fluid rotation;
- internal current circulation;
- internally generated magnetic field;
- internal EM-field rotation;
- thermal/phase state;
- internal shear and damping.

A first state vector is

`P_i = {rho(r), phase(r), Omega_core, Omega_fluid, Omega_mantle, Omega_body, Omega_EM, J_internal, B_internal, gamma_internal, T_internal}`.

### PATH(P,Pa,F)

PATH is not merely the geometric orbit. It contains:

- the instantaneous planetary state along its trajectory;
- orbital/path rotation and changing speed;
- motion through the surrounding displacement structure;
- the deformation/wake geometry produced along that motion;
- phase relation between body spin and path rotation;
- coupling to neighboring planetary displacement states.

`Pa_i = {r_i, v_i, Omega_path_i, phase_path_i, DeltaS_path_i, overlap_i}`.

### FIELD(P,Pa,F)

FIELD contains:

- the local displacement-field center/reference;
- field circulation;
- finite active displacement region;
- orientation and rotation of the displacement shell;
- EM-shell geometry;
- overlap with solar and neighboring planetary fields;
- the larger parent-field relation.

`F_i = {Phi_i, gradPhi_i, curvature_i, R_active_i, Omega_field_i, phase_field_i, EM_shell_i, S_ref_i}`.

## 3. Rotation is primary

Rotation is not a small correction. The planetary displacement state depends strongly on rotational relations.

At minimum calculate:

`Omega_body`

`Omega_core`

`Omega_conducting_fluid`

`Omega_EM_internal`

`Omega_path`

`Omega_field`

and all physically relevant relative rotations, e.g.

`DeltaOmega_core-mantle = Omega_core - Omega_mantle`

`DeltaOmega_matter-EM = Omega_matter - Omega_EM`

`DeltaOmega_point-field = Omega_point - Omega_field`

`DeltaOmega_spin-path = Omega_body - Omega_path`.

These relative rotations generate shear, phase changes, induction/dynamo behavior, and candidate lattice softening/stiffening.

A generic shear/damping channel is

`P_shear ~ gamma * (DeltaOmega)^2`.

This is a state-change term, not ordinary surface friction.

## 4. Internal EM rotation

Internal EM rotation is a distinct but coupled part of the POINT state.

For conducting interiors, calculate together:

- motion of conducting material;
- electrical-current circulation `J_internal`;
- internal magnetic field `B_internal`;
- rotation/orientation of that field;
- magnetic back-reaction on conducting flow;
- resulting shell geometry.

The architecture is

`conducting-flow rotation -> current circulation -> internal B field -> EM-field rotation -> external EM shell`

with feedback from the EM field back into the conducting flow.

The One-Wave hypothesis under test is that this EM state also changes the local bound-lattice/displacement response.

## 5. Planetary active range is an output

A body's displacement range is not assigned first and then corrected for spin or EM.

It is derived from the complete current state:

`R_active_i(t) = R[L2D_i, D_i, rho_i(r), P_i(P,Pa,F), Pa_i(P,Pa,F), F_i(P,Pa,F), EM_i, DeltaS_surroundings]`.

The active region is

`Omega_i(t) = {x : the body's displacement/slope structure remains distinguishable from the current surrounding reference}`.

No universal AU cutoff is allowed.

No stored wake memory or relay mechanism is required in this architecture. All fields/ranges move with their bodies and are recomputed from the current state.

## 6. Planet-to-planet interaction

Every body modifies and is modified by the current overlapping displacement geometry.

At target body `i`:

`S_local_i(t) = H({state_j(t), Omega_j(t), geometry_ij(t)} for all active j)`

and

`DeltaS_i(t) = S_local_i(t) - S_ref_i(t)`.

The next planetary state follows from the entire coupled state:

`X_i(t+dt) = U[X_i(t), DeltaS_i(t), overlaps_i(t)]`

where

`X_i = {L2D_i, PP_i, PPa_i, PF_i, PaP_i, PaPa_i, PaF_i, FP_i, FPa_i, FF_i, EM_i}`.

The orbital trajectory is only one projection of this update.

## 7. What is derived rather than inserted

The solver should derive, from the planetary displacement state:

- effective local slope/well;
- finite active range;
- orbital acceleration and speed changes;
- apsidal/nodal changes;
- point/spin response;
- field orientation/rotation;
- tidal response;
- internal stress/shear;
- shell stability;
- EM-shell modulation.

These are not independent free-force terms.

## 8. EM-shell role

EM does not enter as a generic gravity-like force.

Instead define an EM-dependent shell/bound-state response:

`K_eff_i = K0_i * M_EM_i(P_i, Pa_i, F_i, B_internal_i, B_external_i, alignment_i)`.

The EM term can alter:

- bound-state stiffness;
- local compression response;
- shell integrity;
- rotational coupling;
- active range/gradient shape;
- response to external displacement slopes.

This must be constrained by independently measurable magnetic/interior quantities rather than fitted separately for each planet.

## 9. Mercury special coupling

Mercury has:

- a conducting/internal dynamo state;
- an intrinsic magnetic field;
- 3:2 spin-orbit resonance as the standard control fact;
- strongly changing orbital/path rotation through its eccentric orbit;
- much deeper immersion in the Sun's magnetic environment than Earth.

Therefore its displacement state includes an extra Sun–Mercury EM relation:

`C_SM(t) = C[B_sun(r,t), B_Me(t), relative orientation, shell geometry, Omega_point, Omega_path, Omega_field]`.

This term modifies Mercury's displacement-shell state; it is not assumed to be a direct magnetic propulsion force.

## 10. Earth

Earth's planetary displacement state must explicitly include:

- solid inner core;
- conducting liquid outer core;
- mantle circulation;
- whole-body rotation;
- differential core/mantle rotation;
- geodynamo current circulation;
- intrinsic global magnetic field;
- rotating global EM shell;
- Moon coupling;
- solar and planetary overlap.

Earth is therefore not modeled as a rigid point mass with an optional magnetic correction.

## 11. Mars and Venus controls

Mars currently has no Earth-like global intrinsic dynamo field, though it has localized crustal magnetism. Venus has no comparable present intrinsic global dipole.

They remain critical controls because their planetary displacement states retain internal rotation, path rotation, field rotation, compression, thermal structure, and external interactions while lacking an Earth-like global intrinsic magnetic shell.

The model must not invent a global magnetic shell for either body merely to force an orbital match.

## 12. Giant planets

Jupiter, Saturn, Uranus, and Neptune are essential stress tests because their internal-fluid, rotation, and magnetic structures are very different from the rocky planets.

Especially for Jupiter and Saturn, the state must include rapid internal rotation, conducting fluid/metallic-hydrogen regions, large current systems, strong global magnetic fields, and differential internal rotation.

A correct law must not equate 'larger magnetic moment' with a proportionally larger gravity-like orbital correction.

## 13. Scale analogy

The planetary architecture deliberately mirrors the lower-scale displacement architecture:

`lower-scale persistent displacement structure <-> planetary persistent displacement structure`.

The claim is not that an atom and a planet are materially identical. The claim under test is that the same recursive interaction grammar — bound state, Point–Path–Field, rotation, shell response, local/reference differential — can operate across scale.

## 14. Numerical implementation rule

At every timestep, for every body:

1. update the 2D bound/compressed state;
2. update all nine recursive Point–Path–Field components;
3. update internal material/fluid rotations;
4. update internal current and EM rotation;
5. update whole-body point spin;
6. update path/orbital state;
7. update field rotation/orientation;
8. compute current EM-shell state;
9. compute the body's current displacement slope/profile;
10. derive its finite active range from that full state;
11. calculate instantaneous overlaps with every other active body;
12. calculate local-minus-reference displacement state;
13. update the full planetary state;
14. only then read out orbit, spin, field, tide, stress, and stability observables.

The solver must not start with a preselected orbit and then attach displacement language afterward.

## 15. Ablation tests

To identify which interactions matter, run the same system while disabling one channel at a time:

- internal differential rotation off;
- internal EM/current rotation off;
- 2D damping/shear off;
- point rotation off;
- path rotation coupling off;
- field rotation coupling off;
- EM-shell response off;
- Mercury Sun-coupling off;
- finite-range boundary off;
- neighboring-body overlaps removed one body at a time.

Measure changes in all output channels, not only orbit.

## 16. Falsification requirements

The architecture fails or must be revised if:

- the same rule cannot operate across planets without body-by-body arbitrary coefficients;
- rotation variables do not improve predictions beyond a simpler model;
- the EM-shell law generates contradictions for giant planets or no-dipole controls;
- the finite-range law cannot reproduce observed multi-body dynamics;
- the 2D bound-state variables are mathematically redundant and add no predictive content;
- the recursive Point–Path–Field state merely renames standard state variables without producing compression, prediction, or a distinct measurable residual.

## Locked planetary-scale statement

`PLANET = persistent planetary-scale displacement structure`

`PLANETARY STATE = 2D bound/compressed state + recursive Point–Path–Field + internal material/fluid rotation + internal current/EM rotation + path rotation + field rotation + instantaneous neighboring/reference interactions`

`ACTIVE RANGE = output of the full current planetary displacement state`

`ORBIT / GRAVITY-LIKE RESPONSE / SPIN / TIDES / EM SHELL / STRESS / STABILITY = readouts of that state`

`NO universal cutoff`

`NO memory relay`

`NO mass-only well`

`NO bolt-on magnetic gravity force`

## Claim status

YELLOW / candidate architecture.

This update locks the planetary-scale displacement architecture for implementation and testing. It does not claim experimental confirmation of a superfluid-lattice substrate or a replacement for standard gravitational, geophysical, or electromagnetic theory.