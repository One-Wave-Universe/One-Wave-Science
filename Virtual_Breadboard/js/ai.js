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
      '  wire          2 terminals, no value/color needed (a zero-resistance jumper)',
      '  resistor      2 terminals, "value" in ohms, e.g. 220, 1000, 10000',
      '  led           2 terminals, "color" one of red/yellow/green/blue/white (terminals[0] is the anode/+)',
      '  capacitor     2 terminals, "value" in farads, e.g. 0.0001 for 100uF',
      '  battery       2 terminals, "value" in volts, e.g. 5 or 9 (terminals[0] is +, terminals[1] is -)',
      '  switch        2 terminals, optional "closed": true or false (defaults to open)',
      '  potentiometer 3 terminals in order [end A, wiper, end B], "value" is total ohms',
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

  async function callAnthropic({ apiKey, model, userText }) {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
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
    const res = await fetch('https://api.openai.com/v1/chat/completions', {
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

  const PROVIDERS = { anthropic: callAnthropic, openai: callOpenAI, custom: callCustom };

  function extractJson(text) {
    const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/i);
    const body = fenced ? fenced[1] : text;
    const start = body.indexOf('{');
    const end = body.lastIndexOf('}');
    if (start === -1 || end === -1) throw new Error('No JSON object found in the AI response: ' + text.slice(0, 200));
    return JSON.parse(body.slice(start, end + 1));
  }

  const TERMINALS_NEEDED = { wire: 2, resistor: 2, led: 2, capacitor: 2, battery: 2, switch: 2, potentiometer: 3 };
  const VALID_ROWS = new Set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'railTP', 'railTM', 'railBP', 'railBM']);
  const LED_COLORS = new Set(['red', 'yellow', 'green', 'blue', 'white']);
  const NUMERIC_TYPES = new Set(['resistor', 'capacitor', 'battery', 'potentiometer']);

  // evaluator: is this a structurally legal circuit spec? This checks shape
  // and range only — whether the resulting circuit is safe/complete is the
  // simulator's own job once the parts are actually on the board.
  function validateSpec(spec) {
    const errors = [];
    const parts = spec && Array.isArray(spec.parts) ? spec.parts : null;
    if (!parts) return { ok: false, errors: ['Response has no "parts" array.'], parts: [] };
    if (!parts.length) errors.push('The "parts" array is empty.');
    parts.forEach((p, i) => {
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
    });
    return { ok: errors.length === 0, errors, parts };
  }

  const api = { systemPrompt, PROVIDERS, extractJson, validateSpec };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.AIBuilder = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
