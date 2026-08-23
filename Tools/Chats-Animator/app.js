(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const readFile = (file) => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
  const clone = (value) => JSON.parse(JSON.stringify(value));
  const uid = (prefix = 'id') => `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;

  const state = {
    background: null,
    calibration: { horizonY: 0.36, farY: 0.48, nearY: 0.92, nearScale: 1.0, farScale: 0.35 },
    assets: [],
    selectedAssetId: null,
    calibrationVisible: false,
    placementMode: false
  };

  function status(message) {
    const el = $('runtime-status');
    if (el) el.textContent = message;
  }

  function autoScaleFor(asset) {
    const c = state.calibration;
    const span = Math.max(0.001, c.nearY - c.farY);
    const t = Math.max(0, Math.min(1, (asset.groundY - c.farY) / span));
    return c.farScale + (c.nearScale - c.farScale) * t;
  }

  function renderCalibration() {
    const overlay = $('calibration-overlay');
    if (!overlay) return;
    const visible = state.calibrationVisible || state.placementMode;
    overlay.hidden = !visible;
    if (!visible) return;
    const c = state.calibration;
    const y = (v) => (v * 100).toFixed(2);
    overlay.innerHTML = `<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
      <line class="horizon-line" x1="0" y1="${y(c.horizonY)}" x2="100" y2="${y(c.horizonY)}" />
      <line class="grid-line" x1="0" y1="${y(c.farY)}" x2="100" y2="${y(c.farY)}" />
      <line class="edge-line" x1="0" y1="${y(c.nearY)}" x2="100" y2="${y(c.nearY)}" />
      <line class="grid-line" x1="0" y1="${y(c.farY)}" x2="50" y2="${y(c.horizonY)}" />
      <line class="grid-line" x1="100" y1="${y(c.farY)}" x2="50" y2="${y(c.horizonY)}" />
      <line class="grid-line" x1="0" y1="${y(c.nearY)}" x2="50" y2="${y(c.horizonY)}" />
      <line class="grid-line" x1="100" y1="${y(c.nearY)}" x2="50" y2="${y(c.horizonY)}" />
    </svg>`;
  }

  function renderBackground() {
    const img = $('scene-background');
    const placeholder = $('background-placeholder');
    if (!img) return;
    if (state.background?.src) {
      img.src = state.background.src;
      img.hidden = false;
      if (placeholder) placeholder.hidden = true;
      if ($('background-meta')) $('background-meta').textContent = state.background.name || 'Background loaded';
    } else {
      img.removeAttribute('src');
      img.hidden = true;
      if (placeholder) placeholder.hidden = false;
      if ($('background-meta')) $('background-meta').textContent = 'No background loaded';
    }
  }

  function selectAsset(id) {
    state.selectedAssetId = id || null;
    renderAssets();
    renderSelectedControls();
  }

  function renderAssets() {
    const layer = $('asset-layer');
    if (!layer) return;
    layer.innerHTML = '';
    for (const asset of state.assets) {
      const img = document.createElement('img');
      img.className = `scene-asset${asset.id === state.selectedAssetId ? ' selected' : ''}`;
      img.src = asset.src;
      img.alt = asset.name || asset.kind;
      img.dataset.assetId = asset.id;
      const scale = autoScaleFor(asset) * asset.manualScale;
      img.style.left = `${asset.x * 100}%`;
      img.style.top = `${asset.groundY * 100}%`;
      img.style.height = `${Math.max(5, 42 * scale)}%`;
      img.style.transform = 'translate(-50%, -100%)';
      img.style.zIndex = String(10 + Math.round(asset.groundY * 100));
      img.addEventListener('click', (event) => {
        event.stopPropagation();
        selectAsset(asset.id);
      });
      layer.appendChild(img);
    }
  }

  function renderSelectedControls() {
    const asset = state.assets.find((a) => a.id === state.selectedAssetId);
    const none = $('no-selection');
    const controls = $('selected-controls');
    if (!asset) {
      if (none) none.hidden = false;
      if (controls) controls.hidden = true;
      return;
    }
    if (none) none.hidden = true;
    if (controls) controls.hidden = false;
    if ($('selected-name')) $('selected-name').textContent = `${asset.kind}: ${asset.name}`;
    const pairs = [
      ['asset-x', 'asset-x-value', asset.x],
      ['asset-ground-y', 'asset-ground-y-value', asset.groundY],
      ['asset-manual-scale', 'asset-manual-scale-value', asset.manualScale]
    ];
    for (const [inputId, valueId, value] of pairs) {
      if ($(inputId)) $(inputId).value = value;
      if ($(valueId)) $(valueId).textContent = Number(value).toFixed(2);
    }
    if ($('auto-scale-value')) $('auto-scale-value').textContent = autoScaleFor(asset).toFixed(2);
  }

  function renderAll() {
    renderBackground();
    renderCalibration();
    renderAssets();
    renderSelectedControls();
  }

  async function addAssetFromFile(file, kind) {
    const src = await readFile(file);
    const asset = { id: uid(kind), kind, name: file.name, src, x: 0.5, groundY: 0.72, manualScale: 1.0 };
    state.assets.push(asset);
    state.selectedAssetId = asset.id;
    renderAll();
    window.Animator?.reel?.captureCurrent?.();
    status(`${kind} added`);
  }

  function bindRange(inputId, valueId, key, target = state.calibration) {
    const input = $(inputId);
    if (!input) return;
    input.value = target[key];
    const sync = () => {
      target[key] = Number(input.value);
      if ($(valueId)) $(valueId).textContent = Number(input.value).toFixed(2);
      renderAll();
      window.Animator?.reel?.captureCurrent?.();
    };
    input.addEventListener('input', sync);
    sync();
  }

  $('load-background')?.addEventListener('click', () => $('background-picker')?.click());
  $('background-picker')?.addEventListener('change', async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    state.background = { name: file.name, src: await readFile(file) };
    renderAll();
    window.Animator?.reel?.captureCurrent?.();
    status('Background loaded');
    event.target.value = '';
  });
  $('clear-background')?.addEventListener('click', () => {
    state.background = null;
    renderAll();
    window.Animator?.reel?.captureCurrent?.();
    status('Background removed');
  });
  $('toggle-calibration')?.addEventListener('click', () => {
    state.calibrationVisible = !state.calibrationVisible;
    renderCalibration();
  });
  $('save-calibration')?.addEventListener('click', () => {
    state.calibrationVisible = false;
    if ($('calibration-state')) $('calibration-state').textContent = 'Calibration saved';
    renderAll();
    window.Animator?.reel?.captureCurrent?.();
    status('Calibration saved');
  });
  $('toggle-placement')?.addEventListener('click', () => {
    state.placementMode = !state.placementMode;
    renderCalibration();
    status(state.placementMode ? 'Placement / sizing mode' : 'Placement finished');
  });
  $('add-character')?.addEventListener('click', () => $('character-picker')?.click());
  $('add-prop')?.addEventListener('click', () => $('prop-picker')?.click());
  $('character-picker')?.addEventListener('change', async (event) => {
    const file = event.target.files?.[0];
    if (file) await addAssetFromFile(file, 'character');
    event.target.value = '';
  });
  $('prop-picker')?.addEventListener('change', async (event) => {
    const file = event.target.files?.[0];
    if (file) await addAssetFromFile(file, 'prop');
    event.target.value = '';
  });
  $('remove-selected')?.addEventListener('click', () => {
    if (!state.selectedAssetId) return;
    state.assets = state.assets.filter((a) => a.id !== state.selectedAssetId);
    state.selectedAssetId = null;
    renderAll();
    window.Animator?.reel?.captureCurrent?.();
    status('Selected asset removed');
  });

  for (const [id, valueId, prop] of [
    ['asset-x', 'asset-x-value', 'x'],
    ['asset-ground-y', 'asset-ground-y-value', 'groundY'],
    ['asset-manual-scale', 'asset-manual-scale-value', 'manualScale']
  ]) {
    $(id)?.addEventListener('input', (event) => {
      const asset = state.assets.find((a) => a.id === state.selectedAssetId);
      if (!asset) return;
      asset[prop] = Number(event.target.value);
      if ($(valueId)) $(valueId).textContent = asset[prop].toFixed(2);
      renderAssets();
      renderSelectedControls();
      window.Animator?.reel?.captureCurrent?.();
    });
  }

  bindRange('horizon-y', 'horizon-y-value', 'horizonY');
  bindRange('ground-far-y', 'ground-far-y-value', 'farY');
  bindRange('ground-near-y', 'ground-near-y-value', 'nearY');
  bindRange('near-scale', 'near-scale-value', 'nearScale');
  bindRange('far-scale', 'far-scale-value', 'farScale');
  $('scene-stage')?.addEventListener('click', () => selectAsset(null));

  window.Animator = {
    state,
    clone,
    uid,
    readFile,
    status,
    autoScaleFor,
    renderAll,
    renderAssets,
    renderSelectedControls,
    selectAsset,
    snapshot() {
      return clone({ background: state.background, calibration: state.calibration, assets: state.assets, selectedAssetId: state.selectedAssetId });
    },
    restore(snapshot) {
      state.background = clone(snapshot.background ?? null);
      state.calibration = clone(snapshot.calibration ?? state.calibration);
      state.assets = clone(snapshot.assets ?? []);
      state.selectedAssetId = snapshot.selectedAssetId ?? null;
      renderAll();
    }
  };

  renderAll();
})();
