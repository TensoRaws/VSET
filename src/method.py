from PyQt5.QtCore import QObject


class mlrt_setting(QObject):
    def __init__(self, device, cm_numstream, cm_gragh, tm_numstream,trt_output, trt_force16, trt_graph, trt_cublas, trt_heuristic,
                 om_numstream,nm_numstream, half, gpu_id):
        self.device = device

        self.cm_numstream = cm_numstream
        self.cm_gragh = cm_gragh

        self.tm_numstream = tm_numstream
        self.tm_trt_output = trt_output
        self.tm_trt_force16 = trt_force16
        self.tm_trt_graph = trt_graph
        self.tm_trt_cublas = trt_cublas
        self.tm_trt_heuristic = trt_heuristic

        self.om_numstream=om_numstream
        self.nm_numstream=nm_numstream

        self.half = half
        self.gpu_id = gpu_id

    def mlrt_sr_device(self):
        device_vpy = []
        device_vpy.append('from vsmlrt import CUGAN,RealESRGAN,Waifu2x,RIFE,Backend\n')
        if self.device == 'CUDA':
            device_vpy.append('device_sr=Backend.ORT_CUDA()\n')
            device_vpy.append('device_sr.num_streams=' + str(self.cm_numstream) + '\n')
            device_vpy.append('device_sr.use_cuda_graph=' + str(self.cm_gragh) + '\n')

        elif self.device == 'TRT':
            device_vpy.append('device_sr=Backend.TRT()\n')
            device_vpy.append('device_sr.num_streams=' + str(self.tm_numstream) + '\n')
            device_vpy.append('device_sr.use_cuda_graph=' + str(self.tm_trt_graph) + '\n')
            if str(self.tm_trt_output)=='fp32':
                device_vpy.append('device_sr.output_format=0\n')
            elif str(self.tm_trt_output)=='fp16':
                device_vpy.append('device_sr.output_format=1\n')
            else:
                device_vpy.append('device_sr.output_format=0\n')
            device_vpy.append('device_sr.force_fp16=' + str(self.tm_trt_force16) + '\n')
            device_vpy.append('device_sr.use_cublas=' + str(self.tm_trt_cublas) + '\n')
            device_vpy.append('device_sr.heuristic=' + str(self.tm_trt_heuristic) + '\n')

        elif self.device == 'OV':
            device_vpy.append('device_sr=Backend.OV_GPU()\n')
            device_vpy.append('device_sr.num_streams=' + str(self.om_numstream) + '\n')

        elif self.device == 'NCNN':
            device_vpy.append('device_sr=Backend.NCNN_VK()\n')
            device_vpy.append('device_sr.num_streams=' + str(self.nm_numstream) + '\n')

        device_vpy.append('device_sr.device_id=' + str(self.gpu_id) + '\n')
        device_vpy.append('device_sr.fp16=' + str(self.half) + '\n')
        return device_vpy

    def mlrt_vfi_device(self):
        device_vpy = []
        device_vpy.append('from vsmlrt import CUGAN,RealESRGAN,Waifu2x,RIFE,Backend\n')
        if self.device == 'CUDA':
            device_vpy.append('device_vfi=Backend.ORT_CUDA()\n')
            device_vpy.append('device_vfi.num_streams=' + str(self.cm_numstream) + '\n')
            device_vpy.append('device_vfi.use_cuda_graph=' + str(self.cm_gragh) + '\n')

        elif self.device == 'TRT':
            device_vpy.append('device_vfi=Backend.TRT()\n')
            device_vpy.append('device_vfi.num_streams=' + str(self.tm_numstream) + '\n')
            device_vpy.append('device_vfi.use_cuda_graph=' + str(self.tm_trt_graph) + '\n')
            if str(self.tm_trt_output) == 'fp32':
                device_vpy.append('device_vfi.output_format=0\n')
            elif str(self.tm_trt_output) == 'fp16':
                device_vpy.append('device_vfi.output_format=1\n')
            else:
                device_vpy.append('device_vfi.output_format=0\n')
            device_vpy.append('device_vfi.force_fp16=' + str(self.tm_trt_force16) + '\n')
            device_vpy.append('device_vfi.use_cublas=' + str(self.tm_trt_cublas) + '\n')
            device_vpy.append('device_vfi.heuristic=' + str(self.tm_trt_heuristic) + '\n')

        elif self.device == 'OV':
            device_vpy.append('device_vfi=Backend.OV_GPU()\n')
            device_vpy.append('device_vfi.num_streams=' + str(self.om_numstream) + '\n')

        elif self.device == 'NCNN':
            device_vpy.append('device_vfi=Backend.NCNN_VK()\n')
            device_vpy.append('device_vfi.num_streams=' + str(self.nm_numstream) + '\n')

        device_vpy.append('device_vfi.device_id=' + str(self.gpu_id) + '\n')
        device_vpy.append('device_vfi.fp16=' + str(self.half) + '\n')
        return device_vpy


