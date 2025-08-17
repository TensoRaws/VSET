import type { ChildProcess } from 'node:child_process'
import kill from 'tree-kill'
import { requestStop } from './runCommand'

const childProcesses: ChildProcess[] = []

export function addProcess(proc: ChildProcess): void {
  childProcesses.push(proc)
}

export function removeProcess(proc: ChildProcess): void {
  const index = childProcesses.indexOf(proc)
  if (index !== -1) {
    childProcesses.splice(index, 1)
  }
}

// ✅ 使用 Promise 确保等待 kill 完成
export async function killAllProcesses(): Promise<void> {
  requestStop()
  const promises = childProcesses.map((proc) => {
    return new Promise<void>((resolve) => {
      if (!proc.killed && typeof proc.pid === 'number') {
        console.log(`🔪 正在终止子进程 PID=${proc.pid}`)
        kill(proc.pid, 'SIGKILL', (err) => {
          if (err) {
            console.error(`❌ 无法终止 PID=${proc.pid}:`, err)
          }
          else {
            console.log(`✅ 成功终止 PID=${proc.pid}`)
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
