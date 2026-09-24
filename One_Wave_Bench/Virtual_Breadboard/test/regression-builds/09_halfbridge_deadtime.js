const { Circuit, check } = require('./_lib');

// a real discrete half-bridge: PMOS high-side + NMOS low-side sharing one
// output node, each gate driven INDEPENDENTLY -- unlike the abstracted
// hbridge component (which never allows overlap by construction), this
// can genuinely be driven into shoot-through if both gates are commanded
// on at once.
function halfBridge(gateHighV, gateLowV) {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'vcc', b: 'gnd' },
    { id: 'gh', type: 'diffsource', value: gateHighV, sourceR: 10, a: 'gh', b: 'gnd' },
    { id: 'gl', type: 'diffsource', value: gateLowV, sourceR: 10, a: 'gl', b: 'gnd' },
    { id: 'qh', type: 'pmos', value: 1.5, gate: 'gh', drain: 'out', source: 'vcc' },
    { id: 'ql', type: 'nmos', value: 1.5, gate: 'gl', drain: 'out', source: 'gnd' },
    { id: 'rload', type: 'resistor', value: 1000, a: 'out', b: 'gnd' },
  ] };
  let res;
  for (let i = 0; i < 10; i++) res = c.solve(els, 0.0001);
  return res;
}

function run() {
  const deadTime = halfBridge(5, 0); // both commanded off
  const shootThrough = halfBridge(0, 5); // both commanded on -- a real mistake
  return {
    name: '09_halfbridge_deadtime',
    checks: [
      check('halfbridge-dead-time-no-shootthrough-current', true, Math.abs(deadTime.currents.get('bat1')) < 0.001, null, 'with both switches genuinely off, source current must be negligible'),
      check('halfbridge-shootthrough-detectable', true, Math.abs(shootThrough.currents.get('bat1')) > 1.0, null, 'commanding both switches on at once must produce a real, large, detectable current spike -- exactly what a real dead-time gap exists to prevent'),
    ],
  };
}

module.exports = { run };
