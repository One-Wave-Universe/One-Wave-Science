'use strict';

/*
 * SPICE-style analysis helpers for the Virtual Breadboard solver.
 *
 * This deliberately sits beside Circuit.solve() instead of refactoring the
 * load-bearing MNA core.  The first analysis implemented here is a DC source
 * sweep: vary one independent source, solve each operating point, and record
 * requested node voltages/component currents.  That is the same experiment
 * shape as SPICE .dc and gives the breadboard a repeatable transfer-curve
 * tool without changing the editor or component models.
 */

const CircuitEngine = require('./circuit.js');
const { Circuit } = CircuitEngine;

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
  // Floating-point sweeps must not miss the requested stop because 0.1 is
  // not exactly representable.  Compute by integer index and admit a tiny
  // endpoint epsilon rather than repeatedly adding step to the prior value.
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
 * Sweep one independent source through a numeric range.
 *
 * Supported swept sources for the first implementation: battery and
 * diffsource.  Those are the Virtual Breadboard's real DC independent
 * voltage-source types.  AC sources are intentionally excluded because a
 * transient sinusoid's instantaneous value is not a DC operating parameter.
 *
 * By default every point gets a fresh Circuit instance.  That prevents a
 * capacitor/core/battery history from one point contaminating the next point.
 * Set continuation=true when deliberately testing hysteresis/history; then the
 * same Circuit state is carried point-to-point, similar to continuation in a
 * nonlinear sweep.
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

module.exports = { dcSweep, sweepValues };
