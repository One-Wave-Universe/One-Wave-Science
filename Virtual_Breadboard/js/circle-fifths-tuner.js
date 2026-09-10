(function (root) {
  'use strict';

  const A4 = 440;
  const NOTE_NAMES = ['C', 'C♯/D♭', 'D', 'D♯/E♭', 'E', 'F', 'F♯/G♭', 'G', 'G♯/A♭', 'A', 'A♯/B♭', 'B'];
  const FIFTHS = ['C', 'G', 'D', 'A', 'E', 'B', 'F♯', 'D♭', 'A♭', 'E♭', 'B♭', 'F'];

  function frequencyToMidi(frequency, a4 = A4) {
    if (!Number.isFinite(frequency) || frequency <= 0) return null;
    return 69 + 12 * Math.log2(frequency / a4);
  }

  function midiToFrequency(midi, a4 = A4) {
    if (!Number.isFinite(midi)) return null;
    return a4 * Math.pow(2, (midi - 69) / 12);
  }

  function describeFrequency(frequency, a4 = A4) {
    const midiFloat = frequencyToMidi(frequency, a4);
    if (midiFloat == null) return null;
    const midi = Math.round(midiFloat);
    const cents = (midiFloat - midi) * 100;
    const noteIndex = ((midi % 12) + 12) % 12;
    return {
      frequency,
      midi,
      note: NOTE_NAMES[noteIndex],
      pitchClass: noteIndex,
      octave: Math.floor(midi / 12) - 1,
      cents,
      targetFrequency: midiToFrequency(midi, a4),
    };
  }

  // Normalized autocorrelation pitch detector. It intentionally returns null
  // for weak/noisy/unpitched frames rather than manufacturing a note.
  function detectPitch(samples, sampleRate, options = {}) {
    if (!samples || samples.length < 256 || !Number.isFinite(sampleRate) || sampleRate <= 0) return null;
    const minHz = options.minHz || 55;
    const maxHz = options.maxHz || 1320;
    const rmsGate = options.rmsGate == null ? 0.008 : options.rmsGate;
    const minLag = Math.max(2, Math.floor(sampleRate / maxHz));
    const maxLag = Math.min(samples.length - 2, Math.ceil(sampleRate / minHz));

    let mean = 0;
    for (let i = 0; i < samples.length; i++) mean += samples[i];
    mean /= samples.length;

    let energy = 0;
    for (let i = 0; i < samples.length; i++) {
      const v = samples[i] - mean;
      energy += v * v;
    }
    const rms = Math.sqrt(energy / samples.length);
    if (rms < rmsGate) return null;

    let bestLag = -1;
    let bestCorr = 0;
    const correlations = new Float64Array(maxLag + 1);
    for (let lag = minLag; lag <= maxLag; lag++) {
      let xy = 0, xx = 0, yy = 0;
      const limit = samples.length - lag;
      for (let i = 0; i < limit; i++) {
        const x = samples[i] - mean;
        const y = samples[i + lag] - mean;
        xy += x * y;
        xx += x * x;
        yy += y * y;
      }
      const denom = Math.sqrt(xx * yy);
      const corr = denom > 0 ? xy / denom : 0;
      correlations[lag] = corr;
      if (corr > bestCorr) {
        bestCorr = corr;
        bestLag = lag;
      }
    }

    const confidenceGate = options.confidenceGate == null ? 0.72 : options.confidenceGate;
    if (bestLag < 0 || bestCorr < confidenceGate) return null;

    // Parabolic interpolation around the strongest lag for sub-sample tuning.
    let lag = bestLag;
    if (bestLag > minLag && bestLag < maxLag) {
      const y1 = correlations[bestLag - 1];
      const y2 = correlations[bestLag];
      const y3 = correlations[bestLag + 1];
      const denom = y1 - 2 * y2 + y3;
      if (Math.abs(denom) > 1e-12) lag += 0.5 * (y1 - y3) / denom;
    }

    const frequency = sampleRate / lag;
    if (frequency < minHz || frequency > maxHz) return null;
    return { frequency, confidence: bestCorr, rms };
  }

  const api = { A4, NOTE_NAMES, FIFTHS, frequencyToMidi, midiToFrequency, describeFrequency, detectPitch };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.CircleFifthsTuner = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
