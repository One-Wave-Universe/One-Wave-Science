#!/usr/bin/env bash
set -euo pipefail
ROOM_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
STATE_DIR="$HOME/.local/share/one-wave/miniverse-room"
SYSTEMD_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
AUTOSTART_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/autostart"
SERVICE="$SYSTEMD_DIR/miniverse-room.service"
mkdir -p "$STATE_DIR" "$SYSTEMD_DIR" "$AUTOSTART_DIR"
if [[ ! -f "$ROOM_DIR/node_modules/three/build/three.module.js" ]]; then
  command -v npm >/dev/null 2>&1 || {
    echo "MINIVERSE_ROOM_INSTALL_ERROR: npm is required for the one-time Three.js install" >&2
    exit 2
  }
  (cd "$ROOM_DIR" && npm ci --omit=dev)
fi
cat > "$SERVICE" <<EOF
[Unit]
Description=One-Wave Miniverse 3D Sandbox Room
After=network.target
[Service]
Type=simple
WorkingDirectory=$ROOM_DIR
Environment=MINIVERSE_ROOM_STATE=$STATE_DIR/state.json
ExecStart=/usr/bin/python3 $ROOM_DIR/server.py --host 127.0.0.1 --port 8787
Restart=on-failure
RestartSec=2
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=$STATE_DIR
[Install]
WantedBy=default.target
EOF
cat > "$AUTOSTART_DIR/miniverse-room.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=One-Wave Miniverse Room
Comment=Open the local shared AI sandbox room
Exec=/bin/sh -c 'sleep 3; $ROOM_DIR/launch_visible.sh'
Terminal=false
X-GNOME-Autostart-enabled=true
EOF
systemctl --user daemon-reload
systemctl --user enable --now miniverse-room.service
echo "MINIVERSE_ROOM_SERVICE=$(systemctl --user is-active miniverse-room.service)"
echo "OPEN=http://127.0.0.1:8787/"
