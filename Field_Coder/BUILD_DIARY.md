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
- Attempt: 1/3
- Result: fixture rejected before candidate creation
- Evidence: baseline Python test created untracked `__pycache__`; known-good gate correctly refused dirty source
- Decision: RETRY fixture only; workflow unchanged

## Entry 0030 — Step 13 sacrificial workflow completed
- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/13-sacrificial-repo`
- Step: 13 — End-to-end controlled proof
- Goal: prove composed Field behavior from bounded goal through repair and review-ready packet
- Hard-start check: PASS
- Known-good state: Steps 01-12 verified
- Attempt: 1/3 implementation; one evidence-based fixture correction
- Intended change: `workflow.py`, `test_sacrificial_workflow.py`
- Files actually changed: the two declared Step 13 files plus mandatory progress/diary records; second pass changed fixture setup only to commit `.gitignore`
- Command/check executed: sacrificial end-to-end test against local mirror of checked-in Step 13 contracts
- Exit status/result: PASS — exit 0 after fixture correction
- Observed behavior: clean baseline; attempt-1 bad edit and matching diff; failing declared test; evidence propagated to attempt 2; rollback; corrected edit; passing test; source unchanged; candidate inspectable; review packet pending external review
- What worked: all previously built component contracts composed successfully; three-attempt state used correctly; Git safety protected source; review packet withheld self-approval
- What failed: initial fixture ignored no Python cache files; known-good gate correctly caught it
- What was learned: repository hygiene is part of the known-good contract and must be explicit
- Decision: KEEP
- Next permitted action: transition `field-coder/14-real-repo-trial` to this completed Step 13 lineage, reread controls, select one tiny real repo task, and stop after its review-ready packet
- Hard-stop status: SATISFIED
- Blockers: none

## Entry 0031 — Step 14 real-repo trial pre-pass
- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/14-real-repo-trial`
- Step: 14 — First real controlled task
- Goal: run one tiny real animator defect through Field controls and stop at review-ready evidence
- Hard-start check: PASS — Step 13 completed; full controls and latest diary reread; real animator source/tests inspected
- Known-good state: Steps 01-13 verified
- Attempt: 1/3
- Selected task: fix `One_Wave_Animator/app/scene_model.py::_to_portable_path()` so an in-folder filename beginning with `..` is not mistaken for a parent-directory path
- Evidence: current condition was `rel_path.startswith("..")`; this also matched valid basenames such as `..hero.png`
- Files expected to change: `One_Wave_Animator/app/scene_model.py` and one narrow scene-model regression test
- Must remain unchanged: all other animator behavior/files; Field engine; no Void; no self-approval; no merge/push to main
- Exact success test: existing scene-model tests pass; in-folder `..hero.png` remains relative; true outside path remains absolute; bounded diff only; review packet pending external review
- Decision: KEEP

## Entry 0032 — Step 14 first real animator trial completed
- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/14-real-repo-trial`
- Step: 14 — First real controlled task
- Goal: correct one real animator portability defect without unrelated changes
- Hard-start check: PASS
- Known-good state: Step 13 completed and real target read from repository
- Attempt: 1/3
- Intended change: distinguish the actual parent path component `..` from legal filenames merely beginning with two dots
- Files actually changed: `One_Wave_Animator/app/scene_model.py`, `One_Wave_Animator/tests/test_scene_model.py`, plus mandatory Field progress/diary records
- Command/check executed: exact local Git slice of the checked-in real animator source; `python3 -m pytest -q tests/test_scene_model.py` before and after candidate
- Baseline result with new regression: FAIL as expected — 4 existing tests passed and `test_double_dot_prefixed_filename_inside_scene_stays_portable` failed because current code serialized an absolute path
- Candidate result: PASS — 5/5 scene-model tests passed
- Candidate source change: `rel_path.startswith("..")` -> `rel_path == os.pardir or rel_path.startswith(os.pardir + os.sep)`
- Regression coverage: legal in-folder `..hero.png` remains relative; true parent/outside asset remains absolute
- Branch diff audit from Step 13 baseline: only Field control records plus the two declared animator files; animator source change is 1 addition/1 deletion and test coverage is 27 additions
- What worked: the defect was reproduced before editing; one bounded condition corrected it; existing scene-model behavior remained passing; outside-path protection remained intact
- What failed: nothing in candidate implementation
- What was learned: prefix-string testing was too broad for filesystem component semantics; the parent marker must be matched as a complete path component
- Decision: KEEP — REVIEW_READY_CANDIDATE
- Architecture verdict: PENDING_EXTERNAL_REVIEW
- Next permitted action: none inside the Field Coder build list; Step 14 hard stop reached
- Hard-stop status: SATISFIED — stop after first real review packet; do not start another animator task or Void implementation
- Blockers: none

---

## Required template for any future authorized continuation
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
