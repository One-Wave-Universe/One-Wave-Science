'use strict';

const assert = require('assert');
const Tuner = require('../js/circle-fifths-tuner.js');

function sine(freq, sampleRate, n, amplitude = 0.5) {
  const out = new Float32Array(n);
  for (let i = 0; i < n; i++) out[i] = amplitude * Math.sin(2 * Math.PI * freq * i / sampleRate);
  return out;
}

(function run() {
  const a4 = Tuner.describeFrequency(440);
  assert.equal(a4.note, 'A');
  assert.equal(a4.octave, 4);
  assert(Math.abs(a4.cents) < 1e-9);

  const c4 = Tuner.describeFrequency(261.625565);
  assert.equal(c4.note, 'C');
  assert.equal(c4.octave, 4);
  assert(Math.abs(c4.cents) < 0.01);

  const sampleRate = 48000;
  for (const freq of [82.4069, 110, 220, 440, 659.255]) {
    const found = Tuner.detectPitch(sine(freq, sampleRate, 4096), sampleRate);
    assert(found, `expected pitch for ${freq} Hz`);
    const cents = 1200 * Math.log2(found.frequency / freq);
    assert(Math.abs(cents) < 3, `${freq} Hz detection off by ${cents} cents`);
  }

  const silence = new Float32Array(4096);
  assert.equal(Tuner.detectPitch(silence, sampleRate), null, 'silence must not invent a pitch');

  console.log('circle-fifths-tuner: PASS');
})();
