#!/usr/bin/env bash
set -euo pipefail
ROOT="${HOME}/One-Wave-Science"
MEMORY="${ZER0_MEMORY:-${HOME}/.local/share/algorythm-zer0-brain}"
cd "$ROOT"
exec python3 jetson_brain/brain.py --memory "$MEMORY" --repl
