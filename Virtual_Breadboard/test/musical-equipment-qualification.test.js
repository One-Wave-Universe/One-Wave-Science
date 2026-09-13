#!/usr/bin/env node
'use strict';

const assert = require('assert');
const { Circuit } = require('../js/circuit.js');
const { smallSignalAc, phasorMagnitude } = require('../js/ac-analysis.js');
const { transientAnalysis } = require('../js/spice-analysis.js');

let checks = 0;
function ok(name, condition, detail = '') {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  assert(condition, `${name}${detail ? ': ' + detail : ''}`);
}
function between(name, value, lo, hi, detail = '') {
  ok(name, Number.isFinite(value) && value >= lo && value <= hi,
    `${detail}${detail ? ' ' : ''}value=${value} range=[${lo}, ${hi}]`);
}
function csub(a, b) { return { re: a.re - b.re, im: a.im - b.im }; }
function cadd(a, b) { return { re: a.re + b.re, im: a.im + b.im }; }
function cscale(a, k) { return { re: a.re * k, im: a.im * k }; }
function ac(elements, freq, sourceId = 'VIN', magnitude = 1) {
  return smallSignalAc(elements, { sourceId, frequencies: [freq], magnitude });
}
function acNode(elements, freq, nodeName, sourceId = 'VIN', magnitude = 1) {
  const r = ac(elements, freq, sourceId, magnitude);
  const z = r.rows[0].voltages.get(r.uf.find(nodeName));
  return { result: r, phasor: z, mag: phasorMagnitude(z) };
}
function pickupRig({ cableC = 470e-12, inputR = 1e6, toneR = null, toneC = 22e-9 } = {}) {
  const components = [
    { id: 'VIN', type: 'battery', value: 0, a: 'src', b: 'gnd' },
    // Representative passive guitar pickup: winding resistance + inductance.
    { id: 'RPU', type: 'resistor', value: 6000, a: 'src', b: 'coil' },
    { id: 'LPU', type: 'inductor', value: 2, a: 'coil', b: 'hot' },
    // Cable capacitance and following amp/pedal input impedance are where a
    // real passive pickup's resonant peak and treble loss actually come from.
    { id: 'CCABLE', type: 'capacitor', value: cableC, a: 'hot', b: 'gnd' },
    { id: 'RIN', type: 'resistor', value: inputR, a: 'hot', b: 'gnd' },
  ];
  if (toneR != null) {
    components.push({ id: 'RTONE', type: 'resistor', value: toneR, a: 'hot', b: 'tone' });
    components.push({ id: 'CTONE', type: 'capacitor', value: toneC, a: 'tone', b: 'gnd' });
  }
  return { wires: [], components };
}
function solveClip(vin, asymmetric = false) {
  const components = [
    { id: 'VIN', type: 'battery', value: vin, a: 'src', b: 'gnd' },
    { id: 'RDRIVE', type: 'resistor', value: 10000, a: 'src', b: 'out' },
    { id: 'DP', type: 'diode', a: 'out', b: 'gnd' },
  ];
  if (asymmetric) {
    // One diode on the positive half-cycle, two in series on the negative
    // half-cycle: the standard physical reason asymmetric overdrive clips
    // one polarity later than the other.
    components.push({ id: 'DN1', type: 'diode', a: 'gnd', b: 'nneg' });
    components.push({ id: 'DN2', type: 'diode', a: 'nneg', b: 'out' });
  } else {
    components.push({ id: 'DN', type: 'diode', a: 'gnd', b: 'out' });
  }
  const r = new Circuit().solve({ wires: [], components }, 1e-4, 25,
    { diodeModel: 'newton', maxIterations: 120 });
  ok(`clip-solver-converges-${asymmetric ? 'asym' : 'sym'}-${vin > 0 ? 'pos' : 'neg'}`,
    r.solver.converged === true, JSON.stringify(r.solver));
  return r.voltages.get(r.uf.find('out')) || 0;
}

console.log('=== Virtual Breadboard musical-equipment qualification ===');

