// childProcessManager.ts
import { ChildProcess } from 'child_process';

const childProcesses: ChildProcess[] = [];

export function addProcess(proc: ChildProcess) {
  childProcesses.push(proc);
}

export function removeProcess(proc: ChildProcess) {
  const index = childProcesses.indexOf(proc);
  if (index !== -1) {
    childProcesses.splice(index, 1);
  }
}

export function killAllProcesses() {
  console.log('🛑 正在终止所有子进程...');
  for (const proc of childProcesses) {
    try {
      proc.kill('SIGKILL');
      console.log(`已终止子进程 PID: ${proc.pid}`);
    } catch (e) {
      console.error('❌ 子进程终止失败:', e);
    }
  }
}
