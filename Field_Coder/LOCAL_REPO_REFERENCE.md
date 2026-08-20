# Field Coder — Local Repository Reference

## Required local repo link

Field must operate on the real local checkout/worktree on the computer, not on model memory or an assumed folder path.

At the HARD START of every Field step, resolve and record:

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
ACTIVE_BRANCH="$(git branch --show-current)"
git worktree list --porcelain
```

`REPO_ROOT` is the authoritative local link to the repository files for the active checkout. All file reads, edits, diffs, tests, diary entries, and handoffs must resolve from that root.

## Required pre-step record

Every step must record:

- `REPO_ROOT`: absolute local path returned by Git
- `ACTIVE_BRANCH`: current Field branch
- `HEAD`: `git rev-parse HEAD`
- `WORKTREE`: exact worktree entry, when worktrees are used
- `TARGET_FILES`: repo-root-relative paths that this step is allowed to touch

Never hard-code a guessed Ubuntu path. If the repository is moved, remounted, or checked out on another computer, resolve the location again.

## Local-file rule

Use repo-root-relative references such as:

- `$REPO_ROOT/Field_Coder/BUILD_SCOPE.md`
- `$REPO_ROOT/Field_Coder/CORE_RULES.md`
- `$REPO_ROOT/Field_Coder/BUILD_STEPS.md`
- `$REPO_ROOT/Field_Coder/PROGRESS.md`
- `$REPO_ROOT/Field_Coder/BUILD_DIARY.md`

The branch is a Git state, not automatically a separate folder. If branch-per-folder isolation is required, M4/OpenClaw must use Git worktrees and record the worktree path before work begins.

## Hard stop

A Field step may not begin editing if the local repo root, active branch, and HEAD have not been positively identified and recorded.