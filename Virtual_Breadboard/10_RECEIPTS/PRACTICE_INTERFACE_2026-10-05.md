# Human / AI practice interface receipt — 2026-10-05

## Reference / branch-step
- MAIN GOAL: advance the Field/Void software-construction engine through bounded,
  inspectable and reproducible software work.
- WHY: allow humans and AI to load the same modeled circuit, execute a bounded
  experiment, inspect measurements, change it and repeat without an API account.
- CURRENT STEP GOAL: repair Layer 11 practice controls and interchange only.
- Repository: https://github.com/One-Wave-Universe/One-Wave-Science
- Default branch: main. Starting HEAD: `86a27c8b6087ff890fa6bca5dd5be49ecfba1118`.
- Task branch: `fix/breadboard-practice-controls-20261005`.
- LOCAL REPO ROOT: isolated, ephemeral cloud task checkout
  `/workspace/shared/science-breadboard-repair`; not the user's laptop/Jetson.
- HARD START: fresh upstream clone at verified HEAD, initially clean; existing
  other task worktrees left untouched. No device/runtime activation is claimed.
- References: AGENTS.md, GENERAL_REFERENCE_RULES.md, AI_CANONICAL_START_HERE.md,
  One_Wave_Bench/BREADBOARD_CANONICAL_ARCHITECTURE.md,
  Virtual_Breadboard/11_INTERFACE/README.md, BENCH_REALITY_CONTRACT.md.
- ALLOWED FILES: app.js, index.html, style.css, simulate.js (pot-position adapter
  only), main.js (existing smoke only), package.json, new practice test, README,
  this receipt, existing breadboard-flashlight-tests workflow.
- PROTECTED FEATURES: solver/model equations, CELL topology, existing presets'
  electrical nets, save/load/export, scope and all passing numerical regressions.
- PRIMARY LAYER: 11_INTERFACE. No second physics layer modified.

## Move / field notes
- Added pause/live, reset-time and bounded fixed-duration controls.
- Added atomic offline JSON load, board-spec readback and detached result receipt.
- Added matching local `window.breadboard` API; retained legacy runFast result keys.
- Preserved IDs, supported parameters and named differential measurements.
- Editing with a paused result withholds stale numbers while retaining component
  energy/history. Explicit Reset/load clears history and traces.
- UI and CLI now honor non-midpoint potentiometer position. Unknown parameters
  and unsupported editor parts/execution modes reject explicitly.
- Corrected three occupied-hole placements in two examples to unused holes on
  the identical existing conductive strip; test proves unchanged cellId topology.
- Replaced no-warning physical safety claim with explicit model-only wording.
- Added strict IDs/colors to prevent untrusted JSON from becoming HTML markup;
  escaped embedded exported-state markup, detached exported data/receipts.
- Added durable package/CI test entry and six additional Electron smoke checks,
  with optional screenshot capture and CI artifact preservation.

## View / action evidence
Command: run each package script named `test` or `test:*`, excluding desktop-smoke,
using Node v24.19.0 in this cloud workspace. Final run completed 2026-10-05 UTC.

| Script | Actual |
|---|---|
| `test` | PASS, exit 0 |
| `test:practice-interface` | PASS, exit 0 |
| `test:qualification` | PASS, exit 0 |
| `test:primitives` | PASS, exit 0 |
| `test:regression` | PASS, exit 0 |
| `test:flashlight-calibration` | PASS, exit 0 |
| `test:flashlight-reference` | PASS, exit 0 |
| `test:netlist` | PASS, exit 0 |
| `test:fault-states` | PASS, exit 0 |
| `test:basic-circuits` | PASS, exit 0 |
| `test:spice-analysis` | PASS, exit 0 |
| `test:solver-convergence` | PASS, exit 0 |
| `test:dc-op` | PASS, exit 0 |
| `test:stepping` | PASS, exit 0 |
| `test:diode-newton` | PASS, exit 0 |
| `test:mosfet-continuous` | PASS, exit 0 |
| `test:mosfet-model-cards` | PASS, exit 0 |
| `test:pwl-pulse` | PASS, exit 0 |
| `test:startup-uic` | PASS, exit 0 |
| `test:sparse-mna` | PASS, exit 0 |
| `test:adaptive-transient` | PASS, exit 0 |
| `test:integration-methods` | PASS, exit 0 |
| `test:convergence-diagnostics` | PASS, exit 0 |
| `test:spice-tolerances` | PASS, exit 0 |
| `test:ac-analysis` | PASS, exit 0 |
| `test:bode` | PASS, exit 0 |
| `test:pole-zero` | PASS, exit 0 |
| `test:controlled-sources` | PASS, exit 0 |
| `test:bjt` | PASS, exit 0 |
| `test:ngspice` | BLOCKED, exit 1: ngspice binary missing |

