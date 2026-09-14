#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_BASE="${ONE_WAVE_DATA_OUT:-$HOME/One-Wave-External-Work/work/gwosc}"
mkdir -p "$OUT_BASE"

EVENT_VERSION="${GWOSC_EVENT_VERSION:-GW150914-v2}"
DETECTORS="${GWOSC_DETECTORS:-H1,L1}"
OUT="$OUT_BASE/${EVENT_VERSION}-wave.json"
RAW_DIR="$OUT_BASE/source-${EVENT_VERSION}"

printf '%s\n' '=== ONE-WAVE GWOSC / JETSON RUN ==='
printf 'repo=%s\n' "$ROOT"
printf 'event=%s detectors=%s\n' "$EVENT_VERSION" "$DETECTORS"
printf 'output=%s\n' "$OUT"

if command -v openclaw >/dev/null 2>&1; then
  printf 'openclaw=%s\n' "$(command -v openclaw)"
else
  printf '%s\n' 'openclaw=NOT_FOUND (not required for reproducible pipeline)'
fi

cd "$ROOT"
python3 tools/gwosc_wave/run_with_network_retry.py \
  --attempts 3 \
  --base-delay 3 \
  -- \
  --event-version "$EVENT_VERSION" \
  --detectors "$DETECTORS" \
  --sample-rate-khz 4 \
  --duration 32 \
  --window-seconds 4 \
  --band-min-hz 20 \
  --band-max-hz 512 \
  --top-bins 12 \
  --raw-dir "$RAW_DIR" \
  --output "$OUT"

printf '%s\n' 'GWOSC_JETSON_PIPELINE_COMPLETE'
