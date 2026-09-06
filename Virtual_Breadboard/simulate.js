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
 *
 * Monte Carlo tolerance mode: add a "monteCarlo" key to the input --
 *   "monteCarlo": {
 *     "trials": 200,               // how many randomized runs, default 100
 *     "seed": 12345,                // optional, for a reproducible sequence
 *     "watch": [                    // optional, values to collect stats on
 *       { "label": "MEM", "path": "voltages.<cellId>" },
 *       { "label": "core", "path": "coreStates.mc1" }
 *     ]
 *   }
 * Each trial re-samples every resistor/capacitor/battery/inductor value
 * within its real manufacturing tolerance (CircuitEngine.COMPONENT_TOLERANCE
 * -- honest datasheet-typical bands, not tuned per-circuit) and re-runs the
 * full sim, so a design has to hold up across real part variation instead
 * of one perfect nominal case. Output is a { warningRate, summary } report,
 * not a per-trial dump -- see runMonteCarlo below.
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
  const seenIds = new Map(); // explicit id -> part index that claimed it first
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
    // an explicit "id" is a real, honest convenience -- it's still the
    // same electrical component with the same physical terminals, just a
    // name a receipt/experiment can read instead of guessing "which m2 was
    // that again". No name is special to the solver; it's just a label.
    const id = p.id != null ? String(p.id) : p.type[0] + (i + 1);
    if (seenIds.has(id)) {
      errors.push('part ' + i + ' (' + p.type + '): id "' + id + '" is already used by part ' + seenIds.get(id) + ' -- part ids must be unique');
    }
    seenIds.set(id, i);
    return {
      type: p.type,
      value: p.value,
      color: p.color,
      closed: !!p.closed,
      pos: p.type === 'potentiometer' ? 0.5 : undefined,
      freq: p.freq,
      phase: p.phase,
      sourceR: p.type === 'diffsource' ? p.sourceR : undefined,
      noiseRms: p.type === 'diffsource' ? p.noiseRms : undefined,
      noiseSeed: p.type === 'diffsource' ? (p.noiseSeed != null ? p.noiseSeed : id) : undefined,
      turnsPerSection: p.type === 'toroid' ? p.turns : undefined,
      turnsPerWinding: p.type === 'memorycore' ? p.turns : undefined,
      core: p.type === 'toroid' ? (p.core || 'medium') : p.type === 'memorycore' ? (p.core || 'small') : undefined,
      gauge: p.type === 'toroid' || p.type === 'memorycore' ? (p.gauge || 'standard') : undefined,
      spacing: p.type === 'toroid' ? (p.spacing || 'normal') : undefined,
      initialV: p.type === 'capacitor' ? p.initialV : undefined,
      terminals,
      id,
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
    } else if (p.type === 'diffsource') {
      components.push({
        id: p.id, type: 'diffsource', label: p.id, a: p.terminals[0].cellId, b: p.terminals[1].cellId, value: p.value,
        sourceR: p.sourceR, noiseRms: p.noiseRms, noiseSeed: p.noiseSeed,
      });
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
    } else if (p.type === 'latchrelay') {
      // one real coil (electrically identical to a single-winding
      // memorycore -- the engine's `memoryCores` filter picks up either
      // type by matching on c.windings) plus a genuinely separate
      // mechanical contact pair; N=1 because this is a fixed real part
      // (TQ2-L-5V-class), not a user-wound toroid/core.
      const t = p.terminals;
      const lrSpec = CircuitEngine.LATCHRELAY_SPEC;
      components.push({
        id: p.id, type: 'latchrelay', label: p.id,
        windings: [{ a: t[0].cellId, b: t[1].cellId, N: 1, R: lrSpec.coilR }],
        contactA: t[2].cellId, contactB: t[3].cellId,
        // the shared magnetic-dynamics loop (memoryCores.forEach in
        // circuit.js) reads these three fields straight off the component,
        // exactly like a memorycore's -- latchRelaySpec()'s own defaults
        // merge is used elsewhere (armature/contact logic) but does NOT
        // feed this loop, so they must be set here too or the core never
        // sees a real coercive threshold.
        hcAmpTurns: lrSpec.hcAmpTurns, phiSat: lrSpec.phiSat, switchTau: lrSpec.switchTau,
      });
    } else if (p.type === 'hbridge') {
      const t = p.terminals;
      components.push({
        id: p.id, type: 'hbridge', label: p.id,
        in1: t[0].cellId, in2: t[1].cellId, vm: t[2].cellId, gnd: t[3].cellId,
        out1: t[4].cellId, out2: t[5].cellId,
      });
    } else if (p.type === 'schmitt') {
      const t = p.terminals;
      components.push({
        id: p.id, type: 'schmitt', label: p.id,
        in: t[0].cellId, out: t[1].cellId, vcc: t[2].cellId, gnd: t[3].cellId,
      });
    } else {
      components.push({ id: p.id, type: p.type, label: p.id, a: p.terminals[0].cellId, b: p.terminals[1].cellId, value: p.value, color: p.color, closed: !!p.closed, initialV: p.type === 'capacitor' ? p.initialV : undefined });
    }
  });
  return { wires, components };
}

