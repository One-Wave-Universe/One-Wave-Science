'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const CE = require('../js/circuit.js');
const Spice = require('../js/spice-analysis.js');
const AC = require('../js/ac-analysis.js');
const tolerances = require('./ngspice-tolerances.json');

let checks = 0;
function check(name, condition, detail) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`NGSPICE CROSS-CHECK FAILED: ${name}`);
}
function within(a, b, tol) {
  const limit = (tol.abs || 0) + (tol.rel || 0) * Math.max(Math.abs(a), Math.abs(b));
  return { pass: Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) <= limit, delta: Math.abs(a - b), limit };
}
function compare(name, a, b, tol) {
  const c = within(a, b, tol);
  check(name, c.pass, `vbb=${a} ngspice=${b} delta=${c.delta} limit=${c.limit}`);
}
function tagFor(name) { return `__VBB_SCALAR_${String(name).toUpperCase()}__`; }
function scalar(log, name) {
  const tag = tagFor(name).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const number = '([+\\-]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)(?:[eE][+\\-]?\\d+)?)';
  const m = log.match(new RegExp(`^\\s*${tag}\\s+${number}\\s*$`, 'mi'));
  if (m) return Number(m[1]);
  throw new Error(`ngspice output did not contain tagged scalar ${name}\n${log}`);
}
function emitScalar(name) { return `echo ${tagFor(name)} $&${name}`; }
function runNgspice(body) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'vbb-ngspice-'));
  const net = path.join(dir, 'case.cir');
  const log = path.join(dir, 'case.log');
  fs.writeFileSync(net, body);
  const p = spawnSync('ngspice', ['-b', '-o', log, net], { encoding: 'utf8' });
  const text = fs.existsSync(log) ? fs.readFileSync(log, 'utf8') : `${p.stdout || ''}\n${p.stderr || ''}`;
  fs.rmSync(dir, { recursive: true, force: true });
  if (p.error) throw p.error;
  if (p.status !== 0) throw new Error(`ngspice exited ${p.status}\n${text}`);
  return text;
}
function opScalar(netlist, expr, name) {
  const log = runNgspice(`${netlist}\n.control\nop\nlet ${name}=${expr}\n${emitScalar(name)}\nquit\n.endc\n.end\n`);
  return scalar(log, name);
}

console.log('=== Virtual Breadboard ngspice cross-check qualification ===');
{
  const version = spawnSync('ngspice', ['--version'], { encoding: 'utf8' });
  check('ngspice-installed', version.status === 0, (version.stdout || version.stderr || '').split('\n')[0]);
}

const divider = {
  wires: [],
  components: [
    { id: 'B1', type: 'battery', value: 5, a: 'vin', b: 'gnd' },
    { id: 'R1', type: 'resistor', value: 999, a: 'vin', b: 'out' },
    { id: 'R2', type: 'resistor', value: 1000, a: 'out', b: 'gnd' },
  ],
};
{
  const vbb = Spice.operatingPoint(divider).voltages.get('out');
  const ng = opScalar('V1 nsrc 0 5\nRsrc nsrc vin 1\nR1 vin out 999\nR2 out 0 1000\nRg1 nsrc 0 1g\nRg2 vin 0 1g\nRg3 out 0 1g', 'v(out)', 'vout');
  compare('op-resistor-divider', vbb, ng, tolerances.operatingPoint.resistorDivider);
}

{
  const sweep = Spice.dcSweep(divider, {
    sourceId: 'B1', start: 0, stop: 5, step: 1,
    probes: [{ type: 'voltage', node: 'out', name: 'vout' }],
    dt: 0,
  });
  for (const row of sweep.rows) {
    const ng = opScalar(`V1 nsrc 0 ${row.sourceValue}\nRsrc nsrc vin 1\nR1 vin out 999\nR2 out 0 1000\nRg1 nsrc 0 1g\nRg2 vin 0 1g\nRg3 out 0 1g`, 'v(out)', 'vout');
    compare(`dc-sweep-${row.sourceValue}V`, row.values.vout, ng, tolerances.dcSweep.resistorDivider);
  }
}

