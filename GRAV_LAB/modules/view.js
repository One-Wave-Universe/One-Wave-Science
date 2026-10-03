window.OW = window.OW || {};
OW.view = function (ctx, field, w, h, dpr) {
  const cx = w * 0.5, cy = h * 0.5, scale = Math.min(w, h) * 0.12;
  ctx.fillStyle = "#100c09";
  ctx.fillRect(0, 0, w, h);
  for (const s of field.sites) {
    ctx.beginPath();
    ctx.arc(cx + s.x * scale, cy + s.y * scale, 4 * dpr, 0, 7);
    ctx.fillStyle = `rgba(243, 190, 110, ${0.15 + 0.85 * Math.min(s.chi || 0, 1)})`;
    ctx.fill();
  }
  for (const b of field.kids) {
    ctx.beginPath();
    ctx.arc(cx + b.x * scale, cy + b.y * scale, 8 * dpr, 0, 7);
    ctx.fillStyle = "#ff8a3d";
    ctx.fill();
  }
};
