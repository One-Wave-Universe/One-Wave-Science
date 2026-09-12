'use strict';

/*
 * Bode/transfer-function reporting for the Virtual Breadboard AC solver.
 *
 * This module does no circuit solving of its own. It consumes the complex
 * small-signal node phasors produced by ac-analysis.js and turns named input
 * and output voltage probes into a transfer function H(jw)=Vout/Vin with
 * linear magnitude, dB magnitude, wrapped phase, and plot-friendly unwrapped
 * phase. Keeping this separate means plotting/reporting cannot change the
 * electrical answer.
 */

const AC = require('./ac-analysis.js');
const { smallSignalAc, phasorMagnitude, phasorPhaseDeg } = AC;

const C = (re, im) => ({ re: re || 0, im: im || 0 });
const sub = (a, b) => C(a.re - b.re, a.im - b.im);
const div = (a, b) => {
  const d = b.re * b.re + b.im * b.im;
  if (!(d > 0)) throw new Error('Bode input phasor is zero; transfer function is undefined');
  return C((a.re * b.re + a.im * b.im) / d, (a.im * b.re - a.re * b.im) / d);
};

function normalizeVoltageProbe(name, probe) {
  if (typeof probe === 'string') return { name, positive: probe, negative: null };
  if (!probe || typeof probe !== 'object' || probe.positive == null) {
    throw new TypeError(`${name} probe must be a node name or { positive, negative? }`);
  }
  return {
    name: probe.name || name,
    positive: probe.positive,
    negative: probe.negative == null ? null : probe.negative,
  };
}

function probePhasor(acResult, row, probe) {
  const positiveRoot = acResult.uf.find(probe.positive);
  const vp = row.voltages.get(positiveRoot) || C(0, 0);
  if (probe.negative == null) return vp;
  const negativeRoot = acResult.uf.find(probe.negative);
  const vn = row.voltages.get(negativeRoot) || C(0, 0);
  return sub(vp, vn);
}

function unwrapPhaseDegrees(phases) {
  const out = [];
  let offset = 0;
  let previous = null;
  for (const phase of phases) {
    if (previous != null) {
      const rawDelta = phase + offset - previous;
      if (rawDelta > 180) offset -= 360;
      else if (rawDelta < -180) offset += 360;
    }
    const unwrapped = phase + offset;
    out.push(unwrapped);
    previous = unwrapped;
  }
  return out;
}

function bodeTransfer(elements, options) {
  options = options || {};
  const inputProbe = normalizeVoltageProbe('input', options.input);
  const outputProbe = normalizeVoltageProbe('output', options.output);

  const acOptions = Object.assign({}, options);
  delete acOptions.input;
  delete acOptions.output;
  const acResult = smallSignalAc(elements, acOptions);

  const rawRows = acResult.rows.map((row) => {
    const input = probePhasor(acResult, row, inputProbe);
    const output = probePhasor(acResult, row, outputProbe);
    const transfer = div(output, input);
    const magnitude = phasorMagnitude(transfer);
    const phaseDeg = phasorPhaseDeg(transfer);
    return {
      frequencyHz: row.frequencyHz,
      input,
      output,
      transfer,
      magnitude,
      magnitudeDb: magnitude > 0 ? 20 * Math.log10(magnitude) : -Infinity,
      phaseDeg,
    };
  });

  const unwrapped = unwrapPhaseDegrees(rawRows.map((row) => row.phaseDeg));
  const rows = rawRows.map((row, i) => Object.assign({}, row, { unwrappedPhaseDeg: unwrapped[i] }));

  return {
    analysis: {
      type: 'bode',
      transferFunction: true,
      sourceId: acResult.analysis.sourceId,
      input: inputProbe,
      output: outputProbe,
    },
    frequencies: acResult.frequencies,
    rows,
    operatingPoint: acResult.operatingPoint,
    ac: acResult,
  };
}

module.exports = { bodeTransfer, normalizeVoltageProbe, unwrapPhaseDegrees };
