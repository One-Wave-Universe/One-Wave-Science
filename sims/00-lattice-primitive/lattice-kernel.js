/* G-764 numerical control kernel. Numerical coordinates are not physical spacing. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LatticeKernel = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const SAFETY = 0.25, MAX_TRIALS = 4096;
  function finite(value, name, minimum = -Infinity) {
    if (!Number.isFinite(value) || value < minimum) throw new RangeError(name + ' is outside the finite domain');
    return value;
  }
  function parameters(p) {
    finite(p.frequencyHz, 'frequencyHz', Number.MIN_VALUE);
    for (const key of ['coupling', 'damping', 'nonlinearity']) finite(p[key], key, 0);
    const w = finite(2 * Math.PI * p.frequencyHz, 'angular frequency');
    finite(w * w, 'frequency squared');
    return { w, J: p.coupling, gamma: finite(2 * p.damping * w, 'damping rate'), lam: p.nonlinearity };
  }
  function validate(sites) {
    if (!Array.isArray(sites) || !sites.length) throw new RangeError('At least one site is required');
    for (let i = 0; i < sites.length; i++) {
      const s = sites[i];
      finite(s.x, 'displacement'); finite(s.v, 'velocity'); finite(s.phase, 'phase');
      if (!Array.isArray(s.n) || new Set(s.n).size !== s.n.length) throw new RangeError('Invalid neighbor list');
      for (const j of s.n) {
        if (!Number.isInteger(j) || j < 0 || j >= sites.length || j === i || !Array.isArray(sites[j].n) || !sites[j].n.includes(i)) throw new RangeError('Graph must be reciprocal without self edges');
      }
    }
  }
  function stiffness(sites, p) {
    let x2 = 0, degree = 0;
    for (const s of sites) { x2 = Math.max(x2, s.x * s.x); degree = Math.max(degree, s.n.length); }
    return finite(p.w * p.w + 2 * degree * p.J + 3 * p.lam * x2, 'stiffness', 0);
  }
  function measure(sites, p, ring = []) {
    validate(sites); const c = parameters(p);
    let q = 0, a2 = 0, v2 = 0, re = 0, im = 0, energy = 0, circulation = 0;
    sites.forEach((s, i) => {
      q += s.x; a2 += s.x * s.x; v2 += s.v * s.v;
      re += Math.cos(s.phase); im += Math.sin(s.phase);
      energy += .5 * s.v * s.v + .5 * c.w * c.w * s.x * s.x + .25 * c.lam * s.x ** 4;
      s.n.forEach(j => { if (j > i) energy += .5 * c.J * (sites[j].x - s.x) ** 2; });
    });
    for (const i of ring) if (!Number.isInteger(i) || !sites[i]) throw new RangeError('Invalid circulation ring');
    for (let k = 0; k < ring.length; k++) {
      const a = sites[ring[k]], b = sites[ring[(k + 1) % ring.length]];
      circulation += a.x * b.v - b.x * a.v;
    }
    const result = { Q: q / sites.length, A_rms: Math.sqrt(a2 / sites.length), V_rms: Math.sqrt(v2 / sites.length), phase_coherence: Math.hypot(re, im) / sites.length, energy, circulation };
    for (const [key, value] of Object.entries(result)) finite(value, key);
    return result;
  }
  function advance(sites, p, dt, forces = [], options = {}) {
    validate(sites); const c = parameters(p); finite(dt, 'dt', 0);
    if (!Array.isArray(forces) || (forces.length !== 0 && forces.length !== sites.length)) throw new RangeError('Force array must match sites');
    for (let i = 0; i < forces.length; i++) finite(forces[i], 'force');
    const limit = options.maxTrials === undefined ? MAX_TRIALS : options.maxTrials;
    if (!Number.isInteger(limit) || limit < 1 || limit > MAX_TRIALS) throw new RangeError('Invalid trial budget');
    let state = sites.map(s => ({ ...s, n: [...s.n] }));
    measure(state, p);
    let remaining = dt, trials = 0, substeps = 0, smallestStep = dt;
    while (remaining > 0) {
      let h = Math.min(remaining, SAFETY / Math.sqrt(stiffness(state, c)), c.gamma ? SAFETY / c.gamma : Infinity);
      let trial;
      while (true) {
        if (++trials > limit || h <= 0 || remaining - h === remaining) throw new RangeError('Numerical work limit reached; reduce timestep or drive');
        trial = state.map((s, i) => {
          const lap = s.n.reduce((a, j) => a + state[j].x - s.x, 0);
          const acc = c.J * lap - c.w * c.w * s.x - c.gamma * s.v - c.lam * s.x ** 3 + (forces.length ? forces[i] : 0);
          const v = finite(s.v + acc * h, 'candidate velocity');
          const x = finite(s.x + v * h, 'candidate displacement');
          return { ...s, x, v, phase: Math.atan2(v / c.w, x) };
        });
        if (h * Math.sqrt(stiffness(trial, c)) <= SAFETY * (1 + 1e-12)) break;
        h /= 2;
      }
      measure(trial, p); // Fail atomically rather than publish nonfinite state/energy.
      state = trial; substeps++; smallestStep = Math.min(smallestStep, h);
      remaining = h === remaining ? 0 : remaining - h;
    }
    return { sites: state, receipt: { integrator: 'symplectic-euler-kick-drift', substeps, trials, requested_dt: dt, smallest_dt: smallestStep, safety_bound: SAFETY, max_trials: limit, drive_policy: 'constant over requested sample interval', physical_lattice_spacing: 'UNDEFINED' } };
  }
  return { advance, measure, parameters, SAFETY, MAX_TRIALS };
});
