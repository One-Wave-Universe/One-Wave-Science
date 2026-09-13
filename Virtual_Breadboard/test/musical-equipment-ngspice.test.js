#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const assert = require('assert');
const { spawnSync } = require('child_process');
const CE = require('../js/circuit.js');
const Spice = require('../js/spice-analysis.js');
const AC = require('../js/ac-analysis.js');

let checks = 0;
function ok(name, condition, detail = '') {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  assert(condition, `${name}${detail ? ': ' + detail : ''}`);
}
function compare(name, vbb, ng, absTol = 2e-3, relTol = 1e-3) {
  const limit = absTol + relTol * Math.max(Math.abs(vbb), Math.abs(ng));
  ok(name, Number.isFinite(vbb) && Number.isFinite(ng) && Math.abs(vbb - ng) <= limit,
    `vbb=${vbb} ngspice=${ng} delta=${Math.abs(vbb - ng)} limit=${limit}`);
}
function tagFor(name) { return `__VBB_AUDIO_${String(name).toUpperCase()}__`; }
function scalar(log, name) {
  const tag = tagFor(name).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const number = '([+\\-]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)(?:[eE][+\\-]?\\d+)?)';
  const m = log.match(new RegExp(`^\\s*${tag}\\s+${number}\\s*$`, 'mi'));
  if (!m) throw new Error(`ngspice output missing ${name}\n${log}`);
  return Number(m[1]);
}
function emitScalar(name) { return `echo ${tagFor(name)} $&${name}`; }
function runNgspice(body) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'vbb-audio-ng-'));
  const net = path.join(dir, 'case.cir');
  const log = path.join(dir, 'case.log');
  fs.writeFileSync(net, `VBB musical-equipment parity\n${body}`);
  const p = spawnSync('ngspice', ['-b', '-o', log, net], { encoding: 'utf8' });
  const text = fs.existsSync(log) ? fs.readFileSync(log, 'utf8') : `${p.stdout || ''}\n${p.stderr || ''}`;
  fs.rmSync(dir, { recursive: true, force: true });
  if (p.error) throw p.error;
  if (p.status !== 0) throw new Error(`ngspice exited ${p.status}\n${text}`);
  return text;
}
function ngAcScalar(netlist, f, expr, name) {
  const log = runNgspice(`${netlist}\n.control\nac lin 1 ${f} ${f}\nlet ${name}=${expr}\n${emitScalar(name)}\nquit\n.endc\n.end\n`);
  return scalar(log, name);
}
function ngOpScalar(netlist, expr, name) {
  const log = runNgspice(`${netlist}\n.control\nop\nlet ${name}=${expr}\n${emitScalar(name)}\nquit\n.endc\n.end\n`);
  return scalar(log, name);
}
function vbbMag(elements, f, node, sourceId = 'VIN') {
  const r = AC.smallSignalAc(elements, { sourceId, frequencies: [f], magnitude: 1 });
  return AC.phasorMagnitude(r.rows[0].voltages.get(r.uf.find(node)));
}
function pickupElements(toneR = null) {
  const components = [
    { id: 'VIN', type: 'battery', value: 0, a: 'src', b: 'gnd' },
    { id: 'RPU', type: 'resistor', value: 6000, a: 'src', b: 'coil' },
    { id: 'LPU', type: 'inductor', value: 2, a: 'coil', b: 'hot' },
    { id: 'CCABLE', type: 'capacitor', value: 470e-12, a: 'hot', b: 'gnd' },
    { id: 'RIN', type: 'resistor', value: 1e6, a: 'hot', b: 'gnd' },
  ];
  if (toneR != null) {
    components.push({ id: 'RTONE', type: 'resistor', value: toneR, a: 'hot', b: 'tone' });
    components.push({ id: 'CTONE', type: 'capacitor', value: 22e-9, a: 'tone', b: 'gnd' });
  }
  return { wires: [], components };
}
function pickupNetlist(toneR = null) {
  const cable = { type: 'capacitor', value: 470e-12 };
  const tone = { type: 'capacitor', value: 22e-9 };
  const lines = [
    'V1 nsrc 0 AC 1',
    `Rsrc nsrc src ${CE.BATTERY_RINT}`,
    'RPU src coil0 6000',
    `RLPU coil0 coil1 ${CE.inductorDCR(2)}`,
    'LPU coil1 hot 2',
    `RCABLE hot ccap ${CE.capacitorESR(cable)}`,
    'CCABLE ccap 0 470p',
    `RLEAKC hot 0 ${CE.capacitorLeakageR(cable)}`,
    'RIN hot 0 1meg',
  ];
  if (toneR != null) {
    lines.push(`RTONE hot tone ${toneR}`);
    lines.push(`RTESR tone tcap ${CE.capacitorESR(tone)}`);
    lines.push('CTONE tcap 0 22n');
    lines.push(`RLEAKT tone 0 ${CE.capacitorLeakageR(tone)}`);
  }
  for (const n of ['nsrc','src','coil0','coil1','hot','ccap','tone','tcap']) lines.push(`RG_${n} ${n} 0 1g`);
  return lines.join('\n');
}
function clipElements(vin, asymmetric = false) {
  const components = [
    { id: 'VIN', type: 'battery', value: vin, a: 'src', b: 'gnd' },
    { id: 'RDRIVE', type: 'resistor', value: 10000, a: 'src', b: 'out' },
    { id: 'DP', type: 'diode', a: 'out', b: 'gnd' },
  ];
  if (asymmetric) {
    components.push({ id: 'DN1', type: 'diode', a: 'gnd', b: 'nneg' });
    components.push({ id: 'DN2', type: 'diode', a: 'nneg', b: 'out' });
  } else {
    components.push({ id: 'DN', type: 'diode', a: 'gnd', b: 'out' });
  }
  return { wires: [], components };
}
function clipNetlist(vin, asymmetric = false) {
  const lines = [
    `V1 nsrc 0 ${vin}`,
    `Rsrc nsrc src ${CE.BATTERY_RINT}`,
    'RDRIVE src out 10000',
    'DP out 0 DM',
  ];
  if (asymmetric) lines.push('DN1 0 nneg DM', 'DN2 nneg out DM');
  else lines.push('DN 0 out DM');
  lines.push(`.model DM D(IS=${CE.DIODE_IS} N=${CE.DIODE_N})`, '.temp 25', 'RGsrc src 0 1g', 'RGout out 0 1g', 'RGneg nneg 0 1g');
  return lines.join('\n');
}

