(() => {
  'use strict';
  const A = window.Animator;
  if (!A) throw new Error('C6 Voice Lab requires Animator');
  const $ = (id) => document.getElementById(id);
  const aside = document.querySelector('aside');
  if (!aside) return;

  const uid = (p) => A.uid ? A.uid(p) : `${p}-${Date.now()}-${Math.random().toString(36).slice(2)}`;
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, Number(v)));
  const dbToGain = (db) => Math.pow(10, Number(db) / 20);
  const bufferCache = new Map();
  let liveContext = null;
  let liveSources = [];

  const defaultRecipe = () => ({
    pitch: 0,
    highpass: 70,
    body: 0,
    presence: 1.5,
    compress: -18,
    drive: 0,
    delayMs: 0,
    delayMix: 0,
    reverb: 0
  });

  let state = {
    characters: [{ id: uid('voice'), name: 'GR', recipe: defaultRecipe() }],
    selectedCharacterId: null,
    clips: []
  };
  state.selectedCharacterId = state.characters[0].id;

  const pending = {
    name: 'Line 1', start: 0, layers: [null, null, null],
    settings: [
      { gain: 0, pan: 0, detune: 0, delayMs: 0 },
      { gain: -6, pan: 0, detune: -12, delayMs: 8 },
      { gain: -12, pan: 0, detune: 12, delayMs: 14 }
    ]
  };

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>C6 Voice Lab + Speech Timeline</strong><br>
    Build reusable character voices, combine up to three vocal layers, then place each finished line at an exact time on the video.
    <div style="margin-top:10px;display:flex;gap:6px;flex-wrap:wrap">
      <select id="voice-character"></select>
      <button id="voice-add-character" type="button">New Character</button>
      <button id="voice-rename-character" type="button">Rename</button>
    </div>
    <div class="control"><label><span>Pitch</span><span id="voice-pitch-v">0 cents</span></label><input id="voice-pitch" type="range" min="-1200" max="1200" step="25" value="0"></div>
    <div class="control"><label><span>Low cut</span><span id="voice-hp-v">70 Hz</span></label><input id="voice-hp" type="range" min="20" max="400" step="5" value="70"></div>
    <div class="control"><label><span>Body</span><span id="voice-body-v">0 dB</span></label><input id="voice-body" type="range" min="-12" max="12" step="0.5" value="0"></div>
    <div class="control"><label><span>Presence</span><span id="voice-pres-v">1.5 dB</span></label><input id="voice-pres" type="range" min="-12" max="12" step="0.5" value="1.5"></div>
    <div class="control"><label><span>Compression</span><span id="voice-comp-v">-18 dB</span></label><input id="voice-comp" type="range" min="-40" max="0" step="1" value="-18"></div>
    <div class="control"><label><span>Drive</span><span id="voice-drive-v">0%</span></label><input id="voice-drive" type="range" min="0" max="100" step="1" value="0"></div>
    <div class="control"><label><span>Echo</span><span id="voice-delay-v">0%</span></label><input id="voice-delay" type="range" min="0" max="60" step="1" value="0"></div>
    <div class="control"><label><span>Reverb</span><span id="voice-reverb-v">0%</span></label><input id="voice-reverb" type="range" min="0" max="60" step="1" value="0"></div>
    <hr style="border-color:#343741">
    <strong>Voice combiner — next line</strong>
    <div style="margin-top:8px"><label>Line name <input id="voice-line-name" value="Line 1" style="width:100%"></label></div>
    <div style="margin-top:8px"><label>Start on video (seconds) <input id="voice-line-start" type="number" min="0" step="0.01" value="0" style="width:100%"></label></div>
    <div id="voice-layer-controls"></div>
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:10px">
      <button id="voice-preview" type="button">Preview Combined Voice</button>
      <button id="voice-add-clip" type="button">Lay Speech On Video</button>
      <button id="voice-stop" type="button">Stop Audio</button>
    </div>
    <hr style="border-color:#343741">
    <strong>Speech timeline</strong>
    <div id="voice-timeline" style="margin-top:8px"></div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  const layersBox = $('voice-layer-controls');
  for (let i = 0; i < 3; i += 1) {
    const row = document.createElement('div');
    row.className = 'card';
    row.style.marginTop = '8px';
    row.innerHTML = `
      <strong>Layer ${i + 1}</strong> <span id="voice-layer-${i}-name">empty</span><br>
      <input id="voice-layer-${i}-file" type="file" accept="audio/*">
      <label>Level <input id="voice-layer-${i}-gain" type="range" min="-36" max="12" step="1" value="${pending.settings[i].gain}"> <span id="voice-layer-${i}-gain-v">${pending.settings[i].gain} dB</span></label><br>
      <label>Pan <input id="voice-layer-${i}-pan" type="range" min="-1" max="1" step="0.05" value="${pending.settings[i].pan}"> <span id="voice-layer-${i}-pan-v">0</span></label><br>
      <label>Pitch offset <input id="voice-layer-${i}-detune" type="range" min="-600" max="600" step="10" value="${pending.settings[i].detune}"> <span id="voice-layer-${i}-detune-v">${pending.settings[i].detune} cents</span></label><br>
      <label>Delay <input id="voice-layer-${i}-delay" type="range" min="0" max="250" step="1" value="${pending.settings[i].delayMs}"> <span id="voice-layer-${i}-delay-v">${pending.settings[i].delayMs} ms</span></label>
    `;
    layersBox.appendChild(row);
  }

  function selectedCharacter() {
    return state.characters.find((c) => c.id === state.selectedCharacterId) || state.characters[0];
  }

  function renderCharacters() {
    const select = $('voice-character');
    select.innerHTML = '';
    state.characters.forEach((c) => {
      const option = document.createElement('option');
      option.value = c.id;
      option.textContent = c.name;
      option.selected = c.id === state.selectedCharacterId;
      select.appendChild(option);
    });
    syncRecipeUI();
  }

  function syncRecipeUI() {
    const r = selectedCharacter()?.recipe || defaultRecipe();
    const pairs = [
      ['voice-pitch', r.pitch, 'voice-pitch-v', `${r.pitch} cents`],
      ['voice-hp', r.highpass, 'voice-hp-v', `${r.highpass} Hz`],
      ['voice-body', r.body, 'voice-body-v', `${r.body} dB`],
      ['voice-pres', r.presence, 'voice-pres-v', `${r.presence} dB`],
      ['voice-comp', r.compress, 'voice-comp-v', `${r.compress} dB`],
      ['voice-drive', r.drive, 'voice-drive-v', `${r.drive}%`],
      ['voice-delay', r.delayMix, 'voice-delay-v', `${r.delayMix}%`],
      ['voice-reverb', r.reverb, 'voice-reverb-v', `${r.reverb}%`]
    ];
    pairs.forEach(([id, value, vid, text]) => { if ($(id)) $(id).value = value; if ($(vid)) $(vid).textContent = text; });
  }

  function updateRecipe(prop, value) {
    const c = selectedCharacter();
    if (!c) return;
    c.recipe[prop] = Number(value);
    syncRecipeUI();
  }

  const recipeBindings = [
    ['voice-pitch','pitch'],['voice-hp','highpass'],['voice-body','body'],['voice-pres','presence'],
    ['voice-comp','compress'],['voice-drive','drive'],['voice-delay','delayMix'],['voice-reverb','reverb']
  ];
  recipeBindings.forEach(([id, prop]) => $(id)?.addEventListener('input', e => updateRecipe(prop, e.target.value)));

  $('voice-character')?.addEventListener('change', e => { state.selectedCharacterId = e.target.value; syncRecipeUI(); renderTimeline(); });
  $('voice-add-character')?.addEventListener('click', () => {
    const name = prompt('Character voice name?', `Character ${state.characters.length + 1}`)?.trim();
    if (!name) return;
    const c = { id: uid('voice'), name, recipe: defaultRecipe() };
    state.characters.push(c); state.selectedCharacterId = c.id; renderCharacters();
  });
  $('voice-rename-character')?.addEventListener('click', () => {
    const c = selectedCharacter(); if (!c) return;
    const name = prompt('Rename character voice:', c.name)?.trim(); if (!name) return;
    c.name = name; renderCharacters(); renderTimeline();
  });

  for (let i = 0; i < 3; i += 1) {
    $(`voice-layer-${i}-file`)?.addEventListener('change', async (e) => {
      const file = e.target.files?.[0]; if (!file) return;
      pending.layers[i] = { name: file.name, type: file.type || 'audio', src: await A.readFile(file) };
      $(`voice-layer-${i}-name`).textContent = file.name;
    });
    for (const [suffix, key, unit] of [['gain','gain',' dB'],['pan','pan',''],['detune','detune',' cents'],['delay','delayMs',' ms']]) {
      $(`voice-layer-${i}-${suffix}`)?.addEventListener('input', (e) => {
        pending.settings[i][key] = Number(e.target.value);
        $(`voice-layer-${i}-${suffix}-v`).textContent = `${e.target.value}${unit}`;
      });
    }
  }

  function makeCurve(amount) {
    const n = 2048, curve = new Float32Array(n), k = clamp(amount, 0, 100) / 100 * 20;
    for (let i = 0; i < n; i += 1) {
      const x = i * 2 / (n - 1) - 1;
      curve[i] = k ? Math.tanh(x * (1 + k)) / Math.tanh(1 + k) : x;
    }
    return curve;
  }

  function makeImpulse(context, seconds = 0.55, decay = 2.2) {
    const length = Math.max(1, Math.floor(context.sampleRate * seconds));
    const impulse = context.createBuffer(2, length, context.sampleRate);
    for (let ch = 0; ch < 2; ch += 1) {
      const data = impulse.getChannelData(ch);
      for (let i = 0; i < length; i += 1) data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / length, decay);
    }
    return impulse;
  }

  async function decode(context, src) {
    if (!src) return null;
    const key = `${context.sampleRate}:${src}`;
    if (bufferCache.has(key)) return bufferCache.get(key);
    const arr = await (await fetch(src)).arrayBuffer();
    const buf = await context.decodeAudioData(arr.slice(0));
    bufferCache.set(key, buf);
    return buf;
  }

  function createVoiceBus(context, destination, recipe, masterGain = 1) {
    const input = context.createGain();
    const highpass = context.createBiquadFilter(); highpass.type = 'highpass'; highpass.frequency.value = clamp(recipe.highpass, 20, 600);
    const body = context.createBiquadFilter(); body.type = 'peaking'; body.frequency.value = 180; body.Q.value = 0.8; body.gain.value = clamp(recipe.body, -18, 18);
    const presence = context.createBiquadFilter(); presence.type = 'peaking'; presence.frequency.value = 3200; presence.Q.value = 0.9; presence.gain.value = clamp(recipe.presence, -18, 18);
    const shaper = context.createWaveShaper(); shaper.curve = makeCurve(recipe.drive); shaper.oversample = '2x';
    const compressor = context.createDynamicsCompressor(); compressor.threshold.value = clamp(recipe.compress, -60, 0); compressor.ratio.value = 3.5; compressor.attack.value = 0.006; compressor.release.value = 0.16;
    const dry = context.createGain(); dry.gain.value = masterGain;
    input.connect(highpass).connect(body).connect(presence).connect(shaper).connect(compressor);
    compressor.connect(dry).connect(destination);

    const delayMix = clamp(recipe.delayMix, 0, 100) / 100;
    if (delayMix > 0) {
      const delay = context.createDelay(1); delay.delayTime.value = Math.max(0.045, (Number(recipe.delayMs) || 110) / 1000);
      const feedback = context.createGain(); feedback.gain.value = 0.18;
      const wet = context.createGain(); wet.gain.value = delayMix * masterGain;
      compressor.connect(delay); delay.connect(feedback).connect(delay); delay.connect(wet).connect(destination);
    }

    const reverbMix = clamp(recipe.reverb, 0, 100) / 100;
    if (reverbMix > 0) {
      const convolver = context.createConvolver(); convolver.buffer = makeImpulse(context);
      const wet = context.createGain(); wet.gain.value = reverbMix * masterGain;
      compressor.connect(convolver).connect(wet).connect(destination);
    }
    return input;
  }

  async function scheduleClip(context, destination, clip, baseTime = 0) {
    if (clip.muted) return [];
    const character = state.characters.find(c => c.id === clip.characterId) || { recipe: defaultRecipe() };
    const recipe = character.recipe || defaultRecipe();
    const bus = createVoiceBus(context, destination, recipe, dbToGain(clip.gainDb || 0));
    const scheduled = [];
    for (let i = 0; i < clip.layers.length; i += 1) {
      const layer = clip.layers[i]; if (!layer?.src) continue;
      const setting = clip.settings[i] || { gain:0,pan:0,detune:0,delayMs:0 };
      const buffer = await decode(context, layer.src);
      const source = context.createBufferSource(); source.buffer = buffer;
      source.detune.value = clamp((recipe.pitch || 0) + (setting.detune || 0), -2400, 2400);
      const gain = context.createGain(); gain.gain.value = dbToGain(setting.gain || 0);
      const panner = context.createStereoPanner ? context.createStereoPanner() : null;
      if (panner) panner.pan.value = clamp(setting.pan || 0, -1, 1);
      source.connect(gain); if (panner) gain.connect(panner).connect(bus); else gain.connect(bus);
      source.start(baseTime + Math.max(0, Number(clip.start) || 0) + Math.max(0, Number(setting.delayMs) || 0) / 1000);
      scheduled.push(source);
    }
    return scheduled;
  }

  async function playClip(clip) {
    stopAudio();
    const context = new AudioContext(); liveContext = context;
    await context.resume();
    const preview = A.clone(clip); preview.start = 0;
    liveSources = await scheduleClip(context, context.destination, preview, context.currentTime + 0.03);
  }

  async function playTimeline() {
    stopAudio();
    const context = new AudioContext(); liveContext = context;
    await context.resume();
    liveSources = [];
    for (const clip of state.clips) liveSources.push(...await scheduleClip(context, context.destination, clip, context.currentTime + 0.03));
  }

  function stopAudio() {
    liveSources.forEach(s => { try { s.stop(); } catch (_) {} }); liveSources = [];
    if (liveContext) { try { liveContext.close(); } catch (_) {} liveContext = null; }
  }

  function buildPendingClip() {
    const layers = pending.layers.map(x => x ? A.clone(x) : null);
    if (!layers.some(Boolean)) throw new Error('Load at least one voice layer');
    return {
      id: uid('speech'),
      name: ($('voice-line-name')?.value || 'Line').trim() || 'Line',
      characterId: state.selectedCharacterId,
      start: Math.max(0, Number($('voice-line-start')?.value || 0)),
      gainDb: 0,
      muted: false,
      layers,
      settings: A.clone(pending.settings)
    };
  }

  function renderTimeline() {
    const box = $('voice-timeline'); box.innerHTML = '';
    const sorted = [...state.clips].sort((a,b) => a.start - b.start);
    if (!sorted.length) { box.textContent = 'No speech clips yet.'; return; }
    sorted.forEach((clip) => {
      const c = state.characters.find(x => x.id === clip.characterId);
      const row = document.createElement('div'); row.className = 'card'; row.style.marginBottom = '6px';
      row.innerHTML = `<strong>${c?.name || 'Voice'} — ${clip.name}</strong><br>
        <label>Start <input data-role="start" type="number" min="0" step="0.01" value="${clip.start}" style="width:80px"> s</label>
        <label> Gain <input data-role="gain" type="number" min="-36" max="18" step="1" value="${clip.gainDb || 0}" style="width:60px"> dB</label>
        <label><input data-role="mute" type="checkbox" ${clip.muted?'checked':''}> mute</label><br>
        <button data-role="preview" type="button">Preview</button>
        <button data-role="delete" type="button">Delete</button>`;
      row.querySelector('[data-role=start]').addEventListener('change', e => { clip.start = Math.max(0, Number(e.target.value)||0); renderTimeline(); });
      row.querySelector('[data-role=gain]').addEventListener('change', e => { clip.gainDb = clamp(e.target.value,-36,18); });
      row.querySelector('[data-role=mute]').addEventListener('change', e => { clip.muted = e.target.checked; });
      row.querySelector('[data-role=preview]').addEventListener('click', () => playClip(clip).catch(err => A.status(`Voice preview failed: ${err.message}`)));
      row.querySelector('[data-role=delete]').addEventListener('click', () => { state.clips = state.clips.filter(x => x.id !== clip.id); renderTimeline(); });
      box.appendChild(row);
    });
  }

  $('voice-preview')?.addEventListener('click', () => { try { playClip(buildPendingClip()).catch(err => A.status(`Voice preview failed: ${err.message}`)); } catch (e) { A.status(e.message); } });
  $('voice-add-clip')?.addEventListener('click', () => { try { const clip = buildPendingClip(); state.clips.push(clip); renderTimeline(); A.status(`Speech laid at ${clip.start.toFixed(2)}s`); } catch (e) { A.status(e.message); } });
  $('voice-stop')?.addEventListener('click', stopAudio);

  // Speech follows reel playback from video time zero.
  $('play-button')?.addEventListener('click', () => {
    if (A.playback?.playing) playTimeline().catch(err => A.status(`Speech playback failed: ${err.message}`)); else stopAudio();
  });

  async function makeCombinedAudioTrack(stream) {
    const context = new AudioContext();
    const destination = context.createMediaStreamDestination();
    const sources = [];
    await context.resume();

    // Existing B11 music/dialogue bed joins the same final mix bus.
    if (A.audio?.track?.src) {
      const musicBuffer = await decode(context, A.audio.track.src);
      const musicSource = context.createBufferSource(); musicSource.buffer = musicBuffer;
      const musicGain = context.createGain(); musicGain.gain.value = 1;
      musicSource.connect(musicGain).connect(destination); musicSource.start(context.currentTime + 0.03); sources.push(musicSource);
    }
    for (const clip of state.clips) sources.push(...await scheduleClip(context, destination, clip, context.currentTime + 0.03));
    const audioTrack = destination.stream.getAudioTracks()[0];
    if (audioTrack) stream.addTrack(audioTrack);
    return { context, sources, stop() { sources.forEach(s => { try { s.stop(); } catch (_) {} }); } };
  }

  function serialize() { return A.clone(state); }
  function loadState(next) {
    if (!next) return;
    state = A.clone(next);
    if (!Array.isArray(state.characters) || !state.characters.length) state.characters = [{ id: uid('voice'), name:'GR', recipe:defaultRecipe() }];
    if (!Array.isArray(state.clips)) state.clips = [];
    if (!state.selectedCharacterId || !state.characters.some(c => c.id === state.selectedCharacterId)) state.selectedCharacterId = state.characters[0].id;
    state.characters.forEach(c => { c.recipe = { ...defaultRecipe(), ...(c.recipe || {}) }; });
    renderCharacters(); renderTimeline();
  }

  A.voiceLab = { serialize, loadState, playTimeline, stopAudio, makeCombinedAudioTrack, scheduleClip, createVoiceBus, get state() { return state; } };
  renderCharacters(); renderTimeline();
})();