{
  const Cval = 1e-6;
  const cap = { id: 'C1', type: 'capacitor', value: Cval, a: 'out', b: 'gnd' };
  const esr = CE.capacitorESR(cap);
  const rleak = CE.capacitorLeakageR(cap);
  const f = 1 / (2 * Math.PI * 1000 * Cval);
  const elements = {
    wires: [],
    components: [
      { id: 'V1', type: 'acsource', value: 0, a: 'vin', b: 'gnd' },
      { id: 'R1', type: 'resistor', value: 999, a: 'vin', b: 'out' }, cap,
    ],
  };
  const vbb = AC.smallSignalAc(elements, { sourceId: 'V1', frequencies: [f], magnitude: 1, phaseDeg: 0 });
  const z = vbb.rows[0].voltages.get(vbb.uf.find('out'));
  const mag = AC.phasorMagnitude(z);
  const phase = AC.phasorPhaseDeg(z);
  const log = runNgspice(`V1 nsrc 0 AC 1\nRsrc nsrc vin 1\nR1 vin out 999\nResr out cnode ${esr}\nC1 cnode 0 ${Cval}\nRleak out 0 ${rleak}\nRg1 nsrc 0 1g\nRg2 vin 0 1g\nRg3 out 0 1g\n.control\nac lin 1 ${f} ${f}\nlet vmag=mag(v(out))\nlet vphase=ph(v(out))\n${emitScalar('vmag')}\n${emitScalar('vphase')}\nquit\n.endc\n.end\n`);
  compare('ac-rc-magnitude', mag, scalar(log, 'vmag'), tolerances.ac.rcMagnitude);
  compare('ac-rc-phase', phase, scalar(log, 'vphase'), tolerances.ac.rcPhaseDeg);
}

{
  const Cval = 1e-6;
  const cap = { id: 'C1', type: 'capacitor', value: Cval, a: 'out', b: 'gnd', initialV: 0 };
  const esr = CE.capacitorESR(cap);
  const rleak = CE.capacitorLeakageR(cap);
  const dt = 1e-4, steps = 10, tStop = dt * steps;
  const elements = {
    wires: [],
    components: [
      { id: 'B1', type: 'battery', value: 5, a: 'vin', b: 'gnd' },
      { id: 'R1', type: 'resistor', value: 999, a: 'vin', b: 'out' }, cap,
    ],
  };
  const tran = Spice.transientAnalysis(elements, {
    dt, steps, uic: true, probes: [{ type: 'voltage', node: 'out', name: 'vout' }],
    solverOptions: { integrationMethod: 'backward-euler' },
  });
  const vbb = tran.rows[tran.rows.length - 1].values.vout;
  const log = runNgspice(`V1 nsrc 0 5\nRsrc nsrc vin 1\nR1 vin out 999\nResr out cnode ${esr}\nC1 cnode 0 ${Cval} IC=0\nRleak out 0 ${rleak}\nRg1 nsrc 0 1g\nRg2 vin 0 1g\nRg3 out 0 1g\n.options method=gear maxord=1\n.control\ntran ${dt} ${tStop} uic\nmeas tran vend FIND v(out) AT=${tStop}\n${emitScalar('vend')}\nquit\n.endc\n.end\n`);
  compare('tran-rc-backward-euler', vbb, scalar(log, 'vend'), tolerances.transient.rcBackwardEuler);
}

{
  const elements = {
    wires: [],
    components: [
      { id: 'B1', type: 'battery', value: 2, a: 'vin', b: 'gnd' },
      { id: 'R1', type: 'resistor', value: 1000, a: 'vin', b: 'd' },
      { id: 'D1', type: 'diode', a: 'd', b: 'gnd' },
    ],
  };
  const vbb = Spice.operatingPoint(elements, { solverOptions: { diodeModel: 'newton' } }).voltages.get('d');
  const ng = opScalar('V1 nsrc 0 2\nRsrc nsrc vin 1\nR1 vin d 1000\nD1 d 0 DM\n.model DM D(IS=1e-12 N=1.8)\nRg1 nsrc 0 1g\nRg2 vin 0 1g\nRg3 d 0 1g\n.temp 25', 'v(d)', 'vd');
  compare('op-continuous-diode', vbb, ng, tolerances.operatingPoint.continuousDiode);
}

check('coverage-mosfet-explicitly-scoped', /not claimed/i.test(tolerances.coverage.mosfet), tolerances.coverage.mosfet);
check('coverage-bjt-explicitly-scoped', /not claimed/i.test(tolerances.coverage.bjt), tolerances.coverage.bjt);
console.log(`\n=== ALL ${checks} NGSPICE CROSS-CHECKS PASSED ===`);
