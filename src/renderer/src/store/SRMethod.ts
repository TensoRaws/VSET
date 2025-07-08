const SRMethod_options = [
  {
    value: 'Real_cugan',
    label: 'Real_cugan',
  },
  {
    value: 'Real_esrgan',
    label: 'Real_esrgan',
  },
  // {
  //   value: 'ArtCNN',
  //   label: 'ArtCNN',
  // },
  {
    value: 'Waifu2x',
    label: 'Waifu2x',
  },
  // {
  //   value: 'SwinIR',
  //   label: 'SwinIR',
  // },

]

const VsmlrtTile_options = [
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
  }
]

const Inference_options = [
  {
    value: 'Cuda',
    label: 'Cuda',
  },
  {
    value: 'TensorRt',
    label: 'TensorRt',
  },
  {
    value: 'NCNN',
    label: 'NCNN',
  },
  {
    value: 'OV',
    label: 'OV',
  }
]

const RealcuganModel_options = [
  {
    value: 'pro-conservative-up2x',
    label: 'pro-conservative-up2x',
  },
  {
    value: 'pro-conservative-up3x',
    label: 'pro-conservative-up3x',
  },
  {
    value: 'pro-denoise3x-up2x',
    label: 'pro-denoise3x-up2x',
  },
  {
    value: 'pro-denoise3x-up3x',
    label: 'pro-denoise3x-up3x',
  },
  {
    value: 'pro-no-denoise3x-up2x',
    label: 'pro-no-denoise3x-up2x',
  },
  {
    value: 'pro-no-denoise3x-up3x',
    label: 'pro-no-denoise3x-up3x',
  },
  {
    value: 'up2x-latest-conservative',
    label: 'up2x-latest-conservative',
  },
  {
    value: 'up2x-latest-denoise1x',
    label: 'up2x-latest-denoise1x',
  },
  {
    value: 'up2x-latest-denoise2x',
    label: 'up2x-latest-denoise2x',
  },
  {
    value: 'up2x-latest-denoise3x',
    label: 'up2x-latest-denoise3x',
  },
  {
    value: 'up2x-latest-no-denoise',
    label: 'up2x-latest-no-denoise',
  },
  {
    value: 'up3x-latest-conservative',
    label: 'up3x-latest-conservative',
  },
  {
    value: 'up3x-latest-denoise3x',
    label: 'up3x-latest-denoise3x',
  },
  {
    value: 'up3x-latest-no-denoise',
    label: 'up3x-latest-no-denoise',
  },
  {
    value: 'up4x-latest-conservative',
    label: 'up4x-latest-conservative',
  },
  {
    value: 'up4x-latest-denoise3x',
    label: 'up4x-latest-denoise3x',
  },
  {
    value: 'up4x-latest-no-denoise',
    label: 'up4x-latest-no-denoise',
  },
]

const RealesrganModel_options = [
  {
    value: 'animevideov3',
    label: 'animevideov3',
  },
  {
    value: 'animevideo-xsx2',
    label: 'animevideo-xsx2',
  },
  {
    value: 'animevideo-xsx4',
    label: 'animevideo-xsx4',
  },
  {
    value: 'animejanaiV2L1',
    label: 'animejanaiV2L1',
  },
  {
    value: 'animejanaiV2L2',
    label: 'animejanaiV2L2',
  },
  {
    value: 'animejanaiV2L3',
    label: 'animejanaiV2L3',
  },
  {
    value: 'animejanaiV3_HD_L1',
    label: 'animejanaiV3_HD_L1',
  },
  {
    value: 'animejanaiV3_HD_L2',
    label: 'animejanaiV3_HD_L2',
  },
  {
    value: 'animejanaiV3_HD_L3',
    label: 'animejanaiV3_HD_L3',
  },
  {
    value: 'Ani4Kv2_G6i2_Compact',
    label: 'Ani4Kv2_G6i2_Compact',
  },
  {
    value: 'Ani4Kv2_G6i2_UltraCompact',
    label: 'Ani4Kv2_G6i2_UltraCompact',
  },
]



const RealesrganScale_options = [
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
]

