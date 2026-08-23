# CHATGPT PROJECT — ONE-WAVE VIDEO MAKER

## CURRENT STEP
**B10 — Browser/runtime smoke-test harness**

## STATUS
**IMPLEMENTED — one-click reversible B1–B9 self-test added; real browser execution still required on an unrestricted browser**

## ACTIVE BRANCH
`animator/b10-browser-smoke`

## HARD START
B9 sprite-sheet slicing existed and was integrated after B8, but a real browser click-through had not been completed. The local Chromium available to ChatGPT is policy-blocked from opening both `file://` pages and localhost, so B10 must not pretend that environment produced a runtime PASS.

## WHAT CHANGED
Added `b10-browser-smoke-test.js` and wired it to load only after B9 is available.

The B10 test panel performs a reversible self-test of the loaded B1–B9 chain:
- checks the B1–B3 core runtime object;
- checks the B4 reel/snapshot API;
- checks B6 onion-skin API;
- checks B7 playback API;
- checks B8 batch-import API;
- waits for and verifies the B9 sprite-sheet slicer API;
- checks required editor DOM controls;
- creates a temporary synthetic character and 1×2 sprite sheet;
- runs the real B9 sheet loader and slice-to-frame path;
- verifies that exactly two reel frames are created in row-major identity order;
- restores the prior Animator state, reel, and localStorage after the test.

`b8-batch-pose-import.js` now loads the B10 smoke-test script only after the isolated B9 feature has loaded. Existing B8 import behavior remains unchanged.

## VERIFICATION
- `b10-browser-smoke-test.js` passed `node --check` before repository write.
- B10 source was written successfully to GitHub.
- B8→B9→B10 loader ordering was committed on the B10 branch.
- ChatGPT's available Chromium cannot execute local/localhost pages because of environment policy; that limitation is recorded rather than mislabeled as an Animator failure.

## HOW TO RUN THE REAL TEST
Open `Tools/Chats-Animator/index.html` from branch `animator/b10-browser-smoke` in an unrestricted browser. In the right-side panel, click **Run B1–B9 Smoke Test**. The report must begin with `B10 RESULT: PASS` before B1–B9 are labeled browser-runtime verified.

## PROTECTED WORKING FEATURES
B1 through B9 remain protected. B10 adds verification only; it does not add tweening, artwork generation, audio, camera, export, or new animation behavior.

## FIELD NOTES
The smoke-test attempt exposed an important process issue: repository/static integration is not equivalent to browser verification. B10 turns that distinction into an executable project check instead of relying on narrative status.

## VOID OVERSIGHT / OVERRIDE NOTES
**CORRECT:** Do not mark browser PASS from syntax checks or connector fetches. Require the in-app B10 result from a real unrestricted browser.

## ATTEMPT / STRIKE COUNT
Approach 1/3 — direct local Chromium execution was blocked by environment policy, not by application evidence. Replacement approach: repository-backed reversible in-app smoke test.

## HARD STOP
B10 stops at providing the deterministic browser self-test and loader integration. No next feature is started until the smoke test is actually run.

## NEXT PERMITTED STEP
If B10 reports PASS on Ubuntu/Jetson, record B1–B9 as browser-runtime verified and start the next bounded feature branch. If it reports FAIL, fix only the concrete failing check before moving on.
