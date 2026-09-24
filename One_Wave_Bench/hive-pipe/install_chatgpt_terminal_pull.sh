#!/usr/bin/env bash
set -euo pipefail

# Install the resilient ChatGPT pull bridge against the user's ONE real
# One-Wave-Science checkout. The bridge may fetch transport refs and create
# temporary detached worktrees, but it never switches, merges, rebases, resets,
# or duplicates the active checkout.
SOURCE_REPO="${ONE_WAVE_PROJECT_ROOT:-}"
if [[ -z "$SOURCE_REPO" ]]; then
  SOURCE_REPO="$(git rev-parse --show-toplevel 2>/dev/null || true)"
fi
if [[ -z "$SOURCE_REPO" || ! -d "$SOURCE_REPO/.git" ]]; then
  echo "Run this from inside the One-Wave-Science checkout or set ONE_WAVE_PROJECT_ROOT." >&2
  exit 2
fi
SOURCE_REPO="$(cd "$SOURCE_REPO" && pwd)"

STATE_ROOT="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-chatgpt-terminal"
EXTERNAL_WORK_ROOT="${ONE_WAVE_EXTERNAL_WORK:-$HOME/One-Wave-External-Work}"
SERVICE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICE_PATH="$SERVICE_DIR/one-wave-chatgpt-terminal-pull.service"
BRIDGE_WORKTREE="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-chatgpt-terminal/bridge-worktree"

mkdir -p "$STATE_ROOT" "$SERVICE_DIR"
mkdir -p "$EXTERNAL_WORK_ROOT/inbox" "$EXTERNAL_WORK_ROOT/work" "$EXTERNAL_WORK_ROOT/outbox"

# One repository, one Git object/auth state. Fetch bridge refs into the real repo.
git -C "$SOURCE_REPO" fetch --prune origin main fix/no-runtime-clone chatgpt-terminal chatgpt-terminal-backup

# Use a linked Git worktree, not a clone. This shares the same .git object store,
# remotes, credentials, refs, and branch history as SOURCE_REPO.
if [[ -e "$BRIDGE_WORKTREE" ]]; then
  git -C "$SOURCE_REPO" worktree remove --force "$BRIDGE_WORKTREE" 2>/dev/null || rm -rf -- "$BRIDGE_WORKTREE"
fi
git -C "$SOURCE_REPO" worktree add --detach "$BRIDGE_WORKTREE" origin/fix/no-runtime-clone

cat >"$SERVICE_PATH" <<EOF
[Unit]
Description=One-Wave resilient ChatGPT terminal bridge
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
WorkingDirectory=$BRIDGE_WORKTREE
ExecStart=/usr/bin/python3 $BRIDGE_WORKTREE/One_Wave_Bench/hive-pipe/chatgpt_terminal_pull.py --watch
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$SOURCE_REPO $BRIDGE_WORKTREE $STATE_ROOT $EXTERNAL_WORK_ROOT
Environment=PYTHONUNBUFFERED=1
Environment=CHATGPT_TERMINAL_DEFAULT_CWD=$SOURCE_REPO
Environment=CHATGPT_TERMINAL_ROUTES=primary=origin:chatgpt-terminal,backup=origin:chatgpt-terminal-backup
Environment=HIVE_PIPE_ALLOWED_ROOTS=$SOURCE_REPO:$EXTERNAL_WORK_ROOT
Environment=ONE_WAVE_PROJECT_ROOT=$SOURCE_REPO
Environment=CHATGPT_TERMINAL_REPO=$SOURCE_REPO
Environment=REFERENCE_GATE_LEDGER=$STATE_ROOT/reference-receipts.jsonl

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now one-wave-chatgpt-terminal-pull.service

# The old permanent runtime clone created a second Git/auth state. Once the
# service is confirmed active from the real checkout, remove only that exact
# deprecated directory. Bridge state remains under XDG_STATE_HOME.
OLD_RUNTIME="${XDG_DATA_HOME:-$HOME/.local/share}/one-wave-chatgpt-terminal-runtime"
if systemctl --user is-active --quiet one-wave-chatgpt-terminal-pull.service; then
  if [[ "$OLD_RUNTIME" == "$HOME/.local/share/one-wave-chatgpt-terminal-runtime" && -d "$OLD_RUNTIME" ]]; then
    rm -rf -- "$OLD_RUNTIME"
    printf 'REMOVED_DEPRECATED_RUNTIME_CLONE=%s\n' "$OLD_RUNTIME"
  fi
fi

printf 'CHATGPT_TERMINAL_PULL_INSTALLED\n'
printf 'project=%s\n' "$SOURCE_REPO"
printf 'transport_repo=%s\n' "$SOURCE_REPO"
printf 'bridge_worktree=%s\n' "$BRIDGE_WORKTREE"
printf 'runtime_clone=NOT_USED\n'
printf 'routes=origin:chatgpt-terminal,origin:chatgpt-terminal-backup\n'
systemctl --user is-active one-wave-chatgpt-terminal-pull.service

for attempt in 1 2 3 4 5; do
  if ONE_WAVE_PROJECT_ROOT="$SOURCE_REPO" CHATGPT_TERMINAL_REPO="$SOURCE_REPO" \
     python3 "$BRIDGE_WORKTREE/One_Wave_Bench/hive-pipe/bridge_doctor.py" --profile pull; then
    printf 'CHATGPT_TERMINAL_PULL_HEALTHY\n'
    exit 0
  fi
  sleep 2
done

echo "Bridge service started but did not pass its live pull profile." >&2
echo "Inspect: journalctl --user -u one-wave-chatgpt-terminal-pull.service -n 100 --no-pager" >&2
exit 1
