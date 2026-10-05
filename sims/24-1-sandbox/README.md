# 24→1 Sandbox

Common wrapper for modular One-Wave scientific simulations and visualizations.

- `GOLD_STANDARD.md` is the canonical contract.
- `sandbox.py` validates the module registry headlessly.
- `module-manifest.template.json` is the manifest starting point.
- `modules/01..24/` are adapters, not independent incompatible engines.

The first milestone is **adapter-first**: wrap existing simulations without changing their physics. Once an adapter reproduces the original receipt, the common 2D/3D visual layer can consume its renderer-neutral geometry.

Run:

```bash
python3 sandbox.py --json
```

A module may be exploratory and still run in the sandbox. GOLD status is separate and requires the full checklist in `GOLD_STANDARD.md`.

## Runnable slot 1: lattice primitive

Slot 1 wraps the existing G-764 kernel without changing its update law. Run:

```sh
node sims/24-1-sandbox/modules/01-lattice-primitive/adapter.js > lattice-receipt.json
node --test sims/24-1-sandbox/modules/01-lattice-primitive/test_adapter.js
```

Commands above run from the repository root. An optional JSON request file has
`configuration` (parameters, center-pulse amplitude/velocity) and `run` (steps,
positive dt). The default is 100 steps of 0.001 numerical time; 10,000 steps is
the hard run limit. The CLI returns nonzero for invalid input or a refused step.
A failed step retains the last accepted state and reports its requested index.
No random initialization or external data is used in this adapter's first scope.

The exported API is `manifest`, `initialize`, `step`, `measure`, `geometry`,
`serialize`, `restore`, `references`, and `run`. Snapshots have the Universal
State Container's id/state/measurements/provenance envelope. Manifest paths are
relative to the manifest directory. The receipt includes raw final site state,
per-step measured observables, adaptive-step receipts, numerical energy drift,
configuration, canonical node binding and SHA-256 source identities. Git HEAD is
context only: hashes identify source files at adapter import, and a run refuses
if they changed since import. These hashes do not prove the bytecode identity
of CommonJS modules preloaded by another caller; use the fresh-process CLI for
reproducible receipts. Time and frequency remain uncalibrated numerical units.

The node binding covers G-764's bounded oscillator software only. D-412 remains
the governing standard and G-766's dispersion fixture remains a separate control.
All source claim gates are unchanged. Manifest validation alone does not execute
a module or prove coverage. Spatial convergence, group-velocity calibration,
nonlinear confinement, browser visual review and physical interpretation remain
unverified. The geometry is a native 2D graph; displacement height is a labeled
projection. No additional physical fields are inferred from its appearance.
