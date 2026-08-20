# Field Coder — Progress Report

## Project
- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/09-self-correction`
- Current step: 09 — Three-attempt Field learning loop
- Status: IN PROGRESS
- Attempt: 1/3

## Completed steps
- Steps 00-08: COMPLETE

## Current goal
Feed execution failure evidence into persistent Field state through a mechanically bounded three-attempt transition system with no possible fourth hidden retry.

## Hard-start evidence
- Step 09 moved to completed Step 08 lineage.
- Full Field control set and latest diary reread on this branch.
- Step 08 pass/fail/timeout evidence capture is verified.
- Step 09 is state-transition/evidence logic only; it does not generate corrective code.

## Known-good state
Field has deterministic shell, persistent state, one-task intake, read-only repo context, proposal validation, controlled editing, diff self-check, and bounded test evidence.

## One allowed change
Add only deterministic attempt/evidence state transitions and tests.

## Transition contract
- passing evidence -> `PASS`, attempt unchanged, next action `review_ready`;
- failure at attempt 1 -> `RETRY`, attempt 2, next action `evidence_based_correction`;
- failure at attempt 2 -> `REPLAN`, attempt 3, next action `materially_different_correction`;
- failure at attempt 3 -> `BLOCKED`, attempt remains 3, next action `blocked`;
- transition from already blocked state -> rejected; no attempt 4 exists.

Failure evidence is stored in `last_result` and transition action in `last_action` so state can be saved/reloaded.

## Exact success test
1. failing fixture evidence transitions attempt 1 -> 2 -> 3 -> BLOCKED;
2. evidence is carried in each resulting FieldState;
3. blocked state survives save/reload;
4. fourth transition is rejected;
5. passing evidence routes to review-ready without increment;
6. Steps 01-08 regressions remain passing.

## Must not add in Step 09
- actual corrective code generation
- model calls
- Git rollback/worktree logic
- review packet
- Void logic

## Next allowed action
Create `Field_Coder/field/correction.py` and `Field_Coder/tests/test_correction.py`, then run Step 09 verification plus all prior regressions.

## Hard stop
Stop after the bounded transitions, persisted blocked state, no-fourth-retry proof, regressions, and project-memory updates pass.