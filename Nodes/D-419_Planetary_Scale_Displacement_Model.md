---
node_id: "D-419"
canonical_name: "Planetary-Scale Displacement Model"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Resonance, Modal & Dimensional Structure / Planetary-Scale Displacement Lineage"
claim_gate_detail: "YELLOW (locked candidate architecture for implementation and testing; does not claim experimental confirmation of a superfluid-lattice substrate or a replacement for standard gravitational, geophysical, or electromagnetic theory)"
metadata_standard: "I-06"
---

# Node D-419: Planetary-Scale Displacement Model

## Dependencies

Upstream: D-416, D-417, D-418, A-101, A-102, A-103, A-104, A-105, A-106,
A-107, A-109, A-112, A-112a, A-115, A-116, A-117, B-206a, B-206b, B-216,
B-220, C-303, C-307, C-310, C-311, C-313, C-317, C-318, D-401, D-402,
D-404, D-405, D-408, D-409, D-410, D-412, D-413.

Implementation bench: D-415.

Authority and full engineering contract:
`UPDATED_41_PLANETARY_SCALE_DISPLACEMENT_MODEL.md`.

## Definition

D-419 is the current, locked planetary-scale test architecture and
supersedes the narrower orbital framing of D-417/D-418. A planet is not
mass plus an orbit; it is a planetary-scale displacement structure,
architecturally analogous to the lower-scale displacement structures
used elsewhere in the framework. Orbit, gravity-like response, field
range, spin behavior, tides, EM-shell behavior, internal stress, and
stability are outputs of one coupled displacement state, not separate
mechanisms patched on afterward:

`D_planetary,i(t) = F[L2D_i, P_i(P,Pa,F), Pa_i(P,Pa,F), F_i(P,Pa,F),
rho_i(r), phase_i(r), EM_i, neighbors_i, S_ref_i]`

No single variable — mass, spin, EM, or distance — is the cause by
itself; the physical state is the interaction pattern.

## Layered state

- **2D bound/compressed layer:** `L2D_i = {C_i, T_i, gamma_i, Q_i,
  Omega_i}` (compression, tension/stiffness, shear-damping, integrity,
  circulation). Must not be replaced by a scalar gravity parameter.
- **POINT(P,Pa,F):** internal structure — density profile, core/mantle/
  crust layers, differential rotation, conducting-fluid rotation,
  internal current `J_internal` and field `B_internal`, thermal/phase
  state, internal shear.
- **PATH(P,Pa,F):** `{r_i, v_i, Omega_path_i, phase_path_i,
  DeltaS_path_i, overlap_i}` — not merely the geometric orbit; carries
  the deformation/wake geometry produced along the motion and the
  spin/path phase relation.
- **FIELD(P,Pa,F):** `{Phi_i, gradPhi_i, curvature_i, R_active_i,
  Omega_field_i, phase_field_i, EM_shell_i, S_ref_i}` — the local
  displacement-field center, finite active region, shell orientation,
  and overlap with solar/neighboring fields.

These nine components are coupled views of one displacement system, not
independent corrections.

## Rotation, EM, and active range

Rotation is primary, not a small correction: `Omega_body, Omega_core,
Omega_conducting_fluid, Omega_EM_internal, Omega_path, Omega_field` and
their relative differences drive a shear/damping channel `P_shear ~
gamma * (DeltaOmega)^2`. Internal EM rotation runs `conducting-flow
rotation -> current circulation -> internal B field -> EM-field rotation
-> external EM shell`, feeding back into conducting flow. EM enters only
as a shell/bound-state response modifier, `K_eff_i = K0_i * M_EM_i(P_i,
Pa_i, F_i, B_internal_i, B_external_i, alignment_i)`, never as a direct
gravity-like force. A body's active range is an output, not an
assignment: `R_active_i(t) = R[L2D_i, D_i, rho_i(r), P_i, Pa_i, F_i,
EM_i, DeltaS_surroundings]`, with `Omega_i(t)` the region where its
slope structure stays distinguishable from the current reference — no
universal AU cutoff, no stored wake memory or relay mechanism.

## Per-body assignments

Mercury carries an extra Sun-Mercury EM relation `C_SM` on top of its
intrinsic dynamo state, with the 3:2 spin-orbit resonance retained as the
standard gravitational/tidal control fact. Earth's state includes
core/mantle differential rotation, geodynamo circulation, and Moon
coupling. Mars and Venus retain full rotational/path/field dynamics
without an Earth-like global intrinsic dipole (`C_Mars_global =
C_Venus_intrinsic = 0` on the first pass) and remain the controls against
inventing a global shell to force a fit. Jupiter, Saturn, Uranus, and
Neptune require full internal-fluid/current/field states and are the
mandatory falsification case against "larger magnetic moment implies
larger orbital correction."

## Falsification requirements

Reject or revise if the same rule needs body-by-body arbitrary
coefficients, if rotation variables add no predictive content over a
simpler model, if the EM-shell law contradicts giant-planet or no-dipole
behavior, if the finite-range law cannot reproduce observed multi-body
dynamics, if the 2D bound-state variables are redundant, or if the
recursive Point-Path-Field state merely renames standard variables
without a distinct measurable residual.

## Locked statement

`PLANET = persistent planetary-scale displacement structure`
`PLANETARY STATE = 2D bound/compressed state + recursive Point-Path-Field
+ internal material/fluid rotation + internal current/EM rotation + path
rotation + field rotation + instantaneous neighboring/reference
interactions`
`ACTIVE RANGE = output of the full current planetary displacement state`
`ORBIT / GRAVITY-LIKE RESPONSE / SPIN / TIDES / EM SHELL / STRESS /
STABILITY = readouts of that state`
`NO universal cutoff, NO memory relay, NO mass-only well, NO bolt-on
magnetic gravity force`

## Executable reference

- `Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/planetary_displacement_state.py`
- `Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/solar_system_control.py`
- `Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/planetary_visual.html`
- `UPDATED_41_PLANETARY_SCALE_DISPLACEMENT_MODEL.md`
- `UPDATED_40_RECURSIVE_PLANETARY_POINT_PATH_FIELD_ROTATION_MODEL.md`
- `UPDATED_39_MOVING_FINITE_SLOPE_AND_EM_SHELL_ORBITAL_MODEL.md`
- `UPDATED_38_FINITE_WAKE_THREE_BODY_PERTURBATION_ARCHITECTURE.md`
