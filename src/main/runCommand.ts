import type { TaskConfig } from '@shared/type/taskConfig'
import type { IpcMainEvent } from 'electron'
import type { Buffer } from 'node:buffer'
import { exec as execCallback, spawn } from 'node:child_process'
import path from 'node:path'
import { promisify } from 'node:util'
import { IpcChannelOn } from '@shared/constant/ipc'
import { MagicStr } from '@shared/constant/magicStr'
import iconv from 'iconv-lite'
import { addProcess, removeProcess } from './childProcessManager'
import { getCorePath, getExecPath, getGenVpyPath } from './getCorePath'
import { writeVpyFile } from './writeFile'

const exec = promisify(execCallback)

function splitArgs(str: string): string[] {
  const matches = str.match(/"[^"]+"|\S+/g)
  return matches ? matches.map(s => s.replace(/^"|"$/g, '')) : []
}

// 中断循环
let shouldStop = false

export function requestStop(): void {
  shouldStop = true
}

function generate_cmd(taskConfig: TaskConfig, hasAudio: boolean, hasSubtitle: boolean): string {
  let cmd = ''
  if (hasAudio) {
    cmd += '"-map" "1:a" '
    if (taskConfig.isSaveAudio) {
      cmd += '"-c:a" "copy" '
    }
    else {
      cmd += `"-c:a" ` + `"${taskConfig.audioContainer.toLowerCase()}" `
    }
  }
  if (hasSubtitle && taskConfig.isSaveSubtitle) {
    cmd += '"-map" "1:s" "-c:s" "copy" '
  }
  return cmd
}

// 新增：获取输入视频信息的独立函数
async function getInputVideoInfo(event: IpcMainEvent, video: string): Promise<{
  hasAudio: boolean
  hasSubtitle: boolean
  videoStream: any
}> {
  const ffprobePath = getExecPath().ffprobe

  const ffprobeCommand = `"${ffprobePath}" -v error -show_streams -of json "${video}"`
  const { stdout: probeOut } = await exec(ffprobeCommand)
  const metadata = JSON.parse(probeOut)

  const allStreams = metadata.streams || []
  const videoStream = allStreams.find((s: any) => s.codec_type === 'video')
  const hasAudio = allStreams.some((s: any) => s.codec_type === 'audio')
  const hasSubtitle = allStreams.some((s: any) => s.codec_type === 'subtitle')

  if (videoStream) {
    const frameCount = videoStream.nb_frames || '未知'
    const frameRate = videoStream.avg_frame_rate || '未知'
    const resolution = `${videoStream.width}x${videoStream.height}`
    const audioText = hasAudio ? '是' : '否'
    const subtitleText = hasSubtitle ? '是' : '否'

    event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `正在处理输入视频 ${video} 的信息:\n`)
    event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `帧数(输入): ${frameCount}\n`)
    event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `帧率(输入): ${frameRate}\n`)
    event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `分辨率(输入): ${resolution}\n`)
    event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `是否含有音频: ${audioText}\n`)
    event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `是否含有字幕: ${subtitleText}\n`)
  }

  return {
    hasAudio,
    hasSubtitle,
    videoStream,
  }
}

// 新增：获取输出视频信息的独立函数
async function getOutputVideoInfo(event: IpcMainEvent, vpyPath: string): Promise<{
  width: string
  height: string
  frames: string
  fps: string
}> {
  const vspipePath = getExecPath().vspipe

  const info: {
    width: string
    height: string
    frames: string
    fps: string
  } = {
    width: '未知',
    height: '未知',
    frames: '0',
    fps: '0',
  }

  await new Promise<void>((resolve, reject) => {
    const vspipeInfoProcess = spawn(vspipePath, ['--info', vpyPath])
    addProcess('vspipe', vspipeInfoProcess)

    let vspipeOut = '' // 用于保存 stdout 内容
    // eslint-disable-next-line unused-imports/no-unused-vars
    let stderrOut = '' // 用于保存 stderr 内容

    vspipeInfoProcess.stdout.on('data', (data: Buffer) => {
      const str = iconv.decode(data, 'gbk')
      vspipeOut += str
      event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `${str}`)
    })

    vspipeInfoProcess.stderr.on('data', (data: Buffer) => {
      const str = iconv.decode(data, 'gbk')
      stderrOut += str
      event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `${str}`)
    })

    vspipeInfoProcess.on('close', (code) => {
      removeProcess(vspipeInfoProcess)
      event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `vspipe info 执行完毕，退出码: ${code}\n`)

      info.width = vspipeOut.match(/Width:\s*(\d+)/)?.[1] || '未知'
      info.height = vspipeOut.match(/Height:\s*(\d+)/)?.[1] || '未知'
      info.frames = vspipeOut.match(/Frames:\s*(\d+)/)?.[1] || '0'
      info.fps = vspipeOut.match(/FPS:\s*([\d/]+)\s*\(([\d.]+) fps\)/)?.[2] || '0'

      event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `======= 输出视频信息 =======\n`)
      event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `宽: ${info.width}\n`)
      event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `高: ${info.height}\n`)
      event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `帧数: ${info.frames}\n`)
      event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `帧率: ${info.fps}\n`)
      resolve()
    })

    vspipeInfoProcess.on('error', (err) => {
      event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `vspipe 执行出错: ${err.message}\n`)
      reject(err)
    })
  })

  return info
}

