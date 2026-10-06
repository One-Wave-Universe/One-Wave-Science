# One-Wave Animator

This directory is the runnable desktop Animator product slice. It is intentionally separate from theory documents and simulation experiments.

## Install on Ubuntu / Jetson

```bash
cd animator
chmod +x install.sh
./install.sh
```

Then launch **One-Wave Animator** from the desktop application menu, or run:

```bash
~/.local/bin/one-wave-animator
```

## What v1 already does

- real desktop editor window
- 1280x720 scene canvas
- editor-only placement grid that disappears during playback
- PNG/JPEG/WebP/BMP image layers
- drag-to-position layers
- show/hide and lock/unlock layers
- per-layer first/last frame exposure
- timeline scrubbing
- timed playback at project FPS
- full-screen playback
- current playback-frame export to a 1280x720 PNG with the editor grid removed
- `.animator.json` save and reopen
- image source path preservation with missing-asset warnings

## Product rule

Animator is judged by the complete loop: **install -> open -> build a scene -> save -> reopen -> play -> export**. Architecture work that does not move that loop forward is secondary.

## Next vertical slices

1. Keyframes for position, scale and rotation with interpolation.
2. Background-derived perspective/grid anchors and explicit drift measurements.
3. Motion Atlas actions (walk toward/away, look, kick, reach, pick up, sniff).
4. Asset relinking/packing so projects can move between machines cleanly.
5. Video/reel export through a local encoder (PNG frame export is already available).
6. AI command panel that calls deterministic editor operations rather than directly mutating scene files.
7. Packaging as a distributable Ubuntu/Jetson installer rather than a development bootstrap script.

Do not replace the GUI with a terminal workflow. The terminal is only for installation/debugging.
