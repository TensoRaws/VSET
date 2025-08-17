import { defineStore } from 'pinia'
import { ref } from 'vue'

export default defineStore('srsettingconfig', () => {
  const useSR = ref(true)
  const SRMethodValue = ref('Real_cugan')

  const RealcuganTileValue = ref('1')
  const RealcuganInferenceValue = ref('Cuda')
  const RealcuganModelValue = ref('pro-conservative-up2x')
  const RealcuganAlphaValue = ref(1)

  const RealesrganInferenceValue = ref('Cuda')
  const RealesrganModelValue = ref('animevideov3')
  const RealesrganTileValue = ref('1')
  const RealesrganScaleValue = ref('2')

  // const ArtCNNInferenceValue=ref('Cuda')
  // const ArtCNNModelValue = ref('ArtCNN_C4F32')
  // const ArtCNNTileValue = ref('1')

  const Waifu2xInferenceValue = ref('Cuda')
  const Waifu2xModelValue = ref('anime_style_art_rgb_noise0')
  const Waifu2xTileValue = ref('1')

  const SwinIRInferenceValue = ref('Cuda')
  const SwinIRModelValue = ref('lightweightSR_DIV2K_s64w8_SwinIR_S_x2')
  const SwinIRTileValue = ref('1')

  const SR_ExtraModelInferenceValue = ref('Cuda')
  const SR_ExtraModelValue = ref('AniSD_DC_SPAN_x2')

  const Sr_numstreams = ref('1')
  const Sr_cudagraph = ref(false)

  return {
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

    //   ArtCNNInferenceValue,
    //   ArtCNNModelValue,
    //   ArtCNNTileValue,

    Waifu2xInferenceValue,
    Waifu2xModelValue,
    Waifu2xTileValue,

    SwinIRInferenceValue,
    SwinIRModelValue,
    SwinIRTileValue,

    SR_ExtraModelValue,
    SR_ExtraModelInferenceValue,

    Sr_numstreams,
    Sr_cudagraph,
  // }
  }
}, {
  persist: true,
})
