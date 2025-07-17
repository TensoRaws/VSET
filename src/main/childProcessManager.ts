// childProcessManager.ts

import { ChildProcess } from 'child_process'
import kill from 'tree-kill'

const childProcesses: ChildProcess[] = []

/**
 * 添加子进程
 */
export function addProcess(proc: ChildProcess) {
  childProcesses.push(proc)
}

/**
 * 移除子进程
 */
export function removeProcess(proc: ChildProcess) {
  const index = childProcesses.indexOf(proc)
  if (index !== -1) {
    childProcesses.splice(index, 1)
  }
}

/**
 * 杀死所有子进程及其子进程树
 */
export function killAllProcesses() {
  console.log(`🧹 正在终止 ${childProcesses.length} 个子进程...`)

  for (const proc of childProcesses) {
    if (!proc.killed) {
      const pid = proc.pid
      if (typeof pid === 'number') {
        console.log(`🔪 尝试终止进程树 PID=${pid}`)
        kill(pid, 'SIGKILL', (err) => {
          if (err) {
            console.error(`❌ 无法终止 PID=${pid}:`, err)
          } else {
            console.log(`✅ 成功终止 PID=${pid}`)
          }
        })
      } else {
        console.warn(`⚠ 无法终止进程：找不到有效 PID`)
      }
    }
  }

  // 清空列表
  childProcesses.length = 0
}
