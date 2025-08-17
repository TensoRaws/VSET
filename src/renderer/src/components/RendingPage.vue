<script setup lang="ts">
// ✅ 引入 App 状态 store（isRunning）
import { useAppStore } from '@renderer/store/AppStore'
import useFilterconfigStore from '@renderer/store/FilterStore'
// ✅ 引入状态管理（其他配置）
import useInputconfigStore from '@renderer/store/InputStore'
// ✅ 引入日志 store
import { useLogStore } from '@renderer/store/LogStore'

import useOutputconfigStore from '@renderer/store/OutputStote'
import useSrsettingconfigStore from '@renderer/store/SrSettingsStore'
import useVfisettingconfigStore from '@renderer/store/VfiSettingsStore'
import { useMessage } from 'naive-ui'
import { storeToRefs } from 'pinia'

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

function stopProcesses() {
  window.electron.ipcRenderer.send('stop-all-processes')
  message.warning('已请求终止所有子进程')
  appStore.setRunning(false)
}

// 引入其他 store 数据
const InputConfigStore = useInputconfigStore()
const { fileList } = storeToRefs(InputConfigStore)

const SrSettingStore = useSrsettingconfigStore()
const {
  useSR,
  SRMethodValue,
  RealcuganTileValue,
  RealcuganInferenceValue,
  RealcuganModelValue,
  RealcuganAlphaValue,
  RealesrganInferenceValue,
  RealesrganModelValue,
  RealesrganTileValue,
  RealesrganScaleValue,

  Waifu2xInferenceValue,
  Waifu2xModelValue,
  Waifu2xTileValue,

  SwinIRInferenceValue,
  SwinIRModelValue,
  SwinIRTileValue,

  SR_ExtraModelValue,
  SR_ExtraModelInferenceValue,

  Sr_numstreams,
  Sr_cudagraph,

} = storeToRefs(SrSettingStore)

const VfiSettingStore = useVfisettingconfigStore()
const {
  useVfi,
  VfiMethodValue,
  RifeInferenceValue,
  RifeModelValue,
  RifeScaleValue,
  RifeMultiValue,
  RifeEnsembleValue,
  RifeDetectionValue,
  Vfi_numstreams,
  Vfi_cudagraph,
} = storeToRefs(VfiSettingStore)

const FilterConfigStore = useFilterconfigStore()
const {
  UseResize_BeforeEnhance,
  UseResize_AfterEnhance,
  ResizeWidth_BeforeEnhance,
  ResizeHeight_BeforeEnhance,
  ResizeWidth_AfterEnhance,
  ResizeHeight_AfterEnhance,
  ReduceLeft_BeforeEnhance,
  ReduceRight_BeforeEnhance,
  ReduceOn_BeforeEnhance,
  ReduceDown_BeforeEnhance,
  ReduceLeft_AfterEnhance,
  ReduceRight_AfterEnhance,
  ReduceOn_AfterEnhance,
  ReduceDown_AfterEnhance,
} = storeToRefs(FilterConfigStore)

const OutputConfigStore = useOutputconfigStore()
const {
  bitValue,
  crfValue,
  encoderValue,
  qualityValue,
  videoContainer,
  AudioContainer,
  isUseCrf,
  isSaveAudio,
  isSavesubtitle,
  outputfolder,
} = storeToRefs(OutputConfigStore)

// ✅ IPC 输出回调
function handleOutput(_, msg: string) {
  logStore.appendLog(msg)
}

// ✅ 挂载监听器
onMounted(() => {
  window.electron.ipcRenderer.removeAllListeners('ffmpeg-output')
  window.electron.ipcRenderer.on('ffmpeg-output', handleOutput)

  window.electron.ipcRenderer.on('ffmpeg-finish', () => {
    appStore.setRunning(false) // ✅ 渲染完成后恢复按钮
  })
})

onBeforeUnmount(() => {
  window.electron.ipcRenderer.removeListener('ffmpeg-output', handleOutput)
  window.electron.ipcRenderer.removeAllListeners('ffmpeg-finish')
})

