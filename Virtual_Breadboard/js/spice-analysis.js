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

module.exports = { operatingPoint, steppedOperatingPoint, dcSweep, sweepValues };
