# Field Coder — Build Diary

This diary is mandatory project memory.

## Prior verified history
- Steps 00-12: PASS
- All prior hard stops: SATISFIED

## Entry 0028 — Step 13 sacrificial-repo pre-pass
- Branch: `field-coder/13-sacrificial-repo`
- Hard-start check: PASS
- Attempt: 1/3
- Intended change: compose existing components plus one disposable end-to-end proof

## Entry 0029 — Step 13 first integration execution
- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/13-sacrificial-repo`
- Step: 13 — End-to-end controlled proof
- Attempt: 1/3
- Command/check executed: sacrificial workflow test against local mirror of checked-in Step 13 components
- Exit status/result: FAIL before Field candidate creation
- Observed behavior: fixture baseline test passed, then `capture_known_good()` rejected the source because Python created untracked `__pycache__` files
- What worked: clean-known-good safety gate correctly refused a dirty source; workflow implementation had not modified source or candidate
- What failed: sacrificial fixture did not declare generated Python cache files as ignored
- What was learned: a realistic Python fixture needs repository ignore policy before it can qualify as a clean known-good checkout
- Decision: RETRY test fixture only; workflow implementation unchanged
- Next permitted action: add committed `.gitignore` for `__pycache__/` and `*.pyc` to the sacrificial fixture setup, then rerun Step 13
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
