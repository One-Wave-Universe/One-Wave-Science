(() => {
  'use strict';
  const A = window.Animator;
  if (!A?.voiceLab) throw new Error('C7 requires C6 Voice Lab');
  const aside = document.querySelector('aside');
  const $ = (id) => document.getElementById(id);
  if (!aside) return;
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, Number(v)));
  const dbToGain = (db) => Math.pow(10, Number(db) / 20);
  const cache = new Map();

  const state = { duckDb: 9, attackMs: 80, releaseMs: 300 };

  function ensureClip(clip) {
    if (!Number.isFinite(Number(clip.trimStart))) clip.trimStart = 0;
    if (!Number.isFinite(Number(clip.trimEnd))) clip.trimEnd = 0;
    if (!Number.isFinite(Number(clip.fadeIn))) clip.fadeIn = 0.02;
    if (!Number.isFinite(Number(clip.fadeOut))) clip.fadeOut = 0.04;
    if (!Number.isFinite(Number(clip.gainDb))) clip.gainDb = 0;
    return clip;
  }

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>C7 Dialogue Editor</strong><br>
    Non-destructive speech finishing after Voice Lab: trim, fades, clip gain, and music duck settings are applied to the final exported mix.
    <div class="control"><label><span>Music duck</span><span id="c7-duck-v">9 dB</span></label><input id="c7-duck" type="range" min="0" max="24" step="1" value="9"></div>
    <div class="control"><label><span>Duck attack</span><span id="c7-attack-v">80 ms</span></label><input id="c7-attack" type="range" min="10" max="500" step="10" value="80"></div>
    <div class="control"><label><span>Duck release</span><span id="c7-release-v">300 ms</span></label><input id="c7-release" type="range" min="50" max="1500" step="50" value="300"></div>
    <button id="c7-refresh" type="button">Refresh Dialogue Clips</button>
    <div id="c7-clips" style="margin-top:8px"></div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  function bindRange(id, out, key, suffix) {
    $(id)?.addEventListener('input', (e) => {
      state[key] = Number(e.target.value);
      if ($(out)) $(out).textContent = `${e.target.value}${suffix}`;
    });
  }
  bindRange('c7-duck', 'c7-duck-v', 'duckDb', ' dB');
  bindRange('c7-attack', 'c7-attack-v', 'attackMs', ' ms');
  bindRange('c7-release', 'c7-release-v', 'releaseMs', ' ms');

  async function decode(context, src) {
    const key = `${context.sampleRate}:${src}`;
    if (cache.has(key)) return cache.get(key);
    const bytes = await (await fetch(src)).arrayBuffer();
    const buffer = await context.decodeAudioData(bytes.slice(0));
    cache.set(key, buffer);
    return buffer;
  }

  async function getClipDuration(context, clip) {
    ensureClip(clip);
    const layer = clip.layers?.find(x => x?.src);
    if (!layer) return 0;
    const buffer = await decode(context, layer.src);
    return Math.max(0, buffer.duration - clip.trimStart - clip.trimEnd);
  }

  async function scheduleEditedClip(context, destination, clip, baseTime) {
    ensureClip(clip);
    if (clip.muted) return [];
    const character = A.voiceLab.state.characters.find(c => c.id === clip.characterId);
    const recipe = character?.recipe || { pitch:0, highpass:70, body:0, presence:0, compress:-18, drive:0, delayMix:0, reverb:0 };
    const bus = A.voiceLab.createVoiceBus(context, destination, recipe, dbToGain(clip.gainDb));
    const scheduled = [];
    const clipStart = baseTime + Math.max(0, Number(clip.start) || 0);

    for (let i = 0; i < (clip.layers || []).length; i += 1) {
      const layer = clip.layers[i];
      if (!layer?.src) continue;
      const setting = clip.settings?.[i] || { gain:0, pan:0, detune:0, delayMs:0 };
      const buffer = await decode(context, layer.src);
      const offset = Math.min(buffer.duration, Math.max(0, Number(clip.trimStart) || 0));
      const available = Math.max(0, buffer.duration - offset - Math.max(0, Number(clip.trimEnd) || 0));
      if (!available) continue;

      const source = context.createBufferSource();
      source.buffer = buffer;
      source.detune.value = clamp((Number(recipe.pitch) || 0) + (Number(setting.detune) || 0), -2400, 2400);
      const gain = context.createGain();
      const level = dbToGain(Number(setting.gain) || 0);
      const when = clipStart + Math.max(0, Number(setting.delayMs) || 0) / 1000;
      const fadeIn = Math.min(available / 2, Math.max(0, Number(clip.fadeIn) || 0));
      const fadeOut = Math.min(available / 2, Math.max(0, Number(clip.fadeOut) || 0));
      gain.gain.setValueAtTime(fadeIn ? 0 : level, when);
      if (fadeIn) gain.gain.linearRampToValueAtTime(level, when + fadeIn);
      if (fadeOut) {
        gain.gain.setValueAtTime(level, Math.max(when + fadeIn, when + available - fadeOut));
        gain.gain.linearRampToValueAtTime(0, when + available);
      }
      const panner = context.createStereoPanner ? context.createStereoPanner() : null;
      if (panner) panner.pan.value = clamp(Number(setting.pan) || 0, -1, 1);
      source.connect(gain);
      if (panner) gain.connect(panner).connect(bus); else gain.connect(bus);
      source.start(when, offset, available);
      scheduled.push(source);
    }
    return scheduled;
  }

  async function makeFinalMix(stream) {
    const context = new AudioContext();
    const destination = context.createMediaStreamDestination();
    const sources = [];
    await context.resume();
    const base = context.currentTime + 0.03;

    if (A.audio?.track?.src) {
      const buffer = await decode(context, A.audio.track.src);
      const source = context.createBufferSource();
      source.buffer = buffer;
      const musicGain = context.createGain();
      musicGain.gain.setValueAtTime(1, base);
      const duckGain = dbToGain(-Math.max(0, state.duckDb));
      const attack = Math.max(0.01, state.attackMs / 1000);
      const release = Math.max(0.05, state.releaseMs / 1000);
      const clips = (A.voiceLab.state.clips || []).filter(c => !c.muted).slice().sort((a,b) => Number(a.start) - Number(b.start));
      for (const clip of clips) {
        const duration = await getClipDuration(context, clip);
        if (!duration) continue;
        const start = base + Math.max(0, Number(clip.start) || 0);
        const end = start + duration;
        musicGain.gain.setValueAtTime(1, Math.max(base, start - attack));
        musicGain.gain.linearRampToValueAtTime(duckGain, start);
        musicGain.gain.setValueAtTime(duckGain, end);
        musicGain.gain.linearRampToValueAtTime(1, end + release);
      }
      source.connect(musicGain).connect(destination);
      source.start(base);
      sources.push(source);
    }

    for (const clip of A.voiceLab.state.clips || []) {
      sources.push(...await scheduleEditedClip(context, destination, clip, base));
    }

    const audioTrack = destination.stream.getAudioTracks()[0];
    if (audioTrack) stream.addTrack(audioTrack);
    return {
      context,
      sources,
      stop() { sources.forEach(source => { try { source.stop(); } catch (_) {} }); }
    };
  }

  function render() {
    const box = $('c7-clips');
    box.innerHTML = '';
    const clips = A.voiceLab.state.clips || [];
    if (!clips.length) {
      box.textContent = 'No dialogue clips yet.';
      return;
    }
    clips.slice().sort((a,b) => Number(a.start) - Number(b.start)).forEach((clip) => {
      ensureClip(clip);
      const row = document.createElement('div');
      row.className = 'card';
      row.innerHTML = `
        <strong>${clip.name}</strong><br>
        <label>Start <input data-k="start" type="number" min="0" step="0.01" value="${clip.start}" style="width:72px"> s</label><br>
        <label>Trim in <input data-k="trimStart" type="number" min="0" step="0.01" value="${clip.trimStart}" style="width:72px"> s</label><br>
        <label>Trim out <input data-k="trimEnd" type="number" min="0" step="0.01" value="${clip.trimEnd}" style="width:72px"> s</label><br>
        <label>Fade in <input data-k="fadeIn" type="number" min="0" step="0.01" value="${clip.fadeIn}" style="width:72px"> s</label><br>
        <label>Fade out <input data-k="fadeOut" type="number" min="0" step="0.01" value="${clip.fadeOut}" style="width:72px"> s</label><br>
        <label>Clip gain <input data-k="gainDb" type="number" min="-36" max="18" step="1" value="${clip.gainDb}" style="width:72px"> dB</label>
      `;
      row.querySelectorAll('input[data-k]').forEach((input) => {
        input.addEventListener('change', (e) => {
          const key = e.target.dataset.k;
          let value = Number(e.target.value) || 0;
          if (['start','trimStart','trimEnd','fadeIn','fadeOut'].includes(key)) value = Math.max(0, value);
          if (key === 'gainDb') value = clamp(value, -36, 18);
          clip[key] = value;
          A.status(`Dialogue ${key} updated`);
        });
      });
      box.appendChild(row);
    });
  }

  $('c7-refresh')?.addEventListener('click', render);

  function serialize() { return { ...state }; }
  function loadState(next) {
    if (!next) return;
    if (Number.isFinite(Number(next.duckDb))) state.duckDb = Number(next.duckDb);
    if (Number.isFinite(Number(next.attackMs))) state.attackMs = Number(next.attackMs);
    if (Number.isFinite(Number(next.releaseMs))) state.releaseMs = Number(next.releaseMs);
    if ($('c7-duck')) $('c7-duck').value = String(state.duckDb);
    if ($('c7-attack')) $('c7-attack').value = String(state.attackMs);
    if ($('c7-release')) $('c7-release').value = String(state.releaseMs);
    if ($('c7-duck-v')) $('c7-duck-v').textContent = `${state.duckDb} dB`;
    if ($('c7-attack-v')) $('c7-attack-v').textContent = `${state.attackMs} ms`;
    if ($('c7-release-v')) $('c7-release-v').textContent = `${state.releaseMs} ms`;
    render();
  }

  A.voiceLab.makeCombinedAudioTrack = makeFinalMix;
  A.dialogueEditor = { state, ensureClip, render, serialize, loadState, makeFinalMix, scheduleEditedClip };
  render();
})();
