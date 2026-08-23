# CHATGPT PROJECT — ONE-WAVE VIDEO MAKER

## CURRENT STEP
**C4 — Pre-layout pose normalization + production walk pipeline**

## STATUS
**RUNTIME PASS**

## HARD START
B13 video export runtime PASS and first forest walk production test.

## PRODUCTION TEST LESSONS
The forest walk proved the engine could make a real video, but exposed three production problems:
- manual size stations look jumpy;
- inconsistent pose timing makes the walk rhythm uneven;
- mismatched source image canvases/padding can make feet appear to jump even when editor depth is correct.

## C1 — DETERMINISTIC PATH MOTION
Runtime PASS.
- Existing consecutive pose stills can be fitted to start/end X and feet depth.
- Feet/base depth drives the existing calibrated automatic perspective size.
- Smoothstep easing removes abrupt near/far depth jumps.
- Reverse path builds the toward-camera return motion.
- Midpoint X control now supports a curved trail using a quadratic path.
- Pose artwork and manual scale remain untouched.

## C2 — WALK CADENCE
Runtime PASS.
- Project FPS is converted into even pose holds.
- Default production clock: 24 FPS / 6 pose beats per second = 4-frame holds.
- Optional turnaround multiplier gives the final pose a longer hold.
- Verified 7-pose test produced 4,4,4,4,4,4,12 holds without altering pose art.

## C3 — ONE-CLICK WALK BUILDER
Runtime PASS.
- Synchronizes path pose count with cadence pose count.
- Build Walk Away calls C1 forward path then C2 cadence.
- Build Walk Toward calls C1 reverse path then C2 cadence.
- Designed to start on the first pose frame of an imported run.

## C4 — PRE-LAYOUT POSE NORMALIZER
Runtime PASS.
- Trims transparent padding from selected pose artwork across a consecutive run.
- Resizes each pose to one configurable square transparent canvas.
- Centers visible artwork horizontally.
- Bottom-anchors visible artwork to one consistent pixel line.
- Configurable subject height and bottom margin.
- Deliberately mismatched test images all normalized to 512×512 with the same 15 px visible bottom margin and zero browser errors.

## WORKING PRODUCTION ORDER
1. Import pose stills / sprite sheet.
2. **Normalize the pose canvases first.**
3. Fit the pose run to the straight/curved path and feet-depth range.
4. Apply cadence, or use the one-click walk builder.
5. Add audio.
6. Add per-frame camera movement.
7. Save `.owav` project.
8. Export WebM video.
9. Inspect the real clip and repair only what production exposes.

## PROTECTED WORKING FEATURES
B1 through B13 remain intact: background/calibration, placement/depth sizing, frame reel/holds, pose editing, onion skin, playback, batch pose import, sprite-sheet slicing, project save/load, audio, per-frame camera, and valid WebM video export with optional Opus audio.

C1 through C4 are additive production tools and do not replace the protected B-stage engine.

## NEXT PERMITTED STEP
**C5 — Run the improved forest-path production test through the new Normalization → Path → Cadence pipeline and compare it against the first clip.**

If C5 passes, continue into the first dialogue/episode scene instead of adding speculative engine features.