// 1) Passive pickup + cable + amp input: a real resonant instrument source,
// not a generic RC toy. It must pass low frequencies, form a resonance, then
// roll off above that resonance.
{
  const rig = pickupRig();
  const v100 = acNode(rig, 100, 'hot').mag;
  const v1k = acNode(rig, 1000, 'hot').mag;
  const v5k = acNode(rig, 5000, 'hot').mag;
  const v10k = acNode(rig, 10000, 'hot').mag;
  ok('pickup-low-band-is-not-lost', v100 > 0.90, `100Hz=${v100}`);
  ok('pickup-cable-network-forms-real-resonance', v5k > v1k * 1.5,
    `1kHz=${v1k} 5kHz=${v5k}`);
  ok('pickup-response-rolls-after-resonance', v10k < v5k * 0.25,
    `5kHz=${v5k} 10kHz=${v10k}`);
}

// 2) Guitar cable capacitance. Long/high-capacitance cable must materially
// change the same pickup rather than producing the same canned waveform.
{
  const normal = pickupRig({ cableC: 470e-12 });
  const longCable = pickupRig({ cableC: 2e-9 });
  const normal8k = acNode(normal, 8000, 'hot').mag;
  const long8k = acNode(longCable, 8000, 'hot').mag;
  const long3k = acNode(longCable, 3000, 'hot').mag;
  const long5k = acNode(longCable, 5000, 'hot').mag;
  ok('long-cable-capacitance-kills-more-upper-treble', long8k < normal8k * 0.30,
    `470pF@8k=${normal8k} 2nF@8k=${long8k}`);
  ok('long-cable-shifts-resonance-downward', long3k > long5k * 2,
    `2nF: 3k=${long3k} 5k=${long5k}`);
}

// 3) Pedal/amp input loading. A 1 Mohm guitar input should preserve more of
// the passive pickup signal than a deliberately low 100 kohm input.
{
  const hiZ = acNode(pickupRig({ inputR: 1e6 }), 1000, 'hot').mag;
  const lowZ = acNode(pickupRig({ inputR: 100e3 }), 1000, 'hot').mag;
  ok('high-z-instrument-input-loads-pickup-less', hiZ > lowZ * 1.03,
    `1Mohm=${hiZ} 100kohm=${lowZ}`);
}

// 4) Passive guitar tone control. Turning the tone network down should remove
// treble aggressively without acting like a broadband mute.
{
  const toneUp = pickupRig({ toneR: 250e3 });
  const toneDown = pickupRig({ toneR: 10e3 });
  const up200 = acNode(toneUp, 200, 'hot').mag;
  const down200 = acNode(toneDown, 200, 'hot').mag;
  const up5k = acNode(toneUp, 5000, 'hot').mag;
  const down5k = acNode(toneDown, 5000, 'hot').mag;
  ok('tone-down-preserves-most-low-frequency-level', down200 > up200 * 0.85,
    `up200=${up200} down200=${down200}`);
  ok('tone-down-removes-upper-mid-treble', down5k < up5k * 0.15,
    `up5k=${up5k} down5k=${down5k}`);
}

// 5) Pedal coupling capacitor. A sensible 1 uF input coupling capacitor into
// 10 kohm must pass bass; an intentionally undersized 10 nF capacitor is the
// failure/control case and must audibly eat low end.
{
  function coupling(cap) {
    return { wires: [], components: [
      { id: 'VIN', type: 'battery', value: 0, a: 'src', b: 'gnd' },
      { id: 'CIN', type: 'capacitor', value: cap, a: 'src', b: 'out' },
      { id: 'RLOAD', type: 'resistor', value: 10000, a: 'out', b: 'gnd' },
    ] };
  }
  const good20 = acNode(coupling(1e-6), 20, 'out').mag;
  const good1k = acNode(coupling(1e-6), 1000, 'out').mag;
  const bad100 = acNode(coupling(10e-9), 100, 'out').mag;
  between('1uF-coupler-still-passes-20Hz', good20, 0.70, 1.01);
  ok('1uF-coupler-is-flat-by-1kHz', good1k > 0.98, `1k=${good1k}`);
  ok('undersized-coupler-proves-real-bass-loss', bad100 < 0.12, `10nF@100Hz=${bad100}`);
}

