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
mkdir -p "$RUNTIME_DIR"

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

# Replace any server started by another extracted/installed copy.
if server_alive; then
  previous_dir="$(cat "$DIR_FILE" 2>/dev/null || true)"
  if [[ "$previous_dir" != "$APP_DIR" ]]; then
    stop_server
  fi
fi

# Prefer the live local assistant server. If it cannot start, keep the animator
# usable and fall back to a plain local file server; the dialogue reports AI
# availability separately instead of killing the whole editor.
if ! server_alive; then
  nohup python3 "$APP_DIR/assistant_server.py" >"$LOG_FILE" 2>&1 &
  echo $! > "$PID_FILE"
  printf '%s\n' "$APP_DIR" > "$DIR_FILE"
  sleep 0.5
fi

if ! curl --fail --silent "http://127.0.0.1:${PORT}/api/assistant/health" >/dev/null 2>&1; then
  if server_alive; then
    stop_server
  fi
  nohup python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$APP_DIR" >"$LOG_FILE" 2>&1 &
  echo $! > "$PID_FILE"
  printf '%s\n' "$APP_DIR" > "$DIR_FILE"
  sleep 0.35
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
