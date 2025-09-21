import path from 'node:path'
import { electronApp, is, optimizer } from '@electron-toolkit/utils'
import { IpcChannelInvoke, IpcChannelSend } from '@shared/constant/ipc'
import { app, BrowserWindow, ipcMain, nativeImage, shell } from 'electron'
import appIcon from '../../resources/icon.png?asset'
import { killAllProcesses } from './childProcessManager'
import { getCpuInfo, getGpuInfo } from './getSystemInfo'
import { openDirectory } from './openDirectory'
import { preview, previewFrame } from './previewOutput'
import { PauseCommand, runCommand } from './runCommand'
import { writeSettingsJson } from './writeFile'

function createWindow(): BrowserWindow {
  const mainWindow = new BrowserWindow({
    width: 1000,
    height: 875,
    minWidth: 1000,
    minHeight: 875,
    show: false,
    autoHideMenuBar: true,
    frame: false,
    resizable: true,
    icon: nativeImage.createFromPath(appIcon),
    webPreferences: {
      preload: path.join(__dirname, '../preload/index.js'),
      sandbox: false,
    },
  })

  // ipcMain

  ipcMain.on('window:minimize', () => {
    mainWindow?.minimize()
  })

  ipcMain.on('window:maximize', () => {
    if (mainWindow?.isMaximized()) {
      mainWindow.unmaximize()
    }
    else {
      mainWindow?.maximize()
    }
  })

  ipcMain.on('window:close', () => {
    mainWindow?.close()
  })
  ipcMain.on(IpcChannelSend.EXECUTE_COMMAND, runCommand)

  ipcMain.on(IpcChannelSend.PAUSE, PauseCommand)

  ipcMain.on(IpcChannelSend.PREVIEW, preview)

  ipcMain.on(IpcChannelSend.PREVIEW_FRAME, previewFrame)

  ipcMain.on(IpcChannelSend.STOP_ALL_PROCESSES, killAllProcesses)

  ipcMain.on(IpcChannelSend.GENERATE_JSON, writeSettingsJson)

  ipcMain.handle(IpcChannelInvoke.OPEN_DIRECTORY_DIALOG, openDirectory)

  ipcMain.handle(IpcChannelInvoke.GET_GPU_INFO, getGpuInfo)

  ipcMain.handle(IpcChannelInvoke.GET_CPU_INFO, getCpuInfo)

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
