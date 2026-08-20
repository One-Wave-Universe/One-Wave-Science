# Field Coder — Local Repository Reference

## Required local repo link

Field must operate on the real local checkout/worktree on the computer, not on model memory or an assumed folder path.

At the HARD START of every Field step, resolve and record:

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
ACTIVE_BRANCH="$(git branch --show-current)"
HEAD="$(git rev-parse HEAD)"
git worktree list --porcelain
```

`REPO_ROOT` is the authoritative local link to the repository files for the active checkout. All file reads, edits, diffs, tests, diary entries, and handoffs resolve from that root.

Every step records `REPO_ROOT`, `ACTIVE_BRANCH`, `HEAD`, exact worktree when used, and repo-root-relative `TARGET_FILES`.

Never hard-code a guessed Ubuntu path. Resolve again if the repo moves or another computer/worktree is used.

Required local references include `$REPO_ROOT/Field_Coder/BUILD_SCOPE.md`, `CORE_RULES.md`, `BUILD_STEPS.md`, `PROGRESS.md`, and `BUILD_DIARY.md`.

A branch is Git state, not automatically a separate folder. If branch-per-folder isolation is used, M4/OpenClaw must create/use Git worktrees and record the exact worktree path.

## Hard stop

No Field edit may begin until local repo root, active branch, HEAD, and permitted target paths are positively identified and recorded.