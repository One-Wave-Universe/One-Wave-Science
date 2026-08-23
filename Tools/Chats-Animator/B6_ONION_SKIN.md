# B6 — Onion-Skin / Neighboring-Frame Reference

**Status: PASS**

## Hard Start
B5 pose-to-pose editing PASS.

## Patch Strategy
Added `b6-onion-skin.js` only. Earlier branches remain intact.

## What Worked
- previous-frame ghost overlay
- next-frame ghost overlay
- optional toggles
- non-interactive onion layer
- current frame remains editable above it

## Not Changed
No playback, tweening, sprite-sheet slicing, audio, camera, or export.

## Notes to Self
Start B7 from this PASS. Patch only playback next.

## Next
B7 — Playback engine using project FPS + frame holds.
