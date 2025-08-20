import { defineStore } from 'pinia'
import { ref } from 'vue'

export default defineStore('VfiSettingConfig', () => {
  const useVfi = ref(false)
  const VfiMethodValue = ref('Rife')

  const RifeInferenceValue = ref('Cuda')
  const RifeModelValue = ref('v4_0')
  const RifeScaleValue = ref(1.0)
  const RifeMultiValue = ref(120)
  const RifeEnsembleValue = ref(false)
  const RifeDetectionValue = ref(0.5)

  const Vfi_numstreams = ref('1')
  const Vfi_cudagraph = ref(false)

  return {
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
  }
}, {
  persist: true,
})
