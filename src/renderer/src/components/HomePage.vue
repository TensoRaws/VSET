<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import img1 from '../assets/fufu1.avif'
import img2 from '../assets/fufu2.avif'
import img3 from '../assets/fufu3.avif'
import img4 from '../assets/fufu4.avif'
import { useSystemInfoStore } from '../store/SystemInfoStore'

const systemInfoStore = useSystemInfoStore()

// 使用 Store 中的信息（computed 确保响应式）
const CPUInfo = computed(() => systemInfoStore.cpuInfo)
const GPUInfo = computed(() => systemInfoStore.gpuInfo)
const GPUMainInfo = computed({
  get: () => systemInfoStore.gpuMainInfo,
  set: (val: string) => systemInfoStore.setGPUMainInfo(val),
})
const MemoryInfo = computed(() => systemInfoStore.memoryInfo)

const currentTime = ref('')

function updateTime(): void {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')

  currentTime.value = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

let timer: number | undefined

onMounted(() => {
  updateTime()
  timer = window.setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer)
    clearInterval(timer)
})
</script>

<template>
  <div class="flex-container">
    <n-carousel show-arrow>
      <img class="carousel-img" :src="img1">
      <img
        class="carousel-img"
        :src="img2"
      >
      <img
        class="carousel-img"
        :src="img3"
      >
      <img
        class="carousel-img"
        :src="img4"
      >
    </n-carousel>

    <n-card title="系统信息" :bordered="false" class="system-info-card">
      <div class="slider-demo-block">
        <span class="demonstration">CPU</span>
        <el-tag type="primary" size="large">
          {{ CPUInfo }}
        </el-tag>
      </div>

      <div class="slider-demo-block">
        <span class="demonstration">内存</span>
        <el-tag type="primary" size="large">
          {{ MemoryInfo }}
        </el-tag>
      </div>

      <div class="slider-demo-block">
        <span class="demonstration">GPU</span>
        <el-select v-model="GPUMainInfo" placeholder="GPU列表" style="max-width: 300px">
          <el-option
            v-for="(item, index) in GPUInfo"
            :key="index"
            :label="`${index}: ${item}`"
            :value="item"
          />
        </el-select>
      </div>

      <div class="slider-demo-block">
        <span class="demonstration">当前时间</span>
        <el-tag type="success" size="large">
          {{ currentTime }}
        </el-tag>
      </div>

      <div class="slider-demo-block">
        <span class="demonstration">项目地址</span>
        <el-tag type="info" size="large" class="project-link-tag">
          <a href="https://github.com/EutropicAI/VSET" target="_blank" rel="noopener noreferrer" class="project-link">
            https://github.com/EutropicAI/VSET
          </a>
        </el-tag>
      </div>
    </n-card>
  </div>
</template>

<style scoped>
.carousel-img {
  width: 100%;
  height: 350px;
  object-fit: cover;
}
.slider-demo-block {
  width: 100%;
  display: flex;
  align-items: center;
  flex-basis: calc(100% - 20px);
  margin-bottom: 16px;
}

.slider-demo-block .demonstration {
  font-size: 18px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}

.flex-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.system-info-card {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}

.project-link {
  color: #4a148c;
  text-decoration: none;
  cursor: pointer;
}

.project-link:hover {
  text-decoration: underline;
  color: #6a1b9a;
}

.project-link-tag {
  cursor: pointer;
  background-color: #e1bee7;
  border-color: #ba68c8;
}
</style>
