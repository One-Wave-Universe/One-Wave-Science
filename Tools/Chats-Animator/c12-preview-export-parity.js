(() => {
  'use strict';
  const A = window.Animator;
  if (!A?.voiceLab || !A?.dialogueEditor || !A?.audioHardening || !A?.playback) throw new Error('C12 requires hardened audio + playback');
  const button = document.getElementById('play-button');
  if (!button) return;

  let context = null;
  let sources = [];
  let wasPlaying = false;

  const dbToGain = (db) => Math.pow(10, Number(db) / 20);
  const cache = new Map();

  async function decode(ctx, src) {
    const key = `${ctx.sampleRate}:${src}`;
    if (cache.has(key)) return cache.get(key);
    const bytes = await (await fetch(src)).arrayBuffer();
    const buffer = await ctx.decodeAudioData(bytes.slice(0));
    cache.set(key, buffer);
    return buffer;
  }

  function stopMix() {
    for (const source of sources) {
      try { source.stop(); } catch (_) {}
    }
    sources = [];
    if (context) {
      try { context.close(); } catch (_) {}
      context = null;
    }
  }

  function makeMaster(ctx) {
    const headroom = ctx.createGain();
    headroom.gain.value = 0.88;
    const limiter = ctx.createDynamicsCompressor();
    limiter.threshold.value = -2;
    limiter.knee.value = 0;
    limiter.ratio.value = 20;
    limiter.attack.value = 0.003;
    limiter.release.value = 0.08;
    headroom.connect(limiter).connect(ctx.destination);
    return headroom;
  }

  async function startMix() {
    stopMix();
    context = new AudioContext();
    await context.resume();
    const master = makeMaster(context);
    const base = context.currentTime + 0.05;
    const clips = (A.voiceLab.state.clips || []).filter(c => !c.muted);
    const attack = Math.max(0.01, Number(A.dialogueEditor.state.attackMs) / 1000 || 0.08);
    const release = Math.max(0.05, Number(A.dialogueEditor.state.releaseMs) / 1000 || 0.3);
    const rawWindows = [];
    for (const clip of clips) rawWindows.push(await A.audioHardening.clipWindow(context, clip));
    const windows = A.audioHardening.mergeWindows(rawWindows, attack + release);

    if (A.audio?.track?.src) {
      const buffer = await decode(context, A.audio.track.src);
      const source = context.createBufferSource();
      source.buffer = buffer;
      const gain = context.createGain();
      gain.gain.setValueAtTime(1, base);
      const duck = dbToGain(-Math.max(0, Number(A.dialogueEditor.state.duckDb) || 0));
      for (const win of windows) {
        const start = base + win.start;
        const end = base + win.end;
        gain.gain.setValueAtTime(1, Math.max(base, start - attack));
        gain.gain.linearRampToValueAtTime(duck, start);
        gain.gain.setValueAtTime(duck, end);
        gain.gain.linearRampToValueAtTime(1, end + release);
      }
      source.connect(gain).connect(master);
      source.start(base);
      sources.push(source);
    }

    for (const clip of clips) sources.push(...await A.dialogueEditor.scheduleEditedClip(context, master, clip, base));
    A.status('Playback using final-mix audio path');
  }

  function capturePlayback(event) {
    event.preventDefault();
    event.stopImmediatePropagation();
    if (A.playback.playing) {
      A.playback.stop();
      stopMix();
    } else {
      A.playback.play();
      startMix().catch(error => {
        console.error(error);
        stopMix();
        A.status(`Final-mix preview failed: ${error.message}`);
      });
    }
  }

  button.addEventListener('click', capturePlayback, true);

  const watcher = setInterval(() => {
    const now = Boolean(A.playback?.playing);
    if (wasPlaying && !now) stopMix();
    wasPlaying = now;
  }, 50);

  window.addEventListener('beforeunload', () => {
    clearInterval(watcher);
    stopMix();
  });

  A.previewParity = { startMix, stopMix };
  A.status('Preview/export audio parity loaded');
})();
