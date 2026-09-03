#!/usr/bin/env node
/*
 * Headless CLI: run a circuit spec (the same JSON shape the in-app "Ask AI
 * to build" panel produces and validates -- js/ai.js's validateSpec) through
 * the real circuit engine and print the result as JSON. No browser/DOM
 * needed, so an external test harness (e.g. a Python script on another
 * machine) can shell out to `node simulate.js` and get real physics back,
 * without duplicating any of the circuit engine in a second language.
 *
 * Usage:
 *   node simulate.js < spec.json
 *   node simulate.js spec.json
 *
 * Input shape:
 *   {
 *     "layout": "1large",             // optional, any Board layout key (see LAYOUT_PRESETS below); default "1large"
 *     "parts": [ ... ],                // same shape/rules as js/ai.js's system prompt documents
 *     "sim": { "seconds": 1, "dt": 0.001, "sampleEvery": 0.05 }   // all optional
 *   }
 *
 * Output shape (success):
 *   {
 *     "ok": true,
 *     "errors": [],
 *     "final": { "voltages": {...}, "currents": {...}, "warnings": [...] },
 *     "samples": [ { "t": 0.05, "voltages": {...}, "currents": {...}, "warnings": [...] }, ... ]  // only if sim.sampleEvery given
 *   }
 * Output shape (failure -- bad spec or unresolvable terminal), exit code 1:
 *   { "ok": false, "errors": [ "..." ] }
 */
const fs = require('fs');

const CircuitEngine = require('./js/circuit.js');
const Board = require('./js/board.js');
const Components = require('./js/components.js');
const AIBuilder = require('./js/ai.js');

const LAYOUT_PRESETS = {
  '1large': [{ size: 'large' }],
  '2large': [{ size: 'large' }, { size: 'large' }],
  '2small': [{ size: 'small' }, { size: 'small' }],
  '3small': [{ size: 'small' }, { size: 'small' }, { size: 'small' }],
  '4small': [{ size: 'small' }, { size: 'small' }, { size: 'small' }, { size: 'small' }],
  '1large1small': [{ size: 'large' }, { size: 'small' }],
  '1large2small': [{ size: 'large' }, { size: 'small' }, { size: 'small' }],
};

function readInput() {
  const argPath = process.argv[2];
  const raw = argPath ? fs.readFileSync(argPath, 'utf8') : fs.readFileSync(0, 'utf8');
  return JSON.parse(raw);
}

function fail(errors) {
  console.log(JSON.stringify({ ok: false, errors }, null, 2));
  process.exit(1);
}

function H(board, row, col, boardIdx) {
  const bi = boardIdx == null ? 0 : boardIdx;
  return board.holes.find((h) => h.row === row && h.col === col && h.boardIdx === bi);
}

// ported from js/app.js -- pure geometry, no DOM, safe to duplicate here
// rather than trying to share one copy between a browser file and this CLI
const POT_MIRROR_ROW = { a: 'f', b: 'g', c: 'h', d: 'i', e: 'j', f: 'a', g: 'b', h: 'c', i: 'd', j: 'e' };
function derivePotentiometerHoles(board, anchor) {
  if (!anchor) return null;
  const mirrorRow = POT_MIRROR_ROW[anchor.row];
  if (!mirrorRow) return null;
  const c = anchor.col;
  const bi = anchor.boardIdx || 0;
  const boardMeta = board.boards[bi];
  if (!boardMeta || c + 2 > boardMeta.cols) return null;
  return [
    H(board, anchor.row, c, bi), H(board, anchor.row, c + 1, bi), H(board, anchor.row, c + 2, bi),
    H(board, mirrorRow, c, bi), H(board, mirrorRow, c + 1, bi), H(board, mirrorRow, c + 2, bi),
  ];
}

// ported from js/app.js's deriveTlv3202Holes -- a real 8-pin DIP-8
// straddling the center channel, pins numbered going around the package
function deriveTlv3202Holes(board, anchor) {
  if (!anchor || anchor.row !== 'e') return null;
  const c = anchor.col;
  const bi = anchor.boardIdx || 0;
  const boardMeta = board.boards[bi];
  if (!boardMeta || c + 3 > boardMeta.cols) return null;
  return [
    H(board, 'e', c, bi), H(board, 'e', c + 1, bi), H(board, 'e', c + 2, bi), H(board, 'e', c + 3, bi),
    H(board, 'f', c + 3, bi), H(board, 'f', c + 2, bi), H(board, 'f', c + 1, bi), H(board, 'f', c, bi),
  ];
}

