const { Circuit, Sim, check } = require('./_lib');

function run() {
  const R = 1000, C = 1e-6;
  const fc = 1 / (2 * Math.PI * R * C);
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'ac1', type: 'acsource', value: 5, freq: fc, a: 'src', b: 'g' },
    { id: 'r1', type: 'resistor', value: R, a: 'src', b: 'out' },
    { id: 'c1', type: 'capacitor', value: C, a: 'out', b: 'g' },
  ] };
  const dt = 1 / fc / 200;
  const steps = Math.round(20 / fc / dt);
  const inTrace = [], outTrace = [];
  let res;
  for (let i = 0; i < steps; i++) {
    res = c.solve(els, dt);
    if (i > steps * 0.5) {
      inTrace.push({ t: i * dt, value: res.voltages.get('src') - res.voltages.get('g') });
      outTrace.push({ t: i * dt, value: res.voltages.get('out') - res.voltages.get('g') });
    }
  }
  const ratio = Sim.rmsValue(outTrace) / Sim.rmsValue(inTrace);
  const phaseDeg = Sim.phaseDifferenceDeg(inTrace, outTrace);
  return {
    name: '03_rc_lowpass_filter',
    checks: [
      check('lowpass-attenuation-at-corner', 1 / Math.SQRT2, ratio, 0.05, `at fc=${fc.toFixed(1)}Hz a real RC low-pass attenuates to ~0.707 of input`),
      check('lowpass-phase-lag-at-corner', 45, phaseDeg, 5, 'a real RC low-pass shows ~45deg phase lag at its own corner frequency'),
    ],
  };
}

module.exports = { run };
