<script setup lang="ts">
import useSrsettingconfigStore from '@renderer/store/SrSettingsStore'
import useVfisettingconfigStore from '@renderer/store/VfiSettingsStore'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'
import {
  Inference_options,
  RealcuganModel_options,
  RealesrganModel_options,
  RealesrganScale_options,
  SR_ExtraModel_options,
  sr_numstreams_options,
  SRMethod_options,
  VsmlrtTile_options,
  Waifu2xModel_options,
} from '../store/SRMethod'
import {
  Inference_Vfi_options,
  RifeModel_options,
  Scale_Vfi_options,
  vfi_numstreams_options,
  VfiMethod_options,
} from '../store/VfiMethod'

const SrSettingStore = useSrsettingconfigStore()
const VfiSettingStore = useVfisettingconfigStore()
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

  SR_ExtraModelValue,
  SR_ExtraModelInferenceValue,

  Sr_numstreams,
  Sr_cudagraph,
} = storeToRefs(SrSettingStore)

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

const SrExtra = ref(false)
const VfiExtra = ref(false)

function ShowSrExtra(): void {
  SrExtra.value = true
}

function ShowVfiExtra(): void {
  VfiExtra.value = true
}
</script>

<template>
  <n-tabs type="segment" animated>
    <!-- 分页 1：超分配置 -->
    <n-tab-pane name="sr" tab="超分">
      <div class="flex-container">
        <n-card :bordered="false" class="system-info-card-Method">
          <div class="top-switch-bar">
            <div style="border: 1px solid #dcdfe6; padding: 15px; border-radius: 6px;">
              <el-switch
                v-model="useSR"
                size="large"
                active-text="启用超分"
                inactive-text="关闭超分"
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
        </n-card>

        <div class="flex-container">
          <n-card :bordered="false" class="system-info-card-Method">
            <div class="slider-demo-block">
              <span class="demonstration">超分算法</span>
              <el-select
                v-model="SRMethodValue"
                placeholder="Select"
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
          </n-card>

          <div v-if="SRMethodValue === 'Real_cugan'" class="flex-container">
            <n-card :bordered="false" class="system-info-card-Para">
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
                <el-slider v-model="RealcuganAlphaValue" :min="0" :max="2" :step="0.1" show-input style="max-width: 450px;" />
              </div>
            </n-card>
          </div>

          <div v-if="SRMethodValue === 'Real_esrgan'" class="flex-container">
            <n-card :bordered="false" class="system-info-card-Para">
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
            </n-card>
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

          <div v-if="SRMethodValue === 'Waifu2x'" class="flex-container">
            <n-card :bordered="false" class="system-info-card-Para">
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
            </n-card>
          </div>

          <div v-if="SRMethodValue === 'SR_ExtraModel'" class="flex-container">
            <n-card :bordered="false" class="system-info-card-Para">
              <div class="slider-demo-block">
                <span class="demonstration">超分模型(SR_ExtraModel)</span>
                <el-select
                  v-model="SR_ExtraModelValue"
                  placeholder="Select"
                  size="large"
                  style="width: 240px"
                >
                  <el-option
                    v-for="item in SR_ExtraModel_options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">推理方式(SR_ExtraModel)</span>
                <el-select
                  v-model="SR_ExtraModelInferenceValue"
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
            </n-card>
          </div>

          <div class="flex-container-extra">
            <n-card :bordered="false" class="system-info-card-Para">
              <n-button
                type="primary" size="small" style="height: 30px; width: 130px; background-color: #409eff; border-color: #ff6600; font-size: 18px; padding: 10px 24px; border-radius: 9px;"
                @click="ShowSrExtra"
              >
                Extra
              </n-button>
              <n-drawer v-model:show="SrExtra" :width="300">
                <n-drawer-content title="准备压榨显卡了么？(SR)">
                  <span class="demonstration" style="font-size: 20px;color: black;">通用</span>

                  <div class="slider-demo-block">
                    <span class="demonstration" style="font-size: 15px;color: black;">num_streams</span>
                    <el-select
                      v-model="Sr_numstreams"
                      placeholder="Select"
                      size="small"
                      style="width: 120px"
                    >
                      <el-option
                        v-for="item in sr_numstreams_options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                      />
                    </el-select>
                  </div>

                  <n-divider />

                  <span class="demonstration" style="font-size: 20px;color: black;">TensorRt</span>
                  <div class="slider-demo-block">
                    <span class="demonstration" style="font-size: 15px;color: black;">cuda_graph</span>
                    <el-switch
                      v-model="Sr_cudagraph"
                      size="middle"
                      active-text="启用"
                      inactive-text="关闭"
                    />
                  </div>

                  <n-divider />
                </n-drawer-content>
              </n-drawer>
            </n-card>
          </div>
        </div>
      </div>
    </n-tab-pane>
    <!-- 分页 2：补帧配置 -->
    <n-tab-pane name="fi" tab="补帧">
      <div class="flex-container">
        <n-card :bordered="false" class="system-info-card-Method">
          <div class="top-switch-bar">
            <div style="border: 1px solid #dcdfe6; padding: 15px; border-radius: 6px;">
              <el-switch
                v-model="useVfi"
                size="large"
                active-text="启用补帧"
                inactive-text="关闭补帧"
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
        </n-card>

        <div class="flex-container">
          <n-card :bordered="false" class="system-info-card-Method">
            <div class="slider-demo-block">
              <span class="demonstration">补帧算法</span>
              <el-select
                v-model="VfiMethodValue"
                placeholder="Select"
                size="large"
                style="width: 240px"
              >
                <el-option
                  v-for="item in VfiMethod_options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </div>
          </n-card>

          <div v-if="VfiMethodValue === 'Rife'" class="flex-container">
            <n-card :bordered="false" class="system-info-card-Para">
              <div class="slider-demo-block">
                <span class="demonstration">推理方式(rife)</span>
                <el-select
                  v-model="RifeInferenceValue"
                  placeholder="Select"
                  size="large"
                  style="width: 240px"
                >
                  <el-option
                    v-for="item in Inference_Vfi_options.filter(opt => opt.value !== 'NCNN')"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">补帧模型(rife)</span>
                <el-select
                  v-model="RifeModelValue"
                  placeholder="Select"
                  size="large"
                  style="width: 240px"
                >
                  <el-option
                    v-for="item in RifeModel_options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">光流尺度(rife)</span>
                <el-select
                  v-model="RifeScaleValue"
                  placeholder="Select"
                  size="large"
                  style="width: 240px"
                >
                  <el-option
                    v-for="item in Scale_Vfi_options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">目标帧率(rife)</span>
                <el-slider
                  v-model="RifeMultiValue" :min="60"
                  :max="480" show-input style="max-width: 500px;"
                />
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">转场阈值(rife)</span>
                <el-slider
                  v-model="RifeDetectionValue" :min="0"
                  :max="1" :step="0.1" show-input style="max-width: 500px;"
                />
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">Ensemble(rife)</span>
                <el-radio-group v-model="RifeEnsembleValue">
                  <el-radio-button :value="true">
                    使用
                  </el-radio-button>
                  <el-radio-button :value="false">
                    关闭
                  </el-radio-button>
                </el-radio-group>
              </div>
            </n-card>

            <div class="flex-container-extra">
              <n-card :bordered="false" class="system-info-card-Para">
                <n-button
                  type="primary" size="small" style="height: 30px; width: 130px; background-color: #409eff; border-color: #ff6600; font-size: 18px; padding: 10px 24px; border-radius: 9px;"
                  @click="ShowVfiExtra"
                >
                  Extra
                </n-button>
                <n-drawer v-model:show="VfiExtra" :width="300">
                  <n-drawer-content title="准备压榨显卡了么？(VFI)">
                    <span class="demonstration" style="font-size: 20px;color: black;">通用</span>

                    <div class="slider-demo-block">
                      <span class="demonstration" style="font-size: 15px;color: black;">num_streams</span>
                      <el-select
                        v-model="Vfi_numstreams"
                        placeholder="Select"
                        size="small"
                        style="width: 120px"
                      >
                        <el-option
                          v-for="item in vfi_numstreams_options"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value"
                        />
                      </el-select>
                    </div>

                    <n-divider />

                    <span class="demonstration" style="font-size: 20px;color: black;">TensorRt</span>
                    <div class="slider-demo-block">
                      <span class="demonstration" style="font-size: 15px;color: black;">cuda_graph</span>
                      <el-switch
                        v-model="Vfi_cudagraph"
                        size="middle"
                        active-text="启用"
                        inactive-text="关闭"
                      />
                    </div>

                    <n-divider />
                  </n-drawer-content>
                </n-drawer>
              </n-card>
            </div>
          </div>
        </div>
      </div>
    </n-tab-pane>
  </n-tabs>
</template>

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
.slider-demo-block:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
}
  .slider-demo-block .demonstration + .el-slider {
    flex: 0 0 70%;
  }

  .flex-container {
    display: flex;
    flex-direction: column; /* 设置为垂直排列 */
    gap: 10px; /* 可选项，用于设置组件之间的间隔 */
  }

  /* 修改这里 */
  .flex-container .flex-container {
    flex-wrap: wrap; /* 开启换行 */
  }

  .flex-container-extra {
    display: flex;
    justify-content: flex-end; /* 水平方向靠右 */
}

.system-info-card-Method {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}

.system-info-card-Para {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}
  </style>
