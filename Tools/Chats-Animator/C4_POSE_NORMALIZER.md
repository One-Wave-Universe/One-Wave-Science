# C4 — Pre-Layout Pose Normalizer

**Status: RUNTIME PASS**

C4 enforces the rule that pose stills are normalized before they are laid onto a path. For a selected consecutive pose run it trims transparent padding, rescales visible artwork onto one square transparent canvas, centers it horizontally, and bottom-anchors the visible subject to one consistent line.

Chromium verification used three deliberately mismatched transparent source images. All outputs became 512×512 and their visible artwork ended on the same bottom pixel line (15 px margin), with zero browser errors.

## Production order
Normalize → Path → Cadence → One-click walk → Audio/Camera → Export.
