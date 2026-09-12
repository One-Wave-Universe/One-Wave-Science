'use strict';
const assert = require('assert');
const { transientAnalysis } = require('../js/spice-analysis.js');
const { BATTERY_RINT, capacitorESR, capacitorLeakageR, inductorDCR } = require('../js/circuit.js');

let checks = 0;
function ok(name, value, detail='') {
  checks++;
  assert(value, `${name}${detail ? ': ' + detail : ''}`);
  console.log(`PASS [${name}]${detail ? ' -- ' + detail : ''}`);
}
function near(name, actual, expected, tolerance) {
  checks++;
  assert(Number.isFinite(actual), `${name}: actual is not finite (${actual})`);
  assert(Math.abs(actual - expected) <= tolerance,
    `${name}: expected ${expected}, got ${actual}, tol=${tolerance}`);
  console.log(`PASS [${name}] -- expected=${expected} actual=${actual} tolerance=${tolerance}`);
}

console.log('=== Virtual Breadboard transient startup / UIC qualification ===');

const dt = 1e-4;
const C = 1e-6;
const rc = { wires: [], components: [
  { id:'BAT', type:'battery', a:'src', b:'gnd', value:5 },
  { id:'R', type:'resistor', a:'src', b:'out', value:1000 },
  { id:'C', type:'capacitor', a:'out', b:'gnd', value:C },
]};

const rcNormal = transientAnalysis(rc, {
  dt, steps:1,
  probes:[{type:'voltage', node:'out', name:'Vout'}],
});
ok('normal-startup-reports-dc-operating-point', rcNormal.analysis.startup === 'dc-operating-point');
ok('normal-startup-has-operating-point-result', !!rcNormal.startupResult);
ok('normal-startup-op-converged', rcNormal.startupResult.solver.converged);
const opV = rcNormal.startupResult.voltages.get(rcNormal.startupResult.uf.find('out'));
near('normal-startup-first-sample-stays-at-op', rcNormal.rows[0].values.Vout, opV, 2e-5);

const rcUic = transientAnalysis(rc, {
  uic:true, dt, steps:1,
  probes:[{type:'voltage', node:'out', name:'Vout'}],
});
ok('uic-reports-user-initial-conditions', rcUic.analysis.startup === 'user-initial-conditions');
ok('uic-skips-operating-point', rcUic.startupResult === null);
const cap = rc.components.find(c => c.id === 'C');
const zCap = 1 / (1 / (capacitorESR(cap) + dt / C) + 1 / capacitorLeakageR(cap));
const expectedRcFirst = 5 * zCap / (BATTERY_RINT + 1000 + zCap);
near('uic-zero-capacitor-first-step-matches-backward-euler', rcUic.rows[0].values.Vout, expectedRcFirst, 2e-6);
ok('uic-zero-start-differs-from-op-start', rcUic.rows[0].values.Vout < rcNormal.rows[0].values.Vout * 0.2,
  `uic=${rcUic.rows[0].values.Vout} op=${rcNormal.rows[0].values.Vout}`);

const rcDeclared = JSON.parse(JSON.stringify(rc));
rcDeclared.components.find(c => c.id === 'C').initialV = 2;
const declared = transientAnalysis(rcDeclared, {
  uic:true, dt, steps:1,
  probes:[{type:'voltage', node:'out', name:'Vout'}],
});
const gC = 1 / (capacitorESR(cap) + dt / C);
const gLeak = 1 / capacitorLeakageR(cap);
const rSeries = BATTERY_RINT + 1000;
// Nodal BE reference: (5-V)/Rseries = gC*(V-2V) + gLeak*V.
const expectedDeclared = (5 / rSeries + gC * 2) / (1 / rSeries + gC + gLeak);
near('uic-declared-capacitor-voltage-is-honored', declared.rows[0].values.Vout, expectedDeclared, 2e-6);
ok('declared-capacitor-ic-changes-first-sample', declared.rows[0].values.Vout > rcUic.rows[0].values.Vout + 1,
  `declared=${declared.rows[0].values.Vout} zero=${rcUic.rows[0].values.Vout}`);

const L = 10e-3;
const rlZeroSource = { wires: [], components: [
  { id:'BAT0', type:'battery', a:'src', b:'gnd', value:0 },
  { id:'R', type:'resistor', a:'src', b:'n', value:100 },
  { id:'L', type:'inductor', a:'n', b:'gnd', value:L, initialCurrent:0.1 },
]};
const rlDeclared = transientAnalysis(rlZeroSource, {
  uic:true, dt, steps:1,
  probes:[{type:'current', componentId:'L', name:'IL'}],
});
const ldt = L / dt;
const expectedInductorFirst = ldt * 0.1 / (BATTERY_RINT + 100 + inductorDCR(L) + ldt);
near('uic-declared-inductor-current-matches-backward-euler', rlDeclared.rows[0].values.IL, expectedInductorFirst, 2e-7);

const rlNoIc = JSON.parse(JSON.stringify(rlZeroSource));
delete rlNoIc.components.find(c => c.id === 'L').initialCurrent;
const rlZero = transientAnalysis(rlNoIc, {
  uic:true, dt, steps:1,
  probes:[{type:'current', componentId:'L', name:'IL'}],
});
near('uic-omitted-inductor-current-defaults-zero', rlZero.rows[0].values.IL, 0, 1e-12);

const rlPowered = { wires: [], components: [
  { id:'BAT', type:'battery', a:'src', b:'gnd', value:5 },
  { id:'R', type:'resistor', a:'src', b:'n', value:100 },
  { id:'L', type:'inductor', a:'n', b:'gnd', value:L },
]};
const rlNormal = transientAnalysis(rlPowered, {
  dt, steps:1,
  probes:[{type:'current', componentId:'L', name:'IL'}],
});
const expectedRlOp = 5 / (BATTERY_RINT + 100 + inductorDCR(L));
near('normal-startup-inductor-op-current-is-analytic', rlNormal.startupResult.currents.get('L'), expectedRlOp, 2e-9);
near('normal-startup-seeds-inductor-steady-current', rlNormal.rows[0].values.IL, expectedRlOp, 2e-7);

ok('transient-row-time-is-first-dt', rcUic.rows[0].time === dt, `time=${rcUic.rows[0].time}`);
ok('normal-startup-row-converged', rcNormal.rows[0].converged);
ok('uic-startup-row-converged', rcUic.rows[0].converged);

console.log(`=== ALL ${checks} STARTUP/UIC CHECKS PASSED ===`);
