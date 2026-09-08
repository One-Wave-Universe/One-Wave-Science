#!/usr/bin/env bash
set -euo pipefail

REPO_EXPECTED="One-Wave-Universe/One-Wave-Science"
PREFIX="${GEMINI_NPM_PREFIX:-$HOME/.local}"
BIN_DIR="$PREFIX/bin"

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

command -v git >/dev/null 2>&1 || fail "git is required"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || fail "run this from inside the One-Wave-Science checkout"
cd "$ROOT"

REMOTE="$(git remote get-url origin 2>/dev/null || true)"
case "$REMOTE" in
  *One-Wave-Universe/One-Wave-Science*) ;;
  *) fail "origin is not $REPO_EXPECTED: $REMOTE" ;;
esac

command -v node >/dev/null 2>&1 || fail "node is missing. OpenClaw normally provides a Node-capable Jetson environment; verify node/npm before installing Gemini."
command -v npm >/dev/null 2>&1 || fail "npm is missing"

printf 'Repo: %s\n' "$ROOT"
printf 'Node: %s\n' "$(node --version)"
printf 'npm:  %s\n' "$(npm --version)"

mkdir -p "$PREFIX"
npm install -g --prefix "$PREFIX" @google/gemini-cli@latest

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
  export PATH="$BIN_DIR:$PATH"
fi

command -v gemini >/dev/null 2>&1 || fail "Gemini installed but is not on PATH. Add: export PATH=\"$BIN_DIR:\$PATH\""

printf 'Gemini: %s\n' "$(gemini --version)"

PROFILE="$HOME/.profile"
PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'
if [[ "$PREFIX" == "$HOME/.local" ]] && ! grep -Fqx "$PATH_LINE" "$PROFILE" 2>/dev/null; then
  printf '\n%s\n' "$PATH_LINE" >> "$PROFILE"
  printf 'Added ~/.local/bin to %s\n' "$PROFILE"
fi

cat <<'EOF'

INSTALL COMPLETE.

One-time authentication on the Jetson:
  cd /home/Scales/One-Wave-Science
  NO_BROWSER=true gemini

Prefer "Login with Google" for the official CLI if available for your account.
The no-browser flow prints a URL/code that can be completed from another browser.
After credentials are cached, use the repo wrapper:

  scripts/gemini_min.sh review TASK.md
  scripts/gemini_min.sh code TASK.md

Routine work should stay local with Qwen/OpenClaw. Gemini is the bounded external escalation lane.
Do not put API keys in this repository.
EOF