console.log('=== VBB musical equipment vs ngspice ===');
{
  const ver = spawnSync('ngspice', ['--version'], { encoding: 'utf8' });
  ok('ngspice-installed-for-audio-parity', ver.status === 0, (ver.stdout || ver.stderr || '').split('\n')[0]);
}

// Passive pickup/cable network: compare the whole resonance, not one point.
{
  const elements = pickupElements();
  const net = pickupNetlist();
  for (const f of [100, 1000, 5000, 10000]) {
    const vbb = vbbMag(elements, f, 'hot');
    const ng = ngAcScalar(net, f, 'mag(v(hot))', `pickup_${f}`);
    compare(`pickup-cable-${f}Hz`, vbb, ng, 2e-3, 1e-3);
  }
}

// Tone-down network parity at low and high frequency.
{
  const elements = pickupElements(10000);
  const net = pickupNetlist(10000);
  for (const f of [200, 5000]) {
    compare(`tone-down-${f}Hz`, vbbMag(elements, f, 'hot'),
      ngAcScalar(net, f, 'mag(v(hot))', `tone_${f}`), 2e-3, 1e-3);
  }
}

// Symmetric and asymmetric pedal clipping transfer points.
for (const asymmetric of [false, true]) {
  for (const vin of [3, -3]) {
    const vbbResult = Spice.operatingPoint(clipElements(vin, asymmetric),
      { solverOptions: { diodeModel: 'newton', maxIterations: 120 } });
    const vbb = vbbResult.voltages.get('out');
    const ng = ngOpScalar(clipNetlist(vin, asymmetric), 'v(out)',
      `${asymmetric ? 'asym' : 'sym'}_${vin > 0 ? 'p' : 'n'}`);
    compare(`${asymmetric ? 'asymmetric' : 'symmetric'}-clip-${vin > 0 ? 'positive' : 'negative'}`,
      vbb, ng, 4e-3, 1e-3);
  }
}

