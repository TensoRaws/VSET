<script setup lang="ts">
import useSrsettingconfigStore from '@renderer/store/SrSettingsStore'
import { useSystemInfoStore } from '@renderer/store/SystemInfoStore'
import useVfisettingconfigStore from '@renderer/store/VfiSettingsStore'
import { storeToRefs } from 'pinia'
import { computed, onMounted, ref, watch } from 'vue'
import {
  Inference_options,
  RealcuganModel_options,
  RealesrganModel_options,
  RealesrganScale_options,
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

const SystemInfoStore = useSystemInfoStore()
const { extraSrModelList } = storeToRefs(SystemInfoStore)

// 创建动态的 SR_ExtraModel 选项列表
const SR_ExtraModel_options = computed(() => {
  return extraSrModelList.value.map(model => ({
    value: model,
    label: model,
  }))
})

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

// 当 SRMethodValue 变为 SR_ExtraModel 时，加载模型列表
function loadExtraSRModels(): void {
  if (SRMethodValue.value === 'SR_ExtraModel') {
    SystemInfoStore.fetchExtraSRModelList()
  }
}

// 监听 SRMethodValue 的变化
watch(SRMethodValue, () => {
  loadExtraSRModels()
})

onMounted(() => {
  // 组件加载时，如果当前方法已经是 SR_ExtraModel，则加载模型列表
  loadExtraSRModels()
})
</script>

<template>
  <n-tabs type="segment" animated>
    <!-- 分页 1：超分配置 -->
    <n-tab-pane name="sr" tab="超分">
      <div class="flex-container">
        <n-card :bordered="false" class="system-info-card-Method">
          <div class="top-switch-bar">
            <div style="border: 1px solid #dcdfe6; padding: 15px; border-radius: 6px;">
              <el-tooltip :show-after="500" content="开启后使用超分算法提升视频清晰度" placement="top">
                <el-switch
                  v-model="useSR"
                  size="large"
                  active-text="启用超分"
                  inactive-text="关闭超分"
                />
              </el-tooltip>
            </div>
            <div style="border: 1px solid #dcdfe6; padding: 15px; border-radius: 6px;">
              <el-tooltip :show-after="500" content="当前固定启用半精度以节省显存并提升性能" placement="top">
                <el-switch
                  :model-value="true"
                  size="large"
                  active-text="启动半精度"
                  inactive-text="关闭半精度"
                  disabled
                />
              </el-tooltip>
            </div>
          </div>
        </n-card>

        <div class="flex-container">
          <n-card :bordered="false" class="system-info-card-Method">
            <div class="slider-demo-block">
              <span class="demonstration">超分算法</span>
              <el-tooltip :show-after="500" content="选择要使用的超分算法选择要使用的超分算法选择要使用的超分算法选择要使用的超分算法选择要使用的超分算法" placement="top">
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
              </el-tooltip>
            </div>
          </n-card>

          <div v-if="SRMethodValue === 'Real_cugan'" class="flex-container">
            <n-card :bordered="false" class="system-info-card-Para">
              <div class="slider-demo-block">
                <span class="demonstration">推理方式(Real_cugan)</span>
                <el-tooltip :show-after="500" content="选择 RealCUGAN 的推理引擎/后端" placement="top">
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
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">超分模型(Real_cugan)</span>
                <el-tooltip :show-after="500" content="选择 RealCUGAN 使用的模型" placement="top">
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
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">切割块数量(Real_cugan)</span>
                <el-tooltip :show-after="500" content="切块数量越大越省显存，但可能增加耗时" placement="top">
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
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">强度参数(Real_cugan)</span>
                <el-tooltip :show-after="500" content="调节去噪/锐化强度，0~2 之间" placement="top">
                  <el-slider v-model="RealcuganAlphaValue" :min="0" :max="2" :step="0.1" show-input style="max-width: 450px;" />
                </el-tooltip>
              </div>
            </n-card>
          </div>

          <div v-if="SRMethodValue === 'Real_esrgan'" class="flex-container">
            <n-card :bordered="false" class="system-info-card-Para">
              <div class="slider-demo-block">
                <span class="demonstration">推理方式(Real_esrgan)</span>
                <el-tooltip :show-after="500" content="选择 RealESRGAN 的推理后端" placement="top">
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
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">超分模型(Real_esrgan)</span>
                <el-tooltip :show-after="500" content="选择 RealESRGAN 使用的模型" placement="top">
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
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">放大倍数(Real_esrgan)</span>
                <el-tooltip :show-after="500" content="选择目标放大倍率" placement="top">
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
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">切割块数量(Real_esrgan)</span>
                <el-tooltip :show-after="500" content="切块数量越大越省显存，但可能增加耗时" placement="top">
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
                </el-tooltip>
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
                <el-tooltip :show-after="500" content="选择 Waifu2x 的推理后端" placement="top">
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
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">超分模型(Waifu2x)</span>
                <el-tooltip :show-after="500" content="选择 Waifu2x 使用的模型" placement="top">
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
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">切割块数量(Waifu2x)</span>
                <el-tooltip :show-after="500" content="切块数量越大越省显存，但可能增加耗时" placement="top">
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
                </el-tooltip>
              </div>
            </n-card>
          </div>

          <div v-if="SRMethodValue === 'SR_ExtraModel'" class="flex-container">
            <n-card :bordered="false" class="system-info-card-Para">
              <div class="slider-demo-block">
                <span class="demonstration">超分模型(SR_ExtraModel)</span>
                <el-tooltip :show-after="500" content="选择外部加载的自定义超分模型" placement="top">
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
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">推理方式(SR_ExtraModel)</span>
                <el-tooltip :show-after="500" content="选择自定义模型的推理后端" placement="top">
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
                </el-tooltip>
              </div>
            </n-card>
          </div>

          <div class="flex-container-extra">
            <n-card :bordered="false" class="system-info-card-Para">
              <el-tooltip :show-after="500" content="打开高级超分参数" placement="top">
                <n-button
                  type="primary" size="small" style="height: 30px; width: 130px; background-color: #409eff; border-color: #ff6600; font-size: 18px; padding: 10px 24px; border-radius: 9px;"
                  @click="ShowSrExtra"
                >
                  Extra
                </n-button>
              </el-tooltip>
              <n-drawer v-model:show="SrExtra" :width="380" placement="right">
                <n-drawer-content title="高级设置 (SR)">
                  <div class="drawer-section">
                    <div class="drawer-section-title">
                      通用设置
                    </div>
                    <div class="drawer-item">
                      <span class="drawer-label">num_streams</span>
                      <el-tooltip :show-after="500" content="控制推理并行流数量，提升吞吐或降低占用" placement="top">
                        <el-select
                          v-model="Sr_numstreams"
                          placeholder="请选择"
                          size="default"
                          style="width: 160px"
                        >
                          <el-option
                            v-for="item in sr_numstreams_options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          />
                        </el-select>
                      </el-tooltip>
                    </div>
                  </div>

                  <n-divider style="margin: 20px 0;" />

                  <div class="drawer-section">
                    <div class="drawer-section-title">
                      TensorRT 设置
                    </div>
                    <div class="drawer-item">
                      <span class="drawer-label">cuda_graph</span>
                      <el-tooltip :show-after="500" content="启用 CUDA Graph 以减少推理开销（部分环境可提升性能）" placement="top">
                        <el-switch
                          v-model="Sr_cudagraph"
                          size="default"
                          active-text="启用"
                          inactive-text="关闭"
                        />
                      </el-tooltip>
                    </div>
                  </div>
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
              <el-tooltip :show-after="500" content="开启后使用补帧算法提升帧率" placement="top">
                <el-switch
                  v-model="useVfi"
                  size="large"
                  active-text="启用补帧"
                  inactive-text="关闭补帧"
                />
              </el-tooltip>
            </div>
            <div style="border: 1px solid #dcdfe6; padding: 15px; border-radius: 6px;">
              <el-tooltip :show-after="500" content="当前固定启用半精度以节省显存并提升性能" placement="top">
                <el-switch
                  :model-value="true"
                  size="large"
                  active-text="启动半精度"
                  inactive-text="关闭半精度"
                  disabled
                />
              </el-tooltip>
            </div>
          </div>
        </n-card>

        <div class="flex-container">
          <n-card :bordered="false" class="system-info-card-Method">
            <div class="slider-demo-block">
              <span class="demonstration">补帧算法</span>
              <el-tooltip :show-after="500" content="选择要使用的补帧算法" placement="top">
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
              </el-tooltip>
            </div>
          </n-card>

          <div v-if="VfiMethodValue === 'Rife'" class="flex-container">
            <n-card :bordered="false" class="system-info-card-Para">
              <div class="slider-demo-block">
                <span class="demonstration">推理方式(rife)</span>
                <el-tooltip :show-after="500" content="选择 RIFE 的推理后端" placement="top">
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
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">补帧模型(rife)</span>
                <el-tooltip :show-after="500" content="选择 RIFE 使用的模型" placement="top">
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
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">光流尺度(rife)</span>
                <el-tooltip :show-after="500" content="调整光流金字塔尺度，数值越高越精细但耗时更长" placement="top">
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
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">目标帧率(rife)</span>
                <el-tooltip :show-after="500" content="设置补帧后的目标帧率，60~480" placement="top">
                  <el-slider
                    v-model="RifeMultiValue" :min="60"
                    :max="480" show-input style="max-width: 500px;"
                  />
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">转场阈值(rife)</span>
                <el-tooltip :show-after="500" content="避免转场错误补帧的阈值，0~1，数值越高越保守" placement="top">
                  <el-slider
                    v-model="RifeDetectionValue" :min="0"
                    :max="1" :step="0.1" show-input style="max-width: 500px;"
                  />
                </el-tooltip>
              </div>

              <div class="slider-demo-block">
                <span class="demonstration">Ensemble(rife)</span>
                <el-tooltip :show-after="500" content="开启 Ensemble 可提升质量但会增加耗时" placement="top">
                  <el-radio-group v-model="RifeEnsembleValue">
                    <el-radio-button :value="true">
                      使用
                    </el-radio-button>
                    <el-radio-button :value="false">
                      关闭
                    </el-radio-button>
                  </el-radio-group>
                </el-tooltip>
              </div>
            </n-card>

            <div class="flex-container-extra">
              <n-card :bordered="false" class="system-info-card-Para">
                <el-tooltip :show-after="500" content="打开高级补帧参数" placement="top">
                  <n-button
                    type="primary" size="small" style="height: 30px; width: 130px; background-color: #409eff; border-color: #ff6600; font-size: 18px; padding: 10px 24px; border-radius: 9px;"
                    @click="ShowVfiExtra"
                  >
                    Extra
                  </n-button>
                </el-tooltip>
                <n-drawer v-model:show="VfiExtra" :width="380" placement="right">
                  <n-drawer-content title="高级设置 (VFI)">
                    <div class="drawer-section">
                      <div class="drawer-section-title">
                        通用设置
                      </div>
                      <div class="drawer-item">
                        <span class="drawer-label">num_streams</span>
                        <el-tooltip :show-after="500" content="控制并行流数量，平衡性能与资源" placement="top">
                          <el-select
                            v-model="Vfi_numstreams"
                            placeholder="请选择"
                            size="default"
                            style="width: 160px"
                          >
                            <el-option
                              v-for="item in vfi_numstreams_options"
                              :key="item.value"
                              :label="item.label"
                              :value="item.value"
                            />
                          </el-select>
                        </el-tooltip>
                      </div>
                    </div>

                    <n-divider style="margin: 20px 0;" />

                    <div class="drawer-section">
                      <div class="drawer-section-title">
                        TensorRT 设置
                      </div>
                      <div class="drawer-item">
                        <span class="drawer-label">cuda_graph</span>
                        <el-tooltip :show-after="500" content="启用 CUDA Graph 以减少补帧推理开销（视环境而定）" placement="top">
                          <el-switch
                            v-model="Vfi_cudagraph"
                            size="default"
                            active-text="启用"
                            inactive-text="关闭"
                          />
                        </el-tooltip>
                      </div>
                    </div>
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

/* 抽屉样式优化 */
.drawer-section {
  margin-bottom: 24px;
}

.drawer-section:last-of-type {
  margin-bottom: 0;
}

.drawer-section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e4e7ed;
}

.drawer-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  min-height: 44px;
}

.drawer-label {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
  flex-shrink: 0;
  margin-right: 16px;
}

:deep(.n-drawer-content__body) {
  padding: 20px;
}

:deep(.n-drawer-header) {
  padding: 20px 20px 16px;
  border-bottom: 1px solid #e4e7ed;
}

:deep(.n-drawer-header__main) {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

/* 自定义 el-switch 样式：方形带圆角，激活时绿色 */
.top-switch-bar :deep(.el-switch) {
  border-radius: 6px;
}

.top-switch-bar :deep(.el-switch__core) {
  border-radius: 6px;
  background-color: #dcdfe6;
}

.top-switch-bar :deep(.el-switch.is-checked .el-switch__core) {
  background-color: #89e25c;
  border-color: #67c23a;
}

.top-switch-bar :deep(.el-switch__action) {
  border-radius: 4px;
  width: 20px;
  height: 20px;
}

.top-switch-bar :deep(.el-switch.is-checked .el-switch__action) {
  left: calc(100% - 22px);
}
  </style>
