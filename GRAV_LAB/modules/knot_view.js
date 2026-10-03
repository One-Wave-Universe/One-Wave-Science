window.OW = window.OW || {};
OW.drawVortices = function (ctx, vortices, cx, cy, scale, dpr) {
  for (const v of vortices) {
    ctx.beginPath();
    ctx.arc(cx + v.x * scale, cy + v.y * scale, 10 * dpr, v.spin, v.spin + 4);
    ctx.strokeStyle = "#ffb15e";
    ctx.lineWidth = 2 * dpr;
    ctx.stroke();
  }
};
OW.drawKnot = function (ctx, pts, cx, cy, scale, dpr) {
  ctx.beginPath();
  pts.forEach((p, i) => {
    const x = cx + p.x * scale, y = cy + p.y * scale;
    i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
  });
  ctx.closePath();
  ctx.strokeStyle = "#f3e2c4";
  ctx.lineWidth = 2 * dpr;
  ctx.stroke();
};
