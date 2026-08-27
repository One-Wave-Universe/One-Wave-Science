(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('C14 requires Animator + reel');
  const aside = document.querySelector('aside');
  if (!aside) return;
  const $ = (id) => document.getElementById(id);

  const FORMAT = 'one-wave-motion-library';
  const VERSION = 1;
  const clone = (x) => A.clone ? A.clone(x) : JSON.parse(JSON.stringify(x));
  let library = { format: FORMAT, version: VERSION, name: 'GR Core Motions', sequences: [] };

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>C14 Motion Library</strong><br>
    Store reusable animation sequences separately from the active scene.
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
      <button id="c14-new">New Library</button>
      <button id="c14-open">Open .owmotion</button>
      <button id="c14-save">Save .owmotion</button>
      <input id="c14-file" type="file" accept=".owmotion,.json,application/json" hidden>
    </div>
    <div style="margin-top:8px"><label>Library name <input id="c14-name" value="GR Core Motions" style="width:100%"></label></div>
    <div class="card" style="margin-top:8px">
      <strong>Capture reel range</strong><br>
      <label>Start frame <input id="c14-start" type="number" min="1" value="1" style="width:72px"></label>
      <label>End frame <input id="c14-end" type="number" min="1" value="1" style="width:72px"></label><br>
      <label>Sequence name <input id="c14-seq-name" value="Walk"></label><br>
      <label>Character tag <input id="c14-tag" value="GR"></label><br>
      <label><input id="c14-loop" type="checkbox"> Loop</label><br>
      <label>Notes <input id="c14-notes" value=""></label><br>
      <button id="c14-capture">Capture Range To Slot</button>
    </div>
    <div id="c14-slots"></div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  function normalizeLibrary(data) {
    if (!data || data.format !== FORMAT || Number(data.version) !== VERSION) throw new Error('Unsupported motion library');
    const sequences = Array.isArray(data.sequences) ? data.sequences.slice(0, 5) : [];
    return {
      format: FORMAT,
      version: VERSION,
      name: String(data.name || 'Motion Library').slice(0, 120),
      sequences: sequences.map((s, i) => ({
        id: String(s.id || `seq-${Date.now()}-${i}`),
        name: String(s.name || `Sequence ${i + 1}`).slice(0, 120),
        characterTag: String(s.characterTag || '').slice(0, 80),
        loop: Boolean(s.loop),
        notes: String(s.notes || '').slice(0, 500),
        fps: Math.max(1, Math.min(60, Number(s.fps) || 24)),
        frames: Array.isArray(s.frames) ? clone(s.frames) : []
      }))
    };
  }

  function renderSlots() {
    const box = $('c14-slots');
    box.innerHTML = '';
    for (let i = 0; i < 5; i += 1) {
      const seq = library.sequences[i] || null;
      const row = document.createElement('div');
      row.className = 'card';
      row.innerHTML = seq ? `
        <strong>Slot ${i + 1}: ${seq.name}</strong><br>
        ${seq.characterTag ? `Character: ${seq.characterTag}<br>` : ''}
        ${seq.frames.length} reel frame${seq.frames.length === 1 ? '' : 's'} @ ${seq.fps} fps — ${seq.loop ? 'loop' : 'one-shot'}<br>
        ${seq.notes ? `<small>${seq.notes}</small><br>` : ''}
        <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:6px">
          <button data-action="insert" data-i="${i}">Insert At Current</button>
          <button data-action="rename" data-i="${i}">Rename</button>
          <button data-action="delete" data-i="${i}">Delete</button>
        </div>
      ` : `<strong>Slot ${i + 1}: empty</strong>`;
      box.appendChild(row);
    }
    box.querySelectorAll('button[data-action]').forEach(btn => btn.addEventListener('click', onSlotAction));
  }

  function reelFps() {
    return Math.max(1, A.playback?.fps || Number($('fps-control')?.value || 24));
  }

  function captureRange() {
    R.captureCurrent();
    const start = Math.max(1, Number($('c14-start')?.value || 1));
    const end = Math.max(start, Number($('c14-end')?.value || start));
    const from = Math.min(R.frames.length - 1, start - 1);
    const to = Math.min(R.frames.length - 1, end - 1);
    const frames = clone(R.frames.slice(from, to + 1));
    if (!frames.length) return A.status('No reel frames in capture range');
    const sequence = {
      id: `seq-${Date.now()}-${Math.random().toString(36).slice(2)}`,
      name: String($('c14-seq-name')?.value || `Sequence ${library.sequences.length + 1}`).trim() || 'Sequence',
      characterTag: String($('c14-tag')?.value || '').trim(),
      loop: Boolean($('c14-loop')?.checked),
      notes: String($('c14-notes')?.value || '').trim(),
      fps: reelFps(),
      frames
    };
    if (library.sequences.length < 5) library.sequences.push(sequence);
    else library.sequences[4] = sequence;
    renderSlots();
    A.status(`${sequence.name} captured into Motion Library`);
  }

  function insertSequence(index) {
    const seq = library.sequences[index];
    if (!seq?.frames?.length) return;
    R.captureCurrent();
    const insertAt = Math.max(0, Math.min(R.frames.length, R.activeIndex + 1));
    const frames = clone(seq.frames);
    const next = [...R.frames.slice(0, insertAt), ...frames, ...R.frames.slice(insertAt)];
    R.setFrames(next, insertAt);
    A.status(`${seq.name} inserted at reel frame ${insertAt + 1}`);
  }

  function onSlotAction(event) {
    const i = Number(event.currentTarget.dataset.i);
    const action = event.currentTarget.dataset.action;
    if (action === 'insert') return insertSequence(i);
    if (action === 'delete') {
      library.sequences.splice(i, 1);
      renderSlots();
      return A.status('Motion sequence removed');
    }
    if (action === 'rename') {
      const seq = library.sequences[i];
      const name = prompt('Rename sequence:', seq.name)?.trim();
      if (name) { seq.name = name.slice(0, 120); renderSlots(); }
    }
  }

  function saveLibrary() {
    library.name = String($('c14-name')?.value || library.name).trim() || 'Motion Library';
    const blob = new Blob([JSON.stringify(library, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${library.name.replace(/[^a-z0-9_-]+/gi, '_')}.owmotion`;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 0);
    A.status('Motion Library saved');
  }

  function newLibrary() {
    library = { format: FORMAT, version: VERSION, name: 'GR Core Motions', sequences: [] };
    $('c14-name').value = library.name;
    renderSlots();
    A.status('New Motion Library');
  }

  $('c14-new')?.addEventListener('click', newLibrary);
  $('c14-open')?.addEventListener('click', () => $('c14-file')?.click());
  $('c14-save')?.addEventListener('click', saveLibrary);
  $('c14-capture')?.addEventListener('click', captureRange);
  $('c14-file')?.addEventListener('change', async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      library = normalizeLibrary(JSON.parse(await file.text()));
      $('c14-name').value = library.name;
      renderSlots();
      A.status(`Motion Library loaded: ${library.name}`);
    } catch (error) {
      console.error(error);
      A.status(`Motion Library load failed: ${error.message}`);
    } finally {
      event.target.value = '';
    }
  });

  function syncRangeLimits() {
    const n = Math.max(1, R.frames.length);
    $('c14-start').max = String(n);
    $('c14-end').max = String(n);
    if (Number($('c14-end').value) > n) $('c14-end').value = String(n);
  }

  const oldSetFrames = R.setFrames?.bind(R);
  if (oldSetFrames && !R._c14Wrapped) {
    R.setFrames = function(...args) {
      const result = oldSetFrames(...args);
      syncRangeLimits();
      return result;
    };
    R._c14Wrapped = true;
  }

  A.motionLibrary = {
    get library() { return clone(library); },
    captureRange,
    insertSequence,
    saveLibrary,
    normalizeLibrary,
    setLibrary(next) { library = normalizeLibrary(next); $('c14-name').value = library.name; renderSlots(); }
  };
  syncRangeLimits();
  renderSlots();
})();
