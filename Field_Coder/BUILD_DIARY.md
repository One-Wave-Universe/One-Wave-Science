# Field Coder — Build Diary

This diary is mandatory project memory.

## Prior verified history
- Steps 00-08: PASS
- All prior hard stops: SATISFIED

## Entry 0020 — Step 09 self-correction pre-pass
- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/09-self-correction`
- Step: 09 — Three-attempt Field learning loop
- Goal: make failure evidence drive persistent attempt transitions and prevent any fourth retry
- Hard-start check: PASS — Step 09 moved to completed Step 08 lineage; full control set/latest diary reread; Step 08 evidence capture confirmed
- Known-good state: Steps 01-08 verified
- Attempt: 1/3
- Intended change: add only deterministic evidence/attempt transition logic and tests
- Files expected to change: `Field_Coder/field/correction.py`, `Field_Coder/tests/test_correction.py`
- Must remain unchanged: prior behavior; no corrective code generation/model/Git-safety/review-packet/Void logic
- Exact success test: failure transitions 1->2 RETRY, 2->3 REPLAN, 3->BLOCKED; evidence carried; blocked state persists; fourth transition rejected; pass routes review-ready; prior regressions green
- Files actually changed: pending
- Command/check executed: pending
- Exit status/result: pending
- Observed behavior: pending
- What worked: hard-start/read discipline completed
- What failed: none
- What was learned: the retry ceiling must be encoded as state-machine law rather than prompt advice
- Decision: KEEP
- Next permitted action: create `correction.py` and `test_correction.py`, then run Step 09 and prior regression tests
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
