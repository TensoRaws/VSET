import { Buffer } from 'node:buffer'
import { exec as execCallback, spawn } from 'node:child_process'
import { writeFileSync } from 'node:fs'
import path from 'node:path'
import { promisify } from 'node:util'
import iconv from 'iconv-lite'
import { addProcess, removeProcess } from './childProcessManager'
import { getExecPath, getExtraSRModelPath, getGenVpyPath } from './getCorePath'

const exec = promisify(execCallback)

function generate_cmd(config_json, vipipePath, vpyPath, ffmpegPath, video, hasAudio, hasSubtitle): string {
  let cmd = `"${vipipePath}"` + ` "-c" "y4m" "${vpyPath}" "-" | "${
    ffmpegPath}" "-hide_banner" "-y" "-i" "pipe:" "-i" "${video}"`
    + ` "-map" "0:v:0" `
  if (hasAudio) {
    cmd += '"-map" "1:a" '
  }

  cmd += `"-c:v" "${config_json.encoderValue}" `

  if (hasSubtitle && config_json.isSavesubtitle === true) {
    cmd += '"-map" "1:s" "-c:s" "copy" '
  }

  if (config_json.encoderValue === 'libx265') {
    cmd += '"-pix_fmt" "yuv420p10le" "-profile:v" "main10" "-vtag" "hvc1" '
  }
  if (config_json.encoderValue === 'libx264') {
    cmd += '"-pix_fmt" "yuv420p" "-profile:v" "main" '
  }
  if (config_json.encoderValue === 'libaom-av1') {
    cmd += '"-pix_fmt" "yuv420p10le" '
  }
  if (config_json.encoderValue === 'h264_nvenc') {
    cmd += '"-pix_fmt" "yuv420p" '
  }
  if (config_json.encoderValue === 'hevc_nvenc') {
    cmd += '"-pix_fmt" "p010le" "-profile:v" "main10" "-vtag" "hvc1" '
  }
  if (config_json.encoderValue === 'av1_nvenc') {
    cmd += '"-pix_fmt" "p010le" '
  }
  if (config_json.encoderValue === 'libsvtav1') {
    cmd += '"-pix_fmt" "yuv420p10le" '
  }
  if (config_json.encoderValue === 'libsvtav1') {
    cmd += `-preset ` + `"${config_json.cpusvtav1_qualityValue}" `
  }
  else {
    cmd += `-preset ` + `"${config_json.qualityValue}" `
  }
  if (config_json.isUseCrf === true) {
    if (config_json.encoderValue.includes('nvenc')) {
      cmd += `"-cq" ` + `"${config_json.crfValue}" `
    }
    else {
      cmd += `"-crf" ` + `"${config_json.crfValue}" `
    }
  }
  else {
    cmd += `"-b:v" ` + `"${config_json.bitValue}M" `
  }
  if (hasAudio === true) {
    if (config_json.isSaveAudio === true) {
      cmd += '"-c:a" "copy" '
    }
    else {
      cmd += `"-c:a" ` + `"${config_json.AudioContainer.toLowerCase()}" `
    }
  }

  // 最终cmd命令
  cmd += `"${config_json.outputfolder}/${path.parse(path.basename(video)).name}_enhance` + `.${config_json.videoContainer.toLowerCase()}"`
  return cmd
}

