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
    selectedPartId: null,
    lastResult: { voltages: new Map(), currents: new Map(), warnings: [], uf: null },
    animT: 0,
    wireColorIdx: 0,
  };
  const WIRE_COLORS = ['#2a6f4a', '#c94a4a', '#3f7fe0', '#d4af37', '#7a4a2a', '#a855f7'];

  function H(row, col) {
    return board.holes.find((h) => h.row === row && h.col === col);
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
      } else if (p.type === 'potentiometer') {
        components.push({
          id: p.id, type: 'potentiometer', label: p.id,
          a: p.terminals[0].cellId, wiper: p.terminals[1].cellId, b: p.terminals[2].cellId,
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
      p.textContent = 'Click a hole, then click another hole to drop a jumper wire.';
      toolOptionsEl.appendChild(p);
    } else if (state.tool === 'potentiometer') {
      const p = document.createElement('p');
      p.className = 'hint';
      p.textContent = 'Click 3 holes in order: end A, wiper (middle), end B.';
      toolOptionsEl.appendChild(p);
    } else if (state.tool === 'select') {
      const p = document.createElement('p');
      p.className = 'hint';
      p.textContent = 'Click a switch to toggle it. Click any part to edit or delete it.';
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

  // ---------------- placing / interacting ----------------
  function cancelPending() {
    state.pending = [];
  }

  function terminalsNeeded(type) {
    const def = Components.PALETTE.find((p) => p.type === type);
    return def ? def.terminals : 2;
  }

  function commitPart(type, holes) {
    if (type === 'wire') {
      const color = WIRE_COLORS[state.wireColorIdx++ % WIRE_COLORS.length];
      addPart({ type: 'wire', terminals: holes.slice(0, 2), color });
    } else if (type === 'resistor') {
      addPart({ type: 'resistor', terminals: holes.slice(0, 2), value: state.toolValue.resistor });
    } else if (type === 'led') {
      addPart({ type: 'led', terminals: holes.slice(0, 2), color: state.toolValue.led });
    } else if (type === 'capacitor') {
      addPart({ type: 'capacitor', terminals: holes.slice(0, 2), value: state.toolValue.capacitor });
    } else if (type === 'battery') {
      addPart({ type: 'battery', terminals: holes.slice(0, 2), value: state.toolValue.battery });
    } else if (type === 'switch') {
      addPart({ type: 'switch', terminals: holes.slice(0, 2), closed: false });
    } else if (type === 'potentiometer') {
      addPart({ type: 'potentiometer', terminals: holes.slice(0, 3), value: 10000, pos: 0.5 });
    }
  }

  function hitTestPart(pos) {
    let best = null;
    let bestD = 12 * 12;
    state.parts.forEach((p) => {
      const t = p.terminals;
      if (t.length === 2) {
        const mx = (t[0].x + t[1].x) / 2;
        const my = (t[0].y + t[1].y) / 2;
        const d = (mx - pos.x) ** 2 + (my - pos.y) ** 2;
        if (d < bestD) {
          bestD = d;
          best = p;
        }
      } else if (t.length === 3) {
        const mx = t[1].x;
        const my = t[1].y - 14;
        const d = (mx - pos.x) ** 2 + (my - pos.y) ** 2;
        if (d < 20 * 20) {
          best = p;
          bestD = 0;
        }
      }
    });
    return best;
  }

  canvas.addEventListener('mousemove', (evt) => {
    const pos = mousePos(evt);
    state.hoverHole = Board.hitTest(board, pos.x, pos.y, 8);
  });
  canvas.addEventListener('mouseleave', () => {
    state.hoverHole = null;
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
  }, { passive: true });
  canvas.addEventListener('touchmove', (evt) => {
    const pos = touchPos(evt);
    state.hoverHole = Board.hitTest(board, pos.x, pos.y, 12);
  }, { passive: true });

  canvas.addEventListener('click', (evt) => {
    const pos = mousePos(evt);
    if (state.tool === 'select') {
      const part = hitTestPart(pos);
      if (part && part.type === 'switch') {
        part.closed = !part.closed;
      }
      state.selectedPartId = part ? part.id : null;
      renderProps();
      return;
    }
    const hole = Board.hitTest(board, pos.x, pos.y, 11);
    if (!hole) return;
    const need = terminalsNeeded(state.tool);
    if (state.pending.length && state.pending[state.pending.length - 1].x === hole.x && state.pending[state.pending.length - 1].y === hole.y) {
      return; // clicked the exact same hole again, ignore
    }
    state.pending.push(hole);
    if (state.pending.length >= need) {
      commitPart(state.tool, state.pending);
      state.pending = [];
    }
  });

  window.addEventListener('keydown', (evt) => {
    if (evt.key === 'Escape') {
      cancelPending();
      selectTool('select');
    }
  });

  // ---------------- properties panel ----------------
  const propsEl = document.getElementById('props');
  function renderProps() {
    propsEl.innerHTML = '';
    const part = state.parts.find((p) => p.id === state.selectedPartId);
    if (!part) {
      propsEl.innerHTML = '<p class="hint">Select a placed part to inspect or edit it.</p>';
      return;
    }
    const title = document.createElement('h3');
    title.textContent = part.type[0].toUpperCase() + part.type.slice(1) + ' · ' + part.id;
    propsEl.appendChild(title);

    if (part.type === 'resistor') {
      propsEl.appendChild(makeSelect('Resistance', Components.RESISTOR_VALUES.map((v) => [v, Components.formatOhms(v)]), part.value, (v) => (part.value = Number(v))));
    } else if (part.type === 'capacitor') {
      propsEl.appendChild(makeSelect('Capacitance', Components.CAPACITOR_VALUES.map((v) => [v.farads, v.label]), part.value, (v) => (part.value = Number(v))));
    } else if (part.type === 'battery') {
      propsEl.appendChild(makeSelect('Voltage', Components.BATTERY_VALUES.map((v) => [v, v + ' V']), part.value, (v) => (part.value = Number(v))));
    } else if (part.type === 'led') {
      const wrap = document.createElement('div');
      wrap.className = 'swatches';
      Components.LED_COLORS.forEach((c) => {
        const b = document.createElement('button');
        b.className = 'swatch' + (part.color === c ? ' active' : '');
        b.style.background = Components.LED_HEX[c];
        b.addEventListener('click', () => {
          part.color = c;
          renderProps();
        });
        wrap.appendChild(b);
      });
      propsEl.appendChild(labeled('Color', wrap));
    } else if (part.type === 'switch') {
      const btn = document.createElement('button');
      btn.className = 'action-btn';
      btn.textContent = part.closed ? 'Open switch' : 'Close switch';
      btn.addEventListener('click', () => {
        part.closed = !part.closed;
        renderProps();
      });
      propsEl.appendChild(btn);
    } else if (part.type === 'potentiometer') {
      const range = document.createElement('input');
      range.type = 'range';
      range.min = '0';
      range.max = '100';
      range.value = String(Math.round((part.pos ?? 0.5) * 100));
      range.addEventListener('input', () => (part.pos = Number(range.value) / 100));
      propsEl.appendChild(labeled('Wiper position', range));
      propsEl.appendChild(makeSelect('Total resistance', Components.RESISTOR_VALUES.map((v) => [v, Components.formatOhms(v)]), part.value, (v) => (part.value = Number(v))));
    }

    const readout = document.createElement('div');
    readout.className = 'readout';
    const I = state.lastResult.currents.get(part.id);
    const uf = state.lastResult.uf;
    if (uf) {
      const va = state.lastResult.voltages.get(uf.find(part.terminals[0].cellId));
      const vb = state.lastResult.voltages.get(uf.find(part.terminals[part.type === 'potentiometer' ? 2 : 1].cellId));
      readout.innerHTML = `
        <div><span>V(A)</span><b>${fmtV(va)}</b></div>
        <div><span>V(B)</span><b>${fmtV(vb)}</b></div>
        <div><span>ΔV</span><b>${fmtV(va - vb)}</b></div>
        <div><span>Current</span><b>${fmtI(I)}</b></div>
      `;
    }
    propsEl.appendChild(readout);

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
  function loadPresetLedResistor() {
    state.parts = [];
    circuit.reset();
    addPart({ type: 'battery', terminals: [H('e', 10), H('f', 10)], value: 5 });
    addPart({ type: 'resistor', terminals: [H('c', 10), H('c', 15)], value: 220 });
    addPart({ type: 'led', terminals: [H('a', 15), H('j', 15)], color: 'red' });
    const color = WIRE_COLORS[state.wireColorIdx++ % WIRE_COLORS.length];
    addPart({ type: 'wire', terminals: [H('h', 10), H('h', 15)], color });
  }
  function loadPresetShort() {
    state.parts = [];
    circuit.reset();
    addPart({ type: 'battery', terminals: [H('e', 10), H('f', 10)], value: 9 });
    const color = WIRE_COLORS[state.wireColorIdx++ % WIRE_COLORS.length];
    addPart({ type: 'wire', terminals: [H('c', 10), H('h', 10)], color });
  }
  function loadPresetRC() {
    state.parts = [];
    circuit.reset();
    addPart({ type: 'battery', terminals: [H('e', 5), H('f', 5)], value: 9 });
    addPart({ type: 'switch', terminals: [H('b', 5), H('b', 8)], closed: false });
    addPart({ type: 'resistor', terminals: [H('c', 8), H('c', 20)], value: 100000 });
    addPart({ type: 'capacitor', terminals: [H('d', 20), H('g', 20)], value: 100e-6 });
    const color = WIRE_COLORS[state.wireColorIdx++ % WIRE_COLORS.length];
    addPart({ type: 'wire', terminals: [H('i', 5), H('i', 20)], color });
  }
  document.getElementById('presetLed').addEventListener('click', () => { loadPresetLedResistor(); selectTool('select'); });
  document.getElementById('presetShort').addEventListener('click', () => { loadPresetShort(); selectTool('select'); });
  document.getElementById('presetRC').addEventListener('click', () => { loadPresetRC(); selectTool('select'); });

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
      if (p.type === 'wire') {
        Components.drawWire(ctx, t[0].x, t[0].y, t[1].x, t[1].y, p.color);
      } else if (p.type === 'resistor') {
        Components.drawResistor(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y);
      } else if (p.type === 'led') {
        const I = currents.get(p.id) || 0;
        const glow = Math.min(1, I * 60);
        Components.drawLed(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y, glow);
      } else if (p.type === 'capacitor') {
        Components.drawCapacitor(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y);
      } else if (p.type === 'battery') {
        Components.drawBattery(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y);
      } else if (p.type === 'switch') {
        Components.drawSwitch(ctx, p, t[0].x, t[0].y, t[1].x, t[1].y);
      } else if (p.type === 'potentiometer') {
        Components.drawPotentiometer(ctx, p, { a: t[0], wiper: t[1], b: t[2] });
      }

      if (p.id === state.selectedPartId) {
        const mx = t.length === 3 ? t[1].x : (t[0].x + t[1].x) / 2;
        const my = (t.length === 3 ? t[1].y - 14 : (t[0].y + t[1].y) / 2);
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
          drawCurrentDots(t[0], t[1], I, p.type === 'wire');
        }
      }
    });

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
    parts: state.parts.map((p) => ({ id: p.id, type: p.type, value: p.value, color: p.color, closed: p.closed, pos: p.pos, terminals: p.terminals.map((t) => ({ x: t.x, y: t.y, cellId: t.cellId })) })),
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
})();
