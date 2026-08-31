const { app, BrowserWindow, Menu, shell, ipcMain } = require('electron');
const path = require('path');

// the renderer can only ask for this by name (see preload.js) -- validate
// it's an actual http(s) URL before ever handing it to the OS to open
ipcMain.on('open-external', (event, url) => {
  if (typeof url === 'string' && /^https:\/\//.test(url)) shell.openExternal(url);
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
