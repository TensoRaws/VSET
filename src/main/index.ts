import { app, shell, BrowserWindow, ipcMain, dialog } from 'electron'
import { join } from 'path'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import { RunCommand } from './RunCommand'
import { killAllProcesses } from './childProcessManager'
import ipc from './ipc'

const appPath = app.getAppPath()
const path = require('path')
const fs = require('fs')

let mainWindow: BrowserWindow | null = null

function createWindow(): BrowserWindow {
  mainWindow = new BrowserWindow({
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
    mainWindow?.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  // ✅ 点击“关闭按钮 X”时：优雅终止进程再退出
  mainWindow.on('close', async (e) => {
    if ((app as any).isQuitting) return

    e.preventDefault()
    ;(app as any).isQuitting = true

    console.log('🛑 窗口关闭中，正在终止子进程...')
    try {
      await killAllProcesses()
      console.log('✅ 所有子进程已终止，准备退出应用')
    } catch (err) {
      console.error('❌ 终止子进程时出错：', err)
    }

    // 手动退出
    app.quit()
  })

  // ✅ 加载主页面
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }

  return mainWindow
}

// ✅ 当用户点击任务栏关闭或调用 app.quit() 时，先清理子进程
app.on('before-quit', async (event) => {
  if ((app as any).isQuitting) return
  event.preventDefault()
  ;(app as any).isQuitting = true

  try {
    await killAllProcesses()
  } catch (err) {
    console.error('❌ killAllProcesses 失败：', err)
  }

  // 退出应用（再次触发 before-quit 也无害）
  app.quit()
})

// ✅ 初始化窗口和主进程监听
app.whenReady().then(() => {
  electronApp.setAppUserModelId('com.electron')

  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  ipcMain.on('execute-command', RunCommand)

  ipcMain.on('stop-all-processes', () => {
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
