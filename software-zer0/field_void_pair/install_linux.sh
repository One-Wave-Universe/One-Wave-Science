#!/usr/bin/env bash
# Install Field/Void Pair for the current user (no sudo):
#   ~/.local/bin/fvpair, ~/.local/bin/fvpair-launch      terminal program + launcher
#   ~/Desktop/fvpair.desktop                            desktop icon
#   ~/.local/share/applications/fvpair.desktop          app-menu entry
#   ~/.config/fvpair/env                                repo path + API keys (chmod 600)
#
#   ./install_linux.sh [--repo /path/to/One-Wave-Science]
#   ./install_linux.sh --uninstall
set -euo pipefail
HERE="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
BIN="$HOME/.local/bin"
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"
APPS="$DATA/applications"
ICON="$DATA/icons/hicolor/scalable/apps/fvpair.svg"
CONF="${XDG_CONFIG_HOME:-$HOME/.config}/fvpair"
DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
[[ -n "$DESKTOP_DIR" && "$DESKTOP_DIR" != "$HOME" ]] || DESKTOP_DIR="$HOME/Desktop"
REPO_URL="https://github.com/one-wave-universe/one-wave-science.git"

is_repo() { [[ -f "$1/AGENTS.md" && -f "$1/simulations/zer0_first_cycle.py" ]]; }

REPO=""
case "${1:-}" in
  --uninstall)
    "$BIN/fvpair-launch" --stop >/dev/null 2>&1 || true
    rm -f "$BIN/fvpair" "$BIN/fvpair-launch" "$APPS/fvpair.desktop" "$DESKTOP_DIR/fvpair.desktop" "$ICON"
    echo "removed Field/Void Pair (kept $CONF/env with your keys; delete it by hand if wanted)"
    exit 0 ;;
  --repo) REPO="$(readlink -f "${2:?--repo needs a path}")" ;;
  "") ;;
  *) echo "usage: $0 [--repo PATH] | --uninstall" >&2; exit 2 ;;
esac

command -v python3 >/dev/null || { echo "python3 is required (sudo apt install python3)" >&2; exit 1; }

# 1. Find the One-Wave repo the lens will read.
if [[ -z "$REPO" ]]; then
  if is_repo "$HERE/../.."; then REPO="$(readlink -f "$HERE/../..")"
  elif [[ -f "$CONF/env" ]] && old="$(sed -n 's/^FVPAIR_REPO=//p' "$CONF/env" | tail -1)" && [[ -n "$old" ]] && is_repo "$old"; then REPO="$old"
  elif is_repo "$HOME/One-Wave-Science"; then REPO="$HOME/One-Wave-Science"
  elif command -v git >/dev/null; then
    echo "cloning the One-Wave repo into $HOME/One-Wave-Science ..."
    git clone --depth 1 "$REPO_URL" "$HOME/One-Wave-Science" && REPO="$HOME/One-Wave-Science"
  fi
fi
if [[ -z "$REPO" ]] || ! is_repo "$REPO"; then
  echo "One-Wave-Science repo not found. Clone it, then run: $0 --repo /path/to/One-Wave-Science" >&2
  exit 1
fi

# 2. Config: repo path + API key slots. Existing keys are kept.
mkdir -p "$CONF"
touch "$CONF/env"; chmod 600 "$CONF/env"
if ! grep -q "API_KEY" "$CONF/env"; then
  cat >>"$CONF/env" <<'ENV'
# Field/Void Pair settings. Fill in the keys for the AIs you want to use.
# ANTHROPIC_API_KEY=
# DEEPSEEK_API_KEY=
# OPENAI_API_KEY=
# GEMINI_API_KEY=
ENV
fi
grep -v '^FVPAIR_REPO=' "$CONF/env" >"$CONF/env.tmp" || true
echo "FVPAIR_REPO=$REPO" >>"$CONF/env.tmp"
mv "$CONF/env.tmp" "$CONF/env"; chmod 600 "$CONF/env"

# 3. Commands.
mkdir -p "$BIN" "$APPS" "$(dirname "$ICON")"
chmod +x "$HERE/fvpair" "$HERE/fvpair-launch" "$HERE/cli.py"
ln -sf "$HERE/fvpair" "$BIN/fvpair"
ln -sf "$HERE/fvpair-launch" "$BIN/fvpair-launch"
cp "$HERE/fvpair.svg" "$ICON"

# 4. Desktop icon + app-menu entry.
entry() {
  cat <<DESK
[Desktop Entry]
Type=Application
Name=Field/Void Pair
Comment=Two AIs in a Field/Void loop through the One-Wave repo lens (Algorythm-Zer0 referee)
Exec="$HERE/fvpair-launch"
Icon=$ICON
Terminal=false
Categories=Development;Science;
Actions=Stop;

[Desktop Action Stop]
Name=Stop Field/Void Pair
Exec="$HERE/fvpair-launch" --stop
DESK
}
entry >"$APPS/fvpair.desktop"
mkdir -p "$DESKTOP_DIR"
entry >"$DESKTOP_DIR/fvpair.desktop"
chmod +x "$APPS/fvpair.desktop" "$DESKTOP_DIR/fvpair.desktop"
# GNOME/Ubuntu: mark the desktop icon trusted so it launches on double-click.
command -v gio >/dev/null && gio set "$DESKTOP_DIR/fvpair.desktop" metadata::trusted true 2>/dev/null || true
command -v update-desktop-database >/dev/null && update-desktop-database "$APPS" 2>/dev/null || true

echo
echo "Installed Field/Void Pair"
echo "  desktop icon : $DESKTOP_DIR/fvpair.desktop"
echo "  app menu     : Field/Void Pair"
echo "  terminal     : fvpair run \"goal\" --field anthropic --void deepseek"
echo "  repo lens    : $REPO"
echo "  API keys     : edit $CONF/env"
case ":$PATH:" in *":$BIN:"*) ;; *) echo "  note         : add $BIN to PATH for the 'fvpair' command";; esac
echo "If double-clicking the icon does nothing, right-click it and choose 'Allow Launching'."
