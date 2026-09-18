#!/usr/bin/env bash
set -euo pipefail
URL="${MINIVERSE_ROOM_URL:-http://127.0.0.1:8787/}"
BROWSER="${MINIVERSE_BROWSER:-$HOME/.local/opt/firefox/firefox}"
if [[ ! -x "$BROWSER" ]]; then
  BROWSER="/usr/bin/firefox"
fi
exec "$BROWSER" --new-window "$URL"
