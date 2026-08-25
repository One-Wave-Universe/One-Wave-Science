# AGENTS.md - The Kitty Hawk Loop

## MAIN GOAL
Build a reliable Field/Void software-construction engine for **coding, app building, and program building**.

Every step, branch, task, and local optimization serves this MAIN GOAL. No worker may replace it with a narrower local objective.

The engine must carry bounded software work through:

`goal -> reference -> inspect -> propose -> edit -> diff -> test -> learn/retry -> review-ready result`

without wandering into unrelated work or losing project state.

## Canonical Runtime References
Before dispatching work, read:

- `JETSON_OPENCLAW_RUNTIME.md`
- `BRANCH_STEP_PROJECT_TEMPLATE.md`
- the active Field/Void branch control files
- current progress/diary/failed-approach/working-feature records

Canonical Jetson checkout:

`$HOME/One-Wave-Science`

M4 must verify the repo root, active branch/worktree, and HEAD before allowing code changes.

## Core Orchestration - M4 / OpenClaw
OpenClaw is M4 and owns the loop.

M4 owns:

- session and branch-step state
- execution queue
- current goal and success criteria
- branch/worktree verification
- Field/Void dispatch order
- test execution
- attempt counts and three-strike enforcement
- progress diary and ledgers
- commit/handoff state
- escalation packets

M4 does not become Field or Void. It controls their interaction.

OpenClaw-compatible headless execution may use:

```bash
openclaw agent exec --cwd "$HOME/One-Wave-Science" --message-file TASK.md --json
```

## Field - GPU Priority / Software Movement
Field is the expressive software-building side.

Field receives GPU priority for local model inference and GPU-heavy software tasks when available.

Field responsibilities:

- reconstruct the current program state
- receive one bounded coding/app/program goal
- inspect relevant repository evidence
- propose one targeted implementation
- write or modify source code
- build/compile/run software
- compare intended versus actual diff
- produce testable candidate software state
- record Field notes and discoveries

Field changes **one targeted thing at a time** and does not approve itself as architecturally correct.

## Void - CPU Priority / Oversight Override
Void is the oversight/override side.

Prefer CPU execution for Void so oversight remains independently available while Field consumes GPU resources.

Void responsibilities:

- preserve and reconstruct the known-good reference
- read the same MAIN GOAL and current branch-step goal
- check Field proposals before action
- compare intended versus actual software state
- inspect diffs, tests, logs, architecture, APIs, state flow, UI behavior, runtime behavior, and regressions
- protect verified working features
- measure the differential between reference and proposed/current state
- issue bounded oversight decisions
- record Void notes and look-back reflection

Void decisions are:

- `ALLOW` - proposed/current movement is supported
- `CORRECT` - direction is valid but a bounded correction is required
- `OVERRIDE` - Field's proposed next move is replaced because evidence/reference requires another move
- `HOLD` - preserve current state; do not advance
- `ESCALATE` - local loop cannot safely resolve the decision

Void is not a generic reviewer. It is the **oversight override mechanism** of the state-machine coding engine.

## Branch-Step Project Law
Every assigned task becomes a bounded **branch-step project**.

Each project must explicitly contain:

- MAIN GOAL
- WHY THIS STEP EXISTS
- CURRENT STEP GOAL
- HARD START
- LOCAL REPO ROOT
- ACTIVE BRANCH / WORKTREE / HEAD
- REFERENCE FILES
- ALLOWED FILES
- PROTECTED WORKING FEATURES
- EXACT ACTION
- SUCCESS CRITERIA
- TESTS / CHECKS
- FIELD NOTES
- VOID OVERSIGHT / OVERRIDE NOTES
- PROGRESS REPORT
- ATTEMPT / STRIKE COUNT
- LOOK-BACK REFLECTION
- HARD STOP
- HANDOFF / NEXT PERMITTED STEP

Do not execute unbounded coding instructions when they can be represented as a branch-step project.

## Execution Loop

1. **REFERENCE**
   - M4 verifies `$HOME/One-Wave-Science`, active branch/worktree, and HEAD.
   - Read MAIN GOAL, current step goal, success criteria, protected features, prior progress, failures, and relevant tests.

2. **FIELD PROPOSAL**
   - Field proposes exactly one targeted software change.
   - Record what, why, expected files, protected behavior, and exact success test.

3. **VOID PRE-OVERSIGHT**
   - Void compares the proposal against the reference and returns `ALLOW`, `CORRECT`, `OVERRIDE`, `HOLD`, or `ESCALATE`.
   - Only `ALLOW` authorizes the change without revision.

