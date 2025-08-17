import { writeFileSync } from 'node:fs'
import path from 'node:path'
import { electronApp, is, optimizer } from '@electron-toolkit/utils'
import { app, BrowserWindow, dialog, ipcMain, nativeImage, shell } from 'electron'
import appIcon from '../../resources/icon.png?asset'
import { killAllProcesses } from './childProcessManager'
import { getGenSettingsPath } from './getCorePath'
import ipc from './ipc'
import { preview, preview_frame, RunCommand } from './RunCommand'

function createWindow(): BrowserWindow {
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 700,
    minWidth: 900,
    minHeight: 670,
    show: false,
    autoHideMenuBar: true,
    icon: nativeImage.createFromPath(appIcon),
    title: 'VSET 4.2.2',
    webPreferences: {
      preload: path.join(__dirname, '../preload/index.js'),
      sandbox: false,
    },
  })

  mainWindow.on('ready-to-show', () => {
    mainWindow?.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  // ✅ 点击“关闭按钮 X”时：优雅终止进程再退出
  mainWindow.on('close', async (e) => {
    if ((app as any).isQuitting)
      return

    e.preventDefault()
    ;(app as any).isQuitting = true
    try {
      await killAllProcesses()
    }
    catch (err) {
      console.error('❌ 终止子进程时出错：', err)
    }

    // 手动退出
    app.quit()
  })

  // ✅ 加载主页面
  if (is.dev && process.env.ELECTRON_RENDERER_URL) {
    mainWindow.loadURL(process.env.ELECTRON_RENDERER_URL)
    // mainWindow.webContents.openDevTools()
  }
  else {
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'))
  }

  return mainWindow
}

// ✅ 当用户点击任务栏关闭或调用 app.quit() 时，先清理子进程
app.on('before-quit', async (event) => {
  if ((app as any).isQuitting)
    return
  event.preventDefault()
  ;(app as any).isQuitting = true

  try {
    await killAllProcesses()
  }
  catch (err) {
    console.error('❌ killAllProcesses 失败：', err)
  }

  // 退出应用（再次触发 before-quit 也无害）
  app.quit()
})

// disable hardware acceleration for Compatibility for windows
app.disableHardwareAcceleration()

// ✅ 初始化窗口和主进程监听
app.whenReady().then(() => {
  electronApp.setAppUserModelId('com.electron')

  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  ipcMain.on('execute-command', RunCommand)

  ipcMain.on('preview', preview)
  ipcMain.on('preview_frame', preview_frame)

  ipcMain.on('stop-all-processes', () => {
    killAllProcesses()
  })

  ipcMain.on('generate-json', (_, data) => {
    const filePath = getGenSettingsPath(data)
    writeFileSync(filePath, JSON.stringify(data, null, 2))
  })

  ipcMain.on('open-folder-dialog', (event) => {
    dialog
      .showOpenDialog({
        properties: ['openDirectory'],
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

  const win = createWindow()
  ipc(win)

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      const newWin = createWindow()
      ipc(newWin)
    }
  })
})

// ✅ 所有窗口关闭时退出（除 macOS）
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
