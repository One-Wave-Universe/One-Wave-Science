'use strict';

/*
 * SPICE-style analysis helpers for the Virtual Breadboard solver.
 *
 * This deliberately sits beside Circuit.solve() instead of refactoring the
 * load-bearing MNA core.  Analysis modes transform only what SPICE itself
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
  const span = Math.abs(stop - start);
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

/**
 * Build and solve a true DC operating point (.op-class).
 *
 * DC rules are explicit and history-free:
 *   - capacitors are open circuits and therefore carry 0 A DC current;
 *   - inductors lose only their reactive L/dt term and retain the same real
 *     winding DCR already used by the transient solver;
 *   - a fresh Circuit instance is always used, so capacitor voltage,
 *     inductor current, battery/runtime state, and magnetic transient history
 *     from any earlier simulation cannot leak into this answer.
 *
 * Everything else is still solved by Circuit.solve(), including the same MNA,
 * nonlinear device iteration, GMIN, convergence report, and fault warnings.
 */
function operatingPoint(elements, options) {
  options = options || {};
  const ambientC = options.ambientC;
  if (ambientC != null) finiteNumber('ambientC', ambientC);

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

  const circuit = new Circuit();
  // dt is irrelevant to the transformed C/L network, but the generic solver
  // still accepts one because other transient-capable component models share
  // the same entry point. A fixed positive value keeps that API well-defined.
  const result = circuit.solve(dcElements, 1, ambientC, options.solverOptions);

  // Preserve original component IDs as measurable DC quantities. Removed
  // capacitors are true open circuits, so their DC current is exactly zero.
  for (const id of capacitorIds) result.currents.set(id, 0);

  result.analysis = {
    type: 'op',
    historyIndependent: true,
    capacitorRule: 'open-circuit',
    inductorRule: 'winding-dcr',
  };
  result.originalElements = original;
  result.dcElements = dcElements;
  return result;
}

/**
 * Sweep one independent source through a numeric range.
 *
 * Supported swept sources: battery and diffsource. Each point uses a fresh
 * Circuit by default so history does not silently contaminate the transfer
 * curve. continuation=true retains the older deliberate history/hysteresis
 * experiment mode.
 */
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

module.exports = { operatingPoint, dcSweep, sweepValues };
