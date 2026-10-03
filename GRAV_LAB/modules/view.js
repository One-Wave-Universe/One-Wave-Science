window.OW = window.OW || {};
OW.view = function (ctx, field, w, h, dpr) {
  const cx = w * 0.5, cy = h * 0.5, scale = Math.min(w, h) * 0.12;
  const a = field.spin || 0;
  const proj = (s) => {
    const x = s.x * Math.cos(a) - s.z * Math.sin(a);
    const z = s.x * Math.sin(a) + s.z * Math.cos(a);
    return { x: cx + x * scale, y: cy - s.y * scale * 0.85 - z * 0.45 * scale, z };
  };
  ctx.fillStyle = "#100c09";
  ctx.fillRect(0, 0, w, h);
  const pts = field.sites.map(proj);
  ctx.strokeStyle = "rgba(243,190,110,0.35)";
  ctx.lineWidth = dpr;
  for (let i = 0; i < field.sites.length; i++) {
    for (let j = i + 1; j < field.sites.length; j++) {
      const dx = field.sites[i].x - field.sites[j].x;
      const dy = field.sites[i].y - field.sites[j].y;
      const dz = field.sites[i].z - field.sites[j].z;
      if (dx * dx + dy * dy + dz * dz < 1.05) {
        ctx.beginPath();
        ctx.moveTo(pts[i].x, pts[i].y);
        ctx.lineTo(pts[j].x, pts[j].y);
        ctx.stroke();
      }
    }
  }
  for (let i = 0; i < pts.length; i++) {
    const p = pts[i];
    ctx.beginPath();
    ctx.arc(p.x, p.y, 5 * dpr, 0, 7);
    const chi = field.sites[i].chi || 0;
    ctx.fillStyle = `rgba(255,176,90,${0.35 + 0.65 * Math.min(chi, 1)})`;
    ctx.fill();
  }
  field.spin = a + 0.008;
};
