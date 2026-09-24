#!/usr/bin/env node
/*
 * Netlist truth tests -- makes breadboard connectivity itself inspectable
 * and testable, per the review that flagged "every tied strip, split
 * rail, ground/reference and center gap has to behave exactly like
 * physical hardware" as needing hard validation, not just plausible-
 * looking behavior.
 *
 * Two separate, independently-checkable netlists:
 *   - Board.netlist(board)   -- the PHYSICAL topology: what a bare board
 *     itself ties together (strips, rails, the center trench), with no
 *     components or jumpers involved at all.
 *   - CircuitEngine.netlist(elements) -- the ELECTRICAL topology: what a
 *     real placed circuit (components + wires) actually ties together,
 *     including any jumpers -- built from the exact same union-find
 *     construction js/circuit.js's own solve() uses, extracted so it can
 *     be inspected without running a full numeric solve.
 *
 * No eyeballing: every check is a real assertion on the netlist's actual
 * grouping, not a rendered picture of one.
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

function netOf(nets, cellId) {
  return nets.find((n) => n.cellId === cellId);
}

console.log('=== Physical netlist: single large board ===');
{
  const board = Board.build([{ size: 'large' }]);
  const nets = Board.netlist(board);
  const cols = board.boards[0].cols;

  // 1. Five holes on one strip really become one net -- checked for
  // EVERY column in both banks, not just a spot check.
  let allStripsHaveFive = true;
  for (let col = 1; col <= cols; col++) {
    const top = netOf(nets, `b0:T${col}`);
    const bottom = netOf(nets, `b0:B${col}`);
    if (!top || top.holes.length !== 5) allStripsHaveFive = false;
    if (!bottom || bottom.holes.length !== 5) allStripsHaveFive = false;
  }
  check('every-column-top-and-bottom-strip-has-exactly-5-holes', allStripsHaveFive,
    `checked all ${cols} columns in both banks`);

  // 2. The center trench does not connect -- no top-bank cellId ever
  // equals a bottom-bank cellId, for any column.
  let trenchNeverConnects = true;
  for (let col = 1; col <= cols; col++) {
    if (`b0:T${col}` === `b0:B${col}`) trenchNeverConnects = false;
    const top = netOf(nets, `b0:T${col}`);
    const bottom = netOf(nets, `b0:B${col}`);
    const topRows = new Set(top.holes.map((h) => h.row));
    const bottomRows = new Set(bottom.holes.map((h) => h.row));
    for (const r of topRows) if (bottomRows.has(r)) trenchNeverConnects = false;
  }
  check('center-trench-never-connects-top-and-bottom-banks', trenchNeverConnects,
    'no column\'s top-bank net shares a cellId or a row with its own bottom-bank net');

  // 3. Split power rails remain split -- the four rails are four
  // genuinely distinct nets, and no rail's holes leak into a strip net.
  const rails = ['b0:railTP', 'b0:railTM', 'b0:railBP', 'b0:railBM'];
  const railNets = rails.map((id) => netOf(nets, id));
  check('four-power-rails-all-present', railNets.every((n) => n != null), 'railTP/railTM/railBP/railBM must each exist as their own net');
  const railRoots = new Set(railNets.map((n) => n.cellId));
  check('four-power-rails-are-four-distinct-nets', railRoots.size === 4,
    'top +/- and bottom +/- must be four genuinely separate nets, never merged with each other');
  check('each-rail-spans-the-full-board-width', railNets.every((n) => n.holes.length === cols),
    `each rail must tie all ${cols} columns together as one continuous node`);

  // 4. A strip column is never accidentally part of a rail net.
  const stripCellIds = new Set(nets.filter((n) => n.kind === 'strip').map((n) => n.cellId));
  const railCellIds = new Set(nets.filter((n) => n.kind === 'rail').map((n) => n.cellId));
  let noOverlap = true;
  for (const id of stripCellIds) if (railCellIds.has(id)) noOverlap = false;
  check('strip-nets-and-rail-nets-never-overlap', noOverlap, 'a terminal-strip column must never be the same net as a power rail');
}

console.log('\n=== Physical netlist: two boards never share a rail ===');
{
  const board = Board.build([{ size: 'large' }, { size: 'small' }]);
  const nets = Board.netlist(board);
  const b0railTP = netOf(nets, 'b0:railTP');
  const b1railTP = netOf(nets, 'b1:railTP');
  check('two-boards-both-have-their-own-railTP', b0railTP != null && b1railTP != null, 'both boards must each have their own + rail net');
  check('two-boards-rails-are-different-nets', b0railTP.cellId !== b1railTP.cellId,
    'board 0\'s + rail and board 1\'s + rail must be genuinely different nodes -- two physical boards on a desk are not tied together unless a real jumper bridges them');
  const b0col1 = netOf(nets, 'b0:T1');
  const b1col1 = netOf(nets, 'b1:T1');
  check('two-boards-same-numbered-column-still-different-nets', b0col1.cellId !== b1col1.cellId,
    'board 0 column 1 and board 1 column 1 must not be confused with each other just because they share a column number');
}

console.log('\n=== Electrical netlist: jumpers create exactly the intended connections ===');
{
  const board = Board.build([{ size: 'large' }]);
  const physicalNets = Board.netlist(board);
  // Two real, physically UNCONNECTED strip columns on the real board.
  const colA = 'b0:T1';
  const colB = 'b0:T5';
  check('setup-colA-and-colB-are-physically-separate', netOf(physicalNets, colA).cellId !== netOf(physicalNets, colB).cellId,
    'sanity check on the physical board before adding any jumper');

  // No jumper: the electrical netlist must keep them apart too.
  const elsNoJumper = { wires: [], components: [
    { id: 'r1', type: 'resistor', value: 1000, a: colA, b: colB },
  ] };
  const netsNoJumper = CircuitEngine.netlist(elsNoJumper);
  const rootA0 = netsNoJumper.find((n) => n.nodes.includes(colA)).root;
  const rootB0 = netsNoJumper.find((n) => n.nodes.includes(colB)).root;
  check('resistor-does-not-merge-its-own-two-terminals', rootA0 !== rootB0,
    'a resistor (or any two-terminal part) connects two real, different nodes -- it must never appear as a single merged net the way a wire does');

  // WITH a jumper: colA and colB must now be exactly one net, and nothing else changes.
  const elsWithJumper = { wires: [{ a: colA, b: colB }], components: [
    { id: 'r1', type: 'resistor', value: 1000, a: colA, b: 'other' },
  ] };
  const netsWithJumper = CircuitEngine.netlist(elsWithJumper);
  const jumperNet = netsWithJumper.find((n) => n.nodes.includes(colA));
  check('jumper-merges-exactly-the-two-intended-nodes', jumperNet.nodes.includes(colB) && jumperNet.nodes.length === 2,
    `a jumper between ${colA} and ${colB} must merge exactly those two node names into one net, got [${jumperNet.nodes.join(', ')}]`);
  const otherNet = netsWithJumper.find((n) => n.nodes.includes('other'));
  check('jumper-does-not-touch-unrelated-nodes', otherNet.nodes.length === 1 && !otherNet.nodes.includes(colA),
    'the resistor\'s other terminal must stay its own separate, untouched net');
}

console.log('\n=== Electrical netlist: closed switch merges, open switch does not ===');
{
  const els = (closed) => ({ wires: [], components: [
    { id: 'sw1', type: 'switch', a: 'x', b: 'y', closed },
  ] });
  const netsClosed = CircuitEngine.netlist(els(true));
  const netsOpen = CircuitEngine.netlist(els(false));
  const closedRootX = netsClosed.find((n) => n.nodes.includes('x')).root;
  const closedRootY = netsClosed.find((n) => n.nodes.includes('y')).root;
  const openRootX = netsOpen.find((n) => n.nodes.includes('x')).root;
  const openRootY = netsOpen.find((n) => n.nodes.includes('y')).root;
  check('closed-switch-merges-its-two-terminals', closedRootX === closedRootY, 'a real closed switch is electrically a wire');
  check('open-switch-keeps-terminals-separate', openRootX !== openRootY, 'a real open switch must NOT be reported as connected');
}

console.log('\n=== Electrical netlist: internal bookkeeping nodes are reported, but marked ===');
{
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 9, a: 'p', b: 'g' },
    { id: 'rref', type: 'resistor', value: 1e9, a: 'p', b: 'g' },
  ] };
  const nets = CircuitEngine.netlist(els);
  const internalNet = nets.find((n) => n.internalNodes.length > 0);
  check('internal-node-exists-and-is-marked', internalNet != null && internalNet.nodes.length === 0,
    'a battery\'s own hidden reference node must show up (so nothing is silently invisible) but never mixed into the list of real, placeable node names');
}

console.log(`\n=== ALL ${checkCount} NETLIST CHECKS PASSED ===`);