function generate_vpy(config_json, videoName): string {
  let vpyContent = ''

  vpyContent += 'import vapoursynth as vs\n'
  vpyContent += 'core = vs.core\n'
  vpyContent += `res = core.lsmas.LWLibavSource(r"${videoName}")\n`
  vpyContent += 'from vsmlrt import CUGAN,RealESRGAN,Waifu2x,RIFE,ArtCNN,SwinIR,Backend\n'
  vpyContent += 'import vsmlrt\n'

  // 前置缩放(需要在此改进色彩控制)
  if (config_json.UseResize_BeforeEnhance === true) {
    vpyContent
    += `res = core.resize.Bicubic(clip=res,width=${config_json.ResizeWidth_BeforeEnhance
      },height=${config_json.ResizeHeight_BeforeEnhance},format=vs.YUV420P16)\n`
  }
  else {
    vpyContent += 'res = core.resize.Bicubic(clip=res,format=vs.YUV420P16)\n'
  }

  vpyContent += `res = core.std.Crop(clip=res,left=${config_json.ReduceLeft_BeforeEnhance
  }, right=${config_json.ReduceRight_BeforeEnhance
  }, top=${config_json.ReduceOn_BeforeEnhance
  }, bottom=${config_json.ReduceDown_BeforeEnhance})\n`

  // 超分
  if (config_json.useSR === true) {
    vpyContent += 'res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n'
    vpyContent += 'res=core.fmtc.bitdepth(res, bits=32)\n'

    // 超分设备
    if (config_json.SRMethodValue === 'Real_cugan') {
      if (config_json.RealcuganInferenceValue === 'Cuda') {
        vpyContent += 'device_sr=Backend.ORT_CUDA()\n'
      }
      if (config_json.RealcuganInferenceValue === 'TensorRt') {
        vpyContent += 'device_sr=Backend.TRT_RTX()\n'
        vpyContent += `device_sr.use_cuda_graph = ${
          config_json.Sr_cudagraph.charAt(0).toUpperCase() + config_json.Sr_cudagraph.slice(1)
        }\n`
      }
      if (config_json.RealcuganInferenceValue === 'TensorRt_RTX') {
        vpyContent += 'device_sr=Backend.MIGX()\n'
      }
      if (config_json.RealcuganInferenceValue === 'NCNN') {
        vpyContent += 'device_sr=Backend.NCNN_VK()\n'
      }
      if (config_json.RealcuganInferenceValue === 'DML') {
        vpyContent += 'device_sr=Backend.ORT_DML()\n'
      }
      if (config_json.RealcuganInferenceValue === 'MIGX') {
        vpyContent += 'device_sr=Backend.MIGX()\n'
      }
    }
    if (config_json.SRMethodValue === 'Real_esrgan') {
      if (config_json.RealesrganInferenceValue === 'Cuda') {
        vpyContent += 'device_sr=Backend.ORT_CUDA()\n'
      }
      if (config_json.RealesrganInferenceValue === 'TensorRt') {
        vpyContent += 'device_sr=Backend.TRT()\n'
        vpyContent += `device_sr.use_cuda_graph = ${
          config_json.Sr_cudagraph.charAt(0).toUpperCase() + config_json.Sr_cudagraph.slice(1)
        }\n`
      }
      if (config_json.RealesrganInferenceValue === 'TensorRt_RTX') {
        vpyContent += 'device_sr=Backend.TRT_RTX()\n'
      }
      if (config_json.RealesrganInferenceValue === 'NCNN') {
        vpyContent += 'device_sr=Backend.NCNN_VK()\n'
      }
      if (config_json.RealesrganInferenceValue === 'DML') {
        vpyContent += 'device_sr=Backend.ORT_DML()\n'
      }
      if (config_json.RealesrganInferenceValue === 'MIGX') {
        vpyContent += 'device_sr=Backend.MIGX()\n'
      }
    }
    if (config_json.SRMethodValue === 'Waifu2x') {
      if (config_json.Waifu2xInferenceValue === 'Cuda') {
        vpyContent += 'device_sr=Backend.ORT_CUDA()\n'
      }
      if (config_json.Waifu2xInferenceValue === 'TensorRt') {
        vpyContent += 'device_sr=Backend.TRT()\n'
        vpyContent += `device_sr.use_cuda_graph = ${
          config_json.Sr_cudagraph.charAt(0).toUpperCase() + config_json.Sr_cudagraph.slice(1)
        }\n`
      }
      if (config_json.Waifu2xInferenceValue === 'TensorRt_RTX') {
        vpyContent += 'device_sr=Backend.TRT_RTX()\n'
      }
      if (config_json.Waifu2xInferenceValue === 'NCNN') {
        vpyContent += 'device_sr=Backend.NCNN_VK()\n'
      }
      if (config_json.Waifu2xInferenceValue === 'DML') {
        vpyContent += 'device_sr=Backend.ORT_DML()\n'
      }
      if (config_json.Waifu2xInferenceValue === 'MIGX') {
        vpyContent += 'device_sr=Backend.MIGX()\n'
      }
    }
    if (config_json.SRMethodValue === 'SR_ExtraModel') {
      if (config_json.SR_ExtraModelInferenceValue === 'Cuda') {
        vpyContent += 'device_sr=Backend.ORT_CUDA()\n'
      }
      if (config_json.SR_ExtraModelInferenceValue === 'TensorRt') {
        vpyContent += 'device_sr=Backend.TRT()\n'
        vpyContent += `device_sr.use_cuda_graph = ${
          config_json.Sr_cudagraph.charAt(0).toUpperCase() + config_json.Sr_cudagraph.slice(1)
        }\n`
      }
      if (config_json.SR_ExtraModelInferenceValue === 'NCNN') {
        vpyContent += 'device_sr=Backend.NCNN_VK()\n'
      }
      if (config_json.SR_ExtraModelInferenceValue === 'DML') {
        vpyContent += 'device_sr=Backend.ORT_DML()\n'
      }
      if (config_json.SR_ExtraModelInferenceValue === 'MIGX') {
        vpyContent += 'device_sr=Backend.MIGX()\n'
      }
    }

    vpyContent += 'device_sr.device_id=0\n'
    vpyContent += 'device_sr.fp16=True\n'
    vpyContent += `device_sr.num_streams=${config_json.Sr_numstreams}\n`

    if (config_json.SRMethodValue === 'Real_cugan') {
      const model_switch = {
        'pro-conservative-up2x': [0, 2, 2],
        'pro-conservative-up3x': [0, 3, 2],
        'pro-denoise3x-up2x': [3, 2, 2],
        'pro-denoise3x-up3x': [3, 3, 2],
        'pro-no-denoise3x-up2x': [-1, 2, 2],
        'pro-no-denoise3x-up3x': [-1, 3, 2],
        'up2x-latest-conservative': [0, 2, 1],
        'up2x-latest-denoise1x': [1, 2, 1],
        'up2x-latest-denoise2x': [2, 2, 1],
        'up2x-latest-denoise3x': [3, 2, 1],
        'up2x-latest-no-denoise': [-1, 2, 1],
        'up3x-latest-conservative': [0, 3, 1],
        'up3x-latest-denoise3x': [3, 3, 1],
        'up3x-latest-no-denoise': [-1, 3, 1],
        'up4x-latest-conservative': [0, 4, 1],
        'up4x-latest-denoise3x': [3, 4, 1],
        'up4x-latest-no-denoise': [-1, 4, 1],
      }
      const [noise, scale, version] = model_switch[config_json.RealcuganModelValue] || [0, 2, 2]
      vpyContent += `res = CUGAN(res, noise=${noise}, scale=${scale}, tiles=${config_json.RealcuganTileValue}, version=${version}, alpha=${config_json.RealcuganAlphaValue}, backend=device_sr)\n`
    }

    if (config_json.SRMethodValue === 'Real_esrgan') {
      const model_switch = {
        'animevideov3': 0,
        'animevideo-xsx2': 1,
        'animevideo-xsx4': 2,
        'animejanaiV2L1': 5005,
        'animejanaiV2L2': 5006,
        'animejanaiV2L3': 5007,
        'animejanaiV3_HD_L1': 5008,
        'animejanaiV3_HD_L2': 5009,
        'animejanaiV3_HD_L3': 5010,
        'Ani4Kv2_G6i2_Compact ': 7000,
        'Ani4Kv2_G6i2_UltraCompact ': 7001,
        'AniScale_x2': 7010,
        'AniScale2_Refiner_x1': 7011,
        'AniScale2S_Compact_x2': 7012,
        'AniSD_AC_Compact_x2': 7013,
        'AniSD_Compact_x2': 7014,
        'AniSD_DB_Compact_x1': 7015,
        'AniSD_PS_Compact_x2': 7016,
      }
      const model = model_switch[config_json.RealesrganModelValue] || 0
      vpyContent += `res = RealESRGAN(res, scale=${config_json.RealesrganScaleValue},tiles=${
        config_json.RealesrganTileValue},model=${model}, backend=device_sr)\n`
    }

    // if (config_json.SRMethodValue=='ArtCNN'){
    //   const model_switch = {
    //           'ArtCNN_C4F32': 0,
    //           'ArtCNN_C4F32_DS': 1,
    //           'ArtCNN_C16F64': 2,
    //           'ArtCNN_C16F64_DS' :3 ,
    //           'ArtCNN_C4F32_Chroma' : 4,
    //           'ArtCNN_C16F64_Chroma' : 5,
    //           'ArtCNN_R16F96' : 6,
    //           'ArtCNN_R8F64' : 7,
    //           'ArtCNN_R8F64_DS' : 8,
    //           'ArtCNN_R8F64_Chroma ' : 9,
    //           'ArtCNN_C4F16 ' : 10,
    //           'ArtCNN_C4F16_DS ' : 11,
    //   };
    //   const model = model_switch[config_json.ArtCNNModelValue] || 0;
    //   vpyContent +='res = core.resize.Bicubic(clip=res, matrix_s="709", format=vs.YUV444PS)\n'

    //   vpyContent +='res = ArtCNN(res, tiles=' +
    //   config_json.ArtCNNTileValue + ', model=' + model + ', backend=device_sr)\n'
    // }

    if (config_json.SRMethodValue === 'Waifu2x') {
      const model_switch = {
        'anime_style_art_rgb_noise0': [1, 0, 1],
        'anime_style_art_rgb_noise1': [1, 1, 1],
        'anime_style_art_rgb_noise2': [1, 2, 1],
        'anime_style_art_rgb_noise3': [1, 3, 1],
        'anime_style_art_rgb_scale2.0x': [1, -1, 2],

        'photo_noise0': [2, 0, 1],
        'photo_noise1': [2, 1, 1],
        'photo_noise2': [2, 2, 1],
        'photo_noise3': [2, 3, 1],
        'photo_scale2.0x': [2, -1, 2],

        'upconv_7_anime_style_art_rgb_noise0_scale2.0x': [3, 0, 2],
        'upconv_7_anime_style_art_rgb_noise1_scale2.0x': [3, 1, 2],
        'upconv_7_anime_style_art_rgb_noise2_scale2.0x': [3, 2, 2],
        'upconv_7_anime_style_art_rgb_noise3_scale2.0x': [3, 3, 2],
        'upconv_7_anime_style_art_rgb_scale2.0x': [3, -1, 2],

        'upconv_7_photo_noise0_scale2.0x': [4, 0, 2],
        'upconv_7_photo_noise1_scale2.0x': [4, 1, 2],
        'upconv_7_photo_noise2_scale2.0x': [4, 2, 2],
        'upconv_7_photo_noise3_scale2.0x': [4, 3, 2],
        'upconv_7_photo_scale2.0x_': [4, -1, 2],

        'upresnet10_noise0_scale2.0x': [5, 0, 2],
        'upresnet10_noise1_scale2.0x': [5, 1, 2],
        'upresnet10_noise2_scale2.0x': [5, 2, 2],
        'upresnet10_noise3_scale2.0x': [5, 3, 2],
        'upresnet10_scale2.0x': [5, -1, 2],

        'cunet_noise0': [6, 0, 1],
        'cunet_noise1': [6, 1, 1],
        'cunet_noise2': [6, 2, 1],
        'cunet_noise3': [6, 3, 1],
        'cunet_noise0_scale2.0x': [6, 0, 2],
        'cunet_noise1_scale2.0x': [6, 1, 2],
        'cunet_noise2_scale2.0x': [6, 2, 2],
        'cunet_noise3_scale2.0x': [6, 3, 2],
        'cunet_scale2.0x': [6, -1, 2],

        'swin_unet_art_noise0': [7, 0, 1],
        'swin_unet_art_noise0_scale2x': [7, 0, 2],
        'swin_unet_art_noise0_scale4x': [7, 0, 4],
        'swin_unet_art_noise1': [7, 1, 1],
        'swin_unet_art_noise1_scale2x': [7, 1, 2],
        'swin_unet_art_noise1_scale4x': [7, 1, 4],
        'swin_unet_art_noise2': [7, 2, 1],
        'swin_unet_art_noise2_scale2x': [7, 2, 2],
        'swin_unet_art_noise2_scale4x': [7, 2, 4],
        'swin_unet_art_noise3': [7, 3, 1],
        'swin_unet_art_noise3_scale2x': [7, 3, 2],
        'swin_unet_art_noise3_scale4x': [7, 3, 4],
        'swin_unet_art_scale2x': [7, -1, 2],
        'swin_unet_art_scale4x': [7, -1, 4],

        'swin_unet_photo_noise0_scale4x': [8, 0, 4],
        'swin_unet_photo_noise1_scale4x': [8, 1, 4],
        'swin_unet_photo_noise2_scale4x': [8, 2, 4],
        'swin_unet_photo_noise3_scale4x': [8, 3, 4],
        'swin_unet_photo_scale4x': [8, -1, 4],

        'swin_unet_photo_v2_noise0_scale4x': [9, 0, 4],
        'swin_unet_photo_v2_noise1_scale4x': [9, 1, 4],
        'swin_unet_photo_v2_noise2_scale4x': [9, 2, 4],
        'swin_unet_photo_v2_noise3_scale4x': [9, 3, 4],
        'swin_unet_photo_v2_scale4x': [9, -1, 4],

        'swin_unet_art_scan_noise0_scale4x': [10, 0, 4],
        'swin_unet_art_scan_noise1_scale4x': [10, 1, 4],
        'swin_unet_art_scan_noise2_scale4x': [10, 2, 4],
        'swin_unet_art_scan_noise3_scale4x': [10, 3, 4],
        'swin_unet_art_scan_scale4x': [10, -1, 4],
      }
      const [model, noise, scale] = model_switch[config_json.Waifu2xModelValue] || [1, 0, 1]
      vpyContent += `res = Waifu2x(res, noise=${noise}, scale=${scale}, tiles=${config_json.Waifu2xTileValue}, model=${model}, backend=device_sr)\n`
    }

    // if (config_json.SRMethodValue=='SwinIR'){
    //   const model_switch = {
    //           'lightweightSR_DIV2K_s64w8_SwinIR_S_x2': 0,
    //           'lightweightSR_DIV2K_s64w8_SwinIR_S_x3': 1,
    //           'lightweightSR_DIV2K_s64w8_SwinIR_S_x4': 2,
    //           'realSR_BSRGAN_DFOWMFC_s64w8_SwinIR_L_x4_GAN': 3,
    //           'realSR_BSRGAN_DFOWMFC_s64w8_SwinIR_L_x4_PSNR': 5,
    //           'classicalSR_DF2K_s64w8_SwinIR_M_x2': 6,
    //           'classicalSR_DF2K_s64w8_SwinIR_M_x3': 7,
    //           'classicalSR_DF2K_s64w8_SwinIR_M_x4': 8,
    //           'classicalSR_DF2K_s64w8_SwinIR_M_x8': 9,
    //           'realSR_BSRGAN_DFO_s64w8_SwinIR_M_x2_GAN': 10,
    //           'realSR_BSRGAN_DFO_s64w8_SwinIR_M_x2_PSNR': 11,
    //           'realSR_BSRGAN_DFO_s64w8_SwinIR_M_x4_GAN': 12,
    //           'realSR_BSRGAN_DFO_s64w8_SwinIR_M_x4_PSNR': 13,
    //           // 'grayDN_DFWB_s128w8_SwinIR_M_noise15': 14,
    //           // 'grayDN_DFWB_s128w8_SwinIR_M_noise25': 15,
    //           // 'grayDN_DFWB_s128w8_SwinIR_M_noise50': 16,
    //           'colorDN_DFWB_s128w8_SwinIR_M_noise15': 17,
    //           'colorDN_DFWB_s128w8_SwinIR_M_noise25': 18,
    //           'colorDN_DFWB_s128w8_SwinIR_M_noise50': 19,
    //           'CAR_DFWB_s126w7_SwinIR_M_jpeg10': 20,
    //           'CAR_DFWB_s126w7_SwinIR_M_jpeg20': 21,
    //           'CAR_DFWB_s126w7_SwinIR_M_jpeg30': 22,
    //           'CAR_DFWB_s126w7_SwinIR_M_jpeg40': 23,
    //           'colorCAR_DFWB_s126w7_SwinIR_M_jpeg10': 24,
    //           'colorCAR_DFWB_s126w7_SwinIR_M_jpeg20': 25,
    //           'colorCAR_DFWB_s126w7_SwinIR_M_jpeg30': 26,
    //           'colorCAR_DFWB_s126w7_SwinIR_M_jpeg40': 27
    //   };
    //   const model = model_switch[config_json.SwinIRModelValue] || 0;
    //   vpyContent +='res = SwinIR(res, tiles=' +
    //   config_json.SwinIRTileValue + ', model=' + model + ', backend=device_sr)\n'
    // }

    if (config_json.SRMethodValue === 'SR_ExtraModel') {
      const model_switch = {
        AniSD_DC_SPAN_x2: 'AniSD_DC_SPAN_x2',
      }

      const model = `${getExtraSRModelPath()}/${model_switch[config_json.SR_ExtraModelValue] || 'AniSD_DC_SPAN_x2'}`

      vpyContent += `res = vsmlrt.inference(res, network_path="${model}", backend=device_sr)\n`
    }
  }

  // 补帧
  if (config_json.useVfi === true) {
    vpyContent += 'res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n'
    vpyContent += 'res=core.fmtc.bitdepth(res, bits=32)\n'

    if (config_json.VfiMethodValue === 'Rife') {
      if (config_json.RifeInferenceValue === 'Cuda') {
        vpyContent += 'device_vfi=Backend.ORT_CUDA()\n'
      }
      if (config_json.RifeInferenceValue === 'TensorRt') {
        vpyContent += 'device_vfi=Backend.TRT()\n'
        vpyContent += `device_vfi.use_cuda_graph = ${
          config_json.Vfi_cudagraph.charAt(0).toUpperCase() + config_json.Vfi_cudagraph.slice(1)
        }\n`
      }
      if (config_json.RifeInferenceValue === 'TensorRt_RTX') {
        vpyContent += 'device_vfi=Backend.TRT_RTX()\n'
      }
      if (config_json.RifeInferenceValue === 'NCNN') {
        vpyContent += 'device_vfi=Backend.NCNN_VK()\n'
      }
      if (config_json.RifeInferenceValue === 'DML') {
        vpyContent += 'device_vfi=Backend.ORT_DML()\n'
      }
      if (config_json.RifeInferenceValue === 'MIGX') {
        vpyContent += 'device_vfi=Backend.MIGX()\n'
      }
    }

    vpyContent += 'device_vfi.device_id=0\n'
    vpyContent += 'device_vfi.fp16=True\n'
    vpyContent += `device_sr.num_streams=${config_json.Vfi_numstreams}\n`
    vpyContent += 'from fractions import Fraction\n'

    if (config_json.VfiMethodValue === 'Rife') {
      const model_switch = {
        v4_0: 40,
        v4_2: 42,
        v4_3: 43,
        v4_4: 44,
        v4_5: 45,
        v4_6: 46,
        v4_7: 47,
        v4_8: 48,
        v4_9: 49,
        v4_10: 410,
        v4_11: 411,
        v4_12: 412,
        v4_12_lite: 4121,
        v4_13: 413,
        v4_13_lite: 4131,
        v4_14: 414,
        v4_14_lite: 4141,
        v4_15: 415,
        v4_15_lite: 4151,
        v4_16_lite: 4161,
        v4_17: 417,
        v4_17_lite: 4171,
        v4_18: 418,
        v4_19: 419,
        v4_20: 420,
        v4_21: 421,
        v4_22: 422,
        v4_22_lite: 4221,
        v4_23: 423,
        v4_24: 424,
        v4_25: 425,
        v4_25_lite: 4251,
        v4_25_heavy: 4252,
        v4_26: 426,
        v4_26_heavy: 4262,
      }
      const model = model_switch[config_json.RifeModelValue] || 40
      const EnsembleBool = config_json.RifeEnsembleValue ? 'True' : 'False'
      vpyContent += `res = core.misc.SCDetect(res,threshold=${config_json.RifeDetectionValue})\n`

      vpyContent += 'res_height = (32 - res.height % 32) % 32\n'
      vpyContent += 'res_width  = (32 - res.width  % 32) % 32\n'
      vpyContent += 'res = core.std.AddBorders(clip=res, right=res_width, bottom=res_height)\n'

      vpyContent += `res = RIFE(res, scale=${config_json.RifeScaleValue},model=${model},ensemble=${EnsembleBool
      },multi=Fraction(${config_json.RifeMultiValue},res.fps)` + `, backend=device_vfi)\n`

      vpyContent += 'res = core.std.Crop(clip=res, right=res_width, bottom=res_height)\n'
    }
  }

  // 后置缩放(需要在此改进色彩控制)
  if (config_json.UseResize_AfterEnhance === true) {
    vpyContent
  += `res = core.resize.Bicubic(clip=res,width=${config_json.ResizeWidth_AfterEnhance
      },height=${config_json.ResizeHeight_AfterEnhance},matrix_s="709", format=vs.YUV420P16)\n`
  }
  else {
    vpyContent += 'res = core.resize.Bicubic(clip=res, matrix_s="709", format=vs.YUV420P16)\n'
  }

  vpyContent += `res = core.std.Crop(clip=res,left=${config_json.ReduceLeft_AfterEnhance
  }, right=${config_json.ReduceRight_AfterEnhance
  }, top=${config_json.ReduceOn_AfterEnhance
  }, bottom=${config_json.ReduceDown_AfterEnhance})\n`
  vpyContent += 'res.set_output()\n'
  return vpyContent
}

