const { app, BrowserWindow, Menu, shell, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');

// classic (always-visible, space-reserving) scrollbars instead of the
// GTK-style auto-hiding overlay ones -- the toolbox sidebar's tool options
// (e.g. the toroid's 5 controls) can extend below the fold, and an overlay
// scrollbar gives no visible hint that there's more to scroll to.
app.commandLine.appendSwitch('disable-features', 'OverlayScrollbar');

const APP_SMOKE_TEST = process.argv.includes('--smoke-test');

// the renderer can only ask for this by name (see preload.js) -- validate
// it's an actual http(s) URL before ever handing it to the OS to open
ipcMain.on('open-external', (event, url) => {
  if (typeof url === 'string' && /^https:\/\//.test(url)) shell.openExternal(url);
});

// AI provider calls (js/ai.js) run as plain fetch() in the renderer, which
// works for Anthropic/Gemini but not OpenAI: api.openai.com never sends
// CORS headers for browser-origin requests, so a page-context fetch to it
// is blocked by the browser before the response body is even readable --
// this is OpenAI's own platform restriction, not something fixable with
// headers on our end. Node's fetch in the main process isn't a browser and
// has no CORS concept, so proxying the request through here (desktop app
// only -- the plain web/browser build has no main process to ask) sidesteps
// it entirely. Restricted to https:// and only reachable by our own
// first-party renderer code, same trust boundary as open-external above.
ipcMain.handle('ai-fetch', async (event, { url, options }) => {
  if (typeof url !== 'string' || !/^https:\/\//.test(url)) {
    throw new Error('ai-fetch: refusing a non-https URL');
  }
  const res = await fetch(url, options);
  const text = await res.text();
  return { ok: res.ok, status: res.status, statusText: res.statusText, text };
});

async function runDesktopSmoke(win) {
  let exportPath = null;
  const timer = setTimeout(() => {
    console.error('APP_SMOKE_FAIL timeout waiting for desktop acceptance');
    app.exit(1);
  }, 30000);

  const fail = (err) => {
    clearTimeout(timer);
    if (exportPath) { try { fs.unlinkSync(exportPath); } catch (e) { /* ignore */ } }
    console.error('APP_SMOKE_FAIL', err && err.stack ? err.stack : String(err));
    app.exit(1);
  };

  try {
    const ui = await win.webContents.executeJavaScript(`(() => ({
      title: document.title,
      canvas: !!document.getElementById('boardCanvas'),
      toolbox: !!document.getElementById('toolbox'),
      save: !!document.getElementById('btnSave'),
      load: !!document.getElementById('btnLoad'),
      exportButton: !!document.getElementById('btnExport'),
      clear: !!document.getElementById('btnClear'),
      inspector: !!document.getElementById('props'),
      scope: !!document.getElementById('scopeCanvas'),
      warnings: !!document.getElementById('warnings'),
      preset: !!document.getElementById('presetLed'),
      musicPreset: !!document.getElementById('presetMusicPickup'),
      musicHook: typeof window.__musicPresetIds === 'function',
      debug: typeof window.__debugState === 'function',
      runFast: typeof window.__runFast === 'function'
    }))()`);
    const required = ['canvas', 'toolbox', 'save', 'load', 'exportButton', 'clear', 'inspector', 'scope', 'warnings', 'preset', 'musicPreset', 'musicHook', 'debug', 'runFast'];
    const missing = required.filter((key) => !ui[key]);
    if (missing.length) throw new Error(`missing required UI/runtime hooks: ${missing.join(', ')}`);
    if (!/Virtual Breadboard Simulator/.test(ui.title)) throw new Error(`unexpected title: ${ui.title}`);

    const acceptance = await win.webContents.executeJavaScript(`(async () => {
      // Clear is a real, deliberate safety prompt for a real user
      // (window.confirm) -- app.js's own behavior is untouched. In this
      // headless acceptance run there is no user to answer it, and Electron's
      // native confirm() blocks the renderer indefinitely waiting for one, so
      // this smoke script (only) answers its own prompts affirmatively.
      window.confirm = () => true;
      localStorage.removeItem('virtual-breadboard-save');
      document.getElementById('btnClear').click();
      document.getElementById('presetLed').click();
      await new Promise((r) => setTimeout(r, 50));
      const normalize = (s) => s.parts.map((p) => ({
        type: p.type,
        value: p.value,
        color: p.color,
        closed: p.closed,
        terminals: p.terminals.map((t) => t.cellId)
      }));
      const built = window.__debugState();
      if (built.parts.length < 3) throw new Error('LED preset did not build a real circuit');
      const run1 = window.__runFast(0.02, 0.001);
      if (!run1 || !run1.voltages || Object.keys(run1.voltages).length === 0) throw new Error('simulation produced no node voltages');
      document.getElementById('btnSave').click();
      const saved = localStorage.getItem('virtual-breadboard-save');
      if (!saved) throw new Error('Save did not persist circuit state');
      document.getElementById('btnClear').click();
      if (window.__debugState().parts.length !== 0) throw new Error('Clear did not empty the board');
      document.getElementById('btnLoad').click();
      await new Promise((r) => setTimeout(r, 20));
      const loaded = window.__debugState();
      if (JSON.stringify(normalize(built)) !== JSON.stringify(normalize(loaded))) throw new Error('Load did not restore the saved circuit exactly');
      const run2 = window.__runFast(0.02, 0.001);
      if (!run2 || !run2.voltages || Object.keys(run2.voltages).length === 0) throw new Error('reloaded circuit did not simulate');

      // Every music preset is a shipping build, not a decorative button.
      // Click each one through the real UI, let its temporary Save/Load payload
      // rebuild the board, and require a live solve with no safety warnings.
      const musicIds = window.__musicPresetIds();
      if (!Array.isArray(musicIds) || musicIds.length < 5) throw new Error('music preset registry is incomplete');
      const musicRuns = [];
      for (const id of musicIds) {
        const button = document.getElementById(id);
        if (!button) throw new Error('missing music preset button: ' + id);
        button.click();
        await new Promise((r) => setTimeout(r, 20));
        const state = window.__debugState();
        if (state.parts.length < 3) throw new Error(id + ' did not build a real circuit');
        const run = window.__runFast(0.03, 0.001);
        const nodes = run && run.voltages ? Object.keys(run.voltages).length : 0;
        if (!nodes) throw new Error(id + ' produced no node voltages');
        if ((run.warnings || []).length) throw new Error(id + ' emitted warnings: ' + run.warnings.join(' | '));
        musicRuns.push({ id, parts: state.parts.length, nodes });
      }

      // Music presets deliberately preserve the user's existing Save slot.
      // Prove that invariant by loading again and getting the pre-music LED
      // build back exactly.
      document.getElementById('btnLoad').click();
      await new Promise((r) => setTimeout(r, 20));
      const restored = window.__debugState();
      if (JSON.stringify(normalize(built)) !== JSON.stringify(normalize(restored))) {
        throw new Error('music presets overwrote the user saved circuit');
      }
      const restoredRun = window.__runFast(0.02, 0.001);
      if (!restoredRun || !Object.keys(restoredRun.voltages || {}).length) throw new Error('restored circuit did not simulate after music presets');

      return {
        partCount: restored.parts.length,
        voltageNodes: Object.keys(restoredRun.voltages).length,
        warningCount: (restoredRun.warnings || []).length,
        savedBytes: saved.length,
        musicPresetCount: musicRuns.length,
        musicPresetParts: musicRuns.reduce((n, r) => n + r.parts, 0),
        musicPresetNodes: musicRuns.reduce((n, r) => n + r.nodes, 0)
      };
    })()`);

    exportPath = path.join(app.getPath('temp'), `virtual-breadboard-smoke-${process.pid}.html`);
    try { fs.unlinkSync(exportPath); } catch (e) { /* ignore */ }
    const downloadDone = new Promise((resolve, reject) => {
      const downloadTimer = setTimeout(() => reject(new Error('Export did not start')), 10000);
      win.webContents.session.once('will-download', (event, item) => {
        item.setSavePath(exportPath);
        item.once('done', (event2, state) => {
          clearTimeout(downloadTimer);
          if (state !== 'completed') reject(new Error(`Export download state: ${state}`));
          else resolve();
        });
      });
    });
    await win.webContents.executeJavaScript(`document.getElementById('btnExport').click()`);
    await downloadDone;
    const exported = fs.readFileSync(exportPath, 'utf8');
    if (exported.length < 10000) throw new Error(`Exported HTML unexpectedly small: ${exported.length} bytes`);
    if (!exported.includes('window.__EXPORT_STATE__')) throw new Error('Exported HTML is missing embedded circuit state');
    if (!exported.includes('Virtual Breadboard Simulator')) throw new Error('Exported HTML is missing the application shell');
    if (!exported.includes('__musicPresetIds')) throw new Error('Exported HTML is missing the music-lab preset module');

    clearTimeout(timer);
    try { fs.unlinkSync(exportPath); } catch (e) { /* ignore */ }
    console.log('APP_SMOKE_OK', JSON.stringify({ ...ui, ...acceptance, exportBytes: exported.length }));
    app.exit(0);
  } catch (err) {
    fail(err);
  }
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 900,
    minHeight: 600,
    backgroundColor: '#10141a',
    title: 'Virtual Breadboard Simulator',
    icon: path.join(__dirname, 'build', 'icon.png'),
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  Menu.setApplicationMenu(null);
  if (APP_SMOKE_TEST) {
    win.webContents.once('did-fail-load', (event, code, description) => {
      console.error('APP_SMOKE_FAIL', `renderer load failed ${code}: ${description}`);
      app.exit(1);
    });
    win.webContents.once('did-finish-load', () => runDesktopSmoke(win));
  }
  win.loadFile(path.join(__dirname, 'index.html'));
  return win;
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (!APP_SMOKE_TEST && BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});