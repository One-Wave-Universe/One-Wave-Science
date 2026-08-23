# CHATGPT PROJECT — ONE-WAVE VIDEO MAKER

## CURRENT STEP
**C9 — Voice Lab / Dialogue Production Pipeline**

## STATUS
**BUILT — runtime production gate next**

## HARD START
B13 video export runtime PASS plus C1–C5 motion production pipeline.

## MOTION PIPELINE — PROTECTED
C1 through C5 remain intact:
- normalize authored stills before layout;
- fit feet/base depth to straight or curved paths;
- calibrated perspective controls size;
- 24 FPS / 6 pose-beat walk cadence supported;
- one-click Walk Away / Walk Toward;
- real forest-path still-frame production output passed.

## C6 — VOICE LAB + SPEECH TIMELINE
Built.
- Reusable named character voice recipes.
- Character pitch, low cut, body EQ, presence EQ, compression, drive, echo, and reverb.
- Three-layer voice combiner per spoken line.
- Each layer has level, pan, pitch offset, and micro-delay.
- Spoken clips are placed at exact timeline seconds.
- Clip gain, mute, preview, delete.
- Voice recipes and speech clips serialize into `.owav` project data.
- Existing B11 soundtrack remains supported.
- Final video export uses a combined soundtrack + dialogue bus when Voice Lab is active.

## C7 — DIALOGUE EDITOR / FINAL MIX
Built.
- Non-destructive trim-in and trim-out per speech clip.
- Fade-in and fade-out per speech clip.
- Per-clip gain.
- Global music duck amount, attack, and release.
- Trim, fades, gain, and music ducking are applied to the actual final export mix.
- Dialogue-editor mix settings serialize into `.owav`.

## C8 — SPEECH ↔ VIDEO FRAME SYNC
Built.
- Converts reel frame/hold timing to exact seconds.
- Next spoken line can snap directly to a target reel frame.
- Existing speech clip can be snapped to the nearest selected frame boundary.
- Frame timing follows current project FPS and reel holds.

## C9 — VOICE RECORDER
Built.
- Browser microphone recording through MediaRecorder.
- Records directly into Voice Lab Layer 1, 2, or 3.
- Recorded take can immediately be combined/shaped without leaving the animator.

## CURRENT AUDIO PRODUCTION ORDER
1. Record or import the raw voice take.
2. Choose/create the character voice recipe.
3. Combine up to three layers if desired.
4. Shape pitch/EQ/compression/drive/echo/reverb.
5. Lay the spoken line onto the video timeline.
6. Trim, fade, and set clip gain.
7. Snap speech to reel frame/hold boundaries where useful.
8. Duck music automatically around speech.
9. Preview against the animated reel.
10. Save the complete `.owav` project.
11. Export WebM with one final mixed audio track.

## LOAD CHAIN
B13 now guards and loads the audio workstation as:
**C6 Voice Lab → C7 Dialogue Editor → C8 Frame Sync → C9 Voice Recorder**.

This remains additive to the protected B1–B13 engine and C1–C5 motion tools.

## NEXT REQUIRED GATE
**Run the full audio workstation in Chromium:**
record/import → three-layer combine → character processing → timed speech placement → trim/fade → frame snap → music duck → project save/load → WebM export.

Do not call C6–C9 production PASS until that end-to-end browser test succeeds.
