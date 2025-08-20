<script setup lang="ts">
import useOutputconfigStore from '@renderer/store/OutputStore'
import { storeToRefs } from 'pinia'

import {
  AmfH264_options,
  AmfH265_options,
  AudioContainer_options,
  CpuAv1_options,
  CpuH264_options,
  CpuH265_options,
  CpusvtAv1_options,
  Encoder_options,
  NvencAv1_options,
  NvencH264_options,
  NvencH265_options,
  QSVH264_options,
  QSVH265_options,
  VideoContainer_options,
} from '../store/OutputMethod'

const OutputConfigStore = useOutputconfigStore()
const {
  bitValue,
  crfValue,
  cqValue,
  qbValue,
  encoderValue,

  Libx265QualityValue,
  Libx264QualityValue,
  Libaomav1QualityValue,
  Libsvtav1QualityValue,
  HevcnvencQualityValue,
  H264nvencQualityValue,
  Av1nvencQualityValue,
  HevcamfQualityValue,
  H264amfQualityValue,
  HevcqsvQualityValue,
  H264qsvQualityValue,

  videoContainer,
  AudioContainer,
  isUseCrf,

  isSaveAudio,
  isSaveSubtitle,

  outputfolder,
  isUseCustomParams,
  CustomParams,
} = storeToRefs(OutputConfigStore)

async function selectDirectory() {
  const pathList = await window.electron.ipcRenderer.invoke('open-folder-dialog', ['openDirectory'])
  if (pathList && pathList.length > 0) {
    outputfolder.value = pathList[0]
  }
  else {
    console.log('No folder selected or selection was cancelled.')
  }
}
</script>

