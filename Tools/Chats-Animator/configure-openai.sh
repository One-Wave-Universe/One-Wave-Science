#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$HOME/.config/one-wave-animator/openai.env"

printf '\nOne-Wave Animator — AI connection setup\n'
printf 'API key setup now happens inside the animator so you can see what you are doing.\n'
if [[ -f "$CONFIG_FILE" ]]; then
  printf 'A saved key configuration already exists. Use Retry AI Connection in the animator to inspect or replace it.\n'
else
  printf 'No saved key configuration was found. The animator will open the key-entry panel automatically.\n'
fi
printf '\nLaunching animator...\n\n'
exec "$APP_DIR/launch-animator.sh"
