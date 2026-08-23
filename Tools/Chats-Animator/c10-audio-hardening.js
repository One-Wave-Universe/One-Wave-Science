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
      earliest = Math.min(earliest, delay);
      latest = Math.max(latest, delay + available);
    }
    if (!Number.isFinite(earliest) || !Number.isFinite(latest)) return null;
    const start = Math.max(0, Number(clip.start) || 0) + earliest;
    const end = Math.max(start, Math.max(0, Number(clip.start) || 0) + latest);
    return { start, end };
  }

  function mergeWindows(windows, bridgeGap = 0) {
    const sorted = windows.filter(Boolean).slice().sort((a, b) => a.start - b.start);
    const merged = [];
    for (const item of sorted) {
      if (!merged.length || item.start > merged[merged.length - 1].end + bridgeGap) {
        merged.push({ start: item.start, end: item.end });
      } else {
        merged[merged.length - 1].end = Math.max(merged[merged.length - 1].end, item.end);
      }
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

  async function makeHardenedMix(stream) {
    const context = new AudioContext();
    const destination = context.createMediaStreamDestination();
    const master = makeMaster(context, destination);
    const sources = [];
    await context.resume();
    const base = context.currentTime + 0.05;

    const clips = (A.voiceLab.state.clips || []).filter(c => !c.muted);
    const rawWindows = [];
    for (const clip of clips) rawWindows.push(await clipWindow(context, clip));

    const attack = Math.max(0.01, Number(A.dialogueEditor.state.attackMs) / 1000 || 0.08);
    const release = Math.max(0.05, Number(A.dialogueEditor.state.releaseMs) / 1000 || 0.3);
    // If speech gaps are shorter than the recovery envelope, keep music down instead of pumping.
    const windows = mergeWindows(rawWindows, attack + release);

    if (A.audio?.track?.src) {
      const buffer = await decode(context, A.audio.track.src);
      const source = context.createBufferSource();
      source.buffer = buffer;
      const musicGain = context.createGain();
      musicGain.gain.setValueAtTime(1, base);
      const duck = dbToGain(-Math.max(0, Number(A.dialogueEditor.state.duckDb) || 0));
      for (const win of windows) {
        const start = base + win.start;
        const end = base + win.end;
        const attackStart = Math.max(base, start - attack);
        musicGain.gain.setValueAtTime(1, attackStart);
        musicGain.gain.linearRampToValueAtTime(duck, start);
        musicGain.gain.setValueAtTime(duck, end);
        musicGain.gain.linearRampToValueAtTime(1, end + release);
      }
      source.connect(musicGain).connect(master);
      source.start(base);
      sources.push(source);
    }

    for (const clip of clips) {
      sources.push(...await A.dialogueEditor.scheduleEditedClip(context, master, clip, base));
    }

    const audioTrack = destination.stream.getAudioTracks()[0];
    if (audioTrack) stream.addTrack(audioTrack);
    return {
      context,
      sources,
      duckWindows: windows,
      stop() {
        for (const source of sources) {
          try { source.stop(); } catch (_) {}
        }
      }
    };
  }

  A.voiceLab.makeCombinedAudioTrack = makeHardenedMix;
  A.audioHardening = { clipWindow, mergeWindows, makeHardenedMix };
  A.status('Audio mix hardening loaded');
})();
