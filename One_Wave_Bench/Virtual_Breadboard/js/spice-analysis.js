'use strict';

/*
 * SPICE-style analysis helpers for the Virtual Breadboard solver.
 *
 * This deliberately sits beside Circuit.solve() instead of refactoring the
 * load-bearing MNA core. Analysis modes transform only what SPICE itself
 * treats differently from transient simulation, then hand the resulting
 * circuit to the same generic electrical solver.
 */

const CircuitEngine = require('./circuit.js');
const { Circuit, inductorDCR } = CircuitEngine;

function cloneElements(elements) {
  return JSON.parse(JSON.stringify(elements || { wires: [], components: [] }));
}

function finiteNumber(name, value) {
  if (!Number.isFinite(value)) throw new TypeError(`${name} must be a finite number`);
  return value;
}

function sweepValues(start, stop, step) {
  finiteNumber('start', start);
  finiteNumber('stop', stop);
  finiteNumber('step', step);
  if (step === 0) throw new RangeError('step must not be zero');
  const direction = stop >= start ? 1 : -1;
  if (Math.sign(step) !== direction) {
    throw new RangeError(`step sign must move from start (${start}) toward stop (${stop})`);
  }

  const out = [];
  const eps = Math.max(1, Math.abs(start), Math.abs(stop)) * 1e-12;
  const maxPoints = 100000;
  for (let k = 0; k < maxPoints; k++) {
    const value = start + k * step;
    if (direction > 0 ? value > stop + eps : value < stop - eps) break;
    out.push(Math.abs(value - stop) <= eps ? stop : value);
  }
  if (!out.length) out.push(start);
  if (out.length >= maxPoints) throw new RangeError(`DC sweep exceeds ${maxPoints} points`);
  return out;
}

function normalizeProbes(probes) {
  return (probes || []).map((probe, index) => {
    if (!probe || typeof probe !== 'object') throw new TypeError(`probe ${index} must be an object`);
    if (probe.type === 'voltage') {
      if (probe.node == null) throw new TypeError(`voltage probe ${index} requires node`);
      return { type: 'voltage', node: probe.node, name: probe.name || `V(${probe.node})` };
    }
    if (probe.type === 'current') {
      if (!probe.componentId) throw new TypeError(`current probe ${index} requires componentId`);
      return { type: 'current', componentId: probe.componentId, name: probe.name || `I(${probe.componentId})` };
    }
    throw new TypeError(`probe ${index} type must be 'voltage' or 'current'`);
  });
}

function sampleProbes(result, probes) {
  const values = {};
  for (const probe of probes) {
    const value = probe.type === 'voltage'
      ? result.voltages.get(probe.node)
      : result.currents.get(probe.componentId);
    values[probe.name] = value == null ? null : value;
  }
  return values;
}

function dcEquivalent(elements) {
  const original = cloneElements(elements);
  const dcElements = cloneElements(elements);
  const capacitorIds = [];

  dcElements.components = (dcElements.components || []).flatMap((component) => {
    if (component.type === 'capacitor') {
      capacitorIds.push(component.id);
      return [];
    }
    if (component.type === 'inductor') {
      return [{
        id: component.id,
        label: component.label,
        type: 'resistor',
        a: component.a,
        b: component.b,
        value: inductorDCR(component.value),
      }];
    }
    return [component];
  });

  return { original, dcElements, capacitorIds };
}

function restoreDcMeasurements(result, capacitorIds) {
  for (const id of capacitorIds) result.currents.set(id, 0);
  return result;
}

function operatingPoint(elements, options) {
  options = options || {};
  const ambientC = options.ambientC;
  if (ambientC != null) finiteNumber('ambientC', ambientC);

  const { original, dcElements, capacitorIds } = dcEquivalent(elements);
  const circuit = new Circuit();
  const result = circuit.solve(dcElements, 0, ambientC, options.solverOptions);
  restoreDcMeasurements(result, capacitorIds);

  result.analysis = {
    type: 'op',
    historyIndependent: true,
    capacitorRule: 'open-circuit',
    inductorRule: 'winding-dcr',
    continuation: false,
  };
  result.originalElements = original;
  result.dcElements = dcElements;
  return result;
}

function normalizeSourceScales(values) {
  const out = values == null ? [0, 0.25, 0.5, 0.75, 1] : Array.from(values);
  if (!out.length) throw new RangeError('sourceScales must contain at least one value');
  out.forEach((v, i) => {
    finiteNumber(`sourceScales[${i}]`, v);
    if (v < 0 || v > 1) throw new RangeError('sourceScales values must be between 0 and 1');
  });
  if (out[out.length - 1] !== 1) out.push(1);
  return out;
}

