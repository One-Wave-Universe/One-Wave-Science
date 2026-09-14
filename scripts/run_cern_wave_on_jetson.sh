#!/usr/bin/env bash
set -euo pipefail

# Jetson-ready CERN -> wave launch script.
# This script intentionally does not install OpenClaw or touch credentials.
# It runs the stdlib-only converter and reports whether OpenClaw is present.

ROOT="${ONE_WAVE_ROOT:-$HOME/One-Wave-Science}"
OUT_ROOT="${CERN_WAVE_OUT:-$HOME/One-Wave-External-Work/work/cern-wave}"
SOURCE_URL="${CERN_WAVE_SOURCE:-https://opendata.cern.ch/record/545/files/Dimuon_DoubleMu.csv}"
MAX_EVENTS="${CERN_WAVE_MAX_EVENTS:-5000}"
REF_GEV="${CERN_WAVE_REF_GEV:-10}"
REF_HZ="${CERN_WAVE_REF_HZ:-1000}"

cd "$ROOT"
mkdir -p "$OUT_ROOT"

printf '%s\n' '=== CORE-RULES-PRE ==='
printf '%s\n' 'Using locked CERN four-vector -> wave transform. Source is preserved; analog scaling is labeled.'

printf '%s\n' '=== HOST ==='
hostname
uname -m
python3 --version

printf '%s\n' '=== OPENCLAW AVAILABILITY ==='
if command -v openclaw >/dev/null 2>&1; then
  command -v openclaw
  openclaw --version || true
else
  printf '%s\n' 'OPENCLAW_NOT_FOUND_IN_PATH'
fi

printf '%s\n' '=== CERN -> WAVE ==='
python3 tools/cern_wave/cern_wave_convert.py \
  --input "$SOURCE_URL" \
  --output "$OUT_ROOT/dimuon-wave.jsonl" \
  --summary "$OUT_ROOT/dimuon-wave-summary.json" \
  --source-record CMS-545 \
  --reference-energy-gev "$REF_GEV" \
  --bench-frequency-hz "$REF_HZ" \
  --max-events "$MAX_EVENTS"

python3 tools/cern_wave/cern_wave_receipt.py \
  "$OUT_ROOT/dimuon-wave.jsonl" \
  --output "$OUT_ROOT/dimuon-wave-receipt.json"

printf '%s\n' '=== OUTPUTS ==='
ls -lh \
  "$OUT_ROOT/dimuon-wave.jsonl" \
  "$OUT_ROOT/dimuon-wave-summary.json" \
  "$OUT_ROOT/dimuon-wave-receipt.json"

printf '%s\n' '=== CORE-RULES-POST ==='
printf '%s\n' 'CERN source preserved; STANDARD_DERIVED and SCALED_ANALOG remain separated; source-lineage warnings remain visible.'
