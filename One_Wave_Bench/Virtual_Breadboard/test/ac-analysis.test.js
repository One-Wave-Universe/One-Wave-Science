#!/usr/bin/env node
'use strict';

const CE = require('../js/circuit.js');
const AC = require('../js/ac-analysis.js');
const {
  BATTERY_RINT, capacitorESR, capacitorLeakageR, inductorDCR,
  DIODE_IS, DIODE_N, THERMAL_VOLTAGE_25C,
} = CE;
const { smallSignalAc, phasorMagnitude, phasorPhaseDeg } = AC;

let checks = 0;
function check(name, condition, detail) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`AC ANALYSIS QUALIFICATION FAILED: ${name}`);
}
const C = (re, im) => ({ re, im });
const add = (a, b) => C(a.re + b.re, a.im + b.im);
const div = (a, b) => {
  const d = b.re * b.re + b.im * b.im;
  return C((a.re * b.re + a.im * b.im) / d, (a.im * b.re - a.re * b.im) / d);
};
const closeComplex = (actual, expected, tol = 2e-6) => Math.hypot(actual.re - expected.re, actual.im - expected.im) <= tol;
function node(row, result, name) { return row.voltages.get(result.uf.find(name)); }

console.log('=== Virtual Breadboard small-signal AC qualification ===');

// RC low-pass. R is 999 ohm so the source's real 1-ohm output resistance
// makes the nominal series resistance exactly 1000 ohm. The exact reference
// includes the simulator's real capacitor ESR and leakage, so its phase is
// intentionally a little different from the ideal textbook -45 degrees.
{
  const cap = { id: 'C1', type: 'capacitor', value: 1e-6, a: 'out', b: 'gnd' };
  const elements = { wires: [], components: [
    { id: 'V1', type: 'battery', value: 0, a: 'vin', b: 'gnd' },
    { id: 'R1', type: 'resistor', value: 999, a: 'vin', b: 'out' },
    cap,
  ] };
  const f = 1 / (2 * Math.PI * 1000 * cap.value);
  const result = smallSignalAc(elements, { sourceId: 'V1', frequencies: [f], magnitude: 1 });
  const actual = node(result.rows[0], result, 'out');
  const w = 2 * Math.PI * f;
  const zSeriesC = C(capacitorESR(cap), -1 / (w * cap.value));
  const ySeries = div(C(1, 0), zSeriesC);
  const yLeak = C(1 / capacitorLeakageR(cap), 0);
  const zc = div(C(1, 0), add(ySeries, yLeak));
  const expected = div(zc, add(C(BATTERY_RINT + 999, 0), zc));
  check('rc-complex-transfer', closeComplex(actual, expected), `actual=${JSON.stringify(actual)} expected=${JSON.stringify(expected)}`);
  check('rc-phase-matches-physical-model', Math.abs(phasorPhaseDeg(actual) - phasorPhaseDeg(expected)) < 0.001,
    `actual=${phasorPhaseDeg(actual)} expected=${phasorPhaseDeg(expected)}`);
  check('rc-magnitude-matches-physical-model', Math.abs(phasorMagnitude(actual) - phasorMagnitude(expected)) < 1e-6,
    `actual=${phasorMagnitude(actual)} expected=${phasorMagnitude(expected)}`);
}

// RL low-pass, measured across the load resistor.
{
  const L = 10e-3;
  const R = 999;
  const elements = { wires: [], components: [
    { id: 'V1', type: 'battery', value: 0, a: 'vin', b: 'gnd' },
    { id: 'L1', type: 'inductor', value: L, a: 'vin', b: 'out' },
    { id: 'R1', type: 'resistor', value: R, a: 'out', b: 'gnd' },
  ] };
  const f = 2000;
  const result = smallSignalAc(elements, { sourceId: 'V1', frequencies: [f] });
  const actual = node(result.rows[0], result, 'out');
  const zL = C(inductorDCR(L), 2 * Math.PI * f * L);
  const expected = div(C(R, 0), add(C(BATTERY_RINT + R, 0), zL));
  check('rl-complex-transfer', closeComplex(actual, expected), `actual=${JSON.stringify(actual)} expected=${JSON.stringify(expected)}`);
  check('rl-phase-negative', phasorPhaseDeg(actual) < 0, `phase=${phasorPhaseDeg(actual)}`);
}

