#!/usr/bin/env node
'use strict';

const CircuitEngine = require('../js/circuit.js');

let checks = 0;
function check(name, condition, detail) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`CONTINUOUS MOSFET QUALIFICATION FAILED: ${name}`);
}

console.log('=== Virtual Breadboard continuous MOSFET qualification ===');

const nmos = { id: 'M', type: 'nmos', value: 2.1, gate: 'g', drain: 'd', source: 's' };
const pmos = { id: 'P', type: 'pmos', value: 2.1, gate: 'g', drain: 'd', source: 's' };

check('precision-helper-exported', typeof CircuitEngine.mosfetChannelCurrent === 'function');
check('region-helper-exported', typeof CircuitEngine.mosfetChannelRegion === 'function');
check('cutoff-region', CircuitEngine.mosfetChannelRegion(nmos, 2.0, 5, 0) === 'cutoff');
check('triode-region', CircuitEngine.mosfetChannelRegion(nmos, 4.0, 0.5, 0) === 'triode');
check('saturation-region', CircuitEngine.mosfetChannelRegion(nmos, 4.0, 4.0, 0) === 'saturation');

const iCut = CircuitEngine.mosfetChannelCurrent(nmos, 2.0, 5, 0, 25);
const iTri = CircuitEngine.mosfetChannelCurrent(nmos, 4.0, 0.5, 0, 25);
const iSat = CircuitEngine.mosfetChannelCurrent(nmos, 4.0, 4.0, 0, 25);
check('cutoff-channel-zero', Math.abs(iCut) < 1e-15, `I=${iCut}`);
check('triode-current-positive', iTri > 0, `I=${iTri}`);
check('saturation-current-positive', iSat > 0, `I=${iSat}`);
check('gate-overdrive-increases-current', CircuitEngine.mosfetChannelCurrent(nmos, 4.5, 4, 0, 25) > iSat);

// The square-law branches must meet continuously at Vds = Vgs - Vth.
const vov = 4.0 - Math.abs(CircuitEngine.mosfetSpec(nmos).vth);
const iBelow = CircuitEngine.mosfetChannelCurrent(nmos, 4.0, vov - 1e-6, 0, 25);
const iAbove = CircuitEngine.mosfetChannelCurrent(nmos, 4.0, vov + 1e-6, 0, 25);
check('triode-saturation-boundary-continuous', Math.abs(iAbove - iBelow) < 1e-6,
  `below=${iBelow} above=${iAbove}`);

// Same 2N7000/BS250-class RDS(on)/Vth values should mirror in sign.
const inMirror = CircuitEngine.mosfetChannelCurrent(nmos, 4, 1, 0, 25);
const ipMirror = CircuitEngine.mosfetChannelCurrent(pmos, 1, 4, 5, 25);
check('pmos-current-has-complementary-sign', ipMirror < 0, `Ipmos=${ipMirror}`);
check('nmos-pmos-mirror-magnitude', Math.abs(Math.abs(inMirror) - Math.abs(ipMirror)) < 1e-9,
  `n=${inMirror} p=${ipMirror}`);

// Enhanced channel is bidirectional; body diode remains separate and is not
// needed to obtain reverse channel current when the gate is strongly on.
const reverseChannel = CircuitEngine.mosfetChannelCurrent(nmos, 4, 0, 1, 25);
check('enhanced-channel-is-bidirectional', reverseChannel < 0, `I=${reverseChannel}`);

function solveLowSide(gateV, options) {
  const elements = {
    wires: [],
    components: [
      { id: 'B1', type: 'battery', value: 5, a: 'vdd', b: 'gnd' },
      { id: 'VG', type: 'diffsource', value: gateV, sourceR: 1, a: 'gate', b: 'gnd' },
      { id: 'R1', type: 'resistor', value: 1000, a: 'vdd', b: 'drain' },
      { id: 'M1', type: 'nmos', value: 2.1, gate: 'gate', drain: 'drain', source: 'gnd' },
    ],
  };
  return new CircuitEngine.Circuit().solve(elements, 1e-3, 25, options);
}

const precise = solveLowSide(2.8, { mosfetModel: 'continuous', maxIterations: 80 });
check('continuous-solver-converges', precise.solver && precise.solver.converged === true,
  JSON.stringify(precise.solver));
check('solver-reports-continuous-model', precise.solver.mosfetModel === 'continuous', JSON.stringify(precise.solver));
check('continuous-state-reports-model', precise.mosfetStates.get('M1').model === 'continuous',
  JSON.stringify(precise.mosfetStates.get('M1')));
check('continuous-state-reports-physical-region', ['triode', 'saturation'].includes(precise.mosfetStates.get('M1').channelRegion),
  JSON.stringify(precise.mosfetStates.get('M1')));

const resistorI = precise.currents.get('R1');
const mosfetI = precise.currents.get('M1');
check('solver-kcl-closes-load-vs-mosfet-current', Math.abs(resistorI - mosfetI) < 1e-6,
  `R=${resistorI} M=${mosfetI}`);
check('precision-channel-current-is-nonzero', mosfetI > 1e-5, `I=${mosfetI}`);

const belowThreshold = solveLowSide(1.5, { mosfetModel: 'continuous', maxIterations: 80 });
check('below-threshold-solver-converges', belowThreshold.solver.converged === true, JSON.stringify(belowThreshold.solver));
check('below-threshold-state-cutoff', belowThreshold.mosfetStates.get('M1').channelRegion === 'cutoff',
  JSON.stringify(belowThreshold.mosfetStates.get('M1')));
check('below-threshold-current-only-leakage-scale', Math.abs(belowThreshold.currents.get('M1')) < 1e-6,
  `I=${belowThreshold.currents.get('M1')}`);

const legacy = solveLowSide(2.8);
check('legacy-model-remains-default', legacy.solver.mosfetModel === 'simple', JSON.stringify(legacy.solver));
check('legacy-state-remains-simple', legacy.mosfetStates.get('M1').model === 'simple',
  JSON.stringify(legacy.mosfetStates.get('M1')));

console.log(`\n=== ALL ${checks} CONTINUOUS-MOSFET CHECKS PASSED ===`);
