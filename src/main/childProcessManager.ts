import type { ChildProcess } from 'node:child_process'
import kill from 'tree-kill'
import { requestStop } from './runCommand'

interface ManagedProc {
  name: string
  proc: ChildProcess
}

const childProcesses: ManagedProc[] = []

export function addProcess(name: string, proc: ChildProcess): void {
  childProcesses.push({ name, proc })
}

export function removeProcess(proc: ChildProcess): void {
  const index = childProcesses.findIndex(p => p.proc === proc)
  if (index !== -1) {
    childProcesses.splice(index, 1)
  }
}

function safeUnpipe(): void {
  const vspipe = childProcesses.find(p => p.name === 'vspipe')
  const ffmpeg = childProcesses.find(p => p.name === 'ffmpeg')

  if (vspipe?.proc?.stdout && ffmpeg?.proc?.stdin) {
    try {
      vspipe.proc.stdout.unpipe(ffmpeg.proc.stdin)
    }
    catch {}
    try {
      ffmpeg.proc.stdin.end()
    }
    catch {}
  }
}

// ✅ 使用 Promise 确保等待 kill 完成
export async function killAllProcesses(): Promise<void> {
  requestStop()

  // 先安全断开管道
  safeUnpipe()
  const promises = childProcesses.map(({ name, proc }) => {
    return new Promise<void>((resolve) => {
      if (!proc.killed && typeof proc.pid === 'number') {
        console.log(`stop [${name}] PID=${proc.pid}`)
        kill(proc.pid, 'SIGKILL', (err) => {
          if (err) {
            console.error(`can not stop [${name}] PID=${proc.pid}:`, err)
          }
          else {
            console.log(`success stop [${name}] PID=${proc.pid}`)
          }
          resolve()
        })
      }
      else {
        resolve()
      }
    })
  })

  await Promise.all(promises)
  childProcesses.length = 0
}
