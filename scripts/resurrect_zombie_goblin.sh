#!/usr/bin/env bash
set -euo pipefail

ROOT="${ONE_WAVE_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [[ -z "$ROOT" || ! -d "$ROOT/.git" ]]; then
  echo "ZOMBIE_GOBLIN_HOLD no canonical checkout" >&2
  exit 2
fi
ROOT="$(cd "$ROOT" && pwd)"

SERVICE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
STATE_ROOT="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-zombie-goblin"
EXTERNAL_WORK_ROOT="${ONE_WAVE_EXTERNAL_WORK:-$HOME/One-Wave-External-Work}"
mkdir -p "$SERVICE_DIR" "$STATE_ROOT" "$EXTERNAL_WORK_ROOT"/{inbox,work,outbox}

cat >"$SERVICE_DIR/one-wave-zombie-goblin.service" <<EOF
[Unit]
Description=One-Wave Zombie Goblin bridge worker
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
WorkingDirectory=$ROOT
ExecStart=/usr/bin/python3 $ROOT/One_Wave_Bench/hive-pipe/chatgpt_terminal_pull.py --watch
Restart=always
RestartSec=3
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$ROOT $STATE_ROOT $EXTERNAL_WORK_ROOT
Environment=PYTHONUNBUFFERED=1
Environment=CHATGPT_TERMINAL_DEFAULT_CWD=$ROOT
Environment=CHATGPT_TERMINAL_ROUTES=primary=origin:chatgpt-terminal,backup=origin:chatgpt-terminal-backup
Environment=HIVE_PIPE_ALLOWED_ROOTS=$ROOT:$EXTERNAL_WORK_ROOT
Environment=ONE_WAVE_PROJECT_ROOT=$ROOT
Environment=XDG_STATE_HOME=${XDG_STATE_HOME:-$HOME/.local/state}
Environment=REFERENCE_GATE_LEDGER=$STATE_ROOT/reference-receipts.jsonl

[Install]
WantedBy=default.target
EOF

cat >"$SERVICE_DIR/one-wave-zombie-goblin-watchdog.service" <<EOF
[Unit]
Description=One-Wave Zombie Goblin watchdog
After=network-online.target

[Service]
Type=oneshot
ExecStart=/bin/bash $ROOT/scripts/zombie_goblin_watchdog.sh
EOF

cat >"$SERVICE_DIR/one-wave-zombie-goblin-watchdog.timer" <<EOF
[Unit]
Description=Run One-Wave Zombie Goblin watchdog

[Timer]
OnBootSec=30s
OnUnitActiveSec=60s
Persistent=true
Unit=one-wave-zombie-goblin-watchdog.service

[Install]
WantedBy=timers.target
EOF

# Bury the old pull worker if it exists; replacement uses a distinct unit/state lane.
systemctl --user disable --now one-wave-chatgpt-terminal-pull.service 2>/dev/null || true
systemctl --user daemon-reload
systemctl --user enable --now one-wave-zombie-goblin.service
systemctl --user enable --now one-wave-zombie-goblin-watchdog.timer

echo "ZOMBIE_GOBLIN_RESURRECTED"
systemctl --user --no-pager --plain is-active one-wave-zombie-goblin.service
systemctl --user --no-pager --plain is-active one-wave-zombie-goblin-watchdog.timer