// 中断循环
let shouldStop = false

export function requestStop(): void {
  shouldStop = true
}

export async function preview(event, config_json): Promise<void> {
  // 工具路径
  const exeDir = path.dirname(process.execPath)
  const vipipePath = path.join(exeDir, 'package', 'VSPipe.exe')
  const videos = config_json.fileList
  if (videos?.length === 0) {
    event.sender.send('ffmpeg-finish')
    return
  }
  const video = videos[0]

  const baseName = path.basename(video, path.extname(video))
  const vpyPath = path.join(exeDir, 'vpyFiles', `${baseName}.vpy`)

  // ========== 生成 vpy 文件 ==========
  const vpyFile = generate_vpy(config_json, video)
  writeFileSync(vpyPath, vpyFile)

  let info: {
    width: string
    height: string
    frames: string
    fps: string
  } = {
    width: '未知',
    height: '未知',
    frames: '0',
    fps: '0',
  }
  await new Promise<void>((resolve, reject) => {
    const vspipeInfoProcess = spawn(vipipePath, ['--info', vpyPath])
    addProcess(vspipeInfoProcess)

    let vspipeOut = '' // 用于保存 stdout 内容
    // eslint-disable-next-line unused-imports/no-unused-vars
    let stderrOut = '' // 用于保存 stderr 内容

    vspipeInfoProcess.stdout.on('data', (data: Buffer) => {
      const str = iconv.decode(data, 'gbk')
      vspipeOut += str
      event.sender.send('ffmpeg-output', `${str}`)
    })

    vspipeInfoProcess.stderr.on('data', (data: Buffer) => {
      const str = iconv.decode(data, 'gbk')
      stderrOut += str
      event.sender.send('ffmpeg-output', `${str}`)
    })

    vspipeInfoProcess.on('close', (code) => {
      removeProcess(vspipeInfoProcess)
      event.sender.send('ffmpeg-output', `vspipe info 执行完毕，退出码: ${code}\n`)///////
      info = {
        width: vspipeOut.match(/Width:\s*(\d+)/)?.[1] || '未知',
        height: vspipeOut.match(/Height:\s*(\d+)/)?.[1] || '未知',
        frames: vspipeOut.match(/Frames:\s*(\d+)/)?.[1] || '0',
        fps: vspipeOut.match(/FPS:\s*([\d/]+)\s*\(([\d.]+) fps\)/)?.[2] || '0',
      }

      event.sender.send('preview-info', {
        width: info.width,
        height: info.height,
        frames: info.frames,
        fps: info.fps,
      })
      resolve()
    })

    vspipeInfoProcess.on('error', (err) => {
      event.sender.send('ffmpeg-output', `vspipe 执行出错: ${err.message}\n`)
      reject(err)
    })
  })
  event.sender.send('preview-vpyPath', vpyPath)
  event.sender.send('ffmpeg-finish')
}

