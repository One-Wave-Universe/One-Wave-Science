#!/usr/bin/env node
/*
 * Normal-circuit reality pass.
 *
 * Purpose: stress the Virtual Breadboard with ordinary electronics before
 * trusting it for unusual experiments. Expected DC values are calculated
 * independently here from Kirchhoff's current law + Ohm's law, including
 * the documented 1 ohm battery internal resistance. Dynamic RC/RL checks
 * compare against standard first-order behavior with the simulator's
 * documented real-part parasitics included in the expected time constant.
 *
 * This test intentionally contains no One-Wave-specific assumptions.
 * Run with: node test/normal-circuits-reality.test.js
 */

const CircuitEngine = require('../js/circuit.js');
const { Circuit } = CircuitEngine;

let checks = 0;
function pass(name, condition, detail = '') {
  checks++;
  const line = `${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`;
  console.log(line);
  if (!condition) throw new Error(`NORMAL CIRCUIT REALITY CHECK FAILED: ${name}${detail ? ' -- ' + detail : ''}`);
}
function approx(name, actual, expected, tolerance, detail = '') {
  pass(name, Number.isFinite(actual) && Math.abs(actual - expected) <= tolerance,
    `expected=${expected} actual=${actual} tolerance=${tolerance}${detail ? '; ' + detail : ''}`);
}

function gaussianSolve(A, b) {
  const n = b.length;
  const M = A.map((row, i) => row.slice().concat([b[i]]));
  for (let col = 0; col < n; col++) {
    let pivot = col;
    for (let r = col + 1; r < n; r++) {
      if (Math.abs(M[r][col]) > Math.abs(M[pivot][col])) pivot = r;
    }
    if (Math.abs(M[pivot][col]) < 1e-18) throw new Error('independent nodal matrix is singular');
    if (pivot !== col) [M[pivot], M[col]] = [M[col], M[pivot]];
    for (let r = 0; r < n; r++) {
      if (r === col) continue;
      const factor = M[r][col] / M[col][col];
      for (let c = col; c <= n; c++) M[r][c] -= factor * M[col][c];
    }
  }
  return M.map((row, i) => row[n] / row[i]);
}

// Independent resistor-network solver for one ordinary battery from p -> g.
// Battery is represented by its real EMF behind BATTERY_RINT; all other
// elements in these DC fixtures are plain resistors.
function expectedNetwork(emf, resistors) {
  const nodeNames = new Set(['p']);
  for (const r of resistors) {
    if (r.a !== 'g') nodeNames.add(r.a);
    if (r.b !== 'g') nodeNames.add(r.b);
  }
  const nodes = Array.from(nodeNames).sort();
  const idx = new Map(nodes.map((n, i) => [n, i]));
  const A = Array.from({ length: nodes.length }, () => Array(nodes.length).fill(0));
  const b = Array(nodes.length).fill(0);

  function stampR(a, z, ohms) {
    const g = 1 / ohms;
    if (a !== 'g') A[idx.get(a)][idx.get(a)] += g;
    if (z !== 'g') A[idx.get(z)][idx.get(z)] += g;
    if (a !== 'g' && z !== 'g') {
      A[idx.get(a)][idx.get(z)] -= g;
      A[idx.get(z)][idx.get(a)] -= g;
    }
  }
  for (const r of resistors) stampR(r.a, r.b, r.value);

  // KCL at source terminal p: (Vp - EMF)/Rint + all load currents = 0.
  A[idx.get('p')][idx.get('p')] += 1 / CircuitEngine.BATTERY_RINT;
  b[idx.get('p')] += emf / CircuitEngine.BATTERY_RINT;

  const solved = gaussianSolve(A, b);
  const v = new Map([['g', 0]]);
  nodes.forEach((n, i) => v.set(n, solved[i]));
  const currents = new Map();
  for (const r of resistors) currents.set(r.id, (v.get(r.a) - v.get(r.b)) / r.value);
  const batteryCurrent = (emf - v.get('p')) / CircuitEngine.BATTERY_RINT;
  return { v, currents, batteryCurrent };
}

