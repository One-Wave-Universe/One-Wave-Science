#!/usr/bin/env bash
# Brain Buddy: packet in, gemini_min out. No credentials.
set -euo pipefail

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || fail "run inside One-Wave-Science"
cd "$ROOT"

MODE="${1:-}"
INPUT="${2:-}"
[[ -n "$MODE" && -n "$INPUT" ]] || {
  cat <<'EOF'
Usage:
  scripts/brain_buddy.sh ask "short question"
  scripts/brain_buddy.sh review path/to/query.md
  scripts/brain_buddy.sh code path/to/query.md
  GEMINI_ALLOW_PRO=1 scripts/brain_buddy.sh deep path/to/query.md
EOF
  exit 2
}

INBOX="$ROOT/External_Work/brain_buddy/inbox"
OUTBOX="$ROOT/External_Work/brain_buddy/outbox"
WORK="$ROOT/External_Work/brain_buddy/work"
mkdir -p "$INBOX" "$OUTBOX" "$WORK"

if [[ -f "$INPUT" ]]; then
  BODY="$(cat "$INPUT")"
else
  BODY="$INPUT"
fi
[[ -n "${BODY// /}" ]] || fail "empty query"
BYTES=$(printf '%s' "$BODY" | wc -c)
[[ "$BYTES" -le 12000 ]] || fail "query $BYTES bytes; keep <= 12 KB and use paths"

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
PACKET="$WORK/packet.md"
cat > "$PACKET" <<EOF
# Gemini bounded task (Brain Buddy)

## Goal

$BODY

## Why external Gemini is needed

Local deterministic tools or Qwen handed this packet. Stay bounded.

## Exact repository state

- branch: $(git branch --show-current)
- HEAD: $(git rev-parse HEAD)

## Read only these references first

- GEMINI.md
- files named in the Goal only

Do not scan the repository.

## Allowed files to edit

- none unless mode is code and the Goal names exact paths

## Protected behavior

Do not merge. Do not sudo. Do not request secrets.
Do not rewrite hop arithmetic. Do not rebase T6.
Do not promote paint or 12-TET. Do not invent bench numbers.

## Exact action

Answer or review the Goal. Stop when done.

## Expected result

Smallest useful answer. Paths not dumps.

## Hard stop

Stop after this bounded result.
EOF

RECEIPT="$OUTBOX/${STAMP}-${MODE}.out"
{
  printf 'brain_buddy mode=%s stamp=%s\n' "$MODE" "$STAMP"
  printf 'packet=%s\n' "$PACKET"
} > "$RECEIPT"

WRAP="$ROOT/scripts/gemini_min.sh"
if [[ ! -x "$WRAP" ]]; then
  printf 'HOLD: scripts/gemini_min.sh missing\n' | tee -a "$RECEIPT"
  exit 3
fi

if ! command -v gemini >/dev/null 2>&1 && [[ ! -x "$HOME/.local/bin/gemini" ]]; then
  printf 'HOLD: gemini CLI not installed. Run scripts/install_gemini_jetson.sh and login.\nPacket written: %s\n' "$PACKET" | tee -a "$RECEIPT"
  exit 4
fi

set +e
bash "$WRAP" "$MODE" "$PACKET" >> "$RECEIPT" 2>&1
RC=$?
set -e
printf 'exit=%s\n' "$RC" >> "$RECEIPT"
printf 'receipt %s\n' "$RECEIPT"
exit "$RC"
