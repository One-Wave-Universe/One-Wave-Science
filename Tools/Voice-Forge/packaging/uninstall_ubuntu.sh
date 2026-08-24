#!/usr/bin/env bash
# Removes what install_ubuntu.sh installed for the current user.
set -euo pipefail

rm -rf "$HOME/.local/share/voiceforge"
rm -f "$HOME/.local/share/icons/voiceforge.png"
rm -f "$HOME/.local/share/applications/voiceforge.desktop"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$HOME/.local/share/applications" >/dev/null 2>&1 || true
fi

echo "Voice Forge uninstalled."
