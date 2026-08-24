#!/usr/bin/env bash
# Installer bundled inside the downloadable VoiceForge-Ubuntu release
# archive. Pure bash -- no Python, pip, or build tools needed on this
# machine, because the app binary is already built and sitting right
# next to this script. Installs for the current user only: no sudo,
# no system-wide changes.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_SRC="$SCRIPT_DIR/VoiceForge"

if [ ! -x "$APP_SRC/VoiceForge" ]; then
  echo "Couldn't find VoiceForge/VoiceForge next to this script -- is the archive intact?" >&2
  exit 1
fi

INSTALL_DIR="$HOME/.local/share/voiceforge"
ICON_DIR="$HOME/.local/share/icons"
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$ICON_DIR" "$APPS_DIR"

echo "== Installing app to $INSTALL_DIR =="
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp -r "$APP_SRC/." "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/VoiceForge"

cp "$SCRIPT_DIR/icon.png" "$ICON_DIR/voiceforge.png"

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
echo "Checking runtime libraries..."
MISSING_PKGS=()
for pkg in libegl1 libgl1 libxkbcommon0 libpulse0; do
  if command -v dpkg >/dev/null 2>&1 && ! dpkg -s "$pkg" >/dev/null 2>&1; then
    MISSING_PKGS+=("$pkg")
  fi
done
if [ "${#MISSING_PKGS[@]}" -gt 0 ]; then
  echo "Missing packages: ${MISSING_PKGS[*]}"
  echo "If the app doesn't launch, install them with:"
  echo "  sudo apt-get install ${MISSING_PKGS[*]}"
fi

echo
echo "Installed. Look for \"One-Wave Voice Forge\" on your Desktop or in"
echo "your Applications menu, or run it directly with:"
echo "  $INSTALL_DIR/VoiceForge"
