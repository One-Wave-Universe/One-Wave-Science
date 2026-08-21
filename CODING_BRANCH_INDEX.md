# CODING BRANCH INDEX — READ BEFORE ANY CODING SESSION

**Status:** Mandatory, repo-root, main-branch authority. This file must be readable from `main` without checking out any other branch, because it is the file that tells a new session which branch to check out.

## WHY THIS FILE EXISTS

This project has repeatedly failed when an AI (ChatGPT or otherwise) is pointed at the whole repository and tries to build the entire Field/Void coding engine — or advance several build tracks — inside one session. That always fails. The project only makes real progress when exactly one branch, containing exactly one bounded step, is worked at a time.

`AGENTS.md`, `BOT_CODING_HANDBOOK.md`, and `BRANCH_STEP_PROJECT_TEMPLATE.md` describe *how* to behave once inside a branch-step. This file exists because none of them are visible from `main`, and `main` is where a fresh session usually starts. Without this file, a new session has no way to discover that the per-branch discipline exists at all, so it defaults to trying to do everything at once.

## THE ONE-BRANCH-AT-A-TIME LAW

1. Never attempt to implement, plan, or advance more than one branch-step in a single session.
2. Never work across more than one branch family (below) in a single session.
3. Never work directly on `main`. `main` is for indexes, cross-cutting docs, and merges — not for branch-step implementation.
4. Before writing any code, run:
   ```bash
   git fetch origin
   git branch -r | grep -E 'field-coder/|void-coder/|expressive-coder/'
   ```
   and pick exactly one branch. Do not invent a new branch unless the chosen family's own build plan explicitly calls for the next numbered step.
5. Check out that one branch, then read **only** that branch family's control directory (see below) before touching code. Do not read the other two families' control directories in the same session — they belong to a different implementation track.
6. Do the one step assigned there. Stop at its hard stop. Do not "catch up" other stalled tracks in the same pass — that is exactly the failure mode this file exists to prevent.
7. Commit and push only to the one branch you checked out.

If a task looks like it needs more than one branch to finish, it is not one bounded step — split it and hand the rest to the next branch-step, per `BRANCH_STEP_PROJECT_TEMPLATE.md`.

## BRANCH FAMILIES (current, as of 2026-08-21)

Three separate, non-interchangeable attempts at the same Field/Void coding-engine goal exist as parallel branch chains. They are not merged into `main` yet and must not be merged into each other.

### `field-coder/00-control` … `field-coder/15-field-state-kernel`
- Control directory: `Field_Coder/` (read `Field_Coder/README.md` first, then follow its read order).
- Language/track: Python.
- Status: **furthest along.** Real implementation exists under `Field_Coder/field/` (controller, editor, git_safety, model_adapter, proposal, repo_reader, review_packet, state_kernel, task_intake, test_runner, workflow, …) with a matching `Field_Coder/tests/` suite. Step 15's state kernel is complete with its regression tests passing (see `Field_Coder/PROGRESS.md` on that branch).
- Next action: `Field_Coder/PROGRESS.md` on `field-coder/15-field-state-kernel` explicitly says the next preplanned Field state-machine branch and its own memorandum/hard start must be defined before further work — do that as its own bounded step, not as an extension of Step 15.
- This is the reference example of the discipline actually working: 15 small, tested, one-change-at-a-time steps produced real passing code. Use its `Field_Coder/BUILD_DIARY.md` as a model for how a branch-step should be recorded.

### `void-coder/00-control` … `void-coder/14-real-repo-trial`
- Control directory: `Void_Coder/` (currently only `Void_Coder/BUILD_SCOPE.md` exists).
- Status: **stalled at scope only.** 14 branches exist but each one only restates/locks the project goal — no `Void_Coder/void/` implementation or tests exist yet, unlike the Field track.
- Next action: the next bounded step on this track is to add the first real Void module (state/reference comparison, mirroring `Field_Coder/field/state.py`'s role) with its own test, following the same one-change, memorandum-first discipline that worked for Field. Do not try to implement all of Void's responsibilities (ALLOW/CORRECT/OVERRIDE/HOLD/ESCALATE, diff/test/log inspection, etc., per `AGENTS.md`) in one branch.

### `expressive-coder/00-master-plan` … `expressive-coder/16-real-app-program-trial`
- Control directory: `Expressive_Coder/` (currently only `Expressive_Coder/BRANCH_MEMORANDUM.md` and `Expressive_Coder/MASTER_CODE_PLAN.md` exist).
- Language/track: C++ (a separate expressive-coder build plan, distinct from the Python Field track).
- Status: **stalled at plan only.** 16 branches exist but no `.cpp`/`.h` implementation has landed yet.
- Next action: same pattern as Void — take the smallest first primitive from `Expressive_Coder/MASTER_CODE_PLAN.md`, implement it with a test, one branch, one change.

## WHAT NOT TO DO

- Do not read `Field_Coder/`, `Void_Coder/`, and `Expressive_Coder/` control files in the same session and try to reconcile or advance all three — they are separate tracks by design.
- Do not summarize this file, `AGENTS.md`, or a branch family's control files as a substitute for reading them; `Field_Coder/ENTER_BRANCH_FIRST.md`'s NO-SUMMARY LAW applies to every family, not only Field.
- Do not treat a branch number as license to guess its content. Read that branch's own `BUILD_STEPS.md`/`BRANCH_MEMORANDUM.md`.
- Do not merge one family's unfinished work into another to "make progress faster." Slower and bounded is the only thing that has produced working code here so far.
