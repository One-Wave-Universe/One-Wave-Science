# Animator placement-grid branch step

- MAIN GOAL: ship the One-Wave Animator as a real explicit-frame desktop program.
- WHY THIS STEP EXISTS: imported transparent animation PNGs need the calibrated distance/size grid immediately; the grid must never enter playback or export.
- CURRENT STEP GOAL: enter placement mode automatically on PNG import and leave it before playback.
- HARD START: main at `3267902531a6e9b0d896c8d0d2933cf378511192`.
- LOCAL REPO ROOT: `One-Wave-Science/Tools/Chats-Animator`.
- ACTIVE BRANCH: `animator/placement-grid-acceptance`.
- REFERENCE FILES: `README.md`, `ANIMATOR_CANONICAL_ARCHITECTURE.md`, `BACKGROUND_SIZING_GRID_RULE.md`.
- ALLOWED FILES: `app.js`, `b7-playback.js`, `test-animator.sh`, this receipt.
- PROTECTED FEATURES: reel/exposure source of truth, fixed background, transparent art layers, holds/FPS, save/load, playback, WebM export, editor-only overlays.
- EXACT ACTION: activate the calibrated overlay when a character/prop image is imported; explicitly clear placement/calibration state before playback; add an explicit 1920×1080 YouTube WebM preset with production bitrates and an export receipt.
- SUCCESS CRITERIA: import enters placement mode; playback hides placement/calibration overlay; a directly uploadable YouTube preset reports resolution, FPS, timeline ticks, duration, and file size; existing smoke suite passes.
- FIELD NOTES: targeted scene/editor and renderer-boundary change only.
- TESTS / CHECKS: `bash test-animator.sh`; live `/api/assistant/health`; live `index.html`; `git diff --check`.
- TEST RESULT: PASS — static/runtime contracts, local server route, application document, and clean diff.
- VOID OVERSIGHT: ALLOW — behavior follows the canonical background/grid rule, preserves the explicit-frame reel, and uses the existing renderer/audio path for final video.
- LOOK-BACK: the import workflow now supplies its placement reference automatically and playback removes it; export now has a clearly usable YouTube target and receipt. Actual browser recording still requires GUI/browser qualification on Ubuntu or Jetson.
- ATTEMPT: 1/3.
- HARD STOP: reached after focused tests and diff review pass.
