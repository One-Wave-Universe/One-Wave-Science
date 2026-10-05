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

## Registry checks are not simulation evidence

`sandbox.py` checks manifest structure, unique IDs/slots and referenced local
paths. Paths are relative to each manifest and must resolve inside this
repository (including symlink resolution). `state_schema` and optional adapter
`entry_point` must be files; adapter `existing` must be a directory. An empty
registry, malformed input or broken reference exits with status 2.

The JSON result labels its scope `manifest-and-paths-only` and always reports
`module_execution: not-run`. `entry_point_present` reports file presence only:
it does not import or run code. It is `null` when malformed structure prevents
path inspection, rather than falsely asserting that a file is absent. An adapter may remain unimplemented while its
manifest and existing-engine reference pass. `ok` and `occupied_slots` describe
valid registry entries, never validated node coverage, fixture execution,
scientific claims, GOLD status or browser quality. Slot 6 has a static diagnostic adapter; file presence alone does not execute it.

Run registry positive/negative controls from the repository root:

```sh
python -m unittest discover -s sims/24-1-sandbox -p 'test*.py' -v
```


## Runnable slot 6: static spectral phase diagnostic

Slot 6 wraps G-767's existing `phases`, `coherence` and `null_test` functions
without changing their arithmetic. This is a positive-scale logarithmic map,
not an FFT or a time-evolving physical solver. Run from the repository root:

```sh
python sims/24-1-sandbox/modules/06-spectral-lattice-phase/adapter.py > spectral-receipt.json
python -m unittest discover -s sims/24-1-sandbox/modules/06-spectral-lattice-phase -p 'test*.py' -v
```

The default uses an explicitly labeled synthetic exact-octave fixture. An
optional JSON file supplies the configuration directly, for example:

```json
{
  "records": [{"scale": 1}, {"scale": 2}, {"scale": 4}],
  "x0": 1,
  "scale_unit": "dimensionless",
  "reference_unit": "dimensionless",
  "reference_policy": "predeclared",
  "source": {"kind": "synthetic", "description": "exact-octave control"},
  "trials": 1000,
  "seed": 767
}
```

For provided data use `source.kind: "caller-provided"`. Units and reference
policy (`predeclared` or `training-frozen`) are caller declarations, not verified
external evidence. All scales and x0 must be finite and positive with matching
units; no implicit unit conversion occurs. Optional row `unit` must match.
Width and uncertainty, when supplied, are nonnegative numbers in the declared
scale unit. Labels are metadata strings. All raw record fields survive the
receipt; labels, widths and uncertainties do not affect this statistic.
Uncertainty propagation, width/Q analysis and mixed-unit ingest are not supplied.
There must be 3–10,000 records, 1–10,000 trials, at most 250,000 sample-trials,
and an integer seed in 0–2^32−1. Inputs whose ratios or null endpoints cannot be
represented by the unchanged floating-point engine are refused.

The API exports `manifest`, `initialize`, `step`, `measure`, `geometry`,
`serialize`, `restore`, `references`, `controls`, `validate`, and `run`. `step`
performs one static analysis and refuses dt, dynamic inputs and a second step.
Initialization/stepping and geometry return independently owned data. Snapshots
use the Universal State Container envelope. Restore and receipt validation
recompute the deterministic result, enforce resource bounds and reject altered
source identities, measurements or unsupported Python versions.

Receipts retain raw scales, log2 ratios, octave indices, fractional scale phases,
coherence, seeded null mean and the add-one upper-tail empirical p. The null is
independent matched-range log-uniform draws, not a permutation test. That p is
only an exploratory diagnostic: the required smooth-density, detector-acceptance,
background, uncertainty, selection and held-out controls remain unverified.
A large coherence or small p does not establish a lattice or physical result.

Input SHA-256 identifies canonical JSON of the declared configuration, not raw
external file bytes. Source hashes identify captured source files and are checked
again before use; the engine executes captured source bytes. Git HEAD is context
only. These checks do not attest the host interpreter or arbitrary in-process
monkeypatching. Use a fresh-process CLI for reproducible receipts; Python version
is retained. No external data is downloaded or silently fabricated.

Geometry consumes the exact verified analysis arrays: log2-ratio/phase scatter
and a unit-circle view of scale phase. Both are nonspatial 2D coordinate plots,
with dimensionless axes. They introduce no time, sample rate, frequency or spatial
field. The manifest's broader visual/validation checklist remains aspirational;
no 3D view or browser visual quality is established by this headless adapter.

## Automatic module receipt refresh

The **Lattice Kernel Tests** workflow now forms an event-driven loop:
repository change → exact-head reference → affected tests → actual adapter
receipts → return-reference comparison → immutable CI artifact. It runs on
relevant PR/main changes, including governed nodes and shared authorities, and
can be manually dispatched. It does not poll or install a device service.

`refresh-dependencies.json` declares paths for the two implemented modules.
G-764/G-766 changes affect slot 1; G-767 changes affect slot 6. Shared authority,
state-schema, controller or workflow changes affect both. The map supplies no
commands: executable argument lists are fixed in `refresh.py`. Unrelated changes
report `NOT_RUN_UNAFFECTED`/`NO_AFFECTED_MODULES`, never borrowed green evidence.
This is a bounded dependency map for these two modules, not all-node coverage.
Adding another module requires updating the map and strict registry/receipt gates.

The controller requires an exact clean HEAD, snapshots dependency membership and
bytes, and checks them before every command and at completion. Added/deleted
files or mid-run changes invalidate the bundle. Dirty files are preserved;
there is no pull, stash, reset, source edit, commit, push, merge or deployment.
Repository tests execute trusted project code in a disposable CI checkout;
reference checks detect changes but are not a sandbox against malicious code.

The automatic repair allowlist is **derived receipt/log regeneration only**.
This is not autonomous source-code healing. Test failures, missing dependencies,
unknown bases, malformed/stale receipts, source drift or exhausted bounds produce
HOLD. Each command gets one attempt, up to 60 seconds and 4 MiB combined output;
the complete run has a 240-second budget. No speculative fix/retry loop is run.
The scientific/physical limits of both adapters remain unchanged.

CI cancels superseded runs per PR/ref. It uses read-only permissions, does not
persist Git credentials and uploads an artifact named with exact HEAD, run ID
and attempt. A canceled/interrupted run cannot finalize a success summary.
Artifacts contain bounded logs, source references, checksums and actual receipts
when available; failure evidence is uploaded with `always()`. Retention is 14 days.
Completed older runs are historical evidence for their recorded HEAD, not current
status. There is no mutable `latest` receipt pointer or cross-run success cache.

For a manual run from a clean checkout (Python and Node installed), supply a
fresh output directory outside the checkout and Git metadata:

```sh
python sims/24-1-sandbox/refresh.py \
  --expected-head "$(git rev-parse HEAD)" \
  --output /tmp/one-wave-refresh-unique-run
```

Optional `--base <full-commit-sha>` selects affected modules by the changed paths;
an unavailable/invalid base HOLDs. With no base, both modules run. The output
parent must already exist; occupied or unsafe output locations are refused.
Separate manual runs with different output paths can run concurrently: automatic
single-flight/cancellation is provided by CI, not a local daemon or lock service.
Only a finalized `summary.json` describes the bundle result. `RUNNING.json` is
an ineligible start record; partial logs/receipts without a completed matching
summary must never be promoted to success. Consumers must compare the summary's
HEAD and dependency fingerprint with the current repository before reuse.
