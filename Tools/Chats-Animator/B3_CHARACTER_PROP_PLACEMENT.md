# B3 — Character / Prop Placement

**Status: PASS**

## Main Goal
Place PNG characters and props into the calibrated background scene without adding animation yet.

## Hard Start
B2 — Background Calibration / Sizing-Grid Setup.

## Files Changed
- `app.js`
- `index.html`
- `CHATGPT_PROJECT_STATUS.md`
- `B3_CHARACTER_PROP_PLACEMENT.md`
- `B3_CHECK.json`

## What Worked
- PNG/image import for characters and props.
- Shared scene-state storage for placed instances.
- Position control using normalized scene coordinates.
- Ground/feet depth reference.
- Automatic scale interpolation from far-to-near background calibration.
- Manual scale trim.
- Placement mode shows grid.
- Finishing placement hides grid.
- Existing B1/B2 behavior carried forward.

## What Was Not Changed
- No frame sequencing.
- No playback.
- No sprite sheet slicing.
- No sound.
- No export.

## Notes to Self
Do not rewrite B1/B2 on later branches. Build from this B3 PASS and patch only the next feature.

Dual Mirror Gate edit mode and Lazy Human mode remain required future features; do not silently lose them.

## Look-Back Reflection
The background-calibrated grid now has a concrete purpose: feet/base depth drives automatic size. This validates the decision to keep the grid temporary instead of baking it into the scene.

## Hard Stop
B3 ends once still characters/props can be placed and sized from background calibration.

## Next
B4 — Frame reel / still-frame sequence foundation.
