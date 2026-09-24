const { Circuit, Sim, check } = require('./_lib');

// L=0.1H (not qualification test #20's 1e-3H) so magnetizing reactance
// genuinely dominates a lightly-loaded secondary's tiny current, letting a
// heavily-loaded secondary's reflected impedance visibly pull the
// primary's own current up -- the real reflected-load mechanism, not
// three isolated outputs that happen to share a core in name only.
function primaryCurrent(loadOnS1) {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'ac1', type: 'acsource', value: 5, freq: 1000, a: 'p1', b: 'gnd' },
    { id: 'r2', type: 'resistor', value: loadOnS1, a: 's1', b: 'gnd' },
    { id: 'r3', type: 'resistor', value: 1e6, a: 's2', b: 'gnd' },
    { id: 'tor1', type: 'toroid', windings: [
      { a: 'p1', b: 'gnd', N: 10, R: 0.5, L: 0.1 },
      { a: 's1', b: 'gnd', N: 10, R: 0.5, L: 0.1 },
      { a: 's2', b: 'gnd', N: 10, R: 0.5, L: 0.1 },
    ], coupling: 0.9 },
  ] };
  const dt = 1 / 1000 / 200;
  let res;
  const pTrace = [];
  for (let i = 0; i < 700; i++) { res = c.solve(els, dt); if (i > 500) pTrace.push({ t: i * dt, value: Math.abs(res.currents.get('tor1:0') || 0) }); }
  return Sim.rmsValue(pTrace);
}

function run() {
  const iLightLoad = primaryCurrent(1e6);
  const iHeavyLoad = primaryCurrent(100);
  return {
    name: '15_three_winding_nerve',
    checks: [
      check('three-winding-secondary-load-reflects-to-primary', true, iHeavyLoad > iLightLoad * 1.5, null, `heavily loading secondary s1 must genuinely raise the primary's own drawn current: light-load ${(iLightLoad * 1000).toFixed(3)}mA vs heavy-load ${(iHeavyLoad * 1000).toFixed(3)}mA`),
    ],
  };
}

module.exports = { run };
