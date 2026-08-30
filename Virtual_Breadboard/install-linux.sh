#!/usr/bin/env bash
# Installs a desktop / app-menu shortcut for the Virtual Breadboard Simulator
# AppImage on Ubuntu (or any freedesktop.org-compliant desktop). No sudo
# needed - everything goes under the current user's home directory.
#
# Usage:
#   ./install-linux.sh /path/to/VirtualBreadboardSimulator.AppImage
#   ./install-linux.sh                 # auto-detects it next to this script
#                                       # or in ~/Downloads
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

APPIMAGE="${1:-}"
if [ -z "$APPIMAGE" ]; then
  for candidate in "$SCRIPT_DIR"/*.AppImage "$HOME/Downloads"/*Breadboard*.AppImage; do
    if [ -f "$candidate" ]; then APPIMAGE="$candidate"; break; fi
  done
fi
if [ -z "$APPIMAGE" ] || [ ! -f "$APPIMAGE" ]; then
  echo "Could not find the AppImage automatically." >&2
  echo "Usage: $0 /path/to/VirtualBreadboardSimulator.AppImage" >&2
  exit 1
fi
APPIMAGE="$(readlink -f "$APPIMAGE")"
chmod +x "$APPIMAGE"

BIN_DIR="$HOME/.local/bin"
ICON_DIR="$HOME/.local/share/icons"
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$BIN_DIR" "$ICON_DIR" "$APPS_DIR"

TARGET_APP="$BIN_DIR/virtual-breadboard-simulator.AppImage"
cp -f "$APPIMAGE" "$TARGET_APP"
chmod +x "$TARGET_APP"

TARGET_ICON="$ICON_DIR/virtual-breadboard-simulator.svg"
cp -f "$SCRIPT_DIR/icon.svg" "$TARGET_ICON"

DESKTOP_FILE="$APPS_DIR/virtual-breadboard-simulator.desktop"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Virtual Breadboard Simulator
Comment=Click-any-hole breadboard simulator with real circuit physics
Exec=$TARGET_APP
Icon=$TARGET_ICON
Terminal=false
Categories=Education;
StartupNotify=true
EOF
chmod +x "$DESKTOP_FILE"

command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true
command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache "$ICON_DIR" >/dev/null 2>&1 || true

echo "Installed app: $TARGET_APP"
echo "App menu entry: $DESKTOP_FILE"
echo "-> Search for 'Virtual Breadboard Simulator' in your applications menu."

DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || echo "$HOME/Desktop")"
if [ -d "$DESKTOP_DIR" ]; then
  cp -f "$DESKTOP_FILE" "$DESKTOP_DIR/"
  chmod +x "$DESKTOP_DIR/$(basename "$DESKTOP_FILE")"
  # Nautilus/GNOME refuses to run a desktop file until it's marked trusted
  gio set "$DESKTOP_DIR/$(basename "$DESKTOP_FILE")" "metadata::trusted" true 2>/dev/null || true
  echo "Desktop icon: $DESKTOP_DIR/$(basename "$DESKTOP_FILE")"
  echo "(If it still shows as untrusted, right-click it -> Allow Launching.)"
fi
