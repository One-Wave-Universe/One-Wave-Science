#!/usr/bin/env node
'use strict';

const CE = require('../js/circuit.js');
const { bodeTransfer, unwrapPhaseDegrees } = require('../js/bode-analysis.js');
const { capacitorESR, capacitorLeakageR } = CE;

let checks = 0;
function check(name, condition, detail) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`BODE QUALIFICATION FAILED: ${name}`);
}

const C = (re, im) => ({ re, im });
const add = (a, b) => C(a.re + b.re, a.im + b.im);
const div = (a, b) => {
  const d = b.re * b.re + b.im * b.im;
  return C((a.re * b.re + a.im * b.im) / d, (a.im * b.re - a.re * b.im) / d);
};
const mag = (z) => Math.hypot(z.re, z.im);
const phase = (z) => Math.atan2(z.im, z.re) * 180 / Math.PI;

console.log('=== Virtual Breadboard Bode qualification ===');

// RC low-pass transfer from the actual source terminal vin to the output.
// The analytic reference includes the simulator's physical capacitor ESR and
// leakage. Because H=Vout/Vin, the battery's 1-ohm internal R cancels out of
// this particular transfer definition; only the declared 999-ohm R is in H.
{
  const cap = { id: 'C1', type: 'capacitor', value: 1e-6, a: 'out', b: 'gnd' };
  const R = 999;
  const f = 1 / (2 * Math.PI * 1000 * cap.value);
  const elements = { wires: [], components: [
    { id: 'V1', type: 'battery', value: 0, a: 'vin', b: 'gnd' },
    { id: 'R1', type: 'resistor', value: R, a: 'vin', b: 'out' },
    cap,
  ] };
  const result = bodeTransfer(elements, {
    sourceId: 'V1', frequencies: [f], input: 'vin', output: 'out', magnitude: 1,
  });
  const row = result.rows[0];
  const w = 2 * Math.PI * f;
  const zSeriesC = C(capacitorESR(cap), -1 / (w * cap.value));
  const zc = div(C(1, 0), add(div(C(1, 0), zSeriesC), C(1 / capacitorLeakageR(cap), 0)));
  const expected = div(zc, add(C(R, 0), zc));
  const expectedMag = mag(expected);
  const expectedDb = 20 * Math.log10(expectedMag);
  const expectedPhase = phase(expected);

  check('bode-analysis-named', result.analysis.type === 'bode' && result.analysis.transferFunction === true,
    JSON.stringify(result.analysis));
  check('rc-transfer-real', Math.abs(row.transfer.re - expected.re) < 2e-6,
    `actual=${row.transfer.re} expected=${expected.re}`);
  check('rc-transfer-imag', Math.abs(row.transfer.im - expected.im) < 2e-6,
    `actual=${row.transfer.im} expected=${expected.im}`);
  check('rc-magnitude', Math.abs(row.magnitude - expectedMag) < 2e-6,
    `actual=${row.magnitude} expected=${expectedMag}`);
  check('rc-db', Math.abs(row.magnitudeDb - expectedDb) < 2e-5,
    `actual=${row.magnitudeDb} expected=${expectedDb}`);
  check('rc-phase', Math.abs(row.phaseDeg - expectedPhase) < 2e-4,
    `actual=${row.phaseDeg} expected=${expectedPhase}`);
  check('single-point-unwrapped-equals-wrapped', row.unwrappedPhaseDeg === row.phaseDeg);
}

// Differential probes: transfer between two differential node pairs must be
// computed from phasor differences, not from either node alone.
{
  const elements = { wires: [], components: [
    { id: 'V1', type: 'battery', value: 0, a: 'p', b: 'n' },
    { id: 'R1', type: 'resistor', value: 1000, a: 'p', b: 'mid' },
    { id: 'R2', type: 'resistor', value: 1000, a: 'mid', b: 'n' },
  ] };
  const result = bodeTransfer(elements, {
    sourceId: 'V1', frequencies: [1000],
    input: { positive: 'p', negative: 'n' },
    output: { positive: 'mid', negative: 'n' },
  });
  const row = result.rows[0];
  check('differential-probe-half-gain', Math.abs(row.magnitude - 0.5) < 0.001,
    `gain=${row.magnitude}`);
  check('differential-probe-zero-phase', Math.abs(row.phaseDeg) < 0.01,
    `phase=${row.phaseDeg}`);
}

// Sweep rows are plot-ready and ordered exactly like the AC frequency sweep.
{
  const elements = { wires: [], components: [
    { id: 'V1', type: 'battery', value: 0, a: 'vin', b: 'gnd' },
    { id: 'R1', type: 'resistor', value: 1000, a: 'vin', b: 'out' },
    { id: 'C1', type: 'capacitor', value: 1e-6, a: 'out', b: 'gnd' },
  ] };
  const result = bodeTransfer(elements, {
    sourceId: 'V1', startHz: 10, stopHz: 100000, pointsPerDecade: 4,
    input: 'vin', output: 'out',
  });
  check('sweep-row-count-matches-frequency-count', result.rows.length === result.frequencies.length,
    `rows=${result.rows.length} f=${result.frequencies.length}`);
  check('sweep-frequency-order-preserved', result.rows.every((r, i) => r.frequencyHz === result.frequencies[i]));
  check('lowpass-gain-falls-with-frequency', result.rows.at(-1).magnitude < result.rows[0].magnitude,
    `${result.rows[0].magnitude} -> ${result.rows.at(-1).magnitude}`);
  check('lowpass-phase-more-negative-at-high-frequency', result.rows.at(-1).unwrappedPhaseDeg < result.rows[0].unwrappedPhaseDeg,
    `${result.rows[0].unwrappedPhaseDeg} -> ${result.rows.at(-1).unwrappedPhaseDeg}`);
}

// Unwrap helper must remove artificial +/-180-degree plotting jumps without
// altering an already continuous sequence.
{
  const wrapped = [170, 179, -179, -170, -160];
  const u = unwrapPhaseDegrees(wrapped);
  check('phase-unwrapper-removes-wrap-jump', JSON.stringify(u) === JSON.stringify([170, 179, 181, 190, 200]), JSON.stringify(u));
  const already = [-10, -20, -30];
  check('phase-unwrapper-preserves-continuous-phase', JSON.stringify(unwrapPhaseDegrees(already)) === JSON.stringify(already));
}

console.log(`\n=== ALL ${checks} BODE CHECKS PASSED ===`);
