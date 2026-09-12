'use strict';

/*
 * Small-signal frequency-domain analysis for the Virtual Breadboard.
 *
 * The transient solver stays real-valued and time-domain. This module builds
 * the SPICE-style AC linearization beside it: first solve the real DC operating
 * point, then stamp a complex MNA system at each requested frequency.
 */

const CE = require('./circuit.js');
const {
  Circuit, buildTopologyUnionFind,
  BATTERY_RINT, AC_RINT, DIODE_RON, DIODE_IS, DIODE_N, THERMAL_VOLTAGE_25C,
  capacitorESR, capacitorLeakageR, inductorDCR,
  mosfetChannelCurrent, MOSFET_OFF_LEAKAGE_G,
} = CE;

const C = (re, im) => ({ re: re || 0, im: im || 0 });
const add = (a, b) => C(a.re + b.re, a.im + b.im);
const sub = (a, b) => C(a.re - b.re, a.im - b.im);
const mul = (a, b) => C(a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re);
const div = (a, b) => {
  const d = b.re * b.re + b.im * b.im;
  if (!(d > 0)) throw new Error('singular complex division');
  return C((a.re * b.re + a.im * b.im) / d, (a.im * b.re - a.re * b.im) / d);
};
const abs = (a) => Math.hypot(a.re, a.im);
const polar = (mag, phaseDeg) => {
  const r = (phaseDeg || 0) * Math.PI / 180;
  return C(mag * Math.cos(r), mag * Math.sin(r));
};

function finite(name, value) {
  if (!Number.isFinite(value)) throw new TypeError(`${name} must be finite`);
  return value;
}

function cloneElements(elements) {
  return JSON.parse(JSON.stringify(elements || { wires: [], components: [] }));
}

function solveComplex(A, b) {
  const n = b.length;
  const M = A.map((row, i) => row.map((z) => C(z.re, z.im)).concat([C(b[i].re, b[i].im)]));
  for (let col = 0; col < n; col++) {
    let pivot = col;
    let best = abs(M[col][col]);
    for (let row = col + 1; row < n; row++) {
      const m = abs(M[row][col]);
      if (m > best) { best = m; pivot = row; }
    }
    if (best < 1e-18) throw new Error(`AC matrix is singular near row ${col}`);
    if (pivot !== col) [M[col], M[pivot]] = [M[pivot], M[col]];
    const p = M[col][col];
    for (let j = col; j <= n; j++) M[col][j] = div(M[col][j], p);
    for (let row = 0; row < n; row++) {
      if (row === col) continue;
      const f = M[row][col];
      if (abs(f) === 0) continue;
      for (let j = col; j <= n; j++) M[row][j] = sub(M[row][j], mul(f, M[col][j]));
    }
  }
  return M.map((row) => row[n]);
}

function dcOperatingPointForAc(elements, ambientC, solverOptions) {
  const dc = cloneElements(elements);
  dc.components = (dc.components || []).flatMap((c) => {
    if (c.type === 'capacitor') return [];
    if (c.type === 'inductor') return [{ id: c.id, type: 'resistor', a: c.a, b: c.b, value: inductorDCR(c.value) }];
    if (c.type === 'acsource') return [Object.assign({}, c, { value: 0, phase: 0 })];
    return [c];
  });
  const opts = Object.assign({ diodeModel: 'newton', mosfetModel: 'continuous' }, solverOptions || {});
  return new Circuit().solve(dc, 0, ambientC, opts);
}

function normalizeFrequencies(options) {
  if (options.frequencies != null) {
    const out = Array.from(options.frequencies).map((f, i) => finite(`frequencies[${i}]`, f));
    if (!out.length) throw new RangeError('frequencies must not be empty');
    if (out.some((f) => !(f > 0))) throw new RangeError('AC frequencies must be > 0');
    return out;
  }
  const start = finite('startHz', options.startHz);
  const stop = finite('stopHz', options.stopHz);
  if (!(start > 0) || !(stop >= start)) throw new RangeError('require 0 < startHz <= stopHz');
  const ppd = options.pointsPerDecade == null ? 10 : Math.trunc(options.pointsPerDecade);
  if (!(ppd >= 1)) throw new RangeError('pointsPerDecade must be >= 1');
  if (start === stop) return [start];
  const decades = Math.log10(stop / start);
  const count = Math.max(1, Math.ceil(decades * ppd));
  const out = [];
  for (let i = 0; i <= count; i++) out.push(i === count ? stop : start * Math.pow(10, i / ppd));
  return out;
}

