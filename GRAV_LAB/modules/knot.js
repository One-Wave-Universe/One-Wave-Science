window.OW = window.OW || {};
OW.knot = function (vortices) {
  const pts = [];
  for (let i = 0; i <= 90; i++) {
    const t = i / 90;
    const a = t * 2 * Math.PI;
    const v = vortices[i % 3];
    const braid = 0.25 * Math.sin(3 * a + v.spin);
    pts.push({ x: (0.9 + braid) * Math.cos(a), y: (0.9 + braid) * Math.sin(a) });
  }
  return pts;
};
