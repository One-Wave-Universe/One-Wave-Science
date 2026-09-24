#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if [[ "$#" -ne 1 ]]; then
  echo "usage: $0 <named-action>" >&2
  python3 "$SCRIPT_DIR/mudl.py" actions >&2
  exit 2
fi
python3 "$SCRIPT_DIR/mudl.py" enqueue "$1"

