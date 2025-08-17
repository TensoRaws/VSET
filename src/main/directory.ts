import { dialog } from 'electron'

export async function selectDirectory(): Promise<string> {
  const res = await dialog.showOpenDialog({
    title: '选择文件夹',
    properties: ['openDirectory', 'createDirectory'],
  })
  return !res.canceled ? res.filePaths[0].replace(/\\/g, '/') : ''
}
