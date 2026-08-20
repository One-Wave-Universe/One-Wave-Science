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
