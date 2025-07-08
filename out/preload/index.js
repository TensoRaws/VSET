"use strict";
const electron = require("electron");
const preload = require("@electron-toolkit/preload");
const api = {
  selectDirectory: () => {
    return electron.ipcRenderer.invoke("selectDirectory");
  },
  getCpuInfo: () => {
    return electron.ipcRenderer.invoke("getCpuInfo");
  },
  getGpuInfo: () => {
    return electron.ipcRenderer.invoke("getGpuInfo");
  }
};
if (process.contextIsolated) {
  try {
    electron.contextBridge.exposeInMainWorld("electron", preload.electronAPI);
    electron.contextBridge.exposeInMainWorld("api", api);
  } catch (error) {
    console.error(error);
  }
} else {
  window.electron = preload.electronAPI;
  window.api = api;
}
