#!/usr/bin/env bash
set -euo pipefail

ROOT="${ONE_WAVE_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [[ -z "$ROOT" || ! -d "$ROOT/.git" ]]; then
  echo "GOBLIN_HOLD no canonical One-Wave-Science checkout found" >&2
  exit 2
fi
ROOT="$(cd "$ROOT" && pwd)"

export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}"

echo "GOBLIN_REFERENCE=$ROOT"
test -f "$ROOT/AI_CANONICAL_START_HERE.md"
test -f "$ROOT/Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md"
test -x "$ROOT/scripts/gemini_min.sh" || test -f "$ROOT/scripts/gemini_min.sh"

echo "GOBLIN_PHASE=repair-services"
systemctl --user daemon-reload

if systemctl --user list-unit-files | grep -q '^one-wave-chatgpt-terminal-pull.service'; then
  systemctl --user enable --now one-wave-chatgpt-terminal-pull.service
fi
for unit in hive-pipe-agent.service hive-pipe-gateway.service; do
  if systemctl --user list-unit-files | grep -q "^$unit"; then
    systemctl --user restart "$unit"
  fi
done

echo "GOBLIN_PHASE=gemini-reference"
mkdir -p "$HOME/.gemini"
python3 - <<'PY'
import json, os
p=os.path.expanduser("~/.gemini/settings.json")
try:
    data=json.load(open(p)) if os.path.exists(p) else {}
except Exception:
    data={}
data.setdefault("security",{}).setdefault("auth",{})["selectedType"]="oauth-personal"
with open(p,"w",encoding="utf-8") as f:
    json.dump(data,f,indent=2)
    f.write("\n")
os.chmod(p,0o600)
print("GEMINI_AUTH_SELECTED=oauth-personal")
PY

echo "GOBLIN_PHASE=verify"
python3 "$ROOT/One_Wave_Bench/hive-pipe/bridge_doctor.py" --profile all || doctor_rc=$?
doctor_rc="${doctor_rc:-0}"

echo "GOBLIN_PHASE=service-status"
systemctl --user --no-pager --plain is-active   one-wave-chatgpt-terminal-pull.service   hive-pipe-agent.service   hive-pipe-gateway.service 2>/dev/null || true

if [[ "$doctor_rc" -eq 0 || "$doctor_rc" -eq 2 ]]; then
  echo "GOBLIN_BRIDGE_FIXER_COMPLETE"
  exit "$doctor_rc"
fi

echo "GOBLIN_HOLD bridge doctor still reports a required failure" >&2
exit "$doctor_rc"
