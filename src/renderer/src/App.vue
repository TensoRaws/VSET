<script lang="ts">
import type { MenuOption } from 'naive-ui'
import type { Component, VNode } from 'vue'
import {
  CloseOutline as Close,
  ConstructOutline as enhanceIcon,
  CameraOutline as filterIcon,
  BookOutline as homeIcon,
  AddCircleOutline as inputIcon,
  ColorFillOutline as outputIcon,
  GlassesOutline as PreviewIcon,
  RemoveOutline as Remove,
  SendOutline as renderingIcon,
  SquareOutline as Square,
} from '@vicons/ionicons5'
import { NIcon } from 'naive-ui'
import { defineComponent, h, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import appIcon from '../../../resources/icon.png'
import { useSystemInfoStore } from './store/SystemInfoStore'

function renderIcon(icon: Component): () => VNode {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions: MenuOption[] = [
  { whateverLabel: '主页', whateverKey: 'home', icon: renderIcon(homeIcon), path: '/' },
  { whateverLabel: '输入', whateverKey: 'input', icon: renderIcon(inputIcon), path: '/input' },
  { whateverLabel: '增强', whateverKey: 'enhance', icon: renderIcon(enhanceIcon), path: '/enhance' },
  { whateverLabel: '滤镜', whateverKey: 'filter', icon: renderIcon(filterIcon), path: '/filter' },
  { whateverLabel: '输出', whateverKey: 'output', icon: renderIcon(outputIcon), path: '/output' },
  { whateverLabel: '渲染', whateverKey: 'render', icon: renderIcon(renderingIcon), path: '/render' },
  { whateverLabel: '预览', whateverKey: 'preview', icon: renderIcon(PreviewIcon), path: '/preview' },
]

export default defineComponent({
  setup() {
    const router = useRouter()
    const collapsed = ref(true)
    const systemInfoStore = useSystemInfoStore()

    // 在应用启动时初始化系统信息
    onMounted(() => {
      systemInfoStore.initSystemInfo()
      // 清空并重新加载模型列表，确保每次启动都获取最新模型
      systemInfoStore.extraSrModelList = []
    })

    const onMenuChange = (value: string): void => {
      router.push(value)
    }

    // 添加折叠状态切换处理函数
    const handleCollapseChange = (isCollapsed: boolean) => {
      collapsed.value = isCollapsed
    }

    const handleMinimize = () => window.electronWindow?.minimize()
    const handleMaximize = () => window.electronWindow?.maximize()
    const handleClose = () => window.electronWindow?.close()

    router.push('/home')

    return {
      appIcon,
      collapsed,
      menuOptions,
      onMenuChange,
      handleCollapseChange, // 导出折叠处理函数
      handleMinimize,
      handleMaximize,
      handleClose,
      Remove,
      Square,
      Close,
    }
  },
})
</script>

<template>
  <n-message-provider>
    <div class="app-container">
      <!-- 上边框 -->
      <div class="top-bar">
        <div class="top-bar-content">
          <div class="left-section">
            <img class="app-icon" :src="appIcon" alt="app icon">
            <div class="title">
              VSET 4.4.1
            </div>
          </div>
          <div class="window-buttons">
            <button class="win-btn" @click="handleMinimize">
              <n-icon :component="Remove" size="14" />
            </button>
            <button class="win-btn" @click="handleMaximize">
              <n-icon :component="Square" size="14" />
            </button>
            <button class="win-btn close" @click="handleClose">
              <n-icon :component="Close" size="14" />
            </button>
          </div>
        </div>
      </div>

      <!-- 主体内容 -->
      <div class="body-wrapper">
        <!-- 左侧边栏 -->
        <n-layout-sider
          class="left-sider"
          collapse-mode="width"
          :collapsed-width="64"
          :width="120"
          :collapsed="collapsed"
          :show-trigger="true"
          @collapse="handleCollapseChange"
          @expand="handleCollapseChange"
        >
          <n-menu
            :collapsed="collapsed"
            :collapsed-width="64"
            :collapsed-icon-size="22"
            :options="menuOptions"
            key-field="whateverKey"
            label-field="whateverLabel"
            children-field="whateverChildren"
            @update:value="onMenuChange"
          />
        </n-layout-sider>

        <!-- 内容区域 -->
        <n-layout-content class="main-content">
          <router-view />
        </n-layout-content>
      </div>

      <!-- 下边框 -->
      <div class="bottom-bar" />
    </div>
  </n-message-provider>
</template>

<style scoped>
/* 容器 */
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

/* 上边框 */
.top-bar {
  height: 32px;
  background: linear-gradient(135deg, #8fa9f9 0%, #b794f8 50%, #d8b4fc 100%);
  -webkit-app-region: drag; /* 全部可拖动 */
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 8px;
  -webkit-app-region: drag;
}

.app-icon {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  user-select: none;
  pointer-events: none;
}

.top-bar-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-left: 12px;
  padding-right: 0;
}

.title {
  color: white;
  font-size: 14px;
  font-weight: 500;
  margin-left: 4px;
}

.window-buttons {
  display: flex;
  gap: 0;                 /* 不留间隙，按钮紧贴 */
  margin-right: 0;        /* 去掉内缩 */
  height: 100%;           /* 按钮撑满顶部栏 */
}

.win-btn {
  width: 46px;            /* 按钮宽度自定义 */
  height: 32px;           /* 顶栏高度 */
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  -webkit-app-region: no-drag;
  color: white;
  transition: background-color 0.2s;
  border-radius: 0;       /* 默认无圆角 */
}

.win-btn:hover {
  background-color: rgba(255,255,255,0.15);
}

.win-btn.close:hover {
  background-color: #e81123;
}

.win-btn.close {
  border-top-right-radius: 8px;   /* 和窗口圆角保持一致 */
}

/* 主体区域 */
.body-wrapper {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* 左侧边栏 */
.left-sider {
  ackground: #ffffff; /* 白色背景 */
  overflow: visible; /* 让 trigger 可点击 */
  position: relative;
}

/* 内容区域 */
.main-content {
  flex: 1;
  padding: 24px;
  background-color: #d0ebff !important;
  overflow: auto;
}

/* 下边框 */
.bottom-bar {
  height: 28px;
  background: linear-gradient(135deg, #8fa9f9 0%, #b794f8 50%, #d8b4fc 100%);
  border-top: 1px solid #e0e0e0;
}
</style>
