#!/usr/bin/env bash
set -euo pipefail

REPO="${ONE_WAVE_REPO:-$HOME/One-Wave-Science-git}"
BRIDGE_DIR="$REPO/Tools/Local_Bridge"
USER_SYSTEMD="$HOME/.config/systemd/user"
mkdir -p "$USER_SYSTEMD"

if [[ ! -d "$REPO/.git" ]]; then
  echo "One-Wave repo not found at: $REPO" >&2
  exit 1
fi

# Bring in the bridge itself once, safely.
cd "$REPO"
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Repo has local changes. Commit/stash them before installing the bridge." >&2
  exit 1
fi

git fetch origin main
git merge --ff-only origin/main
chmod +x "$BRIDGE_DIR/one_wave_repo_sync.sh" "$BRIDGE_DIR/install_local_bridge.sh"

cat > "$USER_SYSTEMD/one-wave-local-bridge.service" <<EOF
[Unit]
Description=One-Wave safe GitHub-to-laptop sync

[Service]
Type=oneshot
Environment=ONE_WAVE_REPO=$REPO
ExecStart=$BRIDGE_DIR/one_wave_repo_sync.sh
EOF

cat > "$USER_SYSTEMD/one-wave-local-bridge.timer" <<'EOF'
[Unit]
Description=Check One-Wave GitHub for safe updates every minute

[Timer]
OnBootSec=20s
OnUnitActiveSec=60s
AccuracySec=10s
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now one-wave-local-bridge.timer
systemctl --user start one-wave-local-bridge.service

echo
echo "ONE-WAVE LOCAL BRIDGE INSTALLED"
echo "Repo: $REPO"
echo "Safe mode: fast-forward only; local changes are never overwritten."
echo "Checks GitHub once per minute."
echo "Log: ${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-local-bridge/sync.log"
echo
echo "After this, files I commit to One-Wave-Science/main can arrive on this laptop automatically."
