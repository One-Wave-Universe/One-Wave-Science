#!/usr/bin/env bash
# Builds a standalone Voice Forge binary for Ubuntu (and Jetson/other
# Debian-based desktops) using PyInstaller. Produces dist/VoiceForge/,
# a self-contained folder with the VoiceForge executable inside it.
#
# Usage:
#   Tools/Voice-Forge/packaging/build_ubuntu.sh
#
# Then either run it directly:
#   dist/VoiceForge/VoiceForge
# or install a menu launcher for it:
#   Tools/Voice-Forge/packaging/install_ubuntu.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

echo "== Checking system libraries PySide6 needs at runtime =="
MISSING_PKGS=()
for pkg in libegl1 libgl1 libxkbcommon0 libpulse0; do
  if ! dpkg -s "$pkg" >/dev/null 2>&1; then
    MISSING_PKGS+=("$pkg")
  fi
done
if [ "${#MISSING_PKGS[@]}" -gt 0 ]; then
  echo "Missing packages: ${MISSING_PKGS[*]}"
  echo "Install them with: sudo apt-get install ${MISSING_PKGS[*]}"
else
  echo "All required system libraries are already installed."
fi

VENV_DIR="$PROJECT_ROOT/.venv-build"
if [ ! -d "$VENV_DIR" ]; then
  echo "== Creating build virtualenv at $VENV_DIR =="
  python3 -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "== Installing dependencies =="
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
pip install --quiet pyinstaller

if [ ! -f "assets/icon.png" ] || [ ! -f "assets/sample/sample_voice_a.wav" ]; then
  echo "== Generating icon and demo reference voices =="
  QT_QPA_PLATFORM=offscreen python tools/make_icon.py
  python tools/make_sample_voices.py
fi

echo "== Running PyInstaller =="
pyinstaller packaging/voiceforge.spec --noconfirm --clean

echo
echo "Build complete: $PROJECT_ROOT/dist/VoiceForge/VoiceForge"
echo "Run it directly, or install a menu launcher with packaging/install_ubuntu.sh"
