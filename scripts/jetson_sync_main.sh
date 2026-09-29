#!/usr/bin/env bash
# Park local-only commits, put this checkout on origin/main.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git fetch origin
git switch main >/dev/null 2>&1 || git checkout main
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
if ! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git status --porcelain)" ]]; then
  git stash push -u -m "jetson-sync-$STAMP" || true
fi
git branch "backup/jetson-$STAMP" || true
git reset --hard origin/main
echo "HEAD=$(git rev-parse --short HEAD)"
if [[ -f Engine/parser2_goblins.py ]]; then
  python3 Engine/parser2_goblins.py
else
  echo "HOLD: parser still missing after reset"
  exit 2
fi
