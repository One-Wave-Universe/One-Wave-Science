#!/usr/bin/env bash
# Assembles a downloadable, self-contained Ubuntu release archive:
# the prebuilt binary plus a plain-bash installer, no Python needed on
# the machine that downloads it. Produces:
#   Tools/Voice-Forge/release/VoiceForge-Ubuntu-x86_64.tar.gz
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

if [ ! -x "dist/VoiceForge/VoiceForge" ]; then
  "$SCRIPT_DIR/build_ubuntu.sh"
fi

STAGE_DIR="$PROJECT_ROOT/release/VoiceForge-Ubuntu"
rm -rf "$PROJECT_ROOT/release"
mkdir -p "$STAGE_DIR"

cp -r "dist/VoiceForge" "$STAGE_DIR/VoiceForge"
cp "assets/icon.png" "$STAGE_DIR/icon.png"
cp "$SCRIPT_DIR/release_install.sh" "$STAGE_DIR/install.sh"
cp "$SCRIPT_DIR/release_uninstall.sh" "$STAGE_DIR/uninstall.sh"
cp "$SCRIPT_DIR/RELEASE_README.txt" "$STAGE_DIR/README.txt"
chmod +x "$STAGE_DIR/install.sh" "$STAGE_DIR/uninstall.sh" "$STAGE_DIR/VoiceForge/VoiceForge"

ARCHIVE_PATH="$PROJECT_ROOT/release/VoiceForge-Ubuntu-x86_64.tar.gz"
tar -C "$PROJECT_ROOT/release" -czf "$ARCHIVE_PATH" "VoiceForge-Ubuntu"

echo
echo "Release archive ready: $ARCHIVE_PATH"
du -h "$ARCHIVE_PATH"
