const { app, BrowserWindow, Menu, shell, ipcMain } = require('electron');
const path = require('path');

// classic (always-visible, space-reserving) scrollbars instead of the
// GTK-style auto-hiding overlay ones -- the toolbox sidebar's tool options
// (e.g. the toroid's 5 controls) can extend below the fold, and an overlay
// scrollbar gives no visible hint that there's more to scroll to.
app.commandLine.appendSwitch('disable-features', 'OverlayScrollbar');

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
  win.loadFile(path.join(__dirname, 'index.html'));
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
