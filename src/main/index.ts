import { writeFileSync } from 'node:fs'
import path from 'node:path'
import { electronApp, is, optimizer } from '@electron-toolkit/utils'
import { app, BrowserWindow, ipcMain, nativeImage, shell } from 'electron'
import appIcon from '../../resources/icon.png?asset'
import { killAllProcesses } from './childProcessManager'
import { getGenSettingsPath } from './getCorePath'
import { getCpuInfo, getGpuInfo } from './getSystemInfo'
import { openDirectory } from './openDirectory'
import { preview, previewFrame } from './previewOutput'
import { PauseCommand, runCommand } from './runCommand'

function createWindow(): BrowserWindow {
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 700,
    minWidth: 900,
    minHeight: 670,
    show: false,
    autoHideMenuBar: true,
    icon: nativeImage.createFromPath(appIcon),
    title: 'VSET 4.3.6',
    webPreferences: {
      preload: path.join(__dirname, '../preload/index.js'),
      sandbox: false,
    },
  })

  // ipcMain
  ipcMain.on('execute-command', runCommand)

  ipcMain.on('pause', PauseCommand)

  ipcMain.on('preview', preview)

  ipcMain.on('preview-frame', previewFrame)

  ipcMain.on('stop-all-processes', killAllProcesses)

  ipcMain.on('generate-json', (_, data) => {
    const filePath = getGenSettingsPath()
    writeFileSync(filePath, JSON.stringify(data, null, 2))
  })

  ipcMain.handle('open-folder-dialog', openDirectory)

  ipcMain.handle('get-gpu-info', getGpuInfo)

  ipcMain.handle('get-cpu-info', getCpuInfo)

  // mainWindow
  mainWindow.on('ready-to-show', () => {
    mainWindow?.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  mainWindow.on('close', async () => {
    app.quit()
  })

  if (is.dev && process.env.ELECTRON_RENDERER_URL) {
    mainWindow.loadURL(process.env.ELECTRON_RENDERER_URL)
    // mainWindow.webContents.openDevTools()
  }
  else {
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'))
  }

  return mainWindow
}

// disable hardware acceleration for Compatibility for windows
app.disableHardwareAcceleration()

// ✅ 初始化窗口和主进程监听
app.whenReady().then(() => {
  electronApp.setAppUserModelId('com.vset.ai')

  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

// ✅ 所有窗口关闭时退出（除 macOS）
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// ✅ 当用户点击任务栏关闭或调用 app.quit() 时，先清理子进程
let isQuitting = false
app.on('before-quit', async (event) => {
  if (isQuitting) {
    console.log('Quitting...')
    return
  }
  console.log('Killing child process before quitting...')
  event.preventDefault()
  isQuitting = true
  try {
    await killAllProcesses()
  }
  catch (err) {
    console.error('❌ killAllProcesses 失败：', err)
  }
  app.quit()
})
