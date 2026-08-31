/*
 * Pluggable AI backend for "describe a circuit in words, build it on the
 * board." Any provider that can take a system prompt + a user message and
 * return text can be plugged in here — the rest of the app only ever sees
 * a validated parts list, the same shape the hardcoded example presets use.
 *
 * Nothing here ever talks to Anthropic on this app's behalf: the browser
 * running this code calls the provider the *user* configured, with the API
 * key *they* typed in, stored only in that browser's localStorage.
 */
(function (root) {
  'use strict';

  function systemPrompt() {
    return [
      'You are a circuit-design assistant for a virtual breadboard simulator.',
      'The board has 63 numbered columns (1-63) and these rows:',
      '  a, b, c, d, e   top terminal strip. All 5 holes in the same column are one electrical node.',
      '  f, g, h, i, j   bottom terminal strip, same rule, but NOT connected to the top strip in that column.',
      '  There is a center gap between row e and row f. A part can straddle it, or a jumper wire can cross it.',
      '  railTP, railTM  top power rails (+ and -). Each rail is ONE node for its ENTIRE length, any column.',
      '  railBP, railBM  bottom power rails (+ and -), same rule.',
      '',
      "Given the user's request, reply with ONLY a JSON object, no prose and no markdown code fences, of exactly this shape:",
      '{"parts": [ {"type": "resistor", "value": 220, "terminals": [{"row":"c","col":10},{"row":"c","col":15}]} ]}',
      '',
      'Rules for "type" and how many terminals each needs:',
      '  wire          2 terminals, no value needed (a zero-resistance jumper)',
      '  ywire         4 terminals [end1A, end1B, end2A, end2B]: a standalone wire bridging two',
      '                rows, forked to 2 holes at each end (a V/Y shape). All 4 holes end up as',
      '                one electrical node — use this instead of separate wires when one node',
      '                (e.g. ground) needs to reach 2 points on one side and 2 more on the other.',
      '  resistor      2 terminals, "value" in ohms, e.g. 220, 1000, 10000',
      '  led           2 terminals, "color" one of red/yellow/green/blue/white (terminals[0] is the anode/+)',
      '  diode         2 terminals, a generic silicon rectifier, no value/color (terminals[0] is the anode/+)',
      '  capacitor     2 terminals, "value" in farads, e.g. 0.0001 for 100uF',
      '  battery       2 terminals, "value" in volts, e.g. 5 or 9 (terminals[0] is +, terminals[1] is -)',
      '  switch        2 terminals, optional "closed": true or false (defaults to open)',
      '  pushbutton    2 terminals, momentary — only conducts while "closed": true',
      '  potentiometer 1 terminal: an anchor hole in row a-e or f-j (not a rail), column 1-61.',
      '                It is a real 6-pin part: the simulator places 5 more pins for you,',
      '                mirrored in the corresponding row of the OTHER bank (a<->f, b<->g, c<->h,',
      '                d<->i, e<->j) to straddle the center channel, so leave those 6 holes clear.',
      '                "value" is total ohms.',
      '  vgnd          3 terminals [railA, railB, out]: a virtual-ground / rail-splitter. Its "out"',
      '                node is always forced to the midpoint voltage between railA and railB — e.g.',
      '                splitting a 9V battery gives a 4.5V virtual ground (V0) usable as a 0V',
      '                reference for a bipolar/split -4.5V/0V/+4.5V power scheme. No value needed.',
      '  inductor      2 terminals, "value" in henries, e.g. 0.001 for 1mH, 0.01 for 10mH. Real AC/',
      '                transient behavior (backward-Euler), not just a wire.',
      '  acsource      2 terminals, real time-varying AC (not a single-frequency snapshot): "value"',
      '                is peak amplitude in volts, "freq" in Hz (default 1), optional "phase" in',
      '                degrees (default 0). terminals[0] is the reference/+ side.',
      '  mtjsensor     3 terminals [ref, sinOut, cosOut]: a rotary angle-sensor IC (real MTJ/TMR-class',
      '                hardware, e.g. AS5047P/TLE5012). Outputs sin(theta) and cos(theta) of a',
      '                rotating field referenced to "ref", "value" = peak amplitude in volts,',
      '                "freq" = rotation rate in Hz (default 1). Use with a vgnd on "ref" for a',
      '                proper bipolar sensor reference.',
      '  scope         1 terminal: a zero-load probe tap for visualizing a node on the Oscilloscope',
      '                panel. Never affects the circuit. No value needed.',
      '  toroid        A ferrite-core inductor/transformer. Terminals = 2 per winding "section"',
      '                (1-3 sections): [s1a,s1b] or [s1a,s1b,s2a,s2b] etc. Needs a "turns" array,',
      '                one positive integer per section (e.g. [10,20] for a 1:2-turns-ratio',
      '                transformer). Optional "core": "small"/"medium"/"large" (default "medium",',
      '                bigger = more inductance per turn), "gauge": "thin"/"standard"/"thick"',
      '                (default "standard", affects winding resistance), "spacing":',
      '                "tight"/"normal"/"wide" (default "normal", only matters with 2+ sections --',
      '                how tightly coupled the windings are to each other). One section behaves like',
      '                a plain inductor; 2+ sections are real mutual-inductance-coupled windings on',
      '                one core (an actual transformer, including turns-ratio voltage transformation).',
      '',
      'Build a real, working circuit: a battery needs a closed path back to itself through the other parts.',
      'Use wires to connect parts that do not already share a node.',
      'Only include parts the user actually asked for.',
    ].join('\n');
  }

  async function readError(res) {
    let body = '';
    try { body = (await res.text()).slice(0, 300); } catch (e) { /* ignore */ }
    return res.status + ' ' + res.statusText + (body ? ': ' + body : '');
  }

  // Some providers (OpenAI's chat completions endpoint, notably) never send
  // CORS headers for browser-origin requests, so a plain page-context
  // fetch() to them is blocked before the response body is even readable --
  // that's OpenAI's own platform restriction, not something fixable with
  // request headers here. In the desktop app, main.js exposes a fetch that
  // runs in the Node/main process instead (no CORS concept there), routed
  // through this helper transparently; the plain browser/web build has no
  // such bridge and falls back to a normal fetch, which still works fine
  // for the providers that DO allow direct browser calls (Anthropic, Gemini).
  async function doFetch(url, options) {
    if (typeof window !== 'undefined' && window.electronAPI && window.electronAPI.aiFetch) {
      const { ok, status, statusText, text } = await window.electronAPI.aiFetch(url, options);
      return { ok, status, statusText, text: async () => text, json: async () => JSON.parse(text) };
    }
    return fetch(url, options);
  }

  async function callAnthropic({ apiKey, model, userText }) {
    const res = await doFetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
        // Anthropic's documented opt-in for calling the Messages API directly
        // from a browser (instead of through your own backend).
        'anthropic-dangerous-direct-browser-access': 'true',
      },
      body: JSON.stringify({
        model: model || 'claude-sonnet-4-5',
        max_tokens: 2048,
        system: systemPrompt(),
        messages: [{ role: 'user', content: userText }],
      }),
    });
    if (!res.ok) throw new Error('Anthropic API error ' + (await readError(res)));
    const data = await res.json();
    return (data.content || []).map((b) => b.text || '').join('');
  }

  async function callOpenAI({ apiKey, model, userText }) {
    const res = await doFetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        authorization: 'Bearer ' + apiKey,
      },
      body: JSON.stringify({
        model: model || 'gpt-4o-mini',
        messages: [
          { role: 'system', content: systemPrompt() },
          { role: 'user', content: userText },
        ],
      }),
    });
    if (!res.ok) throw new Error('OpenAI API error ' + (await readError(res)));
    const data = await res.json();
    return (data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content) || '';
  }

  async function callGemini({ apiKey, model, userText }) {
    const m = model || 'gemini-2.5-flash';
    const res = await doFetch(
      'https://generativelanguage.googleapis.com/v1beta/models/' + encodeURIComponent(m) + ':generateContent?key=' + encodeURIComponent(apiKey),
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          system_instruction: { parts: [{ text: systemPrompt() }] },
          contents: [{ role: 'user', parts: [{ text: userText }] }],
        }),
      }
    );
    if (!res.ok) throw new Error('Gemini API error ' + (await readError(res)));
    const data = await res.json();
    const parts = (data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts) || [];
    return parts.map((p) => p.text || '').join('');
  }

  // Any OpenAI-chat-completions-compatible endpoint: a local Ollama/LM Studio
  // server, a self-hosted proxy, another vendor's compatible API, etc.
  async function callCustom({ endpoint, apiKey, model, userText }) {
    if (!endpoint) throw new Error('No endpoint URL configured for the custom provider.');
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: Object.assign(
        { 'content-type': 'application/json' },
        apiKey ? { authorization: 'Bearer ' + apiKey } : {}
      ),
      body: JSON.stringify({
        model: model || 'default',
        messages: [
          { role: 'system', content: systemPrompt() },
          { role: 'user', content: userText },
        ],
      }),
    });
    if (!res.ok) throw new Error('Custom endpoint error ' + (await readError(res)));
    const data = await res.json();
    if (data.choices && data.choices[0] && data.choices[0].message) return data.choices[0].message.content || '';
    if (data.content && data.content[0] && data.content[0].text) return data.content[0].text;
    return JSON.stringify(data).slice(0, 500);
  }

  const PROVIDERS = { anthropic: callAnthropic, openai: callOpenAI, gemini: callGemini, custom: callCustom };

  function extractJson(text) {
    const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/i);
    const body = fenced ? fenced[1] : text;
    const start = body.indexOf('{');
    const end = body.lastIndexOf('}');
    if (start === -1 || end === -1) throw new Error('No JSON object found in the AI response: ' + text.slice(0, 200));
    return JSON.parse(body.slice(start, end + 1));
  }

  const TERMINALS_NEEDED = {
    wire: 2, ywire: 4, resistor: 2, led: 2, diode: 2, capacitor: 2, battery: 2, switch: 2, pushbutton: 2,
    potentiometer: 1, vgnd: 3, inductor: 2, acsource: 2, mtjsensor: 3, scope: 1,
  };
  const VALID_ROWS = new Set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'railTP', 'railTM', 'railBP', 'railBM']);
  const STRIP_ROWS = new Set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']);
  const LED_COLORS = new Set(['red', 'yellow', 'green', 'blue', 'white']);
  const NUMERIC_TYPES = new Set(['resistor', 'capacitor', 'battery', 'potentiometer', 'inductor', 'acsource', 'mtjsensor']);

  // evaluator: is this a structurally legal circuit spec? This checks shape
  // and range only — whether the resulting circuit is safe/complete is the
  // simulator's own job once the parts are actually on the board.
  function validateSpec(spec) {
    const errors = [];
    const parts = spec && Array.isArray(spec.parts) ? spec.parts : null;
    if (!parts) return { ok: false, errors: ['Response has no "parts" array.'], parts: [] };
    if (!parts.length) errors.push('The "parts" array is empty.');
    parts.forEach((p, i) => {
      if (p && p.type === 'toroid') {
        const turns = Array.isArray(p.turns) ? p.turns : null;
        if (!turns || !turns.length || turns.length > 3) {
          errors.push('part ' + i + ' (toroid): needs a "turns" array of 1-3 positive integers (one per winding section)');
          return;
        }
        if (turns.some((n) => !(Number(n) > 0))) errors.push('part ' + i + ' (toroid): all turns counts must be positive');
        const needT = turns.length * 2;
        if (!Array.isArray(p.terminals) || p.terminals.length !== needT) {
          errors.push('part ' + i + ' (toroid): needs ' + needT + ' terminals (2 per winding section), got ' + (p.terminals ? p.terminals.length : 0));
          return;
        }
        p.terminals.forEach((t, j) => {
          if (!t || !VALID_ROWS.has(t.row)) errors.push('part ' + i + ' terminal ' + j + ': bad row "' + (t && t.row) + '"');
          if (!t || !Number.isInteger(t.col) || t.col < 1 || t.col > 63) errors.push('part ' + i + ' terminal ' + j + ': bad col ' + (t && t.col));
        });
        return;
      }
      const need = TERMINALS_NEEDED[p && p.type];
      if (!need) {
        errors.push('part ' + i + ': unknown type "' + (p && p.type) + '"');
        return;
      }
      if (!Array.isArray(p.terminals) || p.terminals.length !== need) {
        errors.push('part ' + i + ' (' + p.type + '): needs ' + need + ' terminals, got ' + (p.terminals ? p.terminals.length : 0));
        return;
      }
      p.terminals.forEach((t, j) => {
        if (!t || !VALID_ROWS.has(t.row)) errors.push('part ' + i + ' terminal ' + j + ': bad row "' + (t && t.row) + '"');
        if (!t || !Number.isInteger(t.col) || t.col < 1 || t.col > 63) errors.push('part ' + i + ' terminal ' + j + ': bad col ' + (t && t.col));
      });
      if (p.type === 'led' && p.color && !LED_COLORS.has(p.color)) errors.push('part ' + i + ': bad led color "' + p.color + '"');
      if (NUMERIC_TYPES.has(p.type) && !(Number(p.value) > 0)) errors.push('part ' + i + ' (' + p.type + '): needs a positive numeric value');
      if (p.type === 'potentiometer') {
        const t = p.terminals[0];
        if (t && !STRIP_ROWS.has(t.row)) errors.push('part ' + i + ' (potentiometer): anchor must be in row a-j, not a rail ("' + t.row + '")');
        if (t && Number.isInteger(t.col) && t.col > 61) errors.push('part ' + i + ' (potentiometer): anchor column ' + t.col + ' leaves no room for its other 2 columns (max 61)');
      }
    });
    return { ok: errors.length === 0, errors, parts };
  }

  const api = { systemPrompt, PROVIDERS, extractJson, validateSpec };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.AIBuilder = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
