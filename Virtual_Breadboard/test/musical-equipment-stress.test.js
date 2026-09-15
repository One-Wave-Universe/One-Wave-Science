#!/usr/bin/env node
'use strict';

const assert = require('assert');
const CE = require('../js/circuit.js');
const { Circuit, BATTERY_RINT, capacitorESR, inductorDCR } = CE;
const Sim = require('../simulate.js');
const Spice = require('../js/spice-analysis.js');
const { smallSignalAc, phasorMagnitude, phasorPhaseDeg } = require('../js/ac-analysis.js');

let checks = 0;
function ok(name, condition, detail = '') {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  assert(condition, `${name}${detail ? ': ' + detail : ''}`);
}
function close(name, actual, expected, tolerance, detail = '') {
  ok(name, Number.isFinite(actual) && Math.abs(actual - expected) <= tolerance,
    `${detail}${detail ? ' ' : ''}actual=${actual} expected=${expected} tol=${tolerance}`);
}
function magAt(elements, f, node, sourceId = 'VIN') {
  const r = smallSignalAc(elements, { sourceId, frequencies: [f], magnitude: 1, solverOptions: { maxIterations: 120 } });
  return phasorMagnitude(r.rows[0].voltages.get(r.uf.find(node)));
}
function gainAt(elements, f, inNode, outNode, sourceId = 'VIN') {
  const r = smallSignalAc(elements, { sourceId, frequencies: [f], magnitude: 1, solverOptions: { maxIterations: 120 } });
  const row = r.rows[0];
  const a = row.voltages.get(r.uf.find(inNode));
  const b = row.voltages.get(r.uf.find(outNode));
  const den = a.re * a.re + a.im * a.im;
  return {
    re: (b.re * a.re + b.im * a.im) / den,
    im: (b.im * a.re - b.re * a.im) / den,
  };
}

console.log('=== Virtual Breadboard musical-equipment stress pack ===');

// 1) Real headphone impedances punish output impedance. The answer is an
// independent voltage-divider calculation including VBB's disclosed 1-ohm
// battery/source resistance, not a subjective loudness judgement.
for (const load of [16, 32, 80, 250, 600]) {
  const elements = { wires: [], components: [
    { id: 'VIN', type: 'battery', value: 0, a: 'src', b: 'gnd' },
    { id: 'ROUT', type: 'resistor', value: 10, a: 'src', b: 'out' },
    { id: 'HP', type: 'resistor', value: load, a: 'out', b: 'gnd' },
  ] };
  const actual = magAt(elements, 1000, 'out');
  const expected = load / (load + 10 + BATTERY_RINT);
  close(`headphone-${load}ohm-loaded-level`, actual, expected, 2e-5,
    `10ohm output impedance into ${load}ohm headphones`);
}

// 2) Headphone output coupling capacitor: verify bass corner and verify that
// DC is blocked down to only the model's real capacitor leakage current.
{
  const C = 470e-6;
  const cap = { id: 'COUT', type: 'capacitor', value: C, a: 'pre', b: 'out' };
  const elements = { wires: [], components: [
    { id: 'VIN', type: 'battery', value: 0, a: 'src', b: 'gnd' },
    { id: 'ROUT', type: 'resistor', value: 10, a: 'src', b: 'pre' },
    cap,
    { id: 'HP', type: 'resistor', value: 32, a: 'out', b: 'gnd' },
  ] };
  for (const f of [20, 1000]) {
    const seriesR = 32 + 10 + BATTERY_RINT + capacitorESR(cap);
    const xc = 1 / (2 * Math.PI * f * C);
    const expected = 32 / Math.sqrt(seriesR * seriesR + xc * xc);
    close(`headphone-coupling-cap-${f}Hz`, magAt(elements, f, 'out'), expected, 0.012,
      `ESR=${capacitorESR(cap)} Xc=${xc}`);
  }
  const dc = { wires: [], components: [
    { id: 'VIN', type: 'battery', value: 1, a: 'src', b: 'gnd' },
    { id: 'ROUT', type: 'resistor', value: 10, a: 'src', b: 'pre' },
    cap,
    { id: 'HP', type: 'resistor', value: 32, a: 'out', b: 'gnd' },
  ] };
  const op = Spice.operatingPoint(dc);
  const out = op.voltages.get('out') || 0;
  ok('headphone-coupling-cap-blocks-dc', Math.abs(out) < 2e-5,
    `DC at headphone=${out}V; finite capacitor leakage is allowed`);
}

// 3) Dynamic-microphone electrical interface: winding resistance + inductance
// feeding a finite preamp input. The inductance must make the high-frequency
// source/load interaction different from the low-frequency case.
{
  const elements = { wires: [], components: [
    { id: 'VIN', type: 'battery', value: 0, a: 'src', b: 'gnd' },
    { id: 'RMIC', type: 'resistor', value: 200, a: 'src', b: 'coil' },
    { id: 'LMIC', type: 'inductor', value: 0.02, a: 'coil', b: 'out' },
    { id: 'RPRE', type: 'resistor', value: 2000, a: 'out', b: 'gnd' },
  ] };
  const low = magAt(elements, 100, 'out');
  const high = magAt(elements, 20000, 'out');
  ok('dynamic-mic-low-band-transfer-is-strong', low > 0.85, `100Hz=${low}`);
  ok('dynamic-mic-coil-inductance-changes-high-band-loading', high < low * 0.75,
    `100Hz=${low} 20kHz=${high} L-DCR=${inductorDCR(0.02)}`);
}

