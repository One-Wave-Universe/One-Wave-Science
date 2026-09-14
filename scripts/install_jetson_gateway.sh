#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "ERROR: run from inside the One-Wave-Science checkout" >&2
  exit 1
}
cd "$ROOT"

CANONICAL="$ROOT/hive-pipe/install_gateway.sh"
[[ -f "$CANONICAL" ]] || {
  echo "ERROR: missing canonical Hive Pipe installer: $CANONICAL" >&2
  exit 1
}

# Compatibility migration: PR #84 used ~/.config/hive-pipe/gateway.token.
# Hive Pipe v3 uses per-client tokens. Preserve the old token as the Codex token
# when possible so an existing GitHub/remote client does not suddenly lose access.
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/hive-pipe"
OLD_TOKEN="$CONFIG_DIR/gateway.token"
CODEX_TOKEN="$CONFIG_DIR/tokens/codex.token"
if [[ -s "$OLD_TOKEN" && ! -e "$CODEX_TOKEN" ]]; then
  mkdir -p "$(dirname -- "$CODEX_TOKEN")"
  chmod 700 "$CONFIG_DIR" "$(dirname -- "$CODEX_TOKEN")"
  cp "$OLD_TOKEN" "$CODEX_TOKEN"
  chmod 600 "$CODEX_TOKEN"
  echo "Migrated existing gateway token to $CODEX_TOKEN"
fi

echo "scripts/install_jetson_gateway.sh is now a compatibility entrypoint."
echo "Canonical gateway: hive-pipe/install_gateway.sh (MCP terminal parser)."
exec bash "$CANONICAL"
