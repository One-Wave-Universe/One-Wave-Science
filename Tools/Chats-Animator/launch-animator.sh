#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${ONE_WAVE_ANIMATOR_PORT:-8765}"
BUILD_ID="$(date +%s)"
URL="http://127.0.0.1:${PORT}/index.html?build=${BUILD_ID}"
RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp}/one-wave-animator"
PID_FILE="$RUNTIME_DIR/server.pid"
DIR_FILE="$RUNTIME_DIR/server-app-dir"
LOG_FILE="$RUNTIME_DIR/server.log"
CONFIG_FILE="$HOME/.config/one-wave-animator/openai.env"
mkdir -p "$RUNTIME_DIR"

if [[ -f "$CONFIG_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$CONFIG_FILE"
fi

server_alive() {
  if [[ -f "$PID_FILE" ]]; then
    local pid
    pid="$(cat "$PID_FILE" 2>/dev/null || true)"
    [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
  else
    return 1
  fi
}

stop_server() {
  if server_alive; then
    kill "$(cat "$PID_FILE")" 2>/dev/null || true
    sleep 0.2
  fi
  rm -f "$PID_FILE" "$DIR_FILE"
}

if server_alive; then
  previous_dir="$(cat "$DIR_FILE" 2>/dev/null || true)"
  if [[ "$previous_dir" != "$APP_DIR" ]]; then
    stop_server
  fi
fi

if ! server_alive; then
  nohup python3 "$APP_DIR/assistant_server.py" >"$LOG_FILE" 2>&1 &
  echo $! > "$PID_FILE"
  printf '%s\n' "$APP_DIR" > "$DIR_FILE"
fi

bridge_ready=0
for _ in {1..20}; do
  if curl --fail --silent "http://127.0.0.1:${PORT}/api/assistant/health" >/dev/null 2>&1; then
    bridge_ready=1
    break
  fi
  sleep 0.15
done

if [[ "$bridge_ready" != "1" ]]; then
  stop_server
  echo "One-Wave Animator could not start its local AI bridge." >&2
  echo "Log: $LOG_FILE" >&2
  if [[ -s "$LOG_FILE" ]]; then
    echo >&2
    tail -n 40 "$LOG_FILE" >&2 || true
  fi
  exit 1
fi

if command -v chromium >/dev/null 2>&1; then
  exec chromium --app="$URL"
elif command -v chromium-browser >/dev/null 2>&1; then
  exec chromium-browser --app="$URL"
elif command -v google-chrome >/dev/null 2>&1; then
  exec google-chrome --app="$URL"
elif command -v google-chrome-stable >/dev/null 2>&1; then
  exec google-chrome-stable --app="$URL"
elif command -v firefox >/dev/null 2>&1; then
  exec firefox --new-window "$URL"
else
  exec xdg-open "$URL"
fi