// 6) Symmetric diode clipping: a pedal-style 10k drive resistor feeding two
// anti-parallel silicon diodes must compress both polarities similarly.
{
  const pos = solveClip(3, false);
  const neg = solveClip(-3, false);
  between('symmetric-clip-positive-is-diode-scale', pos, 0.55, 1.10);
  between('symmetric-clip-negative-is-diode-scale', neg, -1.10, -0.55);
  ok('symmetric-clip-is-polarity-balanced', Math.abs(pos + neg) < 0.06,
    `pos=${pos} neg=${neg}`);
  ok('symmetric-clip-compresses-3V-input', Math.abs(pos / 3) < 0.40,
    `gain=${pos / 3}`);
}

// 7) Asymmetric overdrive: two series diodes on one half-cycle should move
// that clipping threshold outward relative to the single-diode half-cycle.
{
  const pos = solveClip(3, true);
  const neg = solveClip(-3, true);
  ok('asymmetric-clip-has-two-distinct-thresholds', Math.abs(neg) > pos + 0.45,
    `positive=${pos} negative=${neg}`);
  between('asymmetric-two-diode-side-stays-physical', Math.abs(neg), 1.10, 2.10);
}

// 8) Loudspeaker/voice-coil load. A real 8 ohm + 1 mH load must draw less
// current at 10 kHz than at 100 Hz because its inductive impedance rises.
{
  const speaker = { wires: [], components: [
    { id: 'VIN', type: 'battery', value: 0, a: 'src', b: 'gnd' },
    { id: 'RSRC', type: 'resistor', value: 10, a: 'src', b: 'drive' },
    { id: 'RVC', type: 'resistor', value: 8, a: 'drive', b: 'coil' },
    { id: 'LVC', type: 'inductor', value: 1e-3, a: 'coil', b: 'gnd' },
  ] };
  function sourceCurrent(f) {
    const r = ac(speaker, f);
    const row = r.rows[0];
    const vs = row.voltages.get(r.uf.find('src'));
    const vd = row.voltages.get(r.uf.find('drive'));
    return phasorMagnitude(cscale(csub(vs, vd), 1 / 10));
  }
  const i100 = sourceCurrent(100);
  const i10k = sourceCurrent(10000);
  ok('speaker-coil-impedance-rises-with-frequency', i10k < i100 * 0.45,
    `I100=${i100} I10k=${i10k}`);
}

// 9) First-order tweeter crossover: series capacitor into an 8 ohm load.
{
  const xo = { wires: [], components: [
    { id: 'VIN', type: 'battery', value: 0, a: 'src', b: 'gnd' },
    { id: 'CX', type: 'capacitor', value: 22e-6, a: 'src', b: 'tweet' },
    { id: 'RTWEET', type: 'resistor', value: 8, a: 'tweet', b: 'gnd' },
  ] };
  const v100 = acNode(xo, 100, 'tweet').mag;
  const v5k = acNode(xo, 5000, 'tweet').mag;
  ok('tweeter-crossover-rejects-bass', v100 < 0.20, `100Hz=${v100}`);
  ok('tweeter-crossover-passes-highs', v5k > 0.90, `5kHz=${v5k}`);
}

// 10) Envelope follower used by compressors/synths. A pulse through a diode
// must charge the detector quickly, then the capacitor must decay through its
// release resistor after the input drops.
{
  const env = { wires: [], components: [
    { id: 'VIN', type: 'pulse', a: 'src', b: 'gnd', v1: 0, v2: 5,
      delay: 0, rise: 1e-6, width: 0.005, fall: 1e-6, period: 0.05 },
    { id: 'RATTACK', type: 'resistor', value: 100, a: 'src', b: 'rect' },
    { id: 'DRECT', type: 'diode', a: 'rect', b: 'env' },
    { id: 'CENV', type: 'capacitor', value: 1e-6, a: 'env', b: 'gnd' },
    { id: 'RREL', type: 'resistor', value: 10000, a: 'env', b: 'gnd' },
  ] };
  const tr = transientAnalysis(env, {
    uic: true,
    dt: 5e-5,
    steps: 300,
    probes: [{ type: 'voltage', node: 'env', name: 'Venv' }],
  });
  const vals = tr.rows.map((r) => r.values.Venv);
  const peak = Math.max(...vals.slice(0, 130));
  const tail = vals[vals.length - 1];
  ok('envelope-detector-attacks', peak > 3.5, `peak=${peak}`);
  ok('envelope-detector-releases-after-note', tail < peak * 0.55 && tail > 0.05,
    `peak=${peak} tail=${tail}`);
  ok('envelope-transient-remains-converged', tr.rows.every((r) => r.converged),
    `rows=${tr.rows.length}`);
}

