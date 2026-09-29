#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "ERROR: run inside One-Wave-Science" >&2
  exit 2
}
cd "$ROOT"
exec python3 scripts/brain_buddy_council.py "$@"
