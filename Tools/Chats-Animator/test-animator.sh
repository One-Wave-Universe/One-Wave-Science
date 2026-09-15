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
  assistant_server.py
  configure-openai.sh
  launch-animator.sh
  install-ubuntu.sh
)

for file in "${required[@]}"; do
  [[ -f "$file" ]] || { echo "FAIL missing $file" >&2; exit 1; }
done

echo "PASS required animator files"

python3 -m py_compile assistant_server.py
echo "PASS assistant server syntax"

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
bash -n configure-openai.sh
echo "PASS launcher/install/config shell syntax"

grep -q 'c19-local-control-api.js' index.html
grep -q 'c20-five-scale-architecture.js' index.html
grep -q 'c18-director-dialogue.js' index.html
grep -q 'c21-copy-paste-assistant-plugin.js' index.html
echo "PASS control/architecture/director/live-AI scripts wired into index"

grep -q 'state.placementMode = true' app.js
grep -q "placementMode = false" b7-playback.js
grep -q "calibration-overlay.*hidden" b7-playback.js
echo "PASS placement grid enters with PNG placement and leaves before playback"

grep -q 'export-youtube-preset' b13-video-export.js
grep -q "1920×1080" b13-video-export.js
grep -q 'videoBitsPerSecond: width >= 1920 ? 12000000 : 8000000' b13-video-export.js
grep -q 'one-wave-youtube-' b13-video-export.js
grep -q 'ticks / fps' b13-video-export.js
echo "PASS YouTube-ready 1080p export contract"

grep -q 'gpt-5.6-sol' assistant_server.py
grep -q 'gpt-image-2' assistant_server.py
grep -q 'x/z-image-turbo' assistant_server.py
grep -q 'OPENAI_API_KEY' configure-openai.sh
echo "PASS OpenAI Director + local-first art contract"

grep -q 'one-wave-assistant-plugin/v1' c18-director-dialogue.js
grep -q 'live-ai-creative-partner' c21-copy-paste-assistant-plugin.js
grep -q '/api/assistant' c21-copy-paste-assistant-plugin.js
grep -q 'Retry AI connection' c21-copy-paste-assistant-plugin.js
echo "PASS live assistant UI contract"

grep -q 'OneWaveAnimatorControl' c19-local-control-api.js
grep -q 'onewave-control-request' c19-local-control-api.js
echo "PASS external control API contract"

echo "SMOKE TEST PASS"
