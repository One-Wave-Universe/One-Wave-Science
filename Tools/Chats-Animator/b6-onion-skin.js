(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('B6 requires Animator + reel');
  const $ = (id) => document.getElementById(id);
  const assetLayer = $('asset-layer');
  let onionLayer = $('onion-layer');
  if (!onionLayer && assetLayer) {
    onionLayer = document.createElement('div');
    onionLayer.id = 'onion-layer';
    assetLayer.before(onionLayer);
  }

  function addGhosts(snapshot, className) {
    if (!snapshot || !onionLayer) return;
    for (const asset of snapshot.assets || []) {
      const img = document.createElement('img');
      img.className = `onion-asset ${className}`;
      img.src = asset.src;
      const c = snapshot.calibration || A.state.calibration;
      const span = Math.max(0.001, c.nearY - c.farY);
      const t = Math.max(0, Math.min(1, (asset.groundY - c.farY) / span));
      const scale = (c.farScale + (c.nearScale - c.farScale) * t) * asset.manualScale;
      img.style.left = `${asset.x * 100}%`;
      img.style.top = `${asset.groundY * 100}%`;
      img.style.height = `${Math.max(5, 42 * scale)}%`;
      img.style.transform = 'translate(-50%, -100%)';
      onionLayer.appendChild(img);
    }
  }
  function render() {
    if (!onionLayer) return;
    onionLayer.innerHTML = '';
    const i = R.activeIndex;
    if ($('onion-prev')?.checked && i > 0) addGhosts(R.frames[i - 1].snapshot, 'onion-prev');
    if ($('onion-next')?.checked && i < R.frames.length - 1) addGhosts(R.frames[i + 1].snapshot, 'onion-next');
  }
  $('onion-prev')?.addEventListener('change', render);
  $('onion-next')?.addEventListener('change', render);
  A.onion = { render };
  render();
})();
