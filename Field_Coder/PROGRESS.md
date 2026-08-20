# Field Coder — Progress Report

## Project
- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/08-test-runner`
- Current step: 08 — Evidence-producing execution
- Status: IN PROGRESS
- Attempt: 1/3

## Completed steps
- Step 00 — Project control layer: COMPLETE
- Step 01 — Executable Field shell: COMPLETE
- Step 02 — Persistent Field state: COMPLETE
- Step 03 — Goal to one narrow task: COMPLETE
- Step 04 — Read-only repository reconstruction: COMPLETE
- Step 05 — One implementation proposal: COMPLETE
- Step 06 — Apply one declared change: COMPLETE
- Step 07 — Intended vs actual change: COMPLETE

## Current goal
Execute the proposal's declared success test with bounded runtime and return deterministic evidence instead of crashing on test failure or timeout.

## Hard-start evidence
- Step 08 moved to completed Step 07 lineage.
- Step 07 diff-match/mismatch evidence is verified and recorded.
- `README.md`, `BUILD_SCOPE.md`, `CORE_RULES.md`, active `BUILD_STEPS.md`, `PROGRESS.md`, and latest `BUILD_DIARY.md` reread on this branch.
- Step 08 is execution/evidence only; retry logic remains future work.

## Known-good state
Field can start, persist state, accept one bounded task, reconstruct repo context, validate one proposal, make one declared edit, and compare actual diff to intention.

## One allowed change
Add only a bounded command runner for `ImplementationProposal.success_test` plus test-runner-only tests.

## Exact success test
1. known passing command returns `passed=true`, exit 0, captured stdout/stderr;
2. known failing command returns `passed=false`, exact nonzero exit code, captured stdout/stderr, without raising controller-level failure;
3. timed-out command returns `passed=false`, `timed_out=true`, bounded duration/evidence, without crashing;
4. command is tokenized without `shell=True`;
5. Steps 01-07 regressions remain passing.

## Must not add in Step 08
- retry/replan state transitions
- model calls
- Git rollback/commit safety
- review packet behavior
- Void logic

## Next allowed action
Create `Field_Coder/field/test_runner.py` and `Field_Coder/tests/test_test_runner.py`, then run Step 08 verification plus all prior regressions.

## Hard stop
Stop after passing/failing/timeout evidence capture is proven, prior regressions pass, and diary/progress are updated.