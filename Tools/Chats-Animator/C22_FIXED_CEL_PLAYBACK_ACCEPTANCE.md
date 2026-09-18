# C22 — Fixed-Cel Playback Acceptance

**Target layer:** 05 Renderer and Playback, with a small 10 Interface demo hook.

## Failure being prevented

A single image moving across the stage is not accepted as proof of frame animation.

## Acceptance demo

The toolbar action **Load 12-Cel GR Demo** loads the existing Goblin Raccoon
`gr-walk-right-12-cel-sheet.svg` as a 4×3 sheet and builds twelve ordinary reel
frames.

The acceptance invariant is:

```text
12 reel frames
12 distinct cel drawings
same character x on every frame
same character groundY on every frame
same character manualScale on every frame
24 FPS
2-frame exposure per drawing
```

Playback therefore changes the drawing at a fixed stage position. Motion across
the scene is a separate authored transform operation and is not used to fake the
cel-animation qualification.

## Regression

```bash
node c22-fixed-cel-demo.test.js
```

The regression fails if the demo uses fewer than twelve drawings or changes the
fixed transform across the twelve snapshots.

The old `One_Wave_Bench/media/goblin_raccoon/render_moving_layer_demo.py`
remains historical/noncanonical and is not an Animator acceptance path.
