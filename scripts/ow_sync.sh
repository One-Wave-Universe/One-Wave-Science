#!/usr/bin/env bash
# One board command. No --ff-only surprise if you already reset to origin.
set -euo pipefail
cd /home/Scales/One-Wave-Science 2>/dev/null || cd "$(git rev-parse --show-toplevel)"
git fetch origin
if git merge-base --is-ancestor HEAD origin/main; then
  git merge --ff-only origin/main
else
  echo "HOLD: local diverged. Park then reset:"
  echo "  git branch backup/jetson-$(date -u +%Y%m%dT%H%M%SZ)"
  echo "  git reset --hard origin/main"
  exit 2
fi
python3 Engine/fifths_circle.py
python3 Engine/rail_chords.py
python3 Engine/field_from_rail.py
