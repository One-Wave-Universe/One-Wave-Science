'use strict';

const { Circuit, check } = require('./_lib');
const Bench = require('../../js/bench-reality.js');

function solve(elements, options = {}) {
  const c = new Circuit();
  let res;
  for (let i = 0; i < (options.steps || 60); i++) {
    res = c.solve(elements, options.dt || 0.0001, 25, options.solverOptions || { mosfetModel: 'continuous', maxIterations: 80 });
  }
  return res;
}

function dualRailCell(upperR = 10000, lowerR = 10000, centerKind = 'solid') {
  const components = [
    { id: 'VPLUS', type: 'battery', value: 12, a: 'p_src', b: 'zero_src', role: 'positive_supply', benchMaxCurrent: 0.02 },
    { id: 'VMINUS', type: 'battery', value: 12, a: 'zero_src', b: 'n_src', role: 'negative_supply', benchMaxCurrent: 0.02 },
    // model lead/contact resistance rather than pretending the breadboard rails are superconductors
    { id: 'RP_LEAD', type: 'resistor', value: 0.10, a: 'p_src', b: 'p_bus' },
    { id: 'RN_LEAD', type: 'resistor', value: 0.10, a: 'n_bus', b: 'n_src' },
    { id: 'RUP', type: 'resistor', value: upperR, a: 'p_bus', b: 'zero_bus' },
    { id: 'RDN', type: 'resistor', value: lowerR, a: 'zero_bus', b: 'n_bus' },
  ];
  if (centerKind === 'solid') {
    components.push({ id: 'I0_SHUNT', type: 'resistor', value: 0.10, a: 'zero_src', b: 'zero_bus', role: 'center_spine' });
  } else if (centerKind === 'capacitor') {
    components.push({ id: 'C_CENTER', type: 'capacitor', value: 10e-6, a: 'zero_src', b: 'zero_bus', role: 'center_spine', initialV: 0 });
  }
  const elements = { wires: [], components };
  const result = solve(elements, { steps: 80 });
  return { elements, result };
}

function mixedCenterTopology() {
  const elements = { wires: [], components: [
    { id: 'VPLUS', type: 'battery', value: 12, a: 'p', b: 'zero', role: 'positive_supply', benchMaxCurrent: 0.02 },
    { id: 'VMINUS', type: 'battery', value: 12, a: 'zero', b: 'n', role: 'negative_supply', benchMaxCurrent: 0.02 },
    { id: 'VG', type: 'vgnd', a: 'p', b: 'n', out: 'zero_helper' },
    { id: 'R0', type: 'resistor', value: 0.1, a: 'zero', b: 'zero_bus', role: 'center_spine' },
    { id: 'RUP', type: 'resistor', value: 10000, a: 'p', b: 'zero_bus' },
    { id: 'RDN', type: 'resistor', value: 10000, a: 'zero_bus', b: 'n' },
  ] };
  return { elements, result: solve(elements) };
}

function highSideNmosFromFiveVoltGpio() {
  // Textbook failure case: 12 V N-MOS high side, gate driven only to 5 V
  // relative to ground. A real source follower cannot raise OUT anywhere
  // near 12 V because VGS collapses as OUT rises.
  const elements = { wires: [], components: [
    { id: 'V12', type: 'battery', value: 12, a: 'v12', b: 'gnd', role: 'main_supply', benchMaxCurrent: 0.02 },
    { id: 'GPIO', type: 'diffsource', value: 5, sourceR: 25, a: 'gate', b: 'gnd' },
    { id: 'QH', type: 'nmos', model: '2N7000', gate: 'gate', drain: 'v12', source: 'out' },
    { id: 'LOAD', type: 'resistor', value: 1000, a: 'out', b: 'gnd' },
  ] };
  const result = solve(elements, { steps: 120, solverOptions: { mosfetModel: 'continuous', maxIterations: 120 } });
  return { elements, result };
}

function cellWithMotorDriver() {
  const elements = { wires: [], components: [
    { id: 'VPLUS', type: 'battery', value: 12, a: 'p', b: 'zero', role: 'positive_supply', benchMaxCurrent: 0.02 },
    { id: 'VMINUS', type: 'battery', value: 12, a: 'zero', b: 'n', role: 'negative_supply', benchMaxCurrent: 0.02 },
    { id: 'I0_SHUNT', type: 'resistor', value: 0.1, a: 'zero', b: 'zero_bus', role: 'center_spine' },
    { id: 'DRV', type: 'hbridge', in1: 'cmd1', in2: 'cmd2', vm: 'p', gnd: 'zero_bus', out1: 'm1', out2: 'm2' },
    { id: 'RLOAD', type: 'resistor', value: 1000, a: 'p', b: 'zero_bus' },
  ] };
  return { elements, result: solve(elements) };
}

function errorCode(audit, code) {
  return audit.errors.some((e) => e.code === code);
}