<template>
  <div class="flex-container">
    <div class="slider-demo-block">
      <span class="demonstration">编码器/格式</span>
      <el-select
        v-model="encoderValue"
        placeholder="Select"
        size="large"
        style="width: 240px"
      >
        <el-option
          v-for="item in Encoder_options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </div>

    <div v-if="encoderValue === 'libx265'" class="slider-demo-block">
      <span class="demonstration">质量预设(libx265)</span>
      <el-select
        v-model="Libx265QualityValue"
        placeholder="Select Quality Preset"
        size="large"
        style="width: 240px;"
      >
        <el-option v-for="item in CpuH265_options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </div>

    <div v-if="encoderValue === 'libx264'" class="slider-demo-block">
      <span class="demonstration">质量预设(libx264)</span>
      <el-select
        v-model="Libx264QualityValue"
        placeholder="Select Quality Preset"
        size="large"
        style="width: 240px;"
      >
        <el-option v-for="item in CpuH264_options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </div>

    <div v-if="encoderValue === 'libaom-av1'" class="slider-demo-block">
      <span class="demonstration">质量预设(libaom-av1)</span>
      <el-select
        v-model="Libaomav1QualityValue"
        placeholder="Select Quality Preset"
        size="large"
        style="width: 240px;"
      >
        <el-option v-for="item in CpuAv1_options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </div>

    <div v-if="encoderValue === 'libsvtav1'" class="slider-demo-block">
      <span class="demonstration">质量预设(libsvtav1)</span>
      <el-select
        v-model="Libsvtav1QualityValue"
        placeholder="Select Quality Preset"
        size="large"
        style="width: 240px;"
      >
        <el-option v-for="item in CpusvtAv1_options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </div>

    <div v-if="encoderValue === 'hevc_nvenc'" class="slider-demo-block">
      <span class="demonstration">质量预设(hevc_nvenc)</span>
      <el-select
        v-model="HevcnvencQualityValue"
        placeholder="Select Quality Preset"
        size="large"
        style="width: 240px;"
      >
        <el-option v-for="item in NvencH265_options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </div>

    <div v-if="encoderValue === 'h264_nvenc'" class="slider-demo-block">
      <span class="demonstration">质量预设(h264_nvenc)</span>
      <el-select
        v-model="H264nvencQualityValue"
        placeholder="Select Quality Preset"
        size="large"
        style="width: 240px;"
      >
        <el-option v-for="item in NvencH264_options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </div>

    <div v-if="encoderValue === 'av1_nvenc'" class="slider-demo-block">
      <span class="demonstration">质量预设(av1_nvenc)</span>
      <el-select
        v-model="Av1nvencQualityValue"
        placeholder="Select Quality Preset"
        size="large"
        style="width: 240px;"
      >
        <el-option v-for="item in NvencAv1_options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </div>

    <div v-if="encoderValue === 'hevc_amf'" class="slider-demo-block">
      <span class="demonstration">质量预设(hevc_amf)</span>
      <el-select
        v-model="HevcamfQualityValue"
        placeholder="Select Quality Preset"
        size="large"
        style="width: 240px;"
      >
        <el-option v-for="item in AmfH265_options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </div>

    <div v-if="encoderValue === 'h264_amf'" class="slider-demo-block">
      <span class="demonstration">质量预设(h264_amf)</span>
      <el-select
        v-model="H264amfQualityValue"
        placeholder="Select Quality Preset"
        size="large"
        style="width: 240px;"
      >
        <el-option v-for="item in AmfH264_options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </div>

    <div v-if="encoderValue === 'h265_qsv'" class="slider-demo-block">
      <span class="demonstration">质量预设(h265_qsv)</span>
      <el-select
        v-model="HevcqsvQualityValue"
        placeholder="Select Quality Preset"
        size="large"
        style="width: 240px;"
      >
        <el-option v-for="item in QSVH265_options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </div>

    <div v-if="encoderValue === 'h264_qsv'" class="slider-demo-block">
      <span class="demonstration">质量预设(h264_qsv)</span>
      <el-select
        v-model="H264qsvQualityValue"
        placeholder="Select Quality Preset"
        size="large"
        style="width: 240px;"
      >
        <el-option v-for="item in QSVH264_options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </div>

    <!-- <div class="slider-demo-block" v-if="encoderValue.includes('lib')">
      <span class="demonstration">质量控制参数</span>
      <el-radio-group v-model="isUseCrf" >
      <el-radio-button :value="false">码率</el-radio-button>
      <el-radio-button :value="true">CRF</el-radio-button>
    </el-radio-group>
    </div> -->

    <div v-if="isUseCrf && encoderValue.includes('lib')" class="slider-demo-block">
      <span class="demonstration">CRF</span>
      <el-slider v-model="crfValue" :min="1" :max="50" show-input style="max-width: 500px;" />
    </div>

    <div v-if="encoderValue.includes('nvenc')" class="slider-demo-block">
      <span class="demonstration">CQ</span>
      <el-slider v-model="cqValue" :min="0" :max="51" show-input style="max-width: 500px;" />
    </div>

    <div v-if="encoderValue.includes('amf') || encoderValue.includes('qsv')" class="slider-demo-block">
      <span class="demonstration">QP</span>
      <el-slider v-model="qbValue" :min="0" :max="51" show-input style="max-width: 500px;" />
    </div>

    <div class="slider-demo-block">
      <span class="demonstration">码率(M)</span>
      <el-slider v-model="bitValue" :min="1" :max="100" show-input style="max-width: 500px;" />
    </div>

    <div class="slider-demo-block">
      <span class="demonstration">视频容器</span>
      <el-select
        v-model="videoContainer"
        placeholder="Select"
        size="large"
        style="width: 240px"
      >
        <el-option
          v-for="item in VideoContainer_options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </div>

    <div class="slider-demo-block">
      <span class="demonstration">音频处理</span>
      <el-radio-group v-model="isSaveAudio">
        <el-radio-button :value="true">
          保留
        </el-radio-button>
        <el-radio-button :value="false">
          二压
        </el-radio-button>
      </el-radio-group>
    </div>

    <div v-if="!isSaveAudio" class="slider-demo-block">
      <span class="demonstration">音频格式</span>

      <el-select
        v-model="AudioContainer"
        placeholder="Select"
        size="large"
        style="width: 240px"
      >
        <el-option
          v-for="item in AudioContainer_options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </div>

    <div class="slider-demo-block">
      <span class="demonstration">字幕处理</span>
      <el-radio-group v-model="isSaveSubtitle">
        <el-radio-button :value="true">
          保留
        </el-radio-button>
        <el-radio-button :value="false">
          舍去
        </el-radio-button>
      </el-radio-group>
    </div>

    <div class="slider-demo-block">
      <span class="demonstration">输出文件夹</span>
      <el-input
        v-model="outputfolder"
        style="max-width: 600px"
        placeholder="请设置输出文件夹"
      >
        <template #append>
          <el-button size="large" type="primary" @click="selectDirectory">
            点击选择
          </el-button>
        </template>
      </el-input>
    </div>

    <div class="flex-container-extra">
      <n-button
        type="primary" size="small" style="height: 30px; width: 130px; background-color: #409eff; border-color: #ff6600; font-size: 18px; padding: 10px 24px; border-radius: 9px;"
        @click="ShowCustomExtra"
      >
        自定义
      </n-button>
      <n-drawer v-model:show="CustomExtra" :width="400">
        <n-drawer-content title="在使用之前，请确保自身具备一定的压制知识。">
          <span class="demonstration" style="font-size: 20px;color: black;">自定义视频压制参数</span>
          <div class="slider-demo-block">
            <el-switch
              v-model="isUseCustomParams"
              size="large"
              active-text="启用"
              inactive-text="关闭"
            />
          </div>
          <div class="slider-demo-block">
            <el-input
              v-model="CustomParams"
              style="width: 100%; font-size: 18px;"
              :rows="4"
              type="textarea"
              spellcheck="false"
              placeholder="Please input"
            />
          </div>
          <div
            style="margin-top: 10px; font-size: 14px; color: #333; word-break: break-all;"
            v-html="highlightedCommand"
          />
          <n-divider />
        </n-drawer-content>
      </n-drawer>
    </div>
  </div>
</template>

<style scoped>
.slider-demo-block {
  width: 100%;
  display: flex;
  align-items: center;
  flex-basis: calc(100% - 20px);
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
.slider-demo-block .demonstration + .el-slider {
  flex: 0 0 70%;
}

.flex-container {
  display: flex;
  flex-direction: column; /* 设置为垂直排列 */
  gap: 15px; /* 可选项，用于设置组件之间的间隔 */
}

.flex-container-extra {
  display: flex;
  justify-content: flex-end; /* 水平方向靠右 */
}
</style>
