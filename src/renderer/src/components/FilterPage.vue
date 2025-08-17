<script setup lang="ts">
import useFilterconfigStore from '@renderer/store/FilterStore'
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
} = storeToRefs(FilterConfigStore)
</script>

<template>
  <div class="flex-container">
    <div style="border: 1px solid #dcdfe6; padding: 15px; border-radius: 6px; text-align: center;">
      <el-text class="mx-1" size="large">
        预处理（AI渲染前工作）
      </el-text>
    </div>
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
    <div style="border: 1px solid #dcdfe6; padding: 15px; border-radius: 6px; text-align: center;">
      <el-text class="mx-1" size="large">
        后处理（AI渲染后工作）
      </el-text>
    </div>
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
  </div>
</template>

<style scoped>
.flex-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.slider-demo-block {
  width: 100%;
  display: flex;
  align-items: center;
  flex-basis: calc(100% - 20px);
  gap: 10px;
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
</style>
