(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('B12 requires Animator + reel');
  const $ = (id) => document.getElementById(id);
  const aside = document.querySelector('aside');
  if (!aside) return;

  const defaults = { x: 0, y: 0, zoom: 1 };
  let camera = { ...defaults };

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>Camera — current frame</strong><br>
    Pan and zoom are saved into each reel frame. Duplicate a frame to carry its camera forward, then adjust the next frame.
    <div class="control"><label><span>Pan X</span><span id="camera-x-value">0</span></label><input id="camera-x" type="range" min="-50" max="50" step="1" value="0"></div>
    <div class="control"><label><span>Pan Y</span><span id="camera-y-value">0</span></label><input id="camera-y" type="range" min="-50" max="50" step="1" value="0"></div>
    <div class="control"><label><span>Zoom</span><span id="camera-zoom-value">1.00</span></label><input id="camera-zoom" type="range" min="0.50" max="3.00" step="0.05" value="1"></div>
    <button id="reset-camera" type="button">Reset Camera</button>
  `;
  aside.insertBefore(panel, aside.firstChild);

  function normalize(value) {
    return {
      x: Math.max(-50, Math.min(50, Number(value?.x) || 0)),
      y: Math.max(-50, Math.min(50, Number(value?.y) || 0)),
      zoom: Math.max(0.5, Math.min(3, Number(value?.zoom) || 1))
    };
  }

  function applyCamera() {
    const transform = `translate(${camera.x}%, ${camera.y}%) scale(${camera.zoom})`;
    for (const id of ['scene-background', 'asset-layer', 'onion-layer']) {
      const node = $(id);
      if (!node) continue;
      node.style.transformOrigin = '50% 50%';
      node.style.transform = transform;
    }
    if ($('camera-x')) $('camera-x').value = String(camera.x);
    if ($('camera-y')) $('camera-y').value = String(camera.y);
    if ($('camera-zoom')) $('camera-zoom').value = String(camera.zoom);
    if ($('camera-x-value')) $('camera-x-value').textContent = String(camera.x);
    if ($('camera-y-value')) $('camera-y-value').textContent = String(camera.y);
    if ($('camera-zoom-value')) $('camera-zoom-value').textContent = camera.zoom.toFixed(2);
  }

  const originalSnapshot = A.snapshot.bind(A);
  const originalRestore = A.restore.bind(A);

  A.snapshot = function snapshotWithCamera() {
    const snapshot = originalSnapshot();
    snapshot.camera = A.clone(camera);
    return snapshot;
  };

  A.restore = function restoreWithCamera(snapshot) {
    originalRestore(snapshot);
    camera = normalize(snapshot?.camera || defaults);
    applyCamera();
  };

  function update(prop, value) {
    camera[prop] = Number(value);
    camera = normalize(camera);
    applyCamera();
    R.captureCurrent();
    A.status(`Camera ${prop} updated`);
  }

  $('camera-x')?.addEventListener('input', (event) => update('x', event.target.value));
  $('camera-y')?.addEventListener('input', (event) => update('y', event.target.value));
  $('camera-zoom')?.addEventListener('input', (event) => update('zoom', event.target.value));
  $('reset-camera')?.addEventListener('click', () => {
    camera = { ...defaults };
    applyCamera();
    R.captureCurrent();
    A.status('Camera reset');
  });

  A.camera = {
    get state() { return A.clone(camera); },
    set(next) { camera = normalize(next); applyCamera(); R.captureCurrent(); },
    apply: applyCamera,
    reset() { camera = { ...defaults }; applyCamera(); R.captureCurrent(); }
  };
  applyCamera();
})();
