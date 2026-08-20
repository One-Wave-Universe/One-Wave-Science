# Field Coder — Progress Report

## Project
- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/10-git-safety`
- Current step: 10 — Known-good workspace protection
- Status: IN PROGRESS
- Attempt: 1/3

## Completed steps
- Steps 00-09: COMPLETE

## Current goal
Protect the source repository's known-good checkout by performing candidate work in a separate Git worktree and completely restoring failed candidate changes.

## Hard-start evidence
- Step 10 moved to completed Step 09 lineage.
- Full control set and latest diary reread.
- Step 09 persistent three-attempt ceiling is verified.

## Known-good state
Steps 01-09 verified; Field has bounded retries but no workspace rollback layer yet.

## One allowed change
Add only clean-baseline capture, isolated candidate worktree creation, candidate status inspection, and failed-candidate rollback with tests.

## Exact success test
1. clean fixture repo baseline HEAD captured;
2. separate candidate worktree created at same baseline commit;
3. deliberate tracked bad edit plus untracked file in candidate are completely removed by rollback;
4. candidate HEAD returns/remains at baseline and candidate status is clean;
5. original checkout HEAD, branch, status, and baseline file bytes remain unchanged;
6. a later successful candidate edit can remain dirty/inspectable in candidate while original checkout stays clean;
7. Steps 01-09 regressions remain passing.

## Must not add in Step 10
- automatic commit/push/merge
- review packet generation
- model calls
- Void logic

## Next allowed action
Create `Field_Coder/field/git_safety.py` and `Field_Coder/tests/test_git_safety.py`, then run Step 10 verification plus prior regressions.

## Hard stop
Stop after rollback safety and successful-candidate isolation are proven, regressions pass, and diary/progress are updated.