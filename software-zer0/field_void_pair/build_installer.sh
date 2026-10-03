#!/usr/bin/env bash
# Build one downloadable file: fvpair-installer.sh (self-extracting).
# Running it unpacks the program to ~/.local/share/fvpair/app and runs install_linux.sh,
# which puts the icon on the desktop. It carries a compressed text snapshot of the
# repo (lens_bundle.tar.xz) so the target machine never needs a clone.
#
#   ./build_installer.sh [output-dir]     default: ./dist
set -euo pipefail
HERE="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
OUT="${1:-$HERE/dist}"
mkdir -p "$OUT"
STAGE="$(mktemp -d)"; trap 'rm -rf "$STAGE"' EXIT
python3 - "$HERE" "$STAGE/lens_bundle.tar.xz" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from repo_lens import find_repo_root, write_bundle
write_bundle(find_repo_root(Path(sys.argv[1])), Path(sys.argv[2]))
PY
FILES=(__init__.py app.html cli.py fvpair fvpair-launch fvpair.svg install_linux.sh
       pair_loop.py providers.py repo_lens.py server.py README.md test_field_void_pair.py)
cp "${FILES[@]/#/$HERE/}" "$STAGE/"
# The bundle is already xz-compressed; plain tar avoids compressing it twice.
PAYLOAD="$(tar -C "$STAGE" -cf - "${FILES[@]}" lens_bundle.tar.xz | base64 -w 0)"
REV="$(git -C "$HERE" rev-parse --short HEAD 2>/dev/null || echo unknown)"

cat >"$OUT/fvpair-installer.sh" <<EOF
#!/usr/bin/env bash
# Field/Void Pair installer (built from One-Wave-Science @ $REV).
# Usage: bash fvpair-installer.sh [--repo /path/to/One-Wave-Science]
# Installs to your home folder only (no sudo) and adds a desktop icon.
set -euo pipefail
DEST="\${XDG_DATA_HOME:-\$HOME/.local/share}/fvpair/app"
NEED_KB=8000
command -v python3 >/dev/null || { echo "python3 is required (sudo apt install python3)" >&2; exit 1; }
FREE_KB="\$(df -Pk "\$HOME" | awk 'NR==2 {print \$4}')"
if [[ -n "\$FREE_KB" && "\$FREE_KB" -lt "\$NEED_KB" ]]; then
  echo "Not enough space: need about \$((NEED_KB / 1000)) MB free in \$HOME, have \$((FREE_KB / 1000)) MB." >&2
  exit 1
fi
rm -rf "\$DEST"; mkdir -p "\$DEST"
sed -n '/^__PAYLOAD__\$/,\$p' "\$0" | tail -n +2 | base64 -d | tar -xf - -C "\$DEST"
exec bash "\$DEST/install_linux.sh" "\$@"
__PAYLOAD__
EOF
echo "$PAYLOAD" >>"$OUT/fvpair-installer.sh"
chmod +x "$OUT/fvpair-installer.sh"
echo "built $OUT/fvpair-installer.sh ($(du -h "$OUT/fvpair-installer.sh" | cut -f1))"