// Named nodes: a name is a real label for an EXISTING physical hole (given
// by row/col/board, exactly like a part terminal), not a new electrical
// node -- resolving it just looks up that hole's real cellId, the same
// cellId any part wired to that same bus already uses. No topology
// changes; it's purely a label for readable specs/receipts (e.g. "V0",
// "LEAN", "CORE_SENSE" instead of "b0:T14").
function resolveNodeNames(board, nodeNamesSpec) {
  const errors = [];
  const names = {};
  Object.keys(nodeNamesSpec || {}).forEach((name) => {
    const ref = nodeNamesSpec[name];
    const hole = ref && H(board, ref.row, ref.col, ref.board);
    if (!hole) {
      errors.push('nodeNames.' + name + ': does not resolve to a real hole on layout "' + (board.layoutKey || '') + '"');
      return;
    }
    names[name] = hole.cellId;
  });
  return { names, errors };
}

// look up each declared name's real solved voltage -- voltages are keyed
// by union-find root, not raw cellId, so this resolves through result.uf
// exactly like every other lookup in this file does
function namedVoltagesFrom(result, nodeNameCellIds) {
  const out = {};
  Object.keys(nodeNameCellIds || {}).forEach((name) => {
    const root = result.uf.find(nodeNameCellIds[name]);
    const v = result.voltages.get(root);
    if (typeof v === 'number') out[name] = v;
  });
  return out;
}

// named measurement groups (e.g. Decision = V(LEAN) - V(V0)) -- only the
// difference form the milestone actually needs; a richer expression
// language is not built here
function measurementsFrom(namedVoltages, measurementsSpec) {
  const out = {};
  (measurementsSpec || []).forEach((m) => {
    const va = namedVoltages[m.a];
    const vb = namedVoltages[m.b];
    if (typeof va === 'number' && typeof vb === 'number') out[m.label] = va - vb;
  });
  return out;
}

function snapshot(result, opts) {
  opts = opts || {};
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
  if (result && result.coreFlux && result.coreFlux.size) {
    out.coreFlux = Object.fromEntries(result.coreFlux);
  }
  if (result && result.comparatorStates && result.comparatorStates.size) {
    out.comparatorStates = Object.fromEntries(result.comparatorStates);
  }
  if (opts.nodeNameCellIds && Object.keys(opts.nodeNameCellIds).length) {
    out.namedVoltages = namedVoltagesFrom(result, opts.nodeNameCellIds);
    if (opts.measurements && opts.measurements.length) {
      out.measurements = measurementsFrom(out.namedVoltages, opts.measurements);
    }
  }
  return out;
}

