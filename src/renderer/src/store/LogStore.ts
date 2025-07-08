import { defineStore } from 'pinia'

export const useLogStore = defineStore('log', {
  state: () => ({
    logs: '' as string,
  }),
  actions: {
    appendLog(message: string) {
      // 可选：去除 ANSI 控制字符
      const cleanMessage = message.replace(/\x1b\[[0-9;]*m/g, '')
      if (cleanMessage.startsWith('[Progress_vspipe_ffmpeg]')) {
    // 删除旧的 Progress 行
    this.logs = this.logs.replace(/\[Progress_vspipe_ffmpeg\].*\n?$/, '')
  }
  this.logs += cleanMessage
    },
    clearLog() {
      this.logs = ''
    }
  }
})
