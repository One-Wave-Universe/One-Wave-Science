# Field Coder — Build Diary

This diary is mandatory project memory.

## Prior verified history
- Steps 00-08: PASS
- All prior hard stops: SATISFIED

## Entry 0020 — Step 09 self-correction pre-pass
- Branch: `field-coder/09-self-correction`
- Hard-start check: PASS
- Attempt: 1/3
- Intended change: deterministic evidence/attempt state transitions and tests

## Entry 0021 — Step 09 self-correction completed
- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/09-self-correction`
- Step: 09 — Three-attempt Field learning loop
- Goal: encode the three-attempt law as persistent state-machine behavior
- Hard-start check: PASS
- Known-good state: Steps 01-08 verified
- Attempt: 1/3 implementation
- Intended change: `correction.py`, `test_correction.py`
- Files actually changed: exactly the two declared Step 09 files plus mandatory progress/diary records
- Command/check executed: Step 09 test plus all Step 01-08 regression tests in exact local mirror
- Exit status/result: PASS — all nine test files exit 0
- Observed behavior: failure moved 1->2 RETRY, 2->3 REPLAN, 3->BLOCKED; blocked state persisted; fourth transition rejected; pass routed review-ready
- What worked: bounded state transitions, JSON-safe evidence persistence, hard blocked state
- What failed: nothing in implementation or tests
- What was learned: three-strike behavior is now enforceable code, not an instruction the agent can ignore
- Decision: KEEP
- Next permitted action: transition `field-coder/10-git-safety` to this completed Step 09 lineage and begin only known-good workspace protection after rereading controls
- Hard-stop status: SATISFIED
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
