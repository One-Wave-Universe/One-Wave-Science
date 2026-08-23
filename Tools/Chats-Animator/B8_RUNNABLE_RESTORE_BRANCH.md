# Branch-Step — Restore Runnable B8

## MAIN GOAL
Preserve the One-Wave Animator as a reliable human + AI collaborative frame-by-frame video-making application with a complete runnable repository checkpoint.

## WHY THIS STEP EXISTS
The B8 HTML shell and branch notes were backed up, but the six JavaScript implementation files referenced by `index.html` were absent from the repository checkpoint. New feature work must not continue on a broken foundation.

## CURRENT STEP GOAL
Restore the smallest complete B8 JavaScript runtime required by the existing HTML without adding B9 or later features.

## HARD START
- Repository: `One-Wave-Universe/One-Wave-Science`
- Animator path: `Tools/Chats-Animator/`
- Base: `main`
- Base HEAD: `8c79920832557864bf6921bdd95ae418603e62b3`
- Active branch: `animator/b8-runnable-restore`

## REFERENCE FILES
- `AGENTS.md`
- `Tools/Chats-Animator/index.html`
- `B3_CHARACTER_PROP_PLACEMENT.md`
- `B4_FRAME_REEL_FOUNDATION.md`
- `B5_POSE_TO_POSE_EDITING.md`
- `B6_ONION_SKIN.md`
- `B7_REPAIR_AND_PLAYBACK.md`
- `B8_BATCH_POSE_IMPORT.md`

## ALLOWED FILES
- `app.js`
- `b4-frame-reel.js`
- `b5-pose-editing.js`
- `b6-onion-skin.js`
- `b7-playback.js`
- `b8-batch-pose-import.js`
- this branch control note

## PROTECTED WORKING FEATURES
- Background load/remove and calibration.
- Grid visible only during calibration/placement work.
- Character/prop placement by normalized X and feet/base depth.
- Depth-based automatic scale plus manual trim.
- Ordered frame reel and stable frame snapshots.
- 1x–12x frame holds.
- Insert/reorder/replace/copy pose operations.
- Previous/next onion skin.
- 1–60 FPS playback with hold expansion.
- Multi-file naturally sorted batch pose import.

## EXACT ACTION
Restore only the six missing implementation files required by the existing B8 `index.html` script tags.

## SUCCESS CRITERIA
1. All six JavaScript files exist on the branch.
2. Each file parses with `node --check` against the exact locally reconstructed content.
3. Existing `index.html` references all six files in dependency order.
4. No B9 sprite-sheet slicing, tweening, audio, camera, export, or AI generation is added.

## TESTS / CHECKS
Local reconstruction test:
`node --check app.js b4-frame-reel.js b5-pose-editing.js b6-onion-skin.js b7-playback.js b8-batch-pose-import.js`

Result: PASS for all six files before repository write.

Repository existence check: required after commit.

Browser interaction smoke test: still pending; syntax/static PASS is not being mislabeled as full browser verification.

## FIELD NOTES
The implementation was reconstructed from the existing B3–B8 branch contracts and the exact B8 HTML controls/script dependency order. The change stays deliberately inside the missing runtime surface.

## VOID OVERSIGHT / OVERRIDE NOTES
ALLOW restoration because the repository checkpoint was incomplete and feature advancement would otherwise build on a false known-good state. HOLD B9 until this branch is confirmed complete.

## PROGRESS REPORT
- Branch created from the backed-up B8 main HEAD.
- `app.js` restored.
- B4 frame reel runtime restored.
- B5 pose editing runtime restored.
- B6 onion skin runtime restored.
- B7 playback runtime restored.
- B8 batch pose import runtime restored.

## ATTEMPT / STRIKE COUNT
Approach 1/3 — PASS static/syntax reconstruction.

## LOOK-BACK REFLECTION
What changed: the repository now contains the implementation files that its B8 HTML already expected.

What worked: all reconstructed JavaScript parses successfully with Node syntax checking.

What did not work: no full browser click-through test has been performed in this branch yet.

Evidence: six local `node --check` passes plus repository file existence verification.

Assumption changed: prior B8 PASS notes were insufficient as a repository checkpoint because the implementation files were absent.

Protected software: no later feature was introduced and the existing B8 HTML contract was preserved.

## HARD STOP
STOP when all six runtime files are present on `animator/b8-runnable-restore` and repository existence is verified. Do not begin B9 in this branch.

## HANDOFF / NEXT PERMITTED STEP
After this branch is accepted as the runnable B8 checkpoint: create a new branch for **B9 — Sprite-sheet slicer / pose-sheet extraction**.
