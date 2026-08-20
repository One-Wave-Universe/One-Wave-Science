# Field Coder — Step 14 External Review Packet

## Status

- Candidate status: `REVIEW_READY_CANDIDATE`
- Architecture verdict: `PENDING_EXTERNAL_REVIEW`
- Trial branch: `field-coder/14-real-repo-trial`
- Base known-good Field build commit: `4f2843aad4e2cc54fb258713aed093a5ce439902`

## Goal

Complete the first tiny real repository task with bounded scope and produce evidence for external review without Field self-approval.

## Task

Fix One-Wave Animator scene portability when an asset is inside the scene directory but its legal filename begins with two dots, such as `..hero.png`.

## Grounded cause

`One_Wave_Animator/app/scene_model.py::_to_portable_path()` used:

```python
if rel_path.startswith(".."):
    return abs_path
```

That condition matches both:

- a true parent path such as `../outside.png`, and
- a legal in-directory basename such as `..hero.png`.

## Proposal

Replace the prefix test with a path-component boundary test:

```python
if rel_path == os.pardir or rel_path.startswith(os.pardir + os.sep):
    return abs_path
```

Preserve all other scene serialization behavior.

## Files changed

- `One_Wave_Animator/app/scene_model.py`
- `One_Wave_Animator/tests/test_scene_model.py`

## Verification evidence

Before the fix, the exact checked-in source plus the narrow regression produced:

- 4 existing scene-model tests passed
- `test_double_dot_prefixed_filename_inside_scene_stays_portable` failed
- the stored scene JSON contained an absolute path for `..hero.png`

After the fix:

- 5/5 scene-model tests passed
- `..hero.png` stayed relative
- a true asset outside the scene directory remained absolute

## Diff boundary

Animator implementation diff:

- `scene_model.py`: 1 addition / 1 deletion
- `test_scene_model.py`: 27 additions
- no other animator files changed

Field progress/diary records were updated separately as required by the build protocol.

## Attempt record

- Attempt 1: PASS after reproducing the defect and applying the single bounded correction.
- No repair retry was required for the production candidate.

## Remaining uncertainty

- External architecture/reviewer acceptance has not occurred.
- No GUI-level behavior was changed or required for this scene-model-only defect.
- The candidate has not been merged to `main`.

## Field authority boundary

Field does **not** approve this candidate architecturally.

Final architecture verdict remains:

`PENDING_EXTERNAL_REVIEW`
