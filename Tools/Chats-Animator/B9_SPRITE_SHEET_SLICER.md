# B9 — SPRITE-SHEET SLICER / POSE-SHEET EXTRACTION

## MAIN GOAL
Build the One-Wave Video Maker as a human + AI collaborative frame-by-frame animation application with explicit reel frames, depth-aware placement, editable holds, and reusable pose workflows.

## WHY THIS STEP EXISTS
B8 can import many already-separated pose PNGs, but a common animation asset is one large pose sheet containing many cells. B9 removes the manual external-cropping step by extracting those cells directly into reel frames.

## CURRENT STEP GOAL
Add one bounded manual sprite-sheet slicer: load one pose sheet, choose rows and columns, preview the slice grid, and create consecutive reel frames from the cells.

## HARD START
Branch from the verified repository-backed B8 runnable checkpoint: `animator/b8-runnable-restore`.

## LOCAL REPO ROOT
`$HOME/One-Wave-Science`

## ACTIVE BRANCH / WORKTREE / HEAD
Branch: `animator/b9-sprite-sheet-slicer`

## REFERENCE FILES
- `AGENTS.md`
- `Tools/Chats-Animator/CHATGPT_PROJECT_STATUS.md`
- `Tools/Chats-Animator/b4-frame-reel.js`
- `Tools/Chats-Animator/b8-batch-pose-import.js`
- `Tools/Chats-Animator/B8_BATCH_POSE_IMPORT.md`
- `Tools/Chats-Animator/B8_RUNNABLE_RESTORE_BRANCH.md`

## ALLOWED FILES
- `Tools/Chats-Animator/b9-sprite-sheet-slicer.js`
- `Tools/Chats-Animator/b8-batch-pose-import.js` only for loading the isolated B9 feature after B8 is initialized
- `Tools/Chats-Animator/B9_SPRITE_SHEET_SLICER.md`
- `Tools/Chats-Animator/CHATGPT_PROJECT_STATUS.md`

## PROTECTED WORKING FEATURES
B1–B8 behavior remains intact: background loading/calibration, depth-aware placement, frame reel, pose editing, onion skin, playback, and multi-file batch pose import.

## EXACT ACTION
1. Add an isolated B9 sprite-sheet slicer file.
2. Load it only after B8 runtime APIs are available.
3. Require a selected character/prop before slicing.
4. Load one PNG/JPEG/WebP pose sheet.
5. Let the user set manual row and column counts from 1–24.
6. Draw a preview grid over the loaded sheet.
7. Slice cells in row-major order using canvas.
8. Preserve the selected asset identity, scene position, ground/depth, manual scale, background, and calibration by modifying only that asset inside B4 snapshots.
9. Create one consecutive reel frame per slice with an adjustable 1x–12x hold.
10. Restore/select the first inserted slice frame when complete.

## SUCCESS CRITERIA
- B9 feature file exists on the branch.
- Manual row/column controls exist.
- Preview grid reflects the chosen rows/columns.
- One sheet can produce N = rows × columns PNG-backed frame snapshots.
- Frame order is left-to-right, top-to-bottom.
- Existing asset placement and scene state are carried forward.
- B8 multi-file import remains available.
- No B10 feature is introduced.

## TESTS / CHECKS
Repository-level checks:
- Branch created from `animator/b8-runnable-restore`.
- B9 feature file written to repository.
- B8 loader changed only to append the isolated B9 script after B8 initialization.
- Repository files re-fetched after write for presence/content verification.

Browser click-through is still required before labeling the feature browser-runtime verified. This branch does not claim that unperformed test.

## FIELD NOTES
The smallest B9 implementation is manual rows/columns rather than automatic pose detection. That keeps the crop rule visible, reversible, and understandable while reusing the already-working B4 snapshot/reel mechanism.

## VOID OVERSIGHT / OVERRIDE NOTES
ALLOW with boundary: B9 may extract cells and feed them into the existing frame mechanism, but may not add automatic artwork generation, tweening, audio, camera, export, or image-recognition-based pose detection.

## PROGRESS REPORT
- Created `animator/b9-sprite-sheet-slicer` from the B8 runnable branch.
- Added `b9-sprite-sheet-slicer.js`.
- Added manual rows/columns, preview canvas/grid, per-slice hold, and frame extraction.
- Preserved selected asset ID and scene snapshot fields.
- Updated B8 only to load the isolated B9 script after B8 initialization.

## ATTEMPT / STRIKE COUNT
Approach 1 — manual equal-cell row/column slicing: Attempt 1/3. No strike recorded from repository-level verification.

## LOOK-BACK REFLECTION
### What changed?
The Animator can now turn one regular pose sheet into consecutive still-frame reel entries without requiring the poses to be manually exported as separate files first.

### What actually worked?
The repository branch and isolated feature integration were written successfully and use the existing B4 snapshot/reel APIs rather than creating a second frame system.

### What did not work?
No browser interaction test has been performed yet, so actual browser image decoding/canvas slicing/UI interaction remains pending verification.

### What evidence proves the result?
The branch contains the new B9 source and the B8 loader integration, with repository fetch used to verify the files after write.

### What did we learn?
B8's snapshot model is sufficient for sheet extraction: only the selected asset's image data/dimensions/name need to change per generated frame.

### Which assumption changed?
None of the B1–B8 contracts needed redesign to support sprite sheets.

### Did previously verified software still work?
No protected B1–B8 implementation was deliberately changed except the minimal B8 post-initialization loader. Full browser regression remains pending.

### Did this advance the MAIN GOAL?
Yes. It reduces repetitive human preprocessing and makes pose-sequence production more AI/human coeditable.

### State the next branch must inherit
A B9 branch containing B1–B8 plus manual equal-cell sprite-sheet extraction. Browser smoke testing should precede deeper slicing intelligence.

## HARD STOP
Stop at manual equal-cell rows/columns → preview → consecutive frame extraction.

## HANDOFF / NEXT PERMITTED STEP
First: browser smoke-test B1–B9 together. After that passes, the next bounded feature may add adjustable crop margins/gutters or transparent-cell filtering. Do not begin automatic pose detection in this branch.
