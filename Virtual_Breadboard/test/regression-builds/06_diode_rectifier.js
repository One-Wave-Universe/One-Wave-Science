const { Circuit, Sim, check } = require('./_lib');

function run() {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'ac1', type: 'acsource', value: 5, freq: 60, phase: 0, a: 'src', b: 'g' },
    { id: 'd1', type: 'diode', a: 'src', b: 'out' },
    { id: 'rload', type: 'resistor', value: 1000, a: 'out', b: 'g' },
  ] };
  const dt = 1 / 60 / 200;
  const outTrace = [], inTrace = [];
  let res;
  for (let i = 0; i < 400; i++) { // ~2 full AC cycles
    res = c.solve(els, dt);
    // no battery in this circuit, so the solver may pin 'src' itself as
    // its own implicit zero reference -- always read real differences
    // against the shared return 'g', never a raw absolute voltage
    outTrace.push({ t: i * dt, value: res.voltages.get('out') - res.voltages.get('g') });
    inTrace.push({ t: i * dt, value: res.voltages.get('src') - res.voltages.get('g') });
  }
  const inAvg = Sim.averageValue(inTrace);
  const outAvg = Sim.averageValue(outTrace);
  const outMin = Math.min(...outTrace.map((s) => s.value));
  return {
    name: '06_diode_rectifier',
    checks: [
      check('rectifier-input-symmetric', true, Math.abs(inAvg) < 0.1, null, `the raw AC source must be genuinely symmetric, average was ${inAvg.toFixed(4)}V`),
      check('rectifier-output-real-positive-average', true, outAvg > 1.0, null, `a real half-wave rectifier must produce a positive DC component the input never had, got ${outAvg.toFixed(4)}V`),
      check('rectifier-output-never-goes-hard-negative', true, outMin > -0.5, null, 'the blocked half-cycle must stay blocked, not follow the source down'),
    ],
  };
}

module.exports = { run };
