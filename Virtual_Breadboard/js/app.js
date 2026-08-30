(function () {
  'use strict';

  const board = Board.build();
  const circuit = new CircuitEngine.Circuit();

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
    },
    pending: [],
    hoverHole: null,
    hoverPart: null,
    selectedPartId: null,
    lastResult: { voltages: new Map(), currents: new Map(), warnings: [], uf: null },
    animT: 0,
    wireColorIdx: 0,
  };
  const WIRE_COLORS = ['#2a6f4a', '#c94a4a', '#3f7fe0', '#d4af37', '#7a4a2a', '#a855f7'];

  function H(row, col) {
    return board.holes.find((h) => h.row === row && h.col === col);
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
    if (c + 2 > Board.COLS) return null;
    return [
      H(anchor.row, c), H(anchor.row, c + 1), H(anchor.row, c + 2),
      H(mirrorRow, c), H(mirrorRow, c + 1), H(mirrorRow, c + 2),
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

  function toEngineElements() {
    const wires = [];
    const components = [];
    state.parts.forEach((p) => {
      if (p.type === 'wire') {
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

  const toolOptionsEl = document.getElementById('toolOptions');
  function renderToolOptions() {
    toolOptionsEl.innerHTML = '';
    if (state.tool === 'resistor') {
      toolOptionsEl.appendChild(makeSelect('Value', Components.RESISTOR_VALUES.map((v) => [v, Components.formatOhms(v)]), state.toolValue.resistor, (v) => (state.toolValue.resistor = Number(v))));
    } else if (state.tool === 'capacitor') {
      toolOptionsEl.appendChild(makeSelect('Value', Components.CAPACITOR_VALUES.map((v) => [v.farads, v.label]), state.toolValue.capacitor, (v) => (state.toolValue.capacitor = Number(v))));
    } else if (state.tool === 'led') {
      const wrap = document.createElement('div');
      wrap.className = 'swatches';
      Components.LED_COLORS.forEach((c) => {
        const b = document.createElement('button');
        b.className = 'swatch' + (state.toolValue.led === c ? ' active' : '');
        b.style.background = Components.LED_HEX[c];
        b.title = c;
        b.addEventListener('click', () => {
          state.toolValue.led = c;
          renderToolOptions();
        });
        wrap.appendChild(b);
      });
      toolOptionsEl.appendChild(labeled('LED color', wrap));
    } else if (state.tool === 'battery') {
      toolOptionsEl.appendChild(makeSelect('Voltage', Components.BATTERY_VALUES.map((v) => [v, v + ' V']), state.toolValue.battery, (v) => (state.toolValue.battery = Number(v))));
    } else if (state.tool === 'wire') {
      const p = document.createElement('p');
      p.className = 'hint';
      p.textContent = 'Click a hole, then click another hole to drop a jumper wire. Right-click a placed wire to change its color or style.';
      toolOptionsEl.appendChild(p);
    } else if (state.tool === 'ywire') {
      const p = document.createElement('p');
      p.className = 'hint';
      p.textContent = 'One physical wire bridging 2 rows, forked to 2 holes at each end — good for a ground/rail tap. Click 2 holes for one end, then 2 holes for the other end.';
      toolOptionsEl.appendChild(p);
    } else if (state.tool === 'diode') {
      const p = document.createElement('p');
      p.className = 'hint';
      p.textContent = 'Click the anode, then the cathode (banded end).';
      toolOptionsEl.appendChild(p);
    } else if (state.tool === 'pushbutton') {
      const p = document.createElement('p');
      p.className = 'hint';
      p.textContent = 'Click two holes. Hold it down on the board (or in the Inspector) to close the circuit.';
      toolOptionsEl.appendChild(p);
    } else if (state.tool === 'potentiometer') {
      const p = document.createElement('p');
      p.className = 'hint';
      p.textContent = 'Click one hole in either bank (not a rail) — a real 6-pin trimmer straddles the center channel, so the other 5 pins are placed for you.';
      toolOptionsEl.appendChild(p);
    } else if (state.tool === 'select') {
      const p = document.createElement('p');
      p.className = 'hint';
      p.textContent = 'Click a switch to toggle it, or hold down a pushbutton. Click any part to edit or delete it.';
      toolOptionsEl.appendChild(p);
    }
  }
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
      if (Number(v) === Number(value)) opt.selected = true;
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
    const def = Components.PALETTE.find((p) => p.type === type);
    return def ? def.terminals : 2;
  }

  // generator: given a tool + the holes clicked, decide what the resulting
  // part looks like. Pure — no state mutation, easy to test/reason about on
  // its own. Wire color selection is the one stateful exception (a counter
  // for cosmetic color-cycling), so the caller resolves it and passes it in.
  function buildPart(type, holes, opts) {
    if (type === 'wire') return { type: 'wire', terminals: holes.slice(0, 2), color: opts.wireColor, style: 'loop' };
    if (type === 'ywire') return { type: 'ywire', terminals: holes.slice(0, 4), color: opts.wireColor, style: 'loop' };
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
      return { type: 'potentiometer', terminals, value: 10000, pos: 0.5 };
    }
    return null;
  }

  // executor: picks the next cosmetic wire color (the one bit of state this
  // path needs) and commits the generated part into the board.
  function nextWireColor() {
    return WIRE_COLORS[state.wireColorIdx++ % WIRE_COLORS.length];
  }

  function commitPart(type, holes) {
    const part = buildPart(type, holes, {
      resistorValue: state.toolValue.resistor,
      capacitorValue: state.toolValue.capacitor,
      ledColor: state.toolValue.led,
      batteryValue: state.toolValue.battery,
      wireColor: type === 'wire' || type === 'ywire' ? nextWireColor() : undefined,
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
      if (t.length === 6) {
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
      } else if (t.length === 2) {
        if (distToSegment(pos.x, pos.y, t[0].x, t[0].y, t[1].x, t[1].y) < 14) return p;
      }
    }
    return null;
  }

  // where the selection ring / occupied-hole body is centered for a part
  function partCenter(p) {
    const t = p.terminals;
    if (t.length === 6) return { x: (t[1].x + t[4].x) / 2, y: (t[1].y + t[4].y) / 2 };
    if (t.length === 4) {
      const [j1, j2] = Components.yWireJunctions(t);
      return { x: (j1.x + j2.x) / 2, y: (j1.y + j2.y) / 2 };
    }
    return { x: (t[0].x + t[1].x) / 2, y: (t[0].y + t[1].y) / 2 };
  }

  // executor: the state changes behind a momentary pushbutton press/release
  function pressPushbutton(pos) {
    const part = hitTestPart(pos);
    if (part && part.type === 'pushbutton') part.closed = true;
  }
  function releaseAllPushbuttons() {
    state.parts.forEach((p) => {
      if (p.type === 'pushbutton') p.closed = false;
    });
  }

  canvas.addEventListener('mousemove', (evt) => {
    const pos = mousePos(evt);
    state.hoverHole = Board.hitTest(board, pos.x, pos.y, 8);
    state.hoverPart = hitTestPart(pos);
  });
  canvas.addEventListener('mouseleave', () => {
    state.hoverHole = null;
    state.hoverPart = null;
    releaseAllPushbuttons();
  });
  canvas.addEventListener('mousedown', (evt) => {
    if (state.tool === 'select') pressPushbutton(mousePos(evt));
  });
  canvas.addEventListener('mouseup', releaseAllPushbuttons);

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
    if (state.tool === 'select') pressPushbutton(pos);
  }, { passive: true });
  canvas.addEventListener('touchmove', (evt) => {
    const pos = touchPos(evt);
    state.hoverHole = Board.hitTest(board, pos.x, pos.y, 12);
    state.hoverPart = hitTestPart(pos);
  }, { passive: true });
  canvas.addEventListener('touchend', releaseAllPushbuttons, { passive: true });

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
  canvas.addEventListener('click', (evt) => handleCanvasClick(mousePos(evt)));

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
    } else if (part.type === 'led') {
      const wrap = document.createElement('div');
      wrap.className = 'swatches';
      Components.LED_COLORS.forEach((c) => {
        const b = document.createElement('button');
        b.className = 'swatch' + (part.color === c ? ' active' : '');
        b.style.background = Components.LED_HEX[c];
        b.addEventListener('click', () => {
          part.color = c;
          notify();
        });
        wrap.appendChild(b);
      });
      container.appendChild(labeled('Color', wrap));
    } else if (part.type === 'switch') {
      const btn = document.createElement('button');
      btn.className = 'action-btn';
      btn.textContent = part.closed ? 'Open switch' : 'Close switch';
      btn.addEventListener('click', () => {
        part.closed = !part.closed;
        notify();
      });
      container.appendChild(btn);
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
      const range = document.createElement('input');
      range.type = 'range';
      range.min = '0';
      range.max = '100';
      range.value = String(Math.round((part.pos ?? 0.5) * 100));
      range.addEventListener('input', () => (part.pos = Number(range.value) / 100));
      container.appendChild(labeled('Wiper position', range));
      container.appendChild(makeSelect('Total resistance', Components.RESISTOR_VALUES.map((v) => [v, Components.formatOhms(v)]), part.value, (v) => (part.value = Number(v))));
    } else if (part.type === 'wire' || part.type === 'ywire') {
      const wrap = document.createElement('div');
      wrap.className = 'swatches';
      Components.WIRE_COLOR_CHOICES.forEach((c) => {
        const b = document.createElement('button');
        b.className = 'swatch' + (part.color === c ? ' active' : '');
        b.style.background = c;
        b.addEventListener('click', () => {
          part.color = c;
          notify();
        });
        wrap.appendChild(b);
      });
      container.appendChild(labeled('Color', wrap));

      const styleWrap = document.createElement('div');
      styleWrap.className = 'seg-toggle';
      [['loop', 'Looped'], ['flat', 'Flat']].forEach(([val, label]) => {
        const b = document.createElement('button');
        b.className = 'seg-btn' + ((part.style || 'loop') === val ? ' active' : '');
        b.textContent = label;
        b.addEventListener('click', () => {
          part.style = val;
          notify();
        });
        styleWrap.appendChild(b);
      });
      container.appendChild(labeled('Style', styleWrap));
    }
  }

  function renderProps() {
    propsEl.innerHTML = '';
    const part = state.parts.find((p) => p.id === state.selectedPartId);
    if (!part) {
      propsEl.innerHTML = '<p class="hint">Select a placed part to inspect or edit it.</p>';
      currentReadoutEl = null;
      return;
    }
    const title = document.createElement('h3');
    title.textContent = partTitle(part);
    propsEl.appendChild(title);

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
    const va = state.lastResult.voltages.get(uf.find(part.terminals[0].cellId));
    const vb = state.lastResult.voltages.get(uf.find(part.terminals[part.type === 'potentiometer' ? 2 : 1].cellId));
    currentReadoutEl.innerHTML = `
      <div><span>V(A)</span><b>${fmtV(va)}</b></div>
      <div><span>V(B)</span><b>${fmtV(vb)}</b></div>
      <div><span>ΔV</span><b>${fmtV(va - vb)}</b></div>
      <div><span>Current</span><b>${fmtI(I)}</b></div>
    `;
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
  document.getElementById('btnSave').addEventListener('click', () => {
    try {
      localStorage.setItem('virtual-breadboard-save', JSON.stringify(state.parts));
      flashStatus('Saved to browser storage.');
    } catch (e) {
      flashStatus('Could not save: ' + e.message);
    }
  });
  document.getElementById('btnLoad').addEventListener('click', () => {
    try {
      const raw = localStorage.getItem('virtual-breadboard-save');
      if (!raw) return flashStatus('No saved build found.');
      const loaded = JSON.parse(raw);
      let maxId = 0;
      loaded.forEach((p) => {
        const n = parseInt(String(p.id).slice(1), 10);
        if (!Number.isNaN(n)) maxId = Math.max(maxId, n);
      });
      state.nextId = maxId + 1;
      state.parts = loaded;
      circuit.reset();
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
          color: isWire ? nextWireColor() : p.color,
          closed: !!p.closed,
          pos: p.type === 'potentiometer' ? 0.5 : undefined,
          style: isWire ? 'loop' : undefined,
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

  // ---------------- main loop ----------------
  let lastT = performance.now();
  function frame(now) {
    let dt = (now - lastT) / 1000;
    lastT = now;
    dt = Math.min(Math.max(dt, 0), 0.05);
    state.animT += dt;

    const elements = toEngineElements();
    state.lastResult = circuit.solve(elements, dt);

    render(dt);
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
        Components.drawWire(ctx, t[0].x, t[0].y, t[1].x, t[1].y, p.color, opacity, p.style);
      } else if (p.type === 'ywire') {
        Components.drawYWire(ctx, t, p.color, opacity, p.style);
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
    parts: state.parts.map((p) => ({ id: p.id, type: p.type, value: p.value, color: p.color, closed: p.closed, pos: p.pos, style: p.style, terminals: p.terminals.map((t) => ({ x: t.x, y: t.y, cellId: t.cellId })) })),
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
  window.__nodeVoltage = (cellId) => {
    const uf = state.lastResult.uf;
    return uf ? state.lastResult.voltages.get(uf.find(cellId)) : undefined;
  };
})();
