/*
 * Breadboard geometry: a real full-size (830-point-style) solderless
 * breadboard layout — two power rails top and bottom, and two 5-row
 * terminal-strip banks (a-e / f-j) split by a center channel.
 *
 * Electrically (this is what makes the simulator "real"):
 *   - Each power rail is ONE continuous node running the full length.
 *   - Each column's five holes in the top bank (rows a-e) are tied together.
 *   - Each column's five holes in the bottom bank (rows f-j) are tied
 *     together, but NOT to the top bank of the same column — the center
 *     channel is a real gap components straddle to cross it.
 */
(function (root) {
  'use strict';

  const COLS = 63;
  const HOLE = 16;
  const GROUP_GAP = 7; // extra breathing room every 5 columns, like a real board
  const MARGIN = 40;

  const ROW_DEFS = [
    { id: 'railTP', kind: 'rail', label: '+', color: '#e0483f' },
    { id: 'railTM', kind: 'rail', label: '-', color: '#3f7fe0' },
    { id: 'a', kind: 'strip', bank: 'top' },
    { id: 'b', kind: 'strip', bank: 'top' },
    { id: 'c', kind: 'strip', bank: 'top' },
    { id: 'd', kind: 'strip', bank: 'top' },
    { id: 'e', kind: 'strip', bank: 'top' },
    { id: 'f', kind: 'strip', bank: 'bottom' },
    { id: 'g', kind: 'strip', bank: 'bottom' },
    { id: 'h', kind: 'strip', bank: 'bottom' },
    { id: 'i', kind: 'strip', bank: 'bottom' },
    { id: 'j', kind: 'strip', bank: 'bottom' },
    { id: 'railBP', kind: 'rail', label: '+', color: '#e0483f' },
    { id: 'railBM', kind: 'rail', label: '-', color: '#3f7fe0' },
  ];

  const GAP_BEFORE = { a: 16, f: 10, railBP: 16 };

  function xForCol(col) {
    return MARGIN + (col - 1) * HOLE + Math.floor((col - 1) / 5) * GROUP_GAP;
  }

  function cellIdFor(rowId, col) {
    if (rowId === 'railTP' || rowId === 'railTM' || rowId === 'railBP' || rowId === 'railBM') return rowId;
    if (rowId === 'a' || rowId === 'b' || rowId === 'c' || rowId === 'd' || rowId === 'e') return 'T' + col;
    return 'B' + col;
  }

  function build() {
    const holes = [];
    const rowsOut = [];
    let y = MARGIN;
    ROW_DEFS.forEach((rd) => {
      y += GAP_BEFORE[rd.id] || 0;
      const rowInfo = { ...rd, y };
      rowsOut.push(rowInfo);
      for (let col = 1; col <= COLS; col++) {
        holes.push({
          x: xForCol(col),
          y,
          row: rd.id,
          col,
          kind: rd.kind,
          cellId: cellIdFor(rd.id, col),
        });
      }
      y += HOLE;
    });
    const width = xForCol(COLS) + MARGIN;
    const height = y - HOLE + MARGIN;
    return { holes, rows: rowsOut, width, height };
  }

  function hitTest(board, px, py, radius) {
    radius = radius || 8;
    let best = null;
    let bestD = radius * radius;
    for (const h of board.holes) {
      const dx = h.x - px;
      const dy = h.y - py;
      const d = dx * dx + dy * dy;
      if (d <= bestD) {
        bestD = d;
        best = h;
      }
    }
    return best;
  }

  function holeAt(board, cellId, preferCol) {
    // find a representative hole for a cellId (used for drawing component legs
    // when we only know the logical node, e.g. hover highlight of a rail)
    let candidates = board.holes.filter((h) => h.cellId === cellId);
    if (preferCol != null) {
      candidates = candidates.sort((a, b) => Math.abs(a.col - preferCol) - Math.abs(b.col - preferCol));
    }
    return candidates[0];
  }

  function draw(ctx, board, opts) {
    opts = opts || {};
    const highlightCellId = opts.highlightCellId || null;
    const highlightSet = opts.highlightSet || null; // Set of cellIds sharing the hovered node

    ctx.save();
    ctx.fillStyle = '#eef1e8';
    ctx.fillRect(0, 0, board.width, board.height);

    // subtle board texture / border
    ctx.strokeStyle = '#c9cdbd';
    ctx.lineWidth = 2;
    ctx.strokeRect(1, 1, board.width - 2, board.height - 2);

    // rail color guide lines
    board.rows.forEach((rd) => {
      if (rd.kind === 'rail') {
        ctx.strokeStyle = rd.color;
        ctx.globalAlpha = 0.55;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(MARGIN - 14, rd.y);
        ctx.lineTo(board.width - MARGIN + 14, rd.y);
        ctx.stroke();
        ctx.globalAlpha = 1;
        ctx.fillStyle = rd.color;
        ctx.font = 'bold 11px monospace';
        ctx.fillText(rd.label, 14, rd.y + 4);
        ctx.fillText(rd.label, board.width - 24, rd.y + 4);
      }
    });

    // center channel label
    const eRow = board.rows.find((r) => r.id === 'e');
    const fRow = board.rows.find((r) => r.id === 'f');
    if (eRow && fRow) {
      ctx.fillStyle = '#aab0a0';
      ctx.font = '9px monospace';
      ctx.fillText('center channel', board.width / 2 - 34, (eRow.y + fRow.y) / 2 + 3);
    }

    // column numbers every 5
    const topStripRow = board.rows.find((r) => r.id === 'a');
    if (topStripRow) {
      ctx.fillStyle = '#8b9080';
      ctx.font = '9px monospace';
      for (let col = 5; col <= COLS; col += 5) {
        const x = xForCol(col);
        ctx.fillText(String(col), x - 4, topStripRow.y - 6);
      }
    }

    // row labels (a-j) on the left edge
    board.rows.forEach((rd) => {
      if (rd.kind === 'strip') {
        ctx.fillStyle = '#8b9080';
        ctx.font = '9px monospace';
        ctx.fillText(rd.id, MARGIN - 24, rd.y + 3);
      }
    });

    // holes
    for (const h of board.holes) {
      const isHighlighted = highlightSet && highlightSet.has(h.cellId);
      ctx.beginPath();
      ctx.arc(h.x, h.y, isHighlighted ? 3.6 : 2.6, 0, Math.PI * 2);
      if (isHighlighted) {
        ctx.fillStyle = '#ffb020';
      } else if (h.kind === 'rail') {
        ctx.fillStyle = '#7d8272';
      } else {
        ctx.fillStyle = '#5b5f52';
      }
      ctx.fill();
    }

    if (highlightSet && highlightSet.size) {
      ctx.strokeStyle = 'rgba(255,176,32,0.55)';
      ctx.lineWidth = 6;
      ctx.lineCap = 'round';
      // draw a faint tie line across each contiguous strip group being highlighted
      const byRowBank = {};
      for (const h of board.holes) {
        if (!highlightSet.has(h.cellId)) continue;
        byRowBank[h.row] = byRowBank[h.row] || [];
        byRowBank[h.row].push(h);
      }
      Object.values(byRowBank).forEach((list) => {
        if (list.length < 2) return;
        list.sort((a, b) => a.x - b.x);
        ctx.globalAlpha = 0.35;
        ctx.beginPath();
        ctx.moveTo(list[0].x, list[0].y);
        ctx.lineTo(list[list.length - 1].x, list[list.length - 1].y);
        ctx.stroke();
        ctx.globalAlpha = 1;
      });
    }

    ctx.restore();
  }

  const api = { COLS, HOLE, MARGIN, build, hitTest, holeAt, cellIdFor, draw, xForCol };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.Board = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
