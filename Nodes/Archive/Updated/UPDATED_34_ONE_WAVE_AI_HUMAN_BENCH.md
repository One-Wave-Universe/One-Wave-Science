# Updated 34 — One-Wave AI + Human Bench

This update adds a **shared AI + human laboratory** on top of the D-413 Ground
Lattice Orbital-Restoring Simulation, plus **fixed reproducible simulations**
embeddable in wiki pages. Everything obeys the D-412 simulation standard and the
A-117 native-dimension rule. Stage 01 remains a **Yellow reduced model**.

## What was added

### 1. Experiment protocol (the contract)
`One_Wave_Bench/schema/experiment_protocol.json` — defines an experiment
**request** (id, author `human|ai`, hypothesis, parameter cases, falsifiers,
required measurements) and a **receipt** (measured fields, control checks,
pass/fail, native dimension, and a separate interpretation field). Governed by
D-412 and A-117.

### 2. Headless engine + manifest
- `One_Wave_Bench/engine/run_experiment.py` imports the **canonical** D-413
  physics from `Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation/simulate_d413.py`
  (single source of truth — no forked physics), runs any request, and writes a
  receipt plus per-case CSV time series. It also runs a zero-input drift control
  and an "activity" check so runs can fail.
- `One_Wave_Bench/engine/build_manifest.py` scans `runs/` and writes
  `runs/manifest.json`, which the bench UI reads.

### 3. Shared bench UI
`One_Wave_Bench/index.html` — one page both a human and an AI use:
- Live D-413 simulation (same engine the runner drives headlessly).
- Experiment ledger of **real runs**, each tagged author / status / native
  dimension, with per-case measurement cards, sparkline charts, and the honest
  interpretation.
- Experiment composer with a Human/AI toggle that emits a request JSON matching
  the protocol.
- Must be served over HTTP (it fetches `manifest.json`).

### 4. Fixed simulations for wiki pages
`One_Wave_Bench/fixed_sim.html` — locked-parameter, reproducible player selected
by URL. Scenarios: `orbit_asymmetric`, `deep_well`, `travel_across`,
`lattice_scrolls`. The last two are the same run under two cameras: displacement
moving across a fixed lattice, and the lattice scrolling with the displacement
centred. The gravity/curvature well renders explicitly (contours + depth marker
+ shaded surface); the bounded shell rotates/spins from its own state.
Embedded into `Wiki_Pages/D-413_Wiki_Page.html` under **Embedded Fixed
Simulations**.

## Real experiments run this session (already in `runs/`)
- **EXP-DEMO-001** — asymmetry sweep. Induced spin rose monotonically with shell
  asymmetry (0.080 → 0.134 → 0.219). Hypothesis **confirmed**.
- **EXP-2026-07-23-002** — well-depth sweep. **Partially falsified**:
  `well_distance_min` was non-monotonic (3.098 → 2.960 → 3.043) and spin rose
  strongly with depth (0.080 → 0.134 → 0.205), because the auto orbit-velocity is
  derived from `well_depth`, coupling depth to torque. **Next test:** hold orbit
  velocity fixed while varying depth to separate the two effects.

## Integrity
Both repository validators pass with zero errors. The consolidated receipt
(`Integrity_Tools/CONSOLIDATED_INTEGRITY_RECEIPT.json`) reflects the new files:
overall_pass true, 566 files, 0 hard issues, 1 documented benign flag
(quarantined historical draft quoting a misspelled filename).

## Suggested next builds
- Add an "orbit-velocity-fixed" well-depth experiment to close the EXP-002
  finding.
- Wire the composer's "Generate request JSON" to a one-click run when an AI is
  driving the session end to end.
- Progress toward the Updated 33 target (circulation-emergence laboratory): add
  derived circulation/vorticity measurements to the receipt schema.
