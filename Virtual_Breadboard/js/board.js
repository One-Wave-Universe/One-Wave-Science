/*
 * Breadboard geometry: one or more real full-size/half-size (830/400-point
 * style) solderless breadboards — each with two power rails top and bottom,
 * and two 5-row terminal-strip banks (a-e / f-j) split by a center channel.
 *
 * Electrically (this is what makes the simulator "real"):
 *   - Each power rail is ONE continuous node running the full length of
 *     its own board — a small board's rails are NOT the same node as a
 *     different board's rails, exactly like two physical boards on a
 *     desk. Bridge them with an ordinary jumper wire (or share a supply
 *     across them) if you want them tied together.
 *   - Each column's five holes in the top bank (rows a-e) are tied together.
 *   - Each column's five holes in the bottom bank (rows f-j) are tied
 *     together, but NOT to the top bank of the same column — the center
 *     channel is a real gap components straddle to cross it.
 */
(function (root) {
  'use strict';

  const BOARD_SIZES = {
    large: { cols: 63, label: 'Large (63-col)' },
    small: { cols: 30, label: 'Small (30-col)' },
  };
  const HOLE = 16;
  const GROUP_GAP = 7; // extra breathing room every 5 columns, like a real board
  const MARGIN = 40;
  const BOARD_GAP_X = 46; // gap between adjacent boards on the same row
  const BOARD_GAP_Y = 34; // gap between rows of boards
  const MAX_BOARDS_PER_ROW = 2;

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

  function xForColLocal(col) {
    return (col - 1) * HOLE + Math.floor((col - 1) / 5) * GROUP_GAP;
  }

  function localWidth(cols) {
    return xForColLocal(cols) + HOLE;
  }

  function cellIdFor(boardIdx, rowId, col) {
    const b = 'b' + boardIdx + ':';
    if (rowId === 'railTP' || rowId === 'railTM' || rowId === 'railBP' || rowId === 'railBM') return b + rowId;
    if (rowId === 'a' || rowId === 'b' || rowId === 'c' || rowId === 'd' || rowId === 'e') return b + 'T' + col;
    return b + 'B' + col;
  }

  // build one board's holes/rows at a local origin (0,0); the caller shifts
  // them into place once the overall grid layout is known
  function buildOne(boardIdx, cols) {
    const holes = [];
    const rows = [];
    let y = 0;
    ROW_DEFS.forEach((rd) => {
      y += GAP_BEFORE[rd.id] || 0;
      const rowInfo = { ...rd, y, boardIdx };
      rows.push(rowInfo);
      for (let col = 1; col <= cols; col++) {
        holes.push({
          x: xForColLocal(col),
          y,
          row: rd.id,
          col,
          kind: rd.kind,
          boardIdx,
          cellId: cellIdFor(boardIdx, rd.id, col),
        });
      }
      y += HOLE;
    });
    const width = localWidth(cols);
    const height = y - HOLE;
    return { holes, rows, width, height, cols };
  }

  /**
   * layout = [{size:'large'|'small'}, ...] — one entry per physical board,
   * laid out left-to-right wrapping into rows. Defaults to a single large
   * board (today's classic single-breadboard layout).
   */
  function build(layout) {
    const specs = layout && layout.length ? layout : [{ size: 'large' }];
    const built = specs.map((s, i) => buildOne(i, (BOARD_SIZES[s.size] || BOARD_SIZES.large).cols));

    const perRow = specs.length > 2 ? MAX_BOARDS_PER_ROW : specs.length;
    const boardsMeta = [];
    let rowX = MARGIN;
    let rowY = MARGIN;
    let rowMaxH = 0;
    let overallW = 0;
    built.forEach((b, i) => {
      if (i > 0 && i % perRow === 0) {
        rowX = MARGIN;
        rowY += rowMaxH + BOARD_GAP_Y;
        rowMaxH = 0;
      }
      boardsMeta.push({ boardIdx: i, xOffset: rowX, yOffset: rowY, width: b.width, height: b.height, cols: b.cols, rows: b.rows.map((r) => ({ ...r, y: r.y + rowY })) });
      rowX += b.width + BOARD_GAP_X;
      rowMaxH = Math.max(rowMaxH, b.height);
      overallW = Math.max(overallW, rowX - BOARD_GAP_X);
    });
    const overallH = rowY + rowMaxH;

    const holes = [];
    const rows = [];
    built.forEach((b, i) => {
      const meta = boardsMeta[i];
      b.holes.forEach((h) => holes.push({ ...h, x: h.x + meta.xOffset, y: h.y + meta.yOffset }));
      b.rows.forEach((r) => rows.push({ ...r, y: r.y + meta.yOffset }));
    });

    return {
      holes,
      rows,
      width: overallW + MARGIN,
      height: overallH + MARGIN,
      boards: boardsMeta,
    };
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
    const highlightSet = opts.highlightSet || null; // Set of cellIds sharing the hovered node

    ctx.save();
    ctx.fillStyle = '#0d1017';
    ctx.fillRect(0, 0, board.width, board.height);

    board.boards.forEach((meta) => {
      const x0 = meta.xOffset - MARGIN / 2;
      const y0 = meta.yOffset - MARGIN / 2;
      const w = meta.width + MARGIN;
      const h = meta.height + MARGIN;

      ctx.fillStyle = '#eef1e8';
      ctx.fillRect(x0, y0, w, h);
      ctx.strokeStyle = '#c9cdbd';
      ctx.lineWidth = 2;
      ctx.strokeRect(x0 + 1, y0 + 1, w - 2, h - 2);

      meta.rows.forEach((rd) => {
        if (rd.kind === 'rail') {
          ctx.strokeStyle = rd.color;
          ctx.globalAlpha = 0.55;
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(meta.xOffset - 14, rd.y);
          ctx.lineTo(meta.xOffset + meta.width + 14, rd.y);
          ctx.stroke();
          ctx.globalAlpha = 1;
          ctx.fillStyle = rd.color;
          ctx.font = 'bold 11px monospace';
          ctx.fillText(rd.label, x0 + 10, rd.y + 4);
          ctx.fillText(rd.label, x0 + w - 20, rd.y + 4);
        }
      });

      const eRow = meta.rows.find((r) => r.id === 'e');
      const fRow = meta.rows.find((r) => r.id === 'f');
      if (eRow && fRow) {
        ctx.fillStyle = '#aab0a0';
        ctx.font = '9px monospace';
        ctx.fillText('center channel', meta.xOffset + meta.width / 2 - 34, (eRow.y + fRow.y) / 2 + 3);
      }

      const topStripRow = meta.rows.find((r) => r.id === 'a');
      if (topStripRow) {
        ctx.fillStyle = '#8b9080';
        ctx.font = '9px monospace';
        for (let col = 5; col <= meta.cols; col += 5) {
          const x = meta.xOffset + xForColLocal(col);
          ctx.fillText(String(col), x - 4, topStripRow.y - 6);
        }
      }

      meta.rows.forEach((rd) => {
        if (rd.kind === 'strip') {
          ctx.fillStyle = '#8b9080';
          ctx.font = '9px monospace';
          ctx.fillText(rd.id, meta.xOffset - 24, rd.y + 3);
        }
      });
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
      // draw a faint tie line across each contiguous strip group being
      // highlighted -- grouped per board+row so a jumper tying two boards'
      // nodes together doesn't draw a phantom line through the gap between them
      const byRowBank = {};
      for (const h of board.holes) {
        if (!highlightSet.has(h.cellId)) continue;
        const key = h.boardIdx + ':' + h.row;
        byRowBank[key] = byRowBank[key] || [];
        byRowBank[key].push(h);
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

  const api = { BOARD_SIZES, HOLE, MARGIN, build, hitTest, holeAt, cellIdFor, draw };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.Board = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
