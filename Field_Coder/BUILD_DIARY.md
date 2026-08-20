# Field Coder — Build Diary

This diary is mandatory project memory. Every coding pass, failure, retry, replan, branch close, and branch open gets an entry.

---

## Entry 0001 — Step 00 control layer started

- Date/time: 2026-08-19 19:50 America/Los_Angeles
- Branch: `field-coder/00-control`
- Step: 00 — Project control layer
- Goal: establish a drift-resistant Field Coder build process before implementation begins
- Hard-start check: PASS — repository found, `main` accessible, existing `AGENTS.md` read
- Known-good state: existing repository preserved; no root protocol file overwritten
- Attempt: 1/3
- Intended change: create isolated Field Coder control documentation and branch plan
- Files expected to change: `Field_Coder/*` control documents only
- Must remain unchanged: root `AGENTS.md`, existing animator code, science content, existing branches
- Success test: all required control docs exist, future branches inherit them, every branch has explicit hard start/stop
- Work completed so far:
  - created `field-coder/00-control`
  - added project index
  - locked Field-only scope
  - added permanent carry-forward rules
  - added full branch build map with hard starts/stops
  - added persistent progress report
- Result: PASS so far
- Decision: KEEP
- Next action: finish diary/control verification, create all named branches from the completed control branch, then close Step 00
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
