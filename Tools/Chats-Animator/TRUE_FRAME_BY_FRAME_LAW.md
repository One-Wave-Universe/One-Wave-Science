# ONE-WAVE ANIMATOR — TRUE FRAME-BY-FRAME LAW

**Status: HARD REQUIREMENT**

The One-Wave Animator is a real frame-by-frame / exposure-sheet animator.

## What counts as animation

The reel is the animation source of truth. A frame contains the actual character/prop artwork or pose state that is shown for that frame. A hold/exposure may keep one drawing on screen for multiple playback ticks, but when the action changes, the reel must advance to a genuinely different drawing/pose.

A valid walk therefore looks like:

```text
frame 1: GR walk pose A
frame 2: GR walk pose B
frame 3: GR walk pose C
frame 4: GR walk pose D
...
```

The background may remain fixed while GR's drawing changes frame by frame. Position, depth, scale, camera, and layer transforms may also change, but those transforms do not replace the required pose/drawing changes.

## What does NOT count

None of these can be presented as proof of a working Animator:

- one still image translated across the screen;
- one still image scaled larger/smaller to imitate walking toward/away;
- a camera pan over a still scene;
- a set of already-composited screenshots stitched into a GIF;
- a sprite/reference sheet played as whole-image frames;
- tween-only motion with no changing character drawings;
- external GIF/video assembly that bypasses the Animator reel;
- a demo that never proves distinct reel-frame artwork.

Those may be useful reference or export formats, but they are not acceptance evidence for the Animator itself.

## Required editor behavior

The Animator must support normal frame-animation work directly:

- create, duplicate, insert, delete, and reorder reel frames;
- select an individual frame;
- replace/edit the pose artwork on that frame;
- copy a pose to adjacent frames and then modify it;
- onion-skin previous/next drawings;
- set explicit holds/exposures per drawing;
- scrub and see the exact drawing for each reel frame;
- play the reel at the declared FPS;
- keep background and character/prop layers independent;
- save and reopen without losing per-frame drawings or holds;
- export the same changing drawings and timing seen in preview.

## Required acceptance proof

A frame-by-frame qualification clip must use:

1. one fixed background;
2. one character identity, such as GR;
3. at least six reel frames;
4. at least four genuinely distinct character pose/drawing states;
5. at least one repeated drawing using a hold/exposure;
6. visible pose change during playback;
7. save -> close/reopen -> playback with the same frame order and holds;
8. video/reel export from the Animator itself.

The receipt must identify the pose/art source used on each reel frame. Where practical, the test should record an asset ID or content hash so a moving/scaling copy of one still cannot falsely pass as frame-by-frame animation.

## GR demonstration standard

The canonical GR demo is not "move GR across a forest image."

It is:

```text
fixed forest background
+
GR pose A -> GR pose B -> GR pose C -> GR pose D -> ...
+
per-frame placement/depth/scale only as needed
+
exposure-sheet timing
+
Animator playback
+
Animator export
```

GR's feet, body, arms, head, clothing/tail silhouette, or other pose features must visibly change through the walk cycle. Depth scaling may accompany the walk, but it is not the walk animation itself.

## AI access rule

Any AI operating Animator through the universal control lane must manipulate these same reel frames and pose sources. An AI may not substitute a GIF generator, screenshot stitcher, transform tween, or external compositor and call the result an Animator pass.

## Final law

**Different action frames require different drawings/poses.**

A changing transform is not a changing drawing. A GIF is not the Animator. A stitched storyboard is not the Animator. The real reel must contain and play the frame-by-frame work.