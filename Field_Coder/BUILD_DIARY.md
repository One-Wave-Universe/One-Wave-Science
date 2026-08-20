# Field Coder — Build Diary

This diary is mandatory project memory.

## Prior verified history
- Steps 00-09: PASS
- All prior hard stops: SATISFIED

## Entry 0022 — Step 10 Git-safety pre-pass
- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/10-git-safety`
- Step: 10 — Known-good workspace protection
- Goal: isolate candidate edits from the known-good checkout and completely restore failed candidate work
- Hard-start check: PASS — Step 10 moved to completed Step 09 lineage; full controls/latest diary reread; Step 09 hard-stop confirmed
- Known-good state: Steps 01-09 verified
- Attempt: 1/3
- Intended change: add only baseline capture, separate candidate worktree creation/status, rollback, and tests
- Files expected to change: `Field_Coder/field/git_safety.py`, `Field_Coder/tests/test_git_safety.py`
- Must remain unchanged: prior behavior; no auto commit/push/merge, review packet, model, or Void behavior
- Exact success test: bad tracked/untracked candidate edits fully rollback; original checkout remains identical; successful candidate can remain inspectable separately; prior regressions green
- Files actually changed: pending
- Command/check executed: pending
- Exit status/result: pending
- Observed behavior: pending
- What worked: hard-start/read discipline completed
- What failed: none
- What was learned: known-good protection belongs outside the model/editor; candidates need an isolated disposable workspace
- Decision: KEEP
- Next permitted action: create `git_safety.py` and `test_git_safety.py`, then run Step 10 and prior regressions
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
