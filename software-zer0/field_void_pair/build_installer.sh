#!/usr/bin/env bash
# Build one downloadable file: fvpair-installer.sh (self-extracting).
# Running it unpacks the program to ~/.local/share/fvpair/app and runs install_linux.sh,
# which puts the icon on the desktop.
#
#   ./build_installer.sh [output-dir]     default: ./dist
set -euo pipefail
HERE="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
OUT="${1:-$HERE/dist}"
mkdir -p "$OUT"
FILES=(__init__.py app.html cli.py fvpair fvpair-launch fvpair.svg install_linux.sh
       pair_loop.py providers.py repo_lens.py server.py README.md test_field_void_pair.py)
PAYLOAD="$(tar -C "$HERE" -czf - "${FILES[@]}" | base64 -w 0)"
REV="$(git -C "$HERE" rev-parse --short HEAD 2>/dev/null || echo unknown)"

cat >"$OUT/fvpair-installer.sh" <<EOF
#!/usr/bin/env bash
# Field/Void Pair installer (built from One-Wave-Science @ $REV).
# Usage: bash fvpair-installer.sh [--repo /path/to/One-Wave-Science]
# Installs to your home folder only (no sudo) and adds a desktop icon.
set -euo pipefail
DEST="\${XDG_DATA_HOME:-\$HOME/.local/share}/fvpair/app"
command -v python3 >/dev/null || { echo "python3 is required (sudo apt install python3)" >&2; exit 1; }
rm -rf "\$DEST"; mkdir -p "\$DEST"
sed -n '/^__PAYLOAD__\$/,\$p' "\$0" | tail -n +2 | base64 -d | tar -xzf - -C "\$DEST"
exec bash "\$DEST/install_linux.sh" "\$@"
__PAYLOAD__
EOF
echo "$PAYLOAD" >>"$OUT/fvpair-installer.sh"
chmod +x "$OUT/fvpair-installer.sh"
echo "built $OUT/fvpair-installer.sh ($(du -h "$OUT/fvpair-installer.sh" | cut -f1))"