function runResistorFixture(name, emf, resistors, voltageNodes = []) {
  console.log(`\n=== ${name} ===`);
  const expected = expectedNetwork(emf, resistors);
  const c = new Circuit();
  const elements = {
    wires: [],
    components: [
      { id: 'bat', type: 'battery', a: 'p', b: 'g', value: emf },
      ...resistors.map((r) => ({ id: r.id, type: 'resistor', a: r.a, b: r.b, value: r.value })),
    ],
  };
  const actual = c.solve(elements, 0.001);

  for (const n of voltageNodes) {
    approx(`${name}:V(${n})`, actual.voltages.get(n), expected.v.get(n), 2e-4);
  }
  for (const r of resistors) {
    approx(`${name}:I(${r.id})`, actual.currents.get(r.id), expected.currents.get(r.id), 2e-6);
  }
  approx(`${name}:battery-current`, actual.currents.get('bat'), expected.batteryCurrent, 2e-6);

  // Independent energy balance for an ordinary passive DC network:
  // chemical/source power = external resistor heat + battery internal heat.
  const pSource = emf * actual.currents.get('bat');
  let pLoads = 0;
  for (const r of resistors) pLoads += actual.currents.get(r.id) ** 2 * r.value;
  const pInternal = actual.currents.get('bat') ** 2 * CircuitEngine.BATTERY_RINT;
  approx(`${name}:power-balance`, pLoads + pInternal, pSource, Math.max(1e-6, Math.abs(pSource) * 2e-4));
  return { actual, expected };
}

runResistorFixture('series-divider', 5, [
  { id: 'r1', a: 'p', b: 'n', value: 1000 },
  { id: 'r2', a: 'n', b: 'g', value: 2200 },
], ['p', 'n']);

runResistorFixture('three-parallel-loads', 9, [
  { id: 'r1', a: 'p', b: 'g', value: 470 },
  { id: 'r2', a: 'p', b: 'g', value: 1000 },
  { id: 'r3', a: 'p', b: 'g', value: 2200 },
], ['p']);

runResistorFixture('loaded-divider', 9, [
  { id: 'r1', a: 'p', b: 'n', value: 1000 },
  { id: 'r2', a: 'n', b: 'g', value: 2200 },
  { id: 'load', a: 'n', b: 'g', value: 1000 },
], ['p', 'n']);

const ladder = runResistorFixture('three-node-ladder', 12, [
  { id: 'r1', a: 'p', b: 'a', value: 330 },
  { id: 'r2', a: 'a', b: 'g', value: 680 },
  { id: 'r3', a: 'a', b: 'b', value: 470 },
  { id: 'r4', a: 'b', b: 'g', value: 1000 },
  { id: 'r5', a: 'b', b: 'c', value: 820 },
  { id: 'r6', a: 'c', b: 'g', value: 1500 },
], ['p', 'a', 'b', 'c']);

// KCL at an internal node must close numerically, not just individual
// branches happen to look right.
{
  const i1 = ladder.actual.currents.get('r1'); // p -> a
  const i2 = ladder.actual.currents.get('r2'); // a -> g
  const i3 = ladder.actual.currents.get('r3'); // a -> b
  approx('three-node-ladder:KCL-at-a', i1, i2 + i3, 2e-6);
}

runResistorFixture('unbalanced-multi-loop-network', 10, [
  { id: 'r1', a: 'p', b: 'a', value: 470 },
  { id: 'r2', a: 'a', b: 'g', value: 680 },
  { id: 'r3', a: 'p', b: 'b', value: 820 },
  { id: 'r4', a: 'b', b: 'g', value: 1200 },
  { id: 'r5', a: 'a', b: 'b', value: 1500 },
], ['p', 'a', 'b']);

runResistorFixture('source-sag-under-normal-load', 9, [
  { id: 'load', a: 'p', b: 'g', value: 22 },
], ['p']);

runResistorFixture('high-resistance-microcurrent-load', 5, [
  { id: 'load', a: 'p', b: 'g', value: 1e6 },
], ['p']);

// Deterministic family of ordinary 2-node resistor meshes. This catches
// topology-specific solver mistakes that a single carefully chosen example
// can miss while remaining fully reproducible and hand/nodal-calculable.
console.log('\n=== deterministic resistor-mesh sweep ===');
for (let k = 0; k < 8; k++) {
  const base = 220 + k * 37;
  runResistorFixture(`mesh-${k + 1}`, 6 + (k % 3), [
    { id: 'pa', a: 'p', b: 'a', value: base },
    { id: 'ag', a: 'a', b: 'g', value: base + 180 },
    { id: 'pb', a: 'p', b: 'b', value: base + 330 },
    { id: 'bg', a: 'b', b: 'g', value: base + 560 },
    { id: 'ab', a: 'a', b: 'b', value: base + 910 },
    { id: 'pg', a: 'p', b: 'g', value: base + 1800 },
  ], ['p', 'a', 'b']);
}

