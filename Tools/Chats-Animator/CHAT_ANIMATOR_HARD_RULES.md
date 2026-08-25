# CHAT ANIMATOR HARD RULES

> THIS NOTE PERTAINS TO THIS PAGE ONLY. IT HAS NOTHING TO DO WITH RULES OR UPDATES FOR ANY OTHER PAGE. DO NOT SUMMARIZE ANOTHER PAGE INTO THIS ONE, AND DO NOT APPLY THIS PAGE'S NOTE TO ANY OTHER PAGE.

## What this page is
This page is a project-orientation reference for this page only. It records the intended One-Wave Animator identity and examples of the constraints that should be written independently into each actual work page/file. It is not an inheritance mechanism and does not silently modify any other file.

## Identity / project / destination recorded on this page

YOU ARE WORKING ON THE ONE-WAVE ANIMATOR.

The job described on this page is to help make real animation scenes inside the actual animator, using the same project the human can open and manually edit afterward.

The destination recorded here is an AI-directable, human-coeditable, full-screen frame animator where the human can say what a character does, Chat can build the missing still-frame sequence inside the project, the human can play it at FPS, manually correct it, and Chat can continue from the corrected project.

Do not replace that destination on this page with a generic animation demo, a storyboard app, an image-generation workflow, a tweening engine, or a separate prototype.

## Animation model recorded on this page

This page describes projector-film / stop-motion logic:

`fixed still background + completed transparent PNG character/prop state per reel frame -> advance finished reel frames at project FPS`

The background remains still unless the scene explicitly changes backgrounds.
Animation comes from advancing completed still scene states on the reel.

## One file = one frame on this page

ONE PNG FILE EQUALS ONE ANIMATION FRAME.

A 50-frame motion means 50 separate PNG files, for example:
- `motions/GR/run/0001.png`
- `motions/GR/run/0002.png`
- ...
- `motions/GR/run/0050.png`

This page does not define sprite-sheet, contact-sheet, atlas, cropped-strip, or moving-container storage as animation frames.

## Motion-library growth described on this page

Do not prebuild hundreds of motions merely to fill a library.
For a real scene, inspect existing art first, reuse suitable frames, create only missing frames, then retain useful completed sequences for later reuse.

## No fake proof on this page

This page rejects the following as proof of animator correctness:
- moving colored boxes;
- rectangles/circles/dummy divs;
- generic silhouettes;
- text labels moving around;
- one PNG smoothly translated as a substitute for still-frame animation;
- fake stages outside the animator;
- GIF/external-player proofs;
- image-generator output substituted for using the animator.

## In-app test model recorded on this page

A visible feature is considered proven on this page only when the real animator workflow is used:
1. open/launch the actual animator;
2. load a real still background through the animator;
3. load real transparent character/prop frame PNGs through the animator;
4. use actual placement/depth/scale controls;
5. build/edit the reel in the animator;
6. press the animator's actual Play control;
7. verify completed still frames advance at the chosen FPS;
8. verify editor-only overlays disappear during playback/full-screen view;
9. make a manual edit in the same project and verify playback reflects it.

## Background / grid / placement model recorded on this page

- Background is a still scene layer.
- Placement/depth grid appears only while placing or sizing an asset.
- Confirm placement -> grid disappears.
- Grid is not visible during normal playback.
- Character distance is represented by per-frame placement/feet-depth/scale.
- Real PNG art is placed directly into completed scene-frame state.

## Director Mode recorded on this page

Director Mode means the human can describe action in plain language and Chat translates it into edits to the same animator project: inspect scene/assets, find existing motion frames, make only missing frames, place them in reel order, set timing/position/depth/scale/visibility, play/check the result inside the animator, and refine in chunks.

## Real Animator Mode recorded on this page

The human can manually edit the exact same project: select reel frame, replace frame PNG, adjust position/depth/scale/visibility/hold, insert/duplicate/delete/reorder frames, and play the result at project FPS.

## Scene-production loop recorded on this page

Build a short contiguous action section, play/check it inside the animator, correct it until it reads correctly, then add the next section and check the transition.

Current GR short order recorded on this page:
`punk dance -> walk -> run -> jump -> roll -> pick flower -> stop/facing screen -> remove mask -> sunset/darken -> eyes remain -> more eyes appear in darkness`.

## Page-local-reference design

Every different animator work page/file should contain its own independent orientation note at its own top. Each such note must begin by stating that it pertains only to that page/file and has nothing to do with rules or updates on any other page.

No page inherits another page's note. No page is allowed to summarize another page's note into itself as a substitute for writing the correct local reference. Similar wording across pages is deliberate local orientation, not shared-rule inheritance.
