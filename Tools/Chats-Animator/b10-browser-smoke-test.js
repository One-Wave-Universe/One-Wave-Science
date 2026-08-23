(() => {
  const $ = (id) => document.getElementById(id);
  const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  function addPanel() {
    if ($('b10-smoke-panel')) return;
    const aside = document.querySelector('aside');
    if (!aside) return;
    const panel = document.createElement('div');
    panel.id = 'b10-smoke-panel';
    panel.className = 'card';
    panel.innerHTML = `
      <strong>B10 browser smoke test</strong><br>
      <span>Runs a reversible self-test of the loaded B1–B9 runtime.</span><br><br>
      <button id="b10-run-smoke" type="button">Run B1–B9 Smoke Test</button>
      <pre id="b10-smoke-output" style="white-space:pre-wrap;max-height:280px;overflow:auto;margin:10px 0 0"></pre>
    `;
    aside.appendChild(panel);
    $('b10-run-smoke').addEventListener('click', runSmoke);
  }

  function line(out, ok, label, detail = '') {
    out.push(`${ok ? 'PASS' : 'FAIL'} — ${label}${detail ? `: ${detail}` : ''}`);
    return ok;
  }

  function makeSyntheticSheetFile() {
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 32;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, 32, 32);
    ctx.fillStyle = '#000000';
    ctx.fillRect(32, 0, 32, 32);
    return new Promise((resolve) => {
      canvas.toBlob((blob) => resolve(new File([blob], 'b10-synthetic-sheet.png', { type: 'image/png' })), 'image/png');
    });
  }

  async function waitForB9(timeoutMs = 2500) {
    const start = performance.now();
    while (!window.b9SpriteSheetSlicer && performance.now() - start < timeoutMs) await wait(50);
    return !!window.b9SpriteSheetSlicer;
  }

  async function runSmoke() {
    const output = $('b10-smoke-output');
    const button = $('b10-run-smoke');
    button.disabled = true;
    output.textContent = 'Running…';
    const out = [];
    let all = true;

    const A = window.OneWaveAnimator;
    const reel = window.b4Reel;
    all &= line(out, !!A, 'B1–B3 core runtime loaded');
    all &= line(out, !!reel && typeof window.b4Snapshot === 'function', 'B4 frame reel API loaded');
    all &= line(out, typeof window.b6RenderOnion === 'function', 'B6 onion-skin API loaded');
    all &= line(out, typeof window.b7StopPlayback === 'function', 'B7 playback API loaded');
    all &= line(out, typeof window.b8ImportBatch === 'function', 'B8 batch import API loaded');

    const b9Loaded = await waitForB9();
    all &= line(out, b9Loaded, 'B9 sprite-sheet slicer API loaded');

    const requiredIds = [
      'scene-stage','asset-layer','frame-reel','frame-hold','play-button','fps-control',
      'batch-import-poses','batch-pose-picker','selected-controls'
    ];
    const missing = requiredIds.filter((id) => !$(id));
    all &= line(out, missing.length === 0, 'Required editor DOM present', missing.length ? missing.join(', ') : 'complete');

    if (A && reel && b9Loaded) {
      const stateBackup = A.clone(A.state);
      const reelBackup = A.clone(reel);
      const storageBackup = {};
      for (const key of ['one-wave-video-maker-b8','one-wave-video-maker-b8-reel']) storageBackup[key] = localStorage.getItem(key);

      try {
        const syntheticAsset = {
          id: `b10-${Date.now()}`,
          kind: 'character',
          name: 'b10-smoke-character.png',
          dataUrl: '',
          width: 32,
          height: 32,
          x: 0.5,
          groundY: 0.72,
          manualScale: 1
        };

        const assetCanvas = document.createElement('canvas');
        assetCanvas.width = 32;
        assetCanvas.height = 32;
        assetCanvas.getContext('2d').fillRect(0, 0, 32, 32);
        syntheticAsset.dataUrl = assetCanvas.toDataURL('image/png');
        A.state.assets = [syntheticAsset];
        A.state.selectedAssetId = syntheticAsset.id;
        A.renderAll();

        const panelReady = !!$('b9-slicer');
        all &= line(out, panelReady, 'B9 slicer UI injected after asset selection');

        if (panelReady) {
          $('b9-rows').value = '1';
          $('b9-cols').value = '2';
          $('b9-hold').value = '2';
          const file = await makeSyntheticSheetFile();
          await window.b9SpriteSheetSlicer.loadSheet(file);
          const before = reel.frames.length;
          await window.b9SpriteSheetSlicer.createFramesFromSlices();
          const added = reel.frames.length - before;
          all &= line(out, added === 2, 'B9 synthetic 1×2 sheet creates two reel frames', `added ${added}`);
          const names = reel.frames.slice(before, before + 2).map((f) => f.snapshot.assets?.find((a) => a.id === syntheticAsset.id)?.name || '');
          all &= line(out, names.every((name) => /_r1_c[12]\.png$/.test(name)), 'B9 slice identity/order preserved', names.join(' | '));
        }
      } catch (error) {
        all = false;
        line(out, false, 'Synthetic sprite-sheet flow', error?.stack || error?.message || String(error));
      } finally {
        Object.keys(A.state).forEach((key) => delete A.state[key]);
        Object.assign(A.state, stateBackup);
        reel.frames.splice(0, reel.frames.length, ...reelBackup.frames);
        reel.activeIndex = reelBackup.activeIndex;
        for (const [key, value] of Object.entries(storageBackup)) {
          if (value === null) localStorage.removeItem(key); else localStorage.setItem(key, value);
        }
        A.renderAll();
        window.b4RenderFrames();
      }
    }

    out.unshift(all ? 'B10 RESULT: PASS' : 'B10 RESULT: FAIL');
    output.textContent = out.join('\n');
    const status = $('runtime-status');
    if (status) status.textContent = all ? 'B10 smoke test PASS' : 'B10 smoke test FAIL — see report';
    button.disabled = false;
    window.b10LastSmokeResult = { pass: !!all, lines: out.slice() };
  }

  addPanel();
  window.b10RunSmoke = runSmoke;
})();
