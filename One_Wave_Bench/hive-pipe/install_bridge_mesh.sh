#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SYSTEMD_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-bridge-mesh"
SERVICE_PATH="$SYSTEMD_DIR/one-wave-bridge-mesh.service"

mkdir -p "$SYSTEMD_DIR" "$STATE_DIR"
chmod 700 "$STATE_DIR"

cat >"$SERVICE_PATH" <<EOF
[Unit]
Description=One-Wave self-repairing bridge mesh supervisor
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$SCRIPT_DIR
ExecStart=/usr/bin/python3 $SCRIPT_DIR/bridge_mesh.py --watch --interval 30
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$STATE_DIR

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now one-wave-bridge-mesh.service
systemctl --user restart one-wave-bridge-mesh.service

echo "ONE_WAVE_BRIDGE_MESH_INSTALLED"
echo "service=one-wave-bridge-mesh.service"
echo "receipts=$STATE_DIR/receipts.jsonl"
systemctl --user is-active one-wave-bridge-mesh.service
