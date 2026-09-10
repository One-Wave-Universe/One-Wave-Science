const { app, BrowserWindow, Menu, shell, ipcMain } = require('electron');
const path = require('path');

// classic (always-visible, space-reserving) scrollbars instead of the
// GTK-style auto-hiding overlay ones -- the toolbox sidebar's tool options
// can extend below the fold, and an overlay scrollbar gives no visible hint
// that there's more to scroll to.
app.commandLine.appendSwitch('disable-features', 'OverlayScrollbar');

const APP_SMOKE_TEST = process.argv.includes('--smoke-test');

// the renderer can only ask for this by name (see preload.js) -- validate
// it's an actual https URL before ever handing it to the OS to open.
ipcMain.on('open-external', (event, url) => {
  if (typeof url === 'string' && /^https:\/\//.test(url)) shell.openExternal(url);
});

// AI provider calls (js/ai.js) run as plain fetch() in the renderer, which
// works for Anthropic/Gemini but not providers that reject browser CORS.
// Node's fetch in the main process has no browser CORS boundary, so the
// desktop app proxies only explicit https requests from its own renderer.
ipcMain.handle('ai-fetch', async (event, { url, options }) => {
  if (typeof url !== 'string' || !/^https:\/\//.test(url)) {
    throw new Error('ai-fetch: refusing a non-https URL');
  }
  const res = await fetch(url, options);
  const text = await res.text();
  return { ok: res.ok, status: res.status, statusText: res.statusText, text };
});

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
    let finished = false;
    const fail = (reason) => {
      if (finished) return;
      finished = true;
      console.error('APP_SMOKE_FAIL', reason);
      app.exit(1);
    };
    const timer = setTimeout(() => fail('timeout waiting for renderer'), 15000);

    win.webContents.once('did-fail-load', (event, code, description) => {
      clearTimeout(timer);
      fail(`renderer load failed ${code}: ${description}`);
    });

    win.webContents.once('did-finish-load', async () => {
      try {
        const state = await win.webContents.executeJavaScript(`(() => ({
          title: document.title,
          canvas: !!document.getElementById('boardCanvas'),
          toolbox: !!document.getElementById('toolbox'),
          save: !!document.getElementById('btnSave'),
          load: !!document.getElementById('btnLoad'),
          exportButton: !!document.getElementById('btnExport'),
          inspector: !!document.getElementById('props'),
          scope: !!document.getElementById('scopeCanvas')
        }))()`);
        const required = ['canvas', 'toolbox', 'save', 'load', 'exportButton', 'inspector', 'scope'];
        const missing = required.filter((key) => !state[key]);
        if (missing.length) throw new Error(`missing required UI: ${missing.join(', ')}`);
        if (!/Virtual Breadboard Simulator/.test(state.title)) throw new Error(`unexpected title: ${state.title}`);
        finished = true;
        clearTimeout(timer);
        console.log('APP_SMOKE_OK', JSON.stringify(state));
        app.exit(0);
      } catch (err) {
        clearTimeout(timer);
        fail(err && err.stack ? err.stack : String(err));
      }
    });
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
