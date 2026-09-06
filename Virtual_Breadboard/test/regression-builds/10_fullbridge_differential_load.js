const { Circuit, check } = require('./_lib');

function run() {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 8, a: 'vm', b: 'gnd' },
    { id: 'in1', type: 'diffsource', value: 5, sourceR: 50, a: 'in1', b: 'gnd' },
    { id: 'in2', type: 'diffsource', value: 0, sourceR: 50, a: 'in2', b: 'gnd' },
    { id: 'hb1', type: 'hbridge', in1: 'in1', in2: 'in2', vm: 'vm', gnd: 'gnd', out1: 'out1', out2: 'out2' },
    { id: 'rload', type: 'resistor', value: 100, a: 'out1', b: 'out2' },
  ] };
  let res;
  for (let i = 0; i < 10; i++) res = c.solve(els, 0.0001);
  const differential = res.voltages.get('out1') - res.voltages.get('out2');
  const commonMode = (res.voltages.get('out1') + res.voltages.get('out2')) / 2;
  return {
    name: '10_fullbridge_differential_load',
    checks: [
      check('fullbridge-load-sees-real-differential', true, Math.abs(differential) > 6, null, `the load between out1/out2 must see most of the real supply as a differential voltage, got ${differential.toFixed(3)}V`),
      check('fullbridge-commonmode-measurable-separately', true, commonMode > 0 && commonMode < 8, null, `common-mode (average of out1/out2) must be independently measurable, got ${commonMode.toFixed(3)}V`),
    ],
  };
}

module.exports = { run };