// ported from js/app.js's specPartsToBoardParts -- turns a validated AI
// spec's {row,col,board} terminal references into real holes on this
// board, and renames/defaults fields exactly like the in-app AI-build path
// does (the AI spec's toroid "turns" becomes the board part's
// "turnsPerSection", with core/gauge/spacing defaulted when the AI left
// them out). "board" on a terminal (0-indexed, default board 0) is
// threaded straight through to H()'s boardIdx argument -- a part assigned
// to board 1 must resolve to a real hole on board 1, not silently fall
// back to board 0.
function resolveTerminals(board, specParts) {
  const errors = [];
  const parts = specParts.map((p, i) => {
    const terminals = p.type === 'potentiometer'
      ? derivePotentiometerHoles(board, H(board, p.terminals[0].row, p.terminals[0].col, p.terminals[0].board))
      : p.type === 'comparator'
      ? deriveTlv3202Holes(board, H(board, p.terminals[0].row, p.terminals[0].col, p.terminals[0].board))
      : p.terminals.map((t) => H(board, t.row, t.col, t.board));
    if (!terminals || terminals.some((t) => !t)) {
      errors.push('part ' + i + ' (' + p.type + '): a terminal does not resolve to a real hole on layout "' + (board.layoutKey || '') + '"');
      return null;
    }
    return {
      type: p.type,
      value: p.value,
      color: p.color,
      closed: !!p.closed,
      pos: p.type === 'potentiometer' ? 0.5 : undefined,
      freq: p.freq,
      phase: p.phase,
      turnsPerSection: p.type === 'toroid' ? p.turns : undefined,
      turnsPerWinding: p.type === 'memorycore' ? p.turns : undefined,
      core: p.type === 'toroid' ? (p.core || 'medium') : p.type === 'memorycore' ? (p.core || 'small') : undefined,
      gauge: p.type === 'toroid' || p.type === 'memorycore' ? (p.gauge || 'standard') : undefined,
      spacing: p.type === 'toroid' ? (p.spacing || 'normal') : undefined,
      terminals,
      id: p.type[0] + (i + 1),
    };
  });
  const resolved = parts.filter(Boolean);
  // one component lead per physical hole -- same real-bench collision
  // check js/app.js's specPartsToBoardParts applies to an AI-generated
  // layout, ported here so a headless spec gets the identical validation.
  const seen = new Map(); // "x,y" -> part index (into `resolved`) that claimed it first
  resolved.forEach((p, i) => {
    p.terminals.forEach((t) => {
      const key = t.x + ',' + t.y;
      const first = seen.get(key);
      if (first != null && first !== i) {
        errors.push('part ' + i + ' (' + p.type + ') and part ' + first + ' (' + resolved[first].type + ') both claim the same physical hole (' + t.cellId + ') -- a real breadboard hole only fits one lead');
      }
      seen.set(key, i);
    });
  });
  return { parts: resolved, errors };
}

// ported verbatim from js/app.js's toroidWindings/toEngineElements
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

// ported verbatim from js/app.js's memoryCoreWindings
function memoryCoreWindings(p) {
  const coreDef = Components.MEMORY_CORES[p.core] || Components.MEMORY_CORES.small;
  const ohmsPerM = Components.WIRE_GAUGE_OHMS_PER_M[p.gauge] || Components.WIRE_GAUGE_OHMS_PER_M.standard;
  return p.turnsPerWinding.map((turns, i) => ({
    a: p.terminals[i * 2].cellId,
    b: p.terminals[i * 2 + 1].cellId,
    N: turns,
    R: turns * coreDef.meanTurnLen * ohmsPerM,
  }));
}

