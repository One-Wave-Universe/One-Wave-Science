'use strict';

/*
 * Bench-reality audit layer.
 *
 * The circuit engine answers the circuit it was given. This layer answers a
 * different question: does that solved circuit still correspond to a build
 * we could honestly put on a solderless breadboard or bench supply?
 *
 * It deliberately catches design-level false positives that a mathematically
 * valid MNA solve cannot catch by itself: a cut CENTER spine hidden by a
 * capacitor, a virtual-ground helper mixed into a true dual-rail supply,
 * source current beyond the bench limit, an active load with a claimed zero
 * source receipt, and forbidden power-stage blocks inside a cell-only test.
 *
 * Metadata fields such as `role`, `benchMaxCurrent`, and `benchClass` are
 * ignored by the electrical solver; they exist only to make the physical
 * contract explicit and testable here.
 */

function nodeVoltage(result, node) {
  if (!result || !result.voltages) return NaN;
  if (result.voltages.has(node)) return result.voltages.get(node);
  if (result.uf && result.uf.find) {
    const root = result.uf.find(node);
    if (result.voltages.has(root)) return result.voltages.get(root);
  }
  return NaN;
}

function currentFor(result, id) {
  if (!result || !result.currents) return NaN;
  const v = result.currents.get(id);
  return Number.isFinite(v) ? v : NaN;
}

function resistorPower(elements, result) {
  let total = 0;
  for (const c of (elements.components || [])) {
    if (c.type !== 'resistor' || !(c.value > 0)) continue;
    const i = currentFor(result, c.id);
    if (Number.isFinite(i)) {
      total += i * i * c.value;
      continue;
    }
    const va = nodeVoltage(result, c.a);
    const vb = nodeVoltage(result, c.b);
    if (Number.isFinite(va) && Number.isFinite(vb)) {
      total += ((va - vb) * (va - vb)) / c.value;
    }
  }
  return total;
}

function audit(elements, result, options = {}) {
  const components = elements.components || [];
  const errors = [];
  const warnings = [];
  const receipts = {};

  // CENTER is a conductor/reference spine in the bench contract. A series
  // capacitor can look centered under symmetric loading while providing no
  // DC return. That is a false positive, so fail it explicitly.
  const centerParts = components.filter((c) => c.role === 'center_spine');
  if (options.requireSolidCenter) {
    if (!centerParts.length) {
      errors.push({ code: 'CENTER_SPINE_MISSING', message: 'No component/wire is tagged as the physical CENTER spine.' });
    }
    for (const c of centerParts) {
      if (c.type === 'capacitor') {
        errors.push({ code: 'CENTER_SPINE_SERIES_CAP', id: c.id, message: 'CENTER spine contains a series capacitor; DC reference is cut even if symmetric loads make the voltage look centered.' });
      }
      if (c.type === 'isource' || c.type === 'vccs' || c.type === 'cccs') {
        errors.push({ code: 'CENTER_SPINE_NOT_CONDUCTIVE', id: c.id, message: 'CENTER spine is implemented by a current-source element instead of a solid low-impedance conductor.' });
      }
      if (c.type === 'resistor' && Number.isFinite(options.maxCenterResistance) && c.value > options.maxCenterResistance) {
        errors.push({ code: 'CENTER_SPINE_TOO_RESISTIVE', id: c.id, value: c.value, message: `CENTER spine resistance ${c.value} ohm exceeds bench limit ${options.maxCenterResistance} ohm.` });
      }
    }
  }

  // A true dual +/- supply already owns the physical midpoint. Do not also
  // insert a rail-splitter / TLE-like vgnd and call both of them the same 0.
  const hasPositiveSupply = components.some((c) => c.role === 'positive_supply');
  const hasNegativeSupply = components.some((c) => c.role === 'negative_supply');
  const hasVgnd = components.some((c) => c.type === 'vgnd');
  if (hasPositiveSupply && hasNegativeSupply && hasVgnd) {
    errors.push({ code: 'MIXED_CENTER_TOPOLOGY', message: 'Dual +/- supply midpoint and virtual-ground splitter are both present. Pick one physical CENTER architecture.' });
  }

  // Bench current limits are part-specific. The engine historically used a
  // global source ceiling, which is not enough for a supply deliberately set
  // to 20 mA. Treat the declared bench limit as an acceptance gate even when
  // the lower-level solver can still produce a numeric answer.
  for (const c of components) {
    if (!Number.isFinite(c.benchMaxCurrent)) continue;
    const i = currentFor(result, c.id);
    if (!Number.isFinite(i)) {
      warnings.push({ code: 'SOURCE_CURRENT_UNAVAILABLE', id: c.id, message: 'No solved source-current receipt is available for this bench-limited source.' });
      continue;
    }
    receipts[c.id] = i;
    if (Math.abs(i) > c.benchMaxCurrent + 1e-12) {
      errors.push({ code: 'BENCH_CURRENT_LIMIT_EXCEEDED', id: c.id, current: i, limit: c.benchMaxCurrent, message: `${c.id} draws ${Math.abs(i)} A, above declared bench limit ${c.benchMaxCurrent} A.` });
    }
  }

  // If resistors are dissipating real power, at least one declared supply
  // must report real current. This prevents a poster/UI from presenting an
  // active-looking circuit next to a literal 0.00 A source receipt.
  const loadPower = resistorPower(elements, result);
  const supplyParts = components.filter((c) => c.role === 'positive_supply' || c.role === 'negative_supply' || c.role === 'main_supply');
  if (options.requireSourceReceipt && loadPower > (options.minActiveLoadPower || 1e-6) && supplyParts.length) {
    const currents = supplyParts.map((c) => Math.abs(currentFor(result, c.id))).filter(Number.isFinite);
    if (!currents.length || Math.max(...currents) < (options.minSourceReceipt || 1e-6)) {
      errors.push({ code: 'IMPOSSIBLE_ZERO_SOURCE_RECEIPT', loadPower, message: `Solved load power is ${loadPower} W but declared supply current is effectively zero.` });
    }
  }

  if (options.cellOnly) {
    for (const c of components) {
      if (c.type === 'hbridge') {
        errors.push({ code: 'MOTOR_DRIVER_INSIDE_CELL', id: c.id, message: 'CELL_V1 qualification contains an H-bridge/motor-driver block. Motor power stage must remain electrically separate.' });
      }
    }
  }

  return { ok: errors.length === 0, errors, warnings, receipts, loadPower };
}

module.exports = { audit, nodeVoltage, currentFor, resistorPower };