// Series RLC reference: validates that C and L are both true phasor
// impedances in the same solve, not transient approximations sampled in time.
{
  const L = 10e-3;
  const cap = { id: 'C1', type: 'capacitor', value: 1e-6, a: 'n1', b: 'out' };
  const R = 999;
  const f = 1200;
  const elements = { wires: [], components: [
    { id: 'V1', type: 'battery', value: 0, a: 'vin', b: 'gnd' },
    { id: 'L1', type: 'inductor', value: L, a: 'vin', b: 'n1' },
    cap,
    { id: 'R1', type: 'resistor', value: R, a: 'out', b: 'gnd' },
  ] };
  const result = smallSignalAc(elements, { sourceId: 'V1', frequencies: [f] });
  const actual = node(result.rows[0], result, 'out');
  const w = 2 * Math.PI * f;
  const zL = C(inductorDCR(L), w * L);
  const zSeriesC = C(capacitorESR(cap), -1 / (w * cap.value));
  const zC = div(C(1, 0), add(div(C(1, 0), zSeriesC), C(1 / capacitorLeakageR(cap), 0)));
  const expected = div(C(R, 0), add(add(C(BATTERY_RINT + R, 0), zL), zC));
  check('rlc-complex-transfer', closeComplex(actual, expected), `actual=${JSON.stringify(actual)} expected=${JSON.stringify(expected)}`);
}

// Nonlinear proof: the AC solve must use the diode's local slope at the DC
// operating point, not its large-signal current or the old hard threshold.
{
  const elements = { wires: [], components: [
    { id: 'V1', type: 'battery', value: 0.6, a: 'vin', b: 'gnd' },
    { id: 'D1', type: 'diode', a: 'vin', b: 'gnd' },
  ] };
  const result = smallSignalAc(elements, { sourceId: 'V1', frequencies: [1000], magnitude: 1 });
  const row = result.rows[0];
  const actual = node(row, result, 'vin');
  const opRoot = result.operatingPoint.uf.find('vin');
  const vd = result.operatingPoint.voltages.get(opRoot) || 0;
  const nvt = DIODE_N * THERMAL_VOLTAGE_25C;
  const gd = DIODE_IS * Math.exp(Math.max(-5, Math.min(0.8, vd)) / nvt) / nvt;
  const expectedMag = 1 / (1 + BATTERY_RINT * (gd + 1e-9));
  check('diode-op-converged', result.operatingPoint.solver.converged === true, JSON.stringify(result.operatingPoint.solver));
  check('diode-small-signal-slope', Math.abs(phasorMagnitude(actual) - expectedMag) < 2e-6,
    `Vop=${vd} gd=${gd} actual=${phasorMagnitude(actual)} expected=${expectedMag}`);
}

// Log-frequency generator sanity.
{
  const elements = { wires: [], components: [
    { id: 'V1', type: 'battery', value: 0, a: 'vin', b: 'gnd' },
    { id: 'R1', type: 'resistor', value: 1000, a: 'vin', b: 'gnd' },
  ] };
  const result = smallSignalAc(elements, { sourceId: 'V1', startHz: 10, stopHz: 10000, pointsPerDecade: 4 });
  check('log-sweep-start', result.frequencies[0] === 10, `${result.frequencies[0]}`);
  check('log-sweep-stop', result.frequencies[result.frequencies.length - 1] === 10000, `${result.frequencies.at(-1)}`);
  check('log-sweep-has-13-points', result.frequencies.length === 13, `count=${result.frequencies.length}`);
}

console.log(`\n=== ALL ${checks} AC-ANALYSIS CHECKS PASSED ===`);