function normalizeGminSteps(values, targetGmin) {
  const out = values == null ? [1e-3, 1e-5, 1e-7, targetGmin] : Array.from(values);
  if (!out.length) throw new RangeError('gminSteps must contain at least one value');
  out.forEach((v, i) => {
    finiteNumber(`gminSteps[${i}]`, v);
    if (v < 0) throw new RangeError('gminSteps values must be >= 0');
  });
  if (out[out.length - 1] !== targetGmin) out.push(targetGmin);
  return out;
}

function scaleIndependentDcSources(elements, scale) {
  const scaled = cloneElements(elements);
  for (const component of scaled.components || []) {
    if (component.type === 'battery' || component.type === 'diffsource') {
      component.value = (component.value || 0) * scale;
    }
  }
  return scaled;
}

/**
 * Solve a DC operating point with continuation.
 *
 * Phase 1: source stepping. Independent DC sources are ramped from zero to
 * their requested values while reusing the same Circuit instance, so diode,
 * MOSFET, comparator, clamp, and other fixed-point states from the easier
 * solution seed the next harder one.
 *
 * Phase 2: GMIN stepping. With sources at full value, the artificial shunt
 * conductance is reduced from an intentionally easy value back to the normal
 * target GMIN. The final reported result is always the solve at full source
 * values and target GMIN; intermediate answers are never returned as truth.
 */
function steppedOperatingPoint(elements, options) {
  options = options || {};
  const ambientC = options.ambientC;
  if (ambientC != null) finiteNumber('ambientC', ambientC);
  const targetGmin = options.targetGmin == null ? 1e-9 : finiteNumber('targetGmin', options.targetGmin);
  if (targetGmin < 0) throw new RangeError('targetGmin must be >= 0');
  const sourceScales = normalizeSourceScales(options.sourceScales);
  const gminSteps = normalizeGminSteps(options.gminSteps, targetGmin);
  const baseSolverOptions = Object.assign({}, options.solverOptions || {});
  const { original, dcElements, capacitorIds } = dcEquivalent(elements);
  const circuit = new Circuit();
  const trace = [];
  let result = null;

  const sourcePhaseGmin = gminSteps[0];
  for (const sourceScale of sourceScales) {
    const steppedElements = scaleIndependentDcSources(dcElements, sourceScale);
    result = circuit.solve(steppedElements, 0, ambientC, Object.assign({}, baseSolverOptions, { gmin: sourcePhaseGmin }));
    trace.push({
      phase: 'source',
      sourceScale,
      gmin: sourcePhaseGmin,
      converged: !!(result.solver && result.solver.converged),
      iterations: result.solver ? result.solver.iterations : null,
    });
  }

  const fullSourceElements = scaleIndependentDcSources(dcElements, 1);
  for (const gmin of gminSteps) {
    result = circuit.solve(fullSourceElements, 0, ambientC, Object.assign({}, baseSolverOptions, { gmin }));
    trace.push({
      phase: 'gmin',
      sourceScale: 1,
      gmin,
      converged: !!(result.solver && result.solver.converged),
      iterations: result.solver ? result.solver.iterations : null,
    });
  }

  restoreDcMeasurements(result, capacitorIds);
  result.analysis = {
    type: 'op',
    historyIndependent: true,
    capacitorRule: 'open-circuit',
    inductorRule: 'winding-dcr',
    continuation: true,
    method: 'source+gmin-stepping',
    sourceScales,
    gminSteps,
    targetGmin,
    trace,
  };
  result.originalElements = original;
  result.dcElements = dcElements;
  return result;
}

