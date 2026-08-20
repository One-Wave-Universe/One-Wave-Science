# Field Coder — Build Diary

This diary is mandatory project memory.

## Prior verified history
- Steps 00-13: PASS
- All prior hard stops: SATISFIED

## Entry 0031 — Step 14 real-repo trial pre-pass
- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/14-real-repo-trial`
- Step: 14 — First real controlled task
- Goal: run one tiny real animator defect through the Field workflow and stop at review-ready evidence
- Hard-start check: PASS — Step 13 completed; full controls and latest diary reread; real animator source/tests inspected
- Known-good state: Steps 01-13 verified
- Attempt: 1/3
- Selected task: fix `One_Wave_Animator/app/scene_model.py::_to_portable_path()` so an in-folder filename beginning with `..` is not mistaken for a parent-directory path
- Evidence: current condition is `rel_path.startswith("..")`; this also matches valid basenames such as `..hero.png`
- Files expected to change: `One_Wave_Animator/app/scene_model.py` and, only if needed, one narrow scene-model regression test
- Must remain unchanged: all other animator behavior/files; Field engine; no Void; no self-approval; no merge/push to main
- Exact success test: existing scene-model tests pass; in-folder `..hero.png` remains relative; true outside path remains absolute; bounded diff only; review packet pending external review
- Files actually changed: pending
- Command/check executed: pending
- Exit status/result: pending
- Observed behavior: pending
- What worked: Step 14 task selection was grounded in actual animator code and existing tests
- What failed: none
- What was learned: path traversal detection must distinguish the `..` path component from a legal basename prefix
- Decision: KEEP
- Next permitted action: execute this one real task through Field's controlled candidate workflow, inspect evidence, then publish only the review candidate on this branch if it passes
- Hard-stop status: NOT YET SATISFIED
- Blockers: none
