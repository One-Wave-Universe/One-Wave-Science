#!/usr/bin/env bash
set -euo pipefail
rm -rf "${HOME}/.local/lib/one-wave/animator-runner"
rm -f "${HOME}/.local/bin/animator-runner"
echo "Removed animator-runner program."
echo "State/logs remain at ~/.local/share/one-wave/animator-runner"
