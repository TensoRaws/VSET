import type { TaskConfig } from '@shared/type/taskConfig'
import type { IpcMainEvent } from 'electron'
import { Buffer } from 'node:buffer'
import { spawn } from 'node:child_process'
import path from 'node:path'
import iconv from 'iconv-lite'
import { addProcess, removeProcess } from './childProcessManager'
import { getExecPath, getGenVpyPath } from './getCorePath'
import { writeVpyFile } from './writeFile'

export async function preview(event: IpcMainEvent, task_config: TaskConfig): Promise<void> {
  const vspipePath = getExecPath().vspipe

  const video = task_config.fileList[0] // 只预览第一个视频

  // ========== 生成 vpy 文件 ==========
  // 生成唯一 vpy 路径
  const baseName = path.basename(video, path.extname(video))
  const vpyPath = getGenVpyPath(task_config, baseName)
  await writeVpyFile(null, vpyPath, task_config.vpyContent, video)

  let info: {
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
    addProcess(vspipeInfoProcess)

    let vspipeOut = '' // 用于保存 stdout 内容
    // eslint-disable-next-line unused-imports/no-unused-vars
    let stderrOut = '' // 用于保存 stderr 内容

    vspipeInfoProcess.stdout.on('data', (data: Buffer) => {
      const str = iconv.decode(data, 'gbk')
      vspipeOut += str
      event.sender.send('ffmpeg-output', `${str}`)
    })

    vspipeInfoProcess.stderr.on('data', (data: Buffer) => {
      const str = iconv.decode(data, 'gbk')
      stderrOut += str
      event.sender.send('ffmpeg-output', `${str}`)
    })

    vspipeInfoProcess.on('close', (code) => {
      removeProcess(vspipeInfoProcess)
      event.sender.send('ffmpeg-output', `vspipe info 执行完毕，退出码: ${code}\n`)///////
      info = {
        width: vspipeOut.match(/Width:\s*(\d+)/)?.[1] || '未知',
        height: vspipeOut.match(/Height:\s*(\d+)/)?.[1] || '未知',
        frames: vspipeOut.match(/Frames:\s*(\d+)/)?.[1] || '0',
        fps: vspipeOut.match(/FPS:\s*([\d/]+)\s*\(([\d.]+) fps\)/)?.[2] || '0',
      }

      event.sender.send('preview-info', info)
      resolve()
    })

    vspipeInfoProcess.on('error', (err) => {
      event.sender.send('ffmpeg-output', `vspipe 执行出错: ${err.message}\n`)
      reject(err)
    })
  })
  event.sender.send('preview-vpyPath', vpyPath)
  event.sender.send('ffmpeg-finish')
}

export async function previewFrame(event: IpcMainEvent, vpyfile: string, currentFrame: number): Promise<void> {
  const vspipePath = getExecPath().vspipe
  const ffmpegPath = getExecPath().ffmpeg

  // 构造一行命令
  const cmd = `"${vspipePath}" -c y4m --start ${currentFrame} --end ${currentFrame} "${vpyfile}" - | "${ffmpegPath}" -y -f yuv4mpegpipe -i - -frames:v 1 -vcodec png -f image2pipe -`

  const vspipePreviewProcess = spawn(cmd, { shell: true })
  addProcess(vspipePreviewProcess)

  const chunks: Buffer[] = []

  vspipePreviewProcess.stdout.on('data', (chunk) => {
    chunks.push(chunk)
  })

  vspipePreviewProcess.stderr.on('data', (data: Buffer) => {
    const str = iconv.decode(data, 'gbk')
    event.sender.send('ffmpeg-output', str)
  })

  vspipePreviewProcess.on('close', (code) => {
    removeProcess(vspipePreviewProcess)
    if (code === 0) {
      const buffer = Buffer.concat(chunks)
      const base64 = `data:image/png;base64,${buffer.toString('base64')}`
      event.sender.send('preview-image', base64)
    }
    else {
      event.sender.send('ffmpeg-output', `预览失败，退出码: ${code}`)
      event.sender.send('preview-image', null)
    }
    event.sender.send('ffmpeg-finish')
  })

  vspipePreviewProcess.on('error', (err) => {
    event.sender.send('ffmpeg-output', `命令执行出错: ${err.message}`)
  })
}