class cugan_ml_setting(QObject):
    def __init__(self, mlrt_set, model, tile, alpha):
        self.mlrt_set = mlrt_set
        self.model = model
        self.tile = tile
        self.alpha = alpha

    def sr_vpy(self):
        model_switch = {
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
            'up4x-latest-no-denoise': [-1, 4, 1]
        }
        noise, scale, version = model_switch[self.model] \
            if self.model in model_switch else [0, 2, 2]

        cugan_vpy = []
        for str_ in self.mlrt_set.mlrt_sr_device():
            cugan_vpy.append(str_)
        cugan_vpy.append('res = CUGAN(res, noise=' + str(noise) + ', scale=' + str(scale) + ', tiles=' + str(
            self.tile) + ',version=' + str(version) + ',alpha=' + str(
            self.alpha) + ', backend=device_sr)\n')
        return cugan_vpy


class esrgan_ml_setting(QObject):
    def __init__(self, mlrt_set, model, tile, scale):
        self.mlrt_set = mlrt_set
        self.model = model
        self.tile = tile
        self.scale = scale

    def sr_vpy(self):
        model_switch = {
            'animevideov3': 0,
            'animevideo-xsx2': 1,
            'animevideo-xsx4': 2
        }
        model = model_switch[self.model] \
            if self.model in model_switch else 0

        esrgan_vpy = []
        for str_ in self.mlrt_set.mlrt_sr_device():
            esrgan_vpy.append(str_)
        esrgan_vpy.append('res = RealESRGAN(res, scale=' + str(self.scale) + ',tiles=' + str(
            self.tile) + ',model=' + str(model) + ', backend=device_sr)\n')
        return esrgan_vpy


class waifu2x_ml_setting(QObject):
    def __init__(self, mlrt_set, model, tile):
        self.mlrt_set = mlrt_set
        self.model = model
        self.tile = tile

    def sr_vpy(self):
        model_switch = {
            'anime_style_art_rgb_noise0': [0, 1, 1],
            'anime_style_art_rgb_noise1': [1, 1, 1],
            'anime_style_art_rgb_noise2': [2, 1, 1],
            'anime_style_art_rgb_noise3': [3, 1, 1],
            'anime_style_art_rgb_scale2.0x': [-1, 2, 1],

            'cunet_noise0': [0, 1, 6],
            'cunet_noise0_scale2.0x': [0, 2, 6],
            'cunet_noise1': [1, 1, 6],
            'cunet_noise1_scale2.0x': [1, 2, 6],
            'cunet_noise2': [2, 1, 6],
            'cunet_noise2_scale2.0x': [2, 2, 6],
            'cunet_noise3': [3, 1, 6],
            'cunet_noise3_scale2.0x': [3, 2, 6],
            'cunet_scale2.0x': [-1, 2, 6],

            'photo_noise0': [0, 1, 2],
            'photo_noise1': [1, 1, 2],
            'photo_noise2': [2, 1, 2],
            'photo_noise3': [3, 1, 2],
            'photo_scale2.0x': [-1, 2, 2],

            'upconv_7_anime_noise0_scale2.0x': [0, 2, 3],
            'upconv_7_anime_noise1_scale2.0x': [1, 2, 3],
            'upconv_7_anime_noise2_scale2.0x': [2, 2, 3],
            'upconv_7_anime_noise3_scale2.0x': [3, 2, 3],
            'upconv_7_anime_scale2.0x': [-1, 2, 3],

            'upconv_7_photo_noise0_scale2.0x': [0, 2, 4],
            'upconv_7_photo_noise1_scale2.0x': [1, 2, 4],
            'upconv_7_photo_noise2_scale2.0x': [2, 2, 4],
            'upconv_7_photo_noise3_scale2.0x': [3, 2, 4],
            'upconv_7_photo_scale2.0x': [-1, 2, 4],

            'upresnet10_noise0_scale2.0x': [0, 2, 5],
            'upresnet10_noise1_scale2.0x': [1, 2, 5],
            'upresnet10_noise2_scale2.0x': [2, 2, 5],
            'upresnet10_noise3_scale2.0x': [3, 2, 5],
            'upresnet10_scale2.0x': [-1, 2, 5],

            'noise0': [0, 1, 7],
            'noise0_scale2x': [0, 2, 7],
            'noise0_scale4x': [0, 4, 7],
            'noise1': [1, 1, 7],
            'noise1_scale2x': [1, 2, 7],
            'noise1_scale4x': [1, 4, 7],
            'noise2': [2, 1, 7],
            'noise2_scale2x': [2, 2, 7],
            'noise2_scale4x': [2, 4, 7],
            'noise3': [3, 1, 7],
            'noise3_scale2x': [3, 2, 7],
            'noise3_scale4x': [3, 4, 7],
            'scale2x': [-1, 2, 7],
            'scale4x': [-1, 4, 7]
        }
        noise, scale, model = model_switch[self.model] \
            if self.model in model_switch else [1, 1, 1]

        waifu2x_vpy = []
        for str_ in self.mlrt_set.mlrt_sr_device():
            waifu2x_vpy.append(str_)
        waifu2x_vpy.append('res = Waifu2x(res, noise=' + str(noise) + ',scale=' + str(scale) + ',tiles=' + str(
            self.tile) + ',model=' + str(model) + ', backend=device_sr)\n')
        return waifu2x_vpy


