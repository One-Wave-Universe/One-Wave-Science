# CHATGPT PROJECT — ONE-WAVE VIDEO MAKER

## CURRENT STEP
**B9 — Sprite-sheet slicer / pose-sheet extraction**

## STATUS
**STATIC PASS — syntax verified; browser smoke test still required**

## HARD START
B8 batch PNG pose import PASS.

## REPAIR COMPLETED BEFORE B9
The GitHub backup had the B8 HTML shell and branch notes but was missing the JavaScript runtime files referenced by the page.

Restored:
- `app.js`
- `b4-frame-reel.js`
- `b5-pose-editing.js`
- `b6-onion-skin.js`
- `b7-playback.js`
- `b8-batch-pose-import.js`

## B9 WHAT CHANGED
- Added `b9-sprite-sheet-slicer.js`.
- Added sprite/pose-sheet file picker.
- Added configurable sheet rows and columns, 1–16 each.
- Added selectable default hold length for extracted poses.
- Sheet cells extract left-to-right, top-to-bottom.
- Fully transparent/blank cells are skipped.
- Extracted cells become PNG pose artwork on consecutive reel frames after the current frame.
- Selected character/prop identity is preserved.
- Background and calibration are preserved.
- Character/prop X position is preserved.
- Feet/base depth is preserved.
- Manual scale trim is preserved.
- First extracted pose becomes the active frame.

## PROTECTED WORKING FEATURES
B1 through B8 remain separate patch stages, including frame holds, pose editing, onion skin, playback, and batch pose import.

## HARD STOP
B9 does not yet:
- tween poses;
- auto-generate new artwork;
- auto-detect action names;
- add audio;
- add camera animation;
- export video.

## VERIFICATION
All reconstructed B1–B8 JavaScript and B9 pass `node --check`.

A real browser interaction test is still required before B9 can be called fully bench-tested.

## NEXT PERMITTED STEP
**Browser smoke-test B9. Do not begin B10 until B9 gets a runtime PASS.**
