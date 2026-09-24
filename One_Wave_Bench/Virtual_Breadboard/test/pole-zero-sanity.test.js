#!/usr/bin/env node
'use strict';

const CE = require('../js/circuit.js');
const { bodeTransfer } = require('../js/bode-analysis.js');
const { BATTERY_RINT, inductorDCR } = CE;

let checks = 0;
function check(name, condition, detail) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`POLE/ZERO SANITY FAILED: ${name}`);
}
function near(actual, expected, frac) {
  return Math.abs(actual - expected) <= Math.abs(expected) * frac;
}
function rowNearest(rows, f) {
  return rows.reduce((best, r) => Math.abs(Math.log(r.frequencyHz / f)) < Math.abs(Math.log(best.frequencyHz / f)) ? r : best, rows[0]);
}

console.log('=== Virtual Breadboard pole/zero sanity qualification ===');

// RC low-pass: source 1 ohm + 999 ohm = exactly 1 kohm feeding 1 uF.
// With the simulator's tiny capacitor parasitics, the dominant pole remains
// essentially the textbook 1/(2*pi*R*C) value.
{
  const R = BATTERY_RINT + 999;
  const C = 1e-6;
  const fp = 1 / (2 * Math.PI * R * C);
  const elements = { wires: [], components: [
    { id: 'V1', type: 'battery', value: 0, a: 'vin', b: 'gnd' },
    { id: 'R1', type: 'resistor', value: 999, a: 'vin', b: 'out' },
    { id: 'C1', type: 'capacitor', value: C, a: 'out', b: 'gnd' },
  ] };
  const bode = bodeTransfer(elements, {
    sourceId: 'V1', input: 'vin', output: 'out',
    frequencies: [fp / 10, fp, fp * 10],
  });
  const [lo, mid, hi] = bode.rows;
  const normalized = mid.magnitude / lo.magnitude;
  check('rc-pole-frequency-analytic', near(mid.frequencyHz, fp, 1e-12), `fp=${fp}`);
  check('rc-pole-is-about-minus-3db', Math.abs(20 * Math.log10(normalized) + 3.0103) < 0.2,
    `relative=${20 * Math.log10(normalized)}dB`);
  check('rc-pole-phase-about-minus-45deg', Math.abs(mid.phaseDeg + 45) < 1.0, `phase=${mid.phaseDeg}`);
  check('rc-post-pole-rolloff', hi.magnitudeDb < mid.magnitudeDb - 15, `mid=${mid.magnitudeDb} hi=${hi.magnitudeDb}`);
}

// RC high-pass: capacitor in series, resistor to ground. It has a zero at the
// origin: one decade lower in frequency should cost about 20 dB until the pole
// is reached, then the response flattens toward unity.
{
  const R = BATTERY_RINT + 999;
  const C = 1e-6;
  const fp = 1 / (2 * Math.PI * R * C);
  const elements = { wires: [], components: [
    { id: 'V1', type: 'battery', value: 0, a: 'vin', b: 'gnd' },
    { id: 'C1', type: 'capacitor', value: C, a: 'vin', b: 'out' },
    { id: 'R1', type: 'resistor', value: 999, a: 'out', b: 'gnd' },
  ] };
  const bode = bodeTransfer(elements, {
    sourceId: 'V1', input: 'vin', output: 'out',
    frequencies: [fp / 100, fp / 10, fp, fp * 10, fp * 100],
  });
  const [f001, f01, mid, f10, f100] = bode.rows;
  const riseDb = f01.magnitudeDb - f001.magnitudeDb;
  check('rc-highpass-origin-zero-slope', Math.abs(riseDb - 20) < 1.0, `rise/decade=${riseDb}dB`);
  check('rc-highpass-pole-about-minus-3db', Math.abs(mid.magnitudeDb + 3.0103) < 0.25, `mid=${mid.magnitudeDb}dB`);
  check('rc-highpass-flattens-above-pole', Math.abs(f100.magnitudeDb - f10.magnitudeDb) < 0.1,
    `10x=${f10.magnitudeDb} 100x=${f100.magnitudeDb}`);
}

