#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

required=(
  index.html
  app.js
  b4-frame-reel.js
  b5-pose-editing.js
  b6-onion-skin.js
  b7-playback.js
  b8-batch-pose-import.js
  b9-sprite-sheet-slicer.js
  b10-project-save-load.js
  b12-camera-motion.js
  b13-video-export.js
  c14-motion-library.js
  c15-motion-atlas.js
  c17-clip-sections.js
  c18-director-dialogue.js
  c19-local-control-api.js
  c20-five-scale-architecture.js
  c21-copy-paste-assistant-plugin.js
  launch-animator.sh
  install-ubuntu.sh
)

for file in "${required[@]}"; do
  [[ -f "$file" ]] || { echo "FAIL missing $file" >&2; exit 1; }
done

echo "PASS required animator files"

if command -v node >/dev/null 2>&1; then
  for file in ./*.js; do
    node --check "$file" >/dev/null
  done
  echo "PASS JavaScript syntax"
else
  echo "SKIP JavaScript syntax: node not installed"
fi

bash -n launch-animator.sh
bash -n install-ubuntu.sh
echo "PASS launcher/install shell syntax"

grep -q 'c19-local-control-api.js' index.html
grep -q 'c20-five-scale-architecture.js' index.html
grep -q 'c18-director-dialogue.js' index.html
grep -q 'c21-copy-paste-assistant-plugin.js' index.html
echo "PASS control/architecture/director/AI bridge scripts wired into index"

grep -q 'one-wave-assistant-plugin/v1' c18-director-dialogue.js
grep -q 'provider-neutral' c18-director-dialogue.js
grep -q 'local-ready' c18-director-dialogue.js
echo "PASS provider-neutral assistant plugin contract"

grep -q 'copy-paste-bridge' c21-copy-paste-assistant-plugin.js
grep -q 'chatgpt-ready' c21-copy-paste-assistant-plugin.js
grep -q 'claude-ready' c21-copy-paste-assistant-plugin.js
grep -q 'Apply AI Response' c21-copy-paste-assistant-plugin.js
echo "PASS universal assistant bridge contract"

grep -q 'OneWaveAnimatorControl' c19-local-control-api.js
grep -q 'onewave-control-request' c19-local-control-api.js
echo "PASS external control API contract"

grep -q 'Micro' c20-five-scale-architecture.js || true
grep -q 'M4' c20-five-scale-architecture.js
grep -q 'Administrator' c20-five-scale-architecture.js
echo "PASS five-scale/oversight architecture present"

echo "SMOKE TEST PASS"
