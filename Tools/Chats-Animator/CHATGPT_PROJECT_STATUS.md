# CHATGPT PROJECT — ONE-WAVE VIDEO MAKER

## CURRENT STEP
**B8 — Runnable checkpoint restoration**

## STATUS
**PASS — repository runtime restored; static/syntax verified**

## ACTIVE BRANCH
`animator/b8-runnable-restore`

## HARD START
The B8 HTML shell and documentation existed in the repository, but the six JavaScript implementation files referenced by `index.html` were missing.

## WHAT CHANGED
Restored the complete B8 runtime surface:
- `app.js` — background/calibration/character/prop placement core;
- `b4-frame-reel.js` — ordered still-frame reel, snapshots, holds;
- `b5-pose-editing.js` — insert/reorder/replace/copy pose operations;
- `b6-onion-skin.js` — neighboring-frame onion references;
- `b7-playback.js` — 1–60 FPS playback with hold expansion;
- `b8-batch-pose-import.js` — naturally sorted multi-image pose import.

## VERIFICATION
All six reconstructed JavaScript files passed `node --check` before repository write.

The branch directory was then fetched from GitHub to verify the restored runtime files and branch control record are present.

Full browser click-through remains pending; this is not being mislabeled as browser-runtime verification.

## PROTECTED WORKING FEATURES
B1 through B8 contracts are preserved. No B9 feature was added during restoration.

## HARD STOP
This branch stops at a complete repository-backed B8 runtime checkpoint.

## NEXT PERMITTED STEP
Create a new branch for **B9 — Sprite-sheet slicer / pose-sheet extraction**.
