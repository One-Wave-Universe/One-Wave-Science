# G-767 static adapter branch-step receipt

## Reference / hard start

MAIN GOAL: advance the Field/Void software-construction engine with one bounded,
independently reviewed scientific-software module. WHY: slot 6 had a valid
manifest but no executable common-wrapper adapter.

Repository: https://github.com/One-Wave-Universe/One-Wave-Science
Starting main: `a9483a050836d01d20dab319fbcd522ebf06f89e`.
Cloud-runner worktree: `/workspace/shared/science-spectral-adapter`.
Task branch: `fix/spectral-sandbox-adapter-20261005`. Clean at hard start;
old worktrees and their changes preserved. This is not a Jetson/laptop receipt.

Read: AGENTS, GENERAL_REFERENCE_RULES, AI_CANONICAL_START_HERE,
JETSON_OPENCLAW_RUNTIME, BRANCH_STEP_PROJECT_TEMPLATE, I-06, G-767, canonical
external measurement ingest rule, CERN/GWOSC domain READMEs, existing engine
and tests, sandbox GOLD_STANDARD, registry receipt, manifest and state schema.

G-767 remains YELLOW / ACTIVE_HYPOTHESIS. Its current engine computes a static
positive-scale log2/circular-coherence diagnostic and a seeded log-uniform null.
FFT/Parseval/sampled-time sinusoid tests do not apply to this implementation.

## Choice / allowed scope / protected work

Add the Python adapter and tests, its manifest binding and this receipt; extend
sandbox README, registry presence expectation and lattice CI. These seven files
are the full allowed scope. Preserve original engine arithmetic/source bytes,
scientific node metadata/gates, all other solvers/adapters, datasets and worktrees.

One static initialized-to-analyzed transition. No dt or inferred dynamics.
Exact engine equivalence, deterministic source-bound restore, bounded input,
caller-declared common units/provenance, raw metadata retention, same-state
nonspatial geometry and truthful diagnostic/null limitations are required.

## Field / Void / progress and strike record

Approach A, attempt 1. Independent pre-oversight: ALLOW exact seven-file scope.
Field: implementation and targeted controls prepared. Attempt-1 proof passed:
19 new tests, 2 original G-767 controls, 16 registry, 27 Node and 10 dispersion
tests. Independent numerical post-oversight initially ALLOW; 20 additional
varied seeded spectra matched a separately imported original engine.

Source-failure inspection then reproduced a missing manifest reference raising
KeyError (wrong object shapes could raise AttributeError), escaping the CLI's
JSON invalid-receipt path. Final publication gate: CORRECT. State: PARTIAL,
do not scale. Reentry preserved the numerical pass and source-failure gap.

Attempt 2: fresh unchanged HEAD/seven-file scope, independent pre-oversight
ALLOW for manifest/reference shape checks. Invalid shapes now raise ValueError;
added regression cases for missing references, wrong objects and path types.
Final proof and post-review are recorded below.
The engine is executed from captured bytes and source hashes rechecked before use.
Snapshot restore/replay compares recomputed results and provenance; no implicit
migration of old source identities or Python runtimes is performed.

## Tests / success criteria

- `python -m unittest discover -s sims/24-1-sandbox/modules/06-spectral-lattice-phase -p 'test*.py' -v`
- `python sims/06-spectral-lattice-phase/test_spectral_lattice_phase.py`
- `python sims/24-1-sandbox/modules/06-spectral-lattice-phase/adapter.py`
- Registry unittest discovery and real registry JSON CLI.
- Existing Node kernel/slot-1 adapter tests and Python dispersion tests.
- Exact seven-file diff, no engine/node change, independent final oversight,
  exact-head PR CI, head-pinned merge and main CI under parent publication scope.

## Hard stop / next permitted step

Stop on conflicting reference, scientific-math changes, unavailable source,
failed proof or missing authority. Do not expand to new external datasets,
new physical theories, smooth-density/acceptance inference or browser claims.
This step ends after slot-6 receipt verification and authorized publication.

## Final local evidence / State / Scale / Reentry

2026-10-05 isolated Linux runner, Python 3.12.14 / Node v24.19.0:
20 adapter tests, 2 original G-767 controls, 16 registry tests, 27 Node
kernel/slot-1 adapter tests and 10 Python dispersion tests passed. Both actual
adapter and registry CLIs exited 0; `git diff --check` passed. Independent final
post-oversight: ALLOW. Reviewer reran 20 adapter tests after correction;
earlier independent full regression/equivalence evidence remains applicable.

Actual default synthetic receipt: 5 records at scales 1,2,4,8,16, dimensionless
x0=1, seed=767, trials=1000. Coherence=1.0; log-uniform null mean coherence=
0.39574499294268933; add-one empirical upper-tail p=0.000999000999000999.
These are a synthetic diagnostic control, not a measured result or physical
significance claim. Five geometry points consume the same state arrays.
Adapter source SHA-256:
`50cde0133f775d93fa49462d98868093a1b5acd83c0217962bcfeaa1b39fb835`.
Original engine SHA-256 unchanged:
`cccd81a2211a3e3dbb59e00fe51d5ab25c755b01e0570abdde4a57e6442d83ad`.

State: RESOLVED for the bounded headless static adapter contract. DO NOT SCALE
this evidence to physical interpretation, uncertainty propagation, matched-density
nulls, held-out science or visual/browser quality. No external dataset was fetched.

Reflection: preserved the actual scale statistic rather than inventing time
integration or FFT semantics. Exact engine results, immutable input ownership,
source-bound replay and nonspatial plot coordinates are verified. Failed source
reference shapes were retained as negative tests and now yield bounded errors.

Reentry at local completion: base HEAD a9483a0 with only the seven permitted
files changed. Exact-head publication/CI/merge is the next parent-authorized
operation, not a claim made by this local receipt. Stop after publication and
receipt verification; any broader module work begins at fresh Reference.
