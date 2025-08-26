export enum IpcChannelName {
  FFMPEG_OUTPUT = 'ffmpeg-output',
  VSPIPE_PID = 'vspipePID',
  FFMPEG_PID = 'ffmpegPID',
  FFMPEG_FINISHED = 'ffmpeg-finish',

  EXECUTE_COMMAND = 'execute-command',
  GENERATE_JSON = 'generate-json',

  PREVIEW_VPY_PATH = 'preview-vpyPath',
  PREVIEW_IMAGE = 'preview-image',
  PREVIEW_FRAME = 'preview-frame',
  PREVIEW_INFO = 'preview-info',
  PREVIEW = 'preview',

  PAUSE = 'pause',
  STOP_ALL_PROCESSES = 'stop-all-processes',

  OPEN_FOLDER_DIALOG = 'open-folder-dialog',
  GET_GPU_INFO = 'get-gpu-info',
  GET_CPU_INFO = 'get-cpu-info',
}
