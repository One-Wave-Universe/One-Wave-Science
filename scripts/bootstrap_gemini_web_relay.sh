#!/usr/bin/env bash
set -euo pipefail
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}"
STATE="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-gemini-web"
VENV="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-deepseek-web/venv"
PROFILE="$STATE/firefox-profile"
RELAY="$STATE/gemini_web_relay.py"
SERVICE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICE="$SERVICE_DIR/one-wave-gemini-web-relay.service"
RAW_URL="${GEMINI_RELAY_SOURCE_URL:-https://raw.githubusercontent.com/One-Wave-Universe/One-Wave-Science/main/One_Wave_Bench/hive-pipe/gemini_web_relay.py}"
mkdir -p "$STATE" "$SERVICE_DIR"
chmod 700 "$STATE"
[[ -x "$VENV/bin/python" ]] || { echo "Selenium runtime missing; bootstrap DeepSeek relay first."; exit 2; }
if [[ ! -d "$PROFILE" ]]; then
  SOURCE_PROFILE="$HOME/snap/firefox/common/.mozilla/firefox/yy4d2pf9.default"
  [[ -d "$SOURCE_PROFILE" ]] || { echo "Firefox profile missing: $SOURCE_PROFILE"; exit 2; }
  rsync -a --exclude=lock --exclude=.parentlock --exclude=parent.lock "$SOURCE_PROFILE/" "$PROFILE/"
  chmod -R go-rwx "$PROFILE"
fi
python3 - "$RAW_URL" "$RELAY" <<PY
from pathlib import Path
import sys
from urllib.request import urlopen
url,dest=sys.argv[1],Path(sys.argv[2])
dest.write_bytes(urlopen(url,timeout=30).read())
PY
chmod 600 "$RELAY"
cat >"$SERVICE" <<EOF
[Unit]
Description=One-Wave Gemini free web Brain Buddy relay
After=network-online.target
Wants=network-online.target
[Service]
Type=simple
ExecStart=$VENV/bin/python $RELAY --bind 192.168.55.100 --port 3001 --profile $PROFILE
Restart=always
RestartSec=5
Environment=GEMINI_WEB_RELAY_ALLOWED_CLIENTS=127.0.0.1,192.168.55.1
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$STATE
[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now one-wave-gemini-web-relay.service