function run() {
  const checks = [];

  // 1) The exact receipt the bench needs: equal arms => I0 ~ 0; lean one
  // arm => signed I0 appears; swap the lean => sign reverses; zero stays put.
  const balanced = dualRailCell(10000, 10000, 'solid');
  const leanUpper = dualRailCell(6800, 10000, 'solid');
  const leanLower = dualRailCell(10000, 6800, 'solid');
  const auditBalanced = Bench.audit(balanced.elements, balanced.result, {
    requireSolidCenter: true,
    maxCenterResistance: 0.25,
    requireSourceReceipt: true,
    minSourceReceipt: 1e-4,
    cellOnly: true,
  });
  const i0Balanced = balanced.result.currents.get('I0_SHUNT') || 0;
  const i0Upper = leanUpper.result.currents.get('I0_SHUNT') || 0;
  const i0Lower = leanLower.result.currents.get('I0_SHUNT') || 0;
  const zeroWalkUpper = Math.abs((leanUpper.result.voltages.get('zero_bus') || 0) - (leanUpper.result.voltages.get('zero_src') || 0));

  checks.push(
    check('bench-reality-balanced-audit-passes', true, auditBalanced.ok, null, JSON.stringify(auditBalanced.errors)),
    check('bench-reality-equal-10k-i0-near-zero', true, Math.abs(i0Balanced) < 5e-6, null, `I0=${(i0Balanced * 1e6).toFixed(3)}uA`),
    check('bench-reality-lean-produces-i0', true, Math.abs(i0Upper) > 1e-4, null, `I0=${(i0Upper * 1000).toFixed(3)}mA`),
    check('bench-reality-opposite-lean-flips-i0-sign', true, i0Upper * i0Lower < 0, null, `upper=${(i0Upper * 1000).toFixed(3)}mA lower=${(i0Lower * 1000).toFixed(3)}mA`),
    check('bench-reality-solid-zero-does-not-walk', true, zeroWalkUpper < 0.005, null, `zero walk=${(zeroWalkUpper * 1000).toFixed(3)}mV`),
  );

  // 2) A series capacitor can make a symmetric node LOOK centered. The new
  // audit must reject that cosmetic pass because CENTER has no solid DC spine.
  const cutCenter = dualRailCell(10000, 10000, 'capacitor');
  const cutV = Math.abs((cutCenter.result.voltages.get('zero_bus') || 0) - (cutCenter.result.voltages.get('zero_src') || 0));
  const cutAudit = Bench.audit(cutCenter.elements, cutCenter.result, {
    requireSolidCenter: true,
    maxCenterResistance: 0.25,
    requireSourceReceipt: true,
  });
  checks.push(
    check('bench-reality-series-c-center-can-look-deceptively-centered', true, cutV < 0.02, null, `visual center error=${(cutV * 1000).toFixed(3)}mV`),
    check('bench-reality-series-c-center-is-rejected', true, errorCode(cutAudit, 'CENTER_SPINE_SERIES_CAP'), null, JSON.stringify(cutAudit.errors)),
  );

  // 3) Dual +/- supply and a TLE/vgnd are two different physical machines.
  const mixed = mixedCenterTopology();
  const mixedAudit = Bench.audit(mixed.elements, mixed.result, { requireSolidCenter: true, maxCenterResistance: 0.25 });
  checks.push(
    check('bench-reality-dual-supply-plus-vgnd-rejected', true, errorCode(mixedAudit, 'MIXED_CENTER_TOPOLOGY'), null, JSON.stringify(mixedAudit.errors)),
  );

  // 4) Do not let a 5 V GPIO drawing masquerade as a 12 V N-MOS high-side
  // driver. The real solved OUT must stay source-follower-limited, not at 12 V.
  const hs = highSideNmosFromFiveVoltGpio();
  const out = hs.result.voltages.get('out') || 0;
  const v12 = hs.result.voltages.get('v12') || 0;
  const hsAudit = Bench.audit(hs.elements, hs.result, { requireSourceReceipt: true });
  checks.push(
    check('bench-reality-5v-gpio-cannot-drive-12v-nmos-high-side', true, out < 4.0 && out < v12 * 0.5, null, `Vout=${out.toFixed(3)}V Vrail=${v12.toFixed(3)}V`),
    check('bench-reality-active-load-has-nonzero-source-receipt', true, !errorCode(hsAudit, 'IMPOSSIBLE_ZERO_SOURCE_RECEIPT'), null, `I(V12)=${((hs.result.currents.get('V12') || 0) * 1000).toFixed(3)}mA loadPower=${hsAudit.loadPower}`),
  );

  // 5) CELL_V1 qualification is not allowed to silently swallow a motor
  // power stage. The motor driver is a second machine until explicitly tested.
  const motor = cellWithMotorDriver();
  const motorAudit = Bench.audit(motor.elements, motor.result, { requireSolidCenter: true, maxCenterResistance: 0.25, cellOnly: true });
  checks.push(
    check('bench-reality-motor-driver-inside-cell-rejected', true, errorCode(motorAudit, 'MOTOR_DRIVER_INSIDE_CELL'), null, JSON.stringify(motorAudit.errors)),
  );

  return { name: '22_bench_reality_guardrails', checks };
}

module.exports = { run };
