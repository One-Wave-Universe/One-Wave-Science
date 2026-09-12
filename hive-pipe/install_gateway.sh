#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/hive-pipe"
TOKEN_DIR="$CONFIG_DIR/tokens"
SYSTEMD_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICE_FILE="$SYSTEMD_DIR/hive-pipe.service"

mkdir -p "$TOKEN_DIR" "$SYSTEMD_DIR"
chmod 700 "$CONFIG_DIR" "$TOKEN_DIR"

for agent in codex claude gemini; do
  token_file="$TOKEN_DIR/$agent.token"
  if [[ ! -e "$token_file" ]]; then
    umask 077
    python3 -c 'import secrets; print(secrets.token_urlsafe(32))' > "$token_file"
  fi
  chmod 600 "$token_file"
done

escaped_root="$(printf '%s' "$SCRIPT_DIR" | sed 's/ /\\x20/g')"
{
  echo '[Unit]'
  echo 'Description=One-Wave Hive Pipe Agent Gateway'
  echo 'After=network.target'
  echo
  echo '[Service]'
  echo 'Type=simple'
  echo "WorkingDirectory=$escaped_root"
  echo "Environment=HIVE_PIPE_TOKEN_DIR=$TOKEN_DIR"
  echo "ExecStart=/usr/bin/python3 $escaped_root/gateway.py --host 127.0.0.1 --port 8765"
  echo 'Restart=on-failure'
  echo 'RestartSec=3'
  echo 'NoNewPrivileges=true'
  echo 'PrivateTmp=true'
  echo 'ProtectSystem=strict'
  echo "ReadWritePaths=$escaped_root/queue"
  echo
  echo '[Install]'
  echo 'WantedBy=default.target'
} > "$SERVICE_FILE"

systemctl --user daemon-reload
systemctl --user enable --now hive-pipe.service
echo "HIVE_PIPE_GATEWAY_INSTALLED"
echo "Local endpoint: http://127.0.0.1:8765"
echo "Tokens: $TOKEN_DIR (0600; never commit or paste them into the public repository)"

