# Field/Void G-766 frequency repair

## Main goal / why this step exists
Exercise the real Field/Void software-construction loop on a reproducible Science simulation defect, with exact source reference, test evidence, peer exchange and personal progress journals.

## Current step / hard start
Correct cancellation in leapfrog_frequency for small nonzero modes.
GitHub connector repository: One-Wave-Universe/One-Wave-Science.
Base: 9dc26998d6bc901299cae55748df7efd79a3c887.
Branch: feature/field-void-g766-frequency-20261003.
Source scope: exact fixture, tests, README, G-766 and evidence contract. Full tree retrieved without truncation; not exhaustive model reading of every repo file.
Jetson is the model and test worker; its existing Science checkout is not being edited. Pinned UTF-8 sources are passed in a bounded temporary execution packet and Git blob hashes checked before execution.

## Reference files
GENERAL_REFERENCE_RULES.md; AI_CANONICAL_START_HERE.md; AGENTS.md; JETSON_OPENCLAW_RUNTIME.md; BRANCH_STEP_PROJECT_TEMPLATE.md; ENGINE_EVIDENCE_PIPELINES.md; sims/00_CANONICAL_INGEST_RULE.md; Nodes/G-766_Discrete_Lattice_Dispersion_and_Octave_Emergence_Proof.md; sims/00-lattice-primitive/README.md; dispersion_octave_fixture.py and test_dispersion_octave_fixture.py in the same folder.

## Allowed / protected
Allowed: one function in the fixture, targeted regression tests, and this progress journal/receipt.
Protected: all other science equations, physical calibration, G-766 YELLOW gate, original tests, main, existing Jetson working-tree changes.
No timers, scheduled retries or unmanaged repo clones.
External metadata tools remain available but public measurements cannot decide a floating-point identity; no metadata-driven parameter fitting is needed.

## Baseline / exact checks
On Jetson: all 10 pinned original tests pass.
Actual original leapfrog_frequency(1e-16, 0.1) returns 0.0; expected discrete frequency is approximately 1e-8.
Regression plan: tiny nonzero mode, exact zero, independently known angle, exact stability boundary, just-outside stability boundary, invalid input guards, and original convergence tests.
Approach A attempt 1; no edits to simulator yet.

## GPT / Field personal progress journal
Reference/Choice: read supplied exact source; reproduce evidence is from the Jetson test receipt.
Response ID 01a10339-2287-7bb1-bde8-d0a04d97640a.
Proposed half-angle identity replacing cancellation-prone acos expression with asin, with explicit stability guard.
Declared its tests proposed rather than executed. Declared extreme-product and nonfinite policies outside its initial proposal.
No peer approval received yet.

## DeepSeek / Void personal progress journal
Reference/Choice: supplied actual Field reply, same fixture/tests and baseline receipt. Pre-change review running through Jetson → signed-in DeepSeek browser relay.
No DeepSeek result claimed yet.

## Progress / hard stop
Field proposal received; Void review pending.
No code change before supported Void approval.
After accepted patch: run exact regressions, exchange actual test result, resolve objections and record agreement.
Stop this bounded problem once both accept the same tested solution. Do not claim the continuous app engine is complete.

## Next evidence
Boundary probe: sqrt(nextafter(4,+infinity)) rounds to 2 at dt=1. A guard relying only on that rounded square root can incorrectly accept an unstable value. Include this observation in the next peer pass.

## Paused after laptop jam report
The isolated Field candidate passed 10 original tests and 8 targeted checks on Jetson. Candidate and evidence checkpoint: field-void-g766-candidate-evidence-20261003.json under Jetson repo-lens runtime state.
DeepSeek returned no accepted review: the first request failed upstream and the smaller review request ended without a response. No two-AI agreement exists and no simulator patch was committed.
User reported laptop jamming. Model test paused; no further model requests. Dell remote terminal and process-list routes failed to return results; SSH from Jetson to Dell was refused. Targeted systemctl stop for one-wave-deepseek-web-relay.service was attempted but completion was not confirmed. Resource cause remains unverified. Preserve existing working-tree changes and the proven candidate; resume only after laptop responsiveness is restored.
