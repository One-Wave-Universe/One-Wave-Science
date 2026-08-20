# Field Coder — Local Repository Access

Canonical local checkout: `$HOME/One-Wave-Science` (`~/One-Wave-Science`). This is the working source tree for coding, app/program building, diffs, execution, and tests.

Before every coding pass run:
```bash
cd "$HOME/One-Wave-Science"
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git worktree list
```
Record repo root, branch, HEAD, worktree, and dirty/clean status in the diary.

Canonical coding handbook from any branch:
```bash
git show main:BOT_CODING_HANDBOOK.md
```
Search it when stuck:
```bash
git show main:BOT_CODING_HANDBOOK.md | grep -n -i "TOPIC"
```

Rules: never assume the directory; never edit outside the verified repo root unless explicitly allowed; local Home-folder files are the working source and GitHub is the remote/version-control reference; if branch/worktree is wrong, fix it before editing; if the path is missing or not the expected repository, report `BLOCKED` instead of guessing. Field must inspect source, trace app/program structure, modify allowed files, run builds/tests, inspect diffs, preserve verified behavior, and consult the handbook when stuck.
