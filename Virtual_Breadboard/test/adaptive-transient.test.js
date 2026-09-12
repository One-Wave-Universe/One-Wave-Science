'use strict';
const assert = require('assert');
const { adaptiveTransientAnalysis } = require('../js/spice-analysis.js');
const { BATTERY_RINT, capacitorESR, capacitorLeakageR } = require('../js/circuit.js');

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

console.log('=== Virtual Breadboard adaptive transient qualification ===');

const Vs = 5;
const R = 1000;
const C = 100e-9;
const cap = { id:'C', type:'capacitor', a:'out', b:'gnd', value:C };
const rc = { wires: [], components: [
  { id:'BAT', type:'battery', a:'src', b:'gnd', value:Vs },
  { id:'R', type:'resistor', a:'src', b:'out', value:R },
  cap,
]};

// Exact continuous-time reference for the simulator's physical RC network:
// source resistance Rs feeds a terminal that has capacitor leakage Rl in
// parallel with (ESR Re + ideal C). The ideal-C state is first order.
function exactRcTerminal(t, vc0=0) {
  const Rs = BATTERY_RINT + R;
  const Re = capacitorESR(cap);
  const Rl = capacitorLeakageR(cap);
  const Gs = 1 / Rs, Ge = 1 / Re, Gl = 1 / Rl;
  const D = Gs + Ge + Gl;
  const vInf = Gs * Vs / (Gs + Gl);
  const tau = C * D / (Ge * (Gs + Gl));
  const vc = vInf + (vc0 - vInf) * Math.exp(-t / tau);
  return (Gs * Vs + Ge * vc) / D;
}

const tStop = 5e-3;
const strict = adaptiveTransientAnalysis(rc, {
  uic:true,
  tStop,
  initialDt:2e-3,
  minDt:2e-7,
  maxDt:2e-3,
  absTol:1e-6,
  relTol:1e-3,
  probes:[{type:'voltage', node:'out', name:'Vout'}],
});

ok('adaptive-mode-reported', strict.analysis.adaptive === true);
ok('step-doubling-method-reported', strict.analysis.method === 'backward-euler-step-doubling');
ok('oversized-starting-step-is-rejected', strict.analysis.rejectedSteps > 0,
  `rejected=${strict.analysis.rejectedSteps}`);
ok('accepted-steps-recorded', strict.analysis.acceptedSteps === strict.rows.length,
  `accepted=${strict.analysis.acceptedSteps} rows=${strict.rows.length}`);
ok('every-accepted-step-meets-local-error-bound', strict.rows.every(r => r.errorNorm <= 1 + 1e-12));
ok('all-accepted-steps-converged', strict.rows.every(r => r.converged));
near('adaptive-run-lands-exactly-on-stop-time', strict.rows[strict.rows.length-1].time, tStop, 1e-15);
ok('controller-shrinks-below-initial-step', Math.min(...strict.rows.map(r=>r.dt)) < 2e-3 / 4,
  `minAcceptedDt=${Math.min(...strict.rows.map(r=>r.dt))}`);
ok('controller-regrows-after-fast-transient', Math.max(...strict.rows.slice(Math.floor(strict.rows.length/2)).map(r=>r.dt)) > Math.min(...strict.rows.map(r=>r.dt)) * 2,
  `min=${Math.min(...strict.rows.map(r=>r.dt))} maxLate=${Math.max(...strict.rows.slice(Math.floor(strict.rows.length/2)).map(r=>r.dt))}`);

const exactFinal = exactRcTerminal(tStop);
const strictFinal = strict.rows[strict.rows.length-1].values.Vout;
near('adaptive-rc-final-value-matches-continuous-time-analytic-reference', strictFinal, exactFinal, 8e-3);

const loose = adaptiveTransientAnalysis(rc, {
  uic:true,
  tStop,
  initialDt:2e-3,
  minDt:2e-7,
  maxDt:2e-3,
  absTol:1e-4,
  relTol:2e-2,
  probes:[{type:'voltage', node:'out', name:'Vout'}],
});
const looseFinal = loose.rows[loose.rows.length-1].values.Vout;
ok('tighter-tolerance-uses-at-least-as-many-accepted-steps', strict.analysis.acceptedSteps >= loose.analysis.acceptedSteps,
  `strict=${strict.analysis.acceptedSteps} loose=${loose.analysis.acceptedSteps}`);
ok('tighter-tolerance-is-closer-to-analytic-reference', Math.abs(strictFinal-exactFinal) <= Math.abs(looseFinal-exactFinal) + 1e-10,
  `strictErr=${Math.abs(strictFinal-exactFinal)} looseErr=${Math.abs(looseFinal-exactFinal)}`);

// State rollback must be deterministic: rejected trial steps may not leak their
// capacitor/thermal/source-clock state into the retry path.
const repeat = adaptiveTransientAnalysis(rc, {
  uic:true, tStop, initialDt:2e-3, minDt:2e-7, maxDt:2e-3,
  absTol:1e-6, relTol:1e-3,
  probes:[{type:'voltage', node:'out', name:'Vout'}],
});
ok('rejected-step-rollback-is-deterministic', repeat.rows.length === strict.rows.length && repeat.rows.every((r,i) =>
  Math.abs(r.time-strict.rows[i].time) < 1e-15 &&
  Math.abs(r.values.Vout-strict.rows[i].values.Vout) < 1e-12),
  `rows=${repeat.rows.length}`);

assert.throws(() => adaptiveTransientAnalysis(rc, {uic:true, tStop:1e-3, initialDt:1e-4, minDt:2e-4}), /bounds/);
checks++; console.log('PASS [invalid-timestep-bounds-fail-loudly]');

console.log(`=== ALL ${checks} ADAPTIVE TRANSIENT CHECKS PASSED ===`);
