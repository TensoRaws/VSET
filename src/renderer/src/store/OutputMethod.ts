const Encoder_options = [
  { value: 'libx265', label: 'CPU_H265' },
  { value: 'libx264', label: 'CPU_H264' },
  { value: 'libaom-av1', label: 'CPU_Av1' },
  { value: 'libsvtav1', label: 'CPU_svtAv1' },

  { value: 'hevc_nvenc', label: 'NVENC_H265' },
  { value: 'h264_nvenc', label: 'NVENC_H264' },
  { value: 'av1_nvenc', label: 'NVENC_Av1' },

  { value: 'hevc_amf', label: 'AMF_H265' },
  { value: 'h264_amf', label: 'AMF_H264' },

]

const CpuH265_options = [
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
]

const CpuH264_options = [
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
]

const CpuAv1_options = [
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
]

const CpusvtAv1_options = [
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
]

const NvencH265_options = [
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

]

const NvencH264_options = [
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
]

const NvencAv1_options = [
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
]

const AmfH265_options = [
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
]

const AmfH264_options = [
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
]

const QSVH265_options = [
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
]

const QSVH264_options = [
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
]

const VideoContainer_options = [
  {
    value: '.mp4',
    label: 'MP4',
  },
  {
    value: '.mkv',
    label: 'MKV',
  },
  {
    value: '.mov',
    label: 'MOV',
  },
]

const AudioContainer_options = [
  {
    value: 'aac',
    label: 'AAC',
  },
  {
    value: 'flac',
    label: 'FLAC',
  },
]

export { AmfH264_options, AmfH265_options, AudioContainer_options, CpuAv1_options, CpuH264_options, CpuH265_options, CpusvtAv1_options, Encoder_options, NvencAv1_options, NvencH264_options, NvencH265_options, QSVH264_options, QSVH265_options, VideoContainer_options }
