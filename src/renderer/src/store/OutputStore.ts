import { defineStore } from 'pinia'
import { ref } from 'vue'

export default defineStore('outputConfig', () => {
  const bitValue = ref(20)
  const crfValue = ref(16)
  const cqValue = ref(25)
  const qbValue = ref(25)

  const encoderValue = ref('libx265')

  const Libx265QualityValue = ref('medium')
  const Libx264QualityValue = ref('medium')
  const Libaomav1QualityValue = ref('4')
  const Libsvtav1QualityValue = ref('5')
  const HevcnvencQualityValue = ref('medium')
  const H264nvencQualityValue = ref('medium')
  const Av1nvencQualityValue = ref('medium')
  const HevcamfQualityValue = ref('5')
  const H264amfQualityValue = ref('0')
  const HevcqsvQualityValue = ref('medium')
  const H264qsvQualityValue = ref('medium')

  const videoContainer = ref('MP4')
  const AudioContainer = ref('AAC')

  const isUseCrf = ref(true)
  const isSaveAudio = ref(false)
  const isSaveSubtitle = ref(false)

  const outputFolder = ref('')
  const isUseCustomParams = ref(false)
  const CustomParams = ref('')

  return {
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

    outputFolder,
    isUseCustomParams,
    CustomParams,
  }
}, {
  persist: true,
})
