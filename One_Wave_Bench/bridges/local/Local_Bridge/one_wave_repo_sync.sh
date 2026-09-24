#!/usr/bin/env bash
set -euo pipefail

REPO="${ONE_WAVE_REPO:-$HOME/One-Wave-Science-git}"
LOG_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-local-bridge"
LOG_FILE="$LOG_DIR/sync.log"
mkdir -p "$LOG_DIR"

stamp() { date '+%Y-%m-%d %H:%M:%S'; }
log() { printf '%s  %s\n' "$(stamp)" "$*" >> "$LOG_FILE"; }

if [[ ! -d "$REPO/.git" ]]; then
  log "ERROR repo not found at $REPO"
  exit 1
fi

cd "$REPO"

# Never overwrite uncommitted laptop work.
if [[ -n "$(git status --porcelain)" ]]; then
  log "SKIP local working tree has changes"
  exit 0
fi

branch="$(git symbolic-ref --quiet --short HEAD || true)"
if [[ "$branch" != "main" ]]; then
  log "SKIP current branch is ${branch:-detached}; expected main"
  exit 0
fi

if ! git fetch origin main >>"$LOG_FILE" 2>&1; then
  log "ERROR git fetch failed"
  exit 1
fi

local_sha="$(git rev-parse HEAD)"
remote_sha="$(git rev-parse origin/main)"

if [[ "$local_sha" == "$remote_sha" ]]; then
  log "OK already current $local_sha"
  exit 0
fi

# Only fast-forward. No reset, no force, no deletion of local work.
if git merge-base --is-ancestor "$local_sha" "$remote_sha"; then
  if git merge --ff-only origin/main >>"$LOG_FILE" 2>&1; then
    log "UPDATED $local_sha -> $remote_sha"
  else
    log "ERROR fast-forward failed"
    exit 1
  fi
else
  log "SKIP local main diverged from origin/main"
fi
