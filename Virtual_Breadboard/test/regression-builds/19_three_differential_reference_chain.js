const { Circuit, Sim, check } = require('./_lib');

// Reference-continuity precursor for BC-DC -> TC-AC -> QC-RC.
//
// D1 is a stable DC differential around CENTER.
// D2 is a sinusoidal out-and-back differential around the SAME CENTER.
// D3 is a second, independently measurable differential around the SAME
// CENTER, 90 degrees from D2. D2+D3 therefore trace a rotating ELECTRICAL
// drive vector in a plane.
//
// This does NOT claim a 3D magnetic field. The VBB still lacks Bx/By/Bz.
function run() {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 10, a: 'plus_rail', b: 'minus_rail' },
    { id: 'vg1', type: 'vgnd', a: 'plus_rail', b: 'minus_rail', out: 'center' },

    // D1 / BC-DC: stable point/state, explicitly referenced to CENTER.
    { id: 'd1_dc', type: 'diffsource', value: 1.0, sourceR: 50, a: 'd1', b: 'center' },

    // D2 / TC-AC: out-and-back path around that same CENTER.
    { id: 'd2_ac', type: 'acsource', value: 1.0, freq: 10, phase: 0, a: 'd2', b: 'center' },

    // D3 / QC-RC electrical precursor: an independently measurable
    // center-referenced differential in quadrature with D2.
    { id: 'd3_quad', type: 'acsource', value: 1.0, freq: 10, phase: 90, a: 'd3', b: 'center' },
  ] };

  const dt = 0.0005;
  const steps = 1200; // 0.6s = six full 10Hz cycles
  const settle = 200;
  const d1Trace = [];
  const d2Trace = [];
  const d3Trace = [];
  const centerErr = [];
  const radiusErr = [];
  let res;

  for (let i = 0; i < steps; i++) {
    res = c.solve(els, dt);
    const center = res.voltages.get('center');
    const plus = res.voltages.get('plus_rail');
    const minus = res.voltages.get('minus_rail');
    const idealCenter = (plus + minus) / 2;
    const d1 = res.voltages.get('d1') - center;
    const d2 = res.voltages.get('d2') - center;
    const d3 = res.voltages.get('d3') - center;
    const t = i * dt;

    if (i >= settle) {
      d1Trace.push({ t, value: d1 });
      d2Trace.push({ t, value: d2 });
      d3Trace.push({ t, value: d3 });
      centerErr.push(Math.abs(center - idealCenter));
      radiusErr.push(Math.abs(Math.hypot(d2, d3) - 1.0));
    }
  }

  const d1Avg = Sim.averageValue(d1Trace);
  const d2Avg = Sim.averageValue(d2Trace);
  const d3Avg = Sim.averageValue(d3Trace);
  const d2Rms = Sim.rmsValue(d2Trace);
  const d3Rms = Sim.rmsValue(d3Trace);
  const phase = Sim.phaseDifferenceDeg(d2Trace, d3Trace);
  const maxCenterErr = Math.max(...centerErr);
  const maxRadiusErr = Math.max(...radiusErr);

  return {
    name: '19_three_differential_reference_chain',
    checks: [
      check(
        'D1-BC-DC-is-reference-resolved',
        1.0,
        d1Avg,
        0.02,
        `D1 average relative to CENTER = ${d1Avg.toFixed(4)}V`,
      ),
      check(
        'D2-TC-AC-is-centered-on-same-reference',
        0.0,
        d2Avg,
        0.02,
        `D2 mean relative to CENTER = ${d2Avg.toFixed(4)}V`,
      ),
      check(
        'D3-QC-RC-precursor-is-centered-on-same-reference',
        0.0,
        d3Avg,
        0.02,
        `D3 mean relative to CENTER = ${d3Avg.toFixed(4)}V`,
      ),
      check(
        'D2-and-D3-have-matched-differential-magnitude',
        true,
        Math.abs(d2Rms - d3Rms) < 0.02,
        null,
        `D2 RMS ${d2Rms.toFixed(4)}V / D3 RMS ${d3Rms.toFixed(4)}V`,
      ),
      check(
        'D2-and-D3-are-quadrature',
        true,
        phase != null && Math.abs(Math.abs(phase) - 90) < 3,
        null,
        `measured D2/D3 phase difference ${phase == null ? 'null' : phase.toFixed(2) + 'deg'}`,
      ),
      check(
        'D2-D3-electrical-vector-rotates-with-near-constant-radius',
        true,
        maxRadiusErr < 0.03,
        null,
        `max |sqrt(D2^2+D3^2)-1V| = ${maxRadiusErr.toFixed(4)}V`,
      ),
      check(
        'one-CENTER-reference-survives-all-three-differentials',
        true,
        maxCenterErr < 0.02,
        null,
        `worst CENTER midpoint error ${maxCenterErr.toFixed(5)}V`,
      ),
    ],
  };
}

module.exports = { run };
