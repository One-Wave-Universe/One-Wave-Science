# Field Coder — Progress Report

## Project

- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/03-task-intake`
- Current step: 03 — Goal to one narrow task
- Status: IN PROGRESS
- Attempt: 1/3

## Completed steps

- Step 00 — Project control layer: COMPLETE
- Step 01 — Executable Field shell: COMPLETE
- Step 02 — Persistent Field state: COMPLETE

## Current goal

Convert one supplied coding goal into exactly one explicit bounded task with scope and success criteria, while rejecting ambiguous, multi-task, or unbounded intake.

## Hard-start evidence

- Step 03 moved to completed Step 02 lineage.
- Step 02 hard-stop evidence confirmed in progress and diary.
- Full Field control set and active Step 03 section reread.
- Step 03 is parser/validator only; no model or repository editing is allowed.

## Known-good state

- Step 01 shell verified.
- Step 02 persistent state verified across fresh process restart.

## One allowed change

Add only a deterministic one-task intake contract/parser and intake-only tests.

## Intake contract

A broad goal may contain explanatory text, but must declare exactly one bounded task using three explicit lines:

- `TASK: <one task>`
- `SCOPE: <comma-separated bounded paths/components>`
- `SUCCESS: <one or more explicit success criteria separated by semicolons>`

Exactly one of each declaration is required. Multiple `TASK:` declarations, missing scope, missing success criteria, blank values, or duplicate declarations are rejected.

## Exact success test

1. broad sample goal with narrative + one TASK/SCOPE/SUCCESS set yields exactly one `TaskSpec`;
2. resulting task has nonempty summary, bounded scope, and success criteria;
3. two TASK declarations are rejected as ambiguous/multi-task;
4. missing SCOPE is rejected as unbounded;
5. prior Step 01 and Step 02 tests remain passing.

## Must not add in Step 03

- repository reading/editing
- model-driven task generation
- proposal generation
- diff/test runner behavior for target projects
- retry loop behavior
- Void logic

## Next allowed action

Create `Field_Coder/field/task_intake.py` and `Field_Coder/tests/test_task_intake.py`, then run Step 03 verification plus Step 01/02 regressions.

## Hard stop

Stop after the one-task contract and rejection cases are proven and recorded.