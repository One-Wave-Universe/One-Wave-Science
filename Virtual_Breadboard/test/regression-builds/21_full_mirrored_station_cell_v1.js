const { Circuit, check } = require('./_lib');

// Physical-shape qualification for CELL_V1.
//
// IMPORTANT COUNT BOUNDARY:
//   3 logical Mirror gates: G+, G0, G-
//   each logical station has an upper bilateral leg and a lower bilateral leg
//   each bilateral leg uses 2 source-to-source NMOS devices
//   => 12 MOSFET devices in this explicit bench model, but still only 3
//      logical Mirror gates. Hardware device count must not redefine gate count.
//
// The two legs are mirrored around CENTER. In balance, current delivered from
// PLUS into CENTER through the upper leg is matched by current leaving CENTER
// toward MINUS through the lower leg. Imbalance is the observable; CENTER must
// remain a reference rather than becoming the load return that wanders.

function addBilateralPair(components, id, left, right, enabled) {
  const source = `${id}_source`;
  const gate = `${id}_gate`;
  components.push(
    { id: `${id}_q1`, type: 'nmos', value: 1.5, gate, drain: left, source },
    { id: `${id}_q2`, type: 'nmos', value: 1.5, gate, drain: right, source },
    { id: `${id}_drive`, type: 'battery', value: enabled ? 5 : 0, a: gate, b: source },
  );
}

function solveCell({ enabled = true, leanStation = null } = {}) {
  const c = new Circuit();
  const components = [
    { id: 'supply', type: 'battery', value: 5, a: 'plus', b: 'minus' },
    { id: 'vg', type: 'vgnd', a: 'plus', b: 'minus', out: 'center' },
  ];

  for (const station of ['gp', 'g0', 'gm']) {
    const upperR = station === leanStation ? 680 : 1000;
    const lowerR = 1000;
    const upperIn = `${station}_upper_in`;
    const lowerOut = `${station}_lower_out`;

    components.push(
      { id: `${station}_ru`, type: 'resistor', value: upperR, a: 'plus', b: upperIn },
      { id: `${station}_rl`, type: 'resistor', value: lowerR, a: lowerOut, b: 'minus' },
    );
    addBilateralPair(components, `${station}_upper`, upperIn, 'center', enabled);
    addBilateralPair(components, `${station}_lower`, 'center', lowerOut, enabled);
  }

  const els = { wires: [], components };
  let res;
  for (let i = 0; i < 40; i++) res = c.solve(els, 0.0001);

  const vp = res.voltages.get('plus');
  const vg = res.voltages.get('center');
  const vn = res.voltages.get('minus');
  const stationCurrents = {};
  let upperTotal = 0;
  let lowerTotal = 0;
  for (const station of ['gp', 'g0', 'gm']) {
    const upper = Math.abs(res.currents.get(`${station}_ru`) || 0);
    const lower = Math.abs(res.currents.get(`${station}_rl`) || 0);
    stationCurrents[station] = { upper, lower, delta: upper - lower };
    upperTotal += upper;
    lowerTotal += lower;
  }

  return {
    vp, vg, vn,
    ideal: (vp + vn) / 2,
    stationCurrents,
    upperTotal,
    lowerTotal,
    imbalance: upperTotal - lowerTotal,
    warnings: res.warnings || [],
  };
}

function run() {
  const off = solveCell({ enabled: false });
  const balanced = solveCell({ enabled: true });
  const lean = solveCell({ enabled: true, leanStation: 'g0' });
  const checks = [];

  checks.push(
    check('full-cell-off-upper-paths-leakage-only', true, off.upperTotal < 3e-5, null,
      `upper total OFF=${(off.upperTotal * 1e6).toFixed(3)}uA`),
    check('full-cell-off-lower-paths-leakage-only', true, off.lowerTotal < 3e-5, null,
      `lower total OFF=${(off.lowerTotal * 1e6).toFixed(3)}uA`),
    check('full-cell-balanced-center-stays-midpoint', true, Math.abs(balanced.vg - balanced.ideal) < 0.002, null,
      `CENTER=${balanced.vg.toFixed(5)}V midpoint=${balanced.ideal.toFixed(5)}V`),
    check('full-cell-balanced-net-center-current-cancels', true, Math.abs(balanced.imbalance) < 5e-5, null,
      `upper=${(balanced.upperTotal * 1000).toFixed(3)}mA lower=${(balanced.lowerTotal * 1000).toFixed(3)}mA delta=${(balanced.imbalance * 1e6).toFixed(2)}uA`),
  );

  for (const [station, currents] of Object.entries(balanced.stationCurrents)) {
    checks.push(
      check(`${station}-mirrored-upper-lower-current-match`, true, Math.abs(currents.delta) < 5e-5, null,
        `upper=${(currents.upper * 1000).toFixed(3)}mA lower=${(currents.lower * 1000).toFixed(3)}mA`),
    );
  }

  checks.push(
    check('full-cell-g0-resistor-lean-creates-measurable-differential', true, Math.abs(lean.imbalance) > 5e-4, null,
      `lean imbalance=${(lean.imbalance * 1000).toFixed(3)}mA`),
    check('full-cell-center-remains-reference-during-lean', true, Math.abs(lean.vg - lean.ideal) < 0.005, null,
      `lean CENTER error=${(Math.abs(lean.vg - lean.ideal) * 1000).toFixed(3)}mV`),
    check('full-cell-no-solver-warning-balanced', true, balanced.warnings.length === 0, null,
      balanced.warnings.join('; ') || 'none'),
    check('full-cell-no-solver-warning-lean', true, lean.warnings.length === 0, null,
      lean.warnings.join('; ') || 'none'),
  );

  return { name: '21_full_mirrored_station_cell_v1', checks };
}

module.exports = { run };
