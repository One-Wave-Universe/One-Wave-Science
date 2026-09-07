const { Circuit, Sim, check } = require('./_lib');

function run() {
  // Cval stays below js/circuit.js's ELECTROLYTIC_THRESHOLD (1uF) -- a
  // real 1uF+ part is modeled with a real ~20ohm ESR at exactly 1uF, far
  // too lossy for anyone to actually build a resonant tank out of; a real
  // tank uses a ceramic/film cap, which is what 100nF here models.
  const L = 1e-3, Cval = 100e-9, R = 5;
  const f0 = 1 / (2 * Math.PI * Math.sqrt(L * Cval));
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'c1', type: 'capacitor', value: Cval, a: 'a', b: 'b', initialV: 5 },
    { id: 'l1', type: 'inductor', value: L, a: 'b', b: 'c' },
    { id: 'r1', type: 'resistor', value: R, a: 'c', b: 'a' },
  ] };
  const dt = 1 / f0 / 200;
  const capTrace = [];
  let res;
  for (let i = 0; i < 2000; i++) {
    res = c.solve(els, dt);
    capTrace.push({ t: i * dt, value: res.voltages.get('a') - res.voltages.get('b') });
  }
  const per = Sim.findPeriod(capTrace);
  return {
    name: '05_lc_ringdown',
    checks: [
      check('lc-resonant-frequency-matches-analytic', f0, per ? 1 / per.period : 0, f0 * 0.1, `real ringdown frequency must be near f0=1/(2*pi*sqrt(LC))=${f0.toFixed(0)}Hz`),
      check('lc-completes-multiple-real-cycles', true, per != null && per.crossingCount >= 5, null, 'a lightly-damped tank must genuinely ring for multiple cycles, not die out in one'),
    ],
  };
}

module.exports = { run };
