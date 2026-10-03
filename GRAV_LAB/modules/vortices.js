window.OW = window.OW || {};
OW.vortices = function () {
  const out = [];
  for (let k = 0; k < 3; k++) {
    const a = 2 * Math.PI * k / 3;
    out.push({ phase: k, angle: a, x: 0.9 * Math.cos(a), y: 0.9 * Math.sin(a), spin: a });
  }
  return out;
};
OW.stepVortices = function (vortices) {
  for (const v of vortices) v.spin += 0.02;
};
