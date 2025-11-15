// @renderer/store/SystemInfoStore.ts
import { IpcChannelInvoke } from '@shared/constant/ipc'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSystemInfoStore = defineStore('systemInfo', () => {
  const cpuInfo = ref('')
  const gpuInfo = ref<string[]>([])
  const gpuMainInfo = ref('')
  const memoryInfo = ref('')
  const extraSrModelList = ref<string[]>([])

  async function fetchCPUInfo() {
    if (!cpuInfo.value) {
      cpuInfo.value = await window.electron.ipcRenderer.invoke(IpcChannelInvoke.GET_CPU_INFO)
    }
  }

  async function fetchGPUInfo() {
    if (gpuInfo.value.length === 0) {
      gpuInfo.value = await window.electron.ipcRenderer.invoke(IpcChannelInvoke.GET_GPU_INFO)
      if (gpuInfo.value.length > 0) {
        gpuMainInfo.value = gpuInfo.value[0]
      }
    }
  }

  async function fetchMemoryInfo() {
    if (!memoryInfo.value) {
      memoryInfo.value = await window.electron.ipcRenderer.invoke(IpcChannelInvoke.GET_MEMORY_INFO)
    }
  }

  async function fetchExtraSRModelList() {
    // 每次都重新加载，以支持添加新模型文件
    extraSrModelList.value = await window.electron.ipcRenderer.invoke(IpcChannelInvoke.GET_EXTRA_SR_MODEL_LIST)
  }

  async function initSystemInfo() {
    try {
      // 只有在信息为空时才获取
      if (!cpuInfo.value || !memoryInfo.value || gpuInfo.value.length === 0) {
        // 并行获取所有信息以提高性能
        await Promise.all([fetchCPUInfo(), fetchGPUInfo(), fetchMemoryInfo()])
      }
    }
    catch (error) {
      console.error('Failed to initialize system info:', error)
    }
  }

  function setGPUMainInfo(val: string) {
    gpuMainInfo.value = val
  }

  return {
    cpuInfo,
    gpuInfo,
    gpuMainInfo,
    memoryInfo,
    extraSrModelList,
    initSystemInfo,
    setGPUMainInfo,
    fetchExtraSRModelList,
  }
}, {
  persist: true,
})

