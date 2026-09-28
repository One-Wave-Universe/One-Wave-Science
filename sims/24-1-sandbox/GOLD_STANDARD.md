# One-Wave 24→1 Physics Sandbox — Gold Standard v1

**Status:** canonical simulator architecture contract.

## Goal

Every scientific simulation must be both **scientific** and **visual**, while remaining a replaceable module inside one greater sandbox. Twenty-four experiment slots feed one common runtime/state/telemetry/visual contract. The wrapper is not a claim that 24 physical layers exist in nature; 24 is the engineering capacity of the sandbox.

## 24→1 contract

Each module implements the same conceptual interface:

1. `manifest()` — identity, claim gate, dimensions, units, dependencies, data sources.
2. `initialize(config, seed)` — deterministic initial state.
3. `step(state, dt, inputs)` — one bounded physical/numerical update.
4. `measure(state)` — scientific observables and uncertainty/error receipts.
5. `geometry(state)` — renderer-neutral points/lines/surfaces/fields for 2D or 3D.
6. `controls()` — standard/control model and hypothesis switches.
7. `validate(receipt)` — invariants, convergence and falsification checks.
8. `serialize(state)` — Universal State Container compatible snapshot.

The scientific solver never depends on the renderer. 2D and 3D views consume `geometry()` and measurements; changing the camera cannot change physics.

## Layer model

Every sandbox run may expose these layers independently:

- source/raw measurement;
- derived measurement;
- numerical state;
- reference/control;
- One-Wave candidate;
- residual/difference;
- uncertainty/error;
- history/hysteresis;
- relational/path;
- field/vector/scalar;
- 2D projection;
- 3D geometry;
- scale/octave;
- provenance;
- annotations/artistic overlay.

Artistic/cinematic layers are always marked non-solver.

## Gold-standard requirements

A module cannot be GOLD unless it has:

- declared equations/update law and units;
- deterministic seed where stochastic;
- standard/reference control;
- explicit One-Wave candidate isolated from control;
- conservation/error ledger where applicable;
- timestep/resolution/domain convergence;
- positive and negative synthetic fixtures;
- null/ablation tests;
- uncertainty propagation where source uncertainty exists;
- immutable provenance/checksum for external data;
- machine-readable receipt;
- 2D visual representation;
- 3D representation when geometry is genuinely spatial, otherwise an explicitly labeled projection/extrusion;
- headless scientific test path;
- browser visual path;
- failure/invalid states visibly exposed;
- held-out validation for fitted hypotheses;
- documentation of assumptions and known failure modes.

Gold means the implementation meets this engineering/scientific contract. It does **not** mean a One-Wave hypothesis is experimentally established.

## Continuous-improvement rule

Improvements happen through versioned modules and receipts. Never silently alter a solver that produced an old result. A replacement must:
- preserve or migrate the manifest/state schema;
- rerun gold fixtures;
- compare old/new numerical receipts;
- document intentional changes;
- keep failed/negative results;
- promote only after regression and scientific controls pass.

## Initial 24 slots

01 lattice primitive
02 path/transport
03 field/circulation
04 combined-state compression
05 discrete dispersion
06 spectral lattice phase
07 CERN excitation field
08 GWOSC strain field
09 antimatter measurement comparison
10 EM lattice forcing
11 localized knot search
12 nested vortex search
13 defect/anisotropy map
14 hysteresis/history field
15 energy/reinjection ledger
16 continuum-limit comparison
17 Newtonian two-body control
18 three-body stress control
19 spherical-flux control
20 reduced galaxy field
21 accretion control
22 chemistry/ATP energy-transfer bridge
23 CELL/body-lattice bridge
24 cross-scale held-out validator

Slots may be renamed/replaced as science advances, but the wrapper contract remains stable.

## Build priority

Bring existing simulations into the wrapper before multiplying new bespoke engines. First adapters: lattice primitive, G-767 spectral phase, GWOSC, CERN field, then cinematic Newtonian controls.
