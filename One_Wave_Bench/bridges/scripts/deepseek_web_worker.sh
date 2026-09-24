#!/usr/bin/env bash
set -euo pipefail
umask 077

TOOLS_ROOT="${ONE_WAVE_TOOLS_ROOT:-$HOME/One-Wave-Tools}"
RELAY_HOME="${DEEPSEEK_WEB_RELAY_HOME:-$TOOLS_ROOT/deepseek-web-relay}"
STATE_ROOT="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-deepseek-web-relay"
PORT="${DEEPSEEK_WEB_PORT:-3000}"
PID_FILE="$STATE_ROOT/relay.pid"
LOG_FILE="$STATE_ROOT/relay.log"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"

if [[ ! -d "$RELAY_HOME/.git" || ! -s "$RELAY_HOME/.api-key" || ! -s "$RELAY_HOME/state.json" ]]; then
  echo "DEEPSEEK_WEB_RELAY_NOT_BOOTSTRAPPED" >&2
  echo "Run: bash One_Wave_Bench/bridges/scripts/bootstrap_deepseek_web_relay.sh" >&2
  exit 2
fi

mkdir -p "$STATE_ROOT"
chmod 700 "$STATE_ROOT"

relay_health() {
  python3 - "$PORT" <<'PY' >/dev/null 2>&1
import json
import sys
from urllib.request import urlopen

port = int(sys.argv[1])
with urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as response:
    body = json.load(response)
if body.get("status") != "ok":
    raise SystemExit(1)
PY
}

if ! relay_health; then
  (
    cd "$RELAY_HOME"
    export PORT
    export PLAYWRIGHT_BROWSERS_PATH="$RELAY_HOME/browsers"
    export DEEPSEEK_HEADLESS=true
    export DEEPSEEK_SHOW_BROWSER=false
    export DEEPSEEK_RESTORE_SESSION=true
    export RESTORE_SESSION=true
    nohup npm start >"$LOG_FILE" 2>&1 &
    echo $! >"$PID_FILE"
  )

  for _ in $(seq 1 30); do
    if relay_health; then
      break
    fi
    sleep 1
  done
fi

if ! relay_health; then
  echo "DEEPSEEK_WEB_RELAY_START_FAILED" >&2
  echo "log: $LOG_FILE" >&2
  exit 3
fi

export DEEPSEEK_WEB_BASE_URL="http://127.0.0.1:$PORT"
export DEEPSEEK_WEB_API_KEY_FILE="$RELAY_HOME/.api-key"
exec python3 "$REPO_ROOT/One_Wave_Bench/bridges/hive-pipe/deepseek_web_bridge.py" "$@"