export async function preview_frame(event: any, vpyfile: string, currentFrame: number): Promise<void> {
  const vspipePath = getExecPath().vspipe
  const ffmpegPath = getExecPath().ffmpeg

  // 构造一行命令
  const cmd = `"${vspipePath}" -c y4m --start ${currentFrame} --end ${currentFrame} "${vpyfile}" - | "${ffmpegPath}" -y -f yuv4mpegpipe -i - -frames:v 1 -vcodec png -f image2pipe -`

  const vspipePreviewProcess = spawn(cmd, { shell: true })
  addProcess(vspipePreviewProcess)

  const chunks: Buffer[] = []

  vspipePreviewProcess.stdout.on('data', (chunk) => {
    chunks.push(chunk)
  })

  vspipePreviewProcess.stderr.on('data', (data: Buffer) => {
    const str = iconv.decode(data, 'gbk')
    event.sender.send('ffmpeg-output', str)
  })

  vspipePreviewProcess.on('close', (code) => {
    removeProcess(vspipePreviewProcess)
    if (code === 0) {
      const buffer = Buffer.concat(chunks)
      const base64 = `data:image/png;base64,${buffer.toString('base64')}`
      event.sender.send('preview-image', base64)
    }
    else {
      event.sender.send('ffmpeg-output', `预览失败，退出码: ${code}`)
      event.sender.send('preview-image', null)
    }
    event.sender.send('ffmpeg-finish')
  })

  vspipePreviewProcess.on('error', (err) => {
    event.sender.send('ffmpeg-output', `命令执行出错: ${err.message}`)
  })
}

