# One-Wave Animator

This is the restored FPS / exposure-sheet animator that previously reached runtime-tested production features before it was accidentally removed from `main`.

## What it is

A local frame-animation program for making short animated sections against a background, then exporting those sections as clips for assembly in a separate video editor.

The reel is the source of truth. Characters and props are transparent still drawings placed on a calibrated background. Each reel frame can hold a drawing for one or more FPS ticks, while position, depth, camera, and pose remain frame-editable.

This is not a single-image tween/moving-frame shortcut.

## Current production features

- configurable FPS reel, default 24 fps;
- explicit drawing holds / exposures;
- background loading and perspective/depth calibration grid;
- character and prop PNG placement;
- manual per-frame pose replacement and neighboring-frame copying;
- onion skin;
- batch pose import and sprite-sheet slicing;
- project save/load (`.owav`);
- reusable motion-sequence libraries (`.owmotion`);
- reusable character motion atlases (`.owatlas`);
- path/walk production tools;
- per-frame camera motion;
- full-reel WebM export;
- start/end section preview and WebM clip export for external editing.

## Ubuntu install / desktop shortcut

From this directory run:

```bash
bash install-ubuntu.sh
```

That creates **One-Wave Animator** in the Ubuntu application menu and a desktop shortcut. The launcher starts a local-only Python web server and opens the animator in Chromium app mode when Chromium is available, with Firefox/`xdg-open` fallback.

No cloud service is required just to open and edit the animator.

## Working method

1. Load a background.
2. Show the calibration grid, set perspective/depth, then hide the grid.
3. Add character/prop PNGs or insert a saved motion sequence.
4. Build and play the reel at the chosen FPS.
5. Edit any reel frame manually: pose, position, depth, scale, hold, camera, insertion/deletion/order.
6. Save useful actions into `.owmotion` / `.owatlas` archives.
7. Mark a start and end frame in **Clip / section export**.
8. Preview that section.
9. Export the section as WebM and assemble finished clips in the separate video editor.

## AI-director boundary

The animator data model is intentionally human-and-AI coeditable, but this local launcher does not pretend to contain ChatGPT. A real director/chat bridge must edit the same reel and motion-library structures rather than generating a second incompatible animation format.
