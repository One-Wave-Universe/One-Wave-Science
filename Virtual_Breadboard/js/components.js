/*
 * Component palette: what can be placed on the board, its electrical
 * defaults, and how to draw it. Bodies are drawn semi-transparent so the
 * board holes and leads underneath stay visible ("clear and visible" parts).
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

  const PALETTE = [
    { type: 'wire', label: 'Jumper Wire', terminals: 2, icon: '/' },
    { type: 'resistor', label: 'Resistor', terminals: 2, icon: '▭', defaultValue: 220 },
    { type: 'led', label: 'LED', terminals: 2, icon: '●', defaultColor: 'red' },
    { type: 'capacitor', label: 'Capacitor', terminals: 2, icon: '||', defaultValue: 100e-6 },
    { type: 'battery', label: 'Power Supply', terminals: 2, icon: '⎓', defaultValue: 5 },
    { type: 'switch', label: 'Switch', terminals: 2, icon: '⏻' },
    { type: 'potentiometer', label: 'Potentiometer', terminals: 3, icon: '◎', defaultValue: 10000 },
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

  // ---- drawing helpers: components are drawn between two pixel points ----
  function midAngle(x1, y1, x2, y2) {
    return Math.atan2(y2 - y1, x2 - x1);
  }

  function drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd) {
    ctx.strokeStyle = '#b5b5b0';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(bodyStart.x, bodyStart.y);
    ctx.moveTo(bodyEnd.x, bodyEnd.y);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  function lerp(x1, y1, x2, y2, t) {
    return { x: x1 + (x2 - x1) * t, y: y1 + (y2 - y1) * t };
  }

  function drawResistor(ctx, comp, x1, y1, x2, y2) {
    const bodyStart = lerp(x1, y1, x2, y2, 0.28);
    const bodyEnd = lerp(x1, y1, x2, y2, 0.72);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd);
    const ang = midAngle(x1, y1, x2, y2);
    ctx.save();
    ctx.translate((bodyStart.x + bodyEnd.x) / 2, (bodyStart.y + bodyEnd.y) / 2);
    ctx.rotate(ang);
    const len = Math.hypot(bodyEnd.x - bodyStart.x, bodyEnd.y - bodyStart.y);
    const w = 11;
    ctx.globalAlpha = 0.9;
    ctx.fillStyle = '#e8d8b0';
    roundRect(ctx, -len / 2, -w / 2, len, w, 4);
    ctx.fill();
    ctx.globalAlpha = 1;
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

  function drawLed(ctx, comp, x1, y1, x2, y2, glow) {
    const bodyStart = lerp(x1, y1, x2, y2, 0.32);
    const bodyEnd = lerp(x1, y1, x2, y2, 0.68);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd);
    const cx = (bodyStart.x + bodyEnd.x) / 2;
    const cy = (bodyStart.y + bodyEnd.y) / 2;
    const r = 9;
    if (glow > 0) {
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, r * 3.2);
      const hex = LED_HEX[comp.color] || LED_HEX.red;
      g.addColorStop(0, hex + 'cc');
      g.addColorStop(1, hex + '00');
      ctx.fillStyle = g;
      ctx.globalAlpha = Math.min(1, glow);
      ctx.beginPath();
      ctx.arc(cx, cy, r * 3.2, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;
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
  }

  function drawCapacitor(ctx, comp, x1, y1, x2, y2) {
    const bodyStart = lerp(x1, y1, x2, y2, 0.4);
    const bodyEnd = lerp(x1, y1, x2, y2, 0.6);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd);
    const ang = midAngle(x1, y1, x2, y2);
    ctx.save();
    ctx.translate((bodyStart.x + bodyEnd.x) / 2, (bodyStart.y + bodyEnd.y) / 2);
    ctx.rotate(ang);
    ctx.globalAlpha = 0.9;
    ctx.fillStyle = '#274b8f';
    roundRect(ctx, -8, -12, 16, 24, 4);
    ctx.fill();
    ctx.globalAlpha = 1;
    ctx.fillStyle = '#ffffffcc';
    ctx.font = '7px monospace';
    ctx.save();
    ctx.rotate(Math.PI / 2);
    ctx.fillText(comp.label || '', -10, 2);
    ctx.restore();
    ctx.restore();
  }

  function drawBattery(ctx, comp, x1, y1, x2, y2) {
    const bodyStart = lerp(x1, y1, x2, y2, 0.3);
    const bodyEnd = lerp(x1, y1, x2, y2, 0.7);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd);
    const ang = midAngle(x1, y1, x2, y2);
    ctx.save();
    ctx.translate((bodyStart.x + bodyEnd.x) / 2, (bodyStart.y + bodyEnd.y) / 2);
    ctx.rotate(ang);
    ctx.globalAlpha = 0.92;
    ctx.fillStyle = '#3a3f33';
    roundRect(ctx, -22, -13, 44, 26, 5);
    ctx.fill();
    ctx.globalAlpha = 1;
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

  function drawSwitch(ctx, comp, x1, y1, x2, y2) {
    const bodyStart = lerp(x1, y1, x2, y2, 0.25);
    const bodyEnd = lerp(x1, y1, x2, y2, 0.75);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd);
    ctx.save();
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

  function drawPotentiometer(ctx, comp, p) {
    // p = {a:{x,y}, wiper:{x,y}, b:{x,y}}
    ctx.save();
    ctx.globalAlpha = 0.9;
    ctx.fillStyle = '#8a7a54';
    const cx = p.wiper.x;
    const cy = p.wiper.y - 14;
    roundRect(ctx, cx - 16, cy - 16, 32, 32, 6);
    ctx.fill();
    ctx.globalAlpha = 1;
    ctx.strokeStyle = '#b5b5b0';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(p.a.x, p.a.y);
    ctx.lineTo(cx - 12, cy + 12);
    ctx.moveTo(p.b.x, p.b.y);
    ctx.lineTo(cx + 12, cy + 12);
    ctx.moveTo(p.wiper.x, p.wiper.y);
    ctx.lineTo(cx, cy + 12);
    ctx.stroke();
    // knob position shows the wiper setting
    const pos = comp.pos ?? 0.5;
    const angle = -Math.PI * 0.75 + pos * Math.PI * 1.5;
    ctx.beginPath();
    ctx.arc(cx, cy, 9, 0, Math.PI * 2);
    ctx.fillStyle = '#f4f4f0';
    ctx.fill();
    ctx.strokeStyle = '#5b5f52';
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(angle) * 8, cy + Math.sin(angle) * 8);
    ctx.stroke();
    ctx.restore();
  }

  function drawWire(ctx, x1, y1, x2, y2, color, currentFrac) {
    const midY = Math.min(y1, y2) - 18 - Math.min(40, Math.hypot(x2 - x1, y2 - y1) * 0.12);
    ctx.save();
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
    PALETTE, RESISTOR_VALUES, CAPACITOR_VALUES, LED_COLORS, LED_HEX, BATTERY_VALUES,
    resistorColorBands, formatOhms, drawResistor, drawLed, drawCapacitor, drawBattery,
    drawSwitch, drawPotentiometer, drawWire, roundRect, lerp,
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.Components = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
