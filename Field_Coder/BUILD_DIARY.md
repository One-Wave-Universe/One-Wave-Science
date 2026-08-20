# Field Coder — Build Diary

This diary is mandatory project memory.

## Prior verified history
- Steps 00-11: PASS
- All prior hard stops: SATISFIED

## Entry 0026 — Step 12 model-adapter pre-pass
- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/12-model-adapter`
- Step: 12 — Replaceable coding model seat
- Goal: add a provider-neutral model seat plus one localhost model transport without engine lock-in
- Hard-start check: PASS — completed Step 11 lineage inherited; complete control set and latest diary reread
- Known-good state: Steps 01-11 verified
- Attempt: 1/3
- Intended change: add only request/response adapter contract, fake adapter, localhost OpenAI-compatible adapter, adapter-independent invocation function, and tests
- Files expected to change: `Field_Coder/field/model_adapter.py`, `Field_Coder/tests/test_model_adapter.py`
- Must remain unchanged: prior Field behavior; no Step 13 end-to-end orchestration, Void logic, provider-specific controller branch, or self-approval
- Exact success test: fake and localhost adapters satisfy identical `ModelResponse`; identical `run_model(adapter, request)` call works for both; malformed local response rejected; adapter swap requires no controller rewrite
- Files actually changed: pending
- Command/check executed: pending
- Exit status/result: pending
- Observed behavior: pending
- What worked: Step 12 hard-start/read discipline completed
- What failed: none
- What was learned: the model must occupy a replaceable seat rather than becoming the Field engine itself
- Decision: KEEP
- Next permitted action: create the two declared Step 12 files and execute adapter contract tests
- Hard-stop status: NOT YET SATISFIED
- Blockers: none

---

## Required template for every later entry
- Date/time:
- Branch:
- Step:
- Goal:
- Hard-start check:
- Known-good state:
- Attempt:
- Intended change:
- Files expected to change:
- Must remain unchanged:
- Exact success test:
- Files actually changed:
- Command/check executed:
- Exit status/result:
- Observed behavior:
- What worked:
- What failed:
- What was learned:
- Decision: KEEP / REVERT / RETRY / REPLAN / BLOCKED
- Next permitted action:
- Hard-stop status:
- Blockers:
