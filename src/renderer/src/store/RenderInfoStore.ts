import { ref } from 'vue'
import { defineStore } from 'pinia'

export default defineStore('renderconfig',()=>{
  const Rending_log = ref()
  const ffmpeg_command= ref('')
  
  return {
    Rending_log,
    ffmpeg_command,
  }
})