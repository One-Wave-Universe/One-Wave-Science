/*
 * Musical-equipment lab presets.
 *
 * These deliberately load through the application's existing Save/Load path
 * instead of reaching into app.js's private state. That makes a preset prove
 * the same serialization -> board -> solver route a real saved circuit uses.
 * The user's own saved circuit is preserved: the temporary localStorage
 * payload is restored immediately after the synchronous Load click.
 */
(function () {
  'use strict';

  const SAVE_KEY = 'virtual-breadboard-save';
  const WIRE_COLORS = ['#2a6f4a', '#c94a4a', '#3f7fe0', '#d4af37', '#7a4a2a', '#a855f7'];
  const SCOPE_COLORS = ['#f4d35e', '#3ddc6b', '#4d8dff', '#ff6ec7'];

  function largeBoard() {
    return Board.build([{ size: 'large' }]);
  }

  function H(board, row, col) {
    const hole = board.holes.find((h) => h.row === row && h.col === col && h.boardIdx === 0);
    if (!hole) throw new Error(`Music preset hole not found: ${row}${col}`);
    return hole;
  }

  function normalizeParts(parts) {
    return parts.map((p, i) => Object.assign({
      id: `music${i + 1}`,
    }, p));
  }

  function loadPreset(parts) {
    const old = localStorage.getItem(SAVE_KEY);
    try {
      localStorage.setItem(SAVE_KEY, JSON.stringify({ layout: '1large', parts: normalizeParts(parts) }));
      document.getElementById('btnLoad').click();
    } finally {
      if (old == null) localStorage.removeItem(SAVE_KEY);
      else localStorage.setItem(SAVE_KEY, old);
    }
  }

  function wire(board, r1, c1, r2, c2, colorIdx) {
    return {
      type: 'wire', terminals: [H(board, r1, c1), H(board, r2, c2)],
      color: WIRE_COLORS[colorIdx % WIRE_COLORS.length], style: 'loop', gauge: 'standard',
    };
  }

  function scope(board, row, col, colorIdx) {
    return {
      type: 'scope', terminals: [H(board, row, col)], color: SCOPE_COLORS[colorIdx % SCOPE_COLORS.length], samples: [], coupling: 'DC',
    };
  }

  function diffScope(board, r1, c1, r2, c2, colorIdx) {
    return {
      type: 'diffscope', terminals: [H(board, r1, c1), H(board, r2, c2)],
      color: SCOPE_COLORS[colorIdx % SCOPE_COLORS.length], samples: [], coupling: 'DC',
    };
  }

  // Passive guitar electrical model: 4.7k pickup winding resistance + 1H
  // pickup inductance, 470pF cable capacitance and 1M amp/pedal input.
  // The scope at the jack shows the resonant instrument-source waveform.
  function guitarPickupParts() {
    const b = largeBoard();
    return [
      { type: 'acsource', terminals: [H(b, 'e', 5), H(b, 'f', 5)], value: 1, freq: 440, phase: 0 },
      { type: 'resistor', terminals: [H(b, 'a', 5), H(b, 'a', 10)], value: 4700 },
      { type: 'inductor', terminals: [H(b, 'b', 10), H(b, 'b', 15)], value: 1 },
      { type: 'capacitor', terminals: [H(b, 'c', 15), H(b, 'h', 15)], value: 470e-12 },
      { type: 'resistor', terminals: [H(b, 'd', 15), H(b, 'i', 15)], value: 1000000 },
      wire(b, 'h', 5, 'j', 15, 0),
      scope(b, 'e', 5, 0),
      scope(b, 'e', 15, 1),
    ];
  }

  // Classic hard-clipping pedal core: 3Vpk guitar-like source -> 10k drive
  // resistor -> anti-parallel silicon diodes. The output scope should show
  // both half-cycles clipped rather than a smaller clean sine.
  function diodeOverdriveParts() {
    const b = largeBoard();
    return [
      { type: 'acsource', terminals: [H(b, 'e', 5), H(b, 'f', 5)], value: 3, freq: 440, phase: 0 },
      { type: 'resistor', terminals: [H(b, 'a', 5), H(b, 'a', 15)], value: 10000 },
      { type: 'diode', terminals: [H(b, 'c', 15), H(b, 'h', 15)] },
      { type: 'diode', terminals: [H(b, 'i', 15), H(b, 'd', 15)] },
      wire(b, 'g', 5, 'j', 15, 1),
      scope(b, 'e', 5, 0),
      scope(b, 'e', 15, 1),
    ];
  }

  // Speaker/crossover load: 22uF series crossover cap feeding a simplified
  // 8-ohm + 1mH voice coil. This is intentionally a hard low-impedance load,
  // not an easy high-Z electronics demo.
  function speakerCrossoverParts() {
    const b = largeBoard();
    return [
      { type: 'acsource', terminals: [H(b, 'e', 5), H(b, 'f', 5)], value: 1, freq: 1000, phase: 0 },
      { type: 'capacitor', terminals: [H(b, 'a', 5), H(b, 'a', 10)], value: 22e-6 },
      { type: 'inductor', terminals: [H(b, 'b', 10), H(b, 'b', 15)], value: 1e-3 },
      { type: 'resistor', terminals: [H(b, 'c', 15), H(b, 'h', 15)], value: 8 },
      wire(b, 'g', 5, 'j', 15, 2),
      scope(b, 'e', 5, 0),
      scope(b, 'e', 15, 1),
    ];
  }

  // DI/transformer control: isolated 10:20 turn ferrite transformer with a
  // 1k secondary load and a differential scope across each winding.
  function diTransformerParts() {
    const b = largeBoard();
    return [
      { type: 'acsource', terminals: [H(b, 'e', 5), H(b, 'f', 5)], value: 1, freq: 1000, phase: 0 },
      {
        type: 'toroid',
        terminals: [H(b, 'a', 5), H(b, 'h', 5), H(b, 'a', 18), H(b, 'h', 18)],
        turnsPerSection: [10, 20], core: 'medium', gauge: 'standard', spacing: 'tight',
      },
      { type: 'resistor', terminals: [H(b, 'c', 18), H(b, 'i', 18)], value: 1000 },
      diffScope(b, 'b', 5, 'g', 5, 0),
      diffScope(b, 'b', 18, 'g', 18, 1),
    ];
  }

  // Professional-audio reference control: two equal sources 180 degrees
  // apart, equal 100-ohm legs and a 10k differential receiver load.
  function balancedLineParts() {
    const b = largeBoard();
    return [
      { type: 'acsource', terminals: [H(b, 'e', 5), H(b, 'f', 5)], value: 1, freq: 1000, phase: 0 },
      { type: 'acsource', terminals: [H(b, 'e', 8), H(b, 'f', 8)], value: 1, freq: 1000, phase: 180 },
      wire(b, 'g', 5, 'h', 8, 3),
      { type: 'resistor', terminals: [H(b, 'a', 5), H(b, 'a', 15)], value: 100 },
      { type: 'resistor', terminals: [H(b, 'b', 8), H(b, 'b', 20)], value: 100 },
      { type: 'resistor', terminals: [H(b, 'c', 15), H(b, 'c', 20)], value: 10000 },
      diffScope(b, 'd', 15, 'd', 20, 0),
    ];
  }

  const presets = [
    ['presetMusicPickup', 'Guitar pickup + cable', 'Pickup R/L, cable capacitance and 1M instrument input', guitarPickupParts],
    ['presetMusicClipper', 'Diode overdrive', 'Anti-parallel silicon clipping at 440Hz', diodeOverdriveParts],
    ['presetMusicSpeaker', 'Speaker + crossover', '22uF crossover into an 8-ohm + 1mH voice-coil load', speakerCrossoverParts],
    ['presetMusicDI', 'DI transformer', '10:20 ferrite transformer with a loaded isolated secondary', diTransformerParts],
    ['presetMusicBalanced', 'Balanced audio line', 'Equal source impedances, opposite phase, differential receiver load', balancedLineParts],
  ];

  function installButtons() {
    const host = document.querySelector('.presets');
    if (!host || document.getElementById('presetMusicPickup')) return;
    const heading = document.createElement('h3');
    heading.textContent = 'Music lab';
    host.appendChild(heading);
    presets.forEach(([id, label, title, build]) => {
      const button = document.createElement('button');
      button.id = id;
      button.textContent = label;
      button.title = title;
      button.addEventListener('click', () => loadPreset(build()));
      host.appendChild(button);
    });
  }

  installButtons();

  // Test/automation hook: the Electron smoke test uses this to prove every
  // shipping music preset loads through the real board path and simulates.
  window.__musicPresetIds = () => presets.map((p) => p[0]);
})();
