import { defineStore } from 'pinia'
// src/renderer/store/InputStore.ts
import { ref } from 'vue'

export interface FileWithPath extends File {
  path: string
}

export default defineStore('inputConfig', () => {
  const fileList = ref<FileWithPath[]>([])

  return {
    fileList,
  }
})
