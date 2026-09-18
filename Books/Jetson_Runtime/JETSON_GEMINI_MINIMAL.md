# Jetson Gemini — Minimal-Token External Worker

## Purpose

Gemini is the **external escalation/review lane** for the Jetson. It is not the
default worker.

Normal order:

```text
Deterministic tools/tests
        ↓
local Qwen / OpenClaw
        ↓ only when external judgment is useful
Gemini flash-lite review
        ↓ only for bounded coding that needs more capability
Gemini flash code
        ↓ explicit opt-in only
Gemini pro/deep
```

This keeps routine work local and avoids repeatedly sending repository context
to a cloud model.

## What is committed

```text
GEMINI.md                         tiny always-loaded project rules
.gemini/settings.json             low-context/session/tool-output limits
.geminiignore                     blocks binaries, caches, generated files, secrets
scripts/install_gemini_jetson.sh user-local installer; no sudo
scripts/gemini_min.sh             bounded review/code/ask/deep runner
GEMINI_TASK_TEMPLATE.md           small task packet template
```

## Install on the Jetson

From the existing checkout:

```bash
cd /home/Scales/One-Wave-Science
git pull --ff-only origin main
bash scripts/install_gemini_jetson.sh
```

The installer uses the official npm package and installs it under
`~/.local`, so it does not need sudo.

## Authenticate once

Preferred path is the official Gemini CLI's own Google login. On a Jetson or
SSH terminal with no browser:

```bash
cd /home/Scales/One-Wave-Science
NO_BROWSER=true ~/.local/bin/gemini
```

Complete the URL/code flow in another browser when prompted. The official CLI
caches its own credential for later sessions.

An API key is an optional supported authentication path, not a repository
requirement. If you use one, keep it outside the repository (for example in a
private shell environment). Never commit it to `.env`, task files, logs, or
GitHub.

Do not route Gemini CLI OAuth credentials through OpenClaw or another
third-party provider. If later programmatic service-to-service Gemini access is
needed, treat that as a separate supported API-key/Vertex integration.

## First smoke test

```bash
cd /home/Scales/One-Wave-Science
bash scripts/gemini_min.sh ask "Reply with only: GEMINI JETSON OK"
```

The wrapper requests JSON output. Gemini CLI includes usage statistics in its
headless JSON result, so input/output/thought/tool token usage can be inspected
instead of guessed.

## Bounded review

Create a tiny task packet. Reference files by path instead of pasting them.

```bash
cp GEMINI_TASK_TEMPLATE.md /tmp/gemini-task.md
nano /tmp/gemini-task.md
bash scripts/gemini_min.sh review /tmp/gemini-task.md
```

`review` uses `flash-lite`.

## Bounded coding

Use a separate branch/worktree. The wrapper refuses `main` and a dirty working
tree by default so Gemini does not collide with Codex or another worker.

```bash
cd /home/Scales/One-Wave-Science
git switch -c gemini/my-bounded-task
bash scripts/gemini_min.sh code /tmp/gemini-task.md
```

`code` uses `flash` and `auto_edit`: file edit tools may proceed, while broader
commands are not silently YOLO-approved. The task should name allowed files and
the deterministic test to run afterward.

## Deep model is intentionally gated

```bash
GEMINI_ALLOW_PRO=1 bash scripts/gemini_min.sh deep /tmp/gemini-task.md
```

Do not make this the normal path. If `flash-lite` or local Qwen can answer the
question, using Pro just burns more external inference.

## Token controls

Project settings intentionally:

- default to `flash-lite`;
- cap session turns;
- trigger context compression early;
- lower retained/history token budgets;
- summarize large shell output before it becomes model context;
- disable recursive file search;
- respect `.gitignore` and `.geminiignore`;
- disable Gemini auto-memory for this repo;
- disable usage-statistics telemetry;
- disable YOLO mode and permanent tool approval.

The wrapper additionally:

- disables extensions with `--extensions none`;
- rejects task packets larger than 16 KB;
- includes only repo/branch/HEAD plus the bounded task in its prompt;
- tells Gemini not to scan or summarize unrelated files;
- defaults review/ask to `flash-lite`;
- uses `flash` only for code;
- requires explicit `GEMINI_ALLOW_PRO=1` for Pro;
- refuses coding directly on `main` unless explicitly overridden.

## Working with local Qwen/OpenClaw

Keep the two paths separate:

```text
M4 / OpenClaw
    └── local qwen3.5:2b
           ├── deterministic test enough -> finish locally
           └── external judgment useful -> write tiny task/reference packet
                                                ↓
                                     official Gemini CLI wrapper
```

OpenClaw does not need Gemini credentials. It can prepare a small task/reference
file for the official Gemini process, and the returned bounded result can be
reviewed locally.

## Miniverse

The current Miniverse MUD PR already accepts an agent identity named `gemini`,
but that client is a coordination terminal, not an autonomous model process.
First prove this official Gemini CLI worker on the Jetson. Then an Agent Gateway
can hand bounded MUD jobs to this wrapper without giving Gemini unrestricted
shell, raw-device, or credential authority.

## Hard stops

Gemini must not receive:

- raw-drive or formatting authority;
- sudo authority;
- repository/API credentials;
- whole-repo dumps as routine context;
- an instruction to merge its own work;
- permission to rewrite its own acceptance criteria silently.

Prefer reference paths and deterministic tests. External model output is a
candidate/review, not self-validating evidence.
