import { defineStore } from 'pinia'
import { ref } from 'vue'

const defaultEncoderOptions = [
  { value: 'libx265', label: 'CPU_H265' },
  { value: 'libx264', label: 'CPU_H264' },
  { value: 'libaom-av1', label: 'CPU_Av1' },
  { value: 'libsvtav1', label: 'CPU_svtAv1' },
  { value: 'hevc_nvenc', label: 'NVENC_H265' },
  { value: 'h264_nvenc', label: 'NVENC_H264' },
  { value: 'av1_nvenc', label: 'NVENC_Av1' },
]

export default defineStore('outputconfig', () => {
  const bitValue = ref(20)
  const crfValue = ref(16)

  const encoderValue = ref('libx265')
  const qualityValue = ref('slow')
  const videoContainer = ref('MP4')
  const AudioContainer = ref('AAC')

  const cpusvtav1_qualityValue = ref('3')

  const isUseCrf = ref(true)
  const isSaveAudio = ref(false)
  const isSavesubtitle = ref(false)

  const outputfolder = ref('')
  const encoder_options = ref([...defaultEncoderOptions])

  const CpuH265_options = ref([
    {
      value: 'veryslow',
      label: 'veryslow',
    },
    {
      value: 'slower',
      label: 'slower',
    },
    {
      value: 'slow',
      label: 'slow',
    },
    {
      value: 'medium',
      label: 'medium',
    },
    {
      value: 'fast',
      label: 'fast',
    },
    {
      value: 'faster',
      label: 'faster',
    },
    {
      value: 'veryfast',
      label: 'veryfast',
    },
  ])

  const CpuH264_options = CpuH265_options
  const CpuAv1_options = CpuH265_options

  const CpusvtAv1_options = ref([
    {
      value: '0',
      label: '0',
    },
    {
      value: '1',
      label: '1',
    },
    {
      value: '2',
      label: '2',
    },
    {
      value: '3',
      label: '3',
    },
    {
      value: '4',
      label: '4',
    },
    {
      value: '5',
      label: '5',
    },
    {
      value: '6',
      label: '6',
    },
    {
      value: '7',
      label: '7',
    },
    {
      value: '8',
      label: '8',
    },
    {
      value: '9',
      label: '9',
    },
    {
      value: '10',
      label: '10',
    },
    {
      value: '11',
      label: '11',
    },
    {
      value: '12',
      label: '12',
    },
    {
      value: '13',
      label: '13',
    },
  ])

  const NvencH265_options = ref([
    {
      value: 'slow',
      label: 'slow',
    },
    {
      value: 'medium',
      label: 'medium',
    },
    {
      value: 'fast',
      label: 'fast',
    },
    {
      value: 'hp',
      label: 'hp',
    },
    {
      value: 'hq',
      label: 'hq',
    },
    {
      value: 'bd',
      label: 'bd',
    },
    {
      value: 'll',
      label: 'll',
    },
    {
      value: 'llhq',
      label: 'llhq',
    },
    {
      value: 'llhp',
      label: 'llhp',
    },
    {
      value: 'p1',
      label: 'p1',
    },
    {
      value: 'p2',
      label: 'p2',
    },
    {
      value: 'p3',
      label: 'p3',
    },
    {
      value: 'p4',
      label: 'p4',
    },
    {
      value: 'p5',
      label: 'p5',
    },
    {
      value: 'p6',
      label: 'p6',
    },
    {
      value: 'p7',
      label: 'p7',
    },

  ])

  const NvencH264_options = ref([
    {
      value: 'slow',
      label: 'slow',
    },
    {
      value: 'medium',
      label: 'medium',
    },
    {
      value: 'fast',
      label: 'fast',
    },
    {
      value: 'hp',
      label: 'hp',
    },
    {
      value: 'hq',
      label: 'hq',
    },
    {
      value: 'bd',
      label: 'bd',
    },
    {
      value: 'll',
      label: 'll',
    },
    {
      value: 'llhq',
      label: 'llhq',
    },
    {
      value: 'llhp',
      label: 'llhp',
    },
  ])

  const NvencAv1_options = ref([
    {
      value: 'slow',
      label: 'slow',
    },
    {
      value: 'medium',
      label: 'medium',
    },
    {
      value: 'fast',
      label: 'fast',
    },
    {
      value: 'hp',
      label: 'hp',
    },
    {
      value: 'hq',
      label: 'hq',
    },
  ])

  const VideoContainer_options = ref([
    {
      value: 'mp4',
      label: 'MP4',
    },
    {
      value: 'mkv',
      label: 'MKV',
    },
    {
      value: 'mov',
      label: 'MOV',
    },
  ])

  const AudioContainer_options = ref([
    {
      value: 'aac',
      label: 'AAC',
    },
    {
      value: 'flac',
      label: 'FLAC',
    },
  ])

  return {
    bitValue,
    crfValue,
    encoderValue,
    qualityValue,

    cpusvtav1_qualityValue,
    CpusvtAv1_options,

    videoContainer,
    AudioContainer,
    isUseCrf,

    isSaveAudio,
    isSavesubtitle,
    encoder_options,
    CpuH265_options,
    CpuH264_options,

    CpuAv1_options,
    NvencH265_options,
    NvencH264_options,
    NvencAv1_options,

    VideoContainer_options,
    AudioContainer_options,

    outputfolder,
  }
}, {
  persist: {
    afterRestore: (ctx) => {
      // 1. 确保 encoderValue 有默认值
      if (!ctx.store.encoderValue) {
        ctx.store.encoderValue = 'libx265'
      }

      // 2. 合并 encoder_options 默认值
      const existingValues = new Set(ctx.store.encoder_options.map(e => e.value))
      defaultEncoderOptions.forEach((opt) => {
        if (!existingValues.has(opt.value)) {
          ctx.store.encoder_options.push(opt)
        }
      })
    },
  },
} as any)
