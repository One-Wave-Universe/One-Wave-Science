window.OW = window.OW || {};
OW.energy = function (field) {
  let total = 0;
  for (const s of field.sites) {
    s.chi = field.parent.amp * OW.wake(Math.hypot(s.x, s.y), field.parent.sigma);
    total += s.chi;
  }
  field.energy = total;
  return total;
};
