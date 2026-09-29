#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/deepseek_min.sh ask "short question"
  scripts/deepseek_min.sh review TASK.md
  scripts/deepseek_min.sh science TASK.md
  DEEPSEEK_ALLOW_DEEP=1 scripts/deepseek_min.sh deep TASK.md

Default transport:
  free DeepSeek web session on the Dell relay over USB.

Optional paid fallback:
  DEEPSEEK_USE_API=1 ... uses deepseek_bridge.py and requires DEEPSEEK_API_KEY.
EOF
}

fail(){ printf 'ERROR: %s\n' "$*" >&2; exit 1; }
[[ $# -ge 2 ]] || { usage; exit 2; }
MODE="$1"; shift; INPUT="$1"

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || fail "run inside One-Wave-Science"
cd "$ROOT"
REMOTE="$(git remote get-url origin 2>/dev/null || true)"
case "$REMOTE" in *One-Wave-Universe/One-Wave-Science*) ;; *) fail "unexpected origin: $REMOTE" ;; esac

BRANCH="$(git branch --show-current)"
HEAD_SHA="$(git rev-parse HEAD)"

read_task(){
  local value="$1"
  if [[ -f "$value" ]]; then
    local bytes; bytes="$(wc -c < "$value")"
    [[ "$bytes" -le 16000 ]] || fail "task file is $bytes bytes; keep DeepSeek packets <= 16 KB and reference repo files by path"
    cat "$value"
  else printf '%s' "$value"; fi
}
TASK="$(read_task "$INPUT")"
[[ -n "$TASK" ]] || fail "empty task"

MODE_RULES=""
ROUNDS=12
case "$MODE" in
  ask) MODE_RULES="Answer one bounded question. Read mandatory references first. Do not edit files." ;;
  review) MODE_RULES="Review only. Read mandatory references first, then only named files and the smallest direct dependencies." ;;
  science) ROUNDS=18; MODE_RULES="Science/theory review. Separate established physics/math from One-Wave hypotheses. Status comes from I-06 YAML/front matter. Prefer falsifiable PASS/FAIL/INCONCLUSIVE tests." ;;
  deep)
    [[ "${DEEPSEEK_ALLOW_DEEP:-0}" == "1" ]] || fail "deep mode requires DEEPSEEK_ALLOW_DEEP=1"
    ROUNDS=24
    MODE_RULES="Deep review only. Stay bounded to the reference chain and named files. State uncertainty instead of inventing context."
    ;;
  *) usage; fail "unknown mode: $MODE" ;;
esac

PROMPT=$(cat <<EOF
DEEPSEEK BRAIN BUDDY â BOUNDED ONE-WAVE TASK
Mode: $MODE
Repo: One-Wave-Universe/One-Wave-Science
Branch: $BRANCH
HEAD: $HEAD_SHA

MANDATORY REFERENCE ORDER
1. Read GENERAL_REFERENCE_RULES.md
2. Read AI_CANONICAL_START_HERE.md
3. Read Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md
4. Read the exact proof/node/task files named below
5. Check YAML/front matter for gate/lifecycle where present
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
- Cite exact repo paths actually used.
- If a required reference is missing or unreadable, say HOLD and name it.

TASK
$TASK
EOF
)

if [[ "${DEEPSEEK_USE_API:-0}" == "1" ]]; then
  [[ -n "${DEEPSEEK_API_KEY:-}" ]] || fail "DEEPSEEK_USE_API=1 requires DEEPSEEK_API_KEY"
  exec python3 One_Wave_Bench/hive-pipe/deepseek_bridge.py --max-tool-rounds "$ROUNDS" "$PROMPT"
fi

export DEEPSEEK_WEB_BASE_URL="${DEEPSEEK_WEB_BASE_URL:-http://192.168.55.100:3000}"
# The supported relay binds only to the Dell USB interface and allowlists the Jetson.
# A non-secret placeholder satisfies the existing web client header contract.
export DEEPSEEK_WEB_API_KEY="${DEEPSEEK_WEB_API_KEY:-usb-local}"
exec python3 One_Wave_Bench/hive-pipe/deepseek_web_bridge.py --max-tool-rounds "$ROUNDS" "$PROMPT"
