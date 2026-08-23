# Jetson Animator Runner v1

Installable local job runner for the One-Wave Animator.

**No OpenClaw. No cloud API. No tokens. Python standard library only.**

## Install on the Jetson

```bash
cd Tools/Jetson-Animator-Runner
chmod +x install.sh uninstall.sh
./install.sh
```

Installed command:

```bash
~/.local/bin/animator-runner
```

If needed:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## First test

```bash
animator-runner run examples/health.json
```

A successful result contains `"status": "pass"`.

## Local state

```text
~/.local/share/one-wave/animator-runner/
├── jobs/
├── results/
├── logs/
└── state/
```

## Queue worker

Put JSON jobs in the `jobs/` directory, then run:

```bash
animator-runner worker --once
```

or leave it running:

```bash
animator-runner worker
```

## v1 registered actions

- `health`
- `project.manifest`
- `file.copy`

The runner deliberately does **not** execute arbitrary shell commands in v1.

This branch is only the installable local execution foundation. Actual Animator production actions come next after the runner is proven on the Jetson.
