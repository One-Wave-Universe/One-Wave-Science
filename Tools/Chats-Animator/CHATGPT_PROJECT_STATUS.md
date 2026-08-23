# CHATGPT PROJECT — ONE-WAVE VIDEO MAKER

## CURRENT STEP
**B13 — WebM video export**

## STATUS
**RUNTIME PASS — first complete production-output checkpoint**

## B9 — SPRITE-SHEET SLICER
Runtime PASS in Chromium/Playwright.
- Nonblank cells extracted to consecutive frames.
- Transparent blank cells skipped.
- Holds, placement, depth, scale, background, and calibration preserved.
- Zero browser page errors.

## B10 — PROJECT SAVE / LOAD
Runtime PASS in Chromium/Playwright.
- Reel, holds, FPS, active index, snapshots, and embedded art saved to `.owav` JSON.
- Valid projects restore correctly.
- Malformed projects fail safely without mutating the current reel.
- B11 audio track is now included in project persistence.

## B11 — AUDIO TRACK + REEL SYNC
Runtime PASS in Chromium/Playwright.
- Audio file imports as embedded data.
- Reel duration is calculated from holds/FPS.
- Audio starts with reel playback and pauses on stop/end.
- Audio survives project save/load.
- Zero browser page errors.

## B12 — PER-FRAME CAMERA
Runtime PASS in Chromium/Playwright.
- Camera X/Y/zoom stored in each frame snapshot.
- Background and assets move together.
- Playback restores camera state frame by frame.
- Reset works.
- Zero browser page errors.

## B13 — VIDEO EXPORT
Runtime PASS in Chromium/Playwright.
- Reel renders to 16:9 canvas.
- Frame holds are honored.
- Per-frame camera is honored.
- WebM download is produced.
- With B11 audio loaded, export contains both video and audio.
- ffprobe verified VP9 video + Opus audio inside a valid WebM container.
- Zero browser page errors.

## PROTECTED WORKING FEATURES
B1 through B13 remain the working chain: background/calibration, placement/depth sizing, frame reel/holds, pose editing, onion skin, playback, batch pose import, sprite-sheet slicing, project persistence, audio, camera, and video export.

## NEXT PERMITTED STEP
**C1 — First real end-to-end production clip.**

Use the animator before adding more engine features:
1. load a real background;
2. load Goblin Raccoon/character pose PNGs or a sprite sheet;
3. set frame holds and playback timing;
4. load dialogue/music;
5. set any camera moves;
6. save the `.owav` project;
7. export the first real WebM clip;
8. inspect the result and repair only what the production test exposes.

Tweening and other polish stay later unless C1 proves they are actually needed.
