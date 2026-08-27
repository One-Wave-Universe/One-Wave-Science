# CHATGPT PROJECT — ONE-WAVE VIDEO MAKER

## CURRENT STEP
**C14 — Five-slot reusable motion-sequence library + true 24 fps acting pipeline**

## STATUS
**BUILT — C14 runtime save/open/insert gate pending**

## HARD START
B13 export runtime PASS, C1–C5 motion production pipeline, and C6–C12 audio hardening remain protected.

## MOTION TIMING CORRECTION — AUTHORITATIVE
The animator uses a true **24 fps production timeline**.

Do not treat the earlier 24 fps / 6 pose-beat shortcut as the global animation rule.

Use normal animation exposures by action:
- on 1s = new drawing every frame = 24 drawings/sec;
- on 2s = new drawing every 2 frames = 12 drawings/sec;
- on 3s = new drawing every 3 frames = 8 drawings/sec;
- longer holds whenever acting requires them.

Pose artwork may hold while position/depth changes every timeline frame. Perspective movement must not stair-step just because a drawing is held.

Baseline walk cycle target:
1. Contact L
2. Down L
3. Passing L
4. Up L
5. Contact R
6. Down R
7. Passing R
8. Up R

Normally begin by testing that cycle on 2s at 24 fps, then alter exposures/spacing for character weight and acting.

## C14 — REUSABLE MOTION LIBRARY
Built and wired into the live animator.

File format:
**`.owmotion`**

Initial visible capacity:
**5 reusable sequence slots per library file**.

First GR target library:
1. Walk
2. Look / notice
3. Point
4. Wave
5. Flip-off

Slots are renameable/replacable and are not hardcoded to those actions.

### Implemented C14 behavior
- New Motion Library
- Open `.owmotion`
- Save `.owmotion`
- Five visible sequence slots
- Capture reel start/end range into a sequence
- Sequence name
- Character tag
- Loop flag
- Notes
- Rename sequence
- Delete sequence
- Insert sequence at current reel position
- Embedded reel frames/pose art retained in the sequence file
- Stored sequence FPS retained
- Active reel is copied from, not destructively moved
- Inserted frames become ordinary editable reel frames

### C14 source files
- `C14_MOTION_SEQUENCE_LIBRARY.md`
- `c14-motion-library.js`
- `index.html` now loads `c14-motion-library.js`

## C14 REQUIRED RUNTIME GATE
Do not call C14 PASS until one real browser test succeeds:
1. create five sequences;
2. save one `.owmotion` file;
3. reopen that file;
4. confirm all five slots restore;
5. insert each sequence into an active reel;
6. confirm original active-scene frames/background remain intact;
7. confirm pose art and frame exposures survive round trip.

## FIRST FULL ACTING TEST AFTER C14
Build one continuous GR forest performance approximately 8–12 seconds:
- walk around the path;
- slow and look at something;
- head/eyes lead the look;
- point with anticipation then extension;
- relax the arm;
- notice the camera/viewer;
- wave with multiple hand arcs and follow-through;
- pause;
- flip something off with anticipation, extension, hold, and recovery;
- preserve feet/path registration and perspective depth throughout.

This shot should be assembled primarily from the reusable motion library, then hand-edited where transitions need character acting.

## VOICE/AUDIO SPLIT
Voice generation is being separated from the animator.

Standalone program started at:
`Tools/Voice-Forge/README.md`

The animator should ultimately receive finished dialogue clips + timing metadata rather than own the core voice-generation system.

Voice Forge rule:
- use authorized/reference human voices or original project voices;
- blend controllable voice traits non-destructively;
- do not rely on canned TTS/machine voices as the hidden source;
- save reusable character voice recipes;
- render clean WAV + recipe metadata for animator handoff.

## PROTECTED AUDIO WORK
C6–C12 remain intact:
- three-layer dialogue combiner;
- trim/fades/gain;
- frame sync;
- mic recording;
- music ducking;
- limiter/headroom;
- session sanitization;
- preview/export parity;
- prepare → recorder start → audio start synchronization.

## NEXT PERMITTED STEP
**Runtime-test C14, then build the five GR core motion sequences correctly on a true 24 fps timeline.**

Do not add another speculative editor subsystem before those five motions can be saved/reopened/inserted and used to assemble the forest acting test.
