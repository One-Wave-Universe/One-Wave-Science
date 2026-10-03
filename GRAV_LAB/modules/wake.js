window.OW = window.OW || {};
OW.wake = function (r, sigma) {
  const s = Math.max(sigma, 1e-6);
  return Math.exp(-r / s) / Math.sqrt(r * r + 0.04 * s * s);
};
