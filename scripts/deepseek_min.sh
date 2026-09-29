#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/deepseek_min.sh ask "short question"
  scripts/deepseek_min.sh review TASK.md
  scripts/deepseek_min.sh science TASK.md
  DEEPSEEK_ALLOW_DEEP=1 scripts/deepseek_min.sh deep TASK.md

Modes:
  ask      bounded question, repo reference first, no edits
  review   bounded review, named references only, no edits
  science  proof/theory review using canonical One-Wave + I-06 metadata chain
  deep     deeper review, explicit opt-in only

Environment:
  DEEPSEEK_API_KEY       required for model calls
  HIVE_PIPE_MCP_URL      optional; defaults to local Jetson MCP
  HIVE_PIPE_TOKEN_FILE   optional; defaults to DeepSeek Hive token
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

[[ -n "${DEEPSEEK_API_KEY:-}" ]] || fail "DEEPSEEK_API_KEY is required for DeepSeek model calls"

BRANCH="$(git branch --show-current)"
HEAD_SHA="$(git rev-parse HEAD)"
STATUS="$(git status --short)"

read_task() {
  local value="$1"
  if [[ -f "$value" ]]; then
    local bytes
    bytes="$(wc -c < "$value")"
    [[ "$bytes" -le 16000 ]] || fail "task file is $bytes bytes; keep DeepSeek packets <= 16 KB and reference repo files by path"
    cat "$value"
  else
    printf '%s' "$value"
  fi
}

TASK="$(read_task "$INPUT")"
[[ -n "$TASK" ]] || fail "empty task"

MODE_RULES=""
BRIDGE_ARGS=(--max-tool-rounds 12)

case "$MODE" in
  ask)
    MODE_RULES="Answer one bounded question. Read the mandatory reference files first, then only explicitly named dependencies. Do not edit files."
    ;;
  review)
    MODE_RULES="Review only. Do not edit files. Read mandatory references first, then only named files and the smallest direct dependencies needed."
    ;;
  science)
    BRIDGE_ARGS+=(--max-tool-rounds 18)
    MODE_RULES="Science/theory review. Distinguish established external physics/math from One-Wave hypotheses. Status comes from I-06 YAML/front matter, not prose. Prefer falsifiable derivations/tests and explicit PASS/FAIL/INCONCLUSIVE criteria."
    ;;
  deep)
    [[ "${DEEPSEEK_ALLOW_DEEP:-0}" == "1" ]] || fail "deep mode requires DEEPSEEK_ALLOW_DEEP=1"
    BRIDGE_ARGS+=(--max-tool-rounds 24)
    MODE_RULES="Deep review only. Stay bounded to the reference chain and named files. State uncertainty instead of inventing missing context."
    ;;
  *)
    usage
    fail "unknown mode: $MODE"
    ;;
esac

PROMPT=$(cat <<EOF
DEEPSEEK BRAIN BUDDY — BOUNDED ONE-WAVE TASK
Mode: $MODE
Repo: One-Wave-Universe/One-Wave-Science
Branch: $BRANCH
HEAD: $HEAD_SHA

MANDATORY REFERENCE ORDER
1. Read GENERAL_REFERENCE_RULES.md
2. Read AI_CANONICAL_START_HERE.md
3. Read Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md
4. Read the exact proof/node/task files named below
5. Check YAML/front matter for current gate/lifecycle where present
6. Answer only after those references are grounded

REFERENCE LOOP
REFERENCE GIT -> ASK/PIVOT -> REFERENCE METADATA/FLIP -> VALIDATE/PIVOT -> RETURN TO REFERENCE

RULES
- $MODE_RULES
- Use Jetson/Hive Pipe tools for repository reads when needed.
- Do not scan the whole repository.
- Do not use chat memory as authority.
- Do not infer gate/lifecycle from prose.
- Do not claim a command ran without a matching tool receipt.
- Do not merge or push.
- Do not request or expose secrets.
- Keep output concise and cite exact repo paths actually used.
- If a required reference is missing or unreadable, say HOLD and name the exact missing reference.

TASK
$TASK
EOF
)

exec python3 One_Wave_Bench/hive-pipe/deepseek_bridge.py "${BRIDGE_ARGS[@]}" "$PROMPT"
