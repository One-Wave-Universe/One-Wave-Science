#!/usr/bin/env bash
set -euo pipefail

echo "DESKTOP_COMMANDER_REPAIR_START"

if pgrep -af -i 'desktop[ _-]*commander|remote.*commander' >/tmp/dc-procs.$$ 2>/dev/null; then
  echo "DESKTOP_COMMANDER_PROCESS_FOUND"
  cat /tmp/dc-procs.$$
  rm -f /tmp/dc-procs.$$
  exit 0
fi
rm -f /tmp/dc-procs.$$ 2>/dev/null || true

mapfile -t units < <(
  systemctl --user list-unit-files --type=service --no-legend 2>/dev/null |
  awk '{print $1}' |
  grep -Ei 'desktop.*commander|commander.*desktop|remote.*commander' || true
)

if ((${#units[@]})); then
  echo "DESKTOP_COMMANDER_USER_SERVICES=${units[*]}"
  for unit in "${units[@]}"; do
    echo "STARTING_EXISTING_SERVICE=$unit"
    systemctl --user enable --now "$unit" || systemctl --user restart "$unit" || true
    if systemctl --user is-active --quiet "$unit"; then
      echo "DESKTOP_COMMANDER_ACTIVE_SERVICE=$unit"
      exit 0
    fi
  done
fi

echo "DESKTOP_COMMANDER_EXISTING_INSTALLATIONS"
for cmd in desktop-commander desktopcommander desktop-commander-remote; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "COMMAND=$cmd PATH=$(command -v "$cmd")"
  fi
done

find "$HOME/.local/share/applications" "$HOME/.config/systemd/user" "$HOME/.local/bin" \
  -maxdepth 2 -type f \( -iname '*desktop*commander*' -o -iname '*commander*desktop*' \) \
  -print 2>/dev/null || true

echo "DESKTOP_COMMANDER_AGENT_OFFLINE"
echo "No existing running process or startable user service was found."
echo "Do not create a second registration. Inspect the existing installation/launcher shown above."
exit 2
