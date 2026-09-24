# Code by Law Build Journal

Newest verified layer goes first.

## 2026-09-23 — GitHub-only Code by Law path

- Project: Code by Law browser extension
- Build step: reduce architecture to chatbot <-> Code by Law <-> GitHub
- Starting checkpoint: e28c5b4f212f1f15ff196b70b6e8e5fc1313b398
- Branch: codex/code-by-law-extension
- Removed: localhost/Jetson companion dependency from the browser extension
- Removed: terminal/Hive Pipe/OpenClaw routing from the governed-turn packet
- GitHub is now the external source of truth
- Added: GitHub repo, branch, and project-build/journal reference paths in the popup
- Added: direct GitHub branch HEAD lookup
- Added: direct read-only GitHub reference-file fetch for project build and journal files
- Preserved: Think Before You Speak, Parser Goblin, Reference Every Step, six cumulative build levels, Bouncer Goblin, Checker Goblin, journal/checkpoint, re-reference
- Repository mutations are directed through the chatbot's authorized GitHub access
- Mozilla lint: 0 errors, 0 notices, 0 warnings
- Project test: PASS
- Mozilla build: PASS
- Laptop transfer: PASS
- Laptop Mozilla lint: 0 errors, 0 notices, 0 warnings
- Laptop Firefox development launch: PASS through web-ext run
- GitHub publication: branch codex/code-by-law-extension created from current remote main
- GitHub source commit: c9d3ef6c35a3464abe8210982bb4744f0406a0a8
- Next permitted step: clean retired companion wording, republish docs, then keep GitHub as the only external project bridge

## 2026-09-23 — Mozilla web-ext lint/build qualification

- Project: Code by Law browser extension
- Build step: qualify the Firefox Linux/Android build with Mozilla's official web-ext tooling and attempt signing
- Starting checkpoint: 285c8924aa1ee885dbfab3424247f1ec34b4179b
- Branch: codex/code-by-law-extension
- Mozilla lint first pass: 0 errors, 3 warnings
- Corrected: removed Chromium-only service_worker from the Firefox manifest path
- Corrected: raised Firefox/Android strict minimum to 142.0 to match data_collection_permissions support
- Mozilla lint final: 0 errors, 0 notices, 0 warnings
- Mozilla web-ext build: PASS
- Artifact: web-ext-artifacts/code_by_law-0.1.0.zip
- Archive integrity: PASS
- Signing attempt boundary: web-ext requires AMO API key and API secret
- Credential check: WEB_EXT_API_KEY, WEB_EXT_API_SECRET, AMO_JWT_ISSUER, and AMO_JWT_SECRET are not configured on the Jetson
- Signing status: HOLD_CREDENTIALS_REQUIRED; no false signed-complete claim
- Laptop status: scales-Latitude-E7450 remains offline, so live Firefox load test cannot be executed there yet
- Next permitted step: obtain/configure Mozilla AMO signing credentials, run web-ext sign, then install/test signed build on Linux Firefox and Android Firefox

## 2026-09-23 — Firefox Linux + Firefox Android packages

- Project: Code by Law browser extension
- Build step: retarget packaged browser builds to Firefox on Linux and Firefox on Android
- Starting checkpoint: 1b2908ac63d14fbec33596103548741737654218
- Branch: codex/code-by-law-extension
- Verified platform support: Firefox for Android supports extensions through Mozilla's Android add-ons channel
- Added Firefox browser_specific_settings with explicit Gecko extension ID and gecko_android support
- Added Firefox-compatible Manifest V3 background scripts fallback while preserving service_worker for Chromium compatibility
- Added Mozilla data collection declaration: none
- Produced: code-by-law-firefox-linux.xpi / .zip
- Produced: code-by-law-firefox-android.xpi / .zip
- Removed obsolete Chrome/Edge package outputs and notes
- Package validation: all four Firefox archives pass unzip integrity tests
- Existing cumulative project test: PROJECT_TEST_PASS
- Limitation: web-ext is not installed on the Jetson, so Mozilla lint/signing has not yet been run
- Limitation: permanent normal Firefox installation requires Mozilla signing; Android normal distribution goes through Mozilla Add-ons Android support
- Next permitted step: run Mozilla web-ext lint/sign flow and then install/test on the actual Linux laptop and Android Firefox when reachable

## 2026-09-23 — Linux Chrome + Android Edge packages