function dcSweep(elements, options) {
  options = options || {};
  const sourceId = options.sourceId;
  if (!sourceId) throw new TypeError('sourceId is required');

  const points = sweepValues(options.start, options.stop, options.step);
  const probes = normalizeProbes(options.probes);
  const dt = options.dt == null ? 1e-3 : finiteNumber('dt', options.dt);
  if (dt < 0) throw new RangeError('dt must be >= 0');
  const settleSteps = options.settleSteps == null ? 1 : Math.trunc(options.settleSteps);
  if (!(settleSteps >= 1)) throw new RangeError('settleSteps must be >= 1');
  const ambientC = options.ambientC;
  if (ambientC != null) finiteNumber('ambientC', ambientC);
  const continuation = !!options.continuation;

  const base = cloneElements(elements);
  const sourceTemplate = (base.components || []).find((c) => c.id === sourceId);
  if (!sourceTemplate) throw new Error(`DC sweep source '${sourceId}' was not found`);
  if (sourceTemplate.type !== 'battery' && sourceTemplate.type !== 'diffsource') {
    throw new Error(`DC sweep source '${sourceId}' must be a battery or diffsource, got '${sourceTemplate.type}'`);
  }

  let sharedCircuit = continuation ? new Circuit() : null;
  const rows = [];
  for (const sourceValue of points) {
    const pointElements = cloneElements(base);
    const source = pointElements.components.find((c) => c.id === sourceId);
    source.value = sourceValue;
    const circuit = continuation ? sharedCircuit : new Circuit();

    let result = null;
    for (let i = 0; i < settleSteps; i++) {
      result = circuit.solve(pointElements, dt, ambientC);
    }

    rows.push({
      sourceValue,
      values: sampleProbes(result, probes),
      warnings: Array.from(result.warnings || []),
      finite: Array.from(result.voltages.values()).every(Number.isFinite) &&
        Array.from(result.currents.values()).every(Number.isFinite),
    });
  }

  return {
    analysis: 'dc',
    sourceId,
    start: options.start,
    stop: options.stop,
    step: options.step,
    continuation,
    probes,
    rows,
  };
}


/**
 * Run a transient analysis with explicit startup semantics.
 *
 * Default behavior mirrors ordinary SPICE transient startup: solve a DC
 * operating point first, then seed reactive storage from that physical
 * steady state before advancing time. `uic: true` skips that operating-point
 * solve and starts directly from component-declared `initialV` (capacitors)
 * and `initialCurrent` (inductors), defaulting either quantity to zero when
 * omitted. This is intentionally only startup policy; timestep control and
 * integration-method choices remain separate roadmap items.
 */
function transientAnalysis(elements, options) {
  options = options || {};
  const dt = options.dt == null ? 1e-4 : finiteNumber('dt', options.dt);
  if (!(dt > 0)) throw new RangeError('dt must be > 0');
  const steps = options.steps == null ? 1 : Math.trunc(options.steps);
  if (!(steps >= 1)) throw new RangeError('steps must be >= 1');
  const ambientC = options.ambientC;
  if (ambientC != null) finiteNumber('ambientC', ambientC);
  const probes = normalizeProbes(options.probes);
  const uic = !!options.uic;
  const work = cloneElements(elements);
  let startupResult = null;

  if (!uic) {
    const startupOptions = {
      ambientC,
      solverOptions: options.solverOptions,
    };
    startupResult = options.continuation
      ? steppedOperatingPoint(work, Object.assign({}, startupOptions, {
          sourceScales: options.sourceScales,
          gminSteps: options.gminSteps,
          targetGmin: options.targetGmin,
        }))
      : operatingPoint(work, startupOptions);
    if (!startupResult.solver || !startupResult.solver.converged) {
      throw new Error('transient startup operating point did not converge');
    }

    for (const c of work.components || []) {
      if (c.type === 'capacitor') {
        const va = startupResult.voltages.get(startupResult.uf.find(c.a)) || 0;
        const vb = startupResult.voltages.get(startupResult.uf.find(c.b)) || 0;
        c.initialV = va - vb;
      } else if (c.type === 'inductor') {
        c.initialCurrent = startupResult.currents.get(c.id) || 0;
      }
    }
  }

  const circuit = new Circuit();
  const rows = [];
  let result = null;
  for (let k = 0; k < steps; k++) {
    result = circuit.solve(work, dt, ambientC, options.solverOptions);
    const values = {};
    for (const probe of probes) {
      let value = null;
      if (probe.type === 'voltage') {
        const root = result.uf.find(probe.node);
        const raw = result.voltages.get(root);
        value = raw == null ? null : raw;
      } else {
        const raw = result.currents.get(probe.componentId);
        value = raw == null ? null : raw;
      }
      values[probe.name] = value;
    }
    rows.push({
      time: (k + 1) * dt,
      values,
      warnings: Array.from(result.warnings || []),
      converged: !!(result.solver && result.solver.converged),
    });
  }

  return {
    analysis: {
      type: 'tran',
      dt,
      steps,
      uic,
      startup: uic ? 'user-initial-conditions' : 'dc-operating-point',
      continuation: !uic && !!options.continuation,
      capacitorInitialCondition: uic ? 'declared-initialV-or-zero' : 'dc-operating-point-voltage',
      inductorInitialCondition: uic ? 'declared-initialCurrent-or-zero' : 'dc-operating-point-current',
    },
    probes,
    rows,
    startupResult,
    finalResult: result,
  };
}


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

module.exports = { operatingPoint, steppedOperatingPoint, dcSweep, transientAnalysis, adaptiveTransientAnalysis, normalizedTransientError, snapshotCircuitState, restoreCircuitState, sweepValues };