// const ArtCNNModel_options = [
//   {
//     value: 'ArtCNN_C4F32',
//     label: 'ArtCNN_C4F32',
//   },
//   {
//     value: 'ArtCNN_C4F32_DS',
//     label: 'ArtCNN_C4F32_DS',
//   },
//   {
//     value: 'ArtCNN_C16F64',
//     label: 'ArtCNN_C16F64',
//   },
//   {
//     value: 'ArtCNN_C16F64_DS',
//     label: 'ArtCNN_C16F64_DS',
//   },
//   {
//     value: 'ArtCNN_C4F32_Chroma',
//     label: 'ArtCNN_C4F32_Chroma',
//   },
//   {
//     value: 'ArtCNN_C16F64_Chroma',
//     label: 'ArtCNN_C16F64_Chroma',
//   },
//   {
//     value: 'ArtCNN_R16F96',
//     label: 'ArtCNN_R16F96',
//   },
//   {
//     value: 'ArtCNN_R8F64',
//     label: 'ArtCNN_R8F64',
//   },
//   {
//     value: 'ArtCNN_R8F64_DS',
//     label: 'ArtCNN_R8F64_DS',
//   },
//   {
//     value: 'ArtCNN_R8F64_Chroma',
//     label: 'ArtCNN_R8F64_Chroma',
//   },
//   {
//     value: 'ArtCNN_C4F16',
//     label: 'ArtCNN_C4F16',
//   },
//   {
//     value: 'ArtCNN_C4F16_DS',
//     label: 'ArtCNN_C4F16_DS',
//   },
// ]

