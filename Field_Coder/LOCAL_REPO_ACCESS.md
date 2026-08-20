# Field Coder — Local Repository Access

## Canonical local checkout

The computer-side working repository is anchored in the user's Home folder:

`$HOME/One-Wave-Science`

Equivalent shell form:

`~/One-Wave-Science`

Field must treat this local checkout as the working source tree for coding, app building, testing, diffs, and program execution.

## Mandatory verification before every coding pass

Run:

```bash
cd "$HOME/One-Wave-Science"
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git worktree list
```

Record the returned repo root, active branch, HEAD, worktree, and dirty/clean status in the build diary before editing.

## Access law

- Never assume the working directory.
- Never edit outside the verified repo root unless the active step explicitly allows it.
- Never confuse the GitHub remote with the local working files.
- The local Home-folder checkout is where code is read, changed, launched, and tested.
- GitHub is the remote/version-control reference and handoff layer.
- If the expected branch is not checked out, stop and correct branch/worktree state before editing.
- If `$HOME/One-Wave-Science` does not resolve to the expected repository, stop and report BLOCKED rather than guessing another folder.

## Field responsibility

Field must be able to read the local source tree, inspect existing code, trace app/program structure, modify only the active step's allowed files, run local tests/build commands, inspect diffs, and preserve previously verified behavior.
