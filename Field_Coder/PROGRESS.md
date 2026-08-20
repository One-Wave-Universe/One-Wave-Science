# Field Coder — Progress Report

## Project

- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/01-shell`
- Current step: 01 — Executable Field shell
- Status: IN PROGRESS
- Attempt: 1/3

## Completed steps

- Step 00 — Project control layer: COMPLETE

## Current goal

Create the smallest executable Field coding-agent shell that starts deterministically and detects a missing required shell component.

## Hard-start evidence

- Step 00 hard stop satisfied.
- `README.md`, `BUILD_SCOPE.md`, `CORE_RULES.md`, `BUILD_STEPS.md`, `PROGRESS.md`, and latest `BUILD_DIARY.md` entry reread from this branch.
- Field-only scope confirmed.
- Step 01 allowed scope confirmed.

## Known-good state

- Control layer complete.
- No Field implementation code exists yet.
- Existing animator/science files and root `AGENTS.md` remain outside this step.

## One allowed change

Add only the initial Field shell source tree, minimal controller entry point, required shell component, and shell-only test.

## Exact success test

1. controller starts and prints deterministic `FIELD_SHELL_READY` with exit 0;
2. required shell component is temporarily made unavailable and controller exits nonzero with deterministic missing-component status;
3. component is restored and controller returns to `FIELD_SHELL_READY` with exit 0.

## Must not add in Step 01

- state memory
- repo reading
- model calls
- editing/diff logic
- external project test execution
- retry logic
- Void logic

## Next allowed action

Create the minimal shell files and run the exact Step 01 shell test.

## Hard stop

After pass -> deliberate failure detected -> restored pass are all recorded, update diary/progress to COMPLETE and stop coding on this branch.