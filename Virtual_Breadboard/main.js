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
      debug: typeof window.__debugState === 'function',
      runFast: typeof window.__runFast === 'function',
      practice: typeof window.breadboard === 'object' && ['simToggle','simReset','simStep','circuitSpec','specImport','specRead','receiptRead','simReceipt'].every(id => !!document.getElementById(id))
    }))()`);
    const required = ['canvas', 'toolbox', 'save', 'load', 'exportButton', 'clear', 'inspector', 'scope', 'warnings', 'preset', 'debug', 'runFast', 'practice'];
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
      return {
        partCount: loaded.parts.length,
        voltageNodes: Object.keys(run2.voltages).length,
        warningCount: (run2.warnings || []).length,
        savedBytes: saved.length
      };
    })()`);

    const practice = await win.webContents.executeJavaScript(`(async () => {
      const api = window.breadboard;
      const same = (a,b) => JSON.stringify(a) === JSON.stringify(b);
      document.getElementById('simReset').click();
      document.getElementById('specRead').click();
      const spec = JSON.parse(document.getElementById('circuitSpec').value);
      document.getElementById('specImport').click();
      if (api.receipt().status !== 'UNRUN' || api.receipt().running) throw new Error('JSON import did not pause');
      document.getElementById('simSeconds').value = '0.02';
      document.getElementById('simDt').value = '0.001';
      document.getElementById('simStep').click();
      const first = JSON.parse(document.getElementById('simReceipt').value);
      if (first.run.steps !== 20 || first.status !== 'MODELED') throw new Error('fixed-run button did not produce a receipt');
      await new Promise(resolve => setTimeout(resolve, 80));
      if (api.receipt().timeSeconds !== first.timeSeconds) throw new Error('paused renderer advanced simulation');
      document.getElementById('simReset').click();
      document.getElementById('simStep').click();
      const again = JSON.parse(document.getElementById('simReceipt').value);
      if (!same(first.voltages, again.voltages) || !same(first.currents, again.currents)) throw new Error('reset fixed run is not repeatable');
      const before = api.spec();
      document.getElementById('circuitSpec').value = '{bad JSON';
      document.getElementById('specImport').click();
      if (!same(before, api.spec())) throw new Error('failed import changed board');
      const malicious = JSON.parse(JSON.stringify(spec));
      malicious.parts[0].id = '<img src=x onerror=alert(1)>';
      let rejected = false;
      try { api.load(malicious); } catch (e) { rejected = true; }
      if (!rejected || !same(before, api.spec())) throw new Error('unsafe ID accepted');
      document.getElementById('specRead').click();
      document.getElementById('receiptRead').click();
      await new Promise(resolve => requestAnimationFrame(resolve));
      return { practiceChecks: 6, practiceStatus: again.status };
    })()`);
    if (process.env.BREADBOARD_SMOKE_SCREENSHOT) {
      const screenshot = await win.webContents.capturePage();
      fs.writeFileSync(process.env.BREADBOARD_SMOKE_SCREENSHOT, screenshot.toPNG());
    }

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

    clearTimeout(timer);
    try { fs.unlinkSync(exportPath); } catch (e) { /* ignore */ }
    console.log('APP_SMOKE_OK', JSON.stringify({ ...ui, ...acceptance, ...practice, exportBytes: exported.length }));
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
