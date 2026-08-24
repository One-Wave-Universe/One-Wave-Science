#!/usr/bin/env bash
# Installs the already-built Voice Forge app (see build_ubuntu.sh) into
# the current user's account: no sudo, no system-wide changes.
#
#   ~/.local/share/voiceforge/         the app itself
#   ~/.local/share/icons/voiceforge.png
#   ~/.local/share/applications/voiceforge.desktop   (Applications menu entry)
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

DESKTOP_FILE="$APPS_DIR/voiceforge.desktop"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=One-Wave Voice Forge
Comment=Blend two or more reference voices into a reusable character voice
Exec=$INSTALL_DIR/VoiceForge
Icon=$ICON_DIR/voiceforge.png
Terminal=false
Categories=AudioVideo;Audio;
EOF
chmod +x "$DESKTOP_FILE"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true
fi

echo
echo "Installed. Voice Forge should now appear in your Applications menu"
echo "as \"One-Wave Voice Forge\", or run it directly with:"
echo "  $INSTALL_DIR/VoiceForge"
