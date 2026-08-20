# Field Coder — Progress Report

## Project
- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/09-self-correction`
- Current step: 09 — Three-attempt Field learning loop
- Status: COMPLETE
- Attempt: 1/3

## Completed steps
- Steps 00-09: COMPLETE

## Step 09 verified result
- Added `Field_Coder/field/correction.py` and `Field_Coder/tests/test_correction.py` only for Step 09 implementation.
- Attempt 1 failure -> `RETRY`, attempt 2, `evidence_based_correction`.
- Attempt 2 failure -> `REPLAN`, attempt 3, `materially_different_correction`.
- Attempt 3 failure -> `BLOCKED`, attempt remains 3.
- Blocked FieldState saves and reloads exactly.
- A transition from blocked state raises `CorrectionError`; no fourth retry path exists.
- Passing evidence routes directly to `review_ready` without incrementing attempt.
- Failure/test evidence is stored in persistent `last_result`.
- Steps 01-08 regressions all pass.

## Known-good state
Field now has a mechanically bounded three-attempt evidence loop in persistent state.

## Test evidence
`python3 Field_Coder/tests/test_correction.py`
- PASS: attempt 1 -> attempt 2
- PASS: attempt 2 -> materially different attempt 3
- PASS: attempt 3 -> BLOCKED
- PASS: blocked state persists
- PASS: fourth retry rejected
- PASS: passing evidence -> review-ready

All Step 01-08 regression tests: PASS.

## Current blockers
- None.

## Next branch
`field-coder/10-git-safety`

## Step 10 hard start
Move Step 10 to this completed commit, reread all controls, confirm Step 09 hard-stop evidence, then add only known-good Git workspace protection and rollback tests.

## Step 10 hard stop reminder
Stop after a deliberate bad edit is completely restored, original known-good commit remains unchanged, a successful candidate remains inspectable, prior regressions pass, and diary/progress are updated.