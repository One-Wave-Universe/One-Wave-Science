#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PENDING="$SCRIPT_DIR/queue/pending"
PROCESSING="$SCRIPT_DIR/queue/processing"
MODE="${1:---once}"

case "$MODE" in
  --once|--watch) ;;
  *) echo "usage: $0 [--once|--watch]" >&2; exit 2 ;;
esac

mkdir -p "$PENDING" "$PROCESSING" "$SCRIPT_DIR/queue/results" "$SCRIPT_DIR/queue/done"

run_one() {
  local source claimed
  source="$(find "$PENDING" -maxdepth 1 -type f -name '*.json' -print | LC_ALL=C sort | head -n 1)"
  [[ -n "$source" ]] || return 1
  claimed="$PROCESSING/$(basename -- "$source")"
  mv -- "$source" "$claimed"
  python3 "$SCRIPT_DIR/mudl.py" run "$claimed"
}

if [[ "$MODE" == "--once" ]]; then
  if ! run_one; then
    echo "HIVE_PIPE_IDLE"
  fi
  exit 0
fi

echo "HIVE_PIPE_WATCHING $PENDING"
while true; do
  run_one || sleep 2
done

