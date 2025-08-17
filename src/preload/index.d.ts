import { ElectronAPI } from '@electron-toolkit/preload'

declare global {
  interface Window {
    electron: ElectronAPI
    api: {
      selectDirectory:() => Promise<any>
      getCpuInfo:() => Promise<Array<string>>
      getGpuInfo:() => Promise<Array<string>>
    }
  }
}
 