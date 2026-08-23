# CHATGPT PROJECT — ONE-WAVE VIDEO MAKER

## CURRENT STEP
**C12 — Voice Lab hardening / preview-export parity**

## STATUS
**BROWSER STRESS PASS FOR C10-C12 — real microphone end-to-end production gate still required**

## HARD START
B13 video export runtime PASS plus C1–C5 motion production pipeline and C6–C9 Voice Lab build.

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
- Layer level, pan, pitch offset, and micro-delay.
- Spoken clips placed at exact timeline seconds.
- Voice recipes and clips save into `.owav`.

## C7 — DIALOGUE EDITOR / FINAL MIX
Built.
- Non-destructive trim in/out.
- Fade in/out.
- Per-clip gain.
- Music duck amount, attack, release.
- Export mix applies trim/fades/gain/ducking.

## C8 — SPEECH ↔ VIDEO FRAME SYNC
Built + deterministic timing tests PASS.
- Reel frame/hold timing converts to exact seconds.
- Test: frame 2 at 24 FPS with 4-frame hold = 0.1666667 s.
- Test: frame 4 after holds 4,4,12 starts at 0.8333333 s.
- Speech can snap to frame boundaries.

## C9 — VOICE RECORDER
Hardened.
- Browser mic recording into Layer 1/2/3.
- Raw voice mode can disable browser echo cancellation, noise suppression, and auto gain.
- Mic stream cleaned up on errors and completion.
- Empty takes rejected.
- Old preview object URLs revoked to prevent leaks.

## C10 — AUDIO MIX HARDENING
Browser stress PASS.
- Overlapping dialogue duck windows merge instead of pumping music up between lines.
- Short speech gaps inside attack/release envelope stay continuously ducked.
- Long gaps recover normally.
- Duck window follows the longest audible layer, including per-layer micro-delay.
- Pitch changes are included in audible-duration calculation.
- Echo/reverb tails extend ducking so music does not rise under the last tail.
- Final bus adds headroom + limiter before WebM encoding.
- Real Chromium synthetic-audio test produced exactly one mixed audio track and zero page errors.
- Test example: lowered-pitch/effect-tail clip produced 1.00s → 3.55s audible duck window; overlapping following clip extended merged window to 7.35s.

## C11 — AUDIO SESSION SAFETY
Browser stress PASS.
- Extreme/corrupt saved values are clamped on load.
- Character pitch/EQ/compression/drive/effects constrained to editor ranges.
- Clip start/trim/fade/gain constrained.
- Layer gain/pan/detune/delay constrained.
- Music duck settings constrained.
- Chromium corruption test completed with zero page errors.

## C12 — PREVIEW / EXPORT PARITY
Browser stress PASS.
- Old B7/B11/C6 play-button audio listeners are blocked during final-mix playback to prevent double starts.
- Preview now uses the same edited/hardened mix path as export.
- Audio is prepared/decoded before picture playback begins.
- Start order verified in Chromium: prepare → video start → audio start.
- Second click stops picture and audio together.
- No duplicate listener firing and zero page errors.

## AUDIO SYNC FIX
Voice Lab export previously scheduled audio before MediaRecorder started, risking clipped first words or early drift.

Fixed architecture:
**prepare/decode audio first → start MediaRecorder → start prepared audio bus → render reel.**

Normal preview uses the same prepare/start discipline.

## CURRENT AUDIO PRODUCTION ORDER
1. Record/import raw take.
2. Choose/create character voice recipe.
3. Combine up to three layers.
4. Shape voice.
5. Lay line onto video timeline.
6. Trim/fade/set clip gain.
7. Snap speech to frame/hold boundary when useful.
8. Automatic music ducking.
9. Preview through the same final-mix path used by export.
10. Save `.owav`.
11. Export WebM using prepared synchronized final audio bus.

## LOAD CHAIN
**C6 Voice Lab → C7 Dialogue Editor → C8 Frame Sync → C9 Voice Recorder → C10 Audio Hardening → C11 Session Safety → C12 Preview/Export Parity**

## TESTS COMPLETED THIS PASS
- Duck-window overlap/short-gap/long-gap deterministic tests: PASS.
- Multi-layer duration + delay tests: PASS.
- Frame/hold timing tests: PASS.
- Hardened final-mix Chromium test: PASS, one audio track, zero page errors.
- Corrupt-session Chromium clamp test: PASS, zero page errors.
- Preview sequencing Chromium test: PASS, no double listener firing, zero page errors.

## NEXT REQUIRED PRODUCTION GATE
Use a real microphone and real voice take in the animator:
record → three-layer combine → character processing → timed placement → trim/fade → frame snap → music duck → save/load → preview against picture → WebM export → listen for sync and clipping.

Do not call the full C6–C12 voice workstation production PASS until that real recorded-voice round trip succeeds.
