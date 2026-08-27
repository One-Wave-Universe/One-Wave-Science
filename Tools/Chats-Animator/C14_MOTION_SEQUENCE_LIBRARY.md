# C14 — Reusable Motion Sequence Library

## Purpose
Add a dedicated reusable animation-sequence library to the animator. This is separate from the active-scene reel.

The user must be able to build a small set of reusable character motions, save them to one file, reopen them later, and insert any saved motion into a scene without rebuilding it.

## Initial capacity
The first production target is **5 reusable sequences per library file**. The data format should allow more later without redesign.

Suggested first GR library:
1. Walk cycle
2. Look / notice
3. Point
4. Wave
5. Flip-off gesture

These are examples, not hardcoded names. Slots can be renamed/replaced.

## Sequence contents
Each stored sequence keeps:
- sequence id
- sequence name
- character/asset identity tag
- source pose images or embedded data
- exact 24 fps exposure timing for every drawing
- frame holds (1s / 2s / 3s / longer holds)
- per-frame or per-timeline-frame placement offsets
- feet/base anchor
- depth/scale behavior mode
- optional camera-relative orientation
- loop / one-shot flag
- entry pose
- exit pose
- optional transition-in frames
- optional transition-out frames
- notes/tags

## Critical timing rule
The project remains a true **24 fps timeline**.

A reusable sequence stores drawing exposures separately from motion translation. Example: a walk pose can remain visible for 2 frames while X/depth changes on both individual timeline frames. Do not turn sequences into a fixed pose-beat clock.

## Library file
Use a readable JSON-based file initially:

`*.owmotion`

Format example:

```json
{
  "format": "one-wave-motion-library",
  "version": 1,
  "name": "GR Core Motions",
  "sequences": []
}
```

Artwork may be embedded as data URLs for portability in Phase 1. Later versions may support external asset references for large libraries.

## Required UI
Add a **Motion Library** panel with:
- New Library
- Open Library
- Save Library
- 5 visible sequence slots initially
- Capture Reel Range as Sequence
- Rename Sequence
- Delete/Replace Sequence
- Preview Sequence
- Insert Sequence at Current Reel Position
- Loop checkbox
- Character tag
- Notes/tags

## Capture behavior
`Capture Reel Range as Sequence` must:
1. ask/select start and end reel frames;
2. copy the sequence rather than moving it;
3. preserve pose art and true frame exposures;
4. convert scene-global position into sequence-relative offsets where appropriate;
5. store a stable feet/base anchor;
6. never damage the active reel.

## Insert behavior
`Insert Sequence at Current Reel Position` must:
1. duplicate stored sequence frames into the active scene;
2. preserve the current scene/background;
3. map the sequence to the selected character asset;
4. let user choose insertion anchor X/depth;
5. calculate perspective scale from active scene calibration;
6. retain relative body/feet motion;
7. allow inserted frames to be edited normally after insertion.

## Sequence transition rule
Reusable animations are building blocks, not frozen video clips. Entry/exit poses remain editable. Later transition tools can blend from current pose into the saved sequence without altering the master library sequence.

## AI-first requirement
The sequence library must be inspectable and editable by the AI just like the scene reel. The AI should be able to:
- list saved sequences;
- capture a sequence from an existing reel;
- adjust timing;
- replace bad poses;
- insert a saved sequence into a new scene;
- save the updated library;
while leaving the same file available for human editing.

## First production test
Create one `GR Core Motions.owmotion` library containing five sequences:
- walk
- look
- point
- wave
- flip-off

Then build one 8–12 second forest shot by inserting and editing those sequences instead of manually recreating each action.

## Hard stop
C14 passes only when a library file can be saved, reopened, and all five sequences can be inserted into an active scene with their pose art and true 24 fps exposure timing intact.
