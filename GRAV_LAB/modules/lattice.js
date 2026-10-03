window.OW = window.OW || {};
OW.shell12 = [
  [1, 1, 0], [1, -1, 0], [-1, 1, 0], [-1, -1, 0],
  [1, 0, 1], [1, 0, -1], [-1, 0, 1], [-1, 0, -1],
  [0, 1, 1], [0, 1, -1], [0, -1, 1], [0, -1, -1]
];
OW.lattice = function () {
  const sites = [{ x: 0, y: 0, z: 0, role: "center" }];
  for (const n of OW.shell12) sites.push({ x: n[0], y: n[1], z: n[2], role: "neighbor" });
  return sites;
};
