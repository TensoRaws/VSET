<template>
    <div class="flex-container">
      <div class="top-switch-bar" >
        <div style="border: 1px solid #dcdfe6; padding: 15px; border-radius: 6px;">
      <el-switch
        v-model="useSR"
        size="large"
        active-text="启用超分辨率"
        inactive-text="关闭超分辨率"
      />
      </div>
      <div style="border: 1px solid #dcdfe6; padding: 15px; border-radius: 6px;">
      <el-switch
        :model-value="true"
        size="large"
        active-text="启动半精度"
        inactive-text="关闭半精度"
        disabled
      />
      </div>
    </div>
     
      <div class="flex-container">
        <div class="slider-demo-block">
          <span class="demonstration">超分算法</span>
          <el-select
            v-model="SRMethodValue"
            placeholder="Select"
            @change="changeSelect"
            size="large"
            style="width: 240px"
          >
            <el-option
              v-for="item in SRMethod_options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>
  
 
        <div class="flex-container" v-if="SRMethodValue === 'Real_cugan'">
          <div class="slider-demo-block">
            <span class="demonstration">推理方式(Real_cugan)</span>
            <el-select
              v-model="RealcuganInferenceValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in Inference_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
  
          <div class="slider-demo-block">
            <span class="demonstration">超分模型(Real_cugan)</span>
            <el-select
              v-model="RealcuganModelValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in RealcuganModel_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
  
          <div class="slider-demo-block">
            <span class="demonstration">切割块数量(Real_cugan)</span>
            <el-select
              v-model="RealcuganTileValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in VsmlrtTile_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

  
          <div class="slider-demo-block">
            <span class="demonstration">强度参数(Real_cugan)</span>
            <el-slider v-model="RealcuganAlphaValue" :min="0" :max="2" :step="0.1" show-input style="max-width: 450px;"/>
          </div>
        </div>

        <div class="flex-container" v-if="SRMethodValue === 'Real_esrgan'">
            <div class="slider-demo-block">
            <span class="demonstration">推理方式(Real_esrgan)</span>
            <el-select
              v-model="RealesrganInferenceValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in Inference_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">超分模型(Real_esrgan)</span>
            <el-select
              v-model="RealesrganModelValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in RealesrganModel_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">放大倍数(Real_esrgan)</span>
            <el-select
              v-model="RealesrganScaleValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in RealesrganScale_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">切割块数量(Real_esrgan)</span>
            <el-select
              v-model="RealesrganTileValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in VsmlrtTile_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

        </div>

        <!-- <div class="flex-container" v-if="SRMethodValue === 'ArtCNN'">
            <div class="slider-demo-block">
            <span class="demonstration">推理方式(ArtCNN)</span>
            <el-select
              v-model="ArtCNNInferenceValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in Inference_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">超分模型(ArtCNN)</span>
            <el-select
              v-model="ArtCNNModelValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in ArtCNNModel_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">切割块数量(ArtCNN)</span>
            <el-select
              v-model="ArtCNNTileValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in VsmlrtTile_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

        </div>
 -->

      <div class="flex-container" v-if="SRMethodValue === 'Waifu2x'">
            <div class="slider-demo-block">
            <span class="demonstration">推理方式(Waifu2x)</span>
            <el-select
              v-model="Waifu2xInferenceValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in Inference_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">超分模型(Waifu2x)</span>
            <el-select
              v-model="Waifu2xModelValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in Waifu2xModel_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">切割块数量(Waifu2x)</span>
            <el-select
              v-model="Waifu2xTileValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in VsmlrtTile_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

        </div>

      <div class="flex-container" v-if="SRMethodValue === 'SwinIR'">
            <div class="slider-demo-block">
            <span class="demonstration">推理方式(SwinIR)</span>
            <el-select
              v-model="SwinIRInferenceValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in Inference_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">超分模型(SwinIR)</span>
            <el-select
              v-model="SwinIRModelValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in SwinIRModel_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

          <div class="slider-demo-block">
            <span class="demonstration">切割块数量(SwinIR)</span>
            <el-select
              v-model="SwinIRTileValue"
              placeholder="Select"
              size="large"
              style="width: 240px"
            >
              <el-option
                v-for="item in VsmlrtTile_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

        </div>


      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import useSrsettingconfigStore from '@renderer/store/SrSettingsStore'
  import {storeToRefs} from 'pinia'
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
    // ArtCNNInferenceValue,
    // ArtCNNModelValue,
    // ArtCNNTileValue,

    Waifu2xInferenceValue,
    Waifu2xModelValue,
    Waifu2xTileValue,

    SwinIRInferenceValue,
    SwinIRModelValue,
    SwinIRTileValue,
  } = storeToRefs(SrSettingStore)

  const changeSelect=(value: string) =>{
    RealcuganInferenceValue.value = 'Cuda'; 
    RealesrganInferenceValue.value = 'Cuda'; 
    // ArtCNNInferenceValue.value = 'Cuda'; 
    SwinIRInferenceValue.value = 'Cuda'; 
    SRMethodValue.value = value; 
  };

 import {
  SRMethod_options,
  Inference_options,
  RealcuganModel_options,
  RealesrganModel_options,
  VsmlrtTile_options,
  RealesrganScale_options,
  Waifu2xModel_options,
  // ArtCNNModel_options,
  SwinIRModel_options,
} from '../store/SRMethod'
  

  </script>
  
  <style scoped>

  .top-switch-bar {
  display: flex;
  justify-content: space-between; /* 左右对齐 */
  align-items: center;
  padding: 10px 0;
}
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
  
  /* 修改这里 */
  .flex-container .flex-container {
    flex-wrap: wrap; /* 开启换行 */
  }
  </style>
  