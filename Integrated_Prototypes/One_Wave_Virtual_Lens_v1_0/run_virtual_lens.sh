#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 one_wave_virtual_lens.py --out results --ticks 90