export async function RunCommand(event, config_json): Promise<void> {
  const vspipePath = getExecPath().vspipe
  const ffmpegPath = getExecPath().ffmpeg
  const ffprobePath = getExecPath().ffprobe

  const videos = config_json.fileList

  shouldStop = false

  for (const video of videos) {
    if (shouldStop) {
      event.sender.send('ffmpeg-output', `已终止循环:\n`)
      shouldStop = false
      break
    }
    try {
      // 生成唯一 vpy 路径
      const baseName = path.basename(video, path.extname(video))
      const vpyPath = getGenVpyPath(config_json, baseName)

      // ========== 1. 获取输入视频信息 ==========
      const ffprobeCommand = `"${ffprobePath}" -v error -show_streams -of json "${video}"`
      const { stdout: probeOut } = await exec(ffprobeCommand)
      const metadata = JSON.parse(probeOut)

      const allStreams = metadata.streams || []
      const videoStream = allStreams.find((s: any) => s.codec_type === 'video')
      const hasAudio = allStreams.some((s: any) => s.codec_type === 'audio')
      const hasSubtitle = allStreams.some((s: any) => s.codec_type === 'subtitle')

      if (videoStream) {
        const frameCount = videoStream.nb_frames || '未知'
        const frameRate = videoStream.avg_frame_rate || '未知'
        const resolution = `${videoStream.width}x${videoStream.height}`
        const audioText = hasAudio ? '是' : '否'
        const subtitleText = hasSubtitle ? '是' : '否' // 字幕信息

        event.sender.send('ffmpeg-output', `正在处理输入视频 ${video} 的信息:\n`)
        event.sender.send('ffmpeg-output', `帧数(输入): ${frameCount}\n`)
        event.sender.send('ffmpeg-output', `帧率(输入): ${frameRate}\n`)
        event.sender.send('ffmpeg-output', `分辨率(输入): ${resolution}\n`)
        event.sender.send('ffmpeg-output', `是否含有音频: ${audioText}\n`)
        event.sender.send('ffmpeg-output', `是否含有字幕: ${subtitleText}\n`)
      }
      // ========== 2. 生成 vpy 文件 ==========
      const vpyFile = generate_vpy(config_json, video)
      writeFileSync(vpyPath, vpyFile)

      // ========== 3. 获取输出视频信息 ==========
      let info: {
        width: string
        height: string
        frames: string
        fps: string
      } = {
        width: '未知',
        height: '未知',
        frames: '0',
        fps: '0',
      }
      await new Promise<void>((resolve, reject) => {
        const vspipeInfoProcess = spawn(vspipePath, ['--info', vpyPath])
        addProcess(vspipeInfoProcess)

        let vspipeOut = '' // 用于保存 stdout 内容
        // eslint-disable-next-line unused-imports/no-unused-vars
        let stderrOut = '' // 用于保存 stderr 内容

        vspipeInfoProcess.stdout.on('data', (data: Buffer) => {
          const str = iconv.decode(data, 'gbk')
          vspipeOut += str
          event.sender.send('ffmpeg-output', `${str}`)
        })

        vspipeInfoProcess.stderr.on('data', (data: Buffer) => {
          const str = iconv.decode(data, 'gbk')
          stderrOut += str
          event.sender.send('ffmpeg-output', `${str}`)
        })

        vspipeInfoProcess.on('close', (code) => {
          removeProcess(vspipeInfoProcess)
          event.sender.send('ffmpeg-output', `vspipe info 执行完毕，退出码: ${code}\n`)///////

          info = {
            width: vspipeOut.match(/Width:\s*(\d+)/)?.[1] || '未知',
            height: vspipeOut.match(/Height:\s*(\d+)/)?.[1] || '未知',
            frames: vspipeOut.match(/Frames:\s*(\d+)/)?.[1] || '0',
            fps: vspipeOut.match(/FPS:\s*([\d/]+)\s*\(([\d.]+) fps\)/)?.[2] || '0',
          }

          event.sender.send('ffmpeg-output', `======= 输出视频信息 =======\n`)
          event.sender.send('ffmpeg-output', `宽: ${info.width}\n`)
          event.sender.send('ffmpeg-output', `高: ${info.height}\n`)
          event.sender.send('ffmpeg-output', `帧数: ${info.frames}\n`)
          event.sender.send('ffmpeg-output', `帧率: ${info.fps}\n`)
          resolve()
        })

        vspipeInfoProcess.on('error', (err) => {
          event.sender.send('ffmpeg-output', `vspipe 执行出错: ${err.message}\n`)
          reject(err)
        })
      })

      // ========== 4. 构建渲染命令 ==========
      const cmd = generate_cmd(config_json, vspipePath, vpyPath, ffmpegPath, video, hasAudio, hasSubtitle)
      event.sender.send('ffmpeg-output', `Executing command: ${cmd}\n`)

      // ========== 5. 渲染并监听输出 ==========
      await new Promise<void>((resolve, reject) => {
        const renderProcess = spawn(cmd, { shell: true })
        addProcess(renderProcess)
        renderProcess.stdout.on('data', (data) => {
          event.sender.send('ffmpeg-output', data.toString())
        })

        renderProcess.stderr.on('data', (data) => {
          const str = data.toString()
          // eslint-disable-next-line regexp/no-misleading-capturing-group,regexp/no-super-linear-backtracking,regexp/optimal-quantifier-concatenation
          const regex = /frame=\s*(-?\d+)\s+fps=\s*([\d.]+).+time=\s*(-?[\d:.]+)\s+bitrate=\s*([\w/.-]+)/
          const match = str.match(regex)

          if (match) {
            const [_, frame, fps, time, bitrate] = match
            const totalFrames = Number.parseInt(info.frames || '0', 10)
            const renderedFrames = Number.parseInt(frame, 10)
            const currentFps = Number.parseFloat(fps)
            const remainingFrames = totalFrames - renderedFrames

            const estSeconds = remainingFrames / (currentFps || 1)
            const hours = Math.floor(estSeconds / 3600)
            const minutes = Math.floor((estSeconds % 3600) / 60)
            const seconds = Math.floor(estSeconds % 60)

            event.sender.send('ffmpeg-output', `[Progress_vspipe_ffmpeg]已渲染/总帧数: ${frame} / ${totalFrames} `
            + `速度(FPS): ${fps} `
            + `预计剩余时间：${hours}h ${minutes}min ${seconds}s `
            + `已渲染的时间长度: ${time} `
            + `比特率: ${bitrate}\n`)
          }
          else {
            event.sender.send('ffmpeg-output', str)
          }
        })

        renderProcess.on('close', () => {
          removeProcess(renderProcess)
          event.sender.send('ffmpeg-output', 'finish\n')

          resolve()
        })

        renderProcess.on('error', (err) => {
          reject(err)
        })
      })
    }
    catch (error) {
      const errMsg = error instanceof Error ? error.message : String(error)
      event.sender.send('ffmpeg-output', `处理视频 ${video} 时出错: ${errMsg}\n`)
    }
  }
  event.sender.send('ffmpeg-finish')
}
