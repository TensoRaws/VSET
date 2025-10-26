<script setup lang="ts">
import useFilterconfigStore from '@renderer/store/FilterStore'
import { QTGMC_Preset_options } from '@renderer/store/FilterSetting'
import { storeToRefs } from 'pinia'

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
  UseQTGMC_BeforeEnhance,
  QTGMC_Preset_BeforeEnhance,
} = storeToRefs(FilterConfigStore)
</script>

<template>
  <n-tabs type="segment" animated>
    <!-- 分页 1：预处理 -->
    <n-tab-pane name="before" tab="1：预处理">
      <div class="flex-container">
        <n-card :bordered="false" class="system-info-card">
          <div class="slider-demo-block">
            <span class="demonstration">视频长宽缩放(前)</span>

            <div class="switch-container">
              <el-switch
                v-model="UseResize_BeforeEnhance"
                inline-prompt
                size="large"
                style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                active-text="启用缩放"
                inactive-text="关闭缩放"
              />
            </div>

            <div>
              长度：
              <el-input-number v-model="ResizeWidth_BeforeEnhance" :min="1" :max="7680" />
              宽度：
              <el-input-number v-model="ResizeHeight_BeforeEnhance" :min="1" :max="4320" />
            </div>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">视频黑边(左右)</span>
            <div>
              左侧：
              <el-input-number v-model="ReduceLeft_BeforeEnhance" :min="0" :max="1000" />
              右侧：
              <el-input-number v-model="ReduceRight_BeforeEnhance" :min="0" :max="1000" />
            </div>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">视频黑边(上下)</span>
            <div>
              上边：
              <el-input-number v-model="ReduceOn_BeforeEnhance" :min="0" :max="1000" />
              下边：
              <el-input-number v-model="ReduceDown_BeforeEnhance" :min="0" :max="1000" />
            </div>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">QTGMC</span>

            <div class="switch-container">
              <el-switch
                v-model="UseQTGMC_BeforeEnhance"
                inline-prompt
                size="large"
                style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                active-text="启用QTGMC"
                inactive-text="关闭QTGMC"
              />
            </div>

            <div>
              预设：
              <el-select
                v-model="QTGMC_Preset_BeforeEnhance"
                style="width: 150px"
              >
                <el-option v-for="option in QTGMC_Preset_options" :key="option.value" :label="option.label" :value="option.value" />
              </el-select>
            </div>
          </div>
        </n-card>
      </div>
    </n-tab-pane>

    <!-- 分页 2：后处理 -->
    <n-tab-pane name="after" tab="后处理">
      <div class="flex-container">
        <n-card :bordered="false" class="system-info-card">
          <div class="slider-demo-block">
            <span class="demonstration">视频长宽缩放(末)</span>

            <div class="switch-container">
              <el-switch
                v-model="UseResize_AfterEnhance"
                inline-prompt
                size="large"
                style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                active-text="启用缩放"
                inactive-text="关闭缩放"
              />
            </div>

            <div>
              长度：
              <el-input-number v-model="ResizeWidth_AfterEnhance" :min="1" :max="7680" />
              宽度：
              <el-input-number v-model="ResizeHeight_AfterEnhance" :min="1" :max="4320" />
            </div>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">视频黑边(左右)</span>
            <div>
              左侧：
              <el-input-number v-model="ReduceLeft_AfterEnhance" :min="0" :max="1000" />
              右侧：
              <el-input-number v-model="ReduceRight_AfterEnhance" :min="0" :max="1000" />
            </div>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">视频黑边(上下)</span>
            <div>
              上边：
              <el-input-number v-model="ReduceOn_AfterEnhance" :min="0" :max="1000" />
              下边：
              <el-input-number v-model="ReduceDown_AfterEnhance" :min="0" :max="1000" />
            </div>
          </div>
        </n-card>
      </div>
    </n-tab-pane>
  </n-tabs>
</template>

<style scoped>
:deep(.n-tabs-tab--active) {
  color: #409eff !important;
  font-size: 18px !important;
  font-weight: 600;
}
:deep(.n-tabs-tab:hover) {
  background-color: #d9ebff;
  color: #1677ff;
}
:deep(.n-tabs-tab) {
  color: #606266;
}

.flex-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.slider-demo-block {
  width: 100%;
  display: flex;
  align-items: center;
  flex-basis: calc(100% - 20px);
  gap: 16px;
  margin-bottom: 16px;
  padding-bottom: 10px;
}

.slider-demo-block:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
}

.slider-demo-block .demonstration {
  font-size: 18px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  flex: 1;
  white-space: nowrap;
}

/* ✅ 控制开关靠近输入框位置 */
.switch-container {
  margin-left: 40px;
  margin-right: 10px;
}

.system-info-card {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}
</style>
