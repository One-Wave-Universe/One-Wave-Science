# CLAUDE ANIMATION FEDERATION

## READ THIS BEFORE CODING

You are modifying Claude's Animation Federation.

Do not redesign the application.

Do not substitute a different animation architecture because you believe it is cleaner, easier, more modern, or more conventional.

Do not build the whole application at once.

Work ONE BRANCH AT A TIME.

A branch is merged only after its feature is visibly demonstrated to work.

This is a separate implementation from One_Wave_Animator (`../One_Wave_Animator/`). It may share the same production principles. It does not have permission to redesign them.

---

## WHAT WE ARE BUILDING

This is a PNG still-frame animation and video production system shared by:

- a human editor
- an AI editor

Both edit the same project.

The goal is for the human to be able to say:

> Put the character by the dumpster, have him walk toward the chair, turn his head toward Karen, say this line, blink twice, then sit down.

The AI should eventually be able to do as much of that production work as possible.

The human can then manually alter any individual frame.

The AI can continue from the human's corrections.

There is ONE authoritative project state.

---

## THE MOST IMPORTANT RULE

DO NOT MOVE A CHARACTER AROUND INSIDE A MOVABLE ANIMATION BOX.

Do not make a big transparent character canvas and animate that canvas around the scene.

Do not treat a character as a rectangular video clip that slides over a background.

The PNG artwork itself is placed into scene/world coordinates.

The background is the world.

Every animation frame is a composed still.

Conceptually:

```
BACKGROUND
   +
CHARACTER PNG
   +
HEAD / FACE PNGs
   +
PROP PNGs
   +
EFFECTS
   =
ONE FRAME
```

Then:

```
FRAME 1
FRAME 2
FRAME 3
FRAME 4
...
```

are played according to the selected FPS.

That is the animation.

---

## BACKGROUND

A PNG background defines the scene.

Example: `alley.png`

Characters and props are placed over that image using scene coordinates.

Do not move the entire character's coordinate system around inside another artificial box.

---

## PERSPECTIVE GRID

Each background can have a production grid.

The grid establishes:

- ground
- depth
- perspective
- approximate character scale
- foot placement

The grid appears in the EDITOR.

The grid does NOT appear in the final video.

---

## CHARACTER SCALE IS BASED ON FEET / GROUND POSITION

This requirement is critical.

A character's scale is calculated from where their feet correspond to the ground.

Closer ground position: larger character.

Farther ground position: smaller character.

Do not calculate perspective using the center of the character PNG.

Do not calculate depth because the character's head moved upward.

Use the feet/ground location.

---

## JUMPING

A jump has TWO positions:

- GROUND POSITION
- AIR OFFSET

These are not the same thing.

Example:

A character standing at `ground_x = 400, ground_y = 600` jumps upward 100 pixels.

Their ground reference remains `400, 600`.

Their airborne offset becomes `0, -100`.

Therefore their perspective scale stays approximately the same.

THE CHARACTER MUST NOT SHRINK JUST BECAUSE THEY JUMP UPWARD.

### Sideways jumps

If a character jumps sideways, their perspective scale should follow the intended ground path.

If the jump is sideways across approximately the same depth plane, they remain approximately the same size.

Do not use the character PNG's airborne screen Y position as its depth.

---

## STILL-FRAME ANIMATION

Animation should resolve to explicit frames.

Example:

```
Frame 001
Character body = walk_01.png
x = 300
ground_y = 550

Frame 002
Character body = walk_02.png
x = 304
ground_y = 550

Frame 003
Character body = walk_03.png
x = 309
ground_y = 550
```

This is intentionally similar to traditional animation / stop-motion / movie-reel thinking.

Do not replace this architecture with CSS-style sliding animation.

---

## FRAME RATE

Support selectable FPS.

Start with: 12, 24, 30, 60.

Additional FPS options can be added later.

The editor must allow inspection of individual frames.

---

## CHARACTER LIBRARY

Characters need permanent reusable asset libraries.

Example:

```
characters/
    goblin_raccoon/
        body/
        heads/
        eyes/
        mouths/
        hands/
        expressions/
        poses/
        animations/
```

Never assume one flattened PNG is the only possible character representation.

---

## HEAD LIBRARY

Support many angles around the character.

Eventually this may include `000` through `359` degrees.

Do NOT require all 360 images to exist.

Store whichever ones are available.

The program should know the angle associated with each image.

---

## FACE PARTS

Support separate assets where available: head, eyes, mouth, brows, mask.

This allows blinking, looking, talking, and expression changes without regenerating the entire character every time.

---

## LARGE PNG SEQUENCES

The system must comfortably manage 50+, 100+ PNG frames for a movement.

Example: `turn_001.png` ... `turn_060.png`

These should be viewable as an ordered animation strip.

---

## REUSABLE ANIMATION LIBRARY

