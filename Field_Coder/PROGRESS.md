# Field Coder — Progress Report

## Project

- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/02-state-memory`
- Current step: 02 — Persistent Field state
- Status: IN PROGRESS
- Attempt: 1/3

## Completed steps

- Step 00 — Project control layer: COMPLETE
- Step 01 — Executable Field shell: COMPLETE

## Current goal

Persist and restore Field's exact working state across restarts, while rejecting invalid or incomplete state.

## Hard-start evidence

- `field-coder/02-state-memory` advanced to the completed Step 01 commit.
- Step 01 hard-stop evidence exists in progress and diary.
- Full Field control set reread on Step 02 branch.
- Field-only scope and Step 02 allowed work confirmed.

## Known-good state

- Step 01 deterministic shell passes ready -> missing-component failure -> restored ready.
- No task intake, repo reader, model, editor, diff, retry, or Void behavior exists.

## One allowed change

Add only a Field state schema with validated JSON save/load behavior and a state-only test.

## Required state fields

- goal
- current_task
- attempt
- max_attempts
- last_action
- last_result
- next_action
- active_branch
- active_step

## Exact success test

1. create valid state;
2. save to JSON;
3. reload as a new `FieldState` instance and prove exact equality;
4. reject a saved state missing a required field;
5. reject invalid attempt bounds;
6. rerun the Step 01 shell test to prove prior verified behavior remains intact.

## Must not add in Step 02

- goal-to-task narrowing
- repository reading
- model calls
- editing/diff logic
- external project test runner
- retry controller behavior beyond storing attempt fields
- Void logic

## Next allowed action

Create `Field_Coder/field/state.py` and `Field_Coder/tests/test_state.py`, then run only Step 02 state verification plus the Step 01 regression test.

## Hard stop

After exact save/reload restoration, invalid-state rejection, Step 01 regression pass, and diary/progress closeout are recorded, stop coding on this branch.