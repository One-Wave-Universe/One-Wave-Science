#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  JETSON_GATEWAY_URL=https://... JETSON_GATEWAY_TOKEN=... \
    scripts/jetson_remote.sh [--cwd PATH] [--timeout SECONDS] -- COMMAND...

Examples:
  scripts/jetson_remote.sh -- 'uname -a'
  scripts/jetson_remote.sh --cwd "$HOME/One-Wave-Science" -- 'git status --short'

The URL/token may also be placed in:
  ~/.config/hive-pipe/remote.env
with shell lines:
  export JETSON_GATEWAY_URL='https://...'
  export JETSON_GATEWAY_TOKEN='...'
EOF
}

ENV_FILE="${XDG_CONFIG_HOME:-$HOME/.config}/hive-pipe/remote.env"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

CWD=""
TIMEOUT=120
while [[ $# -gt 0 ]]; do
  case "$1" in
    --cwd)
      CWD="${2:?--cwd needs a path}"
      shift 2
      ;;
    --timeout)
      TIMEOUT="${2:?--timeout needs seconds}"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      break
      ;;
  esac
done

[[ $# -gt 0 ]] || { usage >&2; exit 2; }
: "${JETSON_GATEWAY_URL:?set JETSON_GATEWAY_URL}"
: "${JETSON_GATEWAY_TOKEN:?set JETSON_GATEWAY_TOKEN}"

COMMAND="$*"

python3 - "$JETSON_GATEWAY_URL" "$JETSON_GATEWAY_TOKEN" "$CWD" "$TIMEOUT" "$COMMAND" <<'PY'
import json
import sys
import urllib.error
import urllib.request

url, token, cwd, timeout, command = sys.argv[1:]
payload = {"command": command, "timeout": int(timeout)}
if cwd:
    payload["cwd"] = cwd

req = urllib.request.Request(
    url.rstrip("/") + "/v1/exec",
    data=json.dumps(payload).encode(),
    headers={
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
    },
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=int(timeout) + 15) as r:
        result = json.load(r)
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8", errors="replace")
    print(body, file=sys.stderr)
    raise SystemExit(1)

sys.stdout.write(result.get("stdout", ""))
sys.stderr.write(result.get("stderr", ""))
raise SystemExit(int(result.get("exit_code", 0 if result.get("ok") else 1)))
PY
