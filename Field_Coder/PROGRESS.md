# Field Coder — Progress Report

## Project
- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/13-sacrificial-repo`
- Current step: 13 — End-to-end controlled proof
- Status: IN PROGRESS
- Attempt: 1/3

## Completed steps
- Steps 00-12: COMPLETE

## Hard-start evidence
- Step 12 hard stop satisfied and inherited.
- Full Field control set and latest diary reread on this branch.
- All required individual components exist and have prior verification evidence.

## Current goal
Compose the existing Field components into one disposable repo workflow that proves failure -> evidence -> rollback/correction -> success -> review packet while preserving the source baseline.

## One allowed change
Add only orchestration that composes existing components plus a sacrificial end-to-end test. Do not redesign the component contracts.

## Exact success test
1. disposable Git repo starts with passing baseline test;
2. Field parses one bounded task and reads source context read-only;
3. attempt 1 produces a declared edit whose success test fails;
4. failure evidence advances state and candidate worktree is rolled back cleanly;
5. attempt 2 produces a corrected declared edit, diff matches proposal, and success test passes;
6. source checkout remains clean at original HEAD throughout;
7. successful candidate remains inspectable;
8. external-review packet is emitted with `PENDING_EXTERNAL_REVIEW`.

## Must not add
- real repo production change
- Void logic
- self-approval
- push/merge/commit automation

## Next allowed action
Create `Field_Coder/field/workflow.py` and `Field_Coder/tests/test_sacrificial_workflow.py`, then execute the disposable proof.

## Hard stop
Stop Step 13 only after both bad and good candidate paths are proven and recorded.