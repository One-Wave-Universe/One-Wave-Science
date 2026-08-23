# CHATGPT PROJECT — ONE-WAVE VIDEO MAKER

## CURRENT STEP
**B9 — Sprite-sheet slicer / pose-sheet extraction**

## STATUS
**IMPLEMENTED — repository integration verified; browser smoke test pending**

## ACTIVE BRANCH
`animator/b9-sprite-sheet-slicer`

## HARD START
B8 already supported naturally sorted multi-file pose import and a repository-backed runnable JavaScript checkpoint. B9 starts from that exact branch state.

## WHAT CHANGED
Added `b9-sprite-sheet-slicer.js` with:
- one pose-sheet image loader;
- manual rows and columns, 1–24 each;
- visible preview grid over the loaded sheet;
- row-major equal-cell slicing through canvas;
- PNG slice generation preserving transparency;
- adjustable 1x–12x hold per generated slice;
- insertion of one consecutive reel frame per slice;
- preservation of selected asset identity, x position, ground/depth, manual scale, background, and calibration through the existing B4 snapshot model.

`b8-batch-pose-import.js` was changed only to load the isolated B9 feature after B8 initialization. Existing B8 batch import remains intact.

## VERIFICATION
- B9 branch was created directly from `animator/b8-runnable-restore`.
- New B9 source was written successfully and fetched back from GitHub.
- B8 loader integration was written successfully.
- Branch control/diary file `B9_SPRITE_SHEET_SLICER.md` records scope, protected features, tests, Field/Void notes, and hard stop.

A real browser click-through of image load → grid preview → slice → generated reel frames is still pending. Do not label B9 browser-runtime PASS until that is performed.

## PROTECTED WORKING FEATURES
B1 through B8 contracts remain protected: background loading/calibration, depth-aware character/prop placement, ordered frame reel, pose editing, onion skin, playback, and batch multi-file pose import.

## HARD STOP
B9 stops at manual equal-cell rows/columns → preview → consecutive frame extraction. No automatic pose recognition, tweening, artwork generation, audio, camera, or export was added.

## NEXT PERMITTED STEP
Browser smoke-test B1–B9 together. If it passes, the next bounded slicing improvement may add adjustable gutters/margins or transparent-cell filtering.
