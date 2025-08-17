<script setup lang="ts">
import {computed } from 'vue'
import useOutputconfigStore from '@renderer/store/OutputStote'
import {storeToRefs} from 'pinia'
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
    encoder_options,
    CpuH265_options,
    CpuH264_options,
    CpuAv1_options,

    cpusvtav1_qualityValue,
    CpusvtAv1_options,

    NvencH265_options,
    NvencH264_options,
    NvencAv1_options,

    VideoContainer_options,
    AudioContainer_options,
    outputfolder
  } = storeToRefs(OutputConfigStore)

const qualityPresets = computed(() => {
    switch (encoderValue.value) {
      case 'libx265':
        return CpuH265_options.value;
      case 'libx264':
        return CpuH264_options.value;
      case 'libaom-av1':
        return CpuAv1_options.value;
      case 'hevc_nvenc':
        return NvencH265_options.value;
      case 'h264_nvenc':
        return NvencH264_options.value;
      case 'av1_nvenc':
        return NvencAv1_options.value;
      default:
      return [];
    }
  });


const changeSelect = (value: string) => {
  qualityValue.value = 'slow'; 
  encoderValue.value = value; 
};

const selectDirectory = async () => {
  outputfolder.value = await window.api.selectDirectory()
    };

</script>

<template>
<div class="flex-container">
  <div class="slider-demo-block">
    <span class="demonstration">编码器/格式</span>
    <el-select
      v-model="encoderValue"
      placeholder="Select"
      @change="changeSelect"
      size="large"
      style="width: 240px"
    >
      <el-option
        v-for="item in encoder_options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
  </div>


  <div class="slider-demo-block" v-if="encoderValue!='libsvtav1'">
    <span class="demonstration">质量预设</span>
    <el-select 
     v-model="qualityValue"
     placeholder="Select Quality Preset"
     size="large"
     style="width: 240px;">
      <el-option v-for="item in qualityPresets" :key="item.value" :label="item.label" :value="item.value" />
    </el-select>
  </div>

  <div class="slider-demo-block" v-if="encoderValue=='libsvtav1'">
    <span class="demonstration">质量预设</span>
    <el-select 
     v-model="cpusvtav1_qualityValue"
     placeholder="Select Quality Preset"
     size="large"
     style="width: 240px;">
      <el-option v-for="item in CpusvtAv1_options" :key="item.value" :label="item.label" :value="item.value" />
    </el-select>
  </div>

  <div class="slider-demo-block">
    <span class="demonstration">质量控制参数</span>
    <el-radio-group v-model="isUseCrf" >
    <el-radio-button :value="false">码率</el-radio-button>
    <el-radio-button :value="true">CRF</el-radio-button>
  </el-radio-group>
  </div>

<div class="slider-demo-block" v-if="!isUseCrf">
    <span class="demonstration">码率(M)</span>
    <el-slider v-model="bitValue" :min="1" :max="100" show-input style="max-width: 500px;"/>
  </div>
  <div class="slider-demo-block" v-if="isUseCrf">
    <span class="demonstration">CRF</span>
    <el-slider v-model="crfValue" :min="1" :max="50" show-input style="max-width: 500px;"/>
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
    <el-radio-group v-model="isSaveAudio" >
    <el-radio-button :value="true">保留</el-radio-button>
    <el-radio-button :value="false">二压</el-radio-button>
  </el-radio-group>
  </div>

  <div class="slider-demo-block" v-if="!isSaveAudio">
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
    <el-radio-group v-model="isSavesubtitle" >
    <el-radio-button :value="true">保留</el-radio-button>
    <el-radio-button :value="false">舍去</el-radio-button>
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
      <el-button size="large" type="primary" @click="selectDirectory">点击选择</el-button>
      </template>
    </el-input>
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

</style>