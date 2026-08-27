#!/usr/bin/env bash
set -euo pipefail

brain_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_dir=$(CDPATH= cd -- "$brain_dir/../.." && pwd)
install_root=${ONE_WAVE_INSTALL_ROOT:-"$HOME/.local/share/one-wave-brain/runtime"}
bin_dir=${ONE_WAVE_BIN_DIR:-"$HOME/.local/bin"}

mkdir -p "$install_root" "$bin_dir" "$HOME/.local/share/one-wave-brain"
python3 -m venv --system-site-packages "$install_root/venv"

launcher="$bin_dir/one-wave-brain"
{
  echo '#!/usr/bin/env bash'
  printf 'export PYTHONPATH=%q\n' "$repo_dir"
  printf 'exec %q -m One_Wave_Bench.brain.cli "$@"\n' "$install_root/venv/bin/python"
} > "$launcher"
chmod 0755 "$launcher"

"$launcher" init
"$launcher" smoke-test --require-jetson

printf 'Installed: %s\n' "$launcher"
printf 'Run: %s cycle "follow"\n' "$launcher"