// RL low-pass across R: exact pole includes battery output resistance and the
// simulator's physical inductor DCR.
{
  const L = 10e-3;
  const Rload = 999;
  const Rtotal = BATTERY_RINT + Rload + inductorDCR(L);
  const fp = Rtotal / (2 * Math.PI * L);
  const elements = { wires: [], components: [
    { id: 'V1', type: 'battery', value: 0, a: 'vin', b: 'gnd' },
    { id: 'L1', type: 'inductor', value: L, a: 'vin', b: 'out' },
    { id: 'R1', type: 'resistor', value: Rload, a: 'out', b: 'gnd' },
  ] };
  const bode = bodeTransfer(elements, {
    sourceId: 'V1', input: 'vin', output: 'out',
    frequencies: [fp / 10, fp, fp * 10],
  });
  const [lo, mid, hi] = bode.rows;
  const normalized = mid.magnitude / lo.magnitude;
  check('rl-pole-frequency-includes-dcr', near(mid.frequencyHz, fp, 1e-12), `fp=${fp}Hz DCR=${inductorDCR(L)}`);
  check('rl-pole-is-about-minus-3db', Math.abs(20 * Math.log10(normalized) + 3.0103) < 0.2,
    `relative=${20 * Math.log10(normalized)}dB`);
  check('rl-phase-about-minus-45deg', Math.abs(mid.phaseDeg + 45) < 0.6, `phase=${mid.phaseDeg}`);
  check('rl-rolloff-after-pole', hi.magnitudeDb < mid.magnitudeDb - 15, `mid=${mid.magnitudeDb} hi=${hi.magnitudeDb}`);
}

// Series RLC, output across R. The response peaks where XL and XC cancel,
// f0 = 1/(2*pi*sqrt(L*C)). Use a dense local sweep and verify the measured
// maximum stays close to that independently derived resonance.
{
  const L = 10e-3;
  const C = 1e-6;
  const Rload = 20;
  const f0 = 1 / (2 * Math.PI * Math.sqrt(L * C));
  const frequencies = [];
  for (let i = -20; i <= 20; i++) frequencies.push(f0 * Math.pow(10, i / 100));
  const elements = { wires: [], components: [
    { id: 'V1', type: 'battery', value: 0, a: 'vin', b: 'gnd' },
    { id: 'L1', type: 'inductor', value: L, a: 'vin', b: 'n1' },
    { id: 'C1', type: 'capacitor', value: C, a: 'n1', b: 'out' },
    { id: 'R1', type: 'resistor', value: Rload, a: 'out', b: 'gnd' },
  ] };
  const bode = bodeTransfer(elements, { sourceId: 'V1', input: 'vin', output: 'out', frequencies });
  const peak = bode.rows.reduce((best, r) => r.magnitude > best.magnitude ? r : best, bode.rows[0]);
  check('rlc-resonance-near-analytic-f0', Math.abs(peak.frequencyHz - f0) / f0 < 0.03,
    `analytic=${f0}Hz measured=${peak.frequencyHz}Hz`);
  const below = rowNearest(bode.rows, f0 / 1.5);
  const above = rowNearest(bode.rows, f0 * 1.5);
  check('rlc-resonance-is-a-real-peak', peak.magnitude > below.magnitude && peak.magnitude > above.magnitude,
    `below=${below.magnitude} peak=${peak.magnitude} above=${above.magnitude}`);
  check('rlc-phase-crosses-near-zero-at-resonance', Math.abs(peak.phaseDeg) < 8, `phase=${peak.phaseDeg}`);
}

console.log(`\n=== ALL ${checks} POLE/ZERO SANITY CHECKS PASSED ===`);
