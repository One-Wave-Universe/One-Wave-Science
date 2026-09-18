#!/usr/bin/env bash
set -euo pipefail
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
DEST="$HOME/.local/share/one-wave-miniverse"
APPS="$HOME/.local/share/applications"
DESKTOP="${XDG_DESKTOP_DIR:-$(xdg-user-dir DESKTOP 2>/dev/null || printf '%s/Desktop' "$HOME")}"
CONFIG="$HOME/.config/one-wave-miniverse"
KEY="$HOME/.ssh/one_wave_miniverse_ed25519"

python3 - <<'PY'
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.1")
from gi.repository import Gtk, WebKit2
print("GTK_WEBKIT_OK")
PY

mkdir -p "$DEST" "$APPS" "$DESKTOP" "$CONFIG"
install -m 755 "$HERE/miniverse_desktop.py" "$DEST/miniverse_desktop.py"
install -m 644 "$HERE/miniverse.svg" "$DEST/miniverse.svg"

if [[ ! -f "$CONFIG/desktop.json" ]]; then
  cat > "$CONFIG/desktop.json" <<EOF
{
  "remote_user": "Scales",
  "host_candidates": ["192.168.55.1", "192.168.4.45"],
  "ssh_key": "~/.ssh/one_wave_miniverse_ed25519",
  "local_port": 18787,
  "remote_port": 8787
}
EOF
fi

if [[ ! -f "$KEY" ]]; then
  echo "MINIVERSE_SSH_KEY_MISSING=$KEY" >&2
  echo "Create and authorize the dedicated laptop key before launching the app." >&2
fi

ENTRY="$APPS/one-wave-miniverse.desktop"
cat > "$ENTRY" <<EOF
[Desktop Entry]
Type=Application
Name=One-Wave Miniverse
Comment=Open the shared Jetson AI sandbox world
Exec=/usr/bin/python3 $DEST/miniverse_desktop.py
Icon=$DEST/miniverse.svg
Terminal=false
Categories=Development;Game;
StartupNotify=true
StartupWMClass=org.onewave.Miniverse
EOF

chmod 755 "$ENTRY"
cp "$ENTRY" "$DESKTOP/One-Wave-Miniverse.desktop"
chmod 755 "$DESKTOP/One-Wave-Miniverse.desktop"
gio set "$DESKTOP/One-Wave-Miniverse.desktop" metadata::trusted true 2>/dev/null || true
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APPS" || true

echo "MINIVERSE_DESKTOP_APP=$DEST/miniverse_desktop.py"
echo "MINIVERSE_DESKTOP_SHORTCUT=$DESKTOP/One-Wave-Miniverse.desktop"