const Waifu2xModel_options = [
  { value: 'anime_style_art_rgb_noise0', label: 'anime_style_art_rgb_noise0' },
  { value: 'anime_style_art_rgb_noise1', label: 'anime_style_art_rgb_noise1' },
  { value: 'anime_style_art_rgb_noise2', label: 'anime_style_art_rgb_noise2' },
  { value: 'anime_style_art_rgb_noise3', label: 'anime_style_art_rgb_noise3' },
  { value: 'anime_style_art_rgb_scale2.0x', label: 'anime_style_art_rgb_scale2.0x' },

  { value: 'photo_noise0', label: 'photo_noise0' },
  { value: 'photo_noise1', label: 'photo_noise1' },
  { value: 'photo_noise2', label: 'photo_noise2' },
  { value: 'photo_noise3', label: 'photo_noise3' },
  { value: 'photo_scale2.0x', label: 'photo_scale2.0x' },


  { value: 'upconv_7_anime_style_art_rgb_noise0_scale2.0x', label: 'upconv_7_anime_style_art_rgb_noise0_scale2.0x' },
  { value: 'upconv_7_anime_style_art_rgb_noise1_scale2.0x', label: 'upconv_7_anime_style_art_rgb_noise1_scale2.0x' },
  { value: 'upconv_7_anime_style_art_rgb_noise2_scale2.0x', label: 'upconv_7_anime_style_art_rgb_noise2_scale2.0x' },
  { value: 'upconv_7_anime_style_art_rgb_noise3_scale2.0x', label: 'upconv_7_anime_style_art_rgb_noise3_scale2.0x' },
  { value: 'upconv_7_anime_style_art_rgb_scale2.0x', label: 'upconv_7_anime_style_art_rgb_scale2.0x' },

  { value: 'upconv_7_photo_noise0_scale2.0x', label: 'upconv_7_photo_noise0_scale2.0x' },
  { value: 'upconv_7_photo_noise1_scale2.0x', label: 'upconv_7_photo_noise1_scale2.0x' },
  { value: 'upconv_7_photo_noise2_scale2.0x', label: 'upconv_7_photo_noise2_scale2.0x' },
  { value: 'upconv_7_photo_noise3_scale2.0x', label: 'upconv_7_photo_noise3_scale2.0x' },
  { value: 'upconv_7_photo_scale2.0x_', label: 'upconv_7_photo_scale2.0x_' },


  { value: 'upresnet10_noise0_scale2.0x', label: 'upresnet10_noise0_scale2.0x' },
  { value: 'upresnet10_noise1_scale2.0x', label: 'upresnet10_noise1_scale2.0x' },
  { value: 'upresnet10_noise2_scale2.0x', label: 'upresnet10_noise2_scale2.0x' },
  { value: 'upresnet10_noise3_scale2.0x', label: 'upresnet10_noise3_scale2.0x' },
  { value: 'upresnet10_scale2.0x', label: 'upresnet10_scale2.0x' },


  { value: 'cunet_noise0', label: 'cunet_noise0' },
  { value: 'cunet_noise1', label: 'cunet_noise1' },
  { value: 'cunet_noise2', label: 'cunet_noise2' },
  { value: 'cunet_noise3', label: 'cunet_noise3' },
  { value: 'cunet_noise0_scale2.0x', label: 'cunet_noise0_scale2.0x' },
  { value: 'cunet_noise1_scale2.0x', label: 'cunet_noise1_scale2.0x' },
  { value: 'cunet_noise2_scale2.0x', label: 'cunet_noise2_scale2.0x' },
  { value: 'cunet_noise3_scale2.0x', label: 'cunet_noise3_scale2.0x' },
  { value: 'cunet_scale2.0x', label: 'cunet_scale2.0x' },

  { value: 'swin_unet_art_noise0', label: 'swin_unet_art_noise0' },
  { value: 'swin_unet_art_noise0_scale2x', label: 'swin_unet_art_noise0_scale2x' },
  { value: 'swin_unet_art_noise0_scale4x', label: 'swin_unet_art_noise0_scale4x' },
  { value: 'swin_unet_art_noise1', label: 'swin_unet_art_noise1' },
  { value: 'swin_unet_art_noise1_scale2x', label: 'swin_unet_art_noise1_scale2x' },
  { value: 'swin_unet_art_noise1_scale4x', label: 'swin_unet_art_noise1_scale4x' },
  { value: 'swin_unet_art_noise2', label: 'swin_unet_art_noise2' },
  { value: 'swin_unet_art_noise2_scale2x', label: 'swin_unet_art_noise2_scale2x' },
  { value: 'swin_unet_art_noise2_scale4x', label: 'swin_unet_art_noise2_scale4x' },
  { value: 'swin_unet_art_noise3', label: 'swin_unet_art_noise3' },
  { value: 'swin_unet_art_noise3_scale2x', label: 'swin_unet_art_noise3_scale2x' },
  { value: 'swin_unet_art_noise3_scale4x', label: 'swin_unet_art_noise3_scale4x' },
  { value: 'swin_unet_art_scale2x', label: 'swin_unet_art_scale2x' },
  { value: 'swin_unet_art_scale4x', label: 'swin_unet_art_scale4x' },

  { value: 'swin_unet_art_scan_noise0_scale4x', label: 'swin_unet_art_scan_noise0_scale4x' },
  { value: 'swin_unet_art_scan_noise1_scale4x', label: 'swin_unet_art_scan_noise1_scale4x' },
  { value: 'swin_unet_art_scan_noise2_scale4x', label: 'swin_unet_art_scan_noise2_scale4x' },
  { value: 'swin_unet_art_scan_noise3_scale4x', label: 'swin_unet_art_scan_noise3_scale4x' },
  { value: 'swin_unet_art_scan_scale4x', label: 'swin_unet_art_scan_scale4x' },

  { value: 'swin_unet_photo_noise0_scale4x', label: 'swin_unet_photo_noise0_scale4x' },
  { value: 'swin_unet_photo_noise1_scale4x', label: 'swin_unet_photo_noise1_scale4x' },
  { value: 'swin_unet_photo_noise2_scale4x', label: 'swin_unet_photo_noise2_scale4x' },
  { value: 'swin_unet_photo_noise3_scale4x', label: 'swin_unet_photo_noise3_scale4x' },
  { value: 'swin_unet_photo_scale4x', label: 'swin_unet_photo_scale4x' },

  { value: 'swin_unet_photo_v2_noise0_scale4x', label: 'swin_unet_photo_v2_noise0_scale4x' },
  { value: 'swin_unet_photo_v2_noise1_scale4x', label: 'swin_unet_photo_v2_noise1_scale4x' },
  { value: 'swin_unet_photo_v2_noise2_scale4x', label: 'swin_unet_photo_v2_noise2_scale4x' },
  { value: 'swin_unet_photo_v2_noise3_scale4x', label: 'swin_unet_photo_v2_noise3_scale4x' },
  { value: 'swin_unet_photo_v2_scale4x', label: 'swin_unet_photo_v2_scale4x' },

]