// ✅ 启动渲染流程
function StartSR() {
  if (!outputfolder.value) {
    message.info('缺少输出文件夹，请到输出界面选择视频文件输出后的保存位置。', { duration: 5000 })
    return // 终止后续执行
  }

  if (RifeEnsembleValue.value === true && useVfi.value === true) {
    if (RifeModelValue.value === 'v4_21' || RifeModelValue.value === 'v4_22' || RifeModelValue.value === 'v4_22_lite' || RifeModelValue.value === 'v4_23'
      || RifeModelValue.value === 'v4_25' || RifeModelValue.value === 'v4_25_lite' || RifeModelValue.value === 'v4_25_heavy' || RifeModelValue.value === 'v4_26'
      || RifeModelValue.value === 'v4_26_heavy') {
      message.info('该补帧模型不可使用ensemble参数', { duration: 5000 })
      return // 终止后续执行
    }
    if (RifeScaleValue.value !== 1.0) {
      message.info('ensemble设为true时，光流参数需要设置为1.0', { duration: 5000 })
      return // 终止后续执行
    }
  }

  appStore.setRunning(true) // ✅ 设置为运行中，禁用按钮

  const fileListNames = fileList.value.map(file => (file.path).replace(/\\/g, '/'))

  const jsonData = {
    fileList: fileListNames,
    useSR: useSR.value,
    SRMethodValue: SRMethodValue.value,
    RealcuganTileValue: RealcuganTileValue.value,
    RealcuganInferenceValue: RealcuganInferenceValue.value,
    RealcuganModelValue: RealcuganModelValue.value,
    RealcuganAlphaValue: RealcuganAlphaValue.value,
    RealesrganInferenceValue: RealesrganInferenceValue.value,
    RealesrganModelValue: RealesrganModelValue.value,
    RealesrganTileValue: RealesrganTileValue.value,
    RealesrganScaleValue: RealesrganScaleValue.value,
    // ArtCNNInferenceValue: ArtCNNInferenceValue.value,
    // ArtCNNModelValue: ArtCNNModelValue.value,
    // ArtCNNTileValue: ArtCNNTileValue.value,
    Waifu2xInferenceValue: Waifu2xInferenceValue.value,
    Waifu2xModelValue: Waifu2xModelValue.value,
    Waifu2xTileValue: Waifu2xTileValue.value,
    SwinIRInferenceValue: SwinIRInferenceValue.value,
    SwinIRModelValue: SwinIRModelValue.value,
    SwinIRTileValue: SwinIRTileValue.value,
    SR_ExtraModelValue: SR_ExtraModelValue.value,
    SR_ExtraModelInferenceValue: SR_ExtraModelInferenceValue.value,
    Sr_numstreams: Sr_numstreams.value,
    Sr_cudagraph: Sr_cudagraph.value,

    useVfi: useVfi.value,
    VfiMethodValue: VfiMethodValue.value,
    RifeInferenceValue: RifeInferenceValue.value,
    RifeModelValue: RifeModelValue.value,
    RifeScaleValue: RifeScaleValue.value,
    RifeMultiValue: RifeMultiValue.value,
    RifeEnsembleValue: RifeEnsembleValue.value,
    RifeDetectionValue: RifeDetectionValue.value,
    Vfi_numstreams: Vfi_numstreams.value,
    Vfi_cudagraph: Vfi_cudagraph.value,

    UseResize_BeforeEnhance: UseResize_BeforeEnhance.value,
    UseResize_AfterEnhance: UseResize_AfterEnhance.value,
    ResizeWidth_BeforeEnhance: ResizeWidth_BeforeEnhance.value,
    ResizeHeight_BeforeEnhance: ResizeHeight_BeforeEnhance.value,
    ResizeWidth_AfterEnhance: ResizeWidth_AfterEnhance.value,
    ResizeHeight_AfterEnhance: ResizeHeight_AfterEnhance.value,
    ReduceLeft_BeforeEnhance: ReduceLeft_BeforeEnhance.value,
    ReduceRight_BeforeEnhance: ReduceRight_BeforeEnhance.value,
    ReduceOn_BeforeEnhance: ReduceOn_BeforeEnhance.value,
    ReduceDown_BeforeEnhance: ReduceDown_BeforeEnhance.value,
    ReduceLeft_AfterEnhance: ReduceLeft_AfterEnhance.value,
    ReduceRight_AfterEnhance: ReduceRight_AfterEnhance.value,
    ReduceOn_AfterEnhance: ReduceOn_AfterEnhance.value,
    ReduceDown_AfterEnhance: ReduceDown_AfterEnhance.value,

    bitValue: bitValue.value,
    crfValue: crfValue.value,
    encoderValue: encoderValue.value,
    qualityValue: qualityValue.value,
    videoContainer: videoContainer.value,
    AudioContainer: AudioContainer.value,
    isUseCrf: isUseCrf.value,
    isSaveAudio: isSaveAudio.value,
    isSavesubtitle: isSavesubtitle.value,
    outputfolder: outputfolder.value,
  }

  window.electron.ipcRenderer.send('generate-json', jsonData)
  window.electron.ipcRenderer.send('execute-command', jsonData)
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
      <el-button type="success" :disabled="isRunning" @click="StartSR">
        {{ isRunning ? '处理中...' : '启动' }}
      </el-button>
      <el-button type="danger" @click="clearLogs">
        清空日志
      </el-button>
      <el-button type="danger" @click="stopProcesses">
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
