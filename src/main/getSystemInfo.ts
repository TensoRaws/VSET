import si from 'systeminformation'

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