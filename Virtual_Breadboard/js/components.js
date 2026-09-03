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
  const INDUCTOR_VALUES = [1e-6, 10e-6, 100e-6, 1e-3, 10e-3, 100e-3, 1];
  const AC_FREQ_VALUES = [0.1, 0.5, 1, 2, 5, 10, 60, 100];

  // Discrete MOSFET "value" selects a real part class (see circuit.js's
  // NMOS_PARTS/PMOS_PARTS) rather than a made-up continuous parameter.
  const MOSFET_CLASS_LABELS = {
    1.5: 'Logic-level (AO3400A/AO3401A-class, Vth~1.5V)',
    2.1: 'Standard (2N7000/BS250-class, Vth~2.1V)',
  };

  const WIRE_COLOR_CHOICES = ['#2a6f4a', '#c94a4a', '#3f7fe0', '#d4af37', '#7a4a2a', '#a855f7', '#e8ecf1', '#1a1a1a'];
  const WIRE_COLOR_NAMES = {
    '#2a6f4a': 'Green', '#c94a4a': 'Red', '#3f7fe0': 'Blue', '#d4af37': 'Gold',
    '#7a4a2a': 'Brown', '#a855f7': 'Purple', '#e8ecf1': 'White', '#1a1a1a': 'Black',
  };
  const WIRE_GAUGES = { thin: '30 AWG', standard: '22 AWG', thick: '18 AWG' };
  const WIRE_GAUGE_WIDTH = { thin: 1.8, standard: 3, thick: 4.6 };
  // real copper resistance-per-meter for each gauge -- used to give a
  // toroid's windings actual DC resistance from wire gauge + turns + core size
  const WIRE_GAUGE_OHMS_PER_M = { thin: 0.339, standard: 0.0531, thick: 0.0210 };

  // ferrite toroid cores: A_L (inductance factor, henries per turn^2 -- real
  // datasheet parameter, e.g. a small FT37-43-class core) and a
  // representative mean-turn length (meters) for winding-resistance math.
  const TOROID_CORES = {
    small: { al: 100e-9, meanTurnLen: 0.03, label: 'Small' },
    medium: { al: 250e-9, meanTurnLen: 0.05, label: 'Medium' },
    large: { al: 600e-9, meanTurnLen: 0.08, label: 'Large' },
  };
  const TOROID_TURNS_VALUES = [5, 10, 20, 50, 100, 200];
  // coupling coefficient between windings sharing one core, as a function of
  // how tightly the sections are wound relative to each other
  const TOROID_SPACING_COUPLING = { tight: 0.97, normal: 0.9, wide: 0.75 };

  // Square-loop / remanent memory cores: an idealized nonlinear core (see
  // circuit.js) instead of the toroid's linear one. hcAmpTurns is the real
  // ampere-turns coercive threshold that must be exceeded to flip the core's
  // magnetization -- "small" is deliberately a low-coercivity material
  // (real premium square-loop tape cores, e.g. Supermalloy/Metglas-class,
  // genuinely go this low), sized so a real millivolt-scale write current
  // through real MOSFET RDS(on) + winding resistance can actually flip it.
  // phiSat is the core's total flux capacity at saturation (shared by every
  // winding on it: Faraday's law says each winding's induced voltage is
  // turns * phiSat * dB/dt). switchTau is how long the flip itself takes
  // once past threshold -- small but nonzero, so it shows up as a real,
  // finite induced-voltage spike on a sense winding instead of a step.
  const MEMORY_CORES = {
    small: { hcAmpTurns: 2, phiSat: 4e-6, meanTurnLen: 0.03, switchTau: 0.002, label: 'Small (low-coercivity)' },
    medium: { hcAmpTurns: 5, phiSat: 1e-5, meanTurnLen: 0.05, switchTau: 0.004, label: 'Medium' },
    large: { hcAmpTurns: 10, phiSat: 2.5e-5, meanTurnLen: 0.08, switchTau: 0.008, label: 'Large' },
  };
  const MEMORY_CORE_TURNS_VALUES = [5, 10, 20, 50, 100, 200];
  // matches a typical 4-channel scope's trace colors (yellow/CH1, green/CH2, ...)
  const SCOPE_COLORS = ['#f4d35e', '#3ddc6b', '#4d8dff', '#ff6ec7'];

  const PALETTE = [
    { type: 'wire', label: 'Jumper Wire', terminals: 2, icon: '/' },
    // A standalone 4-lead part: each end forks into 2 holes (a V/Y at both
    // ends), joined by one wire in the middle — all 4 holes the same node.
    // For distributing a ground/rail from 2 points to 2 more points.
    { type: 'ywire', label: 'Y-Split Wire', terminals: 4, icon: 'Y' },
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
    // 2 inputs (the rails to split), 1 output forced to their midpoint —
    // an ideal rail-splitter/virtual-ground buffer (TLE2426-class).
    { type: 'vgnd', label: 'Virtual Ground', terminals: 3, icon: 'V0' },
    { type: 'inductor', label: 'Inductor', terminals: 2, icon: 'L', defaultValue: 10e-3 },
    // an ideal function-generator-style source: real time-varying AC,
    // evaluated on the simulator's own running clock every frame.
    { type: 'acsource', label: 'AC Source', terminals: 2, icon: '~', defaultValue: 5, defaultFreq: 1 },
    // 1 reference pin + 2 outputs (sin, cos) -- the electrical interface of
    // a real MTJ/TMR rotary angle-sensor IC, driven by a rotating field.
    { type: 'mtjsensor', label: 'MTJ Angle Sensor', terminals: 3, icon: 'θ', defaultValue: 2.5, defaultFreq: 1 },
    // a zero-load voltage tap, like a real scope probe -- never enters the
    // circuit physics itself, just reads whatever node it's touching.
    { type: 'scope', label: 'Scope Probe', terminals: 1, icon: 'CH' },
    // 2 zero-load taps (A, B) plotted as ONE trace: V(A) - V(B). Same
    // never-loads-the-circuit philosophy as the plain Scope Probe, just
    // reporting a difference instead of one node's voltage -- for reading
    // a millivolt-scale lean relative to a reference (e.g. V0) directly,
    // instead of subtracting two absolute readings by hand.
    { type: 'diffscope', label: 'Differential Scope (A−B)', terminals: 2, icon: 'ΔCH' },
    // terminal count is variable (2 per winding section, chosen before
    // placement) -- app.js overrides terminalsNeeded() for this type;
    // `terminals` here is just the 1-section default.
    { type: 'toroid', label: 'Ferrite Toroid', terminals: 2, icon: '◯' },
    // 3 pins: gate, drain, source -- a real discrete N-channel MOSFET
    // (AO3400A/2N7000-class). Conducts drain-source only while Vgs is above
    // its real threshold; its body diode conducts source->drain regardless
    // of gate state, exactly like the physical part.
    { type: 'nmos', label: 'N-MOSFET', terminals: 3, icon: 'N⏚', defaultValue: 1.5 },
    // P-channel complement (AO3401A/BS250-class): conducts when Vgs is
    // below its (negative) threshold; body diode conducts drain->source.
    { type: 'pmos', label: 'P-MOSFET', terminals: 3, icon: 'P⏚', defaultValue: 1.5 },
    // terminal count is variable (2 per winding, 1-3 windings, chosen
    // before placement) -- app.js overrides terminalsNeeded() for this
    // type, same as the toroid. A real nonlinear square-loop core: DC
    // magnetic memory (remanence) instead of the toroid's linear
    // inductance. Extra windings ARE the group-memory / toward-away-
    // neighbor mechanism -- just more real ampere-turns summed onto the
    // same shared flux, wired by the user, not a scripted state machine.
    { type: 'memorycore', label: 'Memory Core (square-loop)', terminals: 2, icon: 'B±' },
    // 1 click: the pin-1 anchor hole (must be row 'e', the row bordering
    // the center channel). The other 7 pins of a real 8-pin DIP-8 TLV3202
    // dual comparator are derived from it -- 4 columns wide, straddling
    // the gap, exactly how a real DIP chip sits on a breadboard. Pin
    // order matches the real datasheet: OUT1,IN1-,IN1+,GND,IN2+,IN2-,
    // OUT2,VCC.
    { type: 'comparator', label: 'TLV3202 Dual Comparator', terminals: 1, icon: 'IC' },
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
  function potCentroid(t) {
    return { x: (t[1].x + t[4].x) / 2, y: (t[1].y + t[4].y) / 2 };
  }

  // wiper "pos" (0-1) <-> knob pointer angle, a 270-degree sweep from
  // -135deg (fully counter-clockwise) to +135deg (fully clockwise).
  const POT_ANGLE_START = -Math.PI * 0.75;
  const POT_ANGLE_SWEEP = Math.PI * 1.5;
  function potPosToAngle(pos) {
    return POT_ANGLE_START + pos * POT_ANGLE_SWEEP;
  }
  function potAngleToPos(angle) {
    let a = angle - POT_ANGLE_START;
    while (a < 0) a += Math.PI * 2;
    while (a > Math.PI * 2) a -= Math.PI * 2;
    // angles past the sweep's end snap to whichever endpoint is nearer,
    // so grabbing the knob and dragging past a stop just pins it there
    if (a > POT_ANGLE_SWEEP) {
      const past = a - POT_ANGLE_SWEEP;
      const wrapGap = Math.PI * 2 - POT_ANGLE_SWEEP;
      a = past < wrapGap / 2 ? POT_ANGLE_SWEEP : 0;
    }
    return Math.max(0, Math.min(1, a / POT_ANGLE_SWEEP));
  }

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

    // knob position shows the wiper setting -- click-drag it in Select mode
    const pos = comp.pos ?? 0.5;
    const angle = potPosToAngle(pos);
    ctx.beginPath();
    ctx.arc(cx, cy, 10, 0, Math.PI * 2);
    ctx.fillStyle = '#f4f4f0';
    ctx.fill();
    ctx.strokeStyle = comp.dragging ? '#3f7fe0' : '#5b5f52';
    ctx.lineWidth = comp.dragging ? 2 : 1;
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(angle) * 9, cy + Math.sin(angle) * 9);
    ctx.stroke();
    ctx.restore();
  }

  // style: 'loop' (default) is a flexible wire arcing up and over whatever's
  // between its ends; 'flat' is a rigid pre-formed jumper lying straight
  // against the board.
  function drawWire(ctx, x1, y1, x2, y2, color, opacity, style, gauge) {
    ctx.save();
    ctx.globalAlpha = op(opacity);
    ctx.strokeStyle = color || '#2a6f4a';
    ctx.lineWidth = WIRE_GAUGE_WIDTH[gauge] || WIRE_GAUGE_WIDTH.standard;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    if (style === 'flat') {
      ctx.lineTo(x2, y2);
    } else {
      const midY = Math.min(y1, y2) - 18 - Math.min(40, Math.hypot(x2 - x1, y2 - y1) * 0.12);
      ctx.quadraticCurveTo((x1 + x2) / 2, midY, x2, y2);
    }
    ctx.stroke();
    ctx.restore();
  }

  // Y-split wire: a single conductor running end-to-end between t[0] and
  // t[1] (drawn exactly like a normal wire), with a third lead tapping off
  // its midpoint out to t[2] — for feeding a ground/rail node to a second
  // point without a whole second jumper. All 3 holes are one electrical node.
  // t = [end1A, end1B, end2A, end2B]: a standalone 4-lead part — each end
  // forks (a V/Y) into 2 holes, joined by one wire between the two fork
  // points. All 4 holes are one electrical node. Good for bridging one
  // node (e.g. a ground/rail row) from 2 points to 2 more points elsewhere.
  function yWireJunctions(t) {
    return [
      { x: (t[0].x + t[1].x) / 2, y: (t[0].y + t[1].y) / 2 },
      { x: (t[2].x + t[3].x) / 2, y: (t[2].y + t[3].y) / 2 },
    ];
  }

  function drawYWire(ctx, t, color, opacity, style, gauge) {
    const [j1, j2] = yWireJunctions(t);
    drawWire(ctx, t[0].x, t[0].y, j1.x, j1.y, color, opacity, style, gauge);
    drawWire(ctx, t[1].x, t[1].y, j1.x, j1.y, color, opacity, style, gauge);
    drawWire(ctx, j1.x, j1.y, j2.x, j2.y, color, opacity, style, gauge);
    drawWire(ctx, t[2].x, t[2].y, j2.x, j2.y, color, opacity, style, gauge);
    drawWire(ctx, t[3].x, t[3].y, j2.x, j2.y, color, opacity, style, gauge);
    ctx.save();
    ctx.globalAlpha = op(opacity);
    ctx.fillStyle = color || '#2a6f4a';
    [j1, j2].forEach((j) => {
      ctx.beginPath();
      ctx.arc(j.x, j.y, 2.5, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.restore();
  }

  // t = [inA, inB, out]: an ideal rail-splitter forcing its output to the
  // midpoint of the two rails it reads (real hardware: TLE2426-class).
  function vgndCentroid(t) {
    return { x: (t[0].x + t[1].x + t[2].x) / 3, y: (t[0].y + t[1].y + t[2].y) / 3 };
  }

  function drawVGnd(ctx, comp, t, opacity) {
    const o = op(opacity);
    const c = vgndCentroid(t);
    ctx.save();
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#b5b5b0';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    t.forEach((p) => {
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(c.x, c.y);
    });
    ctx.stroke();

    ctx.fillStyle = '#3a3f4d';
    roundRect(ctx, c.x - 15, c.y - 11, 30, 22, 5);
    ctx.fill();
    ctx.strokeStyle = '#5a6178';
    ctx.lineWidth = 1;
    roundRect(ctx, c.x - 15, c.y - 11, 30, 22, 5);
    ctx.stroke();
    ctx.fillStyle = '#8ecbff';
    ctx.font = 'bold 10px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('V0', c.x, c.y + 4);
    ctx.textAlign = 'left';
    ctx.restore();
  }

  // t = [gate, drain, source]: a real discrete MOSFET. Border color reflects
  // the live channel state (green when conducting, gray when off) and a
  // small amber dot marks the body diode conducting -- the same "measured
  // state over labels" idea as the LED glow.
  const MOSFET_ON_COLOR = '#3ddc6b';
  const MOSFET_OFF_COLOR = '#5a6178';
  const MOSFET_DIODE_COLOR = '#e0a83f';
  function mosfetCentroid(t) {
    return { x: (t[0].x + t[1].x + t[2].x) / 3, y: (t[0].y + t[1].y + t[2].y) / 3 };
  }
  function drawMosfet(ctx, comp, t, opacity, state) {
    const o = op(opacity);
    const c = mosfetCentroid(t);
    const channelOn = !!(state && state.channelOn);
    const diodeOn = !!(state && state.bodyDiodeOn);
    const borderColor = channelOn ? MOSFET_ON_COLOR : MOSFET_OFF_COLOR;
    ctx.save();
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#b5b5b0';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    t.forEach((p) => {
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(c.x, c.y);
    });
    ctx.stroke();

    if (channelOn) {
      ctx.globalAlpha = 0.3 * o;
      ctx.fillStyle = borderColor;
      ctx.beginPath();
      ctx.arc(c.x, c.y, 20, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = o;
    }

    ctx.fillStyle = '#2b2f36';
    roundRect(ctx, c.x - 15, c.y - 12, 30, 24, 5);
    ctx.fill();
    ctx.strokeStyle = borderColor;
    ctx.lineWidth = 1.4;
    roundRect(ctx, c.x - 15, c.y - 12, 30, 24, 5);
    ctx.stroke();
    ctx.fillStyle = '#e8ecf1';
    ctx.font = 'bold 10px monospace';
    ctx.textAlign = 'center';
    ctx.fillText(comp.type === 'pmos' ? 'P' : 'N', c.x, c.y + 4);
    ctx.textAlign = 'left';

    if (diodeOn) {
      ctx.fillStyle = MOSFET_DIODE_COLOR;
      ctx.beginPath();
      ctx.arc(c.x + 11, c.y - 9, 3, 0, Math.PI * 2);
      ctx.fill();
    }
    // pin labels: g(ate)/d(rain)/s(ource), tiny, at each lead's outer end
    ctx.globalAlpha = 0.85 * o;
    ctx.fillStyle = '#8a93a5';
    ctx.font = '7px monospace';
    ctx.textAlign = 'center';
    ['g', 'd', 's'].forEach((label, i) => {
      const p = t[i];
      const dx = p.x - c.x;
      const dy = p.y - c.y;
      const len = Math.hypot(dx, dy) || 1;
      ctx.fillText(label, p.x + (dx / len) * 8, p.y + (dy / len) * 8 + 2);
    });
    ctx.textAlign = 'left';
    ctx.restore();
  }

  function drawInductor(ctx, comp, x1, y1, x2, y2, opacity) {
    const o = op(opacity);
    const bodyStart = lerp(x1, y1, x2, y2, 0.25);
    const bodyEnd = lerp(x1, y1, x2, y2, 0.75);
    drawLeads(ctx, x1, y1, x2, y2, bodyStart, bodyEnd, o);
    const ang = midAngle(x1, y1, x2, y2);
    ctx.save();
    ctx.globalAlpha = o;
    ctx.translate((bodyStart.x + bodyEnd.x) / 2, (bodyStart.y + bodyEnd.y) / 2);
    ctx.rotate(ang);
    const len = Math.hypot(bodyEnd.x - bodyStart.x, bodyEnd.y - bodyStart.y);
    // 4 coil loops -- the classic inductor schematic symbol
    ctx.strokeStyle = '#c98a3d';
    ctx.lineWidth = 2.2;
    ctx.lineCap = 'round';
    const loops = 4;
    const r = len / (loops * 2);
    ctx.beginPath();
    for (let k = 0; k < loops; k++) {
      const cx = -len / 2 + r + k * r * 2;
      ctx.moveTo(cx - r, 0);
      ctx.arc(cx, 0, r, Math.PI, 0, false);
    }
    ctx.stroke();
    ctx.fillStyle = '#cfd8e3cc';
    ctx.font = '7px monospace';
    ctx.textAlign = 'center';
    ctx.fillText(formatHenries(comp.value), 0, 13);
    ctx.textAlign = 'left';
    ctx.restore();
  }

  function formatHenries(h) {
    if (h >= 1) return h + 'H';
    if (h >= 1e-3) return (h * 1e3).toFixed(h * 1e3 >= 10 ? 0 : 1) + 'mH';
    return (h * 1e6).toFixed(0) + 'uH';
  }

  function drawAcSource(ctx, comp, x1, y1, x2, y2, opacity) {
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
    ctx.fillStyle = '#2f3550';
    ctx.beginPath();
    ctx.arc(0, 0, 13, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#6d7ba8';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(0, 0, 13, 0, Math.PI * 2);
    ctx.stroke();
    // the standard AC-source schematic symbol: a sine curve inside the circle
    ctx.strokeStyle = '#8ecbff';
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    for (let px = -8; px <= 8; px++) {
      const py = -Math.sin((px / 8) * Math.PI) * 5;
      if (px === -8) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();
    ctx.fillStyle = '#cfd8e3cc';
    ctx.font = '7px monospace';
    ctx.textAlign = 'center';
    ctx.fillText((comp.freq || 1) + 'Hz', 0, 22);
    ctx.textAlign = 'left';
    ctx.restore();
  }

  // t = [ref, sinOut, cosOut]: the electrical interface of a real MTJ/TMR
  // rotary angle-sensor IC -- two analog outputs, sin(theta)/cos(theta) of
  // a rotating field, referenced to a shared pin.
  function mtjCentroid(t) {
    return { x: (t[0].x + t[1].x + t[2].x) / 3, y: (t[0].y + t[1].y + t[2].y) / 3 };
  }

  function drawMtjSensor(ctx, comp, t, opacity, animT) {
    const o = op(opacity);
    const c = mtjCentroid(t);
    ctx.save();
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#b5b5b0';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    t.forEach((p) => {
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(c.x, c.y);
    });
    ctx.stroke();

    ctx.globalAlpha = 0.92 * o;
    ctx.fillStyle = '#3d2f50';
    ctx.beginPath();
    ctx.arc(c.x, c.y, 14, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#8a6fb5';
    ctx.lineWidth = 1;
    ctx.stroke();

    // a live needle showing the sensed field angle, so the "rotating field"
    // is actually visible turning, not just a static badge
    const angle = 2 * Math.PI * (comp.freq || 1) * (animT || 0) + ((comp.phase || 0) * Math.PI) / 180;
    ctx.strokeStyle = '#c9a6ff';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(c.x, c.y);
    ctx.lineTo(c.x + Math.cos(angle) * 10, c.y + Math.sin(angle) * 10);
    ctx.stroke();

    ctx.fillStyle = '#e8d9ff';
    ctx.font = 'bold 9px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('θ', c.x, c.y - 18);
    ctx.textAlign = 'left';
    ctx.restore();
  }

  // a scope probe is a single-point marker, not a 2-lead part -- it draws a
  // small flag at its hole instead of a body-with-leads
  function drawScopeProbe(ctx, comp, x, y, opacity) {
    const o = op(opacity);
    ctx.save();
    ctx.globalAlpha = o;
    ctx.strokeStyle = comp.color || SCOPE_COLORS[0];
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x, y - 22);
    ctx.stroke();
    ctx.fillStyle = comp.color || SCOPE_COLORS[0];
    ctx.beginPath();
    ctx.moveTo(x, y - 22);
    ctx.lineTo(x + 12, y - 18);
    ctx.lineTo(x, y - 14);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.arc(x, y, 3, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  // A differential probe: two ordinary zero-load taps (same real 10MΩ-
  // probe philosophy as drawScopeProbe -- never affects the circuit),
  // joined by a dashed line and a "Δ" marker so it reads visually as ONE
  // A-minus-B measurement, not two independent channels.
  function drawDiffScopeProbe(ctx, comp, x1, y1, x2, y2, opacity) {
    const o = op(opacity);
    const color = comp.color || SCOPE_COLORS[0];
    drawScopeProbe(ctx, comp, x1, y1, opacity);
    drawScopeProbe(ctx, comp, x2, y2, opacity);
    ctx.save();
    ctx.globalAlpha = o;
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.2;
    ctx.setLineDash([3, 3]);
    ctx.beginPath();
    ctx.moveTo(x1, y1 - 22);
    ctx.lineTo(x2, y2 - 22);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = color;
    ctx.font = 'bold 10px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('Δ', (x1 + x2) / 2, Math.min(y1, y2) - 26);
    ctx.textAlign = 'left';
    ctx.restore();
  }

  const TOROID_SECTION_COLORS = ['#d4af37', '#4d8dff', '#3ddc6b'];

  // t = terminal points, 2 per winding section in order [s0a,s0b, s1a,s1b, ...]
  function toroidCentroid(t) {
    const x = t.reduce((s, p) => s + p.x, 0) / t.length;
    const y = t.reduce((s, p) => s + p.y, 0) / t.length;
    return { x, y };
  }

  function drawToroid(ctx, comp, t, opacity) {
    const o = op(opacity);
    const c = toroidCentroid(t);
    const sections = comp.turnsPerSection ? comp.turnsPerSection.length : t.length / 2;
    // unlike a fixed size, scale the ring to the actual leg spread (same
    // idea as drawResistor/drawInductor sizing their body off the real
    // distance between terminals) -- a hardcoded radius bigger than the
    // terminal spacing would swallow the legs and look off-center whenever
    // the toroid is placed on closely-spaced holes, which is the common case
    // for a single compact part
    const spread = Math.max(...t.map((p) => Math.hypot(p.x - c.x, p.y - c.y)));
    const outerR = Math.min(24, Math.max(10, spread * 0.85));
    const innerR = outerR * 0.54;

    ctx.save();
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#b5b5b0';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    t.forEach((p) => {
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(c.x, c.y);
    });
    ctx.stroke();

    // the ferrite core itself -- a dark donut
    ctx.globalAlpha = 0.94 * o;
    ctx.fillStyle = '#2b2b2e';
    ctx.beginPath();
    ctx.arc(c.x, c.y, outerR, 0, Math.PI * 2);
    ctx.arc(c.x, c.y, innerR, 0, Math.PI * 2, true);
    ctx.fill('evenodd');
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#4a4a4e';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(c.x, c.y, outerR, 0, Math.PI * 2);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(c.x, c.y, innerR, 0, Math.PI * 2);
    ctx.stroke();

    // windings: each section gets its own color and its own arc of the ring,
    // drawn as a run of loops over the core -- visual loop count is capped
    // for legibility even though the real turn count (used electrically)
    // can be much higher
    const spacing = comp.spacing || 'normal';
    const arcSpan = spacing === 'tight' ? (Math.PI * 2) / sections / 2.2 : spacing === 'wide' ? (Math.PI * 2) / sections / 1.15 : (Math.PI * 2) / sections / 1.6;
    for (let s = 0; s < sections; s++) {
      const turns = comp.turnsPerSection ? comp.turnsPerSection[s] : 10;
      const loops = Math.max(3, Math.min(14, Math.round(turns / 4)));
      const baseAngle = (Math.PI * 2 * s) / sections - Math.PI / 2;
      ctx.strokeStyle = TOROID_SECTION_COLORS[s % TOROID_SECTION_COLORS.length];
      ctx.lineWidth = 1.6;
      for (let i = 0; i < loops; i++) {
        const ang = baseAngle + (arcSpan * i) / Math.max(1, loops - 1) - arcSpan / 2;
        ctx.beginPath();
        ctx.ellipse(c.x + Math.cos(ang) * (outerR + innerR) / 2, c.y + Math.sin(ang) * (outerR + innerR) / 2, 5, (outerR - innerR) / 2 + 3, ang + Math.PI / 2, 0, Math.PI * 2);
        ctx.stroke();
      }
    }

    ctx.fillStyle = '#cfd8e3cc';
    ctx.font = '7px monospace';
    ctx.textAlign = 'center';
    ctx.fillText((comp.core ? comp.core[0].toUpperCase() + comp.core.slice(1) : '') + ' core', c.x, c.y + outerR + 12);
    ctx.textAlign = 'left';
    ctx.restore();
  }

  // t = terminal points, 2 per winding, in order [w0a,w0b, w1a,w1b, ...].
  // A square-loop memory core: visually similar to the toroid (a ring, one
  // color per winding), but the ring's fill color reflects the REAL solved
  // remanence B (in [-1, 1]) -- amber toward +1, blue toward -1, neutral
  // gray near 0 -- the same "measured state, not a label" idea as the LED
  // glow / MOSFET channel-on halo. This is a readout of a real number the
  // solver computed, never a value this function decides on its own.
  function memoryCoreCentroid(t) {
    const x = t.reduce((s, p) => s + p.x, 0) / t.length;
    const y = t.reduce((s, p) => s + p.y, 0) / t.length;
    return { x, y };
  }
  function drawMemoryCore(ctx, comp, t, opacity, B) {
    const o = op(opacity);
    const c = memoryCoreCentroid(t);
    const windings = comp.turnsPerWinding ? comp.turnsPerWinding.length : t.length / 2;
    const spread = Math.max(...t.map((p) => Math.hypot(p.x - c.x, p.y - c.y)));
    const outerR = Math.min(24, Math.max(10, spread * 0.85));
    const innerR = outerR * 0.54;
    const b = B == null ? 0 : Math.max(-1, Math.min(1, B));
    // blend gray (Hold, b=0) toward amber (+1) or blue (-1)
    const pos = [0xe0, 0xa8, 0x3f];
    const neg = [0x4d, 0x8d, 0xff];
    const hold = [0x5a, 0x61, 0x78];
    const target = b >= 0 ? pos : neg;
    const mix = Math.abs(b);
    const rgb = hold.map((h, i) => Math.round(h + (target[i] - h) * mix));
    const ringColor = `rgb(${rgb[0]},${rgb[1]},${rgb[2]})`;

    ctx.save();
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#b5b5b0';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    t.forEach((p) => {
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(c.x, c.y);
    });
    ctx.stroke();

    ctx.globalAlpha = 0.94 * o;
    ctx.fillStyle = '#2b2b2e';
    ctx.beginPath();
    ctx.arc(c.x, c.y, outerR, 0, Math.PI * 2);
    ctx.arc(c.x, c.y, innerR, 0, Math.PI * 2, true);
    ctx.fill('evenodd');
    ctx.globalAlpha = o;
    ctx.strokeStyle = ringColor;
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.arc(c.x, c.y, outerR, 0, Math.PI * 2);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(c.x, c.y, innerR, 0, Math.PI * 2);
    ctx.stroke();

    const arcSpan = (Math.PI * 2) / windings / 1.6;
    for (let s = 0; s < windings; s++) {
      const turns = comp.turnsPerWinding ? comp.turnsPerWinding[s] : 20;
      const loops = Math.max(3, Math.min(14, Math.round(turns / 4)));
      const baseAngle = (Math.PI * 2 * s) / windings - Math.PI / 2;
      ctx.strokeStyle = TOROID_SECTION_COLORS[s % TOROID_SECTION_COLORS.length];
      ctx.lineWidth = 1.4;
      for (let i = 0; i < loops; i++) {
        const ang = baseAngle + (arcSpan * i) / Math.max(1, loops - 1) - arcSpan / 2;
        ctx.beginPath();
        ctx.ellipse(c.x + Math.cos(ang) * (outerR + innerR) / 2, c.y + Math.sin(ang) * (outerR + innerR) / 2, 4.5, (outerR - innerR) / 2 + 2.5, ang + Math.PI / 2, 0, Math.PI * 2);
        ctx.stroke();
      }
    }

    ctx.fillStyle = ringColor;
    ctx.font = 'bold 9px monospace';
    ctx.textAlign = 'center';
    ctx.fillText(b.toFixed(2), c.x, c.y + 3);
    ctx.textAlign = 'left';
    ctx.restore();
  }

  // A real 8-pin DIP-8 straddling the center channel: pins 1-4 in one row
  // (the datasheet's OUT1,IN1-,IN1+,GND), pins 5-8 in the mirrored row
  // directly across the gap (IN2+,IN2-,OUT2,VCC) -- exactly how a real
  // DIP chip sits on a breadboard, and exactly the hole layout app.js's
  // deriveTlv3202Holes() produces from one anchor click. The two output
  // leads glow amber only while the solver's real comparatorStates says
  // that channel is actually driven HIGH -- never decided here.
  function comparatorCentroid(t) {
    const x = t.reduce((s, p) => s + p.x, 0) / t.length;
    const y = t.reduce((s, p) => s + p.y, 0) / t.length;
    return { x, y };
  }
  function drawComparatorChip(ctx, comp, t, opacity, states) {
    const o = op(opacity);
    if (!t || t.length < 8) return;
    const top = t.slice(0, 4); // pins 1-4: OUT1, IN1-, IN1+, GND
    const bottom = t.slice(4, 8); // pins 5-8: IN2+, IN2-, OUT2, VCC
    const minX = Math.min(...t.map((p) => p.x));
    const maxX = Math.max(...t.map((p) => p.x));
    const topY = top[0].y;
    const botY = bottom[0].y;
    const midY = (topY + botY) / 2;
    ctx.save();
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#b5b5b0';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    top.forEach((p) => { ctx.moveTo(p.x, p.y); ctx.lineTo(p.x, midY - 6); });
    bottom.forEach((p) => { ctx.moveTo(p.x, p.y); ctx.lineTo(p.x, midY + 6); });
    ctx.stroke();

    const bodyPad = 5;
    const bx = minX - bodyPad;
    const by = topY - 6;
    const bw = (maxX - minX) + bodyPad * 2;
    const bh = (botY - topY) + 12;
    ctx.globalAlpha = 0.96 * o;
    ctx.fillStyle = '#1f2430';
    roundRect(ctx, bx, by, bw, bh, 3);
    ctx.fill();
    ctx.globalAlpha = o;
    ctx.strokeStyle = '#5a6178';
    ctx.lineWidth = 1.2;
    roundRect(ctx, bx, by, bw, bh, 3);
    ctx.stroke();
    // pin-1 orientation notch, real DIP convention
    ctx.beginPath();
    ctx.arc(bx, midY, 4, -Math.PI / 2, Math.PI / 2);
    ctx.stroke();

    const out1High = !!(states && states.out1High);
    const out2High = !!(states && states.out2High);
    ctx.fillStyle = out1High ? '#e0a83f' : '#4d5566';
    ctx.beginPath();
    ctx.arc(top[0].x, midY - 6, 2.6, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = out2High ? '#e0a83f' : '#4d5566';
    ctx.beginPath();
    ctx.arc(bottom[2].x, midY + 6, 2.6, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#c7ccd6';
    ctx.font = 'bold 8px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('TLV3202', bx + bw / 2, midY + 3);
    ctx.textAlign = 'left';
    ctx.restore();
  }

  // A canonical, centered rendering of any part type into a small square --
  // used by the preview card in the toolbox/Inspector, so a part looks the
  // same whether you're still choosing its value or it's already on the
  // board. Reuses the exact same draw*() functions the board itself uses.
  function drawPartIcon(ctx, type, part, w, h) {
    ctx.clearRect(0, 0, w, h);
    const cx = w / 2;
    const cy = h / 2;
    const p = part || {};
    if (type === 'wire' || type === 'ywire') {
      const color = p.color || WIRE_COLOR_CHOICES[0];
      const style = p.style || 'loop';
      const gauge = p.gauge || 'standard';
      if (type === 'wire') {
        drawWire(ctx, w * 0.15, h * 0.7, w * 0.85, h * 0.3, color, 1, style, gauge);
      } else {
        const t = [
          { x: w * 0.12, y: h * 0.25 }, { x: w * 0.12, y: h * 0.55 },
          { x: w * 0.88, y: h * 0.45 }, { x: w * 0.88, y: h * 0.75 },
        ];
        drawYWire(ctx, t, color, 1, style, gauge);
      }
      return;
    }
    if (type === 'potentiometer') {
      const halfSpan = w * 0.28;
      const t = [
        { x: cx - halfSpan, y: cy - h * 0.14 }, { x: cx, y: cy - h * 0.14 }, { x: cx + halfSpan, y: cy - h * 0.14 },
        { x: cx - halfSpan, y: cy + h * 0.14 }, { x: cx, y: cy + h * 0.14 }, { x: cx + halfSpan, y: cy + h * 0.14 },
      ];
      drawPotentiometer(ctx, Object.assign({ pos: 0.5 }, p), t, 1);
      return;
    }
    if (type === 'vgnd' || type === 'mtjsensor' || type === 'nmos' || type === 'pmos') {
      const t = [
        { x: cx - w * 0.26, y: cy - h * 0.18 }, { x: cx + w * 0.26, y: cy - h * 0.18 }, { x: cx, y: cy + h * 0.24 },
      ];
      if (type === 'vgnd') drawVGnd(ctx, p, t, 1);
      else if (type === 'nmos' || type === 'pmos') drawMosfet(ctx, Object.assign({}, p, { type }), t, 1, null);
      else drawMtjSensor(ctx, Object.assign({ freq: 1, phase: 0 }, p), t, 1, 0.15);
      return;
    }
    if (type === 'scope') {
      drawScopeProbe(ctx, Object.assign({ color: SCOPE_COLORS[0] }, p), cx, h * 0.78, 1);
      return;
    }
    if (type === 'diffscope') {
      drawDiffScopeProbe(ctx, Object.assign({ color: SCOPE_COLORS[0] }, p), w * 0.3, h * 0.78, w * 0.7, h * 0.78, 1);
      return;
    }
    if (type === 'toroid') {
      const sections = p.turnsPerSection ? p.turnsPerSection.length : 1;
      const t = [];
      for (let s = 0; s < sections; s++) {
        const ang = (Math.PI * 2 * s) / sections;
        t.push({ x: cx + Math.cos(ang) * w * 0.4, y: cy + Math.sin(ang) * h * 0.35 - 4 });
        t.push({ x: cx + Math.cos(ang) * w * 0.4, y: cy + Math.sin(ang) * h * 0.35 + 4 });
      }
      drawToroid(ctx, Object.assign({ turnsPerSection: [10], core: 'medium', spacing: 'normal' }, p), t, 1);
      return;
    }
    if (type === 'memorycore') {
      const windings = p.turnsPerWinding ? p.turnsPerWinding.length : 1;
      const t = [];
      for (let s = 0; s < windings; s++) {
        const ang = (Math.PI * 2 * s) / windings;
        t.push({ x: cx + Math.cos(ang) * w * 0.4, y: cy + Math.sin(ang) * h * 0.35 - 4 });
        t.push({ x: cx + Math.cos(ang) * w * 0.4, y: cy + Math.sin(ang) * h * 0.35 + 4 });
      }
      drawMemoryCore(ctx, Object.assign({ turnsPerWinding: [20], core: 'small' }, p), t, 1, 0);
      return;
    }
    if (type === 'comparator') {
      const colSpacing = w * 0.16;
      const startX = cx - colSpacing * 1.5;
      const topY = cy - h * 0.16;
      const botY = cy + h * 0.16;
      const t = [
        { x: startX, y: topY }, { x: startX + colSpacing, y: topY }, { x: startX + colSpacing * 2, y: topY }, { x: startX + colSpacing * 3, y: topY },
        { x: startX + colSpacing * 3, y: botY }, { x: startX + colSpacing * 2, y: botY }, { x: startX + colSpacing, y: botY }, { x: startX, y: botY },
      ];
      drawComparatorChip(ctx, p, t, 1, { out1High: false, out2High: false });
      return;
    }
    // every remaining type is a plain 2-terminal horizontal part
    const x1 = w * 0.14;
    const x2 = w * 0.86;
    if (type === 'resistor') drawResistor(ctx, Object.assign({ value: 220 }, p), x1, cy, x2, cy, 1);
    else if (type === 'led') drawLed(ctx, Object.assign({ color: 'red' }, p), x1, cy, x2, cy, 0, 1);
    else if (type === 'diode') drawDiode(ctx, p, x1, cy, x2, cy, 1);
    else if (type === 'capacitor') drawCapacitor(ctx, Object.assign({ value: 100e-6 }, p), x1, cy, x2, cy, 1);
    else if (type === 'battery') drawBattery(ctx, Object.assign({ value: 5 }, p), x1, cy, x2, cy, 1);
    else if (type === 'switch') drawSwitch(ctx, Object.assign({ closed: false }, p), x1, cy, x2, cy, 1);
    else if (type === 'pushbutton') drawPushbutton(ctx, p, x1, cy, x2, cy, 1);
    else if (type === 'inductor') drawInductor(ctx, Object.assign({ value: 10e-3 }, p), x1, cy, x2, cy, 1);
    else if (type === 'acsource') drawAcSource(ctx, Object.assign({ freq: 1 }, p), x1, cy, x2, cy, 1);
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
    PALETTE, RESISTOR_VALUES, CAPACITOR_VALUES, LED_COLORS, LED_HEX, BATTERY_VALUES, ELECTROLYTIC_THRESHOLD, WIRE_COLOR_CHOICES,
    INDUCTOR_VALUES, AC_FREQ_VALUES, SCOPE_COLORS, WIRE_GAUGES, WIRE_COLOR_NAMES, WIRE_GAUGE_OHMS_PER_M,
    TOROID_CORES, TOROID_TURNS_VALUES, TOROID_SPACING_COUPLING, MOSFET_CLASS_LABELS,
    MEMORY_CORES, MEMORY_CORE_TURNS_VALUES,
    resistorColorBands, formatOhms, formatFarads, formatHenries,
    drawResistor, drawLed, drawDiode, drawCapacitor, drawBattery,
    drawSwitch, drawPushbutton, drawPotentiometer, drawWire, drawYWire, yWireJunctions, drawVGnd, vgndCentroid, roundRect, lerp,
    potCentroid, potPosToAngle, potAngleToPos,
    drawInductor, drawAcSource, drawMtjSensor, mtjCentroid,
    drawScopeProbe, drawDiffScopeProbe, drawPartIcon,
    drawToroid, toroidCentroid,
    drawMosfet, mosfetCentroid,
    drawMemoryCore, memoryCoreCentroid,
    drawComparatorChip, comparatorCentroid,
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.Components = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
