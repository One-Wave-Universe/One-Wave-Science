const { Circuit, CircuitEngine, check } = require('./_lib');

function run() {
  const SG = CircuitEngine.SCHMITT_SPEC;
  const vPlus = 5 * SG.vtPlusFrac, vMinus = 5 * SG.vtMinusFrac;

  // approach the midpoint (2.5V) from BELOW
  const c1 = new Circuit();
  const midEls = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'vcc', b: 'gnd' },
    { id: 'vsrc', type: 'diffsource', value: 0, sourceR: 10, a: 'in', b: 'gnd' },
    { id: 'sg1', type: 'schmitt', in: 'in', out: 'out', vcc: 'vcc', gnd: 'gnd' },
  ] };
  let res;
  for (const v of [0, 1.0, 1.8, 2.5]) {
    midEls.components[1].value = v;
    for (let i = 0; i < 3; i++) res = c1.solve(midEls, 0.0001);
  }
  const outFromBelow = res.voltages.get('out');

  // approach the SAME midpoint from ABOVE
  const c2 = new Circuit();
  const midEls2 = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'vcc', b: 'gnd' },
    { id: 'vsrc', type: 'diffsource', value: 5, sourceR: 10, a: 'in', b: 'gnd' },
    { id: 'sg1', type: 'schmitt', in: 'in', out: 'out', vcc: 'vcc', gnd: 'gnd' },
  ] };
  for (const v of [5, 4.0, 3.2, 2.5]) {
    midEls2.components[1].value = v;
    for (let i = 0; i < 3; i++) res = c2.solve(midEls2, 0.0001);
  }
  const outFromAbove = res.voltages.get('out');

  return {
    name: '12_schmitt_hysteresis',
    checks: [
      check('schmitt-upper-lower-thresholds-distinct', true, vPlus !== vMinus, null, `separate upper (${vPlus}V) and lower (${vMinus}V) thresholds, not one shared one`),
      check('schmitt-no-chatter-holds-state-in-deadband', true, outFromBelow !== outFromAbove, null, `at the same 2.5V input, output must differ depending on history (${outFromBelow.toFixed(2)}V from below vs ${outFromAbove.toFixed(2)}V from above)`),
    ],
  };
}

module.exports = { run };
