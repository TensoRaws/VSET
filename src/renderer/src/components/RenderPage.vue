<script setup lang="ts">
import { Delete, Lock, WarningFilled } from '@element-plus/icons-vue'
// ✅ 引入 App 状态 store（isRunning）
import { useAppStore } from '@renderer/store/AppStore'
// ✅ 引入日志 store
import { useLogStore } from '@renderer/store/LogStore'
// 引入其他 store 数据
import { CheckSetting } from '@renderer/utils/checkSetting'
import { buildTaskConfig } from '@renderer/utils/getTaskConfig'
import { IpcChannelName } from '@shared/constant/ipc'

import { useMessage } from 'naive-ui'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const message = useMessage()

// 绑定日志 store
const logStore = useLogStore()
const logs = computed(() => logStore.logs)
const logInstRef = ref<any>(null)
const clearLogs = () => logStore.clearLog()

// 绑定 app 状态 store
const appStore = useAppStore()
const isRunning = computed(() => appStore.isRunning)
const isPause = computed(() => appStore.isPause)

function stopProcesses() {
  window.electron.ipcRenderer.send('stop-all-processes')
  message.warning('已请求终止所有子进程')
  appStore.setRunning(false)
  appStore.setPause(true)
}

// ✅ IPC 输出回调
function handleOutput(_, msg: string) {
  logStore.appendLog(msg)
}

// ✅ 挂载监听器
onMounted(() => {
  window.electron.ipcRenderer.removeAllListeners(IpcChannelName.FFMPEG_OUTPUT)
  window.electron.ipcRenderer.on(IpcChannelName.FFMPEG_OUTPUT, handleOutput)

  window.electron.ipcRenderer.removeAllListeners(IpcChannelName.VSPIPE_PID)
  window.electron.ipcRenderer.removeAllListeners(IpcChannelName.FFMPEG_PID)

  window.electron.ipcRenderer.on(IpcChannelName.VSPIPE_PID, (_, pid: number) => {
    appStore.setVspipePID(pid)
  })
  window.electron.ipcRenderer.on(IpcChannelName.FFMPEG_PID, (_, pid: number) => {
    appStore.setFfmpegPID(pid)
  })

  window.electron.ipcRenderer.on(IpcChannelName.FFMPEG_FINISHED, () => {
    appStore.setRunning(false) // ✅ 渲染完成后恢复按钮
  })
})

function Pause() {
  const isPauseValue = isPause.value
  const vspipePID = appStore.vspipePID
  // const ffmpegPID = appStore.ffmpegPID

  if (vspipePID === 0 || isRunning.value === false) {
    message.info('进程还没启动，暂停无效', { duration: 5000 })
    return
  }

  window.electron.ipcRenderer.send('pause', {
    isPause: isPauseValue,
    vspipePID,
  })

  if (isPause.value) {
    appStore.setPause(false)
  }
  else {
    appStore.setPause(true)
  }
}

onBeforeUnmount(() => {
  window.electron.ipcRenderer.removeListener(IpcChannelName.FFMPEG_OUTPUT, handleOutput)
  window.electron.ipcRenderer.removeAllListeners(IpcChannelName.FFMPEG_FINISHED)
})

// ✅ 启动渲染流程
function StartSR() {
  // 调用参数错误查询函数
  if (!CheckSetting()) {
    console.log('参数错误，无法启动渲染流程')
    message.error('参数错误，无法启动渲染流程', { duration: 5000 })
    return
  }

  appStore.setRunning(true) // ✅ 设置为运行中，禁用按钮

  const taskConfig = buildTaskConfig()
  window.electron.ipcRenderer.send(IpcChannelName.GENERATE_JSON, taskConfig)
  window.electron.ipcRenderer.send(IpcChannelName.EXECUTE_COMMAND, taskConfig)
}

// ✅ 日志自动滚动到底部
watch(() => logs.value, () => {
  nextTick(() => {
    logInstRef.value?.scrollTo({ position: 'bottom', silent: true })
  })
})
</script>

<template>
  <div class="flex-container">
    <div class="header">
      <el-button type="primary" :loading="isRunning" :disabled="isRunning" @click="StartSR">
        {{ isRunning ? '处理中...' : '启动' }}
      </el-button>
      <el-button type="primary" :icon="Delete" @click="clearLogs">
        清空日志
      </el-button>
      <el-button type="success" :icon="Lock" @click="Pause">
        {{ isPause ? '暂停' : '恢复' }}
      </el-button>
      <el-button type="danger" :icon="WarningFilled" @click="stopProcesses">
        结束进程
      </el-button>
    </div>

    <div class="log-container">
      <n-log
        ref="logInstRef"
        :log="logs"
        language="naive-log"
        trim
        class="log-content"
      />
    </div>
  </div>
</template>

<style scoped>
.flex-container {
  display: flex;
  flex-direction: column;
  height: 92vh;
  padding: 10px;
  box-sizing: border-box;
}

.header {
  margin-bottom: 10px;
}

.log-container {
  flex: 1;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.log-content {
  flex: 1;
  width: 100%;
  height: 100%;
  overflow: auto;
  padding: 10px;
  box-sizing: border-box;
  font-family: monospace;
  background-color: #fff;
}
</style>