- Project: Code by Law browser extension
- Build step: package the governed extension for Linux Chrome and an Android extension-capable browser
- Starting checkpoint: 9f2d06e0d828be6a80d93f3460ff492c091bfecb
- Branch: codex/code-by-law-extension
- Verified platform fact: Google Chrome on Android does not load browser extensions
- Desktop target: Linux Google Chrome / Chromium-compatible Manifest V3
- Android target: Microsoft Edge Android/mobile extensions
- Added: background companion fetch so governed turns do not depend on page CORS behavior
- Added: optional companion-origin permission for non-localhost Jetson/tunnel URLs
- Added: deterministic packaging script
- Added: Linux Chrome ZIP package and install notes
- Added: Android Edge ZIP package and mobile notes
- Package validation: both ZIP archives pass unzip integrity checks
- Existing project test: PROJECT_TEST_PASS
- Limitation: no live Linux Chrome interaction test yet because the laptop is offline and the Jetson has no Chrome/Chromium binary
- Limitation: Android package still needs testing/installing in the actual phone Edge build; direct sideload availability varies
- Next permitted step: install/test on the real Linux laptop and Android phone when each device is reachable

## 2026-09-23 — Configurable Code by Law companion endpoint

- Project: Code by Law browser extension
- Build step: make the live reference/tool companion endpoint configurable without changing extension source
- Starting checkpoint: 84cda8ec7fb20c47879d42ae6a8d7ad6688a8d18
- Branch: codex/code-by-law-extension
- Added: companion URL field in popup
- Added: stored companion URL in extension storage
- Added: governed-turn packet fetch from the configured companion URL
- Preserved: cumulative six-level project build, project journal history, Parser/Bouncer/Checker laws
- Tests: JavaScript syntax checks, manifest JSON validation, git diff check, cumulative project-state test
- Verified result: PROJECT_TEST_PASS and CONFIGURABLE_COMPANION_PASS
- Hard stop: no new terminal protocol or token storage added
- Next permitted step: real browser load/unpacked functional interaction test

## 2026-09-23 — Code by Law cumulative project-build enforcement

- Project: Code by Law browser extension
- Build step: make project checklists cumulative and force project-build/journal reference on every governed turn
- Starting checkpoint: e8541f3f5be4c5884da628909c11e00c7ed56d11
- Branch: codex/code-by-law-extension
- Added: Parser Goblin and Bouncer Goblin rules
- Added: six cumulative project levels where each higher level carries all previous verified levels
- Added: structured project-build state storage
- Added: journal history storage and injection
- Added: Bouncer gate that blocks higher levels when prior levels are unverified
- Added: live project reference packet from the local Code by Law companion
- Reference rule: every step must reference live repo/source truth together with current project build, cumulative checklist history, checkpoint, and journal entries
- Tests: JSON validation, JavaScript syntax checks, git diff check, cumulative project-state test
- Verified result: PROJECT_TEST_PASS and ALL_CURRENT_CHECKS_PASS
- Protected: canonical One-Wave runtime, Hive Pipe parser/gateway, original dirty checkout
- Unresolved: real browser installation/interaction test and configurable companion endpoint
- Next permitted step: browser-side functional test, then make companion endpoint configurable and checkpoint again

## 2026-09-23 — Layer 1: extension shell + editable rules

- Project: Code by Law browser extension
- Main goal: force AI coding chats through reference-first, tool-aware, layered, checker-verified project work.
- Coder: ChatGPT / GPT-5.6 Sol
- Checker: pending independent OpenClaw/local-model review
- Starting repo: /home/Scales/One-Wave-Science
- Starting branch: codex/ai-local-operations
- Starting HEAD: 4f8a7720c9615a961a9db8a43773fb2d798b22a9
- Build worktree: /home/Scales/One-Wave-Science-code-by-law
- Build branch: codex/code-by-law-extension
- Layer goal: create only the browser-extension shell, editable rule system, and governed-turn injection.
- Added: manifest, default rule pack, shared rule compiler, chat content injector, popup project context, rule manager UI, import/export.
- Protected: existing One-Wave repo runtime, Hive Pipe, terminal parser, GitHub bridge, OpenClaw runtime, and dirty work in the original checkout.
- Tests: JSON parsing, JavaScript syntax checks, git diff --check.
- Static result: PASS.
- Unresolved: real-browser interaction test; live project-reference bridge; checker enforcement; journal/checkpoint persistence; tool-route execution bridge.
- Hard stop: do not implement Jetson/GitHub/Hive Pipe integration in this layer.
- Next permitted layer: independent checker review, then checkpoint Layer 1 before assigning Layer 2 to a different coding program.