function toEngineElements(parts) {
  const wires = [];
  const components = [];
  parts.forEach((p) => {
    if (p.type === 'scope' || p.type === 'diffscope') {
      // zero-load probe(s), never enter the physics
    } else if (p.type === 'wire') {
      wires.push({ a: p.terminals[0].cellId, b: p.terminals[1].cellId });
    } else if (p.type === 'ywire') {
      const t = p.terminals;
      wires.push({ a: t[0].cellId, b: t[1].cellId });
      wires.push({ a: t[0].cellId, b: t[2].cellId });
      wires.push({ a: t[2].cellId, b: t[3].cellId });
    } else if (p.type === 'potentiometer') {
      const t = p.terminals;
      wires.push({ a: t[0].cellId, b: t[3].cellId });
      wires.push({ a: t[1].cellId, b: t[4].cellId });
      wires.push({ a: t[2].cellId, b: t[5].cellId });
      components.push({
        id: p.id, type: 'potentiometer', label: p.id,
        a: t[0].cellId, wiper: t[1].cellId, b: t[2].cellId,
        value: p.value, pos: p.pos != null ? p.pos : 0.5,
      });
    } else if (p.type === 'vgnd') {
      components.push({ id: p.id, type: 'vgnd', label: p.id, a: p.terminals[0].cellId, b: p.terminals[1].cellId, out: p.terminals[2].cellId });
    } else if (p.type === 'nmos' || p.type === 'pmos') {
      components.push({ id: p.id, type: p.type, label: p.id, gate: p.terminals[0].cellId, drain: p.terminals[1].cellId, source: p.terminals[2].cellId, value: p.value });
    } else if (p.type === 'acsource') {
      components.push({ id: p.id, type: 'acsource', label: p.id, a: p.terminals[0].cellId, b: p.terminals[1].cellId, value: p.value, freq: p.freq || 1, phase: p.phase || 0 });
    } else if (p.type === 'mtjsensor') {
      components.push({ id: p.id, type: 'mtjsensor', label: p.id, ref: p.terminals[0].cellId, sin: p.terminals[1].cellId, cos: p.terminals[2].cellId, value: p.value, freq: p.freq || 1, phase: p.phase || 0 });
    } else if (p.type === 'toroid') {
      components.push({
        id: p.id, type: 'toroid', label: p.id,
        windings: toroidWindings(p),
        coupling: p.turnsPerSection.length > 1 ? (Components.TOROID_SPACING_COUPLING[p.spacing] || 0.9) : 0,
      });
    } else if (p.type === 'comparator') {
      const t = p.terminals;
      components.push({
        id: p.id, type: 'comparator', label: p.id,
        out1: t[0].cellId, in1m: t[1].cellId, in1p: t[2].cellId, gnd: t[3].cellId,
        in2p: t[4].cellId, in2m: t[5].cellId, out2: t[6].cellId, vcc: t[7].cellId,
      });
    } else if (p.type === 'memorycore') {
      const coreDef = Components.MEMORY_CORES[p.core] || Components.MEMORY_CORES.small;
      components.push({
        id: p.id, type: 'memorycore', label: p.id,
        windings: memoryCoreWindings(p),
        hcAmpTurns: coreDef.hcAmpTurns, phiSat: coreDef.phiSat, switchTau: coreDef.switchTau,
      });
    } else {
      components.push({ id: p.id, type: p.type, label: p.id, a: p.terminals[0].cellId, b: p.terminals[1].cellId, value: p.value, color: p.color, closed: !!p.closed });
    }
  });
  return { wires, components };
}

function snapshot(result) {
  const out = {
    voltages: Object.fromEntries((result && result.voltages) || []),
    currents: Object.fromEntries((result && result.currents) || []),
    warnings: (result && result.warnings) || [],
  };
  if (result && result.mosfetStates && result.mosfetStates.size) {
    out.mosfetStates = Object.fromEntries(result.mosfetStates);
  }
  if (result && result.coreStates && result.coreStates.size) {
    out.coreStates = Object.fromEntries(result.coreStates);
  }
  if (result && result.comparatorStates && result.comparatorStates.size) {
    out.comparatorStates = Object.fromEntries(result.comparatorStates);
  }
  return out;
}

function main() {
  let input;
  try {
    input = readInput();
  } catch (e) {
    return fail(['Could not read/parse input JSON: ' + e.message]);
  }

  const { ok, errors, parts: validatedParts } = AIBuilder.validateSpec(input);
  if (!ok) return fail(errors);

  const layoutKey = input.layout || '1large';
  const layout = LAYOUT_PRESETS[layoutKey];
  if (!layout) return fail(['unknown layout "' + layoutKey + '"']);

  const board = Board.build(layout);
  board.layoutKey = layoutKey;

  const { parts, errors: holeErrors } = resolveTerminals(board, validatedParts);
  if (holeErrors.length) return fail(holeErrors);

  const elements = toEngineElements(parts);
  const circuit = new CircuitEngine.Circuit();

  const sim = input.sim || {};
  const seconds = sim.seconds != null ? sim.seconds : 1;
  const dt = sim.dt != null ? sim.dt : 0.001;
  const sampleEvery = sim.sampleEvery || null;
  const steps = Math.max(1, Math.round(seconds / dt));

  const samples = [];
  let t = 0;
  let lastResult = null;
  let nextSampleAt = sampleEvery || Infinity;
  for (let i = 0; i < steps; i++) {
    t += dt;
    lastResult = circuit.solve(elements, dt);
    if (t >= nextSampleAt) {
      samples.push(Object.assign({ t: Number(t.toFixed(6)) }, snapshot(lastResult)));
      nextSampleAt += sampleEvery;
    }
  }

  const out = { ok: true, errors: [], final: snapshot(lastResult) };
  if (sampleEvery) out.samples = samples;
  console.log(JSON.stringify(out, null, 2));
}

// run as a CLI when invoked directly (`node simulate.js`); when required
// as a module (the automated test suite does this) just export the
// internals below and skip reading stdin/argv or printing to stdout.
if (require.main === module) main();

module.exports = {
  LAYOUT_PRESETS, H, derivePotentiometerHoles, deriveTlv3202Holes,
  resolveTerminals, memoryCoreWindings, toEngineElements, snapshot, main,
};
