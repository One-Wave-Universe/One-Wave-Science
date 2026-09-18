(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  const Core = window.AnimatorFixedCelCore;
  if (!A || !R || !Core) throw new Error('Fixed-cel demo requires Animator + reel + core');

  const SHEET_URL = '../../Assets/Goblin_Raccoon/gr-walk-right-12-cel-sheet.svg';
  const ROWS = 3;
  const COLS = 4;
  const HOLD = 2;
  const FIXED_PLACEMENT = { x: 0.50, groundY: 0.88, manualScale: 0.82 };

  function loadImage(src) {
    return new Promise((resolve, reject) => {
      const image = new Image();
      image.onload = () => resolve(image);
      image.onerror = () => reject(new Error(`Could not load ${src}`));
      image.src = src;
    });
  }

  async function sliceSheet(url) {
    const image = await loadImage(url);
    const cellW = Math.floor(image.naturalWidth / COLS);
    const cellH = Math.floor(image.naturalHeight / ROWS);
    if (!cellW || !cellH) throw new Error('Invalid 12-cel sheet geometry');
    const poses = [];
    for (let index = 0; index < ROWS * COLS; index += 1) {
      const row = Math.floor(index / COLS);
      const col = index % COLS;
      const canvas = document.createElement('canvas');
      canvas.width = cellW;
      canvas.height = cellH;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(image, col * cellW, row * cellH, cellW, cellH, 0, 0, cellW, cellH);
      poses.push(canvas.toDataURL('image/png'));
    }
    return poses;
  }

  function demoBackground() {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720">
      <rect width="1280" height="720" fill="#14241d"/>
      <rect y="455" width="1280" height="265" fill="#26392d"/>
      <path d="M0 520 C260 470 430 560 650 510 S1030 470 1280 540" fill="none" stroke="#71856d" stroke-width="90"/>
      <path d="M0 520 C260 470 430 560 650 510 S1030 470 1280 540" fill="none" stroke="#b0a078" stroke-width="54"/>
      <text x="42" y="68" fill="#d9e5d6" font-family="sans-serif" font-size="28">Fixed-cel acceptance stage — drawing changes, position does not</text>
    </svg>`;
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  }

  async function loadDemo() {
    const poses = await sliceSheet(SHEET_URL);
    A.state.assets = [];
    A.state.selectedAssetId = null;
    A.setBackgroundFromSource(demoBackground(), 'Fixed Cel Acceptance Stage');
    const asset = A.addAssetFromSource(poses[0], 'character', 'GR Walk Cel 01', FIXED_PLACEMENT);
    const base = A.snapshot();
    const snapshots = Core.buildSnapshots(base, asset.id, poses);
    const check = Core.verifyFixedCelSnapshots(snapshots, asset.id);
    if (!check.fixedTransform || check.uniqueDrawings !== 12) throw new Error('Fixed-cel acceptance invariant failed');
    const frames = snapshots.map((snapshot) => R.makeFrame(snapshot, HOLD));
    R.setFrames(frames, 0);
    const fps = document.getElementById('fps-control');
    if (fps) {
      fps.value = '24';
      fps.dispatchEvent(new Event('input', { bubbles: true }));
    }
    A.status('12-cel demo ready: 12 changing drawings, fixed X/Y/scale, 24 FPS on 2s');
    return check;
  }

  document.getElementById('load-fixed-cel-demo')?.addEventListener('click', () => {
    loadDemo().catch((error) => {
      console.error(error);
      A.status(`Fixed-cel demo failed: ${error.message}`);
    });
  });

  A.fixedCelDemo = { loadDemo, sliceSheet, SHEET_URL, ROWS, COLS, HOLD, FIXED_PLACEMENT };
})();
