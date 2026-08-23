# B12 — Per-Frame Camera Pan / Zoom

**Status: RUNTIME PASS**

B12 stores camera X, Y, and zoom in each reel snapshot. Background, assets, and onion layer receive the same transform, and playback restores the camera with each frame.

Chromium/Playwright verification passed for snapshot storage, restore, transform application, UI synchronization, reset, and zero page errors.

## Next
B13 — Video export.
