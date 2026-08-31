const { contextBridge, ipcRenderer } = require('electron');

// exposes exactly one narrow capability to the renderer: ask the main
// process to open a URL in the user's real default browser. Nothing else
// from Node/Electron is exposed, keeping the sandboxed renderer's access
// as small as possible.
contextBridge.exposeInMainWorld('electronAPI', {
  openExternal: (url) => ipcRenderer.send('open-external', url),
});
