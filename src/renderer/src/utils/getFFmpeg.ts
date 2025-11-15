import useOutputconfigStore from '@renderer/store/OutputStore'
import { MagicStr } from '@shared/constant/magicStr'
import { storeToRefs } from 'pinia'

export function buildFFmpegCMD(): string[] {
  // Output
  const OutputConfigStore = useOutputconfigStore()
  const {
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
    isUseCrf,
  } = storeToRefs(OutputConfigStore)

  // ✅ 返回 JSON 对象
  let cmd_major = ''
  let cmd_minor = ''

  cmd_major
      += `"-hide_banner" "-y" "-i" "pipe:" "-i" "__VIDEO_PATH__"`
        + ` "-map" "0:v:0" `

  cmd_minor += `"-c:v" "${encoderValue.value}" `

  if (encoderValue.value === 'libx265') {
    cmd_minor
        += `"-pix_fmt" "yuv420p10le" "-profile:v" "main10" "-vtag" "hvc1" `
          + `"-preset" "${
            Libx265QualityValue.value
          }" `
    if (isUseCrf.value === true) {
      cmd_minor += `"-crf" "${crfValue.value}" `
    }
    else {
      cmd_minor += `"-b:v" "${bitValue.value}m" `
    }
  }

  if (encoderValue.value === 'libx264') {
    cmd_minor
        += `"-pix_fmt" "yuv420p" "-profile:v" "main" `
          + `"-preset" "${
            Libx264QualityValue.value
          }" `
    if (isUseCrf.value === true) {
      cmd_minor += `"-crf" "${crfValue.value}" `
    }
    else {
      cmd_minor += `"-b:v" "${bitValue.value}M" `
    }
  }

  if (encoderValue.value === 'libaom-av1') {
    cmd_minor += `"-pix_fmt" "yuv420p10le" ` + `"-cpu-used" "${Libaomav1QualityValue.value}" `
    if (isUseCrf.value === true) {
      cmd_minor += `"-crf" "${crfValue.value}" `
    }
    else {
      cmd_minor += `"-b:v" "${bitValue.value}M" `
    }
  }

  if (encoderValue.value === 'libsvtav1') {
    cmd_minor += `"-pix_fmt" "yuv420p10le" ` + `"-preset" "${Libsvtav1QualityValue.value}" `
    if (isUseCrf.value === true) {
      cmd_minor += `"-crf" "${crfValue.value}" `
    }
    else {
      cmd_minor += `"-b:v" "${bitValue.value}M" `
    }
  }

  if (encoderValue.value === 'h264_nvenc') {
    cmd_minor
        += `"-pix_fmt" "yuv420p" `
          + `"-preset" "${
            H264nvencQualityValue.value
          }" `
          + `"-cq" "${
            cqValue.value
          }" `
  }

  if (encoderValue.value === 'hevc_nvenc') {
    cmd_minor
        += `"-pix_fmt" "p010le" "-profile:v" "main10" "-vtag" "hvc1" `
          + `"-preset" "${
            HevcnvencQualityValue.value
          }" `
          + `"-cq" "${
            cqValue.value
          }" `
  }

  if (encoderValue.value === 'av1_nvenc') {
    cmd_minor
        += `"-pix_fmt" "p010le" `
          + `"-preset" "${
            Av1nvencQualityValue.value
          }" `
          + `"-qp" "${
            qbValue.value
          }" `
  }

  if (encoderValue.value === 'hevc_amf') {
    cmd_minor
        += `"-pix_fmt" "yuv420p" `
          + `"-quality" "${
            HevcamfQualityValue.value
          }" `
          + `"-qp" "${
            qbValue.value
          }" `
  }

  if (encoderValue.value === 'h264_amf') {
    cmd_minor
        += `"-pix_fmt" "yuv420p" `
          + `"-quality" "${
            H264amfQualityValue.value
          }" `
          + `"-qp" "${
            qbValue.value
          }" `
  }

  if (encoderValue.value === 'h265_qsv') {
    cmd_minor
        += `"-pix_fmt" "p010le" "-profile:v" "main10" `
          + `"-preset" "${
            HevcqsvQualityValue.value
          }" `
          + `"-qp" "${
            qbValue.value
          }" `
  }

  if (encoderValue.value === 'h264_qsv') {
    cmd_minor
        += `"-pix_fmt" "nv12" `
          + `"-preset" "${
            H264qsvQualityValue.value
          }" `
          + `"-qp" "${
            qbValue.value
          }" `
  }

  cmd_minor += `"${MagicStr.VIDEO_NAME}"`

  const vspipecmd = `"-c" "y4m" "${MagicStr.VPY_PATH}" "-"`
  return [vspipecmd, cmd_major, cmd_minor]
}
