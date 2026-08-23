# B4 — Frame Reel / Still-Frame Sequence Foundation

**Status: PASS**

## Hard Start
B3 character/prop placement PASS.

## Patch Strategy
B4 does not rewrite B3. It adds:
- `b4-frame-reel.js`
- a small reel panel in `index.html`
- B4 status/check/branch notes

## What Worked
- Ordered frame list.
- Stable frame IDs.
- Visible frame numbers.
- Add, duplicate, delete.
- Full scene snapshots per frame.
- Frame selection restores stored visual state.
- Per-frame hold length 1x–12x.
- Default 2x hold.

## Why This Matters
The Animator now has an animation data structure instead of only a scene editor.

The hold value supports limited-animation timing without requiring a unique PNG for every project FPS frame.

## Not Changed
- No playback.
- No tweening.
- No onion skin.
- No sprite-sheet slicing.
- No audio.
- No camera.
- No export.

## Notes to Self
Start B5 from this B4 PASS and patch only the next behavior. Do not rebuild B1-B4.

Keep Dual Mirror Gate edit mode and Lazy Human mode in later editor planning.

## Next
B5 — Frame editing workflow / pose-to-pose reel operations.