console.log('\n=== RC charge curve ===');
{
  const c = new Circuit();
  const cap = { id: 'c1', type: 'capacitor', a: 'n', b: 'g', value: 100e-6 };
  const R = 1000;
  const emf = 5;
  const elements = { wires: [], components: [
    { id: 'bat', type: 'battery', a: 'p', b: 'g', value: emf },
    { id: 'r', type: 'resistor', a: 'p', b: 'n', value: R },
    cap,
  ] };
  const esr = CircuitEngine.capacitorESR(cap);
  const leak = CircuitEngine.capacitorLeakageR(cap);
  const rSeries = CircuitEngine.BATTERY_RINT + R + esr;
  const vInf = emf * leak / (leak + rSeries);
  const rThevenin = 1 / (1 / rSeries + 1 / leak);
  const tau = rThevenin * cap.value;
  const dt = tau / 100;
  let res;
  for (let i = 0; i < 100; i++) res = c.solve(elements, dt);
  const v1tau = res.voltages.get('n');
  const expected1tau = vInf * (1 - Math.exp(-1));
  approx('RC:voltage-at-1-tau', v1tau, expected1tau, 0.08,
    `standard first-order charge; tau=${tau}`);
  for (let i = 100; i < 500; i++) res = c.solve(elements, dt);
  const v5tau = res.voltages.get('n');
  pass('RC:near-steady-after-5-tau', v5tau > 0.985 * vInf && v5tau <= vInf + 0.02,
    `V5tau=${v5tau}, Vinf=${vInf}`);
  pass('RC:charge-is-monotonic-positive', v1tau > 0 && v5tau > v1tau);
}

console.log('\n=== RL current-rise curve ===');
{
  const c = new Circuit();
  const L = 1.0;
  const R = 100;
  const emf = 5;
  const elements = { wires: [], components: [
    { id: 'bat', type: 'battery', a: 'p', b: 'g', value: emf },
    { id: 'r', type: 'resistor', a: 'p', b: 'n', value: R },
    { id: 'l1', type: 'inductor', a: 'n', b: 'g', value: L },
  ] };
  const dcr = CircuitEngine.inductorDCR(L);
  const rTotal = CircuitEngine.BATTERY_RINT + R + dcr;
  const iInf = emf / rTotal;
  const tau = L / rTotal;
  const dt = tau / 100;
  let res;
  for (let i = 0; i < 100; i++) res = c.solve(elements, dt);
  const i1tau = res.currents.get('l1');
  approx('RL:current-at-1-tau', i1tau, iInf * (1 - Math.exp(-1)), iInf * 0.03,
    `standard first-order rise; tau=${tau}`);
  for (let i = 100; i < 500; i++) res = c.solve(elements, dt);
  const i5tau = res.currents.get('l1');
  pass('RL:near-steady-after-5-tau', i5tau > 0.985 * iInf && i5tau <= iInf * 1.01,
    `I5tau=${i5tau}, Iinf=${iInf}`);
  pass('RL:current-rise-is-monotonic-positive', i1tau > 0 && i5tau > i1tau);
}

console.log('\n=== ordinary silicon diode limiter ===');
{
  const c = new Circuit();
  const R = 1000;
  const emf = 5;
  const elements = { wires: [], components: [
    { id: 'bat', type: 'battery', a: 'p', b: 'g', value: emf },
    { id: 'r', type: 'resistor', a: 'p', b: 'n', value: R },
    { id: 'd', type: 'diode', a: 'n', b: 'g' },
  ] };
  let res;
  for (let i = 0; i < 5; i++) res = c.solve(elements, 0.001);
  const expected = (emf - CircuitEngine.DIODE_VF) /
    (CircuitEngine.BATTERY_RINT + R + CircuitEngine.DIODE_RON);
  approx('diode:forward-current-with-1k-limiter', res.currents.get('d'), expected, 2e-5);
  pass('diode:forward-node-clamped-near-vf', res.voltages.get('n') > CircuitEngine.DIODE_VF && res.voltages.get('n') < CircuitEngine.DIODE_VF + 0.05,
    `Vn=${res.voltages.get('n')}`);

  const c2 = new Circuit();
  elements.components[2] = { id: 'd', type: 'diode', a: 'g', b: 'n' };
  for (let i = 0; i < 5; i++) res = c2.solve(elements, 0.001);
  approx('diode:reverse-blocks-normal-5V', res.currents.get('d'), 0, 1e-6);
}

console.log(`\n=== ALL ${checks} NORMAL-CIRCUIT REALITY CHECKS PASSED ===`);
