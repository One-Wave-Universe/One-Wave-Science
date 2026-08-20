# Field Coder — Core Rules

These rules are permanent for the Field Coder project and must be read before every coding pass.

## Carry-forward law

The complete contents of `BUILD_SCOPE.md`, `CORE_RULES.md`, `BUILD_STEPS.md`, `PROGRESS.md`, and the latest `BUILD_DIARY.md` entry carry forward automatically into every later step and branch.

No step starts from model memory alone.

## Work discipline

1. Work on one build step at a time.
2. Inside a step, make one targeted code change at a time.
3. State the exact intended change before editing.
4. State the exact success test before editing.
5. Touch only files allowed by the active step unless the diary records why an additional file is necessary.
6. Test immediately after each code change.
7. Inspect actual evidence before deciding the next action.
8. Preserve all previously verified behavior.
9. Do not implement features assigned to future branches early.
10. Never mark a step complete because code merely looks correct.
11. Never silently change architecture, scope, or role definitions.
12. Do not merge Void responsibilities into Field.

## Failure discipline

Each specific approach receives at most three meaningful attempts.

- Attempt 1: execute the planned approach.
- Attempt 2: make a targeted correction based on failure evidence.
- Attempt 3: use a materially different correction or implementation direction.
- After attempt 3 fails: stop the approach and record it as blocked/abandoned.

A fourth attempt may not be disguised as a new approach.

## Mandatory pre-pass record

Before each change, confirm in the diary:

- active branch
- active step
- current goal
- hard-start conditions satisfied
- known-good state
- attempt number
- exact change intended
- files expected to change
- behavior that must remain unchanged
- exact success test

## Mandatory post-pass record

After each change/test, record:

- files actually changed
- exact command/check run
- exit status/result
- observed behavior
- what worked
- what failed
- what was learned
- keep / revert / retry / replan / blocked decision
- next permitted action

Then update `PROGRESS.md`.

## Hard-stop law

When the active step's hard-stop condition is reached, stop coding on that branch.

Do not begin the next branch until:

- current step success criteria are satisfied,
- progress is updated,
- diary is updated,
- known-good state is recorded,
- the next branch's hard-start conditions are satisfied.

## Project memory law

The repository files are project memory. A replacement AI must be able to resume by reading the Field Coder control files without relying on conversation history.
