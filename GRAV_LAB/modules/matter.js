window.OW = window.OW || {};
OW.matter = function (field, on) {
  if (!on) {
    field.matter = 0;
    return;
  }
  let load = 0;
  for (const v of field.vortices) {
    load += OW.wake(Math.hypot(v.x, v.y), field.parent.sigma);
  }
  field.matter = load;
  field.energy += load;
};
