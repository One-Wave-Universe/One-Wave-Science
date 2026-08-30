/*
 * Component palette: what can be placed on the board, its electrical
 * defaults, and how to draw it. Bodies are drawn semi-transparent so the
 * board holes and leads underneath stay visible ("clear and visible" parts).
 *
 * Every draw*() function takes a trailing `opacity` (0-1, default 1) so a
 * part can be faded to see-through when the user hovers it — everything
 * inside multiplies by that value rather than resetting to 1, so a faded
 * part actually fades as a whole instead of flashing back to solid.
 */
(function (root) {
  'use strict';

  const RESISTOR_VALUES = [100, 220, 330, 470, 1000, 2200, 4700, 10000, 47000, 100000, 1000000];
  const CAPACITOR_VALUES = [
    { label: '100nF', farads: 100e-9 },
    { label: '1uF', farads: 1e-6 },
    { label: '10uF', farads: 10e-6 },
    { label: '100uF', farads: 100e-6 },
    { label: '1000uF', farads: 1000e-6 },
  ];
  const LED_COLORS = ['red', 'yellow', 'green', 'blue', 'white'];
  const LED_HEX = { red: '#ff4d4d', yellow: '#ffd23f', green: '#3ddc6b', blue: '#4d8dff', white: '#f4f7ff' };
  const BATTERY_VALUES = [1.5, 3, 3.3, 5, 9, 12];
  const ELECTROLYTIC_THRESHOLD = 1e-6; // farads; at/above this a cap is drawn as an electrolytic can, below as a ceramic disc

  const PALETTE = [
    { type: 'wire', label: 'Jumper Wire', terminals: 2, icon: '/' },
    { type: 'resistor', label: 'Resistor', terminals: 2, icon: '▭', defaultValue: 220 },
    { type: 'led', label: 'LED', terminals: 2, icon: '●', defaultColor: 'red' },
    { type: 'diode', label: 'Diode', terminals: 2, icon: '▷|' },
    { type: 'capacitor', label: 'Capacitor', terminals: 2, icon: '||', defaultValue: 100e-6 },
    { type: 'battery', label: 'Power Supply', terminals: 2, icon: '⎓', defaultValue: 5 },
    { type: 'switch', label: 'Switch', terminals: 2, icon: '⏻' },
    { type: 'pushbutton', label: 'Pushbutton', terminals: 2, icon: '⏹' },
    // 1 click: the anchor hole. The other 5 pins (a real 6-pin trimmer's
    // mirrored footprint straddling the center channel) are derived from it.
    { type: 'potentiometer', label: 'Potentiometer', terminals: 1, icon: '◎', defaultValue: 10000 },
  ];

  function resistorColorBands(value) {
    // real 4-band resistor color code, computed from the numeric value
    const colors = ['black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet', 'gray', 'white'];
    const hex = {
      black: '#1a1a1a', brown: '#7a4a2a', red: '#e0483f', orange: '#ff9633',
      yellow: '#ffd23f', green: '#3ddc6b', blue: '#4d8dff', violet: '#a855f7',
      gray: '#9aa0a6', white: '#f4f7ff', gold: '#d4af37',
    };
    let v = value;
    let mult = 0;
    while (v >= 100) {
      v /= 10;
      mult++;
    }
    const digits = Math.round(v).toString().padStart(2, '0');
    const d1 = parseInt(digits[0], 10);
    const d2 = parseInt(digits[1], 10);
    return [hex[colors[d1]], hex[colors[d2]], hex[colors[mult]] || hex.gold, hex.gold];
  }

  function formatOhms(v) {
    if (v >= 1e6) return (v / 1e6).toFixed(v % 1e6 === 0 ? 0 : 1) + 'MΩ';
    if (v >= 1e3) return (v / 1e3).toFixed(v % 1e3 === 0 ? 0 : 1) + 'kΩ';
    return v + 'Ω';
  }

  function formatFarads(v) {
    const round = (x) => Math.round(x * 1000) / 1000;
    if (v >= 1e-3) return round(v * 1e3) + 'mF';
    if (v >= 1e-6) return round(v * 1e6) + 'uF';
    if (v >= 1e-9) return round(v * 1e9) + 'nF';
    return round(v * 1e12) + 'pF';
  }

  // ---- drawing helpers: components are drawn between two pixel points ----
  function midAngle(x1, y1, x2, y2) {
    return Math.atan2(y2 - y1, x2 - x1);
  }

  function op(o) {
    return o == null ? 1 : o;
  }

  function drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd, opacity) {
    ctx.save();
    ctx.globalAlpha = op(opacity);
    ctx.strokeStyle = '#b5b5b0';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(bodyStart.x, bodyStart.y);
    ctx.moveTo(bodyEnd.x, bodyEnd.y);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.restore();
  }

  function lerp(x1, y1, x2, y2, t) {
    return { x: x1 + (x2 - x1) * t, y: y1 + (y2 - y1) * t };
  }

  function drawResistor(ctx, comp, x1, y1, x2, y2, opacity) {
    const o = op(opacity);
    const bodyStart = lerp(x1, y1, x2, y2, 0.28);
    const bodyEnd = lerp(x1, y1, x2, y2, 0.72);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd, o);
    const ang = midAngle(x1, y1, x2, y2);
    ctx.save();
    ctx.globalAlpha = o;
    ctx.translate((bodyStart.x + bodyEnd.x) / 2, (bodyStart.y + bodyEnd.y) / 2);
    ctx.rotate(ang);
    const len = Math.hypot(bodyEnd.x - bodyStart.x, bodyEnd.y - bodyStart.y);
    const w = 11;
    ctx.globalAlpha = 0.9 * o;
    ctx.fillStyle = '#e8d8b0';
    roundRect(ctx, -len / 2, -w / 2, len, w, 4);
    ctx.fill();
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#c9b98a';
    ctx.lineWidth = 1;
    roundRect(ctx, -len / 2, -w / 2, len, w, 4);
    ctx.stroke();
    const bands = resistorColorBands(comp.value);
    const bandW = len / 7;
    bands.forEach((c, i) => {
      ctx.fillStyle = c;
      ctx.fillRect(-len / 2 + bandW * (i + 1.2), -w / 2 + 1, bandW * 0.6, w - 2);
    });
    ctx.restore();
  }

  function drawLed(ctx, comp, x1, y1, x2, y2, glow, opacity) {
    const o = op(opacity);
    const bodyStart = lerp(x1, y1, x2, y2, 0.32);
    const bodyEnd = lerp(x1, y1, x2, y2, 0.68);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd, o);
    const cx = (bodyStart.x + bodyEnd.x) / 2;
    const cy = (bodyStart.y + bodyEnd.y) / 2;
    const r = 9;
    ctx.save();
    ctx.globalAlpha = o;
    if (glow > 0) {
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, r * 3.2);
      const hex = LED_HEX[comp.color] || LED_HEX.red;
      g.addColorStop(0, hex + 'cc');
      g.addColorStop(1, hex + '00');
      ctx.fillStyle = g;
      ctx.globalAlpha = Math.min(1, glow) * o;
      ctx.beginPath();
      ctx.arc(cx, cy, r * 3.2, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = o;
    }
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.fillStyle = (LED_HEX[comp.color] || LED_HEX.red) + (glow > 0 ? 'ee' : '55');
    ctx.fill();
    ctx.strokeStyle = '#00000033';
    ctx.lineWidth = 1;
    ctx.stroke();
    // flat side marks the cathode (matches the shorter lead convention)
    ctx.beginPath();
    ctx.arc(cx, cy, r * 0.45, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff55';
    ctx.fill();
    ctx.restore();
  }

  // A generic silicon rectifier diode: same electrical family as an LED
  // (one-way conduction past a threshold) but drawn as the classic
  // black-body-with-a-cathode-band axial part, no glow.
  function drawDiode(ctx, comp, x1, y1, x2, y2, opacity) {
    const o = op(opacity);
    const bodyStart = lerp(x1, y1, x2, y2, 0.32);
    const bodyEnd = lerp(x1, y1, x2, y2, 0.68);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd, o);
    const ang = midAngle(x1, y1, x2, y2);
    ctx.save();
    ctx.globalAlpha = o;
    ctx.translate((bodyStart.x + bodyEnd.x) / 2, (bodyStart.y + bodyEnd.y) / 2);
    ctx.rotate(ang);
    const len = Math.hypot(bodyEnd.x - bodyStart.x, bodyEnd.y - bodyStart.y);
    const w = 9;
    ctx.fillStyle = '#2b2f36';
    roundRect(ctx, -len / 2, -w / 2, len, w, 3);
    ctx.fill();
    ctx.strokeStyle = '#111318';
    ctx.lineWidth = 1;
    roundRect(ctx, -len / 2, -w / 2, len, w, 3);
    ctx.stroke();
    // cathode band near the "b" terminal (terminals[0] is the anode)
    ctx.fillStyle = '#e8ecf1';
    ctx.fillRect(len / 2 - len * 0.22, -w / 2 + 1, len * 0.14, w - 2);
    ctx.restore();
  }

  function drawCapacitor(ctx, comp, x1, y1, x2, y2, opacity) {
    const o = op(opacity);
    const electrolytic = comp.value >= ELECTROLYTIC_THRESHOLD;
    const bodyStart = lerp(x1, y1, x2, y2, electrolytic ? 0.38 : 0.42);
    const bodyEnd = lerp(x1, y1, x2, y2, electrolytic ? 0.62 : 0.58);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd, o);
    const ang = midAngle(x1, y1, x2, y2);
    ctx.save();
    ctx.globalAlpha = o;
    ctx.translate((bodyStart.x + bodyEnd.x) / 2, (bodyStart.y + bodyEnd.y) / 2);
    ctx.rotate(ang);
    if (electrolytic) {
      // electrolytic: blue can with a polarity stripe toward the "-" lead
      ctx.fillStyle = '#274b8f';
      roundRect(ctx, -9, -13, 18, 26, 5);
      ctx.fill();
      ctx.fillStyle = '#9fb8ec';
      ctx.fillRect(4, -12, 3, 24);
      ctx.fillStyle = '#ffffffcc';
      ctx.font = '6px monospace';
      ctx.save();
      ctx.rotate(Math.PI / 2);
      ctx.fillText(formatFarads(comp.value), -9, -3);
      ctx.restore();
    } else {
      // ceramic: a small non-polarized disc
      ctx.beginPath();
      ctx.ellipse(0, 0, 10, 12, 0, 0, Math.PI * 2);
      ctx.fillStyle = '#e8a33d';
      ctx.fill();
      ctx.strokeStyle = '#a5691a';
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.fillStyle = '#3a2000cc';
      ctx.font = '6px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(formatFarads(comp.value), 0, 3);
      ctx.textAlign = 'left';
    }
    ctx.restore();
  }

  function drawBattery(ctx, comp, x1, y1, x2, y2, opacity) {
    const o = op(opacity);
    const bodyStart = lerp(x1, y1, x2, y2, 0.3);
    const bodyEnd = lerp(x1, y1, x2, y2, 0.7);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd, o);
    const ang = midAngle(x1, y1, x2, y2);
    ctx.save();
    ctx.globalAlpha = o;
    ctx.translate((bodyStart.x + bodyEnd.x) / 2, (bodyStart.y + bodyEnd.y) / 2);
    ctx.rotate(ang);
    ctx.globalAlpha = 0.92 * o;
    ctx.fillStyle = '#3a3f33';
    roundRect(ctx, -22, -13, 44, 26, 5);
    ctx.fill();
    ctx.globalAlpha = o;
    ctx.fillStyle = '#f4d35e';
    ctx.font = 'bold 11px monospace';
    ctx.textAlign = 'center';
    ctx.fillText(comp.value + 'V', 0, 4);
    ctx.textAlign = 'left';
    ctx.fillStyle = '#e0483f';
    ctx.font = 'bold 12px monospace';
    ctx.fillText('+', -19, 4);
    ctx.fillStyle = '#3f7fe0';
    ctx.fillText('-', 15, 4);
    ctx.restore();
  }

  function drawSwitch(ctx, comp, x1, y1, x2, y2, opacity) {
    const o = op(opacity);
    const bodyStart = lerp(x1, y1, x2, y2, 0.25);
    const bodyEnd = lerp(x1, y1, x2, y2, 0.75);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd, o);
    ctx.save();
    ctx.globalAlpha = o;
    ctx.strokeStyle = comp.closed ? '#3ddc6b' : '#c94a4a';
    ctx.lineWidth = 2.4;
    ctx.beginPath();
    ctx.arc(bodyStart.x, bodyStart.y, 2.5, 0, Math.PI * 2);
    ctx.arc(bodyEnd.x, bodyEnd.y, 2.5, 0, Math.PI * 2);
    ctx.fillStyle = ctx.strokeStyle;
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(bodyStart.x, bodyStart.y);
    if (comp.closed) {
      ctx.lineTo(bodyEnd.x, bodyEnd.y);
    } else {
      const mid = lerp(bodyStart.x, bodyStart.y, bodyEnd.x, bodyEnd.y, 0.55);
      ctx.lineTo(mid.x, mid.y - 10);
    }
    ctx.stroke();
    ctx.restore();
  }

  // Momentary tactile pushbutton: a square cap that visibly sinks in and
  // turns green while held, distinct from the toggle switch's schematic look.
  function drawPushbutton(ctx, comp, x1, y1, x2, y2, opacity) {
    const o = op(opacity);
    const bodyStart = lerp(x1, y1, x2, y2, 0.3);
    const bodyEnd = lerp(x1, y1, x2, y2, 0.7);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd, o);
    const cx = (bodyStart.x + bodyEnd.x) / 2;
    const cy = (bodyStart.y + bodyEnd.y) / 2;
    const pressed = !!comp.closed;
    ctx.save();
    ctx.globalAlpha = o;
    ctx.fillStyle = '#2b2f36';
    roundRect(ctx, cx - 11, cy - 11, 22, 22, 4);
    ctx.fill();
    ctx.fillStyle = pressed ? '#3ddc6b' : '#cfd8e3';
    const inset = pressed ? 3.5 : 2;
    roundRect(ctx, cx - 11 + inset, cy - 11 + inset, 22 - inset * 2, 22 - inset * 2, 3);
    ctx.fill();
    ctx.restore();
  }

  // A real 6-pin trimmer: two mirrored 3-pin rows straddling the center
  // channel (electrically just 3 nodes — end A, wiper, end B — the mirrored
  // pins on the far row are wired internally to the near row for mechanical
  // stability, modeled upstream as extra jumper wires between them).
  // t = [nearA, nearWiper, nearB, farA, farWiper, farB]
  function drawPotentiometer(ctx, comp, t, opacity) {
    const o = op(opacity);
    const cx = (t[1].x + t[4].x) / 2;
    const cy = (t[1].y + t[4].y) / 2;
    const left = Math.min(t[0].x, t[3].x) - 10;
    const right = Math.max(t[2].x, t[5].x) + 10;
    const halfH = 17;

    ctx.save();
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#b5b5b0';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    for (let i = 0; i < 3; i++) {
      ctx.moveTo(t[i].x, t[i].y);
      ctx.lineTo(t[i].x, cy - halfH);
    }
    for (let i = 3; i < 6; i++) {
      ctx.moveTo(t[i].x, t[i].y);
      ctx.lineTo(t[i].x, cy + halfH);
    }
    ctx.stroke();

    ctx.globalAlpha = 0.92 * o;
    ctx.fillStyle = '#8a7a54';
    roundRect(ctx, left, cy - halfH, right - left, halfH * 2, 6);
    ctx.fill();
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#6b5d3f';
    ctx.lineWidth = 1;
    roundRect(ctx, left, cy - halfH, right - left, halfH * 2, 6);
    ctx.stroke();

    // knob position shows the wiper setting
    const pos = comp.pos ?? 0.5;
    const angle = -Math.PI * 0.75 + pos * Math.PI * 1.5;
    ctx.beginPath();
    ctx.arc(cx, cy, 10, 0, Math.PI * 2);
    ctx.fillStyle = '#f4f4f0';
    ctx.fill();
    ctx.strokeStyle = '#5b5f52';
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(angle) * 9, cy + Math.sin(angle) * 9);
    ctx.stroke();
    ctx.restore();
  }

  function drawWire(ctx, x1, y1, x2, y2, color, opacity) {
    const midY = Math.min(y1, y2) - 18 - Math.min(40, Math.hypot(x2 - x1, y2 - y1) * 0.12);
    ctx.save();
    ctx.globalAlpha = op(opacity);
    ctx.strokeStyle = color || '#2a6f4a';
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.quadraticCurveTo((x1 + x2) / 2, midY, x2, y2);
    ctx.stroke();
    ctx.restore();
    return { quadCtrl: { x: (x1 + x2) / 2, y: midY } };
  }

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }

  const api = {
    PALETTE, RESISTOR_VALUES, CAPACITOR_VALUES, LED_COLORS, LED_HEX, BATTERY_VALUES, ELECTROLYTIC_THRESHOLD,
    resistorColorBands, formatOhms, formatFarads,
    drawResistor, drawLed, drawDiode, drawCapacitor, drawBattery,
    drawSwitch, drawPushbutton, drawPotentiometer, drawWire, roundRect, lerp,
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.Components = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