class vsrpp_setting(QObject):
    def __init__(self, model, length, half, gpu_id):
        self.model = model
        self.length = length
        self.half = half
        self.gpu_id = gpu_id

    def sr_vpy(self):
        model_switch = {
            'reds4': 0,
            'vimeo90k_bi': 1,
            'vimeo90k_bd': 2,
            'ntire_vsr': 3,
            'ntire_decompress_track1': 4,
            'ntire_decompress_track2': 5,
            'ntire_decompress_track3': 6,
            'deblur_dvd': 7,
            'deblur_gopro': 8,
            'denoise': 9
        }
        model = model_switch[self.model] \
            if self.model in model_switch else 6
        vsrpp_vpy = []
        vsrpp_vpy.append('from vsbasicvsrpp import basicvsrpp\n')
        vsrpp_vpy.append('res = basicvsrpp(res,model=' + str(model) + ',length=' + str(
            self.length) + ',device_index=' + str(self.gpu_id) + ')\n')

        return vsrpp_vpy

class swinir_setting(QObject):
    def __init__(self, model, tile, half, gpu_id):
        self.model = model
        self.tile = tile
        self.half = half
        self.gpu_id = gpu_id

    def sr_vpy(self):
        model_switch = {
            'SwinIR-S_x2': 0,
            'SwinIR-S_x3': 1,
            'SwinIR-S_x4': 2,
            'SwinIR-L_x4_GAN': 3,
            '2x_Anime_SwinIR_v1': 4
        }
        model = model_switch[self.model] \
            if self.model in model_switch else 0
        vpy_ = []
        vpy_.append('from vsswinir import swinir\n')

        vpy_.append('res = swinir(res,model=' + str(model) + ',tile_w=' + str(
            self.tile) + ', num_streams=1' + ',device_index=' + str(self.gpu_id) + ')\n')
        return vpy_


class esrgan_setting(QObject):
    def __init__(self, model, tile, half, gpu_id):
        self.model = model
        self.tile = tile
        self.half = half
        self.gpu_id = gpu_id

    def sr_vpy(self):
        model_switch = {
            'SRx4_DF2KOST_official': 0,
            'x2plus': 1,
            'x4plus': 2,
            'x4plus_anime_6B': 3,
            'animevideov3': 4
        }
        model = model_switch[self.model] \
            if self.model in model_switch else 0
        vpy_ = []
        vpy_.append('from vsrealesrgan import RealESRGAN\n')

        vpy_.append('res = RealESRGAN(res,model=' + str(model) + ',num_streams=1' + ',tile_w=' + str(
            self.tile) + ',device_index=' + str(self.gpu_id) + ')\n')
        return vpy_


class codeformer_setting(QObject):
    def __init__(self, model, scale, weight, ocf,gpu_id):
        self.model = model
        self.scale = scale
        self.weight = weight
        self.ocf = ocf
        self.gpu_id = gpu_id

    def sr_vpy(self):
        model_switch = {
            'retinaface_resnet50': 0,
            'dlib': 1
        }
        model = model_switch[self.model] \
            if self.model in model_switch else 0
        vpy_ = []
        vpy_.append('from vscodeformer import codeformer\n')

        vpy_.append('res = codeformer(res,detector=' + str(model) + ',num_streams=1' + ',upscale=' + str(
            self.scale) + ',weight=' + str(self.weight)+ ',only_center_face=' + str(self.ocf)+ ',device_index=' + str(self.gpu_id) + ')\n')
        return vpy_

