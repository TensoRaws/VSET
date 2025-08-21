// @renderer/store/AppStore.ts
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    isRunning: false,
    isPause: true,
    vspipePID: 0,
    ffmpegPID: 0,
  }),
  actions: {
    setRunning(val: boolean) {
      this.isRunning = val
    },
    setPause(val: boolean) {
      this.isPause = val
    },
    setVspipePID(val: number) {
      this.vspipePID = val
    },
    setFfmpegPID(val: number) {
      this.ffmpegPID = val
    },
  },
})
