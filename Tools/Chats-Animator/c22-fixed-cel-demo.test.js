'use strict';
const assert = require('assert');
const core = require('./c22-fixed-cel-core.js');

const base = {
  background: { name: 'stage', src: 'bg' },
  calibration: {},
  selectedAssetId: 'gr',
  assets: [{
    id: 'gr',
    kind: 'character',
    name: 'base',
    src: 'pose-00',
    x: 0.5,
    groundY: 0.88,
    manualScale: 0.82
  }]
};

const poses = Array.from({ length: 12 }, (_, index) => `pose-${String(index + 1).padStart(2, '0')}`);
const snapshots = core.buildSnapshots(base, 'gr', poses);
const check = core.verifyFixedCelSnapshots(snapshots, 'gr');

assert.strictEqual(check.frameCount, 12);
assert.strictEqual(check.uniqueDrawings, 12, 'animation must use 12 distinct drawings');
assert.strictEqual(check.fixedTransform, true, 'demo must not animate by sliding the layer');

for (const snapshot of snapshots) {
  const asset = snapshot.assets.find((item) => item.id === 'gr');
  assert.strictEqual(asset.x, 0.5);
  assert.strictEqual(asset.groundY, 0.88);
  assert.strictEqual(asset.manualScale, 0.82);
}

console.log('PASS fixed-cel demo: drawings change while X/Y/scale remain fixed');