class rife_ml_setting(QObject):
    def __init__(self, mlrt_set, model, cscale, scale, change, debef, deaft):
        self.mlrt_set = mlrt_set
        self.model = model
        self.cscale = cscale
        self.scale = scale
        self.change = change
        self.debef = debef
        self.deaft = deaft

    def vfi_vpy(self):
        model_switch = {
            'rife4.0': [40, False],
            'rife4.2': [42, False],
            'rife4.3': [43, False],
            'rife4.4': [44, False],
            'rife4.5': [45, False],
            'rife4.6': [46, False],
            'rife4.0_ensemble': [40, True],
            'rife4.2_ensemble': [42, True],
            'rife4.3_ensemble': [43, True],
            'rife4.4_ensemble': [44, True],
            'rife4.5_ensemble': [45, True],
            'rife4.6_ensemble': [46, True]
        }
        model, ensemble = model_switch[self.model] \
            if self.model in model_switch else [46, False]

        vpy_ = []
        for str_ in self.mlrt_set.mlrt_vfi_device():
            vpy_.append(str_)

        if self.debef == '间隔一帧':
            vpy_.append('res = core.std.SelectEvery(clip=res, cycle=2, offsets=[0])\n')
        elif self.debef == '间隔两帧':
            vpy_.append('res = core.std.SelectEvery(clip=res, cycle=3, offsets=[0])\n')
        elif self.debef == '间隔三帧':
            vpy_.append('res = core.std.SelectEvery(clip=res, cycle=4, offsets=[0])\n')

        vpy_.append('res = core.misc.SCDetect(res, threshold=' + str(self.change) + ')\n')

        vpy_.append('scale='+str(self.scale)+'\n')
        vpy_.append('import math\n')
        vpy_.append('res_wid = math.ceil(res.width / (32/scale)) * (32/scale)- res.width\n')
        vpy_.append('res_hei = math.ceil(res.height / (32/scale)) * (32/scale)- res.height\n')

        vpy_.append('res = core.std.AddBorders(clip=res, right=res_wid, bottom=res_hei)\n')

        vpy_.append('res = RIFE(res,model=' + str(
            model) + ',multi=' + str(self.cscale) + ',ensemble=' + str(ensemble) +',scale=' + str(self.scale) + ', backend=device_vfi)\n')

        vpy_.append('res = core.std.Crop(clip=res, right=res_wid, bottom=res_hei)\n')

        if self.deaft == '间隔一帧':
            vpy_.append('res = core.std.SelectEvery(clip=res, cycle=2, offsets=[0])\n')
        elif self.deaft == '间隔两帧':
            vpy_.append('res = core.std.SelectEvery(clip=res, cycle=3, offsets=[0])\n')
        elif self.deaft == '间隔三帧':
            vpy_.append('res = core.std.SelectEvery(clip=res, cycle=4, offsets=[0])\n')
        return vpy_


class rifenc_setting(QObject):
    def __init__(self, model, usecs, usec, cscale, clips, skip, tta, uhd, static,gpu_id):
        self.model = model
        self.usecs = usecs
        self.usec = usec
        self.cscale = cscale
        self.clips = clips
        self.skip = skip
        self.tta = tta
        self.uhd = uhd
        self.static = static
        self.gpu_id=gpu_id

    def vfi_vpy(self):
        model_switch = {
            'rife': 0,
            'rife-HD': 1,
            'rife-UHD': 2,
            'rife-anime': 3,
            'rife-v2': 4,
            'rife-v2.3': 5,
            'rife-v2.4': 6,
            'rife-v3.0': 7,
            'rife-v3.1': 8,
            'rife-v4 (ensemble=False / fast=True)': 9,
            'rife-v4 (ensemble=True / fast=False)': 10,
            'rife-v4.1 (ensemble=False / fast=True)': 11,
            'rife-v4.1 (ensemble=True / fast=False)': 12,
            'rife-v4.2 (ensemble=False / fast=True)': 13,
            'rife-v4.2 (ensemble=True / fast=False)': 14,
            'rife-v4.3 (ensemble=False / fast=True)': 15,
            'rife-v4.3 (ensemble=True / fast=False)': 16,
            'rife-v4.4 (ensemble=False / fast=True)': 17,
            'rife-v4.4 (ensemble=True / fast=False)': 18,
            'rife-v4.5 (ensemble=False)': 19,
            'rife-v4.5 (ensemble=True)': 20,
            'rife-v4.6 (ensemble=False)': 21,
            'rife-v4.6 (ensemble=True)': 22,
            'sudo_rife4 (ensemble=False / fast=True)': 23,
            'sudo_rife4 (ensemble=True / fast=False)': 24,
            'sudo_rife4 (ensemble=True / fast=True)': 25
        }
        model = model_switch[self.model] \
            if self.model in model_switch else 21
        vpy_=[]
        vpy_.append('res = core.misc.SCDetect(res, threshold=0.3)\n')
        if self.usecs == True:
            vpy_.append('res=core.rife.RIFE(res,model="' + str(model) + '",factor_num=' + str(
                self.cscale) + ',skip=' + str(self.skip) + ',uhd=' + str(
                self.uhd) + ',tta=' + str(
                self.tta) + ',gpu_id='+str(
                self.gpu_id)+',skip_threshold=' + str(
                self.static) + ',sc=True)\n')

        else:
            vpy_.append('res=core.rife.RIFE(res,model="' + str(model) + '",skip=' + str(self.skip) + ',uhd=' + str(
                self.uhd) + ',tta=' + str(
                self.tta) + ',gpu_id='+str(
                self.gpu_id)+',skip_threshold=' + str(
                self.static) + ',fps_num='+str(self.clips)+',fps_den=1,sc=True)\n')

        return vpy_