// deterministic PRNG (mulberry32) so a seeded Monte Carlo run is
// reproducible run-to-run -- real randomness isn't the point here, real
// part-to-part variation is
function mulberry32(seed) {
  let s = seed >>> 0;
  return function () {
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// real per-type manufacturing tolerance (CircuitEngine.COMPONENT_TOLERANCE)
// -- only part types with a modeled real value spread are perturbed; a
// type with no entry here (MOSFETs' discrete part-class selection,
// comparator, memorycore/toroid core material, etc.) is left at its
// nominal value rather than inventing an untethered tolerance for it.
function toleranceFor(part) {
  if (part.type === 'resistor') return CircuitEngine.COMPONENT_TOLERANCE.resistor;
  if (part.type === 'capacitor') return CircuitEngine.capacitorToleranceFor(part);
  if (part.type === 'battery') return CircuitEngine.COMPONENT_TOLERANCE.battery;
  if (part.type === 'inductor') return CircuitEngine.COMPONENT_TOLERANCE.inductor;
  return null;
}

// a diffsource's deltaV is a controlled experimental input, not a part
// with its own manufacturing spread -- perturbParts leaves it alone
// (toleranceFor returns null for it) so a sweep/Monte-Carlo run varies
// resistors/caps/batteries around it without also smearing the very
// quantity the experiment is deliberately sweeping

function perturbParts(parts, rng) {
  return parts.map((p) => {
    const tol = toleranceFor(p);
    if (tol == null || typeof p.value !== 'number') return p;
    const frac = 1 + (rng() * 2 - 1) * tol; // uniform in [1-tol, 1+tol]
    return Object.assign({}, p, { value: p.value * frac });
  });
}

function getPath(snap, path) {
  let v = snap;
  for (const key of path.split('.')) {
    if (v == null) return undefined;
    v = v[key];
  }
  return v;
}

function runOneTrial(parts, sim) {
  const elements = toEngineElements(parts);
  const circuit = new CircuitEngine.Circuit();
  const seconds = sim.seconds != null ? sim.seconds : 1;
  const dt = sim.dt != null ? sim.dt : 0.001;
  const steps = Math.max(1, Math.round(seconds / dt));
  let lastResult = null;
  for (let i = 0; i < steps; i++) lastResult = circuit.solve(elements, dt, sim.ambientC);
  return lastResult;
}

// parameter sweep: vary ONE declared part field across a real range of
// values and re-run the full sim at each point -- either an explicit
// value list, or a linear from/to/steps range. One dimension only in this
// pass; a real multi-dimensional sweep is a straightforward extension of
// the same mechanism if/when it's needed.
function buildSweepValues(sweep) {
  if (Array.isArray(sweep.values)) return sweep.values.slice();
  const from = sweep.from;
  const to = sweep.to;
  const steps = sweep.steps || 2;
  if (steps <= 1) return [from];
  const out = [];
  for (let i = 0; i < steps; i++) out.push(from + ((to - from) * i) / (steps - 1));
  return out;
}

function applySweepValue(parts, partId, field, value) {
  let found = false;
  const out = parts.map((p) => {
    if (p.id !== partId) return p;
    found = true;
    return Object.assign({}, p, { [field]: value });
  });
  return { parts: out, found };
}

function runSweep(resolvedParts, sim, sweep, snapOpts) {
  const values = buildSweepValues(sweep);
  const points = values.map((value) => {
    const { parts, found } = applySweepValue(resolvedParts, sweep.partId, sweep.field, value);
    if (!found) return { [sweep.field]: value, error: 'no part with id "' + sweep.partId + '" found' };
    const snap = snapshot(runOneTrial(parts, sim), snapOpts);
    return Object.assign({ [sweep.field]: value }, snap);
  });
  return { partId: sweep.partId, field: sweep.field, points };
}

// look up a real declared measurement point for event/persistence checks --
// "node" is a named voltage (see resolveNodeNames), "measurement" is one
// of the declared named differences (see measurementsFrom), "core" is a
// memorycore's real remanent-flux state (direct readout, not inferred
// from a terminal voltage). Exactly one of these should be set.
function valueFor(lastResult, nodeNameCellIds, measurementsSpec, ref) {
  if (ref.coreFlux) {
    return lastResult.coreFlux ? lastResult.coreFlux.get(ref.coreFlux) : undefined;
  }
  if (ref.core) {
    return lastResult.coreStates ? lastResult.coreStates.get(ref.core) : undefined;
  }
  const nv = namedVoltagesFrom(lastResult, nodeNameCellIds);
  if (ref.measurement) {
    const m = (measurementsSpec || []).find((mm) => mm.label === ref.measurement);
    if (!m) return undefined;
    const va = nv[m.a];
    const vb = nv[m.b];
    return typeof va === 'number' && typeof vb === 'number' ? va - vb : undefined;
  }
  if (ref.node) return nv[ref.node];
  return undefined;
}

// A staged experiment: one persistent Circuit instance runs through a
// declared sequence of stages (each its own real duration/dt, optionally
// changing a real part's field before it starts -- "apply the lean",
// "release the drive"), while:
//   - real threshold-crossing events are detected at full solver
//     resolution (every internal step, not just sampled ones) and their
//     exact crossing time is linearly interpolated between the two
//     straddling samples, not just snapped to the nearest step;
//   - an optional persistence check records a real baseline value at the
//     START of one named stage (i.e. the true pre-transition reference --
//     the state right before that stage's own dynamics/drive begin) and
//     then tracks the SMALLEST |value-baseline| seen throughout another
//     named stage's entire duration, so "did it stay distinguishable from
//     where it started the whole time" is a real minimum-over-time
//     measurement, not a single end-of-run sample.
// Because it's the same Circuit instance for every stage, real component
// state (memory-core remanence, capacitor charge, comparator latch, etc.)
// genuinely carries across stages -- releasing a drive and continuing
// the solve is not a reset.
// per-stage trace statistics for one declared signal (a named node, a
// named measurement/difference, or a core's B/flux): real min/max/peak
// over the stage, and a real settling time -- the LATEST time within the
// stage the value was still outside a real tolerance band around the
// stage's own final value, i.e. "how long until it stopped moving",
// not a single end-of-stage sample. A signal that never leaves the band
// settles instantly (settledAt = the stage's own start time).
function traceStatsFromSamples(samples, settleBandFrac) {
  if (!samples.length) return null;
  const values = samples.map((s) => s.value);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const final = values[values.length - 1];
  const band = Math.max(Math.abs(final) * (settleBandFrac || 0.02), 1e-9);
  let settledAt = samples[0].t;
  for (let i = samples.length - 1; i >= 0; i--) {
    if (Math.abs(samples[i].value - final) > band) {
      settledAt = i + 1 < samples.length ? samples[i + 1].t : samples[i].t;
      break;
    }
  }
  return { min, max, peak: Math.max(Math.abs(min), Math.abs(max)), final, settledAt };
}

// ---------------------------------------------------------------------
// Measurement primitives (breadboard qualification spec): real trapezoidal
// integration and real edge-crossing detection over a trace's own actual
// samples -- never a closed-form assumption about what the waveform
// "should" look like. All take the same {t, value} sample arrays every
// other trace/event mechanism here already produces.
// ---------------------------------------------------------------------

// average (DC/mean) value over the sampled window, weighted by real
// elapsed time between samples (trapezoidal), not a plain arithmetic mean
// of however many samples happened to be taken
function averageValue(samples) {
  if (!samples || samples.length < 2) return samples && samples.length ? samples[0].value : null;
  let acc = 0;
  for (let i = 1; i < samples.length; i++) {
    const dt = samples[i].t - samples[i - 1].t;
    acc += 0.5 * (samples[i].value + samples[i - 1].value) * dt;
  }
  return acc / (samples[samples.length - 1].t - samples[0].t);
}

// RMS over the sampled window, same trapezoidal-integration technique
// applied to value^2 -- the real definition, not a peak/sqrt(2) shortcut
// that only holds for an ideal sine
function rmsValue(samples) {
  if (!samples || samples.length < 2) return samples && samples.length ? Math.abs(samples[0].value) : null;
  let acc = 0;
  for (let i = 1; i < samples.length; i++) {
    const dt = samples[i].t - samples[i - 1].t;
    const a = samples[i - 1].value * samples[i - 1].value;
    const b = samples[i].value * samples[i].value;
    acc += 0.5 * (a + b) * dt;
  }
  const meanSq = acc / (samples[samples.length - 1].t - samples[0].t);
  return Math.sqrt(Math.max(meanSq, 0));
}

// real trapezoidal energy integral (Joules) from a power-vs-time trace --
// P is whatever the caller already computed (V*I); this only integrates
function integrateEnergy(powerSamples) {
  if (!powerSamples || powerSamples.length < 2) return 0;
  let acc = 0;
  for (let i = 1; i < powerSamples.length; i++) {
    const dt = powerSamples[i].t - powerSamples[i - 1].t;
    acc += 0.5 * (powerSamples[i].value + powerSamples[i - 1].value) * dt;
  }
  return acc;
}

// builds a real P(t) = V(t)*I(t) trace from two ALREADY-ALIGNED sample
// arrays (the normal case: both captured in the same per-step loop, so
// they share exact timestamps) -- refuses to silently interpolate or
// truncate a real mismatch rather than fabricate a plausible-looking but
// wrong energy number
function powerFromVI(vSamples, iSamples) {
  if (vSamples.length !== iSamples.length) {
    throw new Error('powerFromVI: voltage and current sample counts differ (' + vSamples.length + ' vs ' + iSamples.length + ') -- they must come from the same per-step capture, not be reconciled after the fact');
  }
  return vSamples.map((s, idx) => {
    const is_ = iSamples[idx];
    if (Math.abs(s.t - is_.t) > 1e-9) {
      throw new Error('powerFromVI: sample ' + idx + ' timestamps do not match (' + s.t + ' vs ' + is_.t + ')');
    }
    return { t: s.t, value: s.value * is_.value };
  });
}

// real linearly-interpolated threshold crossings over a trace -- the same
// interpolation technique runExperiment's own event detector uses, factored
// out so period/frequency/duty-cycle/phase can all share one real
// crossing-finder instead of each approximating it differently
function findCrossings(samples, threshold, direction) {
  const out = [];
  for (let i = 1; i < samples.length; i++) {
    const prev = samples[i - 1].value;
    const val = samples[i].value;
    if (prev === val) continue;
    const crossedUp = prev < threshold && val >= threshold;
    const crossedDown = prev > threshold && val <= threshold;
    if ((crossedUp && direction !== 'falling') || (crossedDown && direction !== 'rising')) {
      const frac = (threshold - prev) / (val - prev);
      const t = samples[i - 1].t + frac * (samples[i].t - samples[i - 1].t);
      out.push({ t, direction: crossedUp ? 'rising' : 'falling' });
    }
  }
  return out;
}

// real period from the average spacing between consecutive same-direction
// crossings -- returns null (never a guessed/default value) if there
// aren't at least two crossings to measure a real period from. threshold
// defaults to the trace's own real average (a real AC signal's own DC
// midpoint), not an arbitrary fixed number.
function findPeriod(samples, opts) {
  opts = opts || {};
  if (!samples || samples.length < 2) return null;
  const threshold = opts.threshold != null ? opts.threshold : averageValue(samples);
  const crossings = findCrossings(samples, threshold, 'rising');
  if (crossings.length < 2) return null;
  let sum = 0;
  for (let i = 1; i < crossings.length; i++) sum += crossings[i].t - crossings[i - 1].t;
  return { period: sum / (crossings.length - 1), threshold, crossingCount: crossings.length };
}

function findFrequency(samples, opts) {
  const p = findPeriod(samples, opts);
  return p && p.period > 0 ? 1 / p.period : null;
}

// real phase difference (degrees) between two traces, measured from the
// time offset between their corresponding rising-edge crossings and
// normalized by signal A's own real measured period -- not assumed from
// the two circuits' nominal design values
function phaseDifferenceDeg(samplesA, samplesB, opts) {
  opts = opts || {};
  const perA = findPeriod(samplesA, opts.a);
  if (!perA) return null;
  const crossA = findCrossings(samplesA, opts.a && opts.a.threshold != null ? opts.a.threshold : averageValue(samplesA), 'rising');
  const crossB = findCrossings(samplesB, opts.b && opts.b.threshold != null ? opts.b.threshold : averageValue(samplesB), 'rising');
  if (!crossA.length || !crossB.length) return null;
  // for each A crossing, the nearest B crossing gives one real delay
  // sample; averaging several real cycles is more honest than trusting
  // a single edge, which could be a transient rather than steady state
  const delays = crossA.map((ca) => {
    let nearest = crossB[0];
    let best = Math.abs(crossB[0].t - ca.t);
    crossB.forEach((cb) => {
      const d = Math.abs(cb.t - ca.t);
      if (d < best) { best = d; nearest = cb; }
    });
    return nearest.t - ca.t;
  });
  const meanDelay = delays.reduce((a, b) => a + b, 0) / delays.length;
  let deg = (meanDelay / perA.period) * 360;
  // normalize to (-180, 180]
  deg = ((deg + 180) % 360 + 360) % 360 - 180;
  return deg;
}

// real fraction-of-time (not fraction-of-samples) a trace spends at/above
// a threshold, using the same interpolated crossings so a coarse sample
// rate doesn't bias the answer
function dutyCycle(samples, threshold) {
  if (!samples || samples.length < 2) return null;
  const thr = threshold != null ? threshold : averageValue(samples);
  let highTime = 0;
  for (let i = 1; i < samples.length; i++) {
    const t0 = samples[i - 1].t, t1 = samples[i].t;
    const v0 = samples[i - 1].value, v1 = samples[i].value;
    const dt = t1 - t0;
    if (v0 >= thr && v1 >= thr) highTime += dt;
    else if (v0 >= thr || v1 >= thr) {
      // one endpoint above, one below -- f0 is the crossing's fractional
      // position from t0 (the same interpolation findCrossings uses);
      // falling (v0 high -> v1 low) is above-threshold from t0 TO the
      // crossing (f0*dt), rising (v0 low -> v1 high) is above-threshold
      // from the crossing TO t1 ((1-f0)*dt) -- opposite halves, easy to
      // invert by mistake, so spelled out explicitly rather than reused.
      const f0 = (thr - v0) / (v1 - v0);
      highTime += v0 >= thr ? dt * f0 : dt * (1 - f0);
    }
  }
  return highTime / (samples[samples.length - 1].t - samples[0].t);
}

// Scale-boundary output (item 19 of the hardware-scaling directive): turns
// a real two-cell differential readback into the {sign, magnitude,
// confidence, settled, timestamp} interface the next recursion level
// (Point -> Path -> Field -> next Point) would consume. This reads only
// already-solved, real values (cellA/cellB are ordinary valueFor refs --
// a sense-line voltage, a core state, whatever the experiment actually
// wired up) and asserts nothing about what a valid combination means: a
// Field/Field (both "closed") reading is reported as conflict:true,
// sign:null -- never coerced into -1/0/+1. "settled" is only computed if
// the experiment names both a fast-path and a slow-path (e.g. override)
// readback to compare; it reports whether the slowest confirming signal
// already agrees with the fastest one, not a fixed timer guess.
function resolvedOutputFrom(lastResult, nodeNameCellIds, measurementsSpec, spec, t) {
  const va = valueFor(lastResult, nodeNameCellIds, measurementsSpec, spec.cellA);
  const vb = valueFor(lastResult, nodeNameCellIds, measurementsSpec, spec.cellB);
  if (va == null || vb == null) return null;
  const closedMin = spec.closedMin != null ? spec.closedMin : 4.0;
  const openMax = spec.openMax != null ? spec.openMax : 1.0;
  const classify = (v) => (v >= closedMin ? 'closed' : v <= openMax ? 'open' : 'ambiguous');
  const a = classify(va);
  const b = classify(vb);
  let sign = null;
  let conflict = false;
  if (a === 'open' && b === 'open') sign = 0;
  else if (a === 'closed' && b === 'open') sign = -1;
  else if (a === 'open' && b === 'closed') sign = 1;
  else if (a === 'closed' && b === 'closed') conflict = true;
  // else: at least one cell is genuinely ambiguous (mid-transition/fault)
  // -- sign stays null and conflict stays false, a real third kind of
  // "not resolved yet" distinct from a real Field/Field conflict.
  const scale = spec.scale != null ? spec.scale : 5;
  const magnitude = Number((Math.abs(va - vb) / scale).toFixed(6));
  const confidence = conflict ? 0 : a !== 'ambiguous' && b !== 'ambiguous' ? 1 : 0.5;
  // "settled" compares two already-built taps (e.g. the fast path and the
  // slowest/override path) to see whether the slow one has caught up with
  // the fast one -- but it must NOT assume they land at the same logic
  // polarity. An inverting gate (a real Schmitt trigger is one) flips
  // polarity once per stage it passes through, so two taps built from a
  // different number of inverting stages are EXPECTED to disagree even
  // once both are fully settled. `settleInverted` names that known,
  // real wiring fact explicitly (the same way an event spec names its own
  // "rising"/"falling" direction) rather than the generic comparison here
  // guessing at it.
  let settled = null;
  if (spec.settleA && spec.settleB) {
    const fa = valueFor(lastResult, nodeNameCellIds, measurementsSpec, spec.settleA);
    const fb = valueFor(lastResult, nodeNameCellIds, measurementsSpec, spec.settleB);
    if (fa != null && fb != null) {
      const agree = (fa >= scale / 2) === (fb >= scale / 2);
      settled = spec.settleInverted ? !agree : agree;
    }
  }
  return { sign, magnitude, confidence, conflict, settled, timestamp: Number(t.toFixed(9)) };
}

function runExperiment(resolvedParts, experimentSpec, snapOpts) {
  const stages = experimentSpec.stages || [];
  const eventsSpec = experimentSpec.events || [];
  const persistenceSpec = experimentSpec.persistence || null;
  const tracesSpec = experimentSpec.traces || [];
  const resolvedOutputSpec = experimentSpec.resolvedOutput || null;
  const nodeNameCellIds = snapOpts.nodeNameCellIds;
  const measurementsSpec = snapOpts.measurements;
  const errors = [];

  const circuit = new CircuitEngine.Circuit();
  let parts = resolvedParts;
  let t = 0;
  let lastResult = null;
  // real, settable ambient temperature -- an experiment can change it
  // stage to stage (e.g. simulating a hot enclosure at a later stage); it
  // does not auto-rise on its own without a real heat source modeled, but
  // every component's own self-heating genuinely evolves from real
  // dissipated power against it (see circuit.js's updateTemp).
  let ambientC = experimentSpec.ambientC != null ? experimentSpec.ambientC : undefined;

  const eventPrev = new Map();
  const detectedEvents = [];
  const stageLog = [];
  const persistenceState = persistenceSpec ? { baseline: null, minAbsDelta: Infinity, samples: 0 } : null;

  stages.forEach((stage) => {
    if (stage.ambientC != null) ambientC = stage.ambientC;
    (stage.set || []).forEach((s) => {
      const { parts: nextParts, found } = applySweepValue(parts, s.partId, s.field, s.value);
      if (!found) errors.push('stage "' + stage.name + '": no part with id "' + s.partId + '" found to set');
      parts = nextParts;
    });

    if (persistenceSpec && persistenceSpec.baselineStage === stage.name && lastResult) {
      persistenceState.baseline = valueFor(lastResult, nodeNameCellIds, measurementsSpec, persistenceSpec);
    }

    const elements = toEngineElements(parts);
    const dt = stage.dt != null ? stage.dt : 0.001;
    const seconds = stage.seconds != null ? stage.seconds : 0.01;
    const steps = Math.max(1, Math.round(seconds / dt));
    const stageStartT = t;
    const traceSamples = new Map(tracesSpec.map((tr) => [tr.label, []]));

    for (let i = 0; i < steps; i++) {
      t += dt;
      lastResult = circuit.solve(elements, dt, ambientC);

      tracesSpec.forEach((tr) => {
        const val = valueFor(lastResult, nodeNameCellIds, measurementsSpec, tr);
        if (val != null) traceSamples.get(tr.label).push({ t, value: val });
      });

      eventsSpec.forEach((ev) => {
        const val = valueFor(lastResult, nodeNameCellIds, measurementsSpec, ev);
        if (val == null) return;
        const prev = eventPrev.get(ev.label);
        if (prev != null && prev !== val) {
          const crossedUp = prev < ev.threshold && val >= ev.threshold;
          const crossedDown = prev > ev.threshold && val <= ev.threshold;
          const dir = ev.direction || 'either';
          if ((crossedUp && dir !== 'falling') || (crossedDown && dir !== 'rising')) {
            const frac = (ev.threshold - prev) / (val - prev);
            const crossT = t - dt + frac * dt;
            detectedEvents.push({ label: ev.label, t: Number(crossT.toFixed(9)), stage: stage.name, direction: crossedUp ? 'rising' : 'falling', valueBefore: prev, valueAfter: val });
          }
        }
        eventPrev.set(ev.label, val);
      });

      if (persistenceSpec && persistenceSpec.holdStage === stage.name && persistenceState.baseline != null) {
        const val = valueFor(lastResult, nodeNameCellIds, measurementsSpec, persistenceSpec);
        if (val != null) {
          persistenceState.minAbsDelta = Math.min(persistenceState.minAbsDelta, Math.abs(val - persistenceState.baseline));
          persistenceState.samples++;
        }
      }
    }

    const traces = {};
    tracesSpec.forEach((tr) => {
      const stats = traceStatsFromSamples(traceSamples.get(tr.label), tr.settleBandFrac);
      if (stats) traces[tr.label] = stats;
    });

    stageLog.push({
      name: stage.name,
      startT: Number(stageStartT.toFixed(9)),
      endT: Number(t.toFixed(9)),
      snapshot: snapshot(lastResult, snapOpts),
      traces,
      resolvedOutput: resolvedOutputSpec ? resolvedOutputFrom(lastResult, nodeNameCellIds, measurementsSpec, resolvedOutputSpec, t) : undefined,
    });
  });

  const out = { errors, stages: stageLog, events: detectedEvents, final: snapshot(lastResult, snapOpts) };
  if (resolvedOutputSpec) out.finalResolvedOutput = resolvedOutputFrom(lastResult, nodeNameCellIds, measurementsSpec, resolvedOutputSpec, t);
  if (persistenceSpec) {
    const observed = persistenceState.minAbsDelta === Infinity ? null : persistenceState.minAbsDelta;
    out.persistence = {
      label: persistenceSpec.label,
      baseline: persistenceState.baseline,
      minDelta: persistenceSpec.minDelta,
      minObservedDelta: observed,
      samples: persistenceState.samples,
      distinguishable: observed != null && persistenceState.baseline != null && observed >= persistenceSpec.minDelta,
    };
  }
  return out;
}

function runMonteCarlo(resolvedParts, sim, mc, snapOpts) {
  const trials = mc.trials || 100;
  const rng = mulberry32(mc.seed != null ? mc.seed : 12345);
  const watch = mc.watch || [];
  const watchStats = watch.map((w) => ({ label: w.label || w.path, path: w.path, values: [] }));
  let warningTrials = 0;
  const warningsSample = [];
  for (let i = 0; i < trials; i++) {
    const parts = perturbParts(resolvedParts, rng);
    const snap = snapshot(runOneTrial(parts, sim), snapOpts);
    if (snap.warnings.length) {
      warningTrials++;
      if (warningsSample.length < 5 && !warningsSample.includes(snap.warnings[0])) warningsSample.push(snap.warnings[0]);
    }
    watchStats.forEach((ws) => {
      const v = getPath(snap, ws.path);
      if (typeof v === 'number') ws.values.push(v);
    });
  }
  const summary = {};
  watchStats.forEach((ws) => {
    if (!ws.values.length) {
      summary[ws.label] = { note: 'no numeric value found at "' + ws.path + '" in any trial -- check the path' };
      return;
    }
    const n = ws.values.length;
    const mean = ws.values.reduce((a, b) => a + b, 0) / n;
    const variance = ws.values.reduce((a, b) => a + (b - mean) ** 2, 0) / n;
    summary[ws.label] = { min: Math.min(...ws.values), max: Math.max(...ws.values), mean, stdev: Math.sqrt(variance), n };
  });
  return { trials, warningTrials, warningRate: warningTrials / trials, warningsSample, summary };
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

  const { names: nodeNameCellIds, errors: nodeNameErrors } = resolveNodeNames(board, input.nodeNames);
  if (nodeNameErrors.length) return fail(nodeNameErrors);
  const measurements = input.measurements || [];
  const snapOpts = { nodeNameCellIds, measurements };

  const sim = input.sim || {};

  if (input.monteCarlo) {
    const mcReport = runMonteCarlo(parts, sim, input.monteCarlo, snapOpts);
    console.log(JSON.stringify({ ok: true, errors: [], monteCarlo: mcReport }, null, 2));
    return;
  }

  if (input.sweep) {
    const sweepReport = runSweep(parts, sim, input.sweep, snapOpts);
    console.log(JSON.stringify({ ok: true, errors: [], sweep: sweepReport }, null, 2));
    return;
  }

  if (input.experiment) {
    const expReport = runExperiment(parts, input.experiment, snapOpts);
    console.log(JSON.stringify({ ok: true, errors: expReport.errors, experiment: expReport }, null, 2));
    return;
  }

  const elements = toEngineElements(parts);
  const circuit = new CircuitEngine.Circuit();
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
    lastResult = circuit.solve(elements, dt, sim.ambientC);
    if (t >= nextSampleAt) {
      samples.push(Object.assign({ t: Number(t.toFixed(6)) }, snapshot(lastResult, snapOpts)));
      nextSampleAt += sampleEvery;
    }
  }

  const out = { ok: true, errors: [], final: snapshot(lastResult, snapOpts) };
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
  mulberry32, toleranceFor, perturbParts, getPath, runOneTrial, runMonteCarlo,
  resolveNodeNames, namedVoltagesFrom, measurementsFrom,
  buildSweepValues, applySweepValue, runSweep,
  valueFor, runExperiment, traceStatsFromSamples, resolvedOutputFrom,
  averageValue, rmsValue, integrateEnergy, powerFromVI, findCrossings, findPeriod, findFrequency, phaseDifferenceDeg, dutyCycle,
};
