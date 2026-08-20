# Field Coder — Progress Report

## Project
- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/12-model-adapter`
- Current step: 12 — Replaceable coding model seat
- Status: COMPLETE
- Attempt: 1/3

## Completed steps
- Steps 00-12: COMPLETE

## Step 12 verified result
- Added `Field_Coder/field/model_adapter.py` and `Field_Coder/tests/test_model_adapter.py` only for Step 12 implementation.
- Provider-neutral `ModelRequest`, `ModelResponse`, and `ModelAdapter` contract defined.
- `FakeModelAdapter` satisfies the contract.
- `LocalOpenAICompatibleAdapter` satisfies the same contract through localhost HTTP.
- Both adapters run through the same `run_model(adapter, request)` function with no engine/controller branch.
- Malformed local-model responses are rejected deterministically.
- Local transport uses standard-library HTTP and does not bind Field to a model vendor.
- No end-to-end repo orchestration, Void logic, self-approval, push, or merge behavior was added.

## Test evidence
Exact local mirror of checked-in Step 12 files:
- PASS: fake adapter satisfies ModelResponse contract
- PASS: localhost adapter satisfies identical ModelResponse contract
- PASS: adapter swap requires no run_model/controller change
- PASS: malformed local response rejected

## Known-good state
Field now has a replaceable model seat. A local OpenAI-compatible coding model can occupy that seat without changing the Field engine.

## Current blockers
- None.

## Next branch
`field-coder/13-sacrificial-repo`

## Step 13 hard start
Move Step 13 to this completed commit, reread all controls, confirm Step 12 hard-stop evidence, then wire the already-verified components together only for a disposable end-to-end proof.

## Step 13 hard stop reminder
Stop after one successful tiny task and at least one deliberately bad candidate path are demonstrated end-to-end, known-good baseline is preserved, a review packet is emitted, and diary/progress are updated.