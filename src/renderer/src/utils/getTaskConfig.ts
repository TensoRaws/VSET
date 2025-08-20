import type { TaskConfig } from '@renderer/type/taskConfig'

// 引入 store
import useInputconfigStore from '@renderer/store/InputStore'
import useOutputconfigStore from '@renderer/store/OutputStore'

import { storeToRefs } from 'pinia'

// ✅ 生成 JSON 数据的函数
export function buildTaskConfig(): TaskConfig {
  // Input
  const InputConfigStore = useInputconfigStore()
  const { fileList } = storeToRefs(InputConfigStore)
  const fileListNames = fileList.value.map(file => (file.path).replace(/\\/g, '/'))

  // Output
  const OutputConfigStore = useOutputconfigStore()
  const {
    AudioContainer,
    isSaveAudio,
    isSaveSubtitle,
    outputFolder,
    videoContainer,
  } = storeToRefs(OutputConfigStore)

  // ✅ 返回 JSON 对象
  return {
    fileList: fileListNames,
    AudioContainer: AudioContainer.value,
    isSaveAudio: isSaveAudio.value,
    isSaveSubtitle: isSaveSubtitle.value,
    outputFolder: outputFolder.value,
    videoContainer: videoContainer.value,
  }
}
