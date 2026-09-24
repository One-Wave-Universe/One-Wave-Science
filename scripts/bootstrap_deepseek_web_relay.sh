#!/usr/bin/env bash
set -euo pipefail
umask 077

SOURCE_URL="https://github.com/maresin/deepseek-automation-api.git"
SOURCE_REF="cd952329bf5525d4e8a5591d951a9bb5610aebe0"
TOOLS_ROOT="${ONE_WAVE_TOOLS_ROOT:-$HOME/One-Wave-Tools}"
RELAY_HOME="${DEEPSEEK_WEB_RELAY_HOME:-$TOOLS_ROOT/deepseek-web-relay}"
STATE_ROOT="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-deepseek-web-relay"
PORT="${DEEPSEEK_WEB_PORT:-3000}"
PID_FILE="$STATE_ROOT/relay.pid"
LOG_FILE="$STATE_ROOT/relay.log"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"

for cmd in git node npm python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "DEEPSEEK_WEB_RELAY_MISSING: $cmd" >&2
    exit 2
  fi
done

mkdir -p "$TOOLS_ROOT" "$STATE_ROOT"
chmod 700 "$TOOLS_ROOT" "$STATE_ROOT"

if [[ ! -d "$RELAY_HOME/.git" ]]; then
  git clone --filter=blob:none --no-checkout "$SOURCE_URL" "$RELAY_HOME"
fi

git -C "$RELAY_HOME" fetch --depth 1 origin "$SOURCE_REF"
git -C "$RELAY_HOME" checkout --detach "$SOURCE_REF"

# The pinned upstream currently declares a postinstall script that is absent
# from the repository. Install dependencies without lifecycle scripts, then
# install Chromium explicitly through playwright-core.
(
  cd "$RELAY_HOME"
  npm install --ignore-scripts
)

# Keep the third-party relay private to the Jetson. Do not expose its local API
# on the LAN or through the existing Hive Pipe tunnel.
python3 - "$RELAY_HOME/server.js" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
old = "app.listen(PORT, () => {"
new = "app.listen(PORT, '127.0.0.1', () => {"
if new not in text:
    if old not in text:
        raise SystemExit("DEEPSEEK_WEB_RELAY_PATCH_FAILED: server listen shape changed")
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
PY

(
  cd "$RELAY_HOME"
  npm run build
  mkdir -p browsers
  PLAYWRIGHT_BROWSERS_PATH="$RELAY_HOME/browsers" npx playwright-core install chromium
)

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
  if [[ -f "$PID_FILE" ]]; then
    old_pid="$(cat "$PID_FILE" 2>/dev/null || true)"
    if [[ "$old_pid" =~ ^[0-9]+$ ]] && kill -0 "$old_pid" 2>/dev/null; then
      kill "$old_pid" || true
    fi
  fi
  (
    cd "$RELAY_HOME"
    export PORT
    export PLAYWRIGHT_BROWSERS_PATH="$RELAY_HOME/browsers"
    export DEEPSEEK_HEADLESS="${DEEPSEEK_WEB_HEADLESS:-true}"
    export DEEPSEEK_SHOW_BROWSER="${DEEPSEEK_WEB_SHOW_BROWSER:-false}"
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

if [[ ! -s "$RELAY_HOME/.api-key" || ! -s "$RELAY_HOME/state.json" ]]; then
  if [[ ! -t 0 ]]; then
    echo "DEEPSEEK_WEB_RELAY_LOGIN_REQUIRED: run this script from an interactive Jetson shell" >&2
    exit 4
  fi

  printf 'DeepSeek account email: '
  IFS= read -r DEEPSEEK_BOOT_EMAIL
  printf 'DeepSeek account password (not saved): '
  IFS= read -r -s DEEPSEEK_BOOT_PASSWORD
  printf '\n'
  export DEEPSEEK_BOOT_EMAIL DEEPSEEK_BOOT_PASSWORD

  python3 - "$PORT" <<'PY'
import json
import os
import sys
from urllib.request import Request, urlopen

port = int(sys.argv[1])
payload = {
    "email": os.environ["DEEPSEEK_BOOT_EMAIL"],
    "password": os.environ["DEEPSEEK_BOOT_PASSWORD"],
}
request = Request(
    f"http://127.0.0.1:{port}/v1/register",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urlopen(request, timeout=180) as response:
    result = json.load(response)
if not result.get("api_key"):
    raise SystemExit("DEEPSEEK_WEB_RELAY_REGISTER_FAILED: no local relay key returned")
print("DEEPSEEK_WEB_RELAY_LOGIN_OK")
PY

  unset DEEPSEEK_BOOT_PASSWORD DEEPSEEK_BOOT_EMAIL
fi

chmod 600 "$RELAY_HOME/.api-key" "$RELAY_HOME/state.json" 2>/dev/null || true

export DEEPSEEK_WEB_BASE_URL="http://127.0.0.1:$PORT"
export DEEPSEEK_WEB_API_KEY_FILE="$RELAY_HOME/.api-key"
python3 "$REPO_ROOT/One_Wave_Bench/hive-pipe/deepseek_web_bridge.py" --relay-health --mcp-smoke

echo "DEEPSEEK_WEB_RELAY_READY"
echo "worker: bash scripts/deepseek_web_worker.sh 'your task'"
