const { Circuit, Sim, check } = require('./_lib');

function relaxationFreq(rVal, cVal) {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'vcc', b: 'gnd' },
    { id: 'sg1', type: 'schmitt', in: 'fb', out: 'out', vcc: 'vcc', gnd: 'gnd' },
    { id: 'rfb', type: 'resistor', value: rVal, a: 'out', b: 'fb' },
    { id: 'cfb', type: 'capacitor', value: cVal, a: 'fb', b: 'gnd' },
  ] };
  const dt = rVal * cVal / 200;
  const trace = [];
  let res;
  for (let i = 0; i < 4000; i++) { res = c.solve(els, dt); trace.push({ t: i * dt, value: res.voltages.get('out') }); }
  const per = Sim.findPeriod(trace, { threshold: 2.5 });
  return per ? 1 / per.period : null;
}

function run() {
  const R1 = 10000, C1 = 1e-8;
  const f1 = relaxationFreq(R1, C1);
  const f2 = relaxationFreq(R1 * 2, C1);
  const f3 = relaxationFreq(R1, C1 * 2);
  return {
    name: '13_relaxation_oscillator',
    checks: [
      check('oscillator-real-nonzero-frequency', true, f1 != null && f1 > 0, null, `an RC-fed Schmitt gate must genuinely oscillate, got ${f1}Hz`),
      check('oscillator-frequency-changes-with-r', true, f2 < f1 * 0.7, null, `doubling R must genuinely drop frequency (${f1.toFixed(1)}Hz -> ${f2.toFixed(1)}Hz)`),
      check('oscillator-frequency-changes-with-c', true, f3 < f1 * 0.7, null, `doubling C must genuinely drop frequency (${f1.toFixed(1)}Hz -> ${f3.toFixed(1)}Hz)`),
    ],
  };
}

module.exports = { run };
