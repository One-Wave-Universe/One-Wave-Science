#!/usr/bin/env node
/*
 * Perfboard physical/electrical netlist checks.
 * Board kinds differ only in physical netlist: kind=perf|perfboard isolates
 * every pad; wires still merge via circuit.js (same path as breadboard).
 */
const assert = require('assert');
const Board = require('../js/board.js');
const CircuitEngine = require('../js/circuit.js');

let checkCount = 0;
function check(name, condition, note) {
  checkCount++;
  const line = `${condition ? 'PASS' : 'FAIL'} [${name}]${note ? ' -- ' + note : ''}`;
  console.log(line);
  assert.ok(condition, `NETLIST CHECK FAILED: ${name}${note ? ' -- ' + note : ''}`);
}

console.log('=== Physical netlist: perfboard pads are isolated ===');
{
  const board = Board.build([{ size: 'large', kind: 'perf' }]);
  const nets = Board.netlist(board);
  const cols = board.boards[0].cols;
  const rowCount = 14;

  check('perf-boardKind-is-perf', board.boards[0].boardKind === 'perf',
    'build([{kind:"perf"}]) must record boardKind "perf" on the board meta');

  const allPadsAlone = nets.every((n) => n.holes.length === 1);
  check('perf-every-pad-is-its-own-net', allPadsAlone && nets.length === board.holes.length,
    `expected ${board.holes.length} singleton nets (one per hole), got ${nets.length} nets`);

  const a1 = Board.cellIdFor(0, 'a', 1, 'perf');
  const a2 = Board.cellIdFor(0, 'a', 2, 'perf');
  const b1 = Board.cellIdFor(0, 'b', 1, 'perf');
  check('perf-adjacent-row-pads-not-pre-tied', a1 !== a2,
    `${a1} and ${a2} must be different cellIds on a perfboard`);
  check('perf-adjacent-column-pads-not-pre-tied', a1 !== b1,
    `${a1} and ${b1} must be different cellIds (no a-e strip merge)`);

  const stripIds = ['a', 'b', 'c', 'd', 'e'].map((r) => Board.cellIdFor(0, r, 5, 'perf'));
  check('perf-no-ae-strip-merge', new Set(stripIds).size === 5,
    `a5..e5 must be 5 cellIds on perf, got [${stripIds.join(', ')}]`);
  const bottomIds = ['f', 'g', 'h', 'i', 'j'].map((r) => Board.cellIdFor(0, r, 5, 'perf'));
  check('perf-no-fj-strip-merge', new Set(bottomIds).size === 5,
    `f5..j5 must be 5 cellIds on perf, got [${bottomIds.join(', ')}]`);

  const railIds = [];
  for (let col = 1; col <= Math.min(cols, 8); col++) railIds.push(Board.cellIdFor(0, 'railTP', col, 'perf'));
  check('perf-no-continuous-rail-merge', new Set(railIds).size === railIds.length,
    'each railTP hole must be its own pad, not one board-wide railTP net');

  const alias = Board.build([{ size: 'small', kind: 'perfboard' }]);
  check('perfboard-alias-normalizes-to-perf', alias.boards[0].boardKind === 'perf',
    'kind:"perfboard" is an alias for kind:"perf"');

  const seenXY = new Set();
  const seenRowCol = new Set();
  let uniqueHoles = true;
  for (const h of board.holes) {
    const xy = h.x + ',' + h.y;
    const rc = h.boardIdx + ':' + h.row + ':' + h.col;
    if (seenXY.has(xy) || seenRowCol.has(rc)) uniqueHoles = false;
    seenXY.add(xy);
    seenRowCol.add(rc);
  }
  check('perf-one-lead-per-hole-geometry', uniqueHoles && seenXY.size === board.holes.length,
    'each physical hole must remain a unique placement target (one lead per hole)');
  check('perf-hole-count-matches-grid', board.holes.length === cols * rowCount,
    `large perfboard should have ${cols * rowCount} holes, got ${board.holes.length}`);
}

console.log('\n=== Electrical netlist: jumper merges perf pads the same way ===');
{
  const padA = Board.cellIdFor(0, 'a', 1, 'perf');
  const padB = Board.cellIdFor(0, 'a', 2, 'perf');
  check('setup-perf-pads-are-distinct', padA !== padB, 'sanity: adjacent perf pads start separate');

  const elsNoJumper = { wires: [], components: [
    { id: 'r1', type: 'resistor', value: 1000, a: padA, b: padB },
  ] };
  const netsNoJumper = CircuitEngine.netlist(elsNoJumper);
  const rootA0 = netsNoJumper.find((n) => n.nodes.includes(padA)).root;
  const rootB0 = netsNoJumper.find((n) => n.nodes.includes(padB)).root;
  check('perf-resistor-does-not-merge-pads', rootA0 !== rootB0,
    'a resistor must not merge two perf pads the way a wire does');

  const elsWithJumper = { wires: [{ a: padA, b: padB }], components: [
    { id: 'r1', type: 'resistor', value: 1000, a: padA, b: 'other' },
  ] };
  const netsWithJumper = CircuitEngine.netlist(elsWithJumper);
  const jumperNet = netsWithJumper.find((n) => n.nodes.includes(padA));
  check('perf-jumper-merges-exactly-two-pads', jumperNet.nodes.includes(padB) && jumperNet.nodes.length === 2,
    `jumper between ${padA} and ${padB} must merge exactly those two pads, got [${jumperNet.nodes.join(', ')}]`);
  const otherNet = netsWithJumper.find((n) => n.nodes.includes('other'));
  check('perf-jumper-does-not-touch-unrelated', otherNet.nodes.length === 1 && !otherNet.nodes.includes(padA),
    'unrelated node must stay untouched after a perfboard jumper merge');
}

console.log(`\n=== ALL ${checkCount} PERFBOARD NETLIST CHECKS PASSED ===`);
