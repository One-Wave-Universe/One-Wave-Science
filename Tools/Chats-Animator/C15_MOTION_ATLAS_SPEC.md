# C15 — FULL PNG MOTION ATLAS

## Purpose
The animator needs a production-scale reusable motion corpus, not a small shortcut library. A character should have pages/folders of transparent PNG poses plus timing metadata so complete acting scenes can be assembled from authored motion.

## Canonical clock
- Scene timeline: 24 fps.
- A sequence may animate on 1s, 2s, 3s, or mixed holds.
- Timing is stored per pose/frame. Do not force every action to one cadence.

## Package format
A character motion corpus is stored as a `.owatlas` JSON package with embedded or referenced transparent PNG data.

Top level:
- format: `one-wave-motion-atlas`
- version: 1
- character
- canvas metadata
- categories
- sequences
- facial sequences
- tags

Each sequence stores:
- id
- character
- category
- action
- direction
- variant
- loop
- fps
- frames[]
- notes/tags

Each frame stores:
- PNG/data URL
- hold in 24-fps ticks
- anchor / feet-base position
- optional hand/head/face markers

## Direction convention
Eight-way locomotion/action support:
- N — away/back
- NE — away-right
- E — right profile
- SE — toward-right
- S — toward/front
- SW — toward-left
- W — left profile
- NW — away-left

## Minimum locomotion corpus
### WALK — all 8 directions
Each direction must contain a complete authored cycle with at least:
1. contact A
2. down A
3. passing A
4. up A
5. contact B
6. down B
7. passing B
8. up B

Plus transition sequences:
- idle → walk
- walk → idle
- walk turn 45° left/right
- walk turn 90° left/right
- walk turn 180°
- pivot left/right

### RUN — all 8 directions
Each direction should contain at least:
1. contact A
2. down A
3. passing A
4. up/flight A
5. contact B
6. down B
7. passing B
8. up/flight B

Plus:
- idle → run
- run → stop
- run turn left/right
- run skid/abort

### OTHER LOCOMOTION
- sneak 8 directions
- tiptoe 8 directions
- crouch-walk 8 directions
- limp variants
- backpedal
- side-step left/right
- shuffle

## Body action corpus
### Jump
- anticipate/crouch
- launch
- rising
- apex
- falling
- landing contact
- landing compression
- recover
- standing jump
- running jump
- jump forward/back/left/right

### Fall / roll
- trip
- forward fall
- backward fall
- side fall left/right
- tuck
- forward roll
- backward roll
- shoulder roll left/right
- recover to crouch
- recover to stand

### Height changes
- stand → crouch
- crouch idle
- crouch → stand
- kneel down/up
- sit down/up
- lie down/get up

### Interaction
- reach near/far/high/low
- grab
- release
- pick up
- put down
- carry light/heavy
- push
- pull
- open/close
- throw overhand/underhand
- catch
- kick
- stomp
- tap/poke

## Gesture / acting corpus
- wave small/large
- point left/right/up/down/front/back
- finger wag
- thumbs up/down
- shrug
- hands on hips
- arms crossed
- facepalm
- scratch head
- rub chin/thinking
- beckon
- shoo
- salute
- clap
- cheer
- flip-off left/right/front
- double flip-off

## Look / attention corpus
- neutral look
- look left/right
- look up/down
- look over shoulder left/right
- glance left/right
- double take
- inspect ground
- inspect object at hand height
- inspect overhead
- listen left/right
- startled turn

## Facial expression corpus
Face art must be independently reusable when character construction allows it.

### Eyes
- open neutral
- blink sequence: open → half → closed → half → open
- squint
- wide
- eye left/right/up/down
- cross-eyed
- one-eye squint

### Brows
- neutral
- raised
- worried
- angry
- skeptical single brow

### Mouth / expression
- neutral
- small smile
- grin
- smirk
- frown
- grimace
- annoyed
- angry
- rage/yell
- surprised O
- scared
- disgust
- laugh
- sad
- cry
- confused
- deadpan
- smug
- exhausted
- suspicious

### Speech mouth set
At minimum reusable mouth shapes for:
- closed/rest
- M/B/P
- A/AA
- E/EE
- I
- O
- U/OO
- F/V
- L
- W/Q
- wide consonant

## Browser/editor requirements
The motion atlas browser must support:
- character selector
- category selector
- action search
- direction filter
- loop/non-loop filter
- thumbnails/contact sheet view
- sequence metadata view
- insert sequence into reel
- insert reversed sequence where valid
- duplicate/variant action
- save/open `.owatlas`
- bulk import PNG pages or folders when browser capability permits

## Production target for Goblin Raccoon
First serious GR atlas should target hundreds of PNGs, not five motions.
A reasonable first production milestone is 40–60 complete sequences, which can easily be 300–500 authored PNG frames before facial overlays.

## Rule
The active scene remains separate from the reusable atlas. The atlas is a deliberate reusable asset library. Scene-specific poses may be promoted into the atlas only intentionally.
