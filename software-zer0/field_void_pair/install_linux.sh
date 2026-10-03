#!/usr/bin/env bash
# Install fvpair for the current user:
#   ~/.local/bin/fvpair                          terminal program
#   ~/.local/share/applications/fvpair.desktop   app-menu entry (opens the app version)
# Uninstall: ./install_linux.sh --uninstall
set -euo pipefail
HERE="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
BIN="$HOME/.local/bin"
APPS="${XDG_DATA_HOME:-$HOME/.local/share}/applications"

if [[ "${1:-}" == "--uninstall" ]]; then
  rm -f "$BIN/fvpair" "$APPS/fvpair.desktop"
  echo "removed fvpair"
  exit 0
fi

command -v python3 >/dev/null || { echo "python3 is required" >&2; exit 1; }
mkdir -p "$BIN" "$APPS"
ln -sf "$HERE/fvpair" "$BIN/fvpair"
cat > "$APPS/fvpair.desktop" <<DESK
[Desktop Entry]
Type=Application
Name=Field/Void Pair
Comment=Two AIs in a Field/Void loop through the One-Wave repo lens (Algorythm-Zer0 referee)
Exec=$HERE/fvpair serve
Terminal=true
Categories=Development;Science;
DESK
command -v update-desktop-database >/dev/null && update-desktop-database "$APPS" 2>/dev/null || true
echo "installed: $BIN/fvpair and $APPS/fvpair.desktop"
case ":$PATH:" in *":$BIN:"*) ;; *) echo "add $BIN to PATH to run 'fvpair' directly";; esac
echo "API keys are read from the environment: ANTHROPIC_API_KEY, DEEPSEEK_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY"
