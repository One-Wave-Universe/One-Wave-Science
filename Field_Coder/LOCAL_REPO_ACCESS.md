# Field Coder — Local Repository Access

## Canonical local checkout
The computer-side working repository is `$HOME/One-Wave-Science` (`~/One-Wave-Science`). Field uses this local checkout for coding, app/program building, diffs, execution, and tests.

## Mandatory verification before every coding pass
```bash
cd "$HOME/One-Wave-Science"
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git worktree list
```
Record repo root, active branch, HEAD, worktree, and dirty/clean status in the diary before editing.

## Access law
- Never assume the working directory.
- Never edit outside the verified repo root unless explicitly allowed by the active step.
- Local Home-folder files are the working source; GitHub is the remote/version-control reference.
- If the expected branch/worktree is wrong, stop and correct it before editing.
- If `$HOME/One-Wave-Science` is missing or is not the expected repository, report `BLOCKED`; do not guess another folder.
- Field must be able to inspect source, trace app/program structure, modify allowed files, run builds/tests, inspect diffs, and preserve verified behavior.
