# Chat's Animator — Repository Backup

This directory is the GitHub backup/home for the current ChatGPT-built One-Wave Animator checkpoint while the standalone `Chats-Animatateo` repository is empty.

## Current checkpoint
B9 — Sprite-Sheet Slicer / Pose-Sheet Extraction.

## Important state
The JavaScript runtime chain referenced by `index.html` has been restored in this backup:
- `app.js`
- `b4-frame-reel.js`
- `b5-pose-editing.js`
- `b6-onion-skin.js`
- `b7-playback.js`
- `b8-batch-pose-import.js`
- `b9-sprite-sheet-slicer.js`

All seven JavaScript files pass static `node --check` syntax verification. A real browser smoke test is still required before B9 is considered runtime-verified.

## Protected direction
- Background first, calibrated perspective/depth grid.
- Grid is editor-only and never exported.
- Characters/props live in scene/world coordinates.
- Stop-motion / frame-reel animation with explicit frame holds.
- Human + AI co-edit the same project state.
- B8 supports many separate pose PNGs in one import.
- B9 supports slicing one sprite/pose sheet into consecutive frames.

## Next gate
Browser smoke-test B9. Do not begin B10 until B9 receives a runtime PASS.
