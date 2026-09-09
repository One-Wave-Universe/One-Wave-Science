'use strict';

const assert = require('assert');
const { createWorkerServer, isPrivatePeer } = require('../compute-worker');

async function main() {
  assert.strictEqual(isPrivatePeer('127.0.0.1'), true);
  assert.strictEqual(isPrivatePeer('192.168.4.23'), true);
  assert.strictEqual(isPrivatePeer('10.0.0.7'), true);
  assert.strictEqual(isPrivatePeer('8.8.8.8'), false);

  const server = createWorkerServer({ bind: '127.0.0.1', port: 0, privateOnly: false });
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });

  try {
    const { port } = server.address();
    const base = `http://127.0.0.1:${port}`;

    const healthRes = await fetch(`${base}/health`);
    const health = await healthRes.json();
    assert.strictEqual(healthRes.status, 200);
    assert.strictEqual(health.ok, true);
    assert.strictEqual(health.service, 'one-wave-vbb-compute');
    assert.strictEqual(health.protocol, 1);

    const elements = {
      wires: [],
      components: [
        { id: 'bat', type: 'battery', a: 'vcc', b: 'gnd', value: 5 },
        { id: 'r1', type: 'resistor', a: 'vcc', b: 'mid', value: 1000 },
        { id: 'r2', type: 'resistor', a: 'mid', b: 'gnd', value: 1000 },
      ],
    };

    const solveRes = await fetch(`${base}/v1/solve`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ sessionId: 'divider-test', elements, dt: 1 / 1000 }),
    });
    const solved = await solveRes.json();
    assert.strictEqual(solveRes.status, 200);
    assert.strictEqual(solved.ok, true);

    const root = solved.result.roots.mid || 'mid';
    const midV = solved.result.voltages[root];
    assert.ok(Number.isFinite(midV), `midpoint voltage missing: ${JSON.stringify(solved.result.voltages)}`);
    assert.ok(Math.abs(midV - 2.5) < 0.05, `expected ~2.5V midpoint, got ${midV}V`);

    const resetRes = await fetch(`${base}/v1/reset`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ sessionId: 'divider-test' }),
    });
    assert.strictEqual(resetRes.status, 200);

    console.log('PASS: Jetson compute worker health + ordinary 5V resistor-divider solve');
  } finally {
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
