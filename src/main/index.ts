import { app, shell, BrowserWindow, ipcMain, dialog } from 'electron'
import { join } from 'path'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import { RunCommand } from './RunCommand'
import { killAllProcesses } from './childProcessManager'
import ipc from './ipc'

const appPath = app.getAppPath()
const path = require('path')
const fs = require('fs')

// ✅ 修改函数签名，返回 BrowserWindow
function createWindow(): BrowserWindow {
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 670,
    minWidth: 900,
    minHeight: 670,
    show: false,
    autoHideMenuBar: true,
    icon: path.join(__dirname, '../../resources/fufu.png'),
    title: 'VSET 4.0.0',
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false
    }
  })

  mainWindow.on('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })
mainWindow.on('close', () => {
    console.log('⚠ mainWindow is closing, calling app.quit()');
    killAllProcesses();
  });
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }

  // ✅ 添加 return mainWindow
  return mainWindow
}

app.on('before-quit', () => {
  console.log('⚠ 应用正在退出，终止所有子进程...');
  killAllProcesses();
});

app.whenReady().then(() => {
  electronApp.setAppUserModelId('com.electron')

  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  ipcMain.on('execute-command', RunCommand)

  ipcMain.on('stop-all-processes', () => {
  console.log('🛑 渲染进程请求终止所有子进程')
  killAllProcesses()
})
  
  ipcMain.on('generate-json', (_, data) => {
    const filePath = path.join(appPath, 'json', 'setting.json')
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2))
  })

  ipcMain.on('open-folder-dialog', (event) => {
    dialog
      .showOpenDialog({
        properties: ['openDirectory']
      })
      .then((result) => {
        if (!result.canceled) {
          event.sender.send('selected-folder', result.filePaths[0])
        }
      })
      .catch((err) => {
        console.error('Error opening folder dialog:', err)
      })
  })

  ipcMain.on('ping', () => console.log('pong'))

  ipcMain.on('upload-file', (_, filePath) => {
    console.log('File path:', filePath)
  })

  // ✅ 正确地获取 mainWindow 并传给 ipc
  const win = createWindow()
  ipc(win)

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) {
      const newWin = createWindow()
      ipc(newWin)
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
