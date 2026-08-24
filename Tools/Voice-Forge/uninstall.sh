#!/usr/bin/env bash
# Removes what install.sh installed for the current user.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/packaging/uninstall_ubuntu.sh"
