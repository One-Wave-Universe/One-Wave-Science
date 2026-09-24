#!/usr/bin/env bash
set -euo pipefail

# Safe bootstrap for any authorized One-Wave host, including the Jetson.
# It fetches bridge code without merging/resetting/switching the active checkout.
# The installed worker uses this real checkout and Git's normal branches directly.
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$PROJECT_ROOT" ]]; then
  echo "Run this from inside the One-Wave-Science checkout." >&2
  exit 2
fi

git -C "$PROJECT_ROOT" fetch origin main
ONE_WAVE_PROJECT_ROOT="$PROJECT_ROOT" \
  git -C "$PROJECT_ROOT" show origin/main:One_Wave_Bench/hive-pipe/install_chatgpt_terminal_pull.sh | \
  ONE_WAVE_PROJECT_ROOT="$PROJECT_ROOT" bash
