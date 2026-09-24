#!/usr/bin/env node
/*
 * Bundles index.html + style.css + every js/*.js file into a single,
 * self-contained HTML file with no external dependencies -- the same app,
 * just inlined so it can be dropped straight into a chat window (e.g. as a
 * Claude/ChatGPT artifact) or handed to an AI to read, run, and experiment
 * on without a server or a multi-file project.
 *
 * Usage: node build-standalone.js [output-path]   (default: dist/standalone.html)
 */
const fs = require('fs');
const path = require('path');

const root = __dirname;
const outPath = path.resolve(root, process.argv[2] || 'dist/standalone.html');

const style = fs.readFileSync(path.join(root, 'style.css'), 'utf8');
const scriptFiles = ['js/circuit.js', 'js/board.js', 'js/components.js', 'js/ai.js', 'js/app.js'];
const scripts = scriptFiles
  .map((f) => '<script>\n' + fs.readFileSync(path.join(root, f), 'utf8') + '\n</script>')
  .join('\n\n');

const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const bodyMatch = html.match(/<body>([\s\S]*?)<\/body>/);
if (!bodyMatch) throw new Error('index.html: could not find <body>...</body>');
// external script tags get replaced by the inlined versions above
const body = bodyMatch[1].replace(/<script src="js\/[a-z]+\.js"><\/script>\s*/g, '').trim();

const out = ['<title>Virtual Breadboard Simulator</title>', '<style>\n' + style + '\n</style>', body, scripts].join('\n\n');

fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, out);
console.log('Wrote', outPath, '(' + (out.length / 1024).toFixed(1) + ' KB)');