Approved movements should be saved.

Examples: walk_normal, walk_angry, run, jump, sit, stand, head_turn_left, blink, laugh, pick_up_can.

These animations should be reusable at different locations.

Do not hard-code their original screen coordinates into them.

Store relative movement where appropriate.

---

## PROPS

Props are PNG assets.

Examples: guitar, beer can, chair, trash can, microphone.

They can be placed, dragged, rotated, resized, layered, attached to a character, modified on individual frames.

Human must be able to alter a prop on a single frame.

---

## FRAME-BY-FRAME MANUAL CONTROL

This is mandatory.

A human must always be able to open a specific frame and correct: character position, character pose, scale, head, mouth, eyes, prop, lighting, layer ordering.

AI automation must never remove the ability to manually repair one still.

---

## AI AND HUMAN EDIT THE SAME PROJECT

Do NOT build one AI project representation and another GUI representation.

Architecture:

```
                 PROJECT STATE
                 /           \
                /             \
          HUMAN GUI          AI API
                \             /
                 \           /
                    RENDERER
```

If the human changes frame 47, the AI sees the changed frame 47.

If the AI changes frames 48-75, the human sees those changes immediately.

---

## AI MUST ACTUALLY EDIT

The AI interface must not merely return advice such as "Drag the character onto frame 20."

The AI must eventually be capable of calling commands that actually perform the work.

Examples: `add_character`, `move_character`, `set_ground_position`, `set_air_offset`, `set_pose`, `set_head_angle`, `set_eyes`, `set_mouth`, `add_prop`, `attach_prop`, `apply_animation`, `change_lighting`, `add_audio`, `render_preview`.

---

## HUMAN CORRECTION BECOMES THE NEW REFERENCE

Example: AI builds a head turn. Human manually fixes frame 23. Human says "That's the right position. Make the next frames follow that."

The AI should use the modified project state.

It must NOT overwrite the human correction with an older cached version.

---

## AUDIO

Eventually include a multitrack audio editor.

Tracks include: Dialogue, Music, Sound effects, Ambience.

Needed controls eventually include: trim, split, volume, fade, pan, EQ, compression, limiter.

Do not build audio before the core visual frame system works.

---

## LIGHTING

Characters and scenes need editable: brightness, contrast, saturation, hue, opacity.

Lighting can change over frames.

---

## CHAT

Eventually provide a dialogue panel where the user can type production instructions.

Example: "Goblin should look toward the door around frame 180. Make the movement about half a second long and preview it."

That instruction goes through the same project API used by the editor.

---

## UNDO

Every AI modification must be undoable.

Prefer transactions.

Example:

```
Transaction 583:
AI
Frames 180-192
Changed head angle sequence.
```

Then the human can undo only that operation.

---

## BUILD DISCIPLINE

This is mandatory.

For EACH branch:

1. State the exact branch goal.
2. Read these architecture rules.
3. Change only what is necessary for that goal.
4. Run the program.
5. Perform the branch acceptance test.
6. Inspect the actual output.
7. Report what passed and what failed.
8. Fix failures.
9. Test again.
10. Merge only after the test passes.

---

## THREE-FAIL RULE

If the same implementation approach fails three times: STOP.

Do not keep stacking patches onto it.

Record: what was attempted, what failed, why it probably failed.

Then choose a different implementation approach.

---

## DO NOT DO THESE THINGS

Do NOT:

- redesign the animation philosophy
- replace still-frame PNG animation with sliding containers
- remove frame-level editing
- hide perspective calculations in an uneditable black box
- build the entire application in one pass
- merge untested code
- silently change existing architecture
- add unrelated features during a branch
- overwrite human corrections
- invent character artwork when existing artwork should be used
- create placeholder squares and call the animation system complete
- treat passing unit tests as proof that the visual result is correct

THE ACTUAL RENDERED IMAGE OR VIDEO MUST BE INSPECTED.

---

## FIRST DEVELOPMENT TARGET

Do not begin with AI chat.

Do not begin with audio.

Do not begin with fancy UI.

Prove the primitive first:

```
PNG BACKGROUND
      +
CHARACTER PNG
      +
GROUND/FOOT POSITION
      +
PERSPECTIVE SCALE
      +
EXPLICIT FRAMES
      =
CORRECT ANIMATION
```

Once that primitive works, the rest of Animation Federation can be built around it.

---

## REQUIRED RESPONSE BEFORE CODING

Before changing code, respond with ONLY:

1. The branch you are working on.
2. Its single goal.
3. Files you expect to modify.
4. The acceptance test.
5. Confirmation that you will not work beyond that branch.

Then perform that branch.

Do not reinterpret these instructions into a different project.

Do not begin coding against this constitution until a branch order for a specific branch has been given. This document is the standing law; it is not itself a branch order.
