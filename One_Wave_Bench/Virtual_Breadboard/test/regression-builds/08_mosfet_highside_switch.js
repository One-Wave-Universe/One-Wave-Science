const { Circuit, check } = require('./_lib');

function outV(gateV) {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'vcc', b: 'gnd' },
    { id: 'gsrc', type: 'diffsource', value: gateV, sourceR: 10, a: 'gate', b: 'gnd' },
    { id: 'q1', type: 'pmos', value: 1.5, gate: 'gate', drain: 'out', source: 'vcc' },
    { id: 'rload', type: 'resistor', value: 1000, a: 'out', b: 'gnd' },
  ] };
  let res;
  for (let i = 0; i < 10; i++) res = c.solve(els, 0.0001);
  return res.voltages.get('out');
}

function run() {
  const gateLow = outV(0);
  const gateHigh = outV(5);
  return {
    name: '08_mosfet_highside_switch',
    checks: [
      check('pmos-highside-on-with-gate-low', true, gateLow > 4.9, null, 'a PMOS high-side switch (fixed source at VCC) with gate pulled low must turn on and pull the load near VCC'),
      check('pmos-highside-off-with-gate-high', true, gateHigh < 0.1, null, 'gate at VCC (Vgs=0) must turn the PMOS off, leaving the load pulled to ground through its own resistor'),
    ],
  };
}

module.exports = { run };
