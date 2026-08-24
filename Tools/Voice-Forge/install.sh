#!/usr/bin/env bash
# One-click install: builds Voice Forge (if not already built) and
# installs it for the current user with a Desktop icon and an
# Applications-menu entry. No sudo, no system-wide changes.
#
# Usage:
#   ./install.sh            build (if needed) and install
#   ./install.sh --rebuild  force a fresh build first
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILT_BINARY="$SCRIPT_DIR/dist/VoiceForge/VoiceForge"

if [ ! -x "$BUILT_BINARY" ] || [ "${1:-}" = "--rebuild" ]; then
  "$SCRIPT_DIR/packaging/build_ubuntu.sh"
fi

"$SCRIPT_DIR/packaging/install_ubuntu.sh"
