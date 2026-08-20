# Field Coder — Progress Report

## Project

- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/05-proposal-builder`
- Current step: 05 — One implementation proposal
- Status: IN PROGRESS
- Attempt: 1/3

## Completed steps

- Step 00 — Project control layer: COMPLETE
- Step 01 — Executable Field shell: COMPLETE
- Step 02 — Persistent Field state: COMPLETE
- Step 03 — Goal to one narrow task: COMPLETE
- Step 04 — Read-only repository reconstruction: COMPLETE

## Current goal

Validate exactly one structured implementation proposal grounded in the current task and read-only repository context, without editing files.

## Hard-start evidence

- Step 05 moved to completed Step 04 lineage.
- Step 04 read-only context bundle is verified and recorded.
- Complete Field control set and active Step 05 section reread.
- No model seat exists yet; Step 05 therefore proves the deterministic proposal contract using fixture draft input.

## Known-good state

Field can start, persist state, accept one bounded task, and reconstruct task-scoped repository context read-only.

## One allowed change

Add only proposal data structures, grounding validation, and proposal-only tests.

## Proposal contract

A candidate proposal must provide:

- exactly one intended change
- reason
- exact files expected to change
- invariants to preserve
- expected result
- exact success test

Target files must be inside both the task scope and the read-only repo context.

## Exact success test

1. valid single-change proposal is accepted and normalized;
2. proposal missing target files is rejected;
3. proposal missing invariants is rejected;
4. proposal missing success test is rejected;
5. proposal containing more than one intended change is rejected;
6. proposal targeting a file outside task/context scope is rejected;
7. Steps 01-04 regression tests remain passing.

## Must not add in Step 05

- file editing
- model calls
- diff capture
- target-project command execution
- retry/controller behavior
- Void logic

## Next allowed action

Create `Field_Coder/field/proposal.py` and `Field_Coder/tests/test_proposal.py`, then run proposal verification plus prior regressions.

## Hard stop

Stop after the single-change proposal contract and rejection cases are proven and recorded.