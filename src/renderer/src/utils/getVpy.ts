import useFilterconfigStore from '@renderer/store/FilterStore'
import useSrsettingconfigStore from '@renderer/store/SrSettingsStore'
import useVfisettingconfigStore from '@renderer/store/VfiSettingsStore'

import { storeToRefs } from 'pinia'

// ✅ 生成 JSON 数据的函数
export function buildVpyContent(): string {
  // SR
  const SrSettingStore = useSrsettingconfigStore()
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
    Waifu2xInferenceValue,
    Waifu2xModelValue,
    Waifu2xTileValue,
    SR_ExtraModelValue,
    SR_ExtraModelInferenceValue,
    Sr_numstreams,
    Sr_cudagraph,
  } = storeToRefs(SrSettingStore)

  // VFI
  const VfiSettingStore = useVfisettingconfigStore()
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

  // Filter
  const FilterConfigStore = useFilterconfigStore()
  const {
    UseResize_BeforeEnhance,
    UseResize_AfterEnhance,
    ResizeWidth_BeforeEnhance,
    ResizeHeight_BeforeEnhance,
    ResizeWidth_AfterEnhance,
    ResizeHeight_AfterEnhance,
    ReduceLeft_BeforeEnhance,
    ReduceRight_BeforeEnhance,
    ReduceOn_BeforeEnhance,
    ReduceDown_BeforeEnhance,
    ReduceLeft_AfterEnhance,
    ReduceRight_AfterEnhance,
    ReduceOn_AfterEnhance,
    ReduceDown_AfterEnhance,
  } = storeToRefs(FilterConfigStore)

  // 开始生成 vpy 内容
  let vpyContent = `r"""
Auto generated VapourSynth script by VSET
DON'T edit this file manually if you don't know what you are doing

These magic strings will be replaced in final script:
    - Video Path: __VIDEO_PATH__
    - Extra Model Path: __EXTRA_MODEL_PATH__

GitHub: https://github.com/TensoRaws/VSET
"""
\n
`

  vpyContent += 'import vapoursynth as vs\n'
  vpyContent += 'core = vs.core\n'
  vpyContent += `res = core.lsmas.LWLibavSource(r"__VIDEO_PATH__")\n`
  vpyContent += 'from vsmlrt import CUGAN,RealESRGAN,Waifu2x,RIFE,Backend\n'
  vpyContent += 'import vsmlrt\n'

  // 前置缩放(需要在此改进色彩控制)
  if (UseResize_BeforeEnhance.value === true) {
    vpyContent += `res = core.resize.Bicubic(clip=res,width=${ResizeWidth_BeforeEnhance.value},height=${ResizeHeight_BeforeEnhance.value},format=vs.YUV420P16)\n`
  }
  else {
    vpyContent += 'res = core.resize.Bicubic(clip=res,format=vs.YUV420P16)\n'
  }

  vpyContent += `res = core.std.Crop(clip=res,left=${ReduceLeft_BeforeEnhance.value}, right=${ReduceRight_BeforeEnhance.value}, top=${ReduceOn_BeforeEnhance.value}, bottom=${ReduceDown_BeforeEnhance.value})\n`

  // 超分
  if (useSR.value === true) {
    vpyContent += 'res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n'
    vpyContent += 'res=core.fmtc.bitdepth(res, bits=32)\n'

    // 超分设备
    if (SRMethodValue.value === 'Real_cugan') {
      if (RealcuganInferenceValue.value === 'Cuda') {
        vpyContent += 'device_sr=Backend.ORT_CUDA()\n'
      }
      if (RealcuganInferenceValue.value === 'TensorRt') {
        vpyContent += 'device_sr=Backend.TRT()\n'
        vpyContent += `device_sr.use_cuda_graph = ${String(Sr_cudagraph.value)[0].toUpperCase() + String(Sr_cudagraph.value).slice(1)}\n`
      }
      if (RealcuganInferenceValue.value === 'NCNN') {
        vpyContent += 'device_sr=Backend.NCNN_VK()\n'
      }
      if (RealcuganInferenceValue.value === 'DML') {
        vpyContent += 'device_sr=Backend.ORT_DML()\n'
      }
      if (RealcuganInferenceValue.value === 'MIGX') {
        vpyContent += 'device_sr=Backend.MIGX()\n'
      }
    }
    if (SRMethodValue.value === 'Real_esrgan') {
      if (RealesrganInferenceValue.value === 'Cuda') {
        vpyContent += 'device_sr=Backend.ORT_CUDA()\n'
      }
      if (RealesrganInferenceValue.value === 'TensorRt') {
        vpyContent += 'device_sr=Backend.TRT()\n'
        vpyContent += `device_sr.use_cuda_graph = ${String(Sr_cudagraph.value)[0].toUpperCase() + String(Sr_cudagraph.value).slice(1)}\n`
      }
      if (RealesrganInferenceValue.value === 'TensorRt_RTX') {
        vpyContent += 'device_sr=Backend.TRT_RTX()\n'
      }
      if (RealesrganInferenceValue.value === 'NCNN') {
        vpyContent += 'device_sr=Backend.NCNN_VK()\n'
      }
      if (RealesrganInferenceValue.value === 'DML') {
        vpyContent += 'device_sr=Backend.ORT_DML()\n'
      }
      if (RealesrganInferenceValue.value === 'MIGX') {
        vpyContent += 'device_sr=Backend.MIGX()\n'
      }
    }
    if (SRMethodValue.value === 'Waifu2x') {
      if (Waifu2xInferenceValue.value === 'Cuda') {
        vpyContent += 'device_sr=Backend.ORT_CUDA()\n'
      }
      if (Waifu2xInferenceValue.value === 'TensorRt') {
        vpyContent += 'device_sr=Backend.TRT()\n'
        vpyContent += `device_sr.use_cuda_graph = ${String(Sr_cudagraph.value)[0].toUpperCase() + String(Sr_cudagraph.value).slice(1)}\n`
      }
      if (Waifu2xInferenceValue.value === 'TensorRt_RTX') {
        vpyContent += 'device_sr=Backend.TRT_RTX()\n'
      }
      if (Waifu2xInferenceValue.value === 'NCNN') {
        vpyContent += 'device_sr=Backend.NCNN_VK()\n'
      }
      if (Waifu2xInferenceValue.value === 'DML') {
        vpyContent += 'device_sr=Backend.ORT_DML()\n'
      }
      if (Waifu2xInferenceValue.value === 'MIGX') {
        vpyContent += 'device_sr=Backend.MIGX()\n'
      }
    }
    if (SRMethodValue.value === 'SR_ExtraModel') {
      if (SR_ExtraModelInferenceValue.value === 'Cuda') {
        vpyContent += 'device_sr=Backend.ORT_CUDA()\n'
      }
      if (SR_ExtraModelInferenceValue.value === 'TensorRt') {
        vpyContent += 'device_sr=Backend.TRT()\n'
        vpyContent += `device_sr.use_cuda_graph = ${String(Sr_cudagraph.value)[0].toUpperCase() + String(Sr_cudagraph.value).slice(1)}\n`
      }
      if (SR_ExtraModelInferenceValue.value === 'NCNN') {
        vpyContent += 'device_sr=Backend.NCNN_VK()\n'
      }
      if (SR_ExtraModelInferenceValue.value === 'DML') {
        vpyContent += 'device_sr=Backend.ORT_DML()\n'
      }
      if (SR_ExtraModelInferenceValue.value === 'MIGX') {
        vpyContent += 'device_sr=Backend.MIGX()\n'
      }
    }

    vpyContent += 'device_sr.device_id=0\n'
    vpyContent += 'device_sr.fp16=True\n'
    vpyContent += `device_sr.num_streams=${Sr_numstreams.value}\n`

    if (SRMethodValue.value === 'Real_cugan') {
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
      const [noise, scale, version] = model_switch[RealcuganModelValue.value] || [0, 2, 2]
      vpyContent += `res = CUGAN(res, noise=${noise}, scale=${scale}, tiles=${RealcuganTileValue.value}, version=${version}, alpha=${RealcuganAlphaValue.value}, backend=device_sr)\n`
    }

    if (SRMethodValue.value === 'Real_esrgan') {
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
      const model = model_switch[RealesrganModelValue.value] || 0
      vpyContent += `res = RealESRGAN(res, scale=${RealesrganScaleValue.value},tiles=${
        RealesrganTileValue.value},model=${model}, backend=device_sr)\n`
    }

    if (SRMethodValue.value === 'Waifu2x') {
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
      const [model, noise, scale] = model_switch[Waifu2xModelValue.value] || [1, 0, 1]
      vpyContent += `res = Waifu2x(res, noise=${noise}, scale=${scale}, tiles=${Waifu2xTileValue.value}, model=${model}, backend=device_sr)\n`
    }

    if (SRMethodValue.value === 'SR_ExtraModel') {
      const model_switch = {
        AniSD_DC_SPAN_x2: 'AniSD_DC_SPAN_x2.onnx',
      }

      const model = `__EXTRA_MODEL_PATH__/${model_switch[SR_ExtraModelValue.value] || 'AniSD_DC_SPAN_x2.onnx'}`

      vpyContent += `res = vsmlrt.inference(res, network_path=r"${model}", backend=device_sr)\n`
    }
  }

  // 补帧
  if (useVfi.value === true) {
    vpyContent += 'res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n'
    vpyContent += 'res=core.fmtc.bitdepth(res, bits=32)\n'

    if (VfiMethodValue.value === 'Rife') {
      if (RifeInferenceValue.value === 'Cuda') {
        vpyContent += 'device_vfi=Backend.ORT_CUDA()\n'
      }
      if (RifeInferenceValue.value === 'TensorRt') {
        vpyContent += 'device_vfi=Backend.TRT()\n'
        vpyContent += `device_vfi.use_cuda_graph = ${String(Vfi_cudagraph.value)[0].toUpperCase() + String(Vfi_cudagraph.value).slice(1)}\n`
      }
      if (RifeInferenceValue.value === 'NCNN') {
        vpyContent += 'device_vfi=Backend.NCNN_VK()\n'
      }
      if (RifeInferenceValue.value === 'DML') {
        vpyContent += 'device_vfi=Backend.ORT_DML()\n'
      }
      if (RifeInferenceValue.value === 'MIGX') {
        vpyContent += 'device_vfi=Backend.MIGX()\n'
      }
    }

    vpyContent += 'device_vfi.device_id=0\n'
    vpyContent += 'device_vfi.fp16=True\n'
    vpyContent += `device_vfi.num_streams=${Vfi_numstreams.value}\n`
    vpyContent += 'from fractions import Fraction\n'

    if (VfiMethodValue.value === 'Rife') {
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
      const model = model_switch[RifeModelValue.value] || 40
      const EnsembleBool = RifeEnsembleValue.value ? 'True' : 'False'
      vpyContent += `res = core.misc.SCDetect(res,threshold=${RifeDetectionValue.value})\n`
      let tilesize_requirement = 32
      if (RifeModelValue.value === 'v4_25_lite') {
        tilesize_requirement = 128
      }
      if (RifeModelValue.value === 'v4_25_heavy' || RifeModelValue.value === 'v4_26_heavy'
        || RifeModelValue.value === 'v4_26') {
        tilesize_requirement = 64
      }
      vpyContent += `Borders=${tilesize_requirement} / ${RifeScaleValue.value}\n`
      vpyContent += 'res_height = (Borders - res.height % Borders) \n'
      vpyContent += 'res_width  = (Borders - res.width  % Borders) \n'
      vpyContent += 'res = core.std.AddBorders(clip=res, right=res_width, bottom=res_height)\n'

      vpyContent += `res = RIFE(res, scale=${RifeScaleValue.value},model=${model},ensemble=${EnsembleBool
      },multi=Fraction(${RifeMultiValue.value},res.fps)` + `, backend=device_vfi)\n`

      vpyContent += 'res = core.std.Crop(clip=res, right=res_width, bottom=res_height)\n'
    }
  }

  // 后置缩放(需要在此改进色彩控制)
  if (UseResize_AfterEnhance.value === true) {
    vpyContent
            += `res = core.resize.Bicubic(clip=res,width=${ResizeWidth_AfterEnhance.value
      },height=${ResizeHeight_AfterEnhance.value},matrix_s="709", format=vs.YUV420P16)\n`
  }
  else {
    vpyContent += 'res = core.resize.Bicubic(clip=res, matrix_s="709", format=vs.YUV420P16)\n'
  }

  vpyContent += `res = core.std.Crop(clip=res,left=${ReduceLeft_AfterEnhance.value
  }, right=${ReduceRight_AfterEnhance.value
  }, top=${ReduceOn_AfterEnhance.value
  }, bottom=${ReduceDown_AfterEnhance.value})\n`
  vpyContent += 'res.set_output()\n'
  return vpyContent
}
