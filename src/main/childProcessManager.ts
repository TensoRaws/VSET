import { ChildProcess } from 'child_process';
import kill from 'tree-kill';
import psTree from 'ps-tree';

const childProcesses: ChildProcess[] = [];

export function addProcess(proc: ChildProcess) {
  if (proc && proc.pid) {
    childProcesses.push(proc);
    console.log(`✅ 添加子进程 PID: ${proc.pid}`);
  }
}

export function removeProcess(proc: ChildProcess) {
  const index = childProcesses.indexOf(proc);
  if (index !== -1) {
    console.log(`🧹 移除子进程 PID: ${proc.pid}`);
    childProcesses.splice(index, 1);
  }
}

export function killAllProcesses() {
  console.log('🛑 正在终止所有子进程...');
  for (const proc of childProcesses) {
    if (proc.pid) {
      psTree(proc.pid, (err, children) => {
        if (err) {
          console.error(`❌ 获取进程树失败 PID ${proc.pid}:`, err);
          return;
        }

        const pids = [proc.pid, ...children.map(p => parseInt(p.PID))];
        console.log(`🔪 即将终止进程树: ${pids.join(', ')}`);

        pids.forEach(pid => {
          kill(pid, 'SIGKILL', (err) => {
            if (err) {
              console.error(`❌ 终止失败 PID ${pid}:`, err);
            } else {
              console.log(`✅ 已终止 PID ${pid}`);
            }
          });
        });
      });
    }
  }

  // 清空列表
  childProcesses.length = 0;
}
