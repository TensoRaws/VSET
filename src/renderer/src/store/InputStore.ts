import { defineStore } from 'pinia'
import { ref } from 'vue'

export default defineStore('inputConfig', () => {
  const fileList = ref<{ path: string }[]>([])

  return {
    fileList,
  }
})
