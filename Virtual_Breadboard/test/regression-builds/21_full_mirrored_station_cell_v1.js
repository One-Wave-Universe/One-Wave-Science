const { Circuit, check } = require('./_lib');

// Physical-shape qualification for CELL_V1.
//
// COUNT BOUNDARY:
//   3 logical Mirror gates: G+, G0, G-
//   each logical station has an upper bilateral leg and a lower bilateral leg
//   each bilateral leg uses 2 source-to-source NMOS devices
//   => 12 MOSFET devices in this explicit bench model, but still only 3
//      logical Mirror gates. Hardware device count does not redefine gate count.
//
// Each station has ONE local midpoint. The upper bilateral leg arrives from
// PLUS, the lower bilateral leg leaves toward MINUS, and the local midpoint
// is tied to the CENTER spine through a small sense resistor. In a symmetric
// hold most current passes PLUS -> station -> MINUS and almost no imbalance
// current enters CENTER. A deliberate arm mismatch creates a measurable center
// receipt while the buffered reference itself must stay stiff.

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
    const upperIn = `${station}_upper_in`;
    const lowerOut = `${station}_lower_out`;
    const tap = `${station}_tap`;

    components.push(
      { id: `${station}_ru`, type: 'resistor', value: upperR, a: 'plus', b: upperIn },
      { id: `${station}_rl`, type: 'resistor', value: 1000, a: lowerOut, b: 'minus' },
      { id: `${station}_rg`, type: 'resistor', value: 10, a: tap, b: 'center' },
    );
    addBilateralPair(components, `${station}_upper`, upperIn, tap, enabled);
    addBilateralPair(components, `${station}_lower`, tap, lowerOut, enabled);
  }

  const els = { wires: [], components };
  let res;
  for (let i = 0; i < 50; i++) res = c.solve(els, 0.0001);

  const vp = res.voltages.get('plus');
  const vg = res.voltages.get('center');
  const vn = res.voltages.get('minus');
  const stationCurrents = {};
  let upperTotal = 0;
  let lowerTotal = 0;
  let centerReceiptTotal = 0;

  for (const station of ['gp', 'g0', 'gm']) {
    const upper = Math.abs(res.currents.get(`${station}_ru`) || 0);
    const lower = Math.abs(res.currents.get(`${station}_rl`) || 0);
    const centerReceipt = res.currents.get(`${station}_rg`) || 0;
    const tapV = res.voltages.get(`${station}_tap`);
    stationCurrents[station] = { upper, lower, centerReceipt, tapV };
    upperTotal += upper;
    lowerTotal += lower;
    centerReceiptTotal += centerReceipt;
  }

  return {
    vp, vg, vn,
    ideal: (vp + vn) / 2,
    stationCurrents,
    upperTotal,
    lowerTotal,
    centerReceiptTotal,
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
    check('full-cell-balanced-center-receipt-near-zero', true, Math.abs(balanced.centerReceiptTotal) < 5e-5, null,
      `net I_G receipt=${(balanced.centerReceiptTotal * 1e6).toFixed(2)}uA`),
  );

  for (const [station, s] of Object.entries(balanced.stationCurrents)) {
    checks.push(
      check(`${station}-mirrored-upper-lower-current-match`, true, Math.abs(s.upper - s.lower) < 5e-5, null,
        `upper=${(s.upper * 1000).toFixed(3)}mA lower=${(s.lower * 1000).toFixed(3)}mA`),
      check(`${station}-tap-sits-near-center-in-hold`, true, Math.abs(s.tapV - balanced.vg) < 0.002, null,
        `tap-center=${((s.tapV - balanced.vg) * 1000).toFixed(3)}mV`),
    );
  }

  const leanG0 = lean.stationCurrents.g0;
  checks.push(
    check('full-cell-g0-resistor-lean-creates-center-receipt', true, Math.abs(leanG0.centerReceipt) > 5e-4, null,
      `G0 I_G receipt=${(leanG0.centerReceipt * 1000).toFixed(3)}mA`),
    check('full-cell-g0-lean-moves-local-tap-from-center', true, Math.abs(leanG0.tapV - lean.vg) > 0.005, null,
      `G0 tap-center=${((leanG0.tapV - lean.vg) * 1000).toFixed(3)}mV`),
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