// 4) Common-mode hum through a balanced line. Perfectly matched legs are the
// zero-differential control; 1%, 5%, and 10% source-resistance mismatch must
// monotonically convert more common-mode signal into differential error.
function commonModeLeak(mismatchPct) {
  const rn = 100 * (1 + mismatchPct / 100);
  const elements = { wires: [], components: [
    { id: 'VCM', type: 'battery', value: 0, a: 'cm', b: 'gnd' },
    { id: 'EP', type: 'vcvs', a: 'p0', b: 'gnd', controlP: 'cm', controlN: 'gnd', gain: 1 },
    { id: 'EN', type: 'vcvs', a: 'n0', b: 'gnd', controlP: 'cm', controlN: 'gnd', gain: 1 },
    { id: 'RP', type: 'resistor', value: 100, a: 'p0', b: 'p' },
    { id: 'RN', type: 'resistor', value: rn, a: 'n0', b: 'n' },
    { id: 'RPL', type: 'resistor', value: 10000, a: 'p', b: 'gnd' },
    { id: 'RNL', type: 'resistor', value: 10000, a: 'n', b: 'gnd' },
  ] };
  const r = smallSignalAc(elements, { sourceId: 'VCM', frequencies: [60], magnitude: 1 });
  const row = r.rows[0];
  const p = row.voltages.get(r.uf.find('p'));
  const n = row.voltages.get(r.uf.find('n'));
  return phasorMagnitude({ re: p.re - n.re, im: p.im - n.im });
}
{
  const d0 = commonModeLeak(0);
  const d1 = commonModeLeak(1);
  const d5 = commonModeLeak(5);
  const d10 = commonModeLeak(10);
  ok('balanced-hum-control-is-near-zero', d0 < 1e-9, `matched=${d0}`);
  ok('balanced-line-imbalance-converts-common-mode', d1 > 5e-5, `1%=${d1}`);
  ok('common-mode-leakage-grows-with-imbalance', d1 < d5 && d5 < d10,
    `1%=${d1} 5%=${d5} 10%=${d10}`);
  ok('ten-percent-imbalance-stays-small-but-measurable', d10 > 5e-4 && d10 < 0.01,
    `10% differential=${d10}`);
}

// 5) A small 9V BJT preamp using an actual divider bias, emitter resistor,
// input/output coupling capacitors and 100k following load. This moves beyond
// a bare transistor fixture into a recognisable pedal/preamp topology.
function bjtPreamp() {
  return { wires: [], components: [
    { id: 'VCC', type: 'battery', value: 9, a: 'vcc', b: 'gnd' },
    { id: 'VIN', type: 'battery', value: 0, a: 'in', b: 'gnd' },
    { id: 'R1', type: 'resistor', value: 100000, a: 'vcc', b: 'base' },
    { id: 'R2', type: 'resistor', value: 18000, a: 'base', b: 'gnd' },
    { id: 'RE', type: 'resistor', value: 1000, a: 'emit', b: 'gnd' },
    { id: 'RC', type: 'resistor', value: 4700, a: 'vcc', b: 'collector' },
    { id: 'Q1', type: 'npn', base: 'base', collector: 'collector', emitter: 'emit', betaF: 100 },
    { id: 'CIN', type: 'capacitor', value: 100e-9, a: 'in', b: 'base' },
    { id: 'COUT', type: 'capacitor', value: 1e-6, a: 'collector', b: 'out' },
    { id: 'RLOAD', type: 'resistor', value: 100000, a: 'out', b: 'gnd' },
  ] };
}
{
  const elements = bjtPreamp();
  const op = Spice.operatingPoint(elements, { solverOptions: { maxIterations: 120 } });
  const vc = op.voltages.get('collector');
  const ve = op.voltages.get('emit');
  const ic = op.currents.get('Q1:collector');
  ok('bjt-preamp-dc-op-converges', op.solver.converged === true, JSON.stringify(op.solver));
  ok('bjt-preamp-bias-is-forward-active', vc > 3 && vc < 8 && ve > 0.2 && ve < 1.2,
    `Vc=${vc} Ve=${ve} Ic=${ic}`);
  ok('bjt-preamp-current-is-pedal-scale', ic > 2e-4 && ic < 1.5e-3, `Ic=${ic}`);
  const gain = gainAt(elements, 1000, 'in', 'out');
  const gainMag = phasorMagnitude(gain);
  const phase = Math.abs(phasorPhaseDeg(gain));
  ok('bjt-preamp-has-real-voltage-gain', gainMag > 2 && gainMag < 10, `gain=${gainMag}`);
  ok('bjt-preamp-common-emitter-inverts', phase > 150, `phase=${phasorPhaseDeg(gain)}`);
}

