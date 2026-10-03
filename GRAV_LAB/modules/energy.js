window.OW = window.OW || {};
OW.energy = function (field) {
  let total = 0;
  for (const s of field.sites) {
    const r = Math.hypot(s.x, s.y, s.z || 0);
    s.chi = field.parent.amp * OW.wake(r, field.parent.sigma);
    total += s.chi;
  }
  field.energy = total;
  return total;
};
