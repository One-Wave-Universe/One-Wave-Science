#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  JETSON_GATEWAY_URL=https://... JETSON_GATEWAY_TOKEN=... \
    scripts/jetson_remote.sh --intention TEXT --consequence TEXT [--cwd PATH] [--timeout SECONDS] -- COMMAND ARG...

Examples:
  scripts/jetson_remote.sh --intention 'Inspect host' --consequence 'Read uname output' -- uname -a

The URL/token may also be placed in:
  ~/.config/hive-pipe/remote.env
with shell lines:
  export JETSON_GATEWAY_URL='https://...'
  export JETSON_GATEWAY_TOKEN='...'

Arguments are sent as a structured argv array to Hive Pipe MCP terminal_run.
No shell parsing, pipes, redirection, sudo, raw-disk formatting, or shell -c.
EOF
}

ENV_FILE="${XDG_CONFIG_HOME:-$HOME/.config}/hive-pipe/remote.env"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

CWD=""
TIMEOUT=120
INTENTION=""
CONSEQUENCE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --intention)
      INTENTION="${2:?--intention needs text}"
      shift 2
      ;;
    --consequence)
      CONSEQUENCE="${2:?--consequence needs text}"
      shift 2
      ;;
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
: "${INTENTION:?--intention is required}"
: "${CONSEQUENCE:?--consequence is required}"
: "${JETSON_GATEWAY_URL:?set JETSON_GATEWAY_URL}"
: "${JETSON_GATEWAY_TOKEN:?set JETSON_GATEWAY_TOKEN}"

python3 - "$JETSON_GATEWAY_URL" "$JETSON_GATEWAY_TOKEN" "$CWD" "$TIMEOUT" "$INTENTION" "$CONSEQUENCE" "$@" <<'PY'
import json
import sys
import urllib.error
import urllib.request

url, token, cwd, timeout, intention, consequence, *argv = sys.argv[1:]
arguments = {"argv": argv, "timeout": int(timeout), "intention": intention, "consequence": consequence}
if cwd:
    arguments["cwd"] = cwd
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {"name": "terminal_run", "arguments": arguments},
}

req = urllib.request.Request(
    url.rstrip("/") + "/mcp",
    data=json.dumps(payload).encode(),
    headers={
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
    },
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=int(timeout) + 15) as response:
        envelope = json.load(response)
except urllib.error.HTTPError as exc:
    print(exc.read().decode("utf-8", errors="replace"), file=sys.stderr)
    raise SystemExit(1)

if "error" in envelope:
    print(json.dumps(envelope["error"], indent=2), file=sys.stderr)
    raise SystemExit(1)
result = envelope.get("result", {}).get("structuredContent", {})
sys.stdout.write(result.get("stdout", ""))
sys.stderr.write(result.get("stderr", ""))
if result.get("error"):
    print(result["error"], file=sys.stderr)
raise SystemExit(int(result.get("exit_code", 0 if result.get("ok") else 1)))
PY
