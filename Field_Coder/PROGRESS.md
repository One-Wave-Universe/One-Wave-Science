# Field Coder — Progress Report

## Project
- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/14-real-repo-trial`
- Current step: 14 — First real controlled task
- Status: IN PROGRESS
- Attempt: 1/3

## Completed steps
- Steps 00-13: COMPLETE

## Hard-start evidence
- Step 13 hard stop satisfied and inherited.
- Full Field control set and latest diary reread on this branch.
- Real target confirmed under `One_Wave_Animator/` with existing scene-model tests.

## Selected real task
Fix `_to_portable_path()` in `One_Wave_Animator/app/scene_model.py` so an in-folder filename beginning with `..` (for example `..hero.png`) remains a relative portable path instead of being falsely classified as a parent-directory path.

## Why this task is bounded
Current code uses `rel_path.startswith("..")`, which conflates a basename beginning with two dots with an actual path that traverses to the parent. The fix is limited to the parent-path boundary check.

## Allowed scope
- `One_Wave_Animator/app/scene_model.py`
- narrowly required regression verification for this exact behavior only

## Exact success test
1. existing scene-model tests remain passing;
2. an asset inside the scene directory named `..hero.png` serializes as `..hero.png`, not an absolute path;
3. a true asset outside the scene directory still serializes as an absolute path;
4. candidate diff contains only the bounded scene-model fix plus its narrowly required test if added;
5. review packet remains `PENDING_EXTERNAL_REVIEW`.

## Hard stop
Stop after this first real task produces a review-ready candidate packet. Do not begin another animator task, production autonomy, or Void implementation.