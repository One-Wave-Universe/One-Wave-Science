# Field Coder — Progress Report

## Project
- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/07-diff-self-check`
- Current step: 07 — Intended vs actual change
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

## Current goal
Capture the actual changed-file inventory and unified diff after an edit, then compare that evidence against the accepted proposal before Field can claim success.

## Hard-start evidence
- Step 07 moved to completed Step 06 lineage.
- Step 06 controlled edit boundary is verified.
- Complete controls and active Step 07 section reread.

## Known-good state
Field can perform one proposal-declared write while blocking undeclared paths.

## One allowed change
Add only Git working-tree diff evidence capture and proposal-vs-diff validation with tests.

## Exact success test
1. fixture repo baseline committed;
2. controlled edit to the single proposal-declared file produces changed-file inventory and nonempty unified diff;
3. changed files exactly match proposal files => self-check passes;
4. extra unexpected tracked file modification remains present in evidence and causes self-check failure;
5. evidence is returned even on mismatch;
6. Steps 01-06 regressions remain passing.

## Must not add in Step 07
- target success-test execution
- retry controller
- model calls
- Git rollback/commit safety
- Void logic

## Next allowed action
Create `Field_Coder/field/diff_check.py` and `Field_Coder/tests/test_diff_check.py`, then run diff verification plus prior regressions.

## Hard stop
Stop after matching diff passes, unexpected extra change fails with evidence preserved, regressions pass, and diary/progress are updated.