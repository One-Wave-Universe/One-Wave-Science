#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${HOME}/.local/share/one-wave-animator"
VENV_DIR="${APP_DIR}/venv"
BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

command -v python3 >/dev/null 2>&1 || {
  echo "Animator needs Python 3. Install python3 and python3-venv, then rerun this installer." >&2
  exit 1
}

mkdir -p "${APP_DIR}" "${BIN_DIR}" "${DESKTOP_DIR}"
cp "${HERE}/main.py" "${APP_DIR}/main.py"
cp "${HERE}/requirements.txt" "${APP_DIR}/requirements.txt"

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/python" -m pip install --upgrade pip
"${VENV_DIR}/bin/pip" install -r "${APP_DIR}/requirements.txt"

cat > "${BIN_DIR}/one-wave-animator" <<EOF
#!/usr/bin/env bash
exec "${VENV_DIR}/bin/python" "${APP_DIR}/main.py" "\$@"
EOF
chmod +x "${BIN_DIR}/one-wave-animator"

cat > "${DESKTOP_DIR}/one-wave-animator.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=One-Wave Animator
Comment=Fixed-layer animation editor
Exec=${BIN_DIR}/one-wave-animator
Terminal=false
Categories=Graphics;AudioVideo;
StartupNotify=true
EOF
chmod +x "${DESKTOP_DIR}/one-wave-animator.desktop"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true
fi

echo
echo "Animator installed."
echo "Launch it from your app menu as 'One-Wave Animator'"
echo "or run: ${BIN_DIR}/one-wave-animator"
