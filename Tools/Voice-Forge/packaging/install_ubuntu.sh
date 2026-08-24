#!/usr/bin/env bash
# Installs the already-built Voice Forge app (see build_ubuntu.sh) into
# the current user's account: no sudo, no system-wide changes.
#
#   ~/.local/share/voiceforge/         the app itself
#   ~/.local/share/icons/voiceforge.png
#   ~/.local/share/applications/voiceforge.desktop   (Applications menu entry)
#   ~/Desktop/One-Wave Voice Forge.desktop           (desktop icon)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILT_DIR="$PROJECT_ROOT/dist/VoiceForge"

if [ ! -x "$BUILT_DIR/VoiceForge" ]; then
  echo "No build found at $BUILT_DIR/VoiceForge" >&2
  echo "Run packaging/build_ubuntu.sh first." >&2
  exit 1
fi

INSTALL_DIR="$HOME/.local/share/voiceforge"
ICON_DIR="$HOME/.local/share/icons"
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$ICON_DIR" "$APPS_DIR"

echo "== Installing app to $INSTALL_DIR =="
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp -r "$BUILT_DIR/." "$INSTALL_DIR/"

cp "$PROJECT_ROOT/assets/icon.png" "$ICON_DIR/voiceforge.png"

make_desktop_entry() {
  local out_file="$1"
  cat > "$out_file" <<EOF
[Desktop Entry]
Type=Application
Name=One-Wave Voice Forge
Comment=Blend two or more reference voices into a reusable character voice
Exec=$INSTALL_DIR/VoiceForge
Icon=$ICON_DIR/voiceforge.png
Terminal=false
Categories=AudioVideo;Audio;
EOF
  chmod +x "$out_file"
  # GNOME/Nautilus refuses to run a desktop file it doesn't consider
  # "trusted" (shows a warning dialog instead of launching). Marking it
  # here means the icon just works instead of needing a manual
  # right-click -> "Allow Launching" the first time.
  if command -v gio >/dev/null 2>&1; then
    gio set "$out_file" "metadata::trusted" true >/dev/null 2>&1 || true
  fi
}

echo "== Adding Applications menu entry =="
make_desktop_entry "$APPS_DIR/voiceforge.desktop"
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true
fi

DESKTOP_DIR="$HOME/Desktop"
if command -v xdg-user-dir >/dev/null 2>&1; then
  XDG_DESKTOP="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
  [ -n "$XDG_DESKTOP" ] && DESKTOP_DIR="$XDG_DESKTOP"
fi

if [ -d "$DESKTOP_DIR" ] || mkdir -p "$DESKTOP_DIR" 2>/dev/null; then
  echo "== Adding desktop shortcut in $DESKTOP_DIR =="
  make_desktop_entry "$DESKTOP_DIR/One-Wave Voice Forge.desktop"
else
  echo "No Desktop folder found (skipping desktop shortcut); the Applications menu entry above still works."
fi

echo
echo "Installed. Look for \"One-Wave Voice Forge\" on your Desktop or in"
echo "your Applications menu, or run it directly with:"
echo "  $INSTALL_DIR/VoiceForge"
