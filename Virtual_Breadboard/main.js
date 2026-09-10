const { app, BrowserWindow, Menu, shell, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');

app.commandLine.appendSwitch('disable-features', 'OverlayScrollbar');

const APP_SMOKE_TEST = process.argv.includes('--smoke-test');

ipcMain.on('open-external', (event, url) => {
  if (typeof url === 'string' && /^https:\/\//.test(url)) shell.openExternal(url);
});

ipcMain.handle('ai-fetch', async (event, { url, options }) => {
  if (typeof url !== 'string' || !/^https:\/\//.test(url)) {
    throw new Error('ai-fetch: refusing a non-https URL');
  }
  const res = await fetch(url, options);
  const text = await res.text();
  return { ok: res.ok, status: res.status, statusText: res.statusText, text };
});

async function installPedalLab(win) {
  const scripts = ['circle-fifths-tuner.js', 'pedal-lab.js'];
  for (const name of scripts) {
    const source = fs.readFileSync(path.join(__dirname, 'js', name), 'utf8');
    await win.webContents.executeJavaScript(source, true);
  }
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 900,
    minHeight: 600,
    backgroundColor: '#10141a',
    title: 'Star Forge Digital Bread Board',
    icon: path.join(__dirname, 'build', 'icon.png'),
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  Menu.setApplicationMenu(null);

  win.webContents.on('did-finish-load', () => {
    installPedalLab(win).catch((err) => console.error('PEDAL_LAB_LOAD_FAIL', err));
  });

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
        await new Promise((resolve) => setTimeout(resolve, 100));
        const state = await win.webContents.executeJavaScript(`(() => ({
          title: document.title,
          canvas: !!document.getElementById('boardCanvas'),
          toolbox: !!document.getElementById('toolbox'),
          save: !!document.getElementById('btnSave'),
          load: !!document.getElementById('btnLoad'),
          exportButton: !!document.getElementById('btnExport'),
          inspector: !!document.getElementById('props'),
          scope: !!document.getElementById('scopeCanvas'),
          pedalLab: !!document.getElementById('pedalLabLauncher'),
          tunerCore: !!globalThis.CircleFifthsTuner
        }))()`);
        const required = ['canvas', 'toolbox', 'save', 'load', 'exportButton', 'inspector', 'scope', 'pedalLab', 'tunerCore'];
        const missing = required.filter((key) => !state[key]);
        if (missing.length) throw new Error(`missing required UI: ${missing.join(', ')}`);
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