// Speaker voice-coil current at bass and treble frequencies.
{
  const L = 1e-3;
  const elements = { wires: [], components: [
    { id: 'VIN', type: 'battery', value: 0, a: 'src', b: 'gnd' },
    { id: 'RSRC', type: 'resistor', value: 10, a: 'src', b: 'drive' },
    { id: 'RVC', type: 'resistor', value: 8, a: 'drive', b: 'coil' },
    { id: 'LVC', type: 'inductor', value: L, a: 'coil', b: 'gnd' },
  ] };
  const net = `V1 nsrc 0 AC 1\nRbat nsrc src ${CE.BATTERY_RINT}\nRSRC src drive 10\nRVC drive l0 8\nRL l0 l1 ${CE.inductorDCR(L)}\nLVC l1 0 ${L}\nRG1 src 0 1g\nRG2 drive 0 1g\nRG3 l0 0 1g\nRG4 l1 0 1g`;
  for (const f of [100, 10000]) {
    const r = AC.smallSignalAc(elements, { sourceId: 'VIN', frequencies: [f], magnitude: 1 });
    const row = r.rows[0];
    const vs = row.voltages.get(r.uf.find('src'));
    const vd = row.voltages.get(r.uf.find('drive'));
    const vbb = AC.phasorMagnitude({ re: (vs.re - vd.re) / 10, im: (vs.im - vd.im) / 10 });
    const ng = ngAcScalar(net, f, 'mag((v(src)-v(drive))/10)', `speaker_${f}`);
    compare(`speaker-current-${f}Hz`, vbb, ng, 2e-5, 1e-3);
  }
}

// First-order tweeter crossover including the exact VBB capacitor ESR/leakage.
{
  const cap = { id: 'CX', type: 'capacitor', value: 22e-6, a: 'src', b: 'tweet' };
  const elements = { wires: [], components: [
    { id: 'VIN', type: 'battery', value: 0, a: 'src', b: 'gnd' }, cap,
    { id: 'RT', type: 'resistor', value: 8, a: 'tweet', b: 'gnd' },
  ] };
  const net = `V1 nsrc 0 AC 1\nRbat nsrc src ${CE.BATTERY_RINT}\nRESR src cx ${CE.capacitorESR(cap)}\nCX cx 0 22u\nRLEAK src 0 ${CE.capacitorLeakageR(cap)}\nRT tweet 0 8\nW1 cx tweet 0\nRG1 src 0 1g\nRG2 cx 0 1g\nRG3 tweet 0 1g`;
  // ngspice has no W element for an ideal wire; use a 1 micro-ohm resistor.
  const ngNet = net.replace('W1 cx tweet 0', 'RWIRE cx tweet 1u');
  for (const f of [100, 5000]) {
    compare(`tweeter-crossover-${f}Hz`, vbbMag(elements, f, 'tweet'),
      ngAcScalar(ngNet, f, 'mag(v(tweet))', `xo_${f}`), 3e-3, 1e-3);
  }
}

// Balanced line differential amplitude.
{
  const elements = { wires: [], components: [
    { id: 'VIN', type: 'battery', value: 0, a: 'in', b: 'gnd' },
    { id: 'EP', type: 'vcvs', a: 'p0', b: 'gnd', controlP: 'in', controlN: 'gnd', gain: 1 },
    { id: 'EN', type: 'vcvs', a: 'n0', b: 'gnd', controlP: 'in', controlN: 'gnd', gain: -1 },
    { id: 'RP', type: 'resistor', value: 100, a: 'p0', b: 'p' },
    { id: 'RN', type: 'resistor', value: 100, a: 'n0', b: 'n' },
    { id: 'RL', type: 'resistor', value: 10000, a: 'p', b: 'n' },
  ] };
  const r = AC.smallSignalAc(elements, { sourceId: 'VIN', frequencies: [1000], magnitude: 1 });
  const row = r.rows[0];
  const vp = row.voltages.get(r.uf.find('p'));
  const vn = row.voltages.get(r.uf.find('n'));
  const vbb = AC.phasorMagnitude({ re: vp.re - vn.re, im: vp.im - vn.im });
  const net = `V1 nsrc 0 AC 1\nRbat nsrc in ${CE.BATTERY_RINT}\nEP p0 0 in 0 1\nEN n0 0 in 0 -1\nRP p0 p 100\nRN n0 n 100\nRL p n 10000\nRG1 in 0 1g\nRG2 p0 0 1g\nRG3 n0 0 1g\nRG4 p 0 1g\nRG5 n 0 1g`;
  const ng = ngAcScalar(net, 1000, 'mag(v(p,n))', 'balanced_diff');
  compare('balanced-line-differential-1kHz', vbb, ng, 2e-4, 1e-3);
}

console.log(`\n=== ALL ${checks} MUSICAL NGSPICE PARITY CHECKS PASSED ===`);
