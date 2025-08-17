import type { BrowserWindow } from 'electron'
import { ipcMain } from 'electron'
import { selectDirectory } from './directory'
import { getCpuInfo, getGpuInfo } from './getSystemInfo'

export default (_win: BrowserWindow): void => {
  ipcMain.handle('selectDirectory', async () => {
    return selectDirectory()
  })

  ipcMain.handle('getGpuInfo', async () => {
    return getGpuInfo()
  })

  ipcMain.handle('getCpuInfo', async () => {
    return getCpuInfo()
  })
}
