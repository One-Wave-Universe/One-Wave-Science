'use strict';

const { Circuit, check } = require('./_lib');

// Stress the physical dual-rail reference, not a cosmetic midpoint.
// Sweep equal and deliberately unequal arm loads over more than two orders
// of magnitude, then mirror every unequal case. The solver must preserve:
//   1) near-zero center-spine current when the two arms really match,
//   2) equal/opposite center current when the load imbalance is mirrored,
//   3) mirrored rail voltages around the same physical zero reference,
//   4) monotonic center-current magnitude as imbalance increases,
//   5) a stable center node instead of silently letting the reference walk.

function solveCell(upperR, lowerR) {
  const c = new Circuit();
  const elements = {
    wires: [],
    components: [
      { id: 'VPLUS', type: 'battery', value: 12, a: 'p_src', b: 'zero_src' },
      { id: 'VMINUS', type: 'battery', value: 12, a: 'zero_src', b: 'n_src' },
      { id: 'RP_LEAD', type: 'resistor', value: 0.10, a: 'p_src', b: 'p_bus' },
      { id: 'RN_LEAD', type: 'resistor', value: 0.10, a: 'n_bus', b: 'n_src' },
      { id: 'CENTER_SPINE', type: 'resistor', value: 0.10, a: 'zero_src', b: 'zero_bus' },
      { id: 'RUP', type: 'resistor', value: upperR, a: 'p_bus', b: 'zero_bus' },
      { id: 'RDN', type: 'resistor', value: lowerR, a: 'zero_bus', b: 'n_bus' },
    ],
  };

  let result;
  for (let i = 0; i < 80; i++) {
    result = c.solve(elements, 0.0001, 25, { maxIterations: 80 });
  }

  const zero = result.voltages.get('zero_bus');
  return {
    result,
    i0: result.currents.get('CENTER_SPINE') || 0,
    centerWalk: (result.voltages.get('zero_bus') || 0) - (result.voltages.get('zero_src') || 0),
    plus: (result.voltages.get('p_bus') || 0) - zero,
    minus: (result.voltages.get('n_bus') || 0) - zero,
  };
}

function maxAbs(values) {
  return Math.max(...values.map((v) => Math.abs(v)));
}

