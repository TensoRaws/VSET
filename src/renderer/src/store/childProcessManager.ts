// childProcessManager.ts
import { ChildProcess } from 'child_process';

import treeKill from 'tree-kill';

export const childProcesses: ChildProcess[] = [];

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
  console.log(`准备终止 ${childProcesses.length} 个子进程...`);
  childProcesses.forEach((proc) => {
    if (proc && proc.pid) {
      try {
        treeKill(proc.pid, 'SIGTERM', (err) => {
          if (err) {
            console.error(`终止进程 ${proc.pid} 失败:`, err);
          } else {
            console.log(`已终止进程 ${proc.pid}`);
          }
        });
      } catch (err) {
        console.error(`终止进程 ${proc.pid} 异常:`, err);
      }
    }
  });

  // 清空
  childProcesses.length = 0;
}



