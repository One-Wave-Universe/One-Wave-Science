# CHAT ANIMATOR HARD RULES

MANDATORY: Read this file before changing, testing, demonstrating, or describing anything in this animator.

If a proposed action conflicts with this file, STOP. Do not improvise around it.

## Identity / project / destination

YOU ARE WORKING ON THE ONE-WAVE ANIMATOR.

The job is to help make real animation scenes inside the actual animator, using the same project the human can open and manually edit afterward.

The destination is an AI-directable, human-coeditable, full-screen frame animator where the human can say what a character does, Chat can build the missing still-frame sequence inside the project, the human can play it at FPS, manually correct it, and Chat can continue from the corrected project.

Do not replace that destination with a generic animation demo, a storyboard app, an image-generation workflow, a tweening engine, or a separate prototype.

## Canon animation model

This animator works like projector film / stop motion:

`fixed still background + completed transparent PNG character/prop state per reel frame -> advance finished reel frames at project FPS`

The background remains still unless the scene explicitly changes backgrounds.
Animation comes from advancing completed still scene states on the reel.

## One file = one frame

HARD RULE: ONE PNG FILE EQUALS ONE ANIMATION FRAME.

A 50-frame motion is 50 separate PNG files, for example:

- `motions/GR/run/0001.png`
- `motions/GR/run/0002.png`
- ...
- `motions/GR/run/0050.png`

Do not silently replace this with a sprite sheet, contact sheet, atlas-as-storage, cropped strip, or one container translated across the stage.

A source sheet may be sliced during import, but the canonical editable motion library is still one PNG per frame.

## Build the motion library as scenes require it

Do not prebuild hundreds of motions just to fill a library.

For each scene:
1. inspect existing art and motion folders;
2. reuse suitable existing PNG frames;
3. create only the missing still frames needed for the requested action;
4. save useful completed sequences into the motion library;
5. grow the library naturally as real animation is produced.

## No fake animation proof

A visible animator test must use real available art.

Forbidden as acceptance proof:
- moving colored boxes;
- rectangles/circles/dummy divs;
- generic silhouettes;
- text labels moving around;
- one PNG smoothly translated as a substitute for still-frame animation;
- a fake stage outside the animator;
- a GIF or external player used to claim the animator works;
- image generator output substituted for using the animator.

If required real art is missing, report the missing asset. Do not hide that fact with a placeholder and call it success.

## Test the app by doing what the app does

HARD RULE: AN ANIMATOR FEATURE IS NOT PROVEN UNTIL IT WORKS THROUGH THE REAL ANIMATOR WORKFLOW.

Valid acceptance path:
1. open/launch the actual animator;
2. load the real still background through the animator;
3. load real transparent character/prop frame PNGs through the animator;
4. use the animator's actual placement/depth/scale controls;
5. build/edit the reel in the animator;
6. press the animator's actual Play control;
7. verify the animator itself advances completed still frames at the chosen FPS;
8. verify editor-only overlays disappear in playback/full-screen view;
9. make a manual edit in the same project and confirm playback reflects it.

Pure-function/unit tests may run separately, but they are never final acceptance for visible animator behavior.

## Background / grid / placement law

- Background is a still scene layer.
- Placement/depth grid appears only while placing or sizing an asset.
- Confirm placement -> grid disappears.
- Grid must not be visible in normal playback.
- Character distance is represented by per-frame placement/feet-depth/scale, not by moving a placeholder container.
- Real PNG art is placed directly into each completed scene-frame state.

## FPS / reel law

- Playback is driven by the project clock.
- The reel advances completed scene-frame states at FPS.
- Holds/exposures repeat a completed still for the required clock ticks.
- FPS playback does not mean continuous geometric tweening between frames.
- A motion may contain any number of frame PNGs required by the action; 50 is a useful batch/sequence size, not permission to combine them into one file.

## Director Mode

Director Mode means the human can describe the action in plain language, such as:

`GR dances punk style, walks, runs, jumps, rolls, picks a flower, faces camera and removes his mask.`

Chat must translate that direction into edits to the SAME animator project:
- inspect current scene and assets;
- find existing motion frames;
- make only missing frame sequences;
- place them in reel order;
- set holds/timing/FPS relationships;
- set per-frame position/depth/scale/visibility;
- play/check the result inside the animator;
- refine in chunks until the action reads correctly.

Director Mode is not a chat box that produces an unrelated movie elsewhere.

## Real Animator Mode

The human must be able to manually edit the exact same project Director Mode changed:
- select reel frame;
- replace pose/frame PNG;
- adjust position;
- adjust feet depth;
- adjust scale;
- adjust visibility;
- adjust exposure/hold;
- insert/duplicate/delete/reorder completed scene frames;
- play the result at project FPS.

AI edits and human edits must never fork into incompatible project representations.

## Scene-production loop

For a requested short animation, do not attempt the entire movie blindly in one pass.

Required loop:
1. choose a short contiguous action section;
2. build it inside the animator;
3. play/check it in the animator;
4. inspect timing, readability, continuity, scale/depth and character identity;
5. correct that section until it passes;
6. only then add the next section;
7. replay the joined sections and check the transition;
8. continue until the full short passes.

For the current GR short, the intended action order is:
`punk dance -> walk -> run -> jump -> roll -> pick flower -> stop/facing screen -> remove mask -> sunset/darken -> eyes remain -> more eyes appear in darkness`.

Do not generate unrelated poster art for this task. Use repository art first and add only missing animation frames when actually needed.

## Full-screen playback law

The finished animation view is full-screen scene playback, not a tiny preview box pretending to be the movie.
Editor UI may surround the stage while editing, but playback/full-screen mode must present the scene itself and hide placement grids/editor overlays.

## Do-not-drift checklist before EVERY animator action

Before any edit, answer internally:
1. Am I inside the actual animator project?
2. Am I using its real files/state/runtime?
3. Is one PNG still one frame?
4. Am I preserving the fixed-background + completed-still reel model?
5. Am I using real available art instead of a placeholder?
6. Will the final test occur through the animator itself?
7. Am I changing only what is necessary for the current requested scene/feature?
8. Can the human manually edit the result in the same project afterward?

If any answer is NO, do not execute the change.

## Local-reference law

Every animator directory and every principal animator source/page must carry a nearby orientation reference stating:
- THIS IS THE ONE-WAVE ANIMATOR;
- what this local file/directory does;
- the current animation model;
- the current plan/destination;
- the hard prohibition on placeholder/tween/demo drift;
- where to reread these rules.

When entering a different animator area, reread its local reference before acting.

Primary canon reference: `Tools/Chats-Animator/CHAT_ANIMATOR_HARD_RULES.md`.
