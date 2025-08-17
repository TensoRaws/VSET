import { defineStore } from 'pinia'
import { ref } from 'vue'

export default defineStore('renderconfig', () => {
  const Rending_log = ref()
  const ffmpeg_command = ref('')

  return {
    Rending_log,
    ffmpeg_command,
  }
})
