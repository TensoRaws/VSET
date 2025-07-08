import { ref } from 'vue'
import { defineStore } from 'pinia'

export default defineStore('outputconfig',()=>{

    const bitValue = ref(20)
    const crfValue = ref(16)

    const encoderValue = ref('libx265')
    const qualityValue= ref('slow')
    const videoContainer=ref('MP4')
    const AudioContainer=ref('AAC')


    const isUseCrf=ref(true)
    const isSaveAudio=ref(false)

    const outputfolder=ref('')
    const encoder_options =ref([
  {
    value: 'libx265',
    label: 'CPU_H265',
  },
  {
    value: 'libx264',
    label: 'CPU_H264',
  },
  {
    value: 'libaom-av1',
    label: 'CPU_Av1',
  },
  {
    value: 'hevc_nvenc',
    label: 'NVENC_H265',
  },
  {
    value: 'h264_nvenc',
    label: 'NVENC_H264',
  },
  {
    value: 'av1_nvenc',
    label: 'NVENC_Av1',
  },
])

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

const NvencH264_options=ref([
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
  }
])

const NvencAv1_options=ref([
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
  }
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
    videoContainer,
    AudioContainer,
    isUseCrf,

    isSaveAudio,
    encoder_options,
    CpuH265_options,
    CpuH264_options,

    CpuAv1_options,
    NvencH265_options,
    NvencH264_options,
    NvencAv1_options,

    VideoContainer_options,
    AudioContainer_options,

    outputfolder

  }
})