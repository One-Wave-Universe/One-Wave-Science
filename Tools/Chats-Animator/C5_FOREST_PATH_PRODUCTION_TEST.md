# C5 — Forest Path Production Test

**Status: PASS — production output created**

## Hard Start
C1–C4 production tools runtime PASS.

## Test
Rebuilt the Goblin Raccoon forest-path walk using the intended still-frame production method rather than optical-flow interpolation.

## Pipeline
1. Crop the 14 source walk stills.
2. Normalize every still to one 1024×768 frame size before reel layout.
3. Keep the away and toward pose order intact.
4. Clock playback at 24 FPS / 6 pose beats = 4 frames per pose.
5. Give the far turnaround pose a 12-frame hold.
6. Give the final near pose a short settle hold.
7. Export MP4, WebM, and GIF preview.

## Result
- 14 normalized key stills.
- 72 clock frames total.
- No optical-flow / synthetic tween frames.
- Motion remains visibly stop-motion / reel based.
- Size change reads through the authored depth sequence instead of hand-timed random holds.

## Production Lesson
The still-frame version better matches the core engine than the earlier optical-flow smoothing test. Future walk tools should preserve authored poses and improve path/depth/cadence without inventing in-between artwork unless explicitly requested.

## Next
C6 — first dialogue scene production test using real background + character poses + audio + camera + export.