function run() {
  const checks = [];

  // Equal-load sweep: 220 ohm through 100 kohm. A real center spine should
  // carry almost no net current when the two halves are genuinely matched,
  // even though total rail current changes by hundreds of times.
  const equalRs = [220, 470, 1000, 2200, 4700, 10000, 47000, 100000];
  const equal = equalRs.map((r) => ({ r, s: solveCell(r, r) }));
  const equalMaxI0 = maxAbs(equal.map((x) => x.s.i0));
  const equalMaxCenterWalk = maxAbs(equal.map((x) => x.s.centerWalk));
  const equalMaxRailMirrorError = maxAbs(equal.map((x) => x.s.plus + x.s.minus));

  checks.push(
    check(
      'balanced-reference-equal-load-sweep-keeps-i0-near-zero',
      true,
      equalMaxI0 < 2e-5,
      null,
      `loads=${equalRs.join(',')}ohm worst |I0|=${(equalMaxI0 * 1e6).toFixed(3)}uA`,
    ),
    check(
      'balanced-reference-equal-load-sweep-keeps-center-fixed',
      true,
      equalMaxCenterWalk < 2e-5,
      null,
      `worst center walk=${(equalMaxCenterWalk * 1e6).toFixed(3)}uV`,
    ),
    check(
      'balanced-reference-equal-load-sweep-keeps-rails-mirrored',
      true,
      equalMaxRailMirrorError < 0.01,
      null,
      `worst |Vplus+Vminus| around zero=${equalMaxRailMirrorError.toFixed(6)}V`,
    ),
    check(
      'balanced-reference-equal-load-sweep-all-solves-converge',
      true,
      equal.every((x) => x.s.result.solver && x.s.result.solver.converged === true),
      null,
      equal.map((x) => `${x.r}:${x.s.result.solver && x.s.result.solver.converged}`).join(' '),
    ),
  );

  // Mirror a fixed 10k arm against progressively heavier opposite arms.
  // No absolute sign is assumed: whichever sign the engine uses, swapping
  // upper/lower must reverse it and preserve magnitude/voltage symmetry.
  const mismatchRs = [6800, 4700, 2200, 1000, 470, 220];
  const mirrored = mismatchRs.map((r) => ({
    r,
    upperHeavy: solveCell(r, 10000),
    lowerHeavy: solveCell(10000, r),
  }));

  const allFlip = mirrored.every((x) => x.upperHeavy.i0 * x.lowerHeavy.i0 < 0);
  const worstCurrentMirrorError = maxAbs(mirrored.map((x) => x.upperHeavy.i0 + x.lowerHeavy.i0));
  const worstPlusMirrorError = maxAbs(mirrored.map((x) => x.upperHeavy.plus + x.lowerHeavy.minus));
  const worstMinusMirrorError = maxAbs(mirrored.map((x) => x.upperHeavy.minus + x.lowerHeavy.plus));
  const worstCenterMagnitudeMirrorError = maxAbs(mirrored.map((x) =>
    Math.abs(x.upperHeavy.centerWalk) - Math.abs(x.lowerHeavy.centerWalk)));
  const worstLoadedCenterWalk = Math.max(...mirrored.flatMap((x) => [
    Math.abs(x.upperHeavy.centerWalk),
    Math.abs(x.lowerHeavy.centerWalk),
  ]));

  checks.push(
    check(
      'balanced-reference-mirrored-loads-flip-center-current-sign',
      true,
      allFlip,
      null,
      mirrored.map((x) => `${x.r}/10k:${(x.upperHeavy.i0 * 1000).toFixed(3)}mA <-> ${(x.lowerHeavy.i0 * 1000).toFixed(3)}mA`).join(' | '),
    ),
    check(
      'balanced-reference-mirrored-loads-match-center-current-magnitude',
      true,
      worstCurrentMirrorError < 2e-5,
      null,
      `worst |I0(a)+I0(mirror)|=${(worstCurrentMirrorError * 1e6).toFixed(3)}uA`,
    ),
    check(
      'balanced-reference-mirrored-loads-swap-rail-voltages',
      true,
      worstPlusMirrorError < 0.02 && worstMinusMirrorError < 0.02,
      null,
      `worst rail mirror errors +/mirror-=${worstPlusMirrorError.toFixed(5)}V -/mirror+=${worstMinusMirrorError.toFixed(5)}V`,
    ),
    check(
      'balanced-reference-mirrored-loads-match-center-walk-magnitude',
      true,
      worstCenterMagnitudeMirrorError < 2e-5,
      null,
      `worst mirrored center-walk magnitude error=${(worstCenterMagnitudeMirrorError * 1e6).toFixed(3)}uV`,
    ),
    check(
      'balanced-reference-center-stays-stiff-under-220ohm-vs-10k-stress',
      true,
      worstLoadedCenterWalk < 0.02,
      null,
      `worst center walk across mismatched sweep=${(worstLoadedCenterWalk * 1000).toFixed(3)}mV`,
    ),
    check(
      'balanced-reference-mismatched-sweep-all-solves-converge',
      true,
      mirrored.every((x) =>
        x.upperHeavy.result.solver && x.upperHeavy.result.solver.converged === true &&
        x.lowerHeavy.result.solver && x.lowerHeavy.result.solver.converged === true),
      null,
      'all mirrored stress cases report solver.converged=true',
    ),
  );

  // As one arm gets progressively heavier (lower R), the reference spine
  // must carry progressively more imbalance current. This catches a solver
  // that gets the sign right but stops responding quantitatively to load.
  const magnitudes = mirrored.map((x) => Math.abs(x.upperHeavy.i0));
  const monotonic = magnitudes.every((v, i) => i === 0 || v > magnitudes[i - 1]);
  checks.push(
    check(
      'balanced-reference-lean-current-grows-monotonically-with-imbalance',
      true,
      monotonic,
      null,
      mismatchRs.map((r, i) => `${r}/10k=${(magnitudes[i] * 1000).toFixed(3)}mA`).join(' | '),
    ),
  );

  return { name: '24_balanced_reference_sweep_stress', checks };
}

module.exports = { run };
