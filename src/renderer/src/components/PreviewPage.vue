<script setup lang="ts">
import type { VNode } from 'vue'
import { useAppStore } from '@renderer/store/AppStore'
// ✅ 引入状态管理（其他配置）

import { buildTaskConfig } from '@renderer/utils/getTaskConfig'
import { DownloadOutline } from '@vicons/ionicons5'
import { NButton, NIcon, NImage, useMessage } from 'naive-ui'
import { computed, h, onMounted, ref } from 'vue'

const appStore = useAppStore()
const message = useMessage()

const vpyFilePath = ref('目标.vpy')

const frameCount = ref<number>(0)
const currentFrame = ref(0)
const previewImageSrc = ref('')
const loading = ref(false)
const isRunning = computed(() => appStore.isRunning)

// 保存图片真实宽高
const imageNaturalWidth = ref(0)
const imageNaturalHeight = ref(0)

function downloadImage() {
  const a = document.createElement('a')
  a.href = previewImageSrc.value
  a.download = 'preview.png'
  a.click()
}

function customRenderToolbar(props: {
  nodes: {
    rotateCounterclockwise: VNode
    rotateClockwise: VNode
    resizeToOriginalSize: VNode
    zoomOut: VNode
    zoomIn: VNode
    download: VNode
    close: VNode
  }
}) {
  return [
    props.nodes.rotateCounterclockwise,
    props.nodes.rotateClockwise,
    props.nodes.resizeToOriginalSize,
    props.nodes.zoomOut,
    props.nodes.zoomIn,
    // ✅ 自定义替换 download 节点
    h(
      NButton,
      {
        quaternary: true,
        circle: true,
        type: 'default',
        onClick: downloadImage,
        style: 'margin: 0 6px; color: white;',
      },
      {
        icon: () => h(NIcon, null, { default: () => h(DownloadOutline) }),
      },
    ),
    props.nodes.close,
  ]
}

function handlePreviewInfo(_event: any, data: any) {
  if (data && data.frames) {
    frameCount.value = Number.parseInt(data.frames)
    message.success(`检测到 ${data.frames} 帧，尺寸 ${data.width}×${data.height}`)
  }
}

function handlePreviewImage(_event: any, base64Img: string) {
  loading.value = false
  if (base64Img) {
    previewImageSrc.value = base64Img
    imageNaturalWidth.value = 0
    imageNaturalHeight.value = 0
  }
  else {
    message.error('帧图像加载失败')
  }
}

function startPreview() {
  if (appStore.isRunning)
    return
  appStore.setRunning(true)

  const taskConfig = buildTaskConfig()

  window.electron.ipcRenderer.once('preview-info', handlePreviewInfo)
  window.electron.ipcRenderer.once('preview-image', handlePreviewImage)
  window.electron.ipcRenderer.send('preview', taskConfig)
}

function previewFrame() {
  loading.value = true
  window.electron.ipcRenderer.once('preview-image', handlePreviewImage)
  window.electron.ipcRenderer.send('preview-frame', vpyFilePath.value, currentFrame.value)
}

function onFrameChange(val: number | null) {
  if (appStore.isRunning)
    return
  appStore.setRunning(true)
  if (val !== null) {
    currentFrame.value = val
    previewFrame()
  }
}

function onImageLoad(event: Event) {
  const img = event.target as HTMLImageElement
  imageNaturalWidth.value = img.naturalWidth
  imageNaturalHeight.value = img.naturalHeight
}

// ✅ 挂载监听器
onMounted(() => {
  window.electron.ipcRenderer.on('ffmpeg-finish', () => {
    appStore.setRunning(false) // ✅ 渲染完成后恢复按钮
  })

  window.electron.ipcRenderer.on('preview-vpyPath', (_event, vpyfile: string) => {
    vpyFilePath.value = vpyfile
  })
})
</script>

<template>
  <div class="preview-wrapper">
    <div class="control-group">
      <el-button type="success" :disabled="isRunning" @click="startPreview">
        {{ isRunning ? '运行中...' : '预览初始化' }}
      </el-button>
      <span style="margin-left: 10px;">文件路径：{{ vpyFilePath }}</span>
    </div>

    <div class="control-group">
      <span>总帧数: {{ frameCount }}</span>
      <el-slider
        v-model="currentFrame"
        :min="0"
        :max="frameCount"
        :step="1"
        :disabled="isRunning"
        style="margin-top: 10px; width: 100%;"
        show-input
        @change="onFrameChange"
      />
    </div>

    <div v-if="imageNaturalWidth && imageNaturalHeight" class="resolution-text" style="margin-bottom: 6px;">
      当前图片分辨率: {{ imageNaturalWidth }} × {{ imageNaturalHeight }}
    </div>

    <div class="preview-box">
      <div class="image-container">
        <n-spin :show="loading">
          <NImage
            v-if="previewImageSrc"
            :src="previewImageSrc"
            alt="帧预览图"
            object-fit="contain"
            :render-toolbar="customRenderToolbar"
            @load="onImageLoad"
          />
        </n-spin>
      </div>
    </div>
  </div>
</template>

<style scoped>
.image-container {
  max-width: 100%;
  max-height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-container :deep(img) {
  /* 深度选择器确保作用于内部 img 元素 */
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  display: block;
  user-select: none;
}

.preview-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.preview-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.control-group {
  margin-bottom: 10px;
  color: #888;
  font-size: 14px;
}

.resolution-text {
  font-size: 14px;
  color: #ddd;
  user-select: none;
}

.preview-box {
  flex: 1;
  background-color: #111;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  overflow: hidden;
  box-sizing: border-box;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  display: block;
  user-select: none;
  pointer-events: none;
}
</style>
