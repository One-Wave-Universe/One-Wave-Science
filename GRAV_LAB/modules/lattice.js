window.OW = window.OW || {};
OW.lattice = function (layers) {
  const n = layers || 2;
  const sites = [];
  const s3 = Math.sqrt(3);
  const dz = Math.sqrt(6) / 3;
  for (let L = -n; L <= n; L++) {
    const shift = Math.abs(L) % 2;
    for (let i = -n; i <= n; i++) {
      for (let j = -n; j <= n; j++) {
        const x = i + j / 2 + shift * 0.5;
        const y = j * s3 / 2 + shift * s3 / 6;
        const z = L * dz;
        if (x * x + y * y + z * z > (n + 0.2) * (n + 0.2)) continue;
        sites.push({ x, y, z, role: (i === 0 && j === 0 && L === 0) ? "center" : "neighbor" });
      }
    }
  }
  return sites;
};
