# B5 — Pose-to-Pose Reel Editing

**Status: PASS**

## Hard Start
B4 frame reel PASS.

## Patch Strategy
Added `b5-pose-editing.js`; prior scene/reel code remains intact.

## What Worked
- insert before/after
- frame reorder left/right
- replace selected PNG on current frame
- copy selected pose to adjacent frame
- background/calibration preserved
- frame hold preserved

## Not Changed
No playback, onion skin, tweening, sprite-sheet slicing, audio, camera, or export.

## Notes to Self
Start B6 from this PASS checkpoint. Patch forward only.

## Next
B6 — Onion-skin / neighboring-frame visual reference.
