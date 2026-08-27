# B8 — Batch PNG Pose Import

**Status: PASS — static/syntax verified**

## Hard Start
B7 repaired playback.

## Patch Strategy
One new file: `b8-batch-pose-import.js`.

## Workflow
1. Select an existing placed character or prop.
2. Click `Import Many Pose PNGs`.
3. Choose multiple images.
4. Files sort naturally by filename.
5. The app creates consecutive frames after the current frame.
6. Each frame keeps the selected asset's placement/depth/scale but replaces its artwork with the corresponding pose PNG.
7. Batch hold defaults to 2x and is adjustable before import.

## What Was Not Changed
No sprite-sheet slicing, tweening, AI generation, audio, camera, or export.

## Notes to Self
This is the first direct Lazy Human production accelerator.

## Next
B9 — Sprite-sheet slicer / pose-sheet extraction.
