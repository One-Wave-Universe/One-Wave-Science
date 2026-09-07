// Shared helper for the 17 permanent regression builds. Each build file
// in this directory exports a run() that returns { name, checks }: one
// real circuit, one or more real expected/actual/tolerance/pass-fail
// checks, no eyeballed waveforms. test/run_regression_builds.js loads
// every build in this directory and reruns them all together after any
// major update to js/circuit.js or simulate.js.
const CircuitEngine = require('../../js/circuit.js');
const { Circuit } = CircuitEngine;
const Sim = require('../../simulate.js');

function check(name, expected, actual, tolerance, note) {
  const pass = typeof expected === 'boolean' ? expected === actual : Math.abs(actual - expected) <= tolerance;
  return { name, expected, actual, tolerance: tolerance != null ? tolerance : null, pass, note: note || '' };
}

module.exports = { CircuitEngine, Circuit, Sim, check };
