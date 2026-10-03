window.OW = window.OW || {};
OW.view = function (ctx, field, w, h, dpr) {
  const cx = w * 0.5, cy = h * 0.5, scale = Math.min(w, h) * 0.16;
  const a = field.spin || 0;
  ctx.fillStyle = "#100c09";
  ctx.fillRect(0, 0, w, h);
  const pts = field.sites.map(s => {
    const x = s.x * Math.cos(a) - s.z * Math.sin(a);
    const z = s.x * Math.sin(a) + s.z * Math.cos(a);
    return { x: cx + x * scale, y: cy + s.y * scale - z * 0.35 * scale, chi: s.chi || 0, role: s.role };
  });
  pts.sort((p, q) => p.y - q.y);
  for (const p of pts) {
    ctx.beginPath();
    ctx.arc(p.x, p.y, (p.role === "center" ? 8 : 5) * dpr, 0, 7);
    ctx.fillStyle = `rgba(243, 190, 110, ${0.25 + 0.75 * Math.min(p.chi, 1)})`;
    ctx.fill();
  }
  field.spin = a + 0.01;
};
