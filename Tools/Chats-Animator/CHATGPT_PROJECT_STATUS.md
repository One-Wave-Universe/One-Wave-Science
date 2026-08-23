# CHATGPT PROJECT — ONE-WAVE VIDEO MAKER

## CURRENT STEP
**B8 — Batch PNG pose import**

## STATUS
**PASS — static/syntax verified**

## HARD START
B7 repaired playback PASS.

## WHAT CHANGED
- Added multi-file PNG/image pose picker.
- Batch files sort naturally by filename.
- Selected character/prop identity is used as the batch target.
- Imported poses become consecutive reel frames after the current frame.
- Background is preserved.
- Background calibration is preserved.
- Character/prop X position is preserved.
- Feet/base depth is preserved.
- Manual scale trim is preserved.
- Each imported frame receives a selectable default hold length.
- First imported pose becomes the active frame.

## WHY
This removes the one-PNG-at-a-time bottleneck and starts the Lazy Human production workflow.

A folder like:
`walk_01.png ... walk_12.png`
can now become an ordered pose sequence in one import action.

## PROTECTED WORKING FEATURES
B1 through B7 remain intact, including playback and frame holds.

## HARD STOP
B8 does not yet:
- slice one sprite sheet into cells;
- auto-generate new artwork;
- auto-detect action names;
- tween poses;
- add audio/camera/export.

## NEXT PERMITTED STEP
**B9 — Sprite-sheet slicer / pose-sheet extraction**
