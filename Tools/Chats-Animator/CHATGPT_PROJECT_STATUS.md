# CHATGPT PROJECT — ONE-WAVE VIDEO MAKER

## CURRENT STEP
**B10 — Project save / load**

## STATUS
**RUNTIME PASS**

## HARD START
B9 sprite-sheet slicer runtime PASS.

## B9 RUNTIME GATE CLEARED
B9 was exercised inside Chromium through Playwright using the actual slicer logic and a generated 1x4 sprite sheet containing three opaque pose cells and one fully transparent blank cell.

Runtime result:
- 3 nonblank cells extracted into 3 consecutive reel frames;
- blank transparent cell skipped;
- first extracted pose became active;
- 2x frame holds preserved;
- character X, feet/base depth, manual scale, background, and calibration preserved;
- extracted artwork became PNG data URLs;
- zero browser page errors.

## B10 WHAT CHANGED
- Added `b10-project-save-load.js`.
- Added Save Project and Open Project controls.
- Project format is readable JSON stored as `.owav`.
- Complete reel frames and snapshots are serialized.
- FPS and active-frame index are serialized.
- Save uses one downloadable project file.
- Load validates before replacing the live reel.
- FPS is restored through the existing playback control.
- Malformed project files fail safely without modifying the current reel.

## B10 RUNTIME VERIFICATION
Chromium/Playwright bench test passed:
- serialized frame order, holds, FPS, and active index correctly;
- restored a 3-frame project at FPS 18 and active frame 3;
- malformed frame data was rejected;
- live frame count remained unchanged after malformed rejection;
- `.owav` download was produced;
- zero browser page errors.

## PROTECTED WORKING FEATURES
B1 through B9 remain intact: background/calibration, scene placement/depth sizing, frame reel/holds, pose editing, onion skin, playback, batch pose import, sprite-sheet slicing, and the B5 frame-reorder integrity repair.

## HARD STOP
B10 does not yet:
- add audio;
- animate camera;
- tween poses;
- export finished video.

## NEXT PERMITTED STEP
**B11 — Audio track import + timeline sync.**

Production-output priority after B11:
**B12 camera movement → B13 video export.** Tweening stays later so the animator can produce real videos sooner.
