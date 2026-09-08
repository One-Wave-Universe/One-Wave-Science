#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/gemini_min.sh review TASK.md
  scripts/gemini_min.sh code TASK.md
  scripts/gemini_min.sh ask "short question"
  GEMINI_ALLOW_PRO=1 scripts/gemini_min.sh deep TASK.md

Modes:
  review  flash-lite, bounded read/review, no intentional edits
  code    flash, auto-approve edit tools only; refuses main/dirty tree by default
  ask     flash-lite, short answer with no repo-wide scan
  deep    pro, explicit opt-in only
EOF
}

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

[[ $# -ge 2 ]] || { usage; exit 2; }
MODE="$1"
shift
INPUT="$1"

command -v git >/dev/null 2>&1 || fail "git is required"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || fail "run inside One-Wave-Science"
cd "$ROOT"

REMOTE="$(git remote get-url origin 2>/dev/null || true)"
case "$REMOTE" in
  *One-Wave-Universe/One-Wave-Science*) ;;
  *) fail "unexpected origin: $REMOTE" ;;
esac

if ! command -v gemini >/dev/null 2>&1; then
  if [[ -x "$HOME/.local/bin/gemini" ]]; then
    export PATH="$HOME/.local/bin:$PATH"
  else
    fail "gemini not found; run scripts/install_gemini_jetson.sh first"
  fi
fi

BRANCH="$(git branch --show-current)"
HEAD_SHA="$(git rev-parse HEAD)"
STATUS="$(git status --short)"

read_task() {
  local value="$1"
  if [[ -f "$value" ]]; then
    local bytes
    bytes="$(wc -c < "$value")"
    [[ "$bytes" -le 16000 ]] || fail "task file is $bytes bytes; keep Gemini packets <= 16 KB and reference repo files by path"
    cat "$value"
  else
    printf '%s' "$value"
  fi
}

TASK="$(read_task "$INPUT")"
[[ -n "$TASK" ]] || fail "empty task"

MODEL="flash-lite"
APPROVAL="default"
MODE_RULES=""

case "$MODE" in
  review)
    MODEL="flash-lite"
    APPROVAL="default"
    MODE_RULES="Review only. Do not edit files. Do not run shell commands unless the task explicitly requests one deterministic read-only check. Read only explicitly named files and the smallest dependencies needed."
    ;;
  ask)
    MODEL="flash-lite"
    APPROVAL="default"
    MODE_RULES="Answer the bounded question. Do not scan the repository. Do not edit files or run shell commands."
    ;;
  code)
    MODEL="flash"
    APPROVAL="auto_edit"
    [[ "$BRANCH" != "main" ]] || [[ "${GEMINI_ALLOW_MAIN:-0}" == "1" ]] || fail "code mode refuses main; create/switch to a Gemini work branch, or explicitly set GEMINI_ALLOW_MAIN=1"
    [[ -z "$STATUS" ]] || [[ "${GEMINI_ALLOW_DIRTY:-0}" == "1" ]] || fail "code mode refuses a dirty working tree; preserve another worker's changes first"
    MODE_RULES="Make the smallest bounded edit. Only edit files explicitly named by the task unless one direct dependency is necessary. Do not modify acceptance tests unless the task explicitly says to. Do not merge. Do not use sudo, raw devices, credentials, network installers, or destructive shell commands. Prefer returning the exact deterministic test command for the host/local worker to run after your edit rather than spending another model turn."
    ;;
  deep)
    [[ "${GEMINI_ALLOW_PRO:-0}" == "1" ]] || fail "deep/pro mode requires GEMINI_ALLOW_PRO=1"
    MODEL="pro"
    APPROVAL="default"
    MODE_RULES="Deep review only unless the task explicitly requests an edit. Stay bounded to named references. State uncertainties instead of expanding context automatically."
    ;;
  *) usage; fail "unknown mode: $MODE" ;;
esac

PROMPT=$(cat <<EOF
BOUNDED ONE-WAVE TASK
Mode: $MODE
Repo: One-Wave-Universe/One-Wave-Science
Branch: $BRANCH
HEAD: $HEAD_SHA

$MODE_RULES

Token rule: do not summarize files I did not ask for. Do not repeat long source text. Use paths and concise findings. Stop as soon as the task is satisfied.

TASK:
$TASK
EOF
)

# Disable extensions for predictable low-overhead calls. Project settings in
# .gemini/settings.json further cap context/session/tool-output budgets.
exec gemini \
  --skip-trust \
  --extensions none \
  --model "$MODEL" \
  --approval-mode "$APPROVAL" \
  --output-format json \
  --prompt "$PROMPT"
