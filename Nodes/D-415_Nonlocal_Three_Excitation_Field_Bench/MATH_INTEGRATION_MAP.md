# D-415 Existing-Math Integration Map

## Audit result

The main repository contains 626 files (about 31.1 MB). A filename-level audit
identified at least 160 non-generated files directly related to Field,
displacement, compression, boundary, rotation, resonance, scale, relativity,
orbital dynamics, simulation, or mathematical evaluation. D-415 must ingest
that work; it may not restart the framework from a new candidate equation.

Generated `Wiki_Pages/` are presentation outputs, not the source authority.

## Mandatory authority order for simulator physics

1. `AI_CANONICAL_START_HERE.md`
2. `00_MASTER_INDEX.md`
3. `ONE_WAVE_TERMINOLOGY_LEGEND.md`
4. I-06 YAML metadata in each canonical node
5. latest `UPDATED_*` handoff affecting the mechanism
6. matching audit and internal-proof files
7. canonical node mathematics
8. book Gray/2D/3D interpretation
9. simulation implementation and receipts

Conflicting imported or newly written material must be quarantined rather than
silently merged.

## Planetary simulator load-bearing chain

### Existing architecture that must control D-415

- `UPDATED_38_FINITE_WAKE_THREE_BODY_PERTURBATION_ARCHITECTURE.md`
  - local-minus-reference slope;
  - relational three-body graph;
  - finite-wake boundary;
  - Jupiter perturbation and Mercury stress-test ladders.
- `UPDATED_39_MOVING_FINITE_SLOPE_AND_EM_SHELL_ORBITAL_MODEL.md`
  - instantaneous moving finite slope;
  - active region from distinguishability against the current reference;
  - EM shell as integrity/stiffness/response modifier;
  - Mars and Venus no-global-dipole controls;
  - full Solar-System falsification requirement.
- `UPDATED_40_RECURSIVE_PLANETARY_POINT_PATH_FIELD_ROTATION_MODEL.md`
  - nine recursive Point–Path–Field components;
  - compressed 2D bound-lattice state;
  - internal differential rotation and shear;
  - matter/EM rotation;
  - path and Field rotation;
  - active range derived from the full state;
  - planet-specific ablations.
- `UPDATED_41_PLANETARY_SCALE_DISPLACEMENT_MODEL.md`
  - complete planetary displacement state;
  - internal material/fluid/current/EM rotation;
  - instantaneous neighboring/reference interactions;
  - orbit, spin, tides, shell, stress, and stability as state readouts;
  - no universal cutoff, memory relay, mass-only well, or bolt-on magnetic
    gravity term.

### Foundation nodes

- `A-101` Ground / Zero
- `A-102` Displacement
- `A-103` Differential
- `A-104` Gradient
- `A-105` Restoring Response
- `A-106` Pressure Response
- `A-107` Bounded Motion
- `A-109` Inertial Memory
- `A-112` Persistent Mode
- `A-112a` Traveling Lattice Rupture
- `A-115` Unified Compression Field
- `A-116` Three-Dimensional Spherical Default
- `A-117` Dimensional Integrity and Projection Declaration

### Boundary, rotation, and carried-pattern mechanisms

- `B-206a` Shared Boundary
- `B-206b` Four Views
- `B-216` Threshold Mathematics
- `B-220` Scale Layer
- `C-303` Kinetic Energy
- `C-307` Angular Momentum
- `C-310` Resistance Field
- `C-311` Electric/Magnetic Duality
- `C-313` Lorentz Invariance Conflict
- `C-317` Boundary-Tension Weave
- `C-318` Four-Interaction Mass-Effect Response

### Resonance and Field dynamics

- `D-401` Flux
- `D-402` Resonant Mode
- `D-404` Nested Resonance
- `D-405` Harmonic Shell
- `D-408` native 2D six-neighbor lattice
- `D-409` native 3D twelvefold coordination
- `D-410` 4D recurrence shell
- `D-412` simulation and receipt standard
- `D-413` Ground lattice orbital-restoring simulation
- `E-503` pressure-gradient energy
- `E-518` relativistic energy-density extension
- `E-524` Kuramoto lattice synchronization

## Existing equations that must be represented in the state schema

```text
x = Delta_ref(psi, psi_0)

CHANGE_ij = LOCAL_SLOPE_i - REFERENCE_SLOPE_j
Delta_ij = grad(Phi_i) - grad(Phi_j)

S_i(r,t) = |grad Phi_i(r,t)|
DeltaS_i(r,t) = S_i(r,t) - S_ref(r,t)

L2_i = {D_i, C_i, T_i, gamma_i, q_i, phase_i}
R_i = {PP, PPa, PF, PaP, PaPa, PaF, FP, FPa, FF}_i

DeltaOmega_ab = Omega_a - Omega_b
H_shear,i = SUM_ab gamma_ab |DeltaOmega_ab|^2

Omega_path,i = |r_i x v_i| / |r_i|^2

R_active,i = R[L2D_i, D_i, rho_i, P_i, Pa_i, F_i, EM_i,
                 DeltaS_surroundings]

X_i(t+dt) = U[X_i(t), DeltaS_i(t), overlaps_i(t)]
```

These forms include unresolved functions `R`, `U`, `F`, and coupling maps.
Their presence is not permission to choose arbitrary implementations. Each
requires a declared ansatz, dimensions, ablation, and receipt until derived.

## Role of Newton and Einstein math

`solar_system_control.py` is a Gray comparison harness. It provides a stable
ephemeris-scale control and detects obvious hierarchy failures such as a Moon
escaping Earth or a marker outpacing its parent.

`hybrid_one_wave.py` is an audit bridge. The One Wave explanation is compared
with the relativistic response and is not added as another interaction.

Neither file supersedes Updated 38–41 or the canonical nodes.

## Required implementation sequence

1. Build a typed `PlanetaryDisplacementState` containing `L2D`, all nine PPF
   components, internal rotation, EM rotation, slope/reference, overlap, and
   active-range state.
2. Implement the Gray ephemeris control and attach every rendered object to its
   state-tree parent.
3. Implement `DeltaS` and instantaneous overlap receipts from Updated 38–39.
4. Implement Updated 40–41 rotation and bound-state updates with unresolved
   functions explicitly labeled as candidate ansatzes.
5. Run two-body, three-body, Jupiter, Mercury, Mars/Venus, and giant-planet
   ablations.
6. Compare all readouts—not only orbital position—against the Gray control.
7. Promote nothing until the D-412 receipt and dimensional declarations pass.

## Immediate correction

D-415's current nonlinear Field potential and global kernel are isolated Yellow
experiments. They are not the canonical planetary law and must not be wired into
the Solar-System visualization as though they replaced the existing repository
architecture.
