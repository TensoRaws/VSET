export interface TaskConfig {
  fileList: string[]
  outputFolder: string
  videoContainer: string
  audioContainer: string
  vpyContent: string
  ffmpegCMD: string[]
  isSaveAudio: boolean
  isSaveSubtitle: boolean
}
