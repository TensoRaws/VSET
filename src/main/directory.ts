import { dialog } from 'electron'

export const selectDirectory = async () => {
  const res = await dialog.showOpenDialog({
    title: '选择文件夹',
    properties: ['openDirectory', 'createDirectory']
  })
  return res.canceled === false ? res.filePaths[0].replace(/\\/g, '/') : ''
}