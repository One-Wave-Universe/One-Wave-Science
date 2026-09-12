#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(dirname -- "$SCRIPT_DIR")"
EXTERNAL_WORK_ROOT="${ONE_WAVE_EXTERNAL_WORK:-$HOME/One-Wave-External-Work}"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/hive-pipe"
TOKEN_DIR="$CONFIG_DIR/tokens"
SYSTEMD_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
GATEWAY_SERVICE="$SYSTEMD_DIR/hive-pipe-gateway.service"
AGENT_SERVICE="$SYSTEMD_DIR/hive-pipe-agent.service"

mkdir -p "$TOKEN_DIR" "$SYSTEMD_DIR"
mkdir -p "$EXTERNAL_WORK_ROOT/inbox" "$EXTERNAL_WORK_ROOT/work" "$EXTERNAL_WORK_ROOT/outbox"
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
escaped_repo="$(printf '%s' "$REPO_ROOT" | sed 's/ /\\x20/g')"
escaped_external="$(printf '%s' "$EXTERNAL_WORK_ROOT" | sed 's/ /\\x20/g')"
{
  echo '[Unit]'
  echo 'Description=One-Wave Hive Pipe Agent Gateway'
  echo 'After=network.target'
  echo
  echo '[Service]'
  echo 'Type=simple'
  echo "WorkingDirectory=$escaped_root"
  echo "Environment=HIVE_PIPE_TOKEN_DIR=$TOKEN_DIR"
  echo "Environment=ONE_WAVE_EXTERNAL_WORK=$escaped_external"
  echo "ExecStart=/usr/bin/python3 $escaped_root/gateway.py --host 127.0.0.1 --port 8765"
  echo 'Restart=on-failure'
  echo 'RestartSec=3'
  echo 'NoNewPrivileges=true'
  echo 'PrivateTmp=true'
  echo 'ProtectSystem=strict'
  # AI may build/edit the checkout and explicit external-work workspace. System
  # paths remain read-only and privilege escalation remains blocked.
  echo "ReadWritePaths=$escaped_repo $escaped_external"
  echo
  echo '[Install]'
  echo 'WantedBy=default.target'
} > "$GATEWAY_SERVICE"

{
  echo '[Unit]'
  echo 'Description=One-Wave Hive Pipe Queue Worker'
  echo 'After=network.target'
  echo
  echo '[Service]'
  echo 'Type=simple'
  echo "WorkingDirectory=$escaped_root"
  echo "ExecStart=/usr/bin/bash $escaped_root/agent.sh --watch"
  echo 'Restart=on-failure'
  echo 'RestartSec=3'
  echo 'NoNewPrivileges=true'
  echo 'PrivateTmp=true'
  echo 'ProtectSystem=strict'
  echo "ReadWritePaths=$escaped_root/queue"
  echo
  echo '[Install]'
  echo 'WantedBy=default.target'
} > "$AGENT_SERVICE"

systemctl --user daemon-reload
systemctl --user disable --now hive-pipe.service 2>/dev/null || true
systemctl --user enable --now hive-pipe-agent.service hive-pipe-gateway.service
systemctl --user restart hive-pipe-agent.service hive-pipe-gateway.service
echo "HIVE_PIPE_GATEWAY_INSTALLED"
echo "Local endpoint: http://127.0.0.1:8765"
echo "AI terminal: terminal_pwd / terminal_which / terminal_run via MCP"
echo "Writable repo: $REPO_ROOT"
echo "Writable external work: $EXTERNAL_WORK_ROOT"
echo "Tokens: $TOKEN_DIR (0600; never commit or paste them into the public repository)"
