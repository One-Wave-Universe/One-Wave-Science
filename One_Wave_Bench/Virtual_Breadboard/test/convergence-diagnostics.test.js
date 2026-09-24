'use strict';
const assert = require('assert');
const Engine = require('../js/circuit.js');
let checks = 0;
function ok(name, condition, detail='') {
  checks++;
  assert(condition, `${name}${detail ? ': '+detail : ''}`);
  console.log(`PASS [${name}]${detail ? ' -- '+detail : ''}`);
}

console.log('=== Virtual Breadboard deterministic convergence diagnostics qualification ===');

const linear = {
  wires: [],
  components: [
    { id:'B1', type:'battery', value:5, a:'vin', b:'gnd' },
    { id:'R1', type:'resistor', value:1234, a:'vin', b:'mid' },
    { id:'R2', type:'resistor', value:2345, a:'mid', b:'gnd' },
  ],
};
const r1 = new Engine.Circuit().solve(linear, 1e-3, 25);
const r2 = new Engine.Circuit().solve(linear, 1e-3, 25);
ok('linear-converges', r1.solver.converged === true, JSON.stringify(r1.solver));
ok('success-has-no-failure-reason', r1.solver.failureReason === null, String(r1.solver.failureReason));
ok('overall-worst-residual-present', r1.solver.worstResidual && Number.isFinite(r1.solver.worstResidual.residual), JSON.stringify(r1.solver.worstResidual));
ok('worst-node-residual-is-node', r1.solver.worstNodeResidual && r1.solver.worstNodeResidual.kind === 'node', JSON.stringify(r1.solver.worstNodeResidual));
ok('worst-branch-residual-is-branch', r1.solver.worstBranchResidual && r1.solver.worstBranchResidual.kind === 'branch', JSON.stringify(r1.solver.worstBranchResidual));
ok('branch-row-identifies-source', r1.solver.worstBranchResidual.id === 'B1', JSON.stringify(r1.solver.worstBranchResidual));
ok('max-residual-agrees-with-worst-object', r1.solver.maxResidual === r1.solver.worstResidual.residual,
  `max=${r1.solver.maxResidual} worst=${r1.solver.worstResidual.residual}`);
ok('node-diagnostic-has-row-scale-tolerance', Number.isInteger(r1.solver.worstNodeResidual.row)
  && Number.isFinite(r1.solver.worstNodeResidual.scale)
  && Number.isFinite(r1.solver.worstNodeResidual.tolerance), JSON.stringify(r1.solver.worstNodeResidual));
ok('branch-diagnostic-has-row-scale-tolerance', Number.isInteger(r1.solver.worstBranchResidual.row)
  && Number.isFinite(r1.solver.worstBranchResidual.scale)
  && Number.isFinite(r1.solver.worstBranchResidual.tolerance), JSON.stringify(r1.solver.worstBranchResidual));
const keyDiag = (r) => JSON.stringify({
  worst:r.solver.worstResidual,
  node:r.solver.worstNodeResidual,
  branch:r.solver.worstBranchResidual,
  reason:r.solver.failureReason,
});
ok('diagnostics-repeat-deterministically', keyDiag(r1) === keyDiag(r2), `${keyDiag(r1)} vs ${keyDiag(r2)}`);

const nonlinear = {
  wires: [],
  components: [
    { id:'B1', type:'battery', value:2, a:'vin', b:'gnd' },
    { id:'R1', type:'resistor', value:1000, a:'vin', b:'d' },
    { id:'D1', type:'diode', a:'d', b:'gnd' },
  ],
};
const fail = new Engine.Circuit().solve(nonlinear, 1e-3, 25, { maxIterations:1 });
ok('forced-nonlinear-case-fails', fail.solver.converged === false, JSON.stringify(fail.solver));
ok('failure-reason-is-explicit-iteration-state-code', fail.solver.failureReason === 'ITERATION_LIMIT_STATE_UNSTABLE', fail.solver.failureReason);
ok('failure-still-reports-worst-equation', !!fail.solver.worstResidual && !!fail.solver.worstNodeResidual && !!fail.solver.worstBranchResidual,
  JSON.stringify(fail.solver));
ok('warning-carries-reason-code', fail.warnings.some(w => w.includes('reason=ITERATION_LIMIT_STATE_UNSTABLE')), fail.warnings.join(' | '));
ok('warning-carries-equation-identity', fail.warnings.some(w => /(?:node|branch):.+ row=\d+ residual=/.test(w)), fail.warnings.join(' | '));

console.log(`=== ALL ${checks} CONVERGENCE-DIAGNOSTIC CHECKS PASSED ===`);
