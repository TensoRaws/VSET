import { readdir } from 'node:fs/promises'
import si from 'systeminformation'
import { getExtraSRModelPath } from './getCorePath'

export async function getGpuInfo(): Promise<Array<string>> {
  const deviceList: Array<string> = []
  const gpus = await si.graphics()
  for (const i in gpus.controllers) {
    deviceList.push(gpus.controllers[i].model)
  }
  return deviceList
}

export async function getCpuInfo(): Promise<string> {
  const cpu = await si.cpu()
  return cpu.brand
}

export async function getMemoryInfo(): Promise<string> {
  const mem = await si.mem()
  const totalGB = (mem.total / (1024 * 1024 * 1024)).toFixed(2)
  return `${totalGB} GB`
}

export async function getExtraSRModelList(): Promise<Array<string>> {
  const modelDir = getExtraSRModelPath()
  try {
    const files = await readdir(modelDir)
    // 过滤出 .onnx 文件并去掉扩展名
    return files
      .filter(file => file.endsWith('.onnx'))
      .map(file => file.replace('.onnx', ''))
  }
  catch (error) {
    console.error('Error reading extra SR model directory:', error)
    return []
  }
}