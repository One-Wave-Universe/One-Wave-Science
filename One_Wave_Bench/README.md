# One-Wave Bench — Shared AI + Human Laboratory

A turn-based workbench where **either a human or an AI** can propose a physics
experiment, run it against the canonical D-413 engine, and read the same
receipts. Governed by **D-412** (simulation standard) and **A-117** (native
dimension declaration).

## What is in here

| Path | Purpose |
|------|---------|
| `index.html` | The shared bench UI. Live D-413 simulation, experiment ledger of real runs, per-case charts, and an experiment composer that emits a request JSON. |
| `fixed_sim.html` | Fixed, reproducible simulation player. Locked-parameter scenarios selected by URL, e.g. `fixed_sim.html?scenario=orbit_asymmetric`. Embeddable in wiki pages. |
| `schema/experiment_protocol.json` | The request/receipt contract (hypothesis, cases, falsifiers, required measurements, control checks, native dimension). |
| `engine/run_experiment.py` | Headless runner. Imports the canonical D-413 physics (single source of truth) and executes any experiment request, emitting a D-412 receipt + CSVs. |
| `engine/build_manifest.py` | Scans `runs/` for receipts and writes `runs/manifest.json`, which the bench UI reads. |
| `runs/` | Real receipts, per-case CSV time series, and the manifest. |

## Fixed simulation scenarios

All are the **same engine and one update law**; only initial conditions,
locked parameters, and camera differ. Camera/projection never changes physics.

| `?scenario=` | Shows |
|--------------|-------|
| `orbit_asymmetric` | Bounded shell orbiting an imposed curvature well with induced spin. Ground-fixed camera. |
| `deep_well` | Deeper well capturing the shell into a tight restoring orbit. Well-fixed camera. |
| `travel_across` | Bounded displacement translating across a stationary lattice, with wake. Ground-fixed camera. |
| `lattice_scrolls` | Same run as `travel_across`, displacement-fixed camera, so the lattice scrolls past. |

Add `&autoplay=0` to start paused. Click the canvas to pause/resume.

## Running an experiment (human or AI)

1. Compose a request (use the composer in `index.html`, or write JSON that
   matches `schema/experiment_protocol.json`).
2. Run headless:
   ```
   python One_Wave_Bench/engine/run_experiment.py --stdin << 'JSON'
   { ...request... }
   JSON
   ```
   or `--request path/to/request.json`, or `--demo` for a built-in example.
3. Rebuild the manifest:
   ```
   python One_Wave_Bench/engine/build_manifest.py
   ```
4. Refresh `index.html` (served over HTTP — `manifest.json` is fetched, so a
   `file://` open cannot read it). From the repo root:
   ```
   python -m http.server 8899
   # then open http://localhost:8899/One_Wave_Bench/index.html
   ```

## D-412 discipline (enforced)

- Simulations evolve **declared state → computed measurements → visualization**.
- Every run can **fail**; falsifiers are declared before running.
- **Interpretation is kept separate** from raw output.
- Each run declares its **native dimension** (currently 2D).
- Stage 01 is a **Yellow reduced model**: the well is imposed and the shell is a
  collective coordinate. Nothing here claims gravity, charge, a proton, a Mirror
  Gate, or a Mass Effect.
