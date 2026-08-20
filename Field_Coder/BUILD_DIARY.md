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
- Result: PASS
- Decision: KEEP

---

## Entry 0002 — Step 00 control layer completed

- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/00-control`
- Step: 00 — Project control layer
- Goal: finish and verify the complete Field Coder control layer
- Hard-start check: PASS
- Known-good state: root `AGENTS.md` unchanged; Field work isolated under `Field_Coder/`
- Attempt: 1/3
- Intended change: finish control files, create all planned branches, verify branch set, close Step 00
- Files expected to change: Field Coder control documents only; Git branch refs
- Must remain unchanged: existing animator/science implementation and root protocol
- Exact success test: verify branches `field-coder/00-control` through `field-coder/14-real-repo-trial` exist and each has a documented purpose, hard start, success condition, and hard stop
- Files actually changed: `Field_Coder/README.md`, `Field_Coder/BUILD_SCOPE.md`, `Field_Coder/CORE_RULES.md`, `Field_Coder/BUILD_STEPS.md`, `Field_Coder/PROGRESS.md`, `Field_Coder/BUILD_DIARY.md`
- Command/check executed: GitHub branch search for `field-coder/`
- Exit status/result: PASS — 15 expected branches returned
- Observed behavior: all implementation branches were created from the Field control lineage; control documents exist; root `AGENTS.md` was not overwritten
- What worked: isolated Field-only project scope; branch gates; persistent project memory; hard-start/hard-stop definitions
- What failed: nothing in Step 00
- What was learned: the Field project now has repository-resident memory and does not need conversation memory to know its build rules
- Decision: KEEP
- Next permitted action: open `field-coder/01-shell`, reread the full control set, update progress/diary for Step 01, then make only the minimal executable shell change
- Hard-stop status: SATISFIED — no implementation code added to control branch
- Blockers: none

---

## Entry 0003 — Step 01 shell pre-pass

- Date/time: 2026-08-19 20:03 America/Los_Angeles
- Branch: `field-coder/01-shell`
- Step: 01 — Executable Field shell
- Goal: create the smallest Field coding-agent program that starts successfully and detects a missing required shell component
- Hard-start check: PASS — Step 00 complete; full Field control set reread on this branch
- Known-good state: control layer complete; no Field implementation code yet
- Attempt: 1/3
- Intended change: add only the initial Field source tree, deterministic controller entry point, one required shell component, and shell-only verification test
- Files expected to change: `Field_Coder/field/__init__.py`, `Field_Coder/field/controller.py`, `Field_Coder/field/shell_component.py`, `Field_Coder/tests/test_shell.py`
- Must remain unchanged: all root animator/science code; root `AGENTS.md`; Field state/model/repo/edit/diff/retry/Void behavior
- Exact success test: initial controller run exits 0 with `FIELD_SHELL_READY`; temporary absence of `shell_component.py` is detected with nonzero exit and deterministic missing-component output; restoration returns exit 0 and `FIELD_SHELL_READY`
- Files actually changed: pending
- Command/check executed: pending
- Exit status/result: pending
- Observed behavior: pending
- What worked: hard-start/read discipline completed
- What failed: none
- What was learned: Step 01 is tightly bounded to shell behavior only
- Decision: KEEP
- Next permitted action: create the four declared shell files and run the exact shell test
- Hard-stop status: NOT YET SATISFIED
- Blockers: none

---

## Entry 0004 — Step 01 executable shell completed

- Date/time: 2026-08-19 20:03 America/Los_Angeles
- Branch: `field-coder/01-shell`
- Step: 01 — Executable Field shell
- Goal: prove the minimal Field shell starts, detects a missing required component, and recovers after restoration
- Hard-start check: PASS
- Known-good state: Step 00 control layer complete
- Attempt: 1/3
- Intended change: add only the four declared Step 01 shell files
- Files expected to change: `Field_Coder/field/__init__.py`, `Field_Coder/field/controller.py`, `Field_Coder/field/shell_component.py`, `Field_Coder/tests/test_shell.py`
- Must remain unchanged: all later-step behavior and all non-Field project code
- Exact success test: ready -> deliberate missing component rejected -> restored ready
- Files actually changed: exactly the four declared shell files plus mandatory progress/diary records
- Command/check executed: `python3 Field_Coder/tests/test_shell.py` against an exact local mirror of the checked-in Step 01 files
- Exit status/result: PASS — exit 0
- Observed behavior: `PASS: initial FIELD_SHELL_READY`; `PASS: deliberate missing component detected`; `PASS: restored FIELD_SHELL_READY`
- What worked: deterministic controller status; deliberate component-loss detection; guaranteed restoration via `finally`; restored ready state
- What failed: shallow GitHub clone execution path could not resolve `github.com`; code itself was tested unchanged via exact local mirror
- What was learned: shell behavior passed unchanged
- Decision: KEEP
- Next permitted action: transition `field-coder/02-state-memory` onto the completed Step 01 lineage
- Hard-stop status: SATISFIED
- Blockers: none

---

## Entry 0005 — Step 02 state-memory pre-pass

- Date/time: 2026-08-19 20:03 America/Los_Angeles
- Branch: `field-coder/02-state-memory`
- Step: 02 — Persistent Field state
- Goal: persist and restore Field's exact working state across restarts while rejecting invalid/incomplete state
- Hard-start check: PASS — Step 02 moved to completed Step 01 lineage; full Field control set reread; Step 01 hard-stop evidence confirmed
- Known-good state: Step 01 shell passes all required checks
- Attempt: 1/3
- Intended change: add only a validated Field state schema, JSON save/load behavior, and state-only tests
- Files expected to change: `Field_Coder/field/state.py`, `Field_Coder/tests/test_state.py`
- Must remain unchanged: Step 01 shell behavior; task intake; repo reading; model/editor/diff/retry/Void behavior
- Exact success test: valid state save -> reload exact equality; missing required field rejected; invalid attempt bounds rejected; Step 01 shell regression remains passing
- Files actually changed: pending
- Command/check executed: pending
- Exit status/result: pending
- Observed behavior: pending
- What worked: Step 02 hard-start/read discipline completed
- What failed: none
- What was learned: Step 02 is limited to persistence/validation; it stores attempt fields but does not implement retry logic
- Decision: KEEP
- Next permitted action: create the two declared state files and run Step 02 state test plus Step 01 shell regression
- Hard-stop status: NOT YET SATISFIED
- Blockers: none

---

## Entry 0006 — Step 02 persistent state completed

- Date/time: 2026-08-19 20:03 America/Los_Angeles
- Branch: `field-coder/02-state-memory`
- Step: 02 — Persistent Field state
- Goal: prove exact Field state persistence across process restart and reject invalid state
- Hard-start check: PASS
- Known-good state: Step 01 shell verified
- Attempt: 1/3
- Intended change: add only `state.py` and `test_state.py`
- Files expected to change: `Field_Coder/field/state.py`, `Field_Coder/tests/test_state.py`
- Must remain unchanged: Step 01 shell and all Step 03+ behavior
- Exact success test: fresh-process exact restoration; missing field rejection; invalid attempt rejection; Step 01 regression pass
- Files actually changed: exactly the two declared Step 02 implementation/test files plus mandatory progress/diary records
- Command/check executed: `python3 Field_Coder/tests/test_state.py`; `python3 Field_Coder/tests/test_shell.py` against exact local mirror of checked-in lineage
- Exit status/result: PASS — both commands exit 0
- Observed behavior: exact state restored in fresh process; missing required state rejected; invalid attempt bounds rejected; Step 01 shell remained fully passing
- What worked: frozen dataclass schema; strict required/extra field checking; attempt-bound validation; JSON-serializable result validation; save/load persistence
- What failed: nothing in implementation or tests
- What was learned: Field now has durable validated working state without implementing task or retry behavior early
- Decision: KEEP
- Next permitted action: transition `field-coder/03-task-intake` to this completed Step 02 lineage and begin only Step 03 task-intake work after rereading controls
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
