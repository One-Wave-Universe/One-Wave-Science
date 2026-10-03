window.OW = window.OW || {};
OW.kids = function () {
  const kids = [];
  for (let k = 0; k < 3; k++) {
    const a = 2 * Math.PI * k / 3;
    kids.push({ x: 1.6 * Math.cos(a), y: 1.6 * Math.sin(a), vx: -0.3 * Math.sin(a), vy: 0.3 * Math.cos(a) });
  }
  return kids;
};
OW.motion = function (field) {
  const amp = field.parent.amp;
  const sigma = field.parent.sigma;
  const h = 0.02;
  for (const b of field.kids) {
    const c = (x, y) => amp * OW.wake(Math.hypot(x, y), sigma);
    const gx = (c(b.x + h, b.y) - c(b.x - h, b.y)) / (2 * h);
    const gy = (c(b.x, b.y + h) - c(b.x, b.y - h)) / (2 * h);
    b.vx = (b.vx - 1.4 * gx * 0.03) * 0.995;
    b.vy = (b.vy - 1.4 * gy * 0.03) * 0.995;
    b.x += b.vx * 0.03;
    b.y += b.vy * 0.03;
  }
};
