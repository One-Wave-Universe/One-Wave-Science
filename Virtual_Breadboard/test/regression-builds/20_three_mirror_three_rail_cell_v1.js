const { Circuit, check } = require('./_lib');

// V1 integration qualification for the locked three-rail cell topology.
// Proves the center reference, three logical bidirectional Mirror gates, and
// a finite center-referenced RC hold/release window. Magnetic retention is
// intentionally NOT claimed here because VBB has no spatial Bx/By/Bz solver.

function centerReference(loadOhms = 1e9) {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'plus_rail', b: 'minus_rail' },
    { id: 'vg1', type: 'vgnd', a: 'plus_rail', b: 'minus_rail', out: 'center' },
    { id: 'rp', type: 'resistor', value: 1000, a: 'plus_rail', b: 'center' },
    { id: 'rm', type: 'resistor', value: 1000, a: 'center', b: 'minus_rail' },
    { id: 'load', type: 'resistor', value: loadOhms, a: 'center', b: 'minus_rail' },
  ] };
  let res;
  for (let i = 0; i < 20; i++) res = c.solve(els, 0.0001);
  const vp = res.voltages.get('plus_rail');
  const vc = res.voltages.get('center');
  const vm = res.voltages.get('minus_rail');
  return { vp, vc, vm, ideal: (vp + vm) / 2 };
}

function mirrorCurrent(station, direction, enabled) {
  const c = new Circuit();
  const forward = direction === 'forward';
  const supply = forward ? 'left_supply' : 'right_supply';
  const driven = forward ? 'left' : 'right';
  const returned = forward ? 'right' : 'left';
  const p = station.replace(/[^A-Za-z0-9]/g, '');
  const els = { wires: [], components: [
    { id: `${p}_bat`, type: 'battery', value: 5, a: supply, b: 'gnd' },
    { id: `${p}_rlim`, type: 'resistor', value: 1000, a: supply, b: driven },
    { id: `${p}_rreturn`, type: 'resistor', value: 0.1, a: returned, b: 'gnd' },
    { id: `${p}_qL`, type: 'nmos', value: 1.5, gate: 'gate', drain: 'left', source: 'common_source' },
    { id: `${p}_qR`, type: 'nmos', value: 1.5, gate: 'gate', drain: 'right', source: 'common_source' },
    { id: `${p}_gdrive`, type: 'battery', value: enabled ? 5 : 0, a: 'gate', b: 'common_source' },
  ] };
  let res;
  for (let i = 0; i < 30; i++) res = c.solve(els, 0.0001);
  return Math.abs(res.currents.get(`${p}_rlim`) || 0);
}

function rcHoldPrecursor() {
  const c = new Circuit();
  const drive = { id: 'drive', type: 'diffsource', value: 0.5, sourceR: 10, a: 'drive_node', b: 'center' };
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'plus_rail', b: 'minus_rail' },
    { id: 'vg1', type: 'vgnd', a: 'plus_rail', b: 'minus_rail', out: 'center' },
    drive,
    { id: 'rphase', type: 'resistor', value: 1000, a: 'drive_node', b: 'hold_node' },
    { id: 'chold', type: 'capacitor', value: 10e-6, a: 'hold_node', b: 'center', initialV: 0 },
    { id: 'rbleed', type: 'resistor', value: 100000, a: 'hold_node', b: 'center' },
  ] };
  let res;
  const dt = 0.0001;
  for (let i = 0; i < 250; i++) res = c.solve(els, dt);
  const charged = res.voltages.get('hold_node') - res.voltages.get('center');
  drive.value = 0;
  for (let i = 0; i < 5; i++) res = c.solve(els, dt);
  const shortHold = res.voltages.get('hold_node') - res.voltages.get('center');
  for (let i = 0; i < 1200; i++) res = c.solve(els, dt);
  const resolved = res.voltages.get('hold_node') - res.voltages.get('center');
  return { charged, shortHold, resolved };
}

function run() {
  const unloaded = centerReference();
  const loaded = centerReference(10000);
  const rc = rcHoldPrecursor();
  const checks = [
    check('cell-v1-center-is-midpoint', true, Math.abs(unloaded.vc - unloaded.ideal) < 0.01, null,
      `CENTER=${unloaded.vc.toFixed(4)}V midpoint=${unloaded.ideal.toFixed(4)}V`),
    check('cell-v1-buffered-center-survives-moderate-one-sided-load', true, Math.abs(loaded.vc - loaded.ideal) < 0.03, null,
      `10k one-sided load leaves CENTER within ${(Math.abs(loaded.vc - loaded.ideal) * 1000).toFixed(2)}mV of midpoint`),
  ];

  for (const station of ['G+', 'G0', 'G-']) {
    const offF = mirrorCurrent(station, 'forward', false);
    const offR = mirrorCurrent(station, 'reverse', false);
    const onF = mirrorCurrent(station, 'forward', true);
    const onR = mirrorCurrent(station, 'reverse', true);
    checks.push(
      check(`${station}-off-blocks-forward`, true, offF < 1e-5, null, `${(offF * 1e6).toFixed(3)}uA`),
      check(`${station}-off-blocks-reverse`, true, offR < 1e-5, null, `${(offR * 1e6).toFixed(3)}uA`),
      check(`${station}-forward-traversal`, true, onF > 0.004, null, `${(onF * 1000).toFixed(3)}mA`),
      check(`${station}-reverse-traversal`, true, onR > 0.004, null, `${(onR * 1000).toFixed(3)}mA`),
      check(`${station}-bidirectional-symmetry`, true, Math.abs(onF - onR) < 5e-5, null,
        `${(onF * 1000).toFixed(3)}mA forward / ${(onR * 1000).toFixed(3)}mA reverse`),
    );
  }

  checks.push(
    check('cell-v1-rc-command-charges-relative-to-center', true, rc.charged > 0.35, null,
      `center-referenced stored differential=${rc.charged.toFixed(4)}V after +0.5V command`),
    check('cell-v1-rc-hold-does-not-collapse-instantly', true, rc.shortHold > 0.25 && rc.shortHold < rc.charged, null,
      `after command returns to CENTER, short hold=${rc.shortHold.toFixed(4)}V from charged=${rc.charged.toFixed(4)}V`),
    check('cell-v1-rc-eventually-resolves-back-to-center', true, Math.abs(rc.resolved) < 0.01, null,
      `after long release, residual=${rc.resolved.toFixed(5)}V`),
  );
  return { name: '20_three_mirror_three_rail_cell_v1', checks };
}

module.exports = { run };
