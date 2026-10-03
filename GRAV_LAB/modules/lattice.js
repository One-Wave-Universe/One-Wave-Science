window.OW = window.OW || {};
OW.lattice = function (reach) {
  const sites = [];
  for (let q = -reach; q <= reach; q++) {
    for (let r = -reach; r <= reach; r++) {
      sites.push({ x: (q + r / 2) * 0.55, y: r * 0.476 });
    }
  }
  return sites;
};
