#!/usr/bin/env bash
# Removes what install.sh installed for the current user.
set -euo pipefail

rm -rf "$HOME/.local/share/voiceforge"
rm -f "$HOME/.local/share/icons/voiceforge.png"
rm -f "$HOME/.local/share/applications/voiceforge.desktop"

DESKTOP_DIR="$HOME/Desktop"
if command -v xdg-user-dir >/dev/null 2>&1; then
  XDG_DESKTOP="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
  [ -n "$XDG_DESKTOP" ] && DESKTOP_DIR="$XDG_DESKTOP"
fi
rm -f "$DESKTOP_DIR/One-Wave Voice Forge.desktop"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$HOME/.local/share/applications" >/dev/null 2>&1 || true
fi

echo "Voice Forge uninstalled."
