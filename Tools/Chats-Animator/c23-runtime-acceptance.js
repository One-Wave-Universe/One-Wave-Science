(() => {
  'use strict';

  const A = window.Animator;
  if (!A) throw new Error('Runtime acceptance requires Animator');

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const required = [
    ['reel', () => A.reel],
    ['playback', () => A.playback],
    ['projectIO', () => A.projectIO],
    ['audio', () => A.audio],
    ['voiceLab', () => A.voiceLab],
    ['dialogueEditor', () => A.dialogueEditor],
    ['audioHardening', () => A.audioHardening],
    ['previewParity', () => A.previewParity],
    ['camera', () => A.camera],
    ['videoExport', () => A.videoExport],
    ['clipSections', () => A.clipSections],
    ['motionLibrary', () => A.motionLibrary],
    ['motionAtlas', () => A.motionAtlas],
    ['control', () => A.control]
  ];

  async function waitForModules(timeoutMs = 6000) {
    const started = performance.now();
    while (performance.now() - started < timeoutMs) {
      const missing = required.filter(([, get]) => !get()).map(([name]) => name);
      if (!missing.length) return [];
      await sleep(50);
    }
    return required.filter(([, get]) => !get()).map(([name]) => name);
  }

  function snapshotDigest(frames) {
    return JSON.stringify(frames.map((frame) => ({
      hold: frame.hold,
      snapshot: frame.snapshot
    })));
  }

  function updateSystemPill(ok, text) {
    const pill = document.getElementById('system-status');
    if (!pill) return;
    pill.textContent = text;
    pill.dataset.state = ok ? 'ready' : 'error';
  }

  async function selfTest() {
    const missing = await waitForModules();
    if (missing.length) throw new Error(`Modules not ready: ${missing.join(', ')}`);

    const fixed = await A.fixedCelDemo.loadDemo();
    if (!fixed.fixedTransform || fixed.uniqueDrawings !== 12) throw new Error('Fixed-cel invariant failed');

    const R = A.reel;
    const Core = window.AnimatorFixedCelCore;
    const targetId = R.frames[0].snapshot.assets.find((asset) => asset.kind === 'character')?.id;
    if (!targetId) throw new Error('Demo character missing');

    const built = A.projectIO.buildProject();
    if (built.frames.length !== 12) throw new Error('Project save did not capture 12 reel frames');
    const encoded = JSON.stringify(built);
    A.projectIO.applyProject(JSON.parse(encoded));
    const rebuilt = A.projectIO.buildProject();

    const afterCheck = Core.verifyFixedCelSnapshots(rebuilt.frames.map((f) => f.snapshot), targetId);
    if (!afterCheck.fixedTransform || afterCheck.uniqueDrawings !== 12) throw new Error('Project reload changed cel animation');
    if (rebuilt.frames.some((frame) => Number(frame.hold) !== 2)) throw new Error('Project reload changed drawing holds');
    if (Number(rebuilt.fps) !== 24) throw new Error('Project reload changed FPS');

    const beforePlayback = snapshotDigest(R.frames);
    R.preview(0);
    A.playback.play();
    await sleep(1350);
    if (A.playback.playing) A.playback.stop();
    const afterPlayback = snapshotDigest(R.frames);
    if (beforePlayback !== afterPlayback) throw new Error('Playback mutated canonical reel');

    const thumbs = document.querySelectorAll('.frame-thumb').length;
    if (thumbs !== 12) throw new Error(`Expected 12 reel thumbnails, found ${thumbs}`);

    document.body.dataset.animatorSelftest = 'pass';
    document.body.dataset.animatorFrames = String(R.frames.length);
    document.body.dataset.animatorDrawings = String(afterCheck.uniqueDrawings);
    document.body.dataset.animatorPlaybackReadonly = 'true';
    document.body.dataset.animatorModules = String(required.length);
    updateSystemPill(true, 'CORE READY · 12-CEL PASS');
    A.status('Runtime acceptance PASS — fixed cels, save/load, playback and integrated modules');
    return { fixed: afterCheck, modules: required.map(([name]) => name), frames: R.frames.length, thumbs };
  }

  async function readiness() {
    const missing = await waitForModules();
    if (missing.length) {
      updateSystemPill(false, `CORE PARTIAL · ${missing.length} MISSING`);
      return;
    }
    updateSystemPill(true, 'CORE READY');
  }

  window.addEventListener('load', () => {
    readiness();
    const params = new URLSearchParams(location.search);
    if (params.get('selftest') === '1') {
      selfTest().catch((error) => {
        console.error(error);
        document.body.dataset.animatorSelftest = 'fail';
        document.body.dataset.animatorSelftestError = error.message;
        updateSystemPill(false, 'CORE FAIL');
        A.status(`Runtime acceptance FAIL: ${error.message}`);
      });
    }
  });

  A.runtimeAcceptance = { selfTest, waitForModules };
})();