class every_set_object(QObject):
    def __init__(self, gpu,videos,video_select, audios, subs, outfolder,
                 use_sr, sr_gpu_id, use_half_sr, sr_method, sr_set,
                 use_vfi, vfi_gpu_id, use_half_vfi,vfi_method,vfi_set,
                 use_qtgmc, use_deband, use_taa_bef,use_cas_aft,use_taa_aft,add_noise,
                 is_rs_bef, is_rs_aft, rs_bef_w, rs_bef_h, rs_aft_w,rs_aft_h,
                 encoder, preset, vformat, use_crf, use_bit, crf, bit,
                 use_encode_audio, use_source_audio, use_input_audio,audio_format,
                 use_source_sub, attach_input_sub, embed_input_sub,customization_encode, use_customization_encode,
                 cm_numstream, cm_gragh,tm_numstream,  trt_output, trt_force16, trt_graph, trt_cublas, trt_heuristic, om_numstream,nm_numstream ,
                 qtgmcFps, priority):
        self.gpu=gpu
        self.videos = videos
        self.video_select = video_select
        self.audios = audios
        self.subs = subs

        self.outfolder = outfolder

        self.use_sr = use_sr
        self.sr_gpu_id = sr_gpu_id
        self.use_half_sr = use_half_sr
        self.sr_method = sr_method
        self.sr_set = sr_set

        self.use_vfi = use_vfi
        self.vfi_gpu_id = vfi_gpu_id
        self.use_half_vfi = use_half_vfi
        self.vfi_method = vfi_method
        self.vfi_set = vfi_set

        self.use_qtgmc = use_qtgmc
        self.use_deband = use_deband
        self.use_taa_bef = use_taa_bef

        self.use_cas_aft=use_cas_aft
        self.use_taa_aft=use_taa_aft
        self.add_noise = add_noise

        self.is_rs_bef = is_rs_bef
        self.is_rs_aft = is_rs_aft
        self.rs_bef_w = rs_bef_w
        self.rs_bef_h = rs_bef_h
        self.rs_aft_w = rs_aft_w
        self.rs_aft_h = rs_aft_h

        self.encoder = encoder
        self.preset = preset
        self.vformat = vformat
        self.use_crf = use_crf
        self.use_bit = use_bit
        self.crf = crf
        self.bit = bit

        self.use_encode_audio = use_encode_audio
        self.use_source_audio = use_source_audio
        self.audio_format = audio_format
        self.use_input_audio=use_input_audio

        self.use_source_sub=use_source_sub
        self.attach_input_sub=attach_input_sub
        self.embed_input_sub=embed_input_sub

        self.customization_encode = customization_encode
        self.use_customization_encode = use_customization_encode

        self.cm_numstream=cm_numstream
        self.cm_gragh=cm_gragh

        self.tm_numstream = tm_numstream
        self.mlrt_trt_output = trt_output
        self.mlrt_trt_force16 = trt_force16
        self.mlrt_trt_graph = trt_graph
        self.mlrt_trt_cublas = trt_cublas
        self.mlrt_trt_heuristic = trt_heuristic

        self.om_numstream=om_numstream
        self.nm_numstream=nm_numstream

        self.qtgmcFps = qtgmcFps
        self.priority = priority