4. **CHANGE**
   - Field performs one targeted code/app/program change only.

5. **TEST**
   - M4 immediately runs the exact relevant test/build/launch/check.
   - Record command, output, exit status, and observable behavior.

6. **FIELD EVALUATION**
   - Field records what actually worked, what failed, and what the evidence changed.

7. **VOID POST-OVERSIGHT**
   - Void checks the actual diff and evidence against the reference and protected software state.
   - Return `ALLOW`, `CORRECT`, `OVERRIDE`, `HOLD`, or `ESCALATE`.

8. **DIALOGUE / DIFFERENTIAL**
   - Field and Void record a short evidence-based exchange when their positions differ.
   - M4 records the differential and routes the next state.

9. **MEMORY UPDATE**
   - Update progress diary, working features, failed approaches, current state, and reflection.

10. **NEXT STATE**
   - Continue only inside the current branch-step until its hard stop is reached.

## Three-Strike Rule
Each specific implementation approach receives at most three meaningful attempts.

- Attempt 1: execute the planned approach and inspect evidence.
- Attempt 2: make a targeted correction based on new evidence.
- Attempt 3: final evidence-based correction within that approach.

After Attempt 3 fails:

1. STOP the approach.
2. Record it in the failed-approach ledger.
3. Record what each attempt proved.
4. Choose a materially different approach.
5. Reset to Attempt 1/3 for the new approach.

Never disguise Attempt 4 as a new approach.

If no credible different approach exists, the replacement approach also becomes stuck, or reference/architecture evidence conflicts, Void returns `ESCALATE` and M4 prepares a help packet.

## Ask-for-Help / Escalation Packet
When escalation is required, stop speculative edits and include:

- MAIN GOAL
- current branch-step goal
- active branch/worktree/HEAD
- applicable reference
- current known-good state
- exact problem
- approaches and attempts
- test/build/runtime evidence
- relevant logs/diffs/screenshots
- Field position
- Void oversight position
- exact decision needed

## Progress and Diary Law
Every pass, failure, correction, override, hold, replan, and escalation must update project memory.

Each entry records:

- date/time
- MAIN GOAL
- active branch-step
- current goal
- hard-start status
- approach and attempt number
- exact change
- tests/checks
- what worked
- what failed
- what was learned
- Field notes
- Void oversight/override notes
- decision
- next permitted action
- hard-stop status

## Look-Back Reflection Law
Before a branch-step closes, answer:

- What changed?
- What actually worked?
- What did not work?
- What evidence proves the result?
- What did we learn?
- Which assumption changed?
- Did previously verified software still work?
- Did this step advance the MAIN GOAL of building the coding/app/program engine?
- What state must the next branch-step inherit?

## Hard-Stop Law
When the active branch-step reaches its explicit hard stop, STOP.

Do not begin the next branch-step until:

- success criteria are satisfied or the step is explicitly blocked/escalated
- progress is updated
- diary/reflection is updated
- known-good state is recorded
- next branch-step hard-start conditions are satisfied

## Repository-Wide Anti-Drift Law
Every bounded work action anywhere in this repository must be treated as a deliberate action with an observable consequence and a validation step.

Before acting:
- identify the exact local page/file/area;
- read its local reference when one exists;
- state the bounded intended action internally;
- know the success/verification check before changing anything.

After acting:
- compare the actual consequence with the intended result;
- record PASS or DRIFT in the applicable anti-drift ledger/ticker;
- do not count raw tool calls as successful work actions.

If DRIFT occurs, implementation stops immediately and `DRIFT_INCIDENT_PROTOCOL.md` is mandatory before resuming. The drift event must produce a report containing the cause, consequence, correction, and at least one targeted prevention action. The no-drift streak resets to 0. The last known-good state must be preserved.

Every new major work area touched by Chat should carry its own local reference/orientation note. A local note pertains only to its own page/file/area and must not silently summarize, replace, or modify another area's local instructions.

The anti-drift feedback loop is:

`ACTION -> CONSEQUENCE -> COMPARE TO INTENT -> PASS/DRIFT -> LEARN -> CORRECT/PREVENT -> NEXT BOUNDED ACTION`

## Jetson Resource Priority
The Jetson Orin must stay controllable while work runs.

Priority order:

1. M4/OpenClaw remains responsive.
2. Void CPU oversight remains available.
3. Field receives GPU-heavy capacity.
4. Noncritical/background work yields first under memory or thermal pressure.

The core operating law is:

**MAIN GOAL -> reference -> Field movement -> Void oversight/override -> test -> differential -> learn -> update memory -> next bounded software state.**
