#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "ERROR: run from inside the One-Wave-Science checkout" >&2
  exit 1
}
cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "ERROR: python3 is required" >&2
  exit 1
}
command -v systemctl >/dev/null 2>&1 || {
  echo "ERROR: systemd/systemctl is required" >&2
  exit 1
}
command -v curl >/dev/null 2>&1 || {
  echo "ERROR: curl is required" >&2
  exit 1
}

CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/hive-pipe"
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/hive-pipe"
UNIT_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
TOKEN_FILE="$CONFIG_DIR/gateway.token"
SERVICE_FILE="$UNIT_DIR/hive-pipe-gateway.service"

mkdir -p "$CONFIG_DIR" "$STATE_DIR" "$UNIT_DIR"
chmod 700 "$CONFIG_DIR"

if [[ ! -s "$TOKEN_FILE" ]]; then
  python3 - <<'PY' > "$TOKEN_FILE"
import secrets
print(secrets.token_urlsafe(48))
PY
  chmod 600 "$TOKEN_FILE"
  echo "Generated $TOKEN_FILE"
else
  chmod 600 "$TOKEN_FILE"
  echo "Keeping existing token at $TOKEN_FILE"
fi

if [[ -f "$SERVICE_FILE" ]]; then
  BACKUP="$SERVICE_FILE.bak.$(date +%Y%m%d-%H%M%S)"
  cp -a "$SERVICE_FILE" "$BACKUP"
  echo "Backed up existing unit to $BACKUP"
fi

PYTHON="$(command -v python3)"
GATEWAY="$ROOT/scripts/jetson_gateway.py"

cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=One-Wave Jetson AI command gateway
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$ROOT
ExecStart=$PYTHON $GATEWAY
Restart=on-failure
RestartSec=2
Environment=PYTHONUNBUFFERED=1
Environment=HIVE_GATEWAY_HOST=127.0.0.1
Environment=HIVE_GATEWAY_PORT=8765
NoNewPrivileges=yes
PrivateTmp=yes

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable hive-pipe-gateway.service >/dev/null
systemctl --user restart hive-pipe-gateway.service

for _ in $(seq 1 30); do
  if curl -fsS http://127.0.0.1:8765/healthz >/dev/null 2>&1; then
    break
  fi
  sleep 0.2
done

if ! curl -fsS http://127.0.0.1:8765/healthz; then
  echo >&2
  echo "ERROR: gateway did not become healthy" >&2
  systemctl --user --no-pager --full status hive-pipe-gateway.service >&2 || true
  exit 1
fi

echo
echo "Gateway installed and healthy."
echo "Bearer token stays OUTSIDE git:"
echo "  $TOKEN_FILE"
echo
echo "To print it only when you intentionally need to configure a client:"
echo "  cat '$TOKEN_FILE'"
echo
echo "Emergency stop:"
echo "  touch '$CONFIG_DIR/DISABLED'"
echo "Resume:"
echo "  rm -f '$CONFIG_DIR/DISABLED'"