// 11) Pedal/amp supply ripple filtering. A 100 ohm / 100 uF RC feed with a
// realistic load must attenuate 120 Hz rectifier ripple instead of treating
// supply noise as an abstract label.
{
  const filter = { wires: [], components: [
    { id: 'VIN', type: 'battery', value: 0, a: 'raw', b: 'gnd' },
    { id: 'RISO', type: 'resistor', value: 100, a: 'raw', b: 'clean' },
    { id: 'CDEC', type: 'capacitor', value: 100e-6, a: 'clean', b: 'gnd' },
    { id: 'RLOAD', type: 'resistor', value: 10000, a: 'clean', b: 'gnd' },
  ] };
  const v10 = acNode(filter, 10, 'clean').mag;
  const v120 = acNode(filter, 120, 'clean').mag;
  ok('audio-supply-rc-attenuates-120hz-ripple', v120 < v10 * 0.25,
    `10Hz=${v10} 120Hz=${v120}`);
}

// 12) Balanced line / DI-style differential drive. Equal and opposite line
// drivers through equal source impedances must produce strong differential
// signal while the line's common-mode midpoint stays near reference.
{
  const balanced = { wires: [], components: [
    { id: 'VIN', type: 'battery', value: 0, a: 'in', b: 'gnd' },
    { id: 'EP', type: 'vcvs', a: 'p0', b: 'gnd', controlP: 'in', controlN: 'gnd', gain: 1 },
    { id: 'EN', type: 'vcvs', a: 'n0', b: 'gnd', controlP: 'in', controlN: 'gnd', gain: -1 },
    { id: 'RP', type: 'resistor', value: 100, a: 'p0', b: 'p' },
    { id: 'RN', type: 'resistor', value: 100, a: 'n0', b: 'n' },
    { id: 'RLOAD', type: 'resistor', value: 10000, a: 'p', b: 'n' },
  ] };
  const r = ac(balanced, 1000);
  const row = r.rows[0];
  const vp = row.voltages.get(r.uf.find('p'));
  const vn = row.voltages.get(r.uf.find('n'));
  const diff = phasorMagnitude(csub(vp, vn));
  const common = phasorMagnitude(cscale(cadd(vp, vn), 0.5));
  between('balanced-line-delivers-near-2v-differential', diff, 1.90, 2.00);
  ok('balanced-line-midpoint-stays-near-reference', common < 1e-6, `common=${common}`);
}

// 13) Common-mode interference control. Drive both conductors identically
// through the same source impedance; an ideal symmetric differential load
// must see essentially zero differential signal. This is the reference case
// before adding intentional imbalance and finite-CMRR receiver models later.
{
  const cm = { wires: [], components: [
    { id: 'VCM', type: 'battery', value: 0, a: 'cm', b: 'gnd' },
    { id: 'EP', type: 'vcvs', a: 'p0', b: 'gnd', controlP: 'cm', controlN: 'gnd', gain: 1 },
    { id: 'EN', type: 'vcvs', a: 'n0', b: 'gnd', controlP: 'cm', controlN: 'gnd', gain: 1 },
    { id: 'RP', type: 'resistor', value: 100, a: 'p0', b: 'p' },
    { id: 'RN', type: 'resistor', value: 100, a: 'n0', b: 'n' },
    { id: 'RLOAD', type: 'resistor', value: 10000, a: 'p', b: 'n' },
  ] };
  const r = ac(cm, 60, 'VCM');
  const row = r.rows[0];
  const vp = row.voltages.get(r.uf.find('p'));
  const vn = row.voltages.get(r.uf.find('n'));
  const diff = phasorMagnitude(csub(vp, vn));
  ok('symmetric-balanced-line-rejects-ideal-common-mode-hum', diff < 1e-7, `diff=${diff}`);
}

console.log(`\n=== ALL ${checks} MUSICAL-EQUIPMENT CHECKS PASSED ===`);
