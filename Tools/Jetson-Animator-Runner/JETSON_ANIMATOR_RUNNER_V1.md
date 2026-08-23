# Jetson Animator Runner v1 — Branch Step

## MAIN GOAL
Run useful One-Wave Animator work locally on the Jetson without OpenClaw or cloud-token dependence.

## CURRENT STEP GOAL
Create a zero-token, standard-library Python runner that installs as a real local command, accepts bounded JSON jobs, writes results/logs, and can later host Animator operations.

## HARD START
Animator B10 remains separately blocked on an unrestricted-browser smoke test. This branch does not modify `Tools/Chats-Animator/**`.

## ACTIVE BRANCH
`jetson/animator-runner-v1`

## ALLOWED FILES
Only `Tools/Jetson-Animator-Runner/**`.

## EXACT ACTION
Create the runner, installer, uninstaller, examples, local job queue/result/log directories, and bounded built-in actions.

## SUCCESS CRITERIA
- Python runner compiles.
- direct health job passes.
- queued health job passes and writes a result file.
- install uses user-local paths and no sudo.
- no OpenClaw, model API, network, or token dependency.
- arbitrary shell execution is absent.

## TESTS / CHECKS
Before repository write, local checks passed:
- Python compile check.
- direct health job: PASS.
- queued health job: PASS.
- result JSON created.

## FIELD NOTES
Keep the first local primitive boring and reliable. Deterministic machine work should not require an agent framework.

## VOID OVERSIGHT / OVERRIDE NOTES
ALLOW with protection: v1 runs registered actions only; do not add arbitrary command execution.

## ATTEMPT / STRIKE COUNT
Approach 1/3 — PASS locally.

## HARD STOP
Stop after the installable runner and its health/manifest/file-copy primitives. No local LLM or rendering work in this branch.

## NEXT PERMITTED STEP
Install and run this branch on the Jetson. After it passes there, add the first actual Animator production action in a new branch.
