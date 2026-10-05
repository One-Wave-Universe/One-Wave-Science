# AI explore loop patch bundle

After checking out this branch (or copying this folder onto `main`'s `Virtual_Breadboard/`):

```bash
bash Virtual_Breadboard/_ai_explore_patch/APPLY.sh
cd Virtual_Breadboard && npm run test:ai-build
```

This installs:
- `js/ai-explore.js` — build → test → adjust → retry (`exploreBuild`), offline LED/divider/RC templates, UI-supported filter, receipt summary
- `js/ai.js` — UI-supported prompt lines + `attachExplore`
- `js/app.js` — `runAiBuild` explore loop + offline templates
- `index.html` / `build-standalone.js` — load `ai-explore.js`
- `README.md` — "AI explore: build, test, adjust"
- `test/ai-build.test.js` — canned repair-loop tests

Already applied on this branch without APPLY: `package.json` (`test:ai-build`), `test/ai-build.test.js`, `build-standalone.js`.
