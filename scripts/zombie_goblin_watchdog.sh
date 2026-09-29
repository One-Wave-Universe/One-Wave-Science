#!/usr/bin/env bash
set -euo pipefail

ROOT="${ONE_WAVE_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
[[ -n "$ROOT" && -d "$ROOT/.git" ]] || exit 2
ROOT="$(cd "$ROOT" && pwd)"

export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}"

repair_unit() {
  local unit="$1"
  if systemctl --user list-unit-files | grep -q "^$unit"; then
    if ! systemctl --user is-active --quiet "$unit"; then
      systemctl --user restart "$unit" || true
    fi
  fi
}

repair_unit one-wave-zombie-goblin.service
repair_unit hive-pipe-agent.service
repair_unit hive-pipe-gateway.service

# Verify canonical reference + metadata remain present before trusting the worker.
test -f "$ROOT/AI_CANONICAL_START_HERE.md"
test -f "$ROOT/Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md"

# Keep transport refs fresh without touching the active branch.
git -C "$ROOT" fetch --quiet origin chatgpt-terminal chatgpt-terminal-backup main || true

# Record a compact local heartbeat for diagnosis.
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-zombie-goblin"
mkdir -p "$STATE_DIR"
{
  date -Is
  systemctl --user is-active one-wave-zombie-goblin.service 2>/dev/null || true
  systemctl --user is-active hive-pipe-agent.service 2>/dev/null || true
  systemctl --user is-active hive-pipe-gateway.service 2>/dev/null || true
} > "$STATE_DIR/heartbeat.txt"

exit 0