const SwinIRModel_options = [
  { value: 'lightweightSR_DIV2K_s64w8_SwinIR_S_x2', label: 'lightweightSR_DIV2K_s64w8_SwinIR_S_x2' },
  { value: 'lightweightSR_DIV2K_s64w8_SwinIR_S_x3', label: 'lightweightSR_DIV2K_s64w8_SwinIR_S_x3' },
  { value: 'lightweightSR_DIV2K_s64w8_SwinIR_S_x4', label: 'lightweightSR_DIV2K_s64w8_SwinIR_S_x4' },
  { value: 'realSR_BSRGAN_DFOWMFC_s64w8_SwinIR_L_x4_GAN', label: 'realSR_BSRGAN_DFOWMFC_s64w8_SwinIR_L_x4_GAN' },
  { value: 'realSR_BSRGAN_DFOWMFC_s64w8_SwinIR_L_x4_PSNR', label: 'realSR_BSRGAN_DFOWMFC_s64w8_SwinIR_L_x4_PSNR' },
  { value: 'classicalSR_DF2K_s64w8_SwinIR_M_x2', label: 'classicalSR_DF2K_s64w8_SwinIR_M_x2' },
  { value: 'classicalSR_DF2K_s64w8_SwinIR_M_x3', label: 'classicalSR_DF2K_s64w8_SwinIR_M_x3' },
  { value: 'classicalSR_DF2K_s64w8_SwinIR_M_x4', label: 'classicalSR_DF2K_s64w8_SwinIR_M_x4' },
  { value: 'classicalSR_DF2K_s64w8_SwinIR_M_x8', label: 'classicalSR_DF2K_s64w8_SwinIR_M_x8' },
  { value: 'realSR_BSRGAN_DFO_s64w8_SwinIR_M_x2_GAN', label: 'realSR_BSRGAN_DFO_s64w8_SwinIR_M_x2_GAN' },
  { value: 'realSR_BSRGAN_DFO_s64w8_SwinIR_M_x2_PSNR', label: 'realSR_BSRGAN_DFO_s64w8_SwinIR_M_x2_PSNR' },
  { value: 'realSR_BSRGAN_DFO_s64w8_SwinIR_M_x4_GAN', label: 'realSR_BSRGAN_DFO_s64w8_SwinIR_M_x4_GAN' },
  { value: 'realSR_BSRGAN_DFO_s64w8_SwinIR_M_x4_PSNR', label: 'realSR_BSRGAN_DFO_s64w8_SwinIR_M_x4_PSNR' },
  // { value: 'grayDN_DFWB_s128w8_SwinIR_M_noise15', label: 'grayDN_DFWB_s128w8_SwinIR_M_noise15' },
  // { value: 'grayDN_DFWB_s128w8_SwinIR_M_noise25', label: 'grayDN_DFWB_s128w8_SwinIR_M_noise25' },
  // { value: 'grayDN_DFWB_s128w8_SwinIR_M_noise50', label: 'grayDN_DFWB_s128w8_SwinIR_M_noise50' },
  { value: 'colorDN_DFWB_s128w8_SwinIR_M_noise15', label: 'colorDN_DFWB_s128w8_SwinIR_M_noise15' },
  { value: 'colorDN_DFWB_s128w8_SwinIR_M_noise25', label: 'colorDN_DFWB_s128w8_SwinIR_M_noise25' },
  { value: 'colorDN_DFWB_s128w8_SwinIR_M_noise50', label: 'colorDN_DFWB_s128w8_SwinIR_M_noise50' },
  { value: 'CAR_DFWB_s126w7_SwinIR_M_jpeg10', label: 'CAR_DFWB_s126w7_SwinIR_M_jpeg10' },
  { value: 'CAR_DFWB_s126w7_SwinIR_M_jpeg20', label: 'CAR_DFWB_s126w7_SwinIR_M_jpeg20' },
  { value: 'CAR_DFWB_s126w7_SwinIR_M_jpeg30', label: 'CAR_DFWB_s126w7_SwinIR_M_jpeg30' },
  { value: 'CAR_DFWB_s126w7_SwinIR_M_jpeg40', label: 'CAR_DFWB_s126w7_SwinIR_M_jpeg40' },
  { value: 'colorCAR_DFWB_s126w7_SwinIR_M_jpeg10', label: 'colorCAR_DFWB_s126w7_SwinIR_M_jpeg10' },
  { value: 'colorCAR_DFWB_s126w7_SwinIR_M_jpeg20', label: 'colorCAR_DFWB_s126w7_SwinIR_M_jpeg20' },
  { value: 'colorCAR_DFWB_s126w7_SwinIR_M_jpeg30', label: 'colorCAR_DFWB_s126w7_SwinIR_M_jpeg30' },
  { value: 'colorCAR_DFWB_s126w7_SwinIR_M_jpeg40', label: 'colorCAR_DFWB_s126w7_SwinIR_M_jpeg40' }
]



export { SRMethod_options, VsmlrtTile_options, Inference_options, RealcuganModel_options,RealesrganModel_options,
    RealesrganScale_options, SwinIRModel_options, Waifu2xModel_options};