The 22 new controller checks execute the real app/solver with a minimal DOM
adapter. They prove fixed RC stepping, differential values, paused frame
stability, reset reproducibility, atomic invalid import, edited reruns, UI/CLI
RC and potentiometer numeric equality, all 13 existing preset roundtrips,
metadata save/load, detached outputs, retained capacitor state through switch
editing, strict numeric/parameter validation and markup rejection.

Additional checks: `node --check` app.js/main.js/simulate.js PASS;
`git diff --check` PASS; workflow YAML parses.

### Independent void oversight
Pre-oversight ALLOW for the bounded layer, followed by corrective review:
1. Preserve electrical state on ordinary switch edits; do not reset capacitor/
   magnetic history merely to invalidate old measurements.
2. Reject unsafe IDs/colors, duplicate physical holes and nonfinite winding
   values; detach returned data; preserve metadata and supported parameters.
3. Repair occupied preset holes without changing their electrical nets; preserve
   pot position across CLI/UI and include acquisition settings in receipts.
Post-review ALLOW for the local candidate after 22 tests and independent reruns
of circuit49, qualification80, primitives26 and regression100 checks.

### Failures / attempt ledger
- Initial browser proof: Chromium could not create its process socket, including
  reviewed escalation. Cloud browser rejected localhost with
  `ERR_BLOCKED_BY_CLIENT`. No bypass was attempted. Browser visual QA NOT VERIFIED.
- First minimal DOM adapter lacked insertBefore/options; corrected adapter.
- Preset import test exposed actual occupied-hole collisions in Cal C and memory
  cell; fixed same-node placement, retaining strict validation.
- Adding acquisition metadata exposed lazy default trigger selection during
  render; initialized selection on preset load, then paused evidence was stable.
- Numerical test approach: accepted after final regression pass. No repeatedly
  failed implementation approach was continued past three attempts.

## State / scale and hard stop
State: PARTIAL overall; local interface candidate PASSES declared controller and
numerical checks. DO NOT SCALE or claim complete physical readiness.

BLOCKED / NOT VERIFIED:
- Real Electron source and packaged smoke: not run locally (runtime/browser limit).
- Screenshot/visual layout inspection: not run locally; no screenshot fabricated.
- ngspice cross-check: dependency absent; no independent-SPICE pass claimed.
- New CI, public branch/PR, merge, deployment and user-device installation: not
  performed in this receipt. CI additions are code, not execution evidence.
- Physical bench validation remains a separate hardware/evidence gate.

HARD STOP: tested branch candidate ready for publication review. Next permitted
step is authorized draft publication, then actual CI/Electron/ngspice execution,
inspect returned screenshot, and fix any demonstrated failures in a fresh cycle.

## Reentry / reflection
What worked: humans and AI use the same explicit circuit/measurement contract in
executable controller tests. Repeated fixed trials are numerically reproducible;
ordinary switching retains physical state. Existing numerical suites remain green.
What did not: local actual-browser/independent-SPICE gates are environment-blocked.
What changed in assumptions: existing examples could violate their own import
collision rules; resetting on edit destroys useful transient experiments. Both
were repaired at their responsible interface boundary without touching physics.

Final tested source hashes (SHA-256):
- `Virtual_Breadboard/js/app.js`: `715ea51093d437a946f940ae06643c38e5252023c2bfd5ba11a1b43a637c0a9a`
- `Virtual_Breadboard/simulate.js`: `d79a0ae5c62f2f5cd297faef339d58d8ab8041b72eea2b25a8422b38cc36fc67`
- `Virtual_Breadboard/test/practice-interface.test.js`: `3d205a192ca1ae9b0a493abfc9ec2e5964531dc4ecce497ea5ff458ed214a3dc`
- `Virtual_Breadboard/main.js`: `bdd9f17987e10ba9d9fb0957aa951f0a302c10053c85aa748155f465136ec32a`
