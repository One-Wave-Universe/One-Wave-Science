from pathlib import Path
p=Path('Virtual_Breadboard/js/spice-analysis.js')
s=p.read_text()

anchor="\nmodule.exports = { operatingPoint, steppedOperatingPoint, dcSweep, transientAnalysis, sweepValues };\n"
if anchor not in s:
    raise SystemExit('export anchor missing')

insert=r'''

function cloneStateValue(value) {
  if (value instanceof Map) {
    const out = new Map();
    for (const [k, v] of value.entries()) out.set(k, cloneStateValue(v));
    return out;
  }
  if (Array.isArray(value)) return value.map(cloneStateValue);
  if (value && typeof value === 'object') return JSON.parse(JSON.stringify(value));
  return value;
}

function snapshotCircuitState(circuit) {
  const snap = {};
  for (const key of Object.keys(circuit)) snap[key] = cloneStateValue(circuit[key]);
  return snap;
}

function restoreCircuitState(circuit, snap) {
  for (const key of Object.keys(circuit)) {
    if (!(key in snap)) delete circuit[key];
  }
  for (const [key, value] of Object.entries(snap)) circuit[key] = cloneStateValue(value);
}

function normalizedTransientError(fullResult, halfResult, absTol, relTol) {
  let worst = 0;
  let worstKind = null;
  let worstId = null;
  const check = (kind, fullMap, halfMap) => {
    const keys = new Set([...fullMap.keys(), ...halfMap.keys()]);
    for (const key of keys) {
      const a = fullMap.get(key);
      const b = halfMap.get(key);
      if (!Number.isFinite(a) || !Number.isFinite(b)) continue;
      const scale = absTol + relTol * Math.max(Math.abs(a), Math.abs(b));
      const norm = scale > 0 ? Math.abs(a - b) / scale : Math.abs(a - b);
      if (norm > worst) { worst = norm; worstKind = kind; worstId = key; }
    }
  };
  check('voltage', fullResult.voltages, halfResult.voltages);
  check('current', fullResult.currents, halfResult.currents);
  return { norm: worst, kind: worstKind, id: worstId };
}

/**
 * Adaptive transient analysis using backward-Euler step doubling.
 *
 * One full step of h is compared against two half steps from the exact same
 * saved circuit state. Their difference is the local-error estimate. A step
 * is accepted only when both paths converge and the normalized voltage/current
 * error is <= 1. The two-half-step state is retained as the accepted answer;
 * rejected trials restore the circuit state before retrying with a smaller h.
 */
function adaptiveTransientAnalysis(elements, options) {
  options = options || {};
  const tStop = finiteNumber('tStop', options.tStop);
  if (!(tStop > 0)) throw new RangeError('tStop must be > 0');
  const initialDt = options.initialDt == null ? Math.min(1e-4, tStop) : finiteNumber('initialDt', options.initialDt);
  const minDt = options.minDt == null ? Math.max(1e-12, initialDt / 1024) : finiteNumber('minDt', options.minDt);
  const maxDt = options.maxDt == null ? Math.max(initialDt, tStop / 10) : finiteNumber('maxDt', options.maxDt);
  if (!(initialDt > 0) || !(minDt > 0) || !(maxDt >= minDt)) throw new RangeError('adaptive timestep bounds must satisfy initialDt>0, minDt>0, maxDt>=minDt');
  const absTol = options.absTol == null ? 1e-6 : finiteNumber('absTol', options.absTol);
  const relTol = options.relTol == null ? 1e-3 : finiteNumber('relTol', options.relTol);
  if (absTol < 0 || relTol < 0) throw new RangeError('absTol and relTol must be >= 0');
  const safety = options.safety == null ? 0.9 : finiteNumber('safety', options.safety);
  if (!(safety > 0 && safety <= 1)) throw new RangeError('safety must be in (0,1]');
  const maxAcceptedSteps = options.maxAcceptedSteps == null ? 100000 : Math.trunc(options.maxAcceptedSteps);
  const maxRejectedSteps = options.maxRejectedSteps == null ? 100000 : Math.trunc(options.maxRejectedSteps);
  const ambientC = options.ambientC;
  if (ambientC != null) finiteNumber('ambientC', ambientC);
  const probes = normalizeProbes(options.probes);
  const uic = !!options.uic;
  const work = cloneElements(elements);
  let startupResult = null;

  if (!uic) {
    const startupOptions = { ambientC, solverOptions: options.solverOptions };
    startupResult = options.continuation
      ? steppedOperatingPoint(work, Object.assign({}, startupOptions, {
          sourceScales: options.sourceScales,
          gminSteps: options.gminSteps,
          targetGmin: options.targetGmin,
        }))
      : operatingPoint(work, startupOptions);
    if (!startupResult.solver || !startupResult.solver.converged) throw new Error('adaptive transient startup operating point did not converge');
    for (const c of work.components || []) {
      if (c.type === 'capacitor') {
        const va = startupResult.voltages.get(startupResult.uf.find(c.a)) || 0;
        const vb = startupResult.voltages.get(startupResult.uf.find(c.b)) || 0;
        c.initialV = va - vb;
      } else if (c.type === 'inductor') c.initialCurrent = startupResult.currents.get(c.id) || 0;
    }
  }

  const circuit = new Circuit();
  const rows = [];
  const rejected = [];
  let acceptedSteps = 0;
  let rejectedSteps = 0;
  let t = 0;
  let h = Math.min(initialDt, maxDt, tStop);
  let finalResult = null;

  while (t < tStop) {
    if (acceptedSteps >= maxAcceptedSteps) throw new Error(`adaptive transient exceeded maxAcceptedSteps=${maxAcceptedSteps}`);
    if (rejectedSteps >= maxRejectedSteps) throw new Error(`adaptive transient exceeded maxRejectedSteps=${maxRejectedSteps}`);
    h = Math.min(h, maxDt, tStop - t);
    if (h < minDt && tStop - t > minDt * 1e-9) h = Math.min(minDt, tStop - t);

    const base = snapshotCircuitState(circuit);
    restoreCircuitState(circuit, base);
    const full = circuit.solve(work, h, ambientC, options.solverOptions);
    restoreCircuitState(circuit, base);
    const half1 = circuit.solve(work, h / 2, ambientC, options.solverOptions);
    const half2 = circuit.solve(work, h / 2, ambientC, options.solverOptions);
    const estimate = normalizedTransientError(full, half2, absTol, relTol);
    const converged = !!(full.solver && full.solver.converged && half1.solver && half1.solver.converged && half2.solver && half2.solver.converged);
    const accept = converged && estimate.norm <= 1;

    if (accept) {
      t += h;
      acceptedSteps += 1;
      finalResult = half2;
      const values = {};
      for (const probe of probes) {
        let value = null;
        if (probe.type === 'voltage') {
          const root = half2.uf.find(probe.node);
          const raw = half2.voltages.get(root);
          value = raw == null ? null : raw;
        } else {
          const raw = half2.currents.get(probe.componentId);
          value = raw == null ? null : raw;
        }
        values[probe.name] = value;
      }
      rows.push({ time: t, dt: h, errorNorm: estimate.norm, errorKind: estimate.kind, errorId: estimate.id, values, warnings: Array.from(half2.warnings || []), converged: true });
      const growth = estimate.norm <= 1e-16 ? 2 : Math.min(2, Math.max(0.5, safety * Math.pow(1 / estimate.norm, 0.5)));
      h = Math.min(maxDt, Math.max(minDt, h * growth));
    } else {
      restoreCircuitState(circuit, base);
      rejectedSteps += 1;
      rejected.push({ time: t, attemptedDt: h, errorNorm: estimate.norm, errorKind: estimate.kind, errorId: estimate.id, converged });
      if (h <= minDt * (1 + 1e-12)) {
        throw new Error(`adaptive transient could not satisfy local-error target at minDt=${minDt} (errorNorm=${estimate.norm}, converged=${converged})`);
      }
      const shrink = !converged || !Number.isFinite(estimate.norm) || estimate.norm <= 0
        ? 0.5
        : Math.max(0.1, Math.min(0.5, safety * Math.pow(1 / estimate.norm, 0.5)));
      h = Math.max(minDt, h * shrink);
    }
  }

  return {
    analysis: {
      type: 'tran', adaptive: true, method: 'backward-euler-step-doubling', tStop,
      initialDt, minDt, maxDt, absTol, relTol, safety, acceptedSteps, rejectedSteps,
      uic, startup: uic ? 'user-initial-conditions' : 'dc-operating-point',
    },
    probes, rows, rejected, startupResult, finalResult,
  };
}
'''

s=s.replace(anchor, insert + "\nmodule.exports = { operatingPoint, steppedOperatingPoint, dcSweep, transientAnalysis, adaptiveTransientAnalysis, normalizedTransientError, snapshotCircuitState, restoreCircuitState, sweepValues };\n", 1)
p.write_text(s)
