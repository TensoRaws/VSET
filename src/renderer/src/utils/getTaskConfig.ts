import type { TaskConfig } from '@shared/type/taskConfig'
import useInputconfigStore from '@renderer/store/InputStore'
import useOutputconfigStore from '@renderer/store/OutputStore'
import { buildFFmpegCMD } from '@renderer/utils/getFFmpeg'
import { buildVpyContent } from '@renderer/utils/getVpy'
import { storeToRefs } from 'pinia'

export function buildTaskConfig(): TaskConfig {
  // Input
  const InputConfigStore = useInputconfigStore()
  const { fileList } = storeToRefs(InputConfigStore)
  const fileListNames = fileList.value.map(file => (file.path).replace(/\\/g, '/'))

  // Output
  const OutputConfigStore = useOutputconfigStore()
  const {
    audioContainer,
    isSaveAudio,
    isSaveSubtitle,
    outputFolder,
    videoContainer,
  } = storeToRefs(OutputConfigStore)

  return {
    fileList: fileListNames,
    outputFolder: outputFolder.value,
    videoContainer: videoContainer.value,
    audioContainer: audioContainer.value,
    vpyContent: buildVpyContent(),
    ffmpegCMD: buildFFmpegCMD(),
    isSaveAudio: isSaveAudio.value,
    isSaveSubtitle: isSaveSubtitle.value,
  }
}
