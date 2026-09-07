const { Circuit, Sim, check } = require('./_lib');

function secondaryRatio(turns2) {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'ac1', type: 'acsource', value: 5, freq: 1000, a: 'p1', b: 'gnd' },
    { id: 'rload', type: 'resistor', value: 1e6, a: 's1', b: 'gnd' }, // near-open secondary
    { id: 'tor1', type: 'toroid', windings: [{ a: 'p1', b: 'gnd', N: 10, R: 0.5, L: 1e-3 }, { a: 's1', b: 'gnd', N: turns2, R: 0.5, L: 1e-3 * (turns2 / 10) * (turns2 / 10) }], coupling: 0.97 },
  ] };
  const dt = 1 / 1000 / 200;
  let res;
  const p1Trace = [], s1Trace = [];
  for (let i = 0; i < 1000; i++) {
    res = c.solve(els, dt);
    if (i > 500) {
      p1Trace.push({ t: i * dt, value: res.voltages.get('p1') - res.voltages.get('gnd') });
      s1Trace.push({ t: i * dt, value: res.voltages.get('s1') - res.voltages.get('gnd') });
    }
  }
  return Sim.rmsValue(s1Trace) / Sim.rmsValue(p1Trace);
}

function run() {
  const ratio2to1 = secondaryRatio(20);
  return {
    name: '14_transformer_turns_ratio',
    checks: [
      check('transformer-turns-ratio-approximately-real', 2.0, ratio2to1, 0.3, `a 20:10 turns toroid with a near-open secondary must show output/input near the real 2:1 turns ratio, got ${ratio2to1.toFixed(3)}`),
    ],
  };
}

module.exports = { run };
