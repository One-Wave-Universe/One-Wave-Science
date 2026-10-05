#!/usr/bin/env bash
# Apply Virtual Breadboard AI explore loop. Run from repo root:
#   bash Virtual_Breadboard/_ai_explore_patch/APPLY.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
VB="$(cd "$ROOT/.." && pwd)"
cd "$VB"
if [[ -f "$ROOT/ai-explore.js" ]]; then
  cp "$ROOT/ai-explore.js" js/ai-explore.js
elif [[ -f "$ROOT/ai-explore.js.b64.1" && -f "$ROOT/ai-explore.js.b64.2" ]]; then
  cat "$ROOT/ai-explore.js.b64.1" "$ROOT/ai-explore.js.b64.2" | base64 -d > js/ai-explore.js
else
  echo "missing ai-explore.js" >&2; exit 1
fi
patch -p1 < "$ROOT/ai.js.patch"
patch -p1 < "$ROOT/app.js.patch"
patch -p1 < "$ROOT/index.html.patch"
patch -p1 < "$ROOT/build-standalone.js.patch"
patch -p1 < "$ROOT/README.md.patch"
if [[ -f "$ROOT/package.json.patch" ]]; then patch -p1 < "$ROOT/package.json.patch" || true; fi
cp "$ROOT/ai-build.test.js" test/ai-build.test.js
chmod +x test/ai-build.test.js
echo "Applied AI explore loop. Verify: cd Virtual_Breadboard && npm run test:ai-build"
