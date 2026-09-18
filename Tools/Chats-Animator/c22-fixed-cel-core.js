(function (root, factory) {
  'use strict';
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.AnimatorFixedCelCore = api;
})(typeof window !== 'undefined' ? window : globalThis, function () {
  'use strict';

  const clone = (value) => JSON.parse(JSON.stringify(value));

  function buildSnapshots(baseSnapshot, assetId, poseSources) {
    if (!baseSnapshot || !Array.isArray(baseSnapshot.assets)) throw new Error('Base snapshot assets missing');
    if (!Array.isArray(poseSources) || poseSources.length < 2) throw new Error('At least two pose sources are required');
    const baseAsset = baseSnapshot.assets.find((asset) => asset.id === assetId);
    if (!baseAsset) throw new Error('Target asset missing from base snapshot');

    const fixed = {
      x: baseAsset.x,
      groundY: baseAsset.groundY,
      manualScale: baseAsset.manualScale
    };

    return poseSources.map((src, index) => {
      const snapshot = clone(baseSnapshot);
      const target = snapshot.assets.find((asset) => asset.id === assetId);
      target.src = src;
      target.name = `GR Walk Cel ${String(index + 1).padStart(2, '0')}`;
      target.x = fixed.x;
      target.groundY = fixed.groundY;
      target.manualScale = fixed.manualScale;
      snapshot.selectedAssetId = assetId;
      return snapshot;
    });
  }

  function verifyFixedCelSnapshots(snapshots, assetId) {
    if (!Array.isArray(snapshots) || snapshots.length < 2) throw new Error('Need multiple snapshots');
    const assets = snapshots.map((snapshot) => snapshot.assets.find((asset) => asset.id === assetId));
    if (assets.some((asset) => !asset)) throw new Error('Target asset missing from one or more snapshots');
    const transforms = assets.map((asset) => [asset.x, asset.groundY, asset.manualScale].join('|'));
    const drawings = new Set(assets.map((asset) => asset.src));
    return {
      frameCount: snapshots.length,
      uniqueDrawings: drawings.size,
      fixedTransform: new Set(transforms).size === 1
    };
  }

  return { buildSnapshots, verifyFixedCelSnapshots };
});
