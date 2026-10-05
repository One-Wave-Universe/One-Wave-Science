#!/usr/bin/env node
/*
 * AI explore loop: build → test → adjust → test again.
 * Canned model replies (no network) prove repair retries, offline
 * templates, and UI-supported-part filtering.
 *
 * Run: node test/ai-build.test.js
 */
'use strict';

const assert = require('assert');
const AI = require('../js/ai.js');

let passed = 0;
function ok(name) {
  passed++;
  console.log('PASS ' + name);
}

async function main() {
  {
    const led = AI.matchOfflineTemplate('build me an LED with a current-limiting resistor');
    assert.ok(led && led.name === 'led', 'LED template');
    assert.strictEqual(AI.validateSpec(led).ok, true, 'LED template validates');
    assert.strictEqual(AI.uiSupportErrors(led.parts).length, 0, 'LED template UI-ok');

    const div = AI.matchOfflineTemplate('simple voltage divider');
    assert.ok(div && div.name === 'divider', 'divider template');
    assert.strictEqual(AI.validateSpec(div).ok, true, 'divider validates');

    const rc = AI.matchOfflineTemplate('RC low-pass circuit please');
    assert.ok(rc && rc.name === 'rc', 'RC template');
    assert.strictEqual(AI.validateSpec(rc).ok, true, 'RC validates');

    assert.strictEqual(AI.matchOfflineTemplate('totally unrelated request'), null, 'no false match');
    ok('offline keyword templates (LED / divider / RC)');
  }

  {
    const bad = {
      parts: [
        { type: 'diffsource', value: 0.02, terminals: [{ row: 'a', col: 1 }, { row: 'a', col: 2 }] },
      ],
    };
    const v = AI.validateSpec(bad);
    assert.strictEqual(v.ok, true, 'diffsource still shape-valid for CLI/simulate.js');
    const ui = AI.uiSupportErrors(v.parts);
    assert.ok(ui.length >= 1, 'diffsource rejected for UI/Ask AI');
    assert.ok(/UI-supported|CLI-only/i.test(ui[0]), 'UI error mentions support');
    ok('UI-supported filter rejects CLI-only diffsource');
  }

  {
    const healthy = { status: 'MODELED', warnings: [], currents: { r1: 0.01 }, voltages: { n1: 5 } };
    assert.strictEqual(AI.receiptLooksBad(healthy), false);
    assert.ok(/currents:/.test(AI.summarizeReceipt(healthy)));

    const unhealthy = { warnings: ['Possible short / over-current on battery bat1'] };
    assert.strictEqual(AI.receiptLooksBad(unhealthy), true);
    ok('summarizeReceipt + receiptLooksBad');
  }

  {
    const goodSpec = AI.OFFLINE_TEMPLATES.led;
    const calls = [];
    const result = await AI.exploreBuild({
      userText: 'green LED with 220 ohm',
      maxAttempts: 3,
      callModel: async (prompt) => {
        calls.push(prompt);
        return JSON.stringify(goodSpec);
      },
      probe: async () => ({
        ok: true,
        errors: [],
        receipt: { status: 'MODELED', warnings: [], currents: { led1: 0.012 }, voltages: {} },
        summary: 'ok',
        committed: true,
      }),
    });
    assert.strictEqual(result.ok, true);
    assert.strictEqual(result.attempts, 1);
    assert.strictEqual(calls.length, 1);
    ok('explore succeeds on first good reply');
  }

  {
    const badRaw = JSON.stringify({
      parts: [{ type: 'diffsource', value: 0.1, terminals: [{ row: 'a', col: 1 }, { row: 'a', col: 2 }] }],
    });
    const goodSpec = AI.OFFLINE_TEMPLATES.divider;
    let n = 0;
    const prompts = [];
    const result = await AI.exploreBuild({
      userText: 'voltage divider',
      maxAttempts: 3,
      callModel: async (prompt) => {
        prompts.push(prompt);
        n++;
        return n === 1 ? badRaw : JSON.stringify(goodSpec);
      },
      probe: async (spec) => {
        assert.ok(spec.parts.every((p) => AI.UI_SUPPORTED_TYPES.has(p.type)));
        return {
          ok: true,
          errors: [],
          receipt: { status: 'MODELED', warnings: [], currents: { r1: 0.0045 }, voltages: { mid: 4.5 } },
          summary: AI.summarizeReceipt({ warnings: [], currents: { r1: 0.0045 }, voltages: { mid: 4.5 } }),
          committed: true,
        };
      },
    });
    assert.strictEqual(result.ok, true, 'repair should succeed');
    assert.strictEqual(result.attempts, 2, 'second attempt wins');
    assert.strictEqual(n, 2);
    assert.ok(/Previous JSON|Errors to fix|diffsource|UI-supported/i.test(prompts[1]), 'repair prompt carries errors');
    ok('explore repair loop: bad CLI-only reply then good divider');
  }

  {
    const almost = AI.OFFLINE_TEMPLATES.led;
    let n = 0;
    const result = await AI.exploreBuild({
      userText: 'LED circuit',
      maxAttempts: 3,
      callModel: async () => {
        n++;
        return JSON.stringify(almost);
      },
      probe: async () => {
        if (n === 1) {
          return {
            ok: false,
            errors: ['Simulation warnings: Possible short / over-current'],
            receipt: { warnings: ['Possible short / over-current'], currents: {}, voltages: {} },
            summary: 'warnings: short',
            committed: true,
          };
        }
        return {
          ok: true,
          errors: [],
          receipt: { warnings: [], currents: { led1: 0.01 }, voltages: {} },
          summary: 'clean',
          committed: true,
        };
      },
    });
    assert.strictEqual(result.ok, true);
    assert.strictEqual(result.attempts, 2);
    ok('explore repair loop: unhealthy receipt then clean');
  }

  {
    let n = 0;
    const result = await AI.exploreBuild({
      userText: 'broken',
      maxAttempts: 3,
      callModel: async () => {
        n++;
        return 'not json at all';
      },
      probe: async () => ({ ok: true, errors: [], receipt: { warnings: [] }, committed: true }),
    });
    assert.strictEqual(result.ok, false);
    assert.strictEqual(result.attempts, 3);
    assert.strictEqual(n, 3);
    ok('explore stops after 3 bad extracts');
  }

  {
    const msg = AI.buildRepairUserText('make an LED', { parts: [] }, ['parts empty'], 'warnings: none');
    assert.ok(msg.includes('Original request:'));
    assert.ok(msg.includes('make an LED'));
    assert.ok(msg.includes('parts empty'));
    assert.ok(msg.includes('ONLY revised JSON'));
    ok('buildRepairUserText includes request, errors, JSON-only instruction');
  }

  console.log('\nAll ' + passed + ' ai-build checks passed.');
}

main().catch((err) => {
  console.error('FAIL', err && err.stack ? err.stack : err);
  process.exit(1);
});
