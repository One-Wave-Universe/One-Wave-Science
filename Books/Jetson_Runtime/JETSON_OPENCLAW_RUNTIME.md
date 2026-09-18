# Jetson Orin + OpenClaw Runtime Contract

## Main purpose

This repository builds a Field/Void software-construction engine for coding, app building, and program building. The runtime must remain centered on creating, modifying, testing, validating, and improving real software.

## Local machine target

Canonical local checkout on the Jetson Orin:

`$HOME/One-Wave-Science`

Every branch-step project must begin by resolving and recording the real local repository state:

```bash
cd "$HOME/One-Wave-Science"
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git worktree list
```

If `$HOME/One-Wave-Science` is not a valid Git checkout, STOP and report `BLOCKED_REPO_PATH`. Do not guess another path and do not edit files outside the verified repository root.

## M4 / OpenClaw control

OpenClaw is the M4 orchestration layer. M4 owns:

- current branch-step project
- execution queue
- current goal and success criteria
- Field/Void dispatch order
- attempt counter and three-strike rule
- test execution
- branch/worktree verification
- progress diary updates
- working-feature ledger
- failed-approach ledger
- commit/handoff state
- escalation packets

Field and Void do not own the loop. They operate inside the bounded step selected by M4.

OpenClaw-compatible headless execution should use the repository as the working directory, for example:

```bash
openclaw agent exec --cwd "$HOME/One-Wave-Science" --message-file TASK.md --json
```

OpenClaw configuration may instead assign dedicated agent workspaces, but each software-building agent must resolve back to the verified project checkout/worktree before changing code.

## Compute split on Jetson Orin

### Field — GPU priority

Field is the expressive software-building side. Give Field priority access to GPU-backed local inference and GPU-heavy program tasks when available.

Field responsibilities include:

- proposing software changes
- writing/modifying source code
- building apps and programs
- code generation/refactoring
- compiling/building
- GPU-appropriate tests, rendering, simulation, or model-assisted coding work
- producing the candidate next software state

Field must still make one targeted change at a time and must not self-approve architectural correctness.

### Void — CPU priority

Void is the oversight/override side. Prefer CPU execution for Void so oversight remains independently available while Field consumes GPU resources.

Void responsibilities include:

- reconstructing the known-good reference
- checking the current goal and branch boundary
- reviewing proposed changes before execution
- comparing intended versus actual diff
- checking tests, logs, architecture, regressions, APIs, state flow, UI behavior, and runtime behavior
- protecting verified features
- issuing `ALLOW`, `CORRECT`, `OVERRIDE`, `HOLD`, or `ESCALATE`
- writing oversight notes and reflection

Void may use deterministic CPU tools before model inference: Git diff/status, linters, tests, schema checks, static analysis, log comparison, file/hash comparison, and project-specific validation.

## Resource isolation rule

Field may use the GPU, but it must never monopolize the machine so completely that M4/OpenClaw cannot run the control loop or Void cannot perform oversight.

Priority order:

1. M4/OpenClaw remains responsive.
2. Void oversight can execute.
3. Field receives remaining GPU-heavy capacity.
4. Background/noncritical work yields first under memory or thermal pressure.

M4 must stop or defer noncritical work when memory pressure, thermal throttling, or repeated process failure makes results unreliable.

## Branch-step project law

Every assigned task becomes one bounded branch-step project. The branch-step packet must contain:

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
- TEST COMMANDS
- FIELD NOTES
- VOID OVERSIGHT / OVERRIDE NOTES
- PROGRESS REPORT
- ATTEMPT / STRIKE COUNT
- LOOK-BACK REFLECTION
- HARD STOP
- HANDOFF / NEXT PERMITTED STEP

No task may be executed as an unbounded chat instruction when it can be represented as a branch-step project.

## Execution order

1. M4 loads the branch-step packet.
2. M4 verifies `$HOME/One-Wave-Science`, branch/worktree, HEAD, and clean/known state.
3. Field reads the complete reference and proposes one targeted software change.
4. Void performs pre-change oversight and returns `ALLOW`, `CORRECT`, `OVERRIDE`, `HOLD`, or `ESCALATE`.
5. Only `ALLOW` permits the targeted change.
6. Field performs one change.
7. M4 runs the exact tests/checks.
8. Field records what the evidence shows.
9. Void performs post-change oversight against the reference, diff, tests, and protected features.
10. M4 records the decision and updates diary/ledgers.
11. On success, commit and move only to the next permitted branch-step.
12. On failure, apply the three-strike rule.
13. At the hard stop, stop. Do not leak work into the next branch.

## Three-strike rule

Each specific approach receives at most three meaningful attempts.

- Attempt 1: execute the intended approach.
- Attempt 2: make a targeted correction from new evidence.
- Attempt 3: final evidence-based correction within that approach.

After three failures:

- STOP the approach.
- Record it in the failed-approach ledger.
- Summarize what each attempt proved.
- Select a materially different approach and reset to 1/3.
- If no credible different approach exists, or the replacement approach also becomes stuck, `ESCALATE` for help.

Never disguise Attempt 4 as a new approach.

## Look-back reflection law

Before any branch-step is allowed to close, Field, Void, and M4 must answer:

- What changed?
- What actually worked?
- What did not work?
- What evidence proves the result?
- What did we learn?
- Which assumption changed?
- Did previously verified software still work?
- Did this step advance the MAIN GOAL of building the coding/app/program engine?
- What state must the next branch-step inherit?

## Hard stop law

The active branch-step ends when its explicit success criteria and hard-stop condition are satisfied, or when it is blocked/escalated. Reaching a hard stop means STOP. The next step requires a new branch-step packet and a new M4 dispatch.
