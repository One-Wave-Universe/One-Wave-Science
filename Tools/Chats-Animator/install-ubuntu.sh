#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/share/one-wave-animator"
APP_NAME="One-Wave Animator"
DESKTOP_FILE="one-wave-animator.desktop"
USER_APPS="$HOME/.local/share/applications"
DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
[[ -n "$DESKTOP_DIR" ]] || DESKTOP_DIR="$HOME/Desktop"

mkdir -p "$INSTALL_DIR" "$USER_APPS" "$DESKTOP_DIR"

# Replace the installed animator with this exact downloaded version.
# Keep the install in one stable location so future patches have one target.
find "$INSTALL_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
cp -a "$SOURCE_DIR"/. "$INSTALL_DIR"/
chmod +x "$INSTALL_DIR/launch-animator.sh"

write_desktop_file() {
  local target="$1"
  cat > "$target" <<EOF
[Desktop Entry]
Type=Application
Name=$APP_NAME
Comment=Frame-by-frame FPS animation and clip maker
Exec=$INSTALL_DIR/launch-animator.sh
Terminal=false
Categories=AudioVideo;Graphics;
StartupNotify=true
EOF
  chmod +x "$target"
}

write_desktop_file "$USER_APPS/$DESKTOP_FILE"
write_desktop_file "$DESKTOP_DIR/$DESKTOP_FILE"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$USER_APPS" >/dev/null 2>&1 || true
fi

printf '\nInstalled %s.\n' "$APP_NAME"
printf 'Installed app: %s\n' "$INSTALL_DIR"
printf 'Desktop shortcut: %s/%s\n' "$DESKTOP_DIR" "$DESKTOP_FILE"
printf 'Application menu shortcut: %s/%s\n' "$USER_APPS" "$DESKTOP_FILE"
printf '\nDouble-click the desktop icon or run:\n  %q\n\n' "$INSTALL_DIR/launch-animator.sh"
