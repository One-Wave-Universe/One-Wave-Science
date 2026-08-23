#!/usr/bin/env bash
set -euo pipefail
PREFIX="${HOME}/.local"
LIB_DIR="${PREFIX}/lib/one-wave/animator-runner"
BIN_DIR="${PREFIX}/bin"
STATE_DIR="${HOME}/.local/share/one-wave/animator-runner"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "${LIB_DIR}" "${BIN_DIR}" "${STATE_DIR}"/{jobs,results,logs,state}
rm -rf "${LIB_DIR}/animator_runner"
cp -R "${SCRIPT_DIR}/animator_runner" "${LIB_DIR}/animator_runner"
cat > "${BIN_DIR}/animator-runner" <<EOF
#!/usr/bin/env bash
exec python3 "${LIB_DIR}/animator_runner/cli.py" "\$@"
EOF
chmod +x "${BIN_DIR}/animator-runner"
echo "Installed animator-runner at ${BIN_DIR}/animator-runner"
echo "State directory: ${STATE_DIR}"
echo 'If needed: export PATH="$HOME/.local/bin:$PATH"'
"${BIN_DIR}/animator-runner" init >/dev/null
"${BIN_DIR}/animator-runner" actions