// 6) DI/microphone-transformer style control. A lightly loaded secondary
// should preserve the turns ratio; a 600-ohm load must reflect back and pull
// measurably more primary current from the source.
function transformerMetrics(loadR) {
  const c = new Circuit();
  const elements = { wires: [], components: [
    { id: 'AC', type: 'acsource', value: 1, freq: 1000, a: 'p', b: 'gnd' },
    { id: 'LOAD', type: 'resistor', value: loadR, a: 's', b: 'gnd' },
    { id: 'T', type: 'toroid', coupling: 0.97, windings: [
      { a: 'p', b: 'gnd', N: 10, R: 0.5, L: 0.1 },
      { a: 's', b: 'gnd', N: 20, R: 0.8, L: 0.4 },
    ] },
  ] };
  const dt = 1 / 1000 / 200;
  const pV = [], sV = [], pI = [];
  let r;
  for (let i = 0; i < 800; i++) {
    r = c.solve(elements, dt);
    if (i > 500) {
      pV.push({ t: i * dt, value: r.voltages.get('p') - r.voltages.get('gnd') });
      sV.push({ t: i * dt, value: r.voltages.get('s') - r.voltages.get('gnd') });
      pI.push({ t: i * dt, value: r.currents.get('T:0') || 0 });
    }
  }
  return { ratio: Sim.rmsValue(sV) / Sim.rmsValue(pV), primaryCurrent: Sim.rmsValue(pI) };
}
{
  const openish = transformerMetrics(1e6);
  const loaded = transformerMetrics(600);
  ok('di-transformer-open-load-near-turns-ratio', openish.ratio > 1.6 && openish.ratio < 2.2,
    `ratio=${openish.ratio}`);
  ok('di-transformer-load-reflects-to-primary', loaded.primaryCurrent > openish.primaryCurrent * 1.5,
    `open=${openish.primaryCurrent}A loaded=${loaded.primaryCurrent}A`);
  ok('di-transformer-load-reduces-secondary-voltage', loaded.ratio < openish.ratio,
    `open ratio=${openish.ratio} loaded ratio=${loaded.ratio}`);
}

// 7) Pedal-chain fanout. Three normal high-Z inputs should barely load a low-
// impedance pedal output; one accidentally low 10k input must visibly pull the
// bus down. This catches hidden source-impedance assumptions.
function pedalBus(extraLowLoad) {
  const components = [
    { id: 'VIN', type: 'battery', value: 0, a: 'src', b: 'gnd' },
    { id: 'ROUT', type: 'resistor', value: 1000, a: 'src', b: 'bus' },
    { id: 'IN1', type: 'resistor', value: 100000, a: 'bus', b: 'gnd' },
    { id: 'IN2', type: 'resistor', value: 100000, a: 'bus', b: 'gnd' },
    { id: 'IN3', type: 'resistor', value: 100000, a: 'bus', b: 'gnd' },
  ];
  if (extraLowLoad) components.push({ id: 'BADIN', type: 'resistor', value: 10000, a: 'bus', b: 'gnd' });
  return magAt({ wires: [], components }, 1000, 'bus');
}
{
  const normal = pedalBus(false);
  const bad = pedalBus(true);
  const rEq = 1 / (3 / 100000);
  const expected = rEq / (rEq + 1000 + BATTERY_RINT);
  close('three-pedal-parallel-inputs-match-hand-load', normal, expected, 2e-5);
  ok('low-z-pedal-input-drags-whole-chain', bad < normal * 0.92, `normal=${normal} bad=${bad}`);
}

// 8) Phantom-power-style symmetric feed as a balance/reference control. The
// equal 6.81k legs must land together; a 1% feed mismatch must create a real
// differential offset rather than being silently averaged away.
function phantomDiff(rNeg) {
  const elements = { wires: [], components: [
    { id: 'V48', type: 'battery', value: 48, a: 'v48', b: 'gnd' },
    { id: 'RP', type: 'resistor', value: 6810, a: 'v48', b: 'p' },
    { id: 'RN', type: 'resistor', value: rNeg, a: 'v48', b: 'n' },
    { id: 'MP', type: 'resistor', value: 1000, a: 'p', b: 'common' },
    { id: 'MN', type: 'resistor', value: 1000, a: 'n', b: 'common' },
    { id: 'RET', type: 'resistor', value: 2000, a: 'common', b: 'gnd' },
  ] };
  const r = new Circuit().solve(elements, 1e-3);
  return (r.voltages.get(r.uf.find('p')) || 0) - (r.voltages.get(r.uf.find('n')) || 0);
}
{
  const balanced = phantomDiff(6810);
  const mismatched = phantomDiff(6810 * 1.01);
  ok('phantom-feed-balanced-legs-share-reference', Math.abs(balanced) < 1e-6, `diff=${balanced}`);
  ok('phantom-feed-one-percent-mismatch-is-visible', Math.abs(mismatched) > 0.005,
    `1% mismatch diff=${mismatched}`);
}

console.log(`\n=== ALL ${checks} MUSICAL-EQUIPMENT STRESS CHECKS PASSED ===`);
