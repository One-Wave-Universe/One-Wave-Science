# Field Coder — Progress Report

## Project
- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/12-model-adapter`
- Current step: 12 — Replaceable coding model seat
- Status: IN PROGRESS
- Attempt: 1/3

## Completed steps
- Steps 00-11: COMPLETE

## Hard-start evidence
- Step 11 hard stop satisfied and inherited.
- Full Field control set and latest diary reread on `field-coder/12-model-adapter`.
- Steps 01-11 work without a real provider dependency.

## Current goal
Add one provider-neutral model adapter contract and one localhost OpenAI-compatible transport without changing the Field engine when adapters are swapped.

## One allowed change
Add only model request/response adapter interfaces, fake adapter, localhost adapter, one adapter-independent invocation function, and tests.

## Exact success test
1. fake adapter returns the structured response contract;
2. localhost OpenAI-compatible adapter returns the same structured response contract against a local fixture server;
3. the same `run_model(adapter, request)` call works for both adapters;
4. invalid local response is rejected deterministically;
5. prior known-good behavior remains untouched.

## Must not add
- provider-specific engine logic
- actual production task orchestration
- Void logic
- autonomous approval
- end-to-end repo work (Step 13)

## Next allowed action
Create `Field_Coder/field/model_adapter.py` and `Field_Coder/tests/test_model_adapter.py`, then execute the Step 12 contract test.

## Hard stop
Stop Step 12 when adapter replacement requires only swapping the adapter object/configuration, not rewriting controller/engine code.