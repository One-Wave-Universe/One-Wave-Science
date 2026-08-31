(function () {
  'use strict';

  const LAYOUT_PRESETS = {
    '1large': [{ size: 'large' }],
    '2large': [{ size: 'large' }, { size: 'large' }],
    '2small': [{ size: 'small' }, { size: 'small' }],
    '3small': [{ size: 'small' }, { size: 'small' }, { size: 'small' }],
    '4small': [{ size: 'small' }, { size: 'small' }, { size: 'small' }, { size: 'small' }],
    '1large1small': [{ size: 'large' }, { size: 'small' }],
    '1large2small': [{ size: 'large' }, { size: 'small' }, { size: 'small' }],
  };
  let board = Board.build(LAYOUT_PRESETS['1large']);
  const circuit = new CircuitEngine.Circuit();
  const WIRE_COLORS = ['#2a6f4a', '#c94a4a', '#3f7fe0', '#d4af37', '#7a4a2a', '#a855f7'];

  const state = {
    board,
    parts: [],
    nextId: 1,
    tool: 'select',
    toolValue: {
      resistor: 220,
      capacitor: 100e-6,
      led: 'red',
      battery: 5,
      inductor: 10e-3,
      acsource: 5,
      acsourceFreq: 1,
      mtjsensor: 2.5,
      mtjsensorFreq: 1,
      wireGauge: 'standard',
      potentiometer: 10000,
      wireColor: WIRE_COLORS[0],
      toroidSections: 1,
      toroidCore: 'medium',
      toroidGauge: 'standard',
      toroidSpacing: 'normal',
      toroidTurns: [10, 10, 10],
    },
    pending: [],
    hoverHole: null,
    hoverPart: null,
    selectedPartId: null,
    lastResult: { voltages: new Map(), currents: new Map(), warnings: [], uf: null },
    animT: 0,
    wireColorIdx: 0,
    scopeColorIdx: 0,
    draggingPot: null,
  };
  const SCOPE_WINDOW = 3; // seconds of history each probe trace keeps

  // boardIdx defaults to 0 (the primary/first board) -- row+col alone is
  // ambiguous once more than one board is on the workspace, since every
  // board has its own row 'a'/col 5/etc.
  function H(row, col, boardIdx) {
    const bi = boardIdx == null ? 0 : boardIdx;
    return board.holes.find((h) => h.row === row && h.col === col && h.boardIdx === bi);
  }

  // A real 6-pin trimmer straddles the center channel: 3 pins in one strip
  // row, 3 mirrored pins in the corresponding row of the other bank (a<->f,
  // b<->g, c<->h, d<->i, e<->j — always exactly 5 rows apart). Clicking one
  // anchor hole places all 6; rails have no mirror row and are rejected.
  const POT_MIRROR_ROW = { a: 'f', b: 'g', c: 'h', d: 'i', e: 'j', f: 'a', g: 'b', h: 'c', i: 'd', j: 'e' };
  function derivePotentiometerHoles(anchor) {
    const mirrorRow = POT_MIRROR_ROW[anchor.row];
    if (!mirrorRow) return null;
    const c = anchor.col;
    const bi = anchor.boardIdx || 0;
    const boardMeta = board.boards[bi];
    if (!boardMeta || c + 2 > boardMeta.cols) return null;
    return [
      H(anchor.row, c, bi), H(anchor.row, c + 1, bi), H(anchor.row, c + 2, bi),
      H(mirrorRow, c, bi), H(mirrorRow, c + 1, bi), H(mirrorRow, c + 2, bi),
    ];
  }

  function newId(prefix) {
    return prefix + (state.nextId++);
  }

  function addPart(part) {
    part.id = newId(part.type[0]);
    state.parts.push(part);
    return part;
  }

  // generator: derive each winding's real self-inductance (from turns and
  // core A_L) and DC winding resistance (from turns, wire gauge, and the
  // core's mean turn length) -- the electrical consequences of the part's
  // user-facing dropdowns, computed once per solve rather than baked in
  // at placement time so editing them later (Inspector) takes effect live.
  function toroidWindings(p) {
    const coreDef = Components.TOROID_CORES[p.core] || Components.TOROID_CORES.medium;
    const ohmsPerM = Components.WIRE_GAUGE_OHMS_PER_M[p.gauge] || Components.WIRE_GAUGE_OHMS_PER_M.standard;
    return p.turnsPerSection.map((turns, i) => ({
      a: p.terminals[i * 2].cellId,
      b: p.terminals[i * 2 + 1].cellId,
      L: coreDef.al * turns * turns,
      R: turns * coreDef.meanTurnLen * ohmsPerM,
    }));
  }

  function toEngineElements() {
    const wires = [];
    const components = [];
    state.parts.forEach((p) => {
      if (p.type === 'scope') {
        // a zero-load voltage tap -- never enters the circuit physics
      } else if (p.type === 'wire') {
        wires.push({ a: p.terminals[0].cellId, b: p.terminals[1].cellId });
      } else if (p.type === 'ywire') {
        // each end's fork, plus the run joining the two forks — 3 zero-
        // resistance ties chain all 4 holes into one electrical node
        const t = p.terminals;
        wires.push({ a: t[0].cellId, b: t[1].cellId });
        wires.push({ a: t[0].cellId, b: t[2].cellId });
        wires.push({ a: t[2].cellId, b: t[3].cellId });
      } else if (p.type === 'potentiometer') {
        const t = p.terminals;
        if (t.length === 6) {
          // the far row's 3 pins are wired internally to the near row's —
          // model that as ordinary jumpers rather than touching circuit.js
          wires.push({ a: t[0].cellId, b: t[3].cellId });
          wires.push({ a: t[1].cellId, b: t[4].cellId });
          wires.push({ a: t[2].cellId, b: t[5].cellId });
        }
        components.push({
          id: p.id, type: 'potentiometer', label: p.id,
          a: t[0].cellId, wiper: t[1].cellId, b: t[2].cellId,
          value: p.value, pos: p.pos,
        });
      } else if (p.type === 'vgnd') {
        components.push({
          id: p.id, type: 'vgnd', label: p.id,
          a: p.terminals[0].cellId, b: p.terminals[1].cellId, out: p.terminals[2].cellId,
        });
      } else if (p.type === 'acsource') {
        components.push({
          id: p.id, type: 'acsource', label: p.id,
          a: p.terminals[0].cellId, b: p.terminals[1].cellId,
          value: p.value, freq: p.freq, phase: p.phase,
        });
      } else if (p.type === 'mtjsensor') {
        components.push({
          id: p.id, type: 'mtjsensor', label: p.id,
          ref: p.terminals[0].cellId, sin: p.terminals[1].cellId, cos: p.terminals[2].cellId,
          value: p.value, freq: p.freq, phase: p.phase,
        });
      } else if (p.type === 'toroid') {
        components.push({
          id: p.id, type: 'toroid', label: p.id,
          windings: toroidWindings(p),
          coupling: p.turnsPerSection.length > 1 ? (Components.TOROID_SPACING_COUPLING[p.spacing] || 0.9) : 0,
        });
      } else {
        components.push({
          id: p.id, type: p.type, label: p.id,
          a: p.terminals[0].cellId, b: p.terminals[1].cellId,
          value: p.value, color: p.color, closed: p.closed,
        });
      }
    });
    return { wires, components };
  }

  // ---------------- canvas setup ----------------
  const canvas = document.getElementById('boardCanvas');
  const ctx = canvas.getContext('2d');
  function setupCanvas() {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = board.width * dpr;
    canvas.height = board.height * dpr;
    canvas.style.width = board.width + 'px';
    canvas.style.height = board.height + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  setupCanvas();

  function mousePos(evt) {
    const r = canvas.getBoundingClientRect();
    return { x: evt.clientX - r.left, y: evt.clientY - r.top };
  }

  // ---------------- toolbox ----------------
  const toolboxEl = document.getElementById('toolbox');
  Components.PALETTE.forEach((p) => {
    const btn = document.createElement('button');
    btn.className = 'tool-btn';
    btn.dataset.tool = p.type;
    btn.innerHTML = `<span class="tool-icon">${p.icon}</span><span>${p.label}</span>`;
    btn.addEventListener('click', () => selectTool(p.type));
    toolboxEl.appendChild(btn);
  });
  const selectBtn = document.createElement('button');
  selectBtn.className = 'tool-btn active';
  selectBtn.dataset.tool = 'select';
  selectBtn.innerHTML = `<span class="tool-icon">☞</span><span>Select / Toggle</span>`;
  selectBtn.addEventListener('click', () => selectTool('select'));
  toolboxEl.insertBefore(selectBtn, toolboxEl.firstChild);

  function selectTool(tool) {
    state.tool = tool;
    state.pending = [];
    state.selectedPartId = null;
    [...toolboxEl.children].forEach((b) => b.classList.toggle('active', b.dataset.tool === tool));
    renderToolOptions();
    renderProps();
  }

  // presentation: a framed square preview of a part -- same body a placed
  // part would draw -- with its name in block letters above it. Shown both
  // while still choosing a tool's options (pre-placement) and once a part
  // is selected in the Inspector, so the picture never disappears while
  // the dropdowns underneath it change.
  function buildPreviewCard(type, previewPart) {
    const def = Components.PALETTE.find((pp) => pp.type === type);
    const card = document.createElement('div');
    card.className = 'part-card';
    const name = document.createElement('div');
    name.className = 'part-card-name';
    name.textContent = (def ? def.label : type).toUpperCase();
    card.appendChild(name);
    const frame = document.createElement('div');
    frame.className = 'part-card-frame';
    const canvas = document.createElement('canvas');
    canvas.width = 150;
    canvas.height = 108;
    frame.appendChild(canvas);
    card.appendChild(frame);
    Components.drawPartIcon(canvas.getContext('2d'), type, previewPart, canvas.width, canvas.height);
    return card;
  }

  // generator: a plausible part-shaped object for the icon to draw, built
  // from whatever's currently selected in the tool options
  function toolPreviewPart(tool) {
    const tv = state.toolValue;
    switch (tool) {
      case 'resistor': return { value: tv.resistor };
      case 'capacitor': return { value: tv.capacitor };
      case 'led': return { color: tv.led };
      case 'battery': return { value: tv.battery };
      case 'inductor': return { value: tv.inductor };
      case 'acsource': return { value: tv.acsource, freq: tv.acsourceFreq };
      case 'mtjsensor': return { value: tv.mtjsensor, freq: tv.mtjsensorFreq };
      case 'potentiometer': return { value: tv.potentiometer, pos: 0.5 };
      case 'wire': case 'ywire': return { color: tv.wireColor, style: 'loop', gauge: tv.wireGauge };
      case 'toroid': return { turnsPerSection: tv.toroidTurns.slice(0, tv.toroidSections), core: tv.toroidCore, spacing: tv.toroidSpacing };
      default: return {};
    }
  }

  const toolOptionsEl = document.getElementById('toolOptions');
  function renderToolOptions() {
    toolOptionsEl.innerHTML = '';
    if (state.tool === 'select') return;
    toolOptionsEl.appendChild(buildPreviewCard(state.tool, toolPreviewPart(state.tool)));

    if (state.tool === 'resistor') {
      toolOptionsEl.appendChild(makeSelect('Value', Components.RESISTOR_VALUES.map((v) => [v, Components.formatOhms(v)]), state.toolValue.resistor, (v) => { state.toolValue.resistor = Number(v); renderToolOptions(); }));
    } else if (state.tool === 'capacitor') {
      toolOptionsEl.appendChild(makeSelect('Value', Components.CAPACITOR_VALUES.map((v) => [v.farads, v.label]), state.toolValue.capacitor, (v) => { state.toolValue.capacitor = Number(v); renderToolOptions(); }));
    } else if (state.tool === 'led') {
      toolOptionsEl.appendChild(makeSelect('Color', Components.LED_COLORS.map((c) => [c, c[0].toUpperCase() + c.slice(1)]), state.toolValue.led, (v) => { state.toolValue.led = v; renderToolOptions(); }));
    } else if (state.tool === 'battery') {
      toolOptionsEl.appendChild(makeSelect('Voltage', Components.BATTERY_VALUES.map((v) => [v, v + ' V']), state.toolValue.battery, (v) => { state.toolValue.battery = Number(v); renderToolOptions(); }));
    } else if (state.tool === 'inductor') {
      toolOptionsEl.appendChild(makeSelect('Inductance', Components.INDUCTOR_VALUES.map((v) => [v, Components.formatHenries(v)]), state.toolValue.inductor, (v) => { state.toolValue.inductor = Number(v); renderToolOptions(); }));
    } else if (state.tool === 'acsource') {
      toolOptionsEl.appendChild(makeSelect('Amplitude', Components.BATTERY_VALUES.map((v) => [v, v + ' Vpk']), state.toolValue.acsource, (v) => { state.toolValue.acsource = Number(v); renderToolOptions(); }));
      toolOptionsEl.appendChild(makeSelect('Frequency', Components.AC_FREQ_VALUES.map((v) => [v, v + ' Hz']), state.toolValue.acsourceFreq, (v) => { state.toolValue.acsourceFreq = Number(v); renderToolOptions(); }));
    } else if (state.tool === 'mtjsensor') {
      toolOptionsEl.appendChild(makeSelect('Amplitude', Components.BATTERY_VALUES.map((v) => [v, v + ' Vpk']), state.toolValue.mtjsensor, (v) => { state.toolValue.mtjsensor = Number(v); renderToolOptions(); }));
      toolOptionsEl.appendChild(makeSelect('Rotation', Components.AC_FREQ_VALUES.map((v) => [v, v + ' Hz']), state.toolValue.mtjsensorFreq, (v) => { state.toolValue.mtjsensorFreq = Number(v); renderToolOptions(); }));
    } else if (state.tool === 'potentiometer') {
      toolOptionsEl.appendChild(makeSelect('Resistance', Components.RESISTOR_VALUES.map((v) => [v, Components.formatOhms(v)]), state.toolValue.potentiometer, (v) => { state.toolValue.potentiometer = Number(v); renderToolOptions(); }));
    } else if (state.tool === 'wire' || state.tool === 'ywire') {
      toolOptionsEl.appendChild(makeSelect('Color', Components.WIRE_COLOR_CHOICES.map((c) => [c, Components.WIRE_COLOR_NAMES[c] || c]), state.toolValue.wireColor, (v) => { state.toolValue.wireColor = v; renderToolOptions(); }));
      toolOptionsEl.appendChild(makeSelect('Gauge', Object.entries(Components.WIRE_GAUGES).map(([k, v]) => [k, v]), state.toolValue.wireGauge, (v) => { state.toolValue.wireGauge = v; renderToolOptions(); }));
    } else if (state.tool === 'toroid') {
      const tv = state.toolValue;
      toolOptionsEl.appendChild(makeSelect('Core', Object.entries(Components.TOROID_CORES).map(([k, v]) => [k, v.label]), tv.toroidCore, (v) => { tv.toroidCore = v; renderToolOptions(); }));
      toolOptionsEl.appendChild(makeSelect('Wire gauge', Object.entries(Components.WIRE_GAUGES).map(([k, v]) => [k, v]), tv.toroidGauge, (v) => { tv.toroidGauge = v; renderToolOptions(); }));
      toolOptionsEl.appendChild(makeSelect('Sections', [1, 2, 3].map((n) => [n, n]), tv.toroidSections, (v) => { tv.toroidSections = Number(v); renderToolOptions(); }));
      for (let s = 0; s < tv.toroidSections; s++) {
        toolOptionsEl.appendChild(makeSelect('Turns (section ' + (s + 1) + ')', Components.TOROID_TURNS_VALUES.map((n) => [n, n]), tv.toroidTurns[s], (v) => { tv.toroidTurns[s] = Number(v); renderToolOptions(); }));
      }
      if (tv.toroidSections > 1) {
        toolOptionsEl.appendChild(makeSelect('Winding spacing', Object.keys(Components.TOROID_SPACING_COUPLING).map((k) => [k, k[0].toUpperCase() + k.slice(1)]), tv.toroidSpacing, (v) => { tv.toroidSpacing = v; renderToolOptions(); }));
      }
    }
    updateToolboxScrollHint();
  }

  // an OS/browser overlay scrollbar takes no layout space and only fades in
  // on hover, giving no hint that a tool's own options (e.g. the toroid's
  // Core/gauge/Sections/Turns/spacing, 5 controls deep) extend below the
  // sidebar's fold -- so drive the "scroll for more" hint from real
  // scroll-position math instead of relying on the scrollbar being visible.
  const toolboxAsideEl = document.querySelector('aside.toolbox');
  const toolboxScrollHintEl = document.getElementById('toolboxScrollHint');
  function updateToolboxScrollHint() {
    if (!toolboxAsideEl || !toolboxScrollHintEl) return;
    const scrollable = toolboxAsideEl.scrollHeight > toolboxAsideEl.clientHeight + 2;
    const atBottom = toolboxAsideEl.scrollTop + toolboxAsideEl.clientHeight >= toolboxAsideEl.scrollHeight - 2;
    toolboxScrollHintEl.hidden = !scrollable || atBottom;
  }
  toolboxAsideEl.addEventListener('scroll', updateToolboxScrollHint);
  window.addEventListener('resize', updateToolboxScrollHint);
  function labeled(text, el) {
    const wrap = document.createElement('label');
    wrap.className = 'field';
    const span = document.createElement('span');
    span.textContent = text;
    wrap.appendChild(span);
    wrap.appendChild(el);
    return wrap;
  }
  function makeSelect(label, options, value, onChange) {
    const sel = document.createElement('select');
    options.forEach(([v, text]) => {
      const opt = document.createElement('option');
      opt.value = v;
      opt.textContent = text;
      if (String(v) === String(value)) opt.selected = true;
      sel.appendChild(opt);
    });
    sel.addEventListener('change', () => onChange(sel.value));
    return labeled(label, sel);
  }
  renderToolOptions();

  // the palette's own friendly label (e.g. "Y-Split Wire") beats capitalizing
  // the raw type name (which would read as "Ywire")
  function partTitle(part) {
    const def = Components.PALETTE.find((p) => p.type === part.type);
    const label = def ? def.label : part.type[0].toUpperCase() + part.type.slice(1);
    return label + ' · ' + part.id;
  }

  // ---------------- placing / interacting ----------------
  function cancelPending() {
    state.pending = [];
  }

  function terminalsNeeded(type) {
    // a toroid's terminal count depends on how many winding sections were
    // chosen in the tool options (2 per section) -- not a fixed PALETTE value
    if (type === 'toroid') return state.toolValue.toroidSections * 2;
    const def = Components.PALETTE.find((p) => p.type === type);
    return def ? def.terminals : 2;
  }

  // generator: given a tool + the holes clicked, decide what the resulting
  // part looks like. Pure — no state mutation, easy to test/reason about on
  // its own. Wire color selection is the one stateful exception (a counter
  // for cosmetic color-cycling), so the caller resolves it and passes it in.
  function buildPart(type, holes, opts) {
    if (type === 'wire') return { type: 'wire', terminals: holes.slice(0, 2), color: opts.wireColor, style: 'loop', gauge: opts.wireGauge };
    if (type === 'ywire') return { type: 'ywire', terminals: holes.slice(0, 4), color: opts.wireColor, style: 'loop', gauge: opts.wireGauge };
    if (type === 'resistor') return { type: 'resistor', terminals: holes.slice(0, 2), value: opts.resistorValue };
    if (type === 'led') return { type: 'led', terminals: holes.slice(0, 2), color: opts.ledColor };
    if (type === 'diode') return { type: 'diode', terminals: holes.slice(0, 2) };
    if (type === 'capacitor') return { type: 'capacitor', terminals: holes.slice(0, 2), value: opts.capacitorValue };
    if (type === 'battery') return { type: 'battery', terminals: holes.slice(0, 2), value: opts.batteryValue };
    if (type === 'switch') return { type: 'switch', terminals: holes.slice(0, 2), closed: false };
    if (type === 'pushbutton') return { type: 'pushbutton', terminals: holes.slice(0, 2), closed: false };
    if (type === 'potentiometer') {
      const terminals = derivePotentiometerHoles(holes[0]);
      if (!terminals) return null;
      return { type: 'potentiometer', terminals, value: opts.potValue, pos: 0.5 };
    }
    if (type === 'vgnd') return { type: 'vgnd', terminals: holes.slice(0, 3) };
    if (type === 'inductor') return { type: 'inductor', terminals: holes.slice(0, 2), value: opts.inductorValue };
    if (type === 'acsource') return { type: 'acsource', terminals: holes.slice(0, 2), value: opts.acValue, freq: opts.acFreq, phase: 0 };
    if (type === 'mtjsensor') return { type: 'mtjsensor', terminals: holes.slice(0, 3), value: opts.mtjValue, freq: opts.mtjFreq, phase: 0 };
    if (type === 'scope') return { type: 'scope', terminals: holes.slice(0, 1), color: opts.scopeColor, samples: [] };
    if (type === 'toroid') {
      const sections = opts.toroidSections;
      return {
        type: 'toroid', terminals: holes.slice(0, sections * 2),
        turnsPerSection: opts.toroidTurns.slice(0, sections),
        core: opts.toroidCore, gauge: opts.toroidGauge, spacing: opts.toroidSpacing,
      };
    }
    return null;
  }

  // executor: picks the next cosmetic wire color (the one bit of state this
  // path needs) and commits the generated part into the board.
  function nextWireColor() {
    return WIRE_COLORS[state.wireColorIdx++ % WIRE_COLORS.length];
  }
  function nextScopeColor() {
    return Components.SCOPE_COLORS[state.scopeColorIdx++ % Components.SCOPE_COLORS.length];
  }

  function commitPart(type, holes) {
    const part = buildPart(type, holes, {
      resistorValue: state.toolValue.resistor,
      capacitorValue: state.toolValue.capacitor,
      ledColor: state.toolValue.led,
      batteryValue: state.toolValue.battery,
      inductorValue: state.toolValue.inductor,
      acValue: state.toolValue.acsource,
      acFreq: state.toolValue.acsourceFreq,
      mtjValue: state.toolValue.mtjsensor,
      mtjFreq: state.toolValue.mtjsensorFreq,
      potValue: state.toolValue.potentiometer,
      wireColor: type === 'wire' || type === 'ywire' ? state.toolValue.wireColor : undefined,
      wireGauge: state.toolValue.wireGauge,
      scopeColor: type === 'scope' ? nextScopeColor() : undefined,
      toroidSections: state.toolValue.toroidSections,
      toroidTurns: state.toolValue.toroidTurns,
      toroidCore: state.toolValue.toroidCore,
      toroidGauge: state.toolValue.toroidGauge,
      toroidSpacing: state.toolValue.toroidSpacing,
    });
    if (part) addPart(part);
  }

  // distance from a point to the nearest point on a line segment — lets
  // hovering/clicking register anywhere along a part's drawn body, not just
  // near its exact midpoint
  function distToSegment(px, py, x1, y1, x2, y2) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const lenSq = dx * dx + dy * dy;
    let t = lenSq ? ((px - x1) * dx + (py - y1) * dy) / lenSq : 0;
    t = Math.max(0, Math.min(1, t));
    return Math.hypot(px - (x1 + t * dx), py - (y1 + t * dy));
  }

  // Iterate topmost-first (later-placed parts draw on top) so hovering/
  // clicking an overlapping spot matches what's actually visible.
  function hitTestPart(pos) {
    for (let i = state.parts.length - 1; i >= 0; i--) {
      const p = state.parts[i];
      const t = p.terminals;
      if (p.type === 'toroid') {
        const c = Components.toroidCentroid(t);
        if (Math.hypot(pos.x - c.x, pos.y - c.y) < 28) return p;
        // terminals can sit far from the ring itself (each section's holes
        // are wherever the user clicked) -- also catch a click on a lead
        if (t.some((term) => distToSegment(pos.x, pos.y, term.x, term.y, c.x, c.y) < 10)) return p;
      } else if (t.length === 6) {
        const left = Math.min(t[0].x, t[3].x) - 10;
        const right = Math.max(t[2].x, t[5].x) + 10;
        const top = Math.min(t[1].y, t[4].y) - 17;
        const bottom = Math.max(t[1].y, t[4].y) + 17;
        if (pos.x >= left && pos.x <= right && pos.y >= top && pos.y <= bottom) return p;
      } else if (t.length === 4) {
        const [j1, j2] = Components.yWireJunctions(t);
        if (
          distToSegment(pos.x, pos.y, t[0].x, t[0].y, j1.x, j1.y) < 14 ||
          distToSegment(pos.x, pos.y, t[1].x, t[1].y, j1.x, j1.y) < 14 ||
          distToSegment(pos.x, pos.y, j1.x, j1.y, j2.x, j2.y) < 14 ||
          distToSegment(pos.x, pos.y, t[2].x, t[2].y, j2.x, j2.y) < 14 ||
          distToSegment(pos.x, pos.y, t[3].x, t[3].y, j2.x, j2.y) < 14
        ) return p;
      } else if (t.length === 3) {
        const c = p.type === 'mtjsensor' ? Components.mtjCentroid(t) : Components.vgndCentroid(t);
        if (Math.hypot(pos.x - c.x, pos.y - c.y) < 20) return p;
      } else if (t.length === 2) {
        if (distToSegment(pos.x, pos.y, t[0].x, t[0].y, t[1].x, t[1].y) < 14) return p;
      } else if (t.length === 1) {
        if (Math.hypot(pos.x - t[0].x, pos.y - t[0].y) < 16) return p;
      }
    }
    return null;
  }

  // where the selection ring / occupied-hole body is centered for a part
  function partCenter(p) {
    const t = p.terminals;
    if (p.type === 'toroid') return Components.toroidCentroid(t);
    if (t.length === 6) return { x: (t[1].x + t[4].x) / 2, y: (t[1].y + t[4].y) / 2 };
    if (t.length === 4) {
      const [j1, j2] = Components.yWireJunctions(t);
      return { x: (j1.x + j2.x) / 2, y: (j1.y + j2.y) / 2 };
    }
    if (t.length === 3) return p.type === 'mtjsensor' ? Components.mtjCentroid(t) : Components.vgndCentroid(t);
    if (t.length === 1) return { x: t[0].x, y: t[0].y };
    return { x: (t[0].x + t[1].x) / 2, y: (t[0].y + t[1].y) / 2 };
  }

  // executor: the state changes behind a momentary pushbutton press/release
  function pressPushbutton(pos) {
    const part = hitTestPart(pos);
    if (part && part.type === 'pushbutton') part.closed = true;
  }

  const POT_KNOB_RADIUS = 12;
  // query: is this position over a placed potentiometer's knob?
  function hitTestPotKnob(pos) {
    for (let i = state.parts.length - 1; i >= 0; i--) {
      const p = state.parts[i];
      if (p.type !== 'potentiometer') continue;
      const c = Components.potCentroid(p.terminals);
      if (Math.hypot(pos.x - c.x, pos.y - c.y) < POT_KNOB_RADIUS) return p;
    }
    return null;
  }
  // executor: turning the knob by dragging it directly on the canvas --
  // rounds to 0.1% steps, matching the Inspector's fine slider, so mouse
  // jitter doesn't stop the wiper from settling on an exact value.
  function turnPotKnob(part, pos) {
    const c = Components.potCentroid(part.terminals);
    const angle = Math.atan2(pos.y - c.y, pos.x - c.x);
    part.pos = Math.round(Components.potAngleToPos(angle) * 1000) / 1000;
  }
  function releaseAllPushbuttons() {
    state.parts.forEach((p) => {
      if (p.type === 'pushbutton') p.closed = false;
    });
  }

  // keeps the Inspector's fine slider (and its % readout) in sync while the
  // knob is being turned directly on the canvas, without a full re-render
  function syncPotSliderUi(part) {
    if (!currentPotRangeEl || !currentPotRangeEl.isConnected || currentPotPartId !== part.id) return;
    const steps = String(Math.round(part.pos * 1000));
    currentPotRangeEl.value = steps;
    currentPotLabelEl.textContent = (Number(steps) / 10).toFixed(1) + '%';
  }

  canvas.addEventListener('mousemove', (evt) => {
    const pos = mousePos(evt);
    if (state.draggingPot) {
      turnPotKnob(state.draggingPot, pos);
      syncPotSliderUi(state.draggingPot);
      return;
    }
    state.hoverHole = Board.hitTest(board, pos.x, pos.y, 8);
    state.hoverPart = hitTestPart(pos);
    canvas.style.cursor = state.tool === 'select' && hitTestPotKnob(pos) ? 'grab' : '';
  });
  canvas.addEventListener('mouseleave', () => {
    state.hoverHole = null;
    state.hoverPart = null;
    releaseAllPushbuttons();
  });
  canvas.addEventListener('mousedown', (evt) => {
    if (state.tool !== 'select') return;
    const pos = mousePos(evt);
    const knob = hitTestPotKnob(pos);
    if (knob) {
      state.draggingPot = knob;
      knob.dragging = true;
      canvas.style.cursor = 'grabbing';
      selectPart(knob.id);
      turnPotKnob(knob, pos);
      syncPotSliderUi(knob);
      return;
    }
    pressPushbutton(pos);
  });
  // mousedown+move+up over the canvas still synthesizes a trailing "click"
  // at the release point -- suppress just that one click after a knob drag
  // so releasing off the knob's body doesn't deselect the part it just set
  let suppressNextClick = false;
  window.addEventListener('mouseup', () => {
    if (state.draggingPot) {
      state.draggingPot.dragging = false;
      state.draggingPot = null;
      canvas.style.cursor = '';
      suppressNextClick = true;
    }
    releaseAllPushbuttons();
  });
  // a fast drag can outrun the canvas's own bounds -- keep turning the knob
  // as long as the button's held, even past the board's edge, like a real
  // drag-to-turn control would
  window.addEventListener('mousemove', (evt) => {
    if (!state.draggingPot) return;
    turnPotKnob(state.draggingPot, mousePos(evt));
    syncPotSliderUi(state.draggingPot);
  });

  // touch support (phones/tablets): update the hover readout as a finger
  // moves, and let the browser's own tap-to-click synthesis handle placement
  function touchPos(evt) {
    const t = evt.touches[0] || evt.changedTouches[0];
    const r = canvas.getBoundingClientRect();
    return { x: t.clientX - r.left, y: t.clientY - r.top };
  }
  canvas.addEventListener('touchstart', (evt) => {
    const pos = touchPos(evt);
    state.hoverHole = Board.hitTest(board, pos.x, pos.y, 12);
    state.hoverPart = hitTestPart(pos);
    if (state.tool === 'select') {
      const knob = hitTestPotKnob(pos);
      if (knob) {
        state.draggingPot = knob;
        knob.dragging = true;
        selectPart(knob.id);
        turnPotKnob(knob, pos);
        syncPotSliderUi(knob);
        return;
      }
      pressPushbutton(pos);
    }
  }, { passive: true });
  canvas.addEventListener('touchmove', (evt) => {
    const pos = touchPos(evt);
    if (state.draggingPot) {
      turnPotKnob(state.draggingPot, pos);
      syncPotSliderUi(state.draggingPot);
      return;
    }
    state.hoverHole = Board.hitTest(board, pos.x, pos.y, 12);
    state.hoverPart = hitTestPart(pos);
  }, { passive: true });
  canvas.addEventListener('touchend', () => {
    if (state.draggingPot) {
      state.draggingPot.dragging = false;
      state.draggingPot = null;
    }
    releaseAllPushbuttons();
  }, { passive: true });

  // validator: is this hole a legal next click for the placement in progress?
  // (rejects only re-clicking the exact same hole twice in a row)
  function isValidPlacement(pending, hole) {
    if (!pending.length) return true;
    const last = pending[pending.length - 1];
    return !(last.x === hole.x && last.y === hole.y);
  }

  // executor: the actual state changes for select-mode clicks
  function toggleSwitch(part) {
    part.closed = !part.closed;
  }
  function selectPart(id) {
    state.selectedPartId = id;
    renderProps();
  }

  // router: a click means something different depending on which tool is
  // active — this is the only place that decides which path to take.
  function handleCanvasClick(pos) {
    if (state.tool === 'select') {
      handleSelectClick(pos);
    } else {
      handlePlacementClick(pos);
    }
  }

  function handleSelectClick(pos) {
    const part = hitTestPart(pos);
    if (part && part.type === 'switch') toggleSwitch(part);
    selectPart(part ? part.id : null);
  }

  function handlePlacementClick(pos) {
    const hole = Board.hitTest(board, pos.x, pos.y, 11);
    if (!hole) return;
    if (!isValidPlacement(state.pending, hole)) return;
    state.pending.push(hole);
    if (state.pending.length >= terminalsNeeded(state.tool)) {
      commitPart(state.tool, state.pending);
      state.pending = [];
    }
  }

  // event handler: just captures the click and hands it to the router
  canvas.addEventListener('click', (evt) => {
    if (suppressNextClick) {
      suppressNextClick = false;
      return;
    }
    handleCanvasClick(mousePos(evt));
  });

  window.addEventListener('keydown', (evt) => {
    if (evt.key === 'Escape') {
      cancelPending();
      selectTool('select');
      closeContextMenu();
    }
  });

  // ---------------- properties panel ----------------
  const propsEl = document.getElementById('props');
  let currentReadoutEl = null;
  let currentPotPartId = null;
  let currentPotRangeEl = null;
  let currentPotLabelEl = null;
  // presentation: builds the type-specific controls for a part (value
  // dropdowns, color swatches, toggle buttons, wire color/style) into
  // whatever container is given. Shared by the Inspector panel and the
  // right-click context menu, so each control lives in exactly one place.
  // `refresh` is called only where the control needs its own visual state
  // (an active swatch, a button's label) rebuilt after a change — value
  // dropdowns and the pot slider update natively and skip it, and the
  // pushbutton skips it too so a rebuild never interrupts a press-and-hold.
  function buildPartControls(part, container, refresh) {
    const notify = refresh || (() => {});
    if (part.type === 'resistor') {
      container.appendChild(makeSelect('Resistance', Components.RESISTOR_VALUES.map((v) => [v, Components.formatOhms(v)]), part.value, (v) => (part.value = Number(v))));
    } else if (part.type === 'capacitor') {
      container.appendChild(makeSelect('Capacitance', Components.CAPACITOR_VALUES.map((v) => [v.farads, v.label]), part.value, (v) => (part.value = Number(v))));
    } else if (part.type === 'battery') {
      container.appendChild(makeSelect('Voltage', Components.BATTERY_VALUES.map((v) => [v, v + ' V']), part.value, (v) => (part.value = Number(v))));
    } else if (part.type === 'inductor') {
      container.appendChild(makeSelect('Inductance', Components.INDUCTOR_VALUES.map((v) => [v, Components.formatHenries(v)]), part.value, (v) => (part.value = Number(v))));
    } else if (part.type === 'acsource') {
      container.appendChild(makeSelect('Amplitude', Components.BATTERY_VALUES.map((v) => [v, v + ' Vpk']), part.value, (v) => (part.value = Number(v))));
      container.appendChild(makeSelect('Frequency', Components.AC_FREQ_VALUES.map((v) => [v, v + ' Hz']), part.freq, (v) => (part.freq = Number(v))));
    } else if (part.type === 'mtjsensor') {
      container.appendChild(makeSelect('Output amplitude', Components.BATTERY_VALUES.map((v) => [v, v + ' Vpk']), part.value, (v) => (part.value = Number(v))));
      container.appendChild(makeSelect('Rotation rate', Components.AC_FREQ_VALUES.map((v) => [v, v + ' Hz']), part.freq, (v) => (part.freq = Number(v))));
    } else if (part.type === 'led') {
      container.appendChild(makeSelect('Color', Components.LED_COLORS.map((c) => [c, c[0].toUpperCase() + c.slice(1)]), part.color, (v) => { part.color = v; notify(); }));
    } else if (part.type === 'switch') {
      container.appendChild(makeSelect('State', [['closed', 'Closed'], ['open', 'Open']], part.closed ? 'closed' : 'open', (v) => { part.closed = v === 'closed'; notify(); }));
    } else if (part.type === 'pushbutton') {
      const btn = document.createElement('button');
      btn.className = 'action-btn';
      btn.textContent = 'Hold to press';
      btn.addEventListener('mousedown', () => (part.closed = true));
      btn.addEventListener('mouseup', () => (part.closed = false));
      btn.addEventListener('mouseleave', () => (part.closed = false));
      btn.addEventListener('touchstart', (e) => { e.preventDefault(); part.closed = true; }, { passive: false });
      btn.addEventListener('touchend', () => (part.closed = false));
      container.appendChild(btn);
    } else if (part.type === 'potentiometer') {
      // 0-1000 steps = 0.1% resolution, fine enough to dial in a specific
      // millivolt-scale lean for asymmetric-voltage testing rather than
      // just coarse 1% notches.
      const wrap = document.createElement('div');
      wrap.className = 'pot-slider';
      const range = document.createElement('input');
      range.type = 'range';
      range.min = '0';
      range.max = '1000';
      range.step = '1';
      range.value = String(Math.round((part.pos ?? 0.5) * 1000));
      const pctLabel = document.createElement('span');
      pctLabel.className = 'pot-pct';
      const updatePct = () => { pctLabel.textContent = (Number(range.value) / 10).toFixed(1) + '%'; };
      updatePct();
      range.addEventListener('input', () => {
        part.pos = Number(range.value) / 1000;
        updatePct();
      });
      wrap.appendChild(range);
      wrap.appendChild(pctLabel);
      container.appendChild(labeled('Wiper position (0.1% steps)', wrap));
      container.appendChild(makeSelect('Total resistance', Components.RESISTOR_VALUES.map((v) => [v, Components.formatOhms(v)]), part.value, (v) => (part.value = Number(v))));
      currentPotPartId = part.id;
      currentPotRangeEl = range;
      currentPotLabelEl = pctLabel;
    } else if (part.type === 'wire' || part.type === 'ywire') {
      container.appendChild(makeSelect('Color', Components.WIRE_COLOR_CHOICES.map((c) => [c, Components.WIRE_COLOR_NAMES[c] || c]), part.color, (v) => { part.color = v; notify(); }));
      container.appendChild(makeSelect('Gauge', Object.entries(Components.WIRE_GAUGES).map(([k, v]) => [k, v]), part.gauge || 'standard', (v) => { part.gauge = v; notify(); }));
      container.appendChild(makeSelect('Style', [['loop', 'Looped'], ['flat', 'Flat']], part.style || 'loop', (v) => { part.style = v; notify(); }));
    } else if (part.type === 'toroid') {
      container.appendChild(makeSelect('Core', Object.entries(Components.TOROID_CORES).map(([k, v]) => [k, v.label]), part.core, (v) => { part.core = v; notify(); }));
      container.appendChild(makeSelect('Wire gauge', Object.entries(Components.WIRE_GAUGES).map(([k, v]) => [k, v]), part.gauge, (v) => { part.gauge = v; notify(); }));
      part.turnsPerSection.forEach((turns, s) => {
        container.appendChild(makeSelect('Turns (section ' + (s + 1) + ')', Components.TOROID_TURNS_VALUES.map((n) => [n, n]), turns, (v) => { part.turnsPerSection[s] = Number(v); notify(); }));
      });
      if (part.turnsPerSection.length > 1) {
        container.appendChild(makeSelect('Winding spacing', Object.keys(Components.TOROID_SPACING_COUPLING).map((k) => [k, k[0].toUpperCase() + k.slice(1)]), part.spacing, (v) => { part.spacing = v; notify(); }));
      }
    }
  }

  function renderProps() {
    propsEl.innerHTML = '';
    const part = state.parts.find((p) => p.id === state.selectedPartId);
    if (!part) {
      currentReadoutEl = null;
      return;
    }
    const card = buildPreviewCard(part.type, part);
    const idTag = document.createElement('div');
    idTag.className = 'part-card-id';
    idTag.textContent = part.id;
    card.appendChild(idTag);
    propsEl.appendChild(card);

    buildPartControls(part, propsEl, renderProps);

    currentReadoutEl = document.createElement('div');
    currentReadoutEl.className = 'readout';
    propsEl.appendChild(currentReadoutEl);
    updatePropsReadout();

    const del = document.createElement('button');
    del.className = 'action-btn danger';
    del.textContent = 'Delete part';
    del.addEventListener('click', () => {
      state.parts = state.parts.filter((p) => p.id !== part.id);
      state.selectedPartId = null;
      renderProps();
    });
    propsEl.appendChild(del);
  }
  renderProps();

  // presentation: refresh just the live numbers every frame, without
  // rebuilding the surrounding controls (which would drop focus mid-drag on
  // a slider, or swallow a button press).
  function updatePropsReadout() {
    if (!currentReadoutEl) return;
    const part = state.parts.find((p) => p.id === state.selectedPartId);
    const uf = state.lastResult.uf;
    if (!part || !uf) return;
    const I = state.lastResult.currents.get(part.id);
    const vOf = (idx) => state.lastResult.voltages.get(uf.find(part.terminals[idx].cellId));
    const va = vOf(0);
    const vb = vOf(part.type === 'potentiometer' ? 2 : 1);

    let rows;
    if (part.type === 'vgnd') {
      // the derived virtual-ground/V0 output is the interesting number here,
      // not "V(B)" — show all three explicitly instead of the generic pair
      rows = `
        <div><span>V(in A)</span><b>${fmtV(va)}</b></div>
        <div><span>V(in B)</span><b>${fmtV(vb)}</b></div>
        <div><span>V(out/V0)</span><b>${fmtV(vOf(2))}</b></div>
      `;
    } else if (part.type === 'mtjsensor') {
      // the two analog channels relative to the sensor's own reference pin
      // are what a real angle decoder reads -- plus the angle atan2 decodes
      // them back to, to confirm the quadrature pair is actually correct
      const vRef = va;
      const vSin = vb - vRef;
      const vCos = vOf(2) - vRef;
      const angleDeg = (Math.atan2(vSin, vCos) * 180) / Math.PI;
      currentReadoutEl.innerHTML = `
        <div><span>V(ref)</span><b>${fmtV(vRef)}</b></div>
        <div><span>V(sin) - V(ref)</span><b>${fmtV(vSin)}</b></div>
        <div><span>V(cos) - V(ref)</span><b>${fmtV(vCos)}</b></div>
        <div><span>Decoded angle</span><b>${angleDeg.toFixed(1)}°</b></div>
      `;
      return;
    } else if (part.type === 'toroid') {
      // one V/I pair per winding section -- a transformer's whole point is
      // comparing sections against each other (turns ratio, phase), so the
      // generic single-pair readout would hide the interesting part
      currentReadoutEl.innerHTML = part.turnsPerSection.map((turns, s) => {
        const vs = vOf(s * 2) - vOf(s * 2 + 1);
        const Is = state.lastResult.currents.get(part.id + ':' + s);
        return `
          <div><span>V(section ${s + 1})</span><b>${fmtV(vs)}</b></div>
          <div><span>I(section ${s + 1})</span><b>${fmtI(Is)}</b></div>
        `;
      }).join('');
      return;
    } else {
      rows = `
        <div><span>V(A)</span><b>${fmtV(va)}</b></div>
        <div><span>V(B)</span><b>${fmtV(vb)}</b></div>
      `;
      if (part.type === 'potentiometer') {
        // the wiper is what actually shows an asymmetric lean off a virtual
        // ground — the plain A/B endpoint readout alone can't show that
        rows += `<div><span>V(wiper)</span><b>${fmtV(vOf(1))}</b></div>`;
      }
    }
    rows += `
      <div><span>ΔV</span><b>${fmtV(va - vb)}</b></div>
      <div><span>Current</span><b>${fmtI(I)}</b></div>
    `;
    currentReadoutEl.innerHTML = rows;
  }

  function fmtV(v) {
    if (v == null || Number.isNaN(v)) return '—';
    return v.toFixed(3) + ' V';
  }
  function fmtI(i) {
    if (i == null || Number.isNaN(i)) return '—';
    const a = Math.abs(i);
    if (a >= 1) return i.toFixed(3) + ' A';
    if (a >= 1e-3) return (i * 1000).toFixed(2) + ' mA';
    return (i * 1e6).toFixed(1) + ' µA';
  }

  // ---------------- right-click context menu ----------------
  // router: right-clicking a part opens a floating menu with its controls
  // (via the same buildPartControls used by the Inspector) plus Remove —
  // a quicker path than select-then-scroll-to-Inspector.
  const contextMenuEl = document.getElementById('contextMenu');
  const contextMenuTitleEl = document.getElementById('contextMenuTitle');
  const contextMenuControlsEl = document.getElementById('contextMenuControls');
  const contextMenuRemoveEl = document.getElementById('contextMenuRemove');
  let contextMenuPartId = null;

  function refreshContextMenu() {
    const part = state.parts.find((p) => p.id === contextMenuPartId);
    if (!part) return closeContextMenu();
    contextMenuControlsEl.innerHTML = '';
    buildPartControls(part, contextMenuControlsEl, refreshContextMenu);
  }

  function openContextMenu(part, clientX, clientY) {
    contextMenuPartId = part.id;
    contextMenuTitleEl.textContent = partTitle(part);
    contextMenuEl.hidden = false;
    refreshContextMenu();
    const menuW = contextMenuEl.offsetWidth || 230;
    const menuH = contextMenuEl.offsetHeight || 160;
    contextMenuEl.style.left = Math.max(8, Math.min(clientX, window.innerWidth - menuW - 8)) + 'px';
    contextMenuEl.style.top = Math.max(8, Math.min(clientY, window.innerHeight - menuH - 8)) + 'px';
  }

  function closeContextMenu() {
    contextMenuPartId = null;
    contextMenuEl.hidden = true;
  }

  canvas.addEventListener('contextmenu', (evt) => {
    evt.preventDefault();
    const part = hitTestPart(mousePos(evt));
    if (part) openContextMenu(part, evt.clientX, evt.clientY);
    else closeContextMenu();
  });
  document.addEventListener('click', (evt) => {
    if (!contextMenuEl.hidden && !contextMenuEl.contains(evt.target)) closeContextMenu();
  });
  contextMenuRemoveEl.addEventListener('click', () => {
    state.parts = state.parts.filter((p) => p.id !== contextMenuPartId);
    if (state.selectedPartId === contextMenuPartId) {
      state.selectedPartId = null;
      renderProps();
    }
    closeContextMenu();
  });

  // ---------------- toolbar actions ----------------
  document.getElementById('btnClear').addEventListener('click', () => {
    if (!confirm('Clear the whole breadboard?')) return;
    state.parts = [];
    state.selectedPartId = null;
    circuit.reset();
    renderProps();
  });

  document.getElementById('btnWebVersion').addEventListener('click', () => {
    const url = 'https://one-wave-universe.github.io/One-Wave-Science/';
    if (window.electronAPI && window.electronAPI.openExternal) window.electronAPI.openExternal(url);
    else window.open(url, '_blank');
  });

  // executor: swap in a different board layout. Each board keeps its own
  // power rails (namespaced cellIds) unless the user bridges them with an
  // ordinary jumper wire -- exactly like separate physical boards on a
  // desk. Since existing parts' hole references would no longer line up
  // with a different board geometry, a layout change starts the board over.
  const boardLayoutEl = document.getElementById('boardLayout');
  let currentLayoutKey = '1large';
  function rebuildBoard(layoutKey) {
    const layout = LAYOUT_PRESETS[layoutKey];
    if (!layout) return;
    if (state.parts.length && !confirm('Changing the board layout clears the current build. Continue?')) {
      boardLayoutEl.value = currentLayoutKey;
      return;
    }
    currentLayoutKey = layoutKey;
    board = Board.build(layout);
    state.board = board;
    state.parts = [];
    state.selectedPartId = null;
    state.pending = [];
    state.hoverHole = null;
    state.hoverPart = null;
    circuit.reset();
    setupCanvas();
    renderProps();
  }
  boardLayoutEl.addEventListener('change', () => rebuildBoard(boardLayoutEl.value));
  document.getElementById('btnSave').addEventListener('click', () => {
    try {
      localStorage.setItem('virtual-breadboard-save', JSON.stringify({ layout: currentLayoutKey, parts: state.parts }));
      flashStatus('Saved to browser storage.');
    } catch (e) {
      flashStatus('Could not save: ' + e.message);
    }
  });
  document.getElementById('btnLoad').addEventListener('click', () => {
    try {
      const raw = localStorage.getItem('virtual-breadboard-save');
      if (!raw) return flashStatus('No saved build found.');
      const saved = JSON.parse(raw);
      // older saves stored a bare parts array with no layout info
      const layoutKey = Array.isArray(saved) ? '1large' : saved.layout || '1large';
      const loaded = Array.isArray(saved) ? saved : saved.parts;
      if (layoutKey !== currentLayoutKey && LAYOUT_PRESETS[layoutKey]) {
        currentLayoutKey = layoutKey;
        boardLayoutEl.value = layoutKey;
        board = Board.build(LAYOUT_PRESETS[layoutKey]);
        state.board = board;
        setupCanvas();
      }
      let maxId = 0;
      loaded.forEach((p) => {
        const n = parseInt(String(p.id).slice(1), 10);
        if (!Number.isNaN(n)) maxId = Math.max(maxId, n);
      });
      state.nextId = maxId + 1;
      state.parts = loaded;
      state.selectedPartId = null;
      circuit.reset();
      renderProps();
      flashStatus('Loaded saved build.');
    } catch (e) {
      flashStatus('Could not load: ' + e.message);
    }
  });

  function flashStatus(msg) {
    const el = document.getElementById('flash');
    el.textContent = msg;
    el.style.opacity = '1';
    clearTimeout(flashStatus._t);
    flashStatus._t = setTimeout(() => (el.style.opacity = '0'), 2200);
  }

  // ---------------- example presets ----------------
  // generator: each preset is just data — a list of parts to place. Building
  // this list has no effect on the board by itself.
  function presetLedResistorParts() {
    return [
      { type: 'battery', terminals: [H('e', 10), H('f', 10)], value: 5 },
      { type: 'resistor', terminals: [H('c', 10), H('c', 15)], value: 220 },
      { type: 'led', terminals: [H('a', 15), H('j', 15)], color: 'red' },
      { type: 'wire', terminals: [H('h', 10), H('h', 15)], color: nextWireColor() },
    ];
  }
  function presetShortParts() {
    return [
      { type: 'battery', terminals: [H('e', 10), H('f', 10)], value: 9 },
      { type: 'wire', terminals: [H('c', 10), H('h', 10)], color: nextWireColor() },
    ];
  }
  function presetRCParts() {
    return [
      { type: 'battery', terminals: [H('e', 5), H('f', 5)], value: 9 },
      { type: 'switch', terminals: [H('b', 5), H('b', 8)], closed: false },
      { type: 'resistor', terminals: [H('c', 8), H('c', 20)], value: 100000 },
      { type: 'capacitor', terminals: [H('d', 20), H('g', 20)], value: 100e-6 },
      { type: 'wire', terminals: [H('i', 5), H('i', 20)], color: nextWireColor() },
    ];
  }
  // executor: the one place that actually clears the board and writes a
  // preset's parts into it.
  function applyPreset(parts) {
    state.parts = [];
    circuit.reset();
    parts.forEach(addPart);
  }
  document.getElementById('presetLed').addEventListener('click', () => { applyPreset(presetLedResistorParts()); selectTool('select'); });
  document.getElementById('presetShort').addEventListener('click', () => { applyPreset(presetShortParts()); selectTool('select'); });
  document.getElementById('presetRC').addEventListener('click', () => { applyPreset(presetRCParts()); selectTool('select'); });

  // ---------------- AI build (pluggable generator) ----------------
  // Whatever provider is configured plays the same role the hardcoded
  // presets play above: it produces a parts list, nothing more. Validation
  // and committing to the board go through the exact same evaluator/executor
  // path either way.
  const AI_SETTINGS_KEY = 'virtual-breadboard-ai-settings';

  function loadAiSettings() {
    try {
      return Object.assign({ provider: 'anthropic', apiKey: '', model: '', endpoint: '' }, JSON.parse(localStorage.getItem(AI_SETTINGS_KEY) || '{}'));
    } catch (e) {
      return { provider: 'anthropic', apiKey: '', model: '', endpoint: '' };
    }
  }
  function saveAiSettings(settings) {
    localStorage.setItem(AI_SETTINGS_KEY, JSON.stringify(settings));
  }

  const aiSettingsToggle = document.getElementById('aiSettingsToggle');
  const aiSettingsEl = document.getElementById('aiSettings');
  const aiProviderEl = document.getElementById('aiProvider');
  const aiEndpointField = document.getElementById('aiEndpointField');
  const aiEndpointEl = document.getElementById('aiEndpoint');
  const aiApiKeyEl = document.getElementById('aiApiKey');
  const aiModelEl = document.getElementById('aiModel');
  const aiPromptEl = document.getElementById('aiPrompt');
  const aiStatusEl = document.getElementById('aiStatus');

  function renderAiSettingsForm() {
    const s = loadAiSettings();
    aiProviderEl.value = s.provider;
    aiEndpointEl.value = s.endpoint;
    aiApiKeyEl.value = s.apiKey;
    aiModelEl.value = s.model;
    aiEndpointField.hidden = s.provider !== 'custom';
  }
  renderAiSettingsForm();

  aiSettingsToggle.addEventListener('click', () => {
    aiSettingsEl.hidden = !aiSettingsEl.hidden;
  });
  aiProviderEl.addEventListener('change', () => {
    aiEndpointField.hidden = aiProviderEl.value !== 'custom';
    saveAiSettings({ provider: aiProviderEl.value, endpoint: aiEndpointEl.value, apiKey: aiApiKeyEl.value, model: aiModelEl.value });
  });
  [aiEndpointEl, aiApiKeyEl, aiModelEl].forEach((el) => {
    el.addEventListener('change', () => {
      saveAiSettings({ provider: aiProviderEl.value, endpoint: aiEndpointEl.value, apiKey: aiApiKeyEl.value, model: aiModelEl.value });
    });
  });

  function setAiStatus(text, kind) {
    aiStatusEl.textContent = text;
    aiStatusEl.className = 'ai-status' + (kind ? ' ' + kind : '');
  }

  // generator: turn a validated AI spec's {row,col} references into real
  // board holes, the same terminal shape every other part uses. A
  // potentiometer spec gives one anchor hole; the other 5 pins of its real
  // 6-pin footprint are derived the same way a manual click derives them.
  function specPartsToBoardParts(specParts) {
    return specParts
      .map((p) => {
        const terminals = p.type === 'potentiometer'
          ? derivePotentiometerHoles(H(p.terminals[0].row, p.terminals[0].col))
          : p.terminals.map((t) => H(t.row, t.col));
        if (!terminals) return null;
        const isWire = p.type === 'wire' || p.type === 'ywire';
        return {
          type: p.type,
          value: p.value,
          color: p.type === 'scope' ? nextScopeColor() : isWire ? nextWireColor() : p.color,
          closed: !!p.closed,
          pos: p.type === 'potentiometer' ? 0.5 : undefined,
          style: isWire ? 'loop' : undefined,
          freq: p.freq,
          phase: p.phase,
          turnsPerSection: p.type === 'toroid' ? p.turns : undefined,
          core: p.type === 'toroid' ? (p.core || 'medium') : undefined,
          gauge: p.type === 'toroid' ? (p.gauge || 'standard') : undefined,
          spacing: p.type === 'toroid' ? (p.spacing || 'normal') : undefined,
          terminals,
        };
      })
      .filter(Boolean);
  }

  async function runAiBuild() {
    const text = aiPromptEl.value.trim();
    if (!text) return setAiStatus('Describe what you want built first.', 'err');
    const settings = loadAiSettings();
    if (settings.provider !== 'custom' && !settings.apiKey) {
      return setAiStatus('Add an API key in settings first.', 'err');
    }
    const call = AIBuilder.PROVIDERS[settings.provider];
    if (!call) return setAiStatus('Unknown provider.', 'err');

    setAiStatus('Thinking…', 'busy');
    try {
      const raw = await call({ apiKey: settings.apiKey, model: settings.model, endpoint: settings.endpoint, userText: text });
      const spec = AIBuilder.extractJson(raw);
      const { ok, errors, parts } = AIBuilder.validateSpec(spec);
      if (!ok) {
        setAiStatus("The AI's response wasn't a valid circuit:\n" + errors.join('\n'), 'err');
        return;
      }
      applyPreset(specPartsToBoardParts(parts));
      selectTool('select');
      setAiStatus('Built ' + parts.length + ' part' + (parts.length === 1 ? '' : 's') + '. Check the status bar for any warnings.', 'ok');
    } catch (err) {
      setAiStatus('Could not build that: ' + err.message, 'err');
    }
  }
  document.getElementById('aiBuild').addEventListener('click', runAiBuild);

  // ---------------- oscilloscope ----------------
  // Scope probes are zero-load voltage taps sampled straight off the live
  // solve results every frame, kept as a rolling time window per probe —
  // the same "real, live, frame by frame" philosophy as the RC/AC physics
  // itself, just plotted instead of read as a single number.
  const scopeCanvas = document.getElementById('scopeCanvas');
  const scopeCtx = scopeCanvas.getContext('2d');
  const scopeLegendEl = document.getElementById('scopeLegend');
  let scopeSize = { w: 600, h: 150 };
  function setupScopeCanvas() {
    const dpr = window.devicePixelRatio || 1;
    const w = Math.max(scopeCanvas.clientWidth || scopeCanvas.parentElement.clientWidth, 100);
    const h = 150;
    scopeCanvas.width = w * dpr;
    scopeCanvas.height = h * dpr;
    scopeCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
    scopeSize = { w, h };
  }
  setupScopeCanvas();
  window.addEventListener('resize', setupScopeCanvas);

  function sampleScopeProbes() {
    const uf = state.lastResult.uf;
    state.parts.forEach((p) => {
      if (p.type !== 'scope') return;
      if (!p.samples) p.samples = [];
      const v = uf ? state.lastResult.voltages.get(uf.find(p.terminals[0].cellId)) : undefined;
      p.samples.push({ t: state.animT, v: v == null ? 0 : v });
      while (p.samples.length > 1 && state.animT - p.samples[0].t > SCOPE_WINDOW) p.samples.shift();
    });
  }

  function renderScope() {
    const { w, h } = scopeSize;
    scopeCtx.clearRect(0, 0, w, h);
    const probes = state.parts.filter((p) => p.type === 'scope');

    let vMax = 0.5;
    probes.forEach((p) => (p.samples || []).forEach((s) => { vMax = Math.max(vMax, Math.abs(s.v)); }));
    vMax *= 1.15;

    scopeCtx.strokeStyle = '#1c2430';
    scopeCtx.lineWidth = 1;
    scopeCtx.beginPath();
    for (let i = 1; i < 4; i++) {
      const y = (h / 4) * i;
      scopeCtx.moveTo(0, y);
      scopeCtx.lineTo(w, y);
    }
    for (let i = 1; i < 6; i++) {
      const x = (w / 6) * i;
      scopeCtx.moveTo(x, 0);
      scopeCtx.lineTo(x, h);
    }
    scopeCtx.stroke();
    scopeCtx.strokeStyle = '#3a4454';
    scopeCtx.beginPath();
    scopeCtx.moveTo(0, h / 2);
    scopeCtx.lineTo(w, h / 2);
    scopeCtx.stroke();

    const tNow = state.animT;
    probes.forEach((p) => {
      const samples = p.samples || [];
      if (samples.length < 2) return;
      scopeCtx.strokeStyle = p.color;
      scopeCtx.lineWidth = 1.6;
      scopeCtx.beginPath();
      samples.forEach((s, idx) => {
        const x = w * (1 - (tNow - s.t) / SCOPE_WINDOW);
        const y = h / 2 - (s.v / vMax) * (h / 2 - 6);
        if (idx === 0) scopeCtx.moveTo(x, y);
        else scopeCtx.lineTo(x, y);
      });
      scopeCtx.stroke();
    });

    scopeLegendEl.innerHTML = probes.length
      ? probes.map((p) => {
          const last = (p.samples && p.samples[p.samples.length - 1]) || { v: 0 };
          return `<span class="chip"><span class="swatch-dot" style="background:${p.color}"></span>${p.id} @ ${p.terminals[0].cellId}: <b>${fmtV(last.v)}</b></span>`;
        }).join('')
      : '<span class="chip">No probes placed yet — pick the Scope Probe tool.</span>';
  }

  // ---------------- main loop ----------------
  let lastT = performance.now();
  function frame(now) {
    let dt = (now - lastT) / 1000;
    lastT = now;
    dt = Math.min(Math.max(dt, 0), 0.05);
    state.animT += dt;

    const elements = toEngineElements();
    state.lastResult = circuit.solve(elements, dt);
    sampleScopeProbes();

    render(dt);
    renderScope();
    updateWarnings();
    updatePropsReadout();
    requestAnimationFrame(frame);
  }

  function highlightSetForHover() {
    if (!state.hoverHole || !state.lastResult.uf) return null;
    const root = state.lastResult.uf.find(state.hoverHole.cellId);
    const set = new Set();
    board.holes.forEach((h) => {
      if (state.lastResult.uf.find(h.cellId) === root) set.add(h.cellId);
    });
    return set;
  }

  function render(dt) {
    ctx.clearRect(0, 0, board.width, board.height);
    Board.draw(ctx, board, { highlightSet: highlightSetForHover() });

    const { voltages, currents, uf } = state.lastResult;

    state.parts.forEach((p) => {
      const t = p.terminals;
      // see-through-on-hover: fade whatever's under the cursor so holes
      // hidden underneath its body stay reachable for a jumper wire
      const opacity = state.hoverPart && p.id === state.hoverPart.id ? 0.28 : 1;
      if (p.type === 'wire') {
        Components.drawWire(ctx, t[0].x, t[0].y, t[1].x, t[1].y, p.color, opacity, p.style, p.gauge);
      } else if (p.type === 'ywire') {
        Components.drawYWire(ctx, t, p.color, opacity, p.style, p.gauge);
      } else if (p.type === 'resistor') {
        Components.drawResistor(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y, opacity);
      } else if (p.type === 'led') {
        const I = currents.get(p.id) || 0;
        const glow = Math.min(1, I * 60);
        Components.drawLed(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y, glow, opacity);
      } else if (p.type === 'diode') {
        Components.drawDiode(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y, opacity);
      } else if (p.type === 'capacitor') {
        Components.drawCapacitor(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y, opacity);
      } else if (p.type === 'battery') {
        Components.drawBattery(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y, opacity);
      } else if (p.type === 'switch') {
        Components.drawSwitch(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y, opacity);
      } else if (p.type === 'pushbutton') {
        Components.drawPushbutton(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y, opacity);
      } else if (p.type === 'potentiometer') {
        Components.drawPotentiometer(ctx, p, t, opacity);
      } else if (p.type === 'vgnd') {
        Components.drawVGnd(ctx, p, t, opacity);
      } else if (p.type === 'inductor') {
        Components.drawInductor(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y, opacity);
      } else if (p.type === 'acsource') {
        Components.drawAcSource(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y, opacity);
      } else if (p.type === 'mtjsensor') {
        Components.drawMtjSensor(ctx, p, t, opacity, state.animT);
      } else if (p.type === 'scope') {
        Components.drawScopeProbe(ctx, p, t[0].x, t[0].y, opacity);
      } else if (p.type === 'toroid') {
        Components.drawToroid(ctx, p, t, opacity);
      }

      if (p.id === state.selectedPartId) {
        const { x: mx, y: my } = partCenter(p);
        ctx.save();
        ctx.strokeStyle = '#ffb020';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([3, 3]);
        ctx.beginPath();
        ctx.arc(mx, my, 22, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
      }

      // current-flow animation dots
      if (p.type !== 'potentiometer') {
        const I = currents.get(p.id);
        if (I && Math.abs(I) > 1e-6) {
          drawCurrentDots(t[0], t[1], I, p.type === 'wire' || (p.type === 'ywire' && p.style !== 'flat'));
        }
      }
    });

    // occupied-hole markers for whatever part is faded under the cursor —
    // so it's clear exactly which holes it's using before you place a wire
    if (state.hoverPart) {
      ctx.save();
      ctx.strokeStyle = '#6ea8e0';
      ctx.lineWidth = 2;
      state.hoverPart.terminals.forEach((h) => {
        ctx.beginPath();
        ctx.arc(h.x, h.y, 6, 0, Math.PI * 2);
        ctx.stroke();
      });
      ctx.restore();
    }

    // snap indicator: exactly which hole a placement tool will use next
    if (state.tool !== 'select' && state.hoverHole) {
      ctx.save();
      ctx.strokeStyle = '#ffdd55';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(state.hoverHole.x, state.hoverHole.y, 7, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }

    // pending placement preview
    if (state.pending.length && state.hoverHole) {
      ctx.save();
      ctx.strokeStyle = '#ffb02088';
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      const last = state.pending[state.pending.length - 1];
      ctx.moveTo(last.x, last.y);
      ctx.lineTo(state.hoverHole.x, state.hoverHole.y);
      ctx.stroke();
      ctx.restore();
    }
    state.pending.forEach((h) => {
      ctx.beginPath();
      ctx.arc(h.x, h.y, 5, 0, Math.PI * 2);
      ctx.strokeStyle = '#ffb020';
      ctx.lineWidth = 2;
      ctx.stroke();
    });

    updateHoverReadout();
  }

  function drawCurrentDots(p1, p2, I, isWire) {
    const speed = Math.max(0.3, Math.min(3, Math.abs(I) * 40));
    const dir = I >= 0 ? 1 : -1;
    const n = 2;
    for (let k = 0; k < n; k++) {
      let t = (state.animT * speed * dir + k / n) % 1;
      if (t < 0) t += 1;
      let x, y;
      if (isWire) {
        const midY = Math.min(p1.y, p2.y) - 18 - Math.min(40, Math.hypot(p2.x - p1.x, p2.y - p1.y) * 0.12);
        const cx = (p1.x + p2.x) / 2;
        x = (1 - t) * (1 - t) * p1.x + 2 * (1 - t) * t * cx + t * t * p2.x;
        y = (1 - t) * (1 - t) * p1.y + 2 * (1 - t) * t * midY + t * t * p2.y;
      } else {
        x = p1.x + (p2.x - p1.x) * t;
        y = p1.y + (p2.y - p1.y) * t;
      }
      ctx.beginPath();
      ctx.arc(x, y, 2.2, 0, Math.PI * 2);
      ctx.fillStyle = '#ffdd55';
      ctx.fill();
    }
  }

  const hoverEl = document.getElementById('hoverReadout');
  function updateHoverReadout() {
    if (!state.hoverHole) {
      hoverEl.textContent = 'Hover a hole to read its node voltage.';
      return;
    }
    const h = state.hoverHole;
    const uf = state.lastResult.uf;
    let v = 0;
    if (uf) {
      const root = uf.find(h.cellId);
      v = state.lastResult.voltages.get(root);
    }
    hoverEl.textContent = `Row ${h.row}, col ${h.col} · node ${h.cellId} · ${fmtV(v)}`;
  }

  const warnEl = document.getElementById('warnings');
  function updateWarnings() {
    const w = state.lastResult.warnings || [];
    if (!w.length) {
      warnEl.innerHTML = '<div class="ok">Circuit looks safe — no shorts, no over-current parts.</div>';
      return;
    }
    warnEl.innerHTML = w.map((m) => `<div class="warn">⚠ ${escapeHtml(m)}</div>`).join('');
  }
  function escapeHtml(s) {
    return s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  }

  requestAnimationFrame(frame);

  // debug/test hook (harmless, purely introspective — used by the automated
  // test harness and handy in the browser console while developing)
  window.__debugState = () => ({
    parts: state.parts.map((p) => ({ id: p.id, type: p.type, value: p.value, color: p.color, gauge: p.gauge, closed: p.closed, pos: p.pos, style: p.style, freq: p.freq, phase: p.phase, turnsPerSection: p.turnsPerSection, core: p.core, spacing: p.spacing, terminals: p.terminals.map((t) => ({ x: t.x, y: t.y, cellId: t.cellId })) })),
    voltages: Object.fromEntries(state.lastResult.voltages || []),
    currents: Object.fromEntries(state.lastResult.currents || []),
    warnings: state.lastResult.warnings,
  });
  window.__selectPartById = (id) => {
    state.selectedPartId = id;
    renderProps();
  };
  window.__toggleSwitchById = (id) => {
    const p = state.parts.find((x) => x.id === id);
    if (p) p.closed = !p.closed;
  };
  window.__debugToolValue = () => state.toolValue;
  window.__nodeVoltage = (cellId) => {
    const uf = state.lastResult.uf;
    return uf ? state.lastResult.voltages.get(uf.find(cellId)) : undefined;
  };
  // automation hook: step the simulation forward `seconds` of sim time in
  // one synchronous burst (default 1ms steps), instead of waiting on real
  // wall-clock animation frames. Lets a script (or an AI driving this page
  // headlessly) evaluate a candidate build's settled/transient behavior
  // near-instantly, then keep watching it run live afterward same as always
  // -- the same state.lastResult the render loop itself reads.
  window.__runFast = (seconds, dt) => {
    dt = dt || 1 / 1000;
    const steps = Math.max(1, Math.round(seconds / dt));
    const elements = toEngineElements();
    for (let i = 0; i < steps; i++) {
      state.animT += dt;
      state.lastResult = circuit.solve(elements, dt);
    }
    return {
      seconds,
      steps,
      voltages: Object.fromEntries(state.lastResult.voltages || []),
      currents: Object.fromEntries(state.lastResult.currents || []),
      warnings: state.lastResult.warnings,
    };
  };
})();
