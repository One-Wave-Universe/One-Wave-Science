#!/usr/bin/env bash
set -euo pipefail

# This installer intentionally does not merge, reset, or modify the user's active
# One-Wave-Science checkout. It creates a private runtime clone for bridge code.
SOURCE_REPO="${ONE_WAVE_PROJECT_ROOT:-}"
if [[ -z "$SOURCE_REPO" ]]; then
  SOURCE_REPO="$(git rev-parse --show-toplevel 2>/dev/null || true)"
fi
if [[ -z "$SOURCE_REPO" || ! -d "$SOURCE_REPO/.git" ]]; then
  echo "Run this from inside the One-Wave-Science checkout or set ONE_WAVE_PROJECT_ROOT." >&2
  exit 2
fi
SOURCE_REPO="$(cd "$SOURCE_REPO" && pwd)"

REMOTE_URL="$(git -C "$SOURCE_REPO" remote get-url origin)"
RUNTIME_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/one-wave-chatgpt-terminal-runtime"
STATE_ROOT="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-chatgpt-terminal"
SERVICE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICE_PATH="$SERVICE_DIR/one-wave-chatgpt-terminal-pull.service"

mkdir -p "$(dirname "$RUNTIME_ROOT")" "$STATE_ROOT" "$SERVICE_DIR"

if [[ ! -d "$RUNTIME_ROOT/.git" ]]; then
  git clone --no-checkout "$REMOTE_URL" "$RUNTIME_ROOT"
fi

git -C "$RUNTIME_ROOT" remote set-url origin "$REMOTE_URL"
git -C "$RUNTIME_ROOT" fetch --prune origin main chatgpt-terminal
git -C "$RUNTIME_ROOT" checkout --detach origin/main
git -C "$RUNTIME_ROOT" reset --hard origin/main

cat >"$SERVICE_PATH" <<EOF
[Unit]
Description=One-Wave resilient ChatGPT terminal bridge
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
WorkingDirectory=$RUNTIME_ROOT
ExecStart=/usr/bin/python3 $RUNTIME_ROOT/hive-pipe/chatgpt_terminal_pull.py --watch
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$RUNTIME_ROOT $STATE_ROOT $SOURCE_REPO %h/One-Wave-External-Work
Environment=PYTHONUNBUFFERED=1
Environment=CHATGPT_TERMINAL_DEFAULT_CWD=$SOURCE_REPO
Environment=CHATGPT_TERMINAL_ROUTES=primary=origin:chatgpt-terminal,backup=origin:chatgpt-terminal-backup
Environment=HIVE_PIPE_ALLOWED_ROOTS=$SOURCE_REPO:%h/One-Wave-External-Work

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now one-wave-chatgpt-terminal-pull.service

printf 'CHATGPT_TERMINAL_PULL_INSTALLED\n'
printf 'project=%s\n' "$SOURCE_REPO"
printf 'runtime=%s\n' "$RUNTIME_ROOT"
printf 'routes=origin:chatgpt-terminal,origin:chatgpt-terminal-backup\n'
systemctl --user is-active one-wave-chatgpt-terminal-pull.service
