const { Circuit, check } = require('./_lib');

// V1 integration qualification for the locked three-rail cell topology.
//
// This deliberately proves the electrical pieces one observable at a time:
//   1) + / CENTER / - stays referenced to a buffered center;
//   2) the THREE mirror stations are each one bilateral route, so each is
//      qualified in BOTH directions (3 mirrors x 2 directions = 6 traversals);
//   3) an RC branch stores a center-referenced differential for a finite time
//      and then relaxes when the drive returns to CENTER.
//
// Magnetic retention is NOT faked here. The repo's toroid/memory-core models
// remain separate qualifications because VBB still has no Bx/By/Bz field
// solver. This test is the electrical V1 that a physical breadboard can copy.

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
  return { vp, vc, vm, ideal: (vp + vm) / 2, warnings: res.warnings || [] };
}

// One physical mirror station: two NMOS devices source-to-source so the body
// diodes oppose. The gate drive is referenced to the shared source node.
// This is the same already-qualified bilateral topology used by regression 18,
// instantiated separately as G+, G0 and G- here so the cell's six traversals
// are explicit rather than inferred from a single example.
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
  const vc1 = res.voltages.get('center');
  const charged = res.voltages.get('hold_node') - vc1;

  // Return the command to CENTER. The capacitor must retain the sign briefly
  // instead of collapsing in one ideal timestep.
  drive.value = 0;
  for (let i = 0; i < 5; i++) res = c.solve(els, dt);
  const vc2 = res.voltages.get('center');
  const shortHold = res.voltages.get('hold_node') - vc2;

  // Leave it at CENTER long enough for the ordinary RC path to resolve back.
  for (let i = 0; i < 1200; i++) res = c.solve(els, dt);
  const vc3 = res.voltages.get('center');
  const resolved = res.voltages.get('hold_node') - vc3;

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
