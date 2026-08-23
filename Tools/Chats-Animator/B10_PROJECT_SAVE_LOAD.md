# B10 — Project Save / Load

**Status: RUNTIME PASS**

## Hard Start
B9 sprite-sheet slicer runtime PASS.

## Patch Strategy
Added `b10-project-save-load.js` and wired it after B9. Earlier stages remain separate and protected.

## What Worked
- Save the complete reel to one `.owav` JSON project file.
- Embedded background/artwork data survives because frame snapshots are preserved.
- Frame order and frame holds survive.
- Active frame index survives.
- Project FPS survives and is restored through the existing playback control.
- Calibration, placement/depth, manual scale, and selection state survive inside snapshots.
- Malformed project files are rejected before mutating the current reel.

## Runtime Verification
Chromium/Playwright bench test passed:
- 2-frame project serialized with correct holds and FPS;
- 3-frame project restored at the requested active index and FPS;
- malformed frame data threw a controlled validation error;
- existing project frame count stayed unchanged after malformed-load rejection;
- project download produced a `.owav` file;
- zero browser page errors.

## Hard Stop
B10 does not add audio, camera animation, tweening, or video export.

## Next
B11 — Audio track import + timeline sync.
