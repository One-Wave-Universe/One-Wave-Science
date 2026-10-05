#!/usr/bin/env node
/*
 * Stages the existing Virtual Breadboard web app into mobile/www/ so
 * Capacitor can bundle it. Nothing is rewritten or transpiled: the files are
 * copied byte-for-byte from the same index.html / style.css / js/ that the
 * browser build and the Electron desktop build load.
 *
 * The whole js/ directory is copied (not a hard-coded list) so new engine or
 * UI files -- e.g. a perfboard layout in board.js or new js/*.js modules --
 * ship to Android automatically as soon as index.html references them.
 */
const fs = require('fs');
const path = require('path');

const appRoot = path.resolve(__dirname, '..', '..'); // Virtual_Breadboard/
const www = path.resolve(__dirname, '..', 'www');

const files = ['index.html', 'style.css', 'icon.svg'];
const dirs = ['js'];

fs.rmSync(www, { recursive: true, force: true });
fs.mkdirSync(www, { recursive: true });

for (const f of files) {
  const src = path.join(appRoot, f);
  if (!fs.existsSync(src)) {
    if (f === 'icon.svg') continue; // optional
    throw new Error('missing ' + src);
  }
  fs.copyFileSync(src, path.join(www, f));
}
for (const d of dirs) {
  fs.cpSync(path.join(appRoot, d), path.join(www, d), { recursive: true });
}

// Sanity check: every <script src> / <link href> in index.html must exist.
const html = fs.readFileSync(path.join(www, 'index.html'), 'utf8');
const refs = [...html.matchAll(/<(?:script[^>]*\ssrc|link[^>]*\shref)="([^"]+)"/g)]
  .map((m) => m[1])
  .filter((u) => !/^(https?:|data:|\/\/)/.test(u));
const missing = refs.filter((r) => !fs.existsSync(path.join(www, r)));
if (missing.length) {
  throw new Error('index.html references files not staged into www/: ' + missing.join(', '));
}
console.log('Staged web app into ' + path.relative(process.cwd(), www) + ' (' + refs.length + ' local assets verified)');
