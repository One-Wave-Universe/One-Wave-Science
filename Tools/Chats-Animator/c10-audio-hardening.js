(() => {
  'use strict';
  const A = window.Animator;
  if (!A?.voiceLab || !A?.dialogueEditor) throw new Error('C10 requires Voice Lab + Dialogue Editor');

  const cache = new Map();
  const dbToGain = (db) => Math.pow(10, Number(db) / 20);

  async function decode(context, src) {
    const key = `${context.sampleRate}:${src}`;
    if (cache.has(key)) return cache.get(key);
    const bytes = await (await fetch(src)).arrayBuffer();
    const buffer = await context.decodeAudioData(bytes.slice(0));
    cache.set(key, buffer);
    return buffer;
  }

  async function clipWindow(context, clip) {
    A.dialogueEditor.ensureClip(clip);
    if (clip.muted) return null;
    const character = A.voiceLab.state.characters.find(c => c.id === clip.characterId);
    const recipe = character?.recipe || {};
    const basePitch = Number(recipe.pitch) || 0;
    const tail = Math.max(Number(recipe.delayMix) > 0 ? 0.35 : 0, Number(recipe.reverb) > 0 ? 0.55 : 0);
    let earliest = Infinity;
    let latest = -Infinity;
    for (let i = 0; i < (clip.layers || []).length; i += 1) {
      const layer = clip.layers[i];
      if (!layer?.src) continue;
      const setting = clip.settings?.[i] || {};
      const buffer = await decode(context, layer.src);
      const trimIn = Math.max(0, Number(clip.trimStart) || 0);
      const trimOut = Math.max(0, Number(clip.trimEnd) || 0);
      const available = Math.max(0, buffer.duration - trimIn - trimOut);
      if (!available) continue;
      const delay = Math.max(0, Number(setting.delayMs) || 0) / 1000;
      const cents = Math.max(-2400, Math.min(2400, basePitch + (Number(setting.detune) || 0)));
      const playbackRate = Math.pow(2, cents / 1200);
      const wallDuration = available / Math.max(0.25, playbackRate);
      earliest = Math.min(earliest, delay);
      latest = Math.max(latest, delay + wallDuration + tail);
    }
    if (!Number.isFinite(earliest) || !Number.isFinite(latest)) return null;
    const baseStart = Math.max(0, Number(clip.start) || 0);
    return { start: baseStart + earliest, end: baseStart + Math.max(earliest, latest) };
  }

  function mergeWindows(windows, bridgeGap = 0) {
    const sorted = windows.filter(Boolean).slice().sort((a, b) => a.start - b.start);
    const merged = [];
    for (const item of sorted) {
      if (!merged.length || item.start > merged[merged.length - 1].end + bridgeGap) merged.push({ start: item.start, end: item.end });
      else merged[merged.length - 1].end = Math.max(merged[merged.length - 1].end, item.end);
    }
    return merged;
  }

  function makeMaster(context, destination) {
    const headroom = context.createGain();
    headroom.gain.value = 0.88;
    const limiter = context.createDynamicsCompressor();
    limiter.threshold.value = -2;
    limiter.knee.value = 0;
    limiter.ratio.value = 20;
    limiter.attack.value = 0.003;
    limiter.release.value = 0.08;
    headroom.connect(limiter).connect(destination);
    return headroom;
  }

  async function prepareMix({ stream = null, speaker = false } = {}) {
    const context = new AudioContext();
    if (context.state === 'running') {
      try { await context.suspend(); } catch (_) {}
    }
    const destination = speaker ? context.destination : context.createMediaStreamDestination();
    const master = makeMaster(context, destination);
    const clips = (A.voiceLab.state.clips || []).filter(c => !c.muted);
    const rawWindows = [];
    for (const clip of clips) rawWindows.push(await clipWindow(context, clip));
    const attack = Math.max(0.01, Number(A.dialogueEditor.state.attackMs) / 1000 || 0.08);
    const release = Math.max(0.05, Number(A.dialogueEditor.state.releaseMs) / 1000 || 0.3);
    const windows = mergeWindows(rawWindows, attack + release);
    const musicBuffer = A.audio?.track?.src ? await decode(context, A.audio.track.src) : null;
    const sources = [];
    let started = false;

    if (!speaker) {
      const audioTrack = destination.stream.getAudioTracks()[0];
      if (audioTrack && stream) stream.addTrack(audioTrack);
    }

    async function start() {
      if (started) return;
      started = true;
      const base = context.currentTime + 0.03;

      if (musicBuffer) {
        const source = context.createBufferSource();
        source.buffer = musicBuffer;
        const musicGain = context.createGain();
        musicGain.gain.setValueAtTime(1, base);
        const duck = dbToGain(-Math.max(0, Number(A.dialogueEditor.state.duckDb) || 0));
        for (const win of windows) {
          const startAt = base + win.start;
          const endAt = base + win.end;
          const attackStart = Math.max(base, startAt - attack);
          musicGain.gain.setValueAtTime(1, attackStart);
          musicGain.gain.linearRampToValueAtTime(duck, startAt);
          musicGain.gain.setValueAtTime(duck, endAt);
          musicGain.gain.linearRampToValueAtTime(1, endAt + release);
        }
        source.connect(musicGain).connect(master);
        source.start(base);
        sources.push(source);
      }

      for (const clip of clips) sources.push(...await A.dialogueEditor.scheduleEditedClip(context, master, clip, base));
      await context.resume();
    }

    function stop() {
      for (const source of sources) {
        try { source.stop(); } catch (_) {}
      }
    }

    return { context, sources, duckWindows: windows, start, stop };
  }

  function loadSafety() {
    if (A.audioSessionSafety || document.querySelector('script[data-c11-audio-safety]')) return;
    const script = document.createElement('script');
    script.src = './c11-audio-session-safety.js';
    script.setAttribute('data-c11-audio-safety', 'true');
    document.body.appendChild(script);
  }

  A.voiceLab.makeCombinedAudioTrack = (stream) => prepareMix({ stream, speaker: false });
  A.audioHardening = {
    clipWindow,
    mergeWindows,
    prepareMix,
    prepareSpeakerMix: () => prepareMix({ speaker: true })
  };
  A.status('Audio mix hardening loaded');
  loadSafety();
})();