function sourceResistance(c) {
  if (c.type === 'battery') return BATTERY_RINT;
  if (c.type === 'acsource') return AC_RINT;
  if (c.type === 'diffsource') return c.sourceR != null ? c.sourceR : 0.05;
  throw new Error(`unsupported AC source type '${c.type}'`);
}

function smallSignalAc(elements, options) {
  options = options || {};
  const sourceId = options.sourceId;
  if (!sourceId) throw new TypeError('sourceId is required');
  const magnitude = options.magnitude == null ? 1 : finite('magnitude', options.magnitude);
  const phaseDeg = options.phaseDeg == null ? 0 : finite('phaseDeg', options.phaseDeg);
  const ambientC = options.ambientC == null ? 25 : finite('ambientC', options.ambientC);
  const gmin = options.gmin == null ? 1e-9 : finite('gmin', options.gmin);
  if (gmin < 0) throw new RangeError('gmin must be >= 0');
  const frequencies = normalizeFrequencies(options);
  const base = cloneElements(elements);
  const components = base.components || [];
  const wires = base.wires || [];
  const source = components.find((c) => c.id === sourceId);
  if (!source) throw new Error(`AC source '${sourceId}' was not found`);
  if (!['battery', 'diffsource', 'acsource', 'isource'].includes(source.type)) {
    throw new Error(`AC source '${sourceId}' must be battery, diffsource, acsource, or isource`);
  }

  const supported = new Set(['resistor', 'capacitor', 'inductor', 'battery', 'diffsource', 'acsource', 'isource', 'vccs', 'vcvs', 'cccs', 'ccvs', 'diode', 'led', 'nmos', 'pmos', 'switch', 'pushbutton']);
  const unsupported = components.filter((c) => !supported.has(c.type));
  if (unsupported.length) throw new Error(`AC analysis does not yet support: ${unsupported.map((c) => `${c.id}:${c.type}`).join(', ')}`);

  const op = dcOperatingPointForAc(base, ambientC, options.solverOptions);
  if (!op.solver || !op.solver.converged) throw new Error('DC operating point did not converge; AC linearization is invalid');

  const uf = buildTopologyUnionFind(components, wires);
  const voltageSources = components.filter((c) => ['battery', 'diffsource', 'acsource', 'vcvs', 'ccvs'].includes(c.type));
  const sourceInternal = new Map();
  voltageSources.forEach((c) => {
    if (c.type === 'vcvs' || c.type === 'ccvs') return;
    const name = `__acsmall__${c.id}`;
    uf.find(name);
    sourceInternal.set(c.id, name);
  });

  let groundRoot = null;
  const dcSources = components.filter((c) => c.type === 'battery' || c.type === 'diffsource');
  if (dcSources.length) groundRoot = uf.find(dcSources[0].b);
  else if (wires.length) groundRoot = uf.find(wires[0].a);
  else if (components.length) groundRoot = uf.find(components[0].b != null ? components[0].b : components[0].a);
  if (groundRoot == null) throw new Error('AC analysis needs a circuit reference node');

  const roots = new Set();
  const touch = (n) => { if (n != null) roots.add(uf.find(n)); };
  wires.forEach((w) => { touch(w.a); touch(w.b); });
  components.forEach((c) => {
    touch(c.a); touch(c.b);
    if (c.type === 'nmos' || c.type === 'pmos') { touch(c.gate); touch(c.drain); touch(c.source); }
  });
  sourceInternal.forEach((n) => touch(n));
  components.forEach((c) => { if (c.type === 'vccs' || c.type === 'vcvs') { touch(c.controlP); touch(c.controlN); } });
  roots.add(groundRoot);
  const nodeRoots = Array.from(roots).filter((r) => r !== groundRoot);
  const nodeIndex = new Map(nodeRoots.map((r, i) => [r, i]));
  const nNodes = nodeRoots.length;
  const size = nNodes + voltageSources.length;
  const idx = (n) => {
    if (n == null) return -1;
    const r = uf.find(n);
    return r === groundRoot ? -1 : nodeIndex.get(r);
  };
  const rowSource = (k) => nNodes + k;
  const opV = (n) => {
    const root = op.uf.find(n);
    return op.voltages.get(root) || 0;
  };

  const stampY = (A, a, b, y) => {
    if (a >= 0) A[a][a] = add(A[a][a], y);
    if (b >= 0) A[b][b] = add(A[b][b], y);
    if (a >= 0 && b >= 0) {
      A[a][b] = sub(A[a][b], y);
      A[b][a] = sub(A[b][a], y);
    }
  };
  const stampControlledCurrent = (A, drain, sourceNode, gate, gd, gs, gg) => {
    const terms = [[drain, gd], [sourceNode, gs], [gate, gg]];
    for (const [col, value] of terms) {
      if (drain >= 0 && col >= 0) A[drain][col] = add(A[drain][col], C(value, 0));
      if (sourceNode >= 0 && col >= 0) A[sourceNode][col] = sub(A[sourceNode][col], C(value, 0));
    }
  };

  const rows = frequencies.map((frequencyHz) => {
    const w = 2 * Math.PI * frequencyHz;
    const A = Array.from({ length: size }, () => Array.from({ length: size }, () => C(0, 0)));
    const b = Array.from({ length: size }, () => C(0, 0));

    for (let i = 0; i < nNodes; i++) A[i][i] = add(A[i][i], C(gmin, 0));

    const sourceRowById = new Map(voltageSources.map((s,k)=>[s.id,rowSource(k)]));
    components.forEach((c) => {
      const a = idx(c.a);
      const bb = idx(c.b);
      if (c.type === 'isource') {
        if (c.id === sourceId) {
          const iz = polar(magnitude, phaseDeg);
          if (a >= 0) b[a] = sub(b[a], iz);
          if (bb >= 0) b[bb] = add(b[bb], iz);
        }
      } else if (c.type === 'vccs') {
        const cp=idx(c.controlP), cn=idx(c.controlN), g=Number(c.gain != null ? c.gain : c.value)||0;
        if (a>=0&&cp>=0) A[a][cp]=add(A[a][cp],C(g,0));
        if (a>=0&&cn>=0) A[a][cn]=sub(A[a][cn],C(g,0));
        if (bb>=0&&cp>=0) A[bb][cp]=sub(A[bb][cp],C(g,0));
        if (bb>=0&&cn>=0) A[bb][cn]=add(A[bb][cn],C(g,0));
      } else if (c.type === 'cccs') {
        const cr=sourceRowById.get(c.controlSourceId), gain=Number(c.gain != null ? c.gain : c.value)||0;
        if (cr == null) throw new Error(`CCCS ${c.id} controlSourceId '${c.controlSourceId}' is not a voltage-source branch`);
        if (a>=0) A[a][cr]=add(A[a][cr],C(gain,0));
        if (bb>=0) A[bb][cr]=sub(A[bb][cr],C(gain,0));
      } else if (c.type === 'resistor') {
        stampY(A, a, bb, C(1 / Math.max(c.value, 1e-12), 0));
      } else if (c.type === 'capacitor') {
        const esr = capacitorESR(c);
        const zSeries = C(esr, -1 / (w * Math.max(c.value, 1e-18)));
        const ySeries = div(C(1, 0), zSeries);
        const yLeak = C(1 / capacitorLeakageR(c), 0);
        stampY(A, a, bb, add(ySeries, yLeak));
      } else if (c.type === 'inductor') {
        const z = C(inductorDCR(c.value), w * Math.max(c.value, 1e-18));
        stampY(A, a, bb, div(C(1, 0), z));
      } else if (c.type === 'switch' || c.type === 'pushbutton') {
        if (c.closed) stampY(A, a, bb, C(1e9, 0));
      } else if (c.type === 'diode') {
        const vd = opV(c.a) - opV(c.b);
        const vt = THERMAL_VOLTAGE_25C * ((ambientC + 273.15) / 298.15);
        const nvt = DIODE_N * vt;
        const limited = Math.max(-5, Math.min(0.8, vd));
        const gd = DIODE_IS * Math.exp(limited / nvt) / nvt;
        stampY(A, a, bb, C(gd, 0));
      } else if (c.type === 'led') {
        const on = (op.currents.get(c.id) || 0) > 0;
        if (on) stampY(A, a, bb, C(1 / DIODE_RON, 0));
      } else if (c.type === 'nmos' || c.type === 'pmos') {
        const gate = idx(c.gate);
        const drain = idx(c.drain);
        const sourceNode = idx(c.source);
        const vg = opV(c.gate), vd = opV(c.drain), vs = opV(c.source);
        const h = 1e-5;
        const gm = (mosfetChannelCurrent(c, vg + h, vd, vs, ambientC) - mosfetChannelCurrent(c, vg - h, vd, vs, ambientC)) / (2 * h);
        const gdd = (mosfetChannelCurrent(c, vg, vd + h, vs, ambientC) - mosfetChannelCurrent(c, vg, vd - h, vs, ambientC)) / (2 * h) + MOSFET_OFF_LEAKAGE_G;
        const gss = (mosfetChannelCurrent(c, vg, vd, vs + h, ambientC) - mosfetChannelCurrent(c, vg, vd, vs - h, ambientC)) / (2 * h) - MOSFET_OFF_LEAKAGE_G;
        stampControlledCurrent(A, drain, sourceNode, gate, gdd, gss, gm);
        const bodyOn = op.mosfetStates && op.mosfetStates.get(c.id) && op.mosfetStates.get(c.id).bodyDiodeOn;
        if (bodyOn) stampY(A, drain, sourceNode, C(1 / DIODE_RON, 0));
      }
    });

    voltageSources.forEach((s, k) => {
      const row = rowSource(k);
      const a = idx(s.a), ref = idx(s.b);
      if (s.type === 'vcvs' || s.type === 'ccvs') {
        if (a >= 0) { A[a][row]=add(A[a][row],C(1,0)); A[row][a]=add(A[row][a],C(1,0)); }
        if (ref >= 0) { A[ref][row]=sub(A[ref][row],C(1,0)); A[row][ref]=sub(A[row][ref],C(1,0)); }
        const gain=Number(s.gain != null ? s.gain : s.value)||0;
        if (s.type === 'vcvs') {
          const cp=idx(s.controlP), cn=idx(s.controlN);
          if (cp>=0) A[row][cp]=sub(A[row][cp],C(gain,0));
          if (cn>=0) A[row][cn]=add(A[row][cn],C(gain,0));
        } else {
          const cr=sourceRowById.get(s.controlSourceId);
          if (cr == null || cr === row) throw new Error(`CCVS ${s.id} controlSourceId '${s.controlSourceId}' is not a distinct voltage-source branch`);
          A[row][cr]=sub(A[row][cr],C(gain,0));
        }
      } else {
        const internal = idx(sourceInternal.get(s.id));
        stampY(A, internal, a, C(1 / Math.max(sourceResistance(s), 1e-12), 0));
        if (internal >= 0) { A[internal][row] = add(A[internal][row], C(1, 0)); A[row][internal] = add(A[row][internal], C(1, 0)); }
        if (ref >= 0) { A[ref][row] = sub(A[ref][row], C(1, 0)); A[row][ref] = sub(A[row][ref], C(1, 0)); }
        if (s.id === sourceId) b[row] = add(b[row], polar(magnitude, phaseDeg));
      }
    });

    const x = size ? solveComplex(A, b) : [];
    const voltages = new Map();
    for (const r of roots) voltages.set(r, r === groundRoot ? C(0, 0) : x[nodeIndex.get(r)] || C(0, 0));
    const sourceCurrents = new Map();
    voltageSources.forEach((s, k) => sourceCurrents.set(s.id, x[rowSource(k)] || C(0, 0)));
    return { frequencyHz, voltages, sourceCurrents };
  });

  return {
    analysis: { type: 'ac', smallSignal: true, sourceId, magnitude, phaseDeg, gmin },
    frequencies,
    rows,
    operatingPoint: op,
    uf,
    groundRoot,
  };
}

function phasorMagnitude(z) { return abs(z); }
function phasorPhaseDeg(z) { return Math.atan2(z.im, z.re) * 180 / Math.PI; }

module.exports = { smallSignalAc, solveComplex, phasorMagnitude, phasorPhaseDeg };
