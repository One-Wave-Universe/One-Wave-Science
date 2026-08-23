# B7 — Repair + Playback

**Status: PASS (static/syntax verified)**

## Repair found
The stronger B6 check found that the saved artifact chain was missing `app.js` and `b4-frame-reel.js`, even though later HTML referenced them.

## Smallest repair
- reconstructed the missing B3-compatible core in `app.js`;
- reconstructed B4 reel operations in `b4-frame-reel.js`;
- retained B5 pose editing and B6 onion-skin patches;
- added B7 playback in `b7-playback.js`.

## Playback
- project FPS is adjustable 1–60;
- default 24 FPS;
- reel frame hold values are expanded during playback;
- 1x/2x/3x and longer holds now affect screen duration;
- playback hides editor calibration/placement overlays.

## Verification
All JavaScript files pass `node --check`.

Browser interaction still needs a real user/browser smoke test before calling every UI path fully bench-tested.
