#!/usr/bin/env bash
# Install a user desktop icon. Does not publish to Flathub.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
APPDIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$APPDIR"
sed -e "s|REPLACE_ME|$HERE|g" -e "s|%k/|$HERE/|" \
  "$HERE/one-wave-manipulator.desktop" > "$APPDIR/one-wave-manipulator.desktop"
chmod +x "$HERE/wave_app.py" "$APPDIR/one-wave-manipulator.desktop"
echo "Icon installed: $APPDIR/one-wave-manipulator.desktop"
echo "Flathub listing is not this script."
