/**
 * 渲染进程 → 主进程（invoke/handle）
 */
export enum IpcChannelInvoke {
  OPEN_DIRECTORY_DIALOG = 'ipc:open-directory-dialog',
  GET_GPU_INFO = 'ipc:get-gpu-info',
  GET_CPU_INFO = 'ipc:get-cpu-info',
  GET_MEMORY_INFO = 'ipc:get-memory-info',
  GET_EXTRA_SR_MODEL_LIST = 'ipc:get-extra-sr-model-list',
}

/**
 * 渲染进程 → 主进程（send/on，单向）
 */
export enum IpcChannelSend {
  EXECUTE_COMMAND = 'ipc:send:execute-command',
  PAUSE = 'ipc:send:pause',

  PREVIEW = 'ipc:send:preview',
  PREVIEW_FRAME = 'ipc:send:preview-frame',

  STOP_ALL_PROCESSES = 'ipc:send:stop-all-processes',

  GENERATE_JSON = 'ipc:send:generate-json',
}

/**
 * 主进程 → 渲染进程（send/on，主进程主动 emit）
 */
export enum IpcChannelOn {
  VSPIPE_PID = 'ipc:on:vspipe-pid',
  FFMPEG_PID = 'ipc:on:ffmpeg-pid',

  FFMPEG_OUTPUT = 'ipc:on:ffmpeg-output',
  FFMPEG_FINISHED = 'ipc:on:ffmpeg-finished',

  PREVIEW_VPY_PATH = 'ipc:on:preview-vpy-path',
  PREVIEW_IMAGE = 'ipc:on:preview-image',
  PREVIEW_INFO = 'ipc:on:preview-info',
}
