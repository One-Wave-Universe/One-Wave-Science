# B9 — Sprite-Sheet Slicer / Pose-Sheet Extraction

**Status: STATIC PASS — syntax verified**

## Hard Start
B8 batch PNG pose import PASS.

## Repair First
The GitHub backup was not runnable because the HTML referenced B1–B8 JavaScript files that were absent from the saved backup. Before B9, the missing runtime chain was restored as separate patch files:
- `app.js`
- `b4-frame-reel.js`
- `b5-pose-editing.js`
- `b6-onion-skin.js`
- `b7-playback.js`
- `b8-batch-pose-import.js`

All restored JavaScript plus B9 pass `node --check`.

## B9 Workflow
1. Select an existing character or prop.
2. Choose `Slice Sprite / Pose Sheet`.
3. Select one PNG/WebP/JPEG sprite or pose sheet.
4. Set sheet rows and columns (1–16 each).
5. Set the default hold length for extracted poses.
6. Cells are read left-to-right, top-to-bottom.
7. Fully transparent/blank cells are skipped.
8. Nonblank cells become PNG pose images on consecutive reel frames after the current frame.
9. Character/prop identity, X position, feet/base depth, manual scale trim, background, and calibration remain inherited from the source frame.
10. The first extracted pose becomes the active frame.

## Protected Working Features
B1 through B8 remain separate and are not intentionally replaced by B9.

## Hard Stop
B9 does not add:
- tweening;
- AI-generated artwork;
- automatic action naming;
- audio;
- camera animation;
- export.

## Verification Still Required
A real browser smoke test is still required for UI interaction and actual canvas sprite extraction.

## Next Gate
Do not start B10 until B9 gets a browser smoke-test PASS.
