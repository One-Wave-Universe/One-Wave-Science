# Branch-Step Project Template

## MAIN GOAL
Build and improve the Field/Void coding engine for real code, apps, and programs. This goal is repeated in every branch-step and may not be replaced by a local subtask.

## WHY THIS STEP EXISTS
Explain how this exact step advances the MAIN GOAL.

## CURRENT STEP GOAL
One bounded software-building objective only.

## HARD START
List the exact conditions that must already be true before work begins.

## LOCAL REPO ROOT
`$HOME/One-Wave-Science`

Before work, record:

```bash
cd "$HOME/One-Wave-Science"
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git worktree list
```

If the path/branch/worktree is not the expected one, STOP.

## ACTIVE BRANCH-STEP PROJECT
- Branch:
- Worktree:
- HEAD:
- Parent/previous step:
- Next permitted step:

## REFERENCE FILES
List all architecture, rules, progress, diary, failed-approach, working-feature, and prior-handoff files that must be reread before action.

## ALLOWED FILES
List files/directories this step may modify.

## PROTECTED WORKING FEATURES
List verified behavior that must remain passing.

## FIELD ROLE — GPU PRIORITY
Field proposes and performs one targeted code/app/program change. Record:

- intended change
- reason
- files expected to change
- expected software behavior
- exact success test
- Field notes/discoveries

## VOID ROLE — CPU PRIORITY / OVERSIGHT OVERRIDE
Void checks the proposal and actual result against the reference. It may return:

- `ALLOW`
- `CORRECT`
- `OVERRIDE`
- `HOLD`
- `ESCALATE`

Void records:

- reference state
- discrepancy/differential
- regression risk
- evidence
- protected behavior
- override/correction if required

## OPENCLAW / M4 CONTROL
M4/OpenClaw owns dispatch, branch/worktree state, tests, attempts, diary, progress, commit/handoff, and escalation.

OpenClaw-compatible headless execution can use:

```bash
openclaw agent exec --cwd "$HOME/One-Wave-Science" --message-file TASK.md --json
```

## ONE CHANGE
Describe the one targeted change authorized for the current pass.

## SUCCESS CRITERIA
Observable pass conditions only.

## TESTS / CHECKS
Exact commands and expected results.

## PROGRESS REPORT
- Completed:
- In progress:
- Working:
- Not working:
- Blocked:
- Attempt:
- Tests:
- Field position:
- Void decision:
- M4 next action:

## STRIKE RECORD
### Approach A
- Attempt 1:
- Attempt 2:
- Attempt 3:
- Evidence learned:
- Status: active / abandoned

If three attempts fail, stop Approach A and choose a materially different Approach B. If no credible new approach exists or the replacement approach also becomes stuck, escalate for help.

## LOOK-BACK REFLECTION
- What changed?
- What actually worked?
- What failed?
- What evidence proves it?
- What did we learn?
- Which assumption changed?
- Did all protected software still work?
- Did this advance the MAIN GOAL?
- What must carry forward?

## HARD STOP
State the exact boundary where this branch-step must stop. Work assigned to the next branch is forbidden here.

## HANDOFF
- Known-good commit/state:
- Verified features:
- Open problems:
- Failed approaches not to repeat:
- Files changed:
- Tests that must continue passing:
- Next branch-step:
- Admin/escalation required: YES / NO