export async function runCommand(event: IpcMainEvent, taskConfig: TaskConfig): Promise<void> {
  const vpyContent = taskConfig.vpyContent
  const ffmpegCMD = taskConfig.ffmpegCMD

  const vspipePath = getExecPath().vspipe
  const ffmpegPath = getExecPath().ffmpeg

  const videos = Array.isArray(taskConfig.fileList) ? taskConfig.fileList : []

  shouldStop = false

  for (const video of videos) {
    if (shouldStop) {
      event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `已终止循环:\n`)
      shouldStop = false
      break
    }
    try {
      // ========== 1. 获取输入视频信息 ==========
      const { hasAudio, hasSubtitle } = await getInputVideoInfo(event, video)

      // ========== 2. 生成 vpy 文件 ==========
      const baseName = path.basename(video, path.extname(video))
      const vpyPath = getGenVpyPath(taskConfig, baseName)
      await writeVpyFile(null, vpyPath, vpyContent, video)

      // ========== 3. 获取输出视频信息 ==========
      const info = await getOutputVideoInfo(event, vpyPath)

      // ========== 4. 构建渲染命令 ==========
      const vspipeArgs = ffmpegCMD[0].replace(MagicStr.VPY_PATH, vpyPath)
      const ffmpegMajorArgs = ffmpegCMD[1]
      const ffmpegMinorArgs = ffmpegCMD[2]
      const ffmpeg_audio_sub_Args = generate_cmd(taskConfig, hasAudio, hasSubtitle)
      const ffmpegArgs = ffmpegMajorArgs.replace(MagicStr.VIDEO_PATH, video) + ffmpeg_audio_sub_Args + ffmpegMinorArgs.replace(MagicStr.VIDEO_NAME, path.join(taskConfig.outputFolder, `${baseName}_enhance`) + taskConfig.videoContainer)

      const full_cmd = `${`"${vspipePath}" ${vspipeArgs}`} | "${ffmpegPath}" ${ffmpegArgs}`
      event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `Executing command: ${full_cmd}\n`)

      // ========== 5. 渲染并监听输出 ==========
      await new Promise<void>((resolve, reject) => {
        const renderProcess = spawn(ffmpegPath, splitArgs(ffmpegArgs), { shell: false })
        const vspipeProc = spawn(vspipePath, splitArgs(vspipeArgs), { shell: false })

        event.sender.send(IpcChannelOn.VSPIPE_PID, vspipeProc.pid)
        event.sender.send(IpcChannelOn.FFMPEG_PID, renderProcess.pid)
        console.log(`ffmpegPID:${renderProcess.pid}`)
        console.log(`vspipePID:${vspipeProc.pid}`)
        event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `vspipePID:${vspipeProc.pid}  ||  ffmpegPID:${renderProcess.pid} \n`)

        vspipeProc.stdout.pipe(renderProcess.stdin)
        addProcess('ffmpeg', renderProcess)
        addProcess('vspipe', vspipeProc)

        renderProcess.stdout.on('data', (data) => {
          event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, data.toString())
        })

        renderProcess.stderr.on('data', (data) => {
          const str = data.toString()
          // eslint-disable-next-line regexp/no-misleading-capturing-group,regexp/no-super-linear-backtracking,regexp/optimal-quantifier-concatenation
          const regex = /frame=\s*(-?\d+)\s+fps=\s*([\d.]+).+time=\s*(-?[\d:.]+)\s+bitrate=\s*([\w/.-]+)/
          const match = str.match(regex)

          if (match) {
            const [_, frame, fps, time, bitrate] = match
            const totalFrames = Number.parseInt(info.frames || '0', 10)
            const renderedFrames = Number.parseInt(frame, 10)
            const currentFps = Number.parseFloat(fps)
            const remainingFrames = totalFrames - renderedFrames

            const estSeconds = remainingFrames / (currentFps || 1)
            const hours = Math.floor(estSeconds / 3600)
            const minutes = Math.floor((estSeconds % 3600) / 60)
            const seconds = Math.floor(estSeconds % 60)

            event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `[Progress_vspipe_ffmpeg]已渲染/总帧数: ${frame} / ${totalFrames} `
            + `速度(FPS): ${fps} `
            + `预计剩余时间：${hours}h ${minutes}min ${seconds}s `
            + `已渲染的时间长度: ${time} `
            + `比特率: ${bitrate}\n`)
          }
          else {
            event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, str)
          }
        })

        renderProcess.on('close', () => {
          removeProcess(renderProcess)
          event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, 'finish\n')
          resolve()
        })

        renderProcess.on('error', (err) => {
          reject(err)
        })
      })
    }
    catch (error) {
      const errMsg = error instanceof Error ? error.message : String(error)
      event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `处理视频 ${video} 时出错: ${errMsg}\n`)
    }
  }
  event.sender.send(IpcChannelOn.FFMPEG_FINISHED)
}

export async function PauseCommand(event: IpcMainEvent, data: { isPause: boolean, vspipePID: number }): Promise<void> {
  const pssuspendPath = path.join(getCorePath(), 'pssuspend.exe')
  const { isPause, vspipePID } = data
  const action = isPause ? '' : '-r'

  const vspipeProc = spawn(pssuspendPath, ['-accepteula', action, vspipePID.toString()], { shell: true })
  vspipeProc.on('close', () => {
    event.sender.send(IpcChannelOn.FFMPEG_OUTPUT, `${isPause ? '暂停' : '恢复'}完成\n`)
  })
}
