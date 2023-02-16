import os
import subprocess as sp
import json
from configparser import ConfigParser
from pynvml import *

from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from VSET_UI import Ui_mainWindow

class FFprobe():
    def __init__(self):
        self.filepath = ''
        self._video_info = {}
        self.directory = os.path.dirname(os.path.realpath(sys.argv[0]))

    def parse(self, filepath):
        self.filepath = filepath
        try:
            res = sp.check_output(
                [self.directory + '/ffprobe', '-i', self.filepath, '-print_format', 'json', '-show_format',
                 '-show_streams', '-v',
                 'quiet'], shell=True)

            #测试路径
            # res = sp.check_output(
            #     ['ffprobe', '-i', self.filepath, '-print_format', 'json', '-show_format', '-show_streams', '-v',
            #      'quiet'],shell=True)
            res = res.decode('utf8')
            self._video_info = json.loads(res)
            # print('_video_info ',self._video_info)
        except Exception as e:
            print(e)
            raise Exception('获取视频信息失败')


    def video_full_frame(self):
        stream = self._video_info['streams'][0]
        return stream['nb_frames']

    def video_info(self):

        stream = self._video_info['streams']
        if 'color_space' in stream[0]:
            color_space=stream[0]['color_space']
        else:
            color_space=2
        if 'color_transfer' in stream[0]:
            color_transfer=stream[0]['color_transfer']
        else:
            color_transfer=2
        if 'color_primaries' in stream[0]:
            color_primaries=stream[0]['color_primaries']
        else:
            color_primaries=2

        item = {
            'color_space':color_space,
            'color_transfer':color_transfer,
            'color_primaries':color_primaries
        }
        return item

class Signal(QObject):
    text_update = pyqtSignal(str)

    def write(self, text):
        self.text_update.emit(str(text))
        QApplication.processEvents()

    def flush(self):
        pass

class cugan_ml_setting(QObject):
    def __init__(self,device,half,model,tile,alpha):
        self.device = device
        self.half = half
        self.model = model
        self.tile = tile
        self.alpha = alpha

    def return_model(self):
        return self.model

    def return_tile(self):
        return self.tile

    def return_alpha(self):
        return self.alpha

class esrgan_ml_setting(QObject):
    def __init__(self,device,half,model,tile,scale):
        self.device = device
        self.half = half
        self.model = model
        self.tile = tile
        self.scale = scale

    def return_model(self):
        return self.model

    def return_tile(self):
        return self.tile

    def return_scale(self):
        return self.scale

class waifu2x_ml_setting(QObject):
    def __init__(self,device,half,model,tile):
        self.device = device
        self.half = half
        self.model = model
        self.tile = tile

    def return_model(self):
        return self.model

    def return_tile(self):
        return self.tile

class vsrpp_setting(QObject):
    def __init__(self,model,interval,half):
        self.model = model
        self.interval = interval
        self.half = half

    def return_model(self):
        return self.model

    def return_interval(self):
        return self.interval

class vsr_setting(QObject):
    def __init__(self,model,radius,half):
        self.model = model
        self.radius = radius
        self.half = half

class esrgan_setting(QObject):
    def __init__(self,model,tile):
        self.model = model
        self.tile = tile

class esrgantrt_setting(QObject):
    def __init__(self,model):
        self.model = model

class animesr_setting(QObject):
    def __init__(self,model):
        self.model = model


class animesrtrt_setting(QObject):
    def __init__(self,model):
        self.model = model

class rife_ml_setting(QObject):
    def __init__(self,device,half,model,cscale,scale):
        self.device = device
        self.half = half
        self.model = model
        self.cscale = cscale
        self.scale = scale

class rife_setting(QObject):
    def __init__(self,model,usecs,usec,cscale,clips,scale,sct,use_smooth):
        self.model = model
        self.usecs = usecs
        self.usec = usec
        self.cscale = cscale
        self.clips = clips
        self.scale = scale
        self.sct = sct
        self.use_smooth = use_smooth

class rifetrt_setting(QObject):
    def __init__(self,model,usecs,usec,cscale,clips,scale,sct,use_smooth):
        self.model = model
        self.usecs = usecs
        self.usec = usec
        self.cscale = cscale
        self.clips = clips
        self.scale = scale
        self.sct = sct
        self.use_smooth = use_smooth

class rifenc_setting(QObject):
    def __init__(self,model,usecs,usec,cscale,clips,skip,tta,uhd,static):
        self.model = model
        self.usecs = usecs
        self.usec = usec
        self.cscale = cscale
        self.clips = clips
        self.skip = skip
        self.tta = tta
        self.uhd = uhd
        self.static = static

class gmfss_setting(QObject):
    def __init__(self,model,usecs,usec,cscale,clips,scale,sct,use_smooth):
        self.model = model
        self.usecs = usecs
        self.usec = usec
        self.cscale = cscale
        self.clips = clips
        self.scale = scale
        self.sct = sct
        self.use_smooth = use_smooth

class gmfsstrt_setting(QObject):
    def __init__(self,model,usecs,usec,cscale,clips,scale,sct,use_smooth):
        self.model = model
        self.usecs = usecs
        self.usec = usec
        self.cscale = cscale
        self.clips = clips
        self.scale = scale
        self.sct = sct
        self.use_smooth = use_smooth

class every_set_object(QObject):
    def __init__(self,videos,outfolder,
                                use_sr,sr_gpu,sr_gpu_id,sr_method,sr_set,use_vfi,vfi_gpu,vfi_gpu_id,vfi_method,vfi_set,use_qtgmc,use_deband,use_taa,is_rs_bef,is_rs_aft,rs_bef_w,rs_bef_h,rs_aft_w,rs_aft_h,
                                encoder,preset,eformat,vformat,use_crf,use_bit,crf,bit,use_encode_audio,use_source_audio,audio_format,customization_encode,use_customization_encode):
        self.videos = videos
        self.outfolder = outfolder

        self.use_sr = use_sr
        self.sr_gpu = sr_gpu
        self.sr_gpu_id = sr_gpu_id
        self.sr_method = sr_method
        self.sr_set = sr_set

        self.use_vfi = use_vfi
        self.vfi_gpu = vfi_gpu
        self.vfi_gpu_id = vfi_gpu_id
        self.vfi_method = vfi_method
        self.vfi_set = vfi_set

        self.use_qtgmc = use_qtgmc
        self.use_deband = use_deband
        self.use_taa = use_taa

        self.is_rs_bef = is_rs_bef
        self.is_rs_aft = is_rs_aft
        self.rs_bef_w = rs_bef_w
        self.rs_bef_h = rs_bef_h
        self.rs_aft_w = rs_aft_w
        self.rs_aft_h = rs_aft_h

        self.encoder = encoder
        self.preset = preset
        self.eformat = eformat
        self.vformat = vformat
        self.use_crf = use_crf
        self.use_bit = use_bit
        self.crf = crf
        self.bit = bit
        self.use_encode_audio = use_encode_audio
        self.use_source_audio = use_source_audio
        self.audio_format = audio_format
        self.customization_encode = customization_encode
        self.use_customization_encode = use_customization_encode

class autorun(QThread):
    signal = pyqtSignal()
    def __init__(self, every_setting, run_mode):
        super().__init__()
        self.every_setting=every_setting
        self.run_mode=run_mode
        self.directory = os.path.dirname(os.path.realpath(sys.argv[0]))

    def cugan_mlrt_(self):
        noise = 0
        scale = 2
        version = 2

        if self.every_setting.sr_set.model == 'pro-conservative-up2x':
            noise = 0
            scale = 2
            version = 2
        elif self.every_setting.sr_set.model == 'pro-conservative-up3x':
            noise = 0
            scale = 3
            version = 2
        elif self.every_setting.sr_set.model == 'pro-denoise3x-up2x':
            noise = 3
            scale = 2
            version = 2
        elif self.every_setting.sr_set.model == 'pro-denoise3x-up3x':
            noise = 3
            scale = 3
            version = 2
        elif self.every_setting.sr_set.model == 'pro-no-denoise3x-up2x':
            noise = -1
            scale = 2
            version = 2
        elif self.every_setting.sr_set.model == 'pro-no-denoise3x-up3x':
            noise = -1
            scale = 3
            version = 2
        elif self.every_setting.sr_set.model == 'up2x-latest-conservative':
            noise = 0
            scale = 2
            version = 1
        elif self.every_setting.sr_set.model == 'up2x-latest-denoise1x':
            noise = 1
            scale = 2
            version = 1
        elif self.every_setting.sr_set.model == 'up2x-latest-denoise2x':
            noise = 2
            scale = 2
            version = 1
        elif self.every_setting.sr_set.model == 'up2x-latest-denoise3x':
            noise = 3
            scale = 2
            version = 1
        elif self.every_setting.sr_set.model == 'up2x-latest-no-denoise':
            noise = -1
            scale = 2
            version = 1
        elif self.every_setting.sr_set.model == 'up3x-latest-conservative':
            noise = 0
            scale = 3
            version = 1
        elif self.every_setting.sr_set.model == 'up3x-latest-denoise3x':
            noise = 3
            scale = 3
            version = 1
        elif self.every_setting.sr_set.model == 'up3x-latest-no-denoise':
            noise = -1
            scale = 3
            version = 1
        elif self.every_setting.sr_set.model == 'up4x-latest-conservative':
            noise = 0
            scale = 4
            version = 1
        elif self.every_setting.sr_set.model == 'up4x-latest-denoise3x':
            noise = 3
            scale = 4
            version = 1
        elif self.every_setting.sr_set.model == 'up4x-latest-no-denoise':
            noise = -1
            scale = 4
            version = 1
        cugan_vpy=[]
        if self.every_setting.sr_set.device == 'GPU_CUDA':
            cugan_vpy.append('device=Backend.ORT_CUDA()\n')
        elif self.every_setting.sr_set.device == 'GPU_TRT':
            cugan_vpy.append('device=Backend.TRT()\n')
        elif self.every_setting.sr_set.device == 'NCNN':
            cugan_vpy.append('device=Backend.NCNN_VK()\n')
        cugan_vpy.append('device.device_id=' + str(self.every_setting.sr_gpu_id) + '\n')
        cugan_vpy.append('device.fp16=' + str(self.every_setting.sr_set.half) + '\n')
        cugan_vpy.append('res = CUGAN(res, noise='+str(noise)+', scale='+str(scale)+', tiles='+str(self.every_setting.sr_set.tile)+',version='+str(version)+',alpha='+str(self.every_setting.sr_set.alpha)+', backend=device)\n')
        return cugan_vpy

    def esrgan_mlrt_(self):
        model=0
        if self.every_setting.sr_set.model=='animevideov3':
            model=0
        elif self.every_setting.sr_set.model=='animevideo-xsx2':
            model = 1
        elif self.every_setting.sr_set.model=='animevideo-xsx4':
            model = 2

        esrgan_vpy=[]
        if self.every_setting.sr_set.device == 'GPU_CUDA':
            esrgan_vpy.append('device=Backend.ORT_CUDA()\n')
        elif self.every_setting.sr_set.device == 'GPU_TRT':
            esrgan_vpy.append('device=Backend.TRT()\n')
        elif self.every_setting.sr_set.device == 'NCNN':
            esrgan_vpy.append('device=Backend.NCNN_VK()\n')
        esrgan_vpy.append('device.device_id=' + str(self.every_setting.sr_gpu_id) + '\n')
        esrgan_vpy.append('device.fp16=' + str(self.every_setting.sr_set.half) + '\n')
        esrgan_vpy.append('res = RealESRGAN(res, scale='+str(self.every_setting.sr_set.scale)+',tiles='+str(self.every_setting.sr_set.tile)+',model='+str(model)+', backend=device)\n')
        return esrgan_vpy

    def waifu2x_mlrt_(self):
        noise=1
        scale=1
        model=1
        if self.every_setting.sr_set.model=='anime_style_art_rgb_noise0':
            noise = 0
            scale = 1
            model = 1
        elif self.every_setting.sr_set.model=='anime_style_art_rgb_noise1':
            noise = 1
            scale = 1
            model = 1
        elif self.every_setting.sr_set.model == 'anime_style_art_rgb_noise2':
            noise = 2
            scale = 1
            model = 1
        elif self.every_setting.sr_set.model=='anime_style_art_rgb_noise3':
            noise = 3
            scale = 1
            model = 1
        elif self.every_setting.sr_set.model=='anime_style_art_rgb_scale2.0x':
            noise = -1
            scale = 2
            model = 1
        elif self.every_setting.sr_set.model=='cunet_noise0':
            noise = 0
            scale = 1
            model = 6
        elif self.every_setting.sr_set.model=='cunet_noise0_scale2.0x':
            noise = 0
            scale = 2
            model = 6
        elif self.every_setting.sr_set.model=='cunet_noise1':
            noise = 1
            scale = 1
            model = 6
        elif self.every_setting.sr_set.model=='cunet_noise1_scale2.0x':
            noise = 1
            scale = 2
            model = 6
        elif self.every_setting.sr_set.model=='cunet_noise2':
            noise = 2
            scale = 1
            model = 6
        elif self.every_setting.sr_set.model=='cunet_noise2_scale2.0x':
            noise = 2
            scale = 2
            model = 6
        elif self.every_setting.sr_set.model=='cunet_noise3':
            noise = 3
            scale = 1
            model = 6
        elif self.every_setting.sr_set.model=='cunet_noise3_scale2.0x':
            noise = 3
            scale = 2
            model = 6
        elif self.every_setting.sr_set.model=='cunet_scale2.0x':
            noise = -1
            scale = 2
            model = 6
        elif self.every_setting.sr_set.model=='photo_noise0':
            noise = 0
            scale = 1
            model = 2
        elif self.every_setting.sr_set.model=='photo_noise1':
            noise = 1
            scale = 1
            model = 2
        elif self.every_setting.sr_set.model=='photo_noise2':
            noise = 2
            scale = 1
            model = 2
        elif self.every_setting.sr_set.model=='photo_noise3':
            noise = 3
            scale = 1
            model = 2
        elif self.every_setting.sr_set.model=='photo_scale2.0x':
            noise = -1
            scale = 2
            model = 2
        elif self.every_setting.sr_set.model=='upconv_7_anime_noise0_scale2.0x':
            noise = 0
            scale = 2
            model = 3
        elif self.every_setting.sr_set.model=='upconv_7_anime_noise1_scale2.0x':
            noise = 1
            scale = 2
            model = 3
        elif self.every_setting.sr_set.model=='upconv_7_anime_noise2_scale2.0x':
            noise = 2
            scale = 2
            model = 3
        elif self.every_setting.sr_set.model=='upconv_7_anime_noise3_scale2.0x':
            noise = 3
            scale = 2
            model = 3
        elif self.every_setting.sr_set.model=='upconv_7_anime_scale2.0x':
            noise = -1
            scale = 2
            model = 3
        elif self.every_setting.sr_set.model=='upconv_7_photo_noise0_scale2.0x':
            noise = 0
            scale = 2
            model = 4
        elif self.every_setting.sr_set.model=='upconv_7_photo_noise1_scale2.0x':
            noise = 1
            scale = 2
            model = 4
        elif self.every_setting.sr_set.model=='upconv_7_photo_noise2_scale2.0x':
            noise = 2
            scale = 2
            model = 4
        elif self.every_setting.sr_set.model=='upconv_7_photo_noise3_scale2.0x':
            noise = 3
            scale = 2
            model = 4
        elif self.every_setting.sr_set.model=='upconv_7_photo_scale2.0x':
            noise = -1
            scale = 2
            model = 4
        elif self.every_setting.sr_set.model=='upresnet10_noise0_scale2.0x':
            noise = 0
            scale = 2
            model = 5
        elif self.every_setting.sr_set.model=='upresnet10_noise1_scale2.0x':
            noise = 1
            scale = 2
            model = 5
        elif self.every_setting.sr_set.model=='upresnet10_noise2_scale2.0x':
            noise = 2
            scale = 2
            model = 5
        elif self.every_setting.sr_set.model=='upresnet10_noise3_scale2.0x':
            noise = 3
            scale = 2
            model = 5
        elif self.every_setting.sr_set.model=='upresnet10_scale2.0x':
            noise = -1
            scale = 2
            model = 5

        waifu_vpy = []
        if self.every_setting.sr_set.device == 'GPU_CUDA':
            waifu_vpy.append('device=Backend.ORT_CUDA()\n')
        elif self.every_setting.sr_set.device == 'GPU_TRT':
            waifu_vpy.append('device=Backend.TRT()\n')
        elif self.every_setting.sr_set.device == 'NCNN':
            waifu_vpy.append('device=Backend.NCNN_VK()\n')

        waifu_vpy.append('device.device_id=' + str(self.every_setting.sr_gpu_id) + '\n')
        waifu_vpy.append('device.fp16=' + str(self.every_setting.sr_set.half) + '\n')
        waifu_vpy.append('res = Waifu2x(res, noise='+str(noise)+',scale='+str(scale)+',tiles='+str(self.every_setting.sr_set.tile)+',model='+str(model)+', backend=device)\n')
        return waifu_vpy

    def vsrpp_(self):
        model =0
        if self.every_setting.sr_set.model=='reds4':
            model = 0
        elif self.every_setting.sr_set.model=='vimeo90k_bi':
            model = 1
        elif self.every_setting.sr_set.model=='vimeo90k_bd':
            model = 2
        elif self.every_setting.sr_set.model=='ntire_decompress_track1':
            model = 3
        elif self.every_setting.sr_set.model=='ntire_decompress_track2':
            model = 4
        elif self.every_setting.sr_set.model=='ntire_decompress_track3':
            model = 5
        return ('res = BasicVSRPP(res,model='+str(model)+',interval='+str(self.every_setting.sr_set.interval)+',device_index='+str(self.every_setting.sr_gpu_id)+',fp16='+str(self.every_setting.sr_set.half)+')\n')

    def vsr_(self):
        model = 0
        if self.every_setting.sr_set.model == 'REDS4':
            model = 0
        elif self.every_setting.sr_set.model == 'Vimeo90K_BIx4':
            model = 1
        elif self.every_setting.sr_set.model == 'Vimeo90K_BDx4':
            model = 2

        return ('res = BasicVSR(res,model=' + str(model) + ',radius=' + str(
        self.every_setting.sr_set.radius) + ',device_index=' + str(self.every_setting.sr_gpu_id) + ',fp16=' + str(
        self.every_setting.sr_set.half) + ')\n')

    def esrgan_(self):
        model = 0
        if self.every_setting.sr_set.model == 'SRx4_DF2KOST_official':
            model = 0
        elif self.every_setting.sr_set.model == 'x2plus':
            model = 1
        elif self.every_setting.sr_set.model == 'x4plus':
            model = 2
        elif self.every_setting.sr_set.model == 'x4plus_anime_6B':
            model = 3
        elif self.every_setting.sr_set.model == 'animevideov3':
            model = 4

        return ('res = RealESRGAN(res,model=' + str(model) + ',tile_w='+str(self.every_setting.sr_set.tile)+',device_index=' + str(self.every_setting.sr_gpu_id)+ ')\n')

    def esrgantrt_(self):
        model = 0
        if self.every_setting.sr_set.model == 'SRx4_DF2KOST_official':
            model = 0
        elif self.every_setting.sr_set.model == 'x2plus':
            model = 1
        elif self.every_setting.sr_set.model == 'x4plus':
            model = 2
        elif self.every_setting.sr_set.model == 'x4plus_anime_6B':
            model = 3
        elif self.every_setting.sr_set.model == 'animevideov3':
            model = 4

        return ('res = RealESRGAN(res,model=' + str(model) + ',device_index=' + str(self.every_setting.sr_gpu_id)+ ',trt=True' + ')\n')

    def animesr_(self):
        model = 0
        if self.every_setting.sr_set.model == 'v1-PaperModel':
            model = 0
        elif self.every_setting.sr_set.model == 'v2':
            model = 1

        return ('res = animesr(res,model=' + str(model) +',device_index=' + str(
            self.every_setting.sr_gpu_id) + ')\n')

    def animesrtrt_(self):
        model = 0
        if self.every_setting.sr_set.model == 'v1-PaperModel':
            model = 0
        elif self.every_setting.sr_set.model == 'v2':
            model = 1

        return ('res = animesr(res,model=' + str(model) + ',device_index=' + str(
            self.every_setting.sr_gpu_id) + ',trt=True' + ')\n')

    def rifemlrt_(self):
        model = 0
        if self.every_setting.vfi_set.model=='rife4.0':
            model = 40
        elif self.every_setting.vfi_set.model=='rife4.2':
            model = 42
        elif self.every_setting.vfi_set.model=='rife4.3':
            model = 43
        elif self.every_setting.vfi_set.model=='rife4.4':
            model = 44
        elif self.every_setting.vfi_set.model=='rife4.5':
            model = 45
        elif self.every_setting.vfi_set.model=='rife4.6':
            model = 46
        rifemlrt_vpy=[]
        if self.every_setting.vfi_set.device == 'GPU_CUDA':
            rifemlrt_vpy.append('device_vfi=Backend.ORT_CUDA()\n')
        elif self.every_setting.vfi_set.device == 'GPU_TRT':
            rifemlrt_vpy.append('device_vfi=Backend.TRT()\n')
        elif self.every_setting.vfi_set.device == 'NCNN':
            rifemlrt_vpy.append('device_vfi=Backend.NCNN_VK()\n')
        rifemlrt_vpy.append('device_vfi.device_id=' + str(self.every_setting.vfi_gpu_id) + '\n')
        rifemlrt_vpy.append('device_vfi.fp16=' + str(self.every_setting.vfi_set.half) + '\n')
        rifemlrt_vpy.append('res = RIFE(res,model='+str(model)+',multi='+self.every_setting.vfi_set.cscale+',scale='+self.every_setting.vfi_set.scale+', backend=device_vfi)\n')
        return rifemlrt_vpy

    def rife_(self):
        model=0
        if self.every_setting.vfi_set.model=='rife4.0':
            model = 4.0
        elif self.every_setting.vfi_set.model=='rife4.1':
            model = 4.1
        elif self.every_setting.vfi_set.model=='rife4.2':
            model = 4.2
        elif self.every_setting.vfi_set.model=='rife4.3':
            model = 4.3
        elif self.every_setting.vfi_set.model=='rife4.4':
            model = 4.4
        elif self.every_setting.vfi_set.model=='rife4.5':
            model = 4.5
        elif self.every_setting.vfi_set.model=='rife4.6':
            model = 4.6

        if self.every_setting.vfi_set.usecs==True:
            return 'res=RIFE(res,model="'+str(model)+'",factor_num='+str(self.every_setting.vfi_set.cscale)+',scale='+str(self.every_setting.vfi_set.scale)+',ensemble='+str(self.every_setting.vfi_set.use_smooth)+',sc_threshold='+str(self.every_setting.vfi_set.sct)+')\n'
        else:
            return 'res=RIFE(res,model="'+str(model)+'",fps_num='+str(self.every_setting.vfi_set.clips)+',fps_den=1,scale='+str(self.every_setting.vfi_set.scale)+',ensemble='+str(self.every_setting.vfi_set.use_smooth)+',sc_threshold='+str(self.every_setting.vfi_set.sct)+')\n'

    def rifetrt_(self):
        model=0
        if self.every_setting.vfi_set.model=='rife4.2':
            model = 4.2
        elif self.every_setting.vfi_set.model=='rife4.3':
            model = 4.3
        elif self.every_setting.vfi_set.model=='rife4.4':
            model = 4.4
        elif self.every_setting.vfi_set.model=='rife4.5':
            model = 4.5
        elif self.every_setting.vfi_set.model=='rife4.6':
            model = 4.6

        if self.every_setting.vfi_set.usecs==True:
            return 'res=RIFE(res,model="'+str(model)+'",factor_num='+str(self.every_setting.vfi_set.cscale)+',scale='+str(self.every_setting.vfi_set.scale)+',ensemble='+str(self.every_setting.vfi_set.use_smooth)+',sc_threshold='+str(self.every_setting.vfi_set.sct)+',trt=True)\n'
        else:
            return 'res=RIFE(res,model="'+str(model)+'",fps_num='+str(self.every_setting.vfi_set.clips)+',fps_den=1,scale='+str(self.every_setting.vfi_set.scale)+',ensemble='+str(self.every_setting.vfi_set.use_smooth)+',sc_threshold='+str(self.every_setting.vfi_set.sct)+',trt=True)\n'

    def rifencnn_(self):
        model = 0
        if self.every_setting.vfi_set.model == 'rife':
            model = 0
        elif self.every_setting.vfi_set.model == 'rife-HD':
            model = 1
        elif self.every_setting.vfi_set.model == 'rife-UHD':
            model = 2
        elif self.every_setting.vfi_set.model == 'rife-anime':
            model = 3
        elif self.every_setting.vfi_set.model == 'rife-v2':
            model = 4
        elif self.every_setting.vfi_set.model == 'rife-v2.3':
            model = 5
        elif self.every_setting.vfi_set.model == 'rife-v2.4':
            model = 6
        elif self.every_setting.vfi_set.model == 'rife-v3.0':
            model = 7
        elif self.every_setting.vfi_set.model == 'rife-v3.1':
            model = 8
        elif self.every_setting.vfi_set.model == 'rife-v4 (ensemble=False / fast=True)':
            model = 9
        elif self.every_setting.vfi_set.model == 'rife-v4 (ensemble=True / fast=False)':
            model = 10
        elif self.every_setting.vfi_set.model == 'rife-v4.1 (ensemble=False / fast=True)':
            model = 11
        elif self.every_setting.vfi_set.model == 'rife-v4.1 (ensemble=True / fast=False)':
            model = 12
        elif self.every_setting.vfi_set.model == 'rife-v4.2 (ensemble=False / fast=True)':
            model = 13
        elif self.every_setting.vfi_set.model == 'rife-v4.2 (ensemble=True / fast=False)':
            model = 14
        elif self.every_setting.vfi_set.model == 'rife-v4.3 (ensemble=False / fast=True)':
            model = 15
        elif self.every_setting.vfi_set.model == 'rife-v4.3 (ensemble=True / fast=False)':
            model = 16
        elif self.every_setting.vfi_set.model == 'rife-v4.4 (ensemble=False / fast=True)':
            model = 17
        elif self.every_setting.vfi_set.model == 'rife-v4.4 (ensemble=True / fast=False)':
            model = 18
        elif self.every_setting.vfi_set.model == 'rife-v4.5 (ensemble=False)':
            model = 19
        elif self.every_setting.vfi_set.model == 'rife-v4.5 (ensemble=True)':
            model = 20
        elif self.every_setting.vfi_set.model == 'rife-v4.6 (ensemble=False)':
            model = 21
        elif self.every_setting.vfi_set.model == 'rife-v4.6 (ensemble=True)':
            model = 22
        elif self.every_setting.vfi_set.model == 'sudo_rife4 (ensemble=False / fast=True)':
            model = 23
        elif self.every_setting.vfi_set.model == 'sudo_rife4 (ensemble=True / fast=False)':
            model = 24
        elif self.every_setting.vfi_set.model == 'sudo_rife4 (ensemble=True / fast=True)':
            model = 25

        if self.every_setting.vfi_set.usecs == True:
            return 'res=core.rife.RIFE(res,model="' + str(model) + '",factor_num=' + str(
                self.every_setting.vfi_set.cscale) + ',skip=' + str(self.every_setting.vfi_set.skip) + ',uhd=' + str(
                self.every_setting.vfi_set.uhd) + ',tta=' + str(
                self.every_setting.vfi_set.tta) + ',skip_threshold=' + str(
                self.every_setting.vfi_set.static) + ',sc=True)\n'
        else:
            return 'res=core.rife.RIFE(res,model="' + str(model) + '",skip=' + str(self.every_setting.vfi_set.skip) + ',uhd=' + str(
                self.every_setting.vfi_set.uhd) + ',tta=' + str(
                self.every_setting.vfi_set.tta) + ',skip_threshold=' + str(
                self.every_setting.vfi_set.static) + ',fps_num='+str(self.every_setting.vfi_set.clips)+',fps_den=1,sc=True)\n'

    def gmfss_(self):
        model = 0
        if self.every_setting.vfi_set.model == 'vanillagan':
            model = 0
        elif self.every_setting.vfi_set.model == 'wgan':
            model = 1

        if self.every_setting.vfi_set.usecs==True:
            return 'res=gmfss_union(res,model='+str(model)+',factor_num='+str(self.every_setting.vfi_set.cscale)+',scale='+str(self.every_setting.vfi_set.scale)+',ensemble='+str(self.every_setting.vfi_set.use_smooth)+',sc_threshold='+str(self.every_setting.vfi_set.sct)+')\n'
        else:
            return 'res=gmfss_union(res,model='+str(model)+',fps_num='+str(self.every_setting.vfi_set.clips)+',fps_den=1,scale='+str(self.every_setting.vfi_set.scale)+',ensemble='+str(self.every_setting.vfi_set.use_smooth)+',sc_threshold='+str(self.every_setting.vfi_set.sct)+')\n'

    def gmfsstrt_(self):
        model = 0
        if self.every_setting.vfi_set.model == 'vanillagan':
            model = 0
        elif self.every_setting.vfi_set.model == 'wgan':
            model = 1

        if self.every_setting.vfi_set.usecs==True:
            return 'res=gmfss_union(res,model='+str(model)+',factor_num='+str(self.every_setting.vfi_set.cscale)+',scale='+str(self.every_setting.vfi_set.scale)+',ensemble='+str(self.every_setting.vfi_set.use_smooth)+',sc_threshold='+str(self.every_setting.vfi_set.sct)+'trt=True)\n'
        else:
            return 'res=gmfss_union(res,model='+str(model)+',fps_num='+str(self.every_setting.vfi_set.clips)+',fps_den=1,scale='+str(self.every_setting.vfi_set.scale)+',ensemble='+str(self.every_setting.vfi_set.use_smooth)+',sc_threshold='+str(self.every_setting.vfi_set.sct)+'trt=True)\n'


    def ffmpeg_(self):
        ffmpeg_set = []
        if self.every_setting.use_customization_encode == True:
            ffmpeg_set_customizatio=str(self.every_setting.customization_encode)
            for str_ in ffmpeg_set_customizatio.split():
                ffmpeg_set.append(str_)
        else:
            if self.every_setting.encoder == 'cpu' and self.every_setting.eformat == 'H265':
                ffmpeg_set.append('-c:v')
                ffmpeg_set.append('libx265')
                ffmpeg_set.append('-pix_fmt')
                ffmpeg_set.append('yuv420p10le')
                ffmpeg_set.append('-profile:v')
                ffmpeg_set.append('main10')
            elif self.every_setting.encoder == 'cpu' and self.every_setting.eformat == 'H264':
                ffmpeg_set.append('-c:v')
                ffmpeg_set.append('libx264')
                ffmpeg_set.append('-pix_fmt')
                ffmpeg_set.append('yuv420p')
                ffmpeg_set.append('-profile:v')
                ffmpeg_set.append('main')
            elif self.every_setting.encoder == 'cpu' and self.every_setting.eformat == 'av1':
                ffmpeg_set.append('-c:v')
                ffmpeg_set.append('libsvtav1')
                ffmpeg_set.append('-pix_fmt')
                ffmpeg_set.append('yuv420p10le')
                ffmpeg_set.append('-profile:v')
                ffmpeg_set.append('main10')
            elif self.every_setting.encoder == 'nvenc' and self.every_setting.eformat == 'H264':
                ffmpeg_set.append('-c:v')
                ffmpeg_set.append('h264_nvenc')
                ffmpeg_set.append('-pix_fmt')
                ffmpeg_set.append('yuv420p')
                ffmpeg_set.append('-profile:v')
                ffmpeg_set.append('main')
            elif self.every_setting.encoder == 'nvenc' and self.every_setting.eformat == 'H265':
                ffmpeg_set.append('-c:v')
                ffmpeg_set.append('hevc_nvenc')
                ffmpeg_set.append('-pix_fmt')
                ffmpeg_set.append('yuv420p10le')
                ffmpeg_set.append('-profile:v')
                ffmpeg_set.append('main10')
            elif self.every_setting.encoder == 'nvenc' and self.every_setting.eformat == 'av1':
                ffmpeg_set.append('-c:v')
                ffmpeg_set.append('av1_nvenc')
                ffmpeg_set.append('-pix_fmt')
                ffmpeg_set.append('yuv420p10le')
                ffmpeg_set.append('-profile:v')
                ffmpeg_set.append('main10')

            ffmpeg_set.append('-preset')
            ffmpeg_set.append(self.every_setting.preset)

            if self.every_setting.eformat == 'H265':

                ffmpeg_set.append('-vtag')
                ffmpeg_set.append('hvc1')

            if self.every_setting.use_crf == True:
                ffmpeg_set.append('-crf')
                ffmpeg_set.append(self.every_setting.crf)
            else:
                ffmpeg_set.append('-b:v')
                ffmpeg_set.append(self.every_setting.bit + 'M')

        return  ffmpeg_set


    def run(self):
        vpy_folder = self.every_setting.outfolder + '/vpys'
        if self.run_mode == 'debug':
            bat_file = open(self.every_setting.outfolder + '/run.bat', 'w', encoding='ansi')
        if not os.path.exists(vpy_folder):
            os.makedirs(vpy_folder)#存放配置文件vpy的文件夹
        video_folder = self.every_setting.outfolder + '/out_videos'
        if not os.path.exists(video_folder):
            os.makedirs(video_folder)

        #实测路径
        #FFMPEG_BIN=self.directory + '\\vapoursynth\\ffmpeg.exe'
        #测试路径
        #FFMPEG_BIN = 'ffmpeg.exe'
        num = 1
        for video in self.every_setting.videos:
            print('正在运行队列中第'+str(num)+'个视频')

            ffmpeg_code = self.ffmpeg_()
            ffprobe = FFprobe()
            ffprobe.parse(video)

            video_name = (video.rsplit("/", 1))[-1]
            video_name = (video_name.rsplit(".", 1))[0]  # 只保留文件名的参数

            # 色彩处理(色偏主要原因，注释掉即可恢复，后期再来考虑保证色彩空间的情况下不偏色)
            # color_info=[]
            # v_info = ffprobe.video_info()
            # if v_info['color_space'] != 2:
            #     color_info.append('-vf')
            #     color_info.append('scale=out_color_matrix=' + v_info['color_space'])
            #     color_info.append('-colorspace')
            #     color_info.append(v_info['color_space'])
            #
            # if v_info['color_transfer'] != 2:
            #     color_info.append('-color_trc')
            #     color_info.append(v_info['color_transfer'])
            #
            # if v_info['color_primaries'] != 2:
            #     color_info.append('-color_primaries')
            #     color_info.append(v_info['color_primaries'])

            #音频处理
            audio_info=[]
            have_audio = False
            for i in ffprobe._video_info['streams']:
                if i['codec_type'] == 'audio':
                    have_audio = True
                    break
            if have_audio == True:
                print(video+' 有音频')
            else:
                print(video+' 无音频')

            if have_audio == True:
                if self.every_setting.use_encode_audio == True:
                    audio_info.append('-c:a')
                    audio_info.append(self.every_setting.audio_format)
                    if self.every_setting.audio_format=='flac':
                        audio_info.append('-strict')
                        audio_info.append('-2')
                else:
                    audio_info.append('-c:a')
                    audio_info.append('copy')
            # 实测路径
            # FFMPEG_BIN=self.directory + '/vs_pytorch/ffmpeg.exe'
            # 测试路径
            # FFMPEG_BIN = 'ffmpeg.exe'
            FFMPEG_BIN = self.directory + '/ffmpeg.exe'
            #输入处理
            input_info=[FFMPEG_BIN]
            input_info.append('-hide_banner')
            input_info.append('-y')
            input_info.append('-i')
            input_info.append('pipe:')
            input_info.append('-i')
            input_info.append(video)
            input_info.append('-map')
            input_info.append('0:v:0')
            if have_audio == True:
                input_info.append('-map')
                input_info.append('1:a')

            #输出处理
            output_info=[]

            output_info.append(video_folder+'/'+video_name+'.'+self.every_setting.vformat)
            if self.every_setting.use_customization_encode == False:
                # ffmpeg_code = input_info + ffmpeg_code + color_info + audio_info + output_info
                ffmpeg_code = input_info + ffmpeg_code + audio_info + output_info
            else:
                ffmpeg_code=input_info + ffmpeg_code + output_info

            #vpy配置文件生成
            vpy_place = vpy_folder + '/' + video_name + '.vpy'
            vpy = open(vpy_place, 'w', encoding='utf-8')

            vpy.write('import vapoursynth as vs\n')
            vpy.write('core = vs.core\n')

            vpy.write('res = core.lsmas.LWLibavSource(r"' + video + '")\n')

            if self.every_setting.is_rs_bef == True:
                vpy.write(
                    'res = core.resize.Bicubic(clip=res,width=' + self.every_setting.rs_bef_w + ',height=' + self.every_setting.rs_bef_h + ',format=vs.YUV420P16)\n')
            else:
                vpy.write('res = core.resize.Bicubic(clip=res,format=vs.YUV420P16)\n')
            if self.every_setting.use_qtgmc==True:
                vpy.write('import havsfunc as haf\n')
                vpy.write('res = haf.QTGMC(res, Preset="'+'Slower'+'", TFF=True, FPSDivisor=2)\n')
            if self.every_setting.use_deband == True:
                vpy.write('res  = core.neo_f3kdb.Deband(res,preset="medium",output_depth=16)\n')
            if self.every_setting.use_taa == True:
                vpy.write('import vsTAAmbk as taa\n')
                vpy.write('res = taa.TAAmbk(res, aatype=-3, preaa=-1, strength=0.1, mtype=2, aapair=1, cycle=5, sharp=0)\n')

            vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n')
            vpy.write('res=core.fmtc.bitdepth(res, bits=32)\n')
            #vspipe默认路径
            vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'


            if self.every_setting.use_sr==True:

                #判断超分算法类型
                if self.every_setting.sr_method == 'Real_cugan_mlrt':
                    vpy.write('from vsmlrt import CUGAN,Backend\n')
                    cugan_vpy=self.cugan_mlrt_()

                    for str_ in cugan_vpy:
                        vpy.write(str_)

                    vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'

                if self.every_setting.sr_method == 'Real_esrgan_mlrt':
                    vpy.write('from vsmlrt import RealESRGAN,Backend\n')
                    esrgan_vpy = self.esrgan_mlrt_()
                    for str_ in esrgan_vpy:
                        vpy.write(str_)
                    vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'

                if self.every_setting.sr_method == 'Waifu2x_mlrt':
                    vpy.write('from vsmlrt import Waifu2x,Backend\n')
                    waifu_vpy = self.waifu2x_mlrt_()
                    for str_ in waifu_vpy:
                        vpy.write(str_)
                    vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'

                if self.every_setting.sr_method == 'Basicvsrpp':
                    vpy.write('from vsbasicvsrpp import BasicVSRPP\n')
                    vpy.write(self.vsrpp_())
                    vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

                if self.every_setting.sr_method == 'Basicvsr':
                    vpy.write('from vsbasicvsr import BasicVSR\n')
                    vpy.write(self.vsr_())
                    vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

                if self.every_setting.sr_method == 'Real_esrgan':
                    vpy.write('from vsrealesrgan import RealESRGAN\n')
                    vpy.write(self.esrgan_())
                    vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

                if self.every_setting.sr_method == 'Real_esrgan_trt':
                    vpy.write('from vsrealesrgan import RealESRGAN\n')
                    vpy.write(self.esrgantrt_())
                    vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

                if self.every_setting.sr_method == 'AnimeSR':
                    vpy.write('from vsanimesr import animesr\n')
                    vpy.write(self.animesr_())
                    vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

                if self.every_setting.sr_method == 'AnimeSR_trt':
                    vpy.write('from vsanimesr import animesr\n')
                    vpy.write(self.animesrtrt_())
                    vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

            if self.every_setting.use_vfi == True:

                if self.every_setting.vfi_method == 'rife_mlrt':
                    vpy.write('from vsmlrt import RIFE,Backend\n')
                    for str_ in self.rifemlrt_():
                        vpy.write(str_)
                    vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'

                if self.every_setting.vfi_method == 'rife':
                    vpy.write('from vsrife import RIFE\n')
                    vpy.write(self.rife_())
                    vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

                if self.every_setting.vfi_method == 'rife_trt':
                    vpy.write('from vsrife import RIFE\n')
                    vpy.write(self.rifetrt_())
                    vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'
                if self.every_setting.vfi_method == 'rife_ncnn':
                    vpy.write(self.rifencnn_())
                    vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'
                if self.every_setting.vfi_method == 'gmfss':
                    vpy.write('from vsgmfss_union import gmfss_union\n')
                    vpy.write(self.gmfss_())
                    vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'
                if self.every_setting.vfi_method == 'gmfss_trt':
                    vpy.write('from vsgmfss_union import gmfss_union\n')
                    vpy.write(self.gmfsstrt_())
                    vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

            if self.every_setting.is_rs_aft == True:
                vpy.write(
                    'res = core.resize.Bicubic(clip=res,matrix_s="709",width=' + self.every_setting.rs_aft_w + ',height=' + self.every_setting.rs_aft_h + ',format=vs.YUV444P16)\n')
            else:
                vpy.write('res = core.resize.Bicubic(clip=res,matrix_s="709",format=vs.YUV444P16)\n')

            vpy.write('res.set_output()\n')
            vpy.close()
            print('生成第' + str(num) + '个vpy脚本文件')

            vspipe_code=[]
            #实测路径
            #vspipe_bin=self.directory + '/vapoursynth/VSPipe.exe'
            # 测试路径
            #vspipe_bin = 'D:/VS_NangInShell/VS_Nang/package/VSPipe.exe'
            vspipe_code.append(vspipe_bin)
            vspipe_code.append('-c')
            vspipe_code.append('y4m')
            vspipe_code.append(vpy_place)
            vspipe_code.append('-')
            command_out = vspipe_code
            command_in = ffmpeg_code
            command_test=[]
            command_test.append(vspipe_bin)
            command_test.append('--info')
            command_test.append(vpy_place)

            print(command_out)
            print(command_in)
            print('\n')
            if self.run_mode=='start':
                pipe_out = sp.Popen(command_out, stdout=sp.PIPE, shell=True)
                pipe_in = sp.Popen(command_in, stdin=pipe_out.stdout, stdout=sp.PIPE, stderr=sp.STDOUT, shell=True,
                                   encoding="utf-8", text=True)
                pipe_test=sp.Popen(command_test, stdout=sp.PIPE, stderr=sp.PIPE,shell=True)
                for line in pipe_test.stderr:
                    print(str(line,encoding='utf-8').replace("\n",""))

                print("已输出debug信息，这是队列中第" + str(num) + '个视频。')

                while pipe_in.poll() is None:
                    line = pipe_in.stdout.readline()
                    line = line.strip()
                    if line:
                        print(format(line))
                print(video+" 已经渲染完成，这是队列中第"+str(num)+'个视频。')
            # for line in pipe_in.stdout:
            #     print(line)
            elif self.run_mode=='debug':
                for str_ in command_out:
                    bat_file.write('\"'+str_+'\"'+' ')
                bat_file.write('| ')
                for str_ in command_in:
                    bat_file.write('\"'+str_+'\"'+' ')
                bat_file.write('\n')
                print('队列中第'+str(num)+'个视频：'+video+' 的配置文件已经生成，相关配置信息已经写入输出文件夹的run.bat文件')
            num=num+1
            print('\n')
        if self.run_mode=='debug':
            bat_file.write('pause')
        self.signal.emit()


class MyMainWindow(QMainWindow, Ui_mainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        sys.stdout = Signal()
        sys.stdout.text_update.connect(self.updatetext)

        # self.setWindowFlags(Qt.FramelessWindowHint)#隐藏窗口

        self.real_path = os.path.dirname(os.path.realpath(sys.argv[0]))

        self.video_clear.clicked.connect(self.clear_video_list)
        self.video_clearall.clicked.connect(self.clear_all_video_list)
        self.video_input.clicked.connect(self.input_video_list)

        self.select_of.clicked.connect(self.outfolder)

        self.save_config.clicked.connect(self.save_conf_Manual)
        self.load_config.clicked.connect(self.load_conf_Manual)

        self.pb_autorun.clicked.connect(self.auto_run)
        self.pb_debug.clicked.connect(self.debug_run)

        nvmlInit()
        deviceCount = nvmlDeviceGetCount()

        for i in range(deviceCount):
            handle = nvmlDeviceGetHandleByIndex(i)
            device = (str(i) + ":" + str(nvmlDeviceGetName(handle)))
            self.cb_gpu_sr.addItem(device)
            self.cb_gpu_vfi.addItem(device)

        self.load_conf_auto()#加载预设
        if ' ' in self.real_path:
            QMessageBox.information(self, "提示信息", "你的软件存放路径不符合规范，建议把软件存放到英文的路径下,不要有空格")

        for _char in self.real_path:
            if '\u4e00' <= _char <= '\u9fa5':
                QMessageBox.information(self, "提示信息", "你的软件存放路径不符合规范，建议把软件存放到英文的路径下,不要有空格")
                break

    def updatetext(self, text):
        """
            更新textBrowser
        """
        cursor = self.te_show.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.te_show.insertPlainText(text)
        self.te_show.setTextCursor(cursor)
        self.te_show.ensureCursorVisible()

    def clear_video_list(self):
        self.video_list.takeItem(self.video_list.row(self.video_list.currentItem()))
    def clear_all_video_list(self):
        self.video_list.clear()
    def input_video_list(self):
        files = QFileDialog.getOpenFileNames(self,
                                             "多文件选择",
                                             "./",
                                             "videos (*.mp4 *.mkv *.mov *.m2ts *.avi *.ts *.flv *.rmvb *.m4v)")
        valid_out_folder=True
        for file in files[0]:
            if ' ' in file:
                valid_out_folder=False
                break

        if valid_out_folder==True:
            for file in files[0]:
                self.video_list.addItem(file)
        else:
            QMessageBox.information(self, "提示信息", "视频文件名不能有空格字符，请重新选择。")

    def outfolder(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      "./")  # 起始路径
        valid_out_folder=True
        if ' ' in directory:
            valid_out_folder = False

        if valid_out_folder == True:
            self.out_folder.setText(directory)
        else:
            QMessageBox.information(self, "提示信息", "输出文件夹路径不能有空格字符，请重新选择。")

    def every_set(self):
        videos = []
        video_num = self.video_list.count()
        for i in range(video_num):
            videos.append(self.video_list.item(i).text())

        outfolder = self.out_folder.text()

        use_sr=self.rb_SR.isChecked()
        sr_gpu=self.cb_gpu_sr.currentText()
        sr_gpu_id=self.cb_gpu_sr.currentIndex()

        cugan_ml_device=self.cb_device_mlrt_cg.currentText()
        cugan_ml_half=self.rb_half_mlrt_cg.isChecked()
        cugan_ml_model=self.cb_model_mlrt_cg.currentText()
        cugan_ml_tile=self.cb_tile_mlrt_cg.currentText()
        cugan_ml_alpha=self.db_alpha_mlrt_cg.text()
        cugan_ml_set=cugan_ml_setting(cugan_ml_device,cugan_ml_half,cugan_ml_model,cugan_ml_tile,cugan_ml_alpha)

        esrgan_ml_device = self.cb_device_mlrt_eg.currentText()
        esrgan_ml_half = self.rb_half_mlrt_eg.isChecked()
        esrgan_ml_model=self.cb_model_mlrt_eg.currentText()
        esrgan_ml_tile=self.cb_tile_mlrt_eg.currentText()
        esrgan_ml_scale=self.cb_scale_mlrt_eg.currentText()
        esrgan_ml_set=esrgan_ml_setting(esrgan_ml_device,esrgan_ml_half,esrgan_ml_model,esrgan_ml_tile,esrgan_ml_scale)

        waifu_ml_device = self.cb_device_mlrt_wf.currentText()
        waifu_ml_half = self.rb_half_mlrt_wf.isChecked()
        waifu_ml_model=self.cb_model_mlrt_wf.currentText()
        waifu_ml_tile=self.cb_tile_mlrt_wf.currentText()
        waifu_ml_set=waifu2x_ml_setting(waifu_ml_device,waifu_ml_half,waifu_ml_model,waifu_ml_tile)

        vsrpp_model=self.cb_model_vsrpp.currentText()
        vsrpp_interval=self.sb_interval_vsrpp.text()
        vsrpp_half=self.rb_half_vsrpp.isChecked()
        vsrpp_set=vsrpp_setting(vsrpp_model,vsrpp_interval,vsrpp_half)

        vsr_model=self.cb_model_vsr.currentText()
        vsr_radius=self.sb_radius_vsr.text()
        vsr_hlaf=self.rb_half_vsr.isChecked()
        vsr_set=vsr_setting(vsr_model,vsr_radius,vsr_hlaf)

        esrgan_model=self.cb_model_eg.currentText()
        esrgan_tile=self.cb_tile_eg.currentText()
        esrgan_set=esrgan_setting(esrgan_model,esrgan_tile)

        esrgantrt_model=self.cb_model_egtrt.currentText()
        esrgantrt_set=esrgantrt_setting(esrgantrt_model)

        animesr_model=self.cb_model_as.currentText()
        animesr_set=animesr_setting(animesr_model)


        animesrtrt_model=self.cb_model_astrt.currentText()
        animesrtrt_set=animesrtrt_setting(animesrtrt_model)


        sr_set=cugan_ml_set
        sr_method = self.cb_SR.currentText()#算法名称
        if sr_method == 'Real_cugan_mlrt':
            sr_set = cugan_ml_set
        elif sr_method == 'Real_esrgan_mlrt':
            sr_set = esrgan_ml_set
        elif sr_method == 'Waifu2x_mlrt':
            sr_set = waifu_ml_set
        elif sr_method == 'Basicvsrpp':
            sr_set = vsrpp_set
        elif sr_method == 'Basicvsr':
            sr_set = vsr_set
        elif sr_method == 'Real_esrgan':
            sr_set = esrgan_set
        elif sr_method == 'Real_esrgan_trt':
            sr_set = esrgantrt_set
        elif sr_method == 'AnimeSR':
            sr_set = animesr_set
        elif sr_method == 'AnimeSR_trt':
            sr_set = animesrtrt_set

        use_vfi=self.rb_VFI.isChecked()
        vfi_gpu=self.cb_gpu_vfi.currentText()
        vfi_gpu_id=self.cb_gpu_vfi.currentIndex()

        rife_ml_device=self.cb_device_mlrt_rife.currentText()
        rife_ml_half=self.rb_half_mlrt_rife.isChecked()
        rife_ml_model=self.cb_model_mlrt_rife.currentText()
        rife_ml_cscale=self.sb_cscale_mlrt_rife.text()
        rife_ml_scale=self.cb_scale_mlrt_rife.currentText()
        rife_ml_set=rife_ml_setting(rife_ml_device,rife_ml_half,rife_ml_model,rife_ml_cscale,rife_ml_scale)

        rife_model=self.cb_model_rife.currentText()
        usecs_rife=self.rb_usecs_rife.isChecked()
        usec_rife=self.rb_usec_rife.isChecked()
        cscale_rife=self.sb_cscale_rife.text()
        c_rife=self.sb_c_rife.text()
        scale_rife=self.cb_scale_rife.currentText()
        sct_rife=self.db_sct_rife.text()
        use_smooth_rife=self.rb_smooth_rife.isChecked()
        rife_set=rife_setting(rife_model,usecs_rife,usec_rife,cscale_rife,c_rife,scale_rife,sct_rife,use_smooth_rife)

        rifetrt_model=self.cb_model_rifetrt.currentText()
        usecs_rifetrt = self.rb_usecs_rifetrt.isChecked()
        usec_rifetrt = self.rb_usec_rifetrt.isChecked()
        cscale_rifetrt = self.sb_cscale_rifetrt.text()
        c_rifetrt = self.sb_c_rifetrt.text()
        scale_rifetrt = self.cb_scale_rifetrt.currentText()
        sct_rifetrt = self.db_sct_rifetrt.text()
        use_smooth_rifetrt = self.rb_smooth_rifetrt.isChecked()
        rifetrt_set=rifetrt_setting(rifetrt_model,usecs_rifetrt,usec_rifetrt,cscale_rifetrt,c_rifetrt,scale_rifetrt,sct_rifetrt,use_smooth_rifetrt)


        rifenc_model=self.cb_model_rifenc.currentText()
        usecs_rifenc = self.rb_usecs_rifenc.isChecked()
        usec_rifenc = self.rb_usec_rifenc.isChecked()
        cscale_rifenc = self.sb_cscale_rifenc.text()
        c_rifenc = self.sb_c_rifenc.text()
        skip_rifenc=self.rb_skip_rifenc.isChecked()
        tta_rifenc=self.rb_tta_rifenc.isChecked()
        uhd_rifenc=self.rb_uhd_rifenc.isChecked()
        static_rifenc=self.sb_static_rifenc.text()
        rifenc_set=rifenc_setting(rifenc_model,usecs_rifenc,usec_rifenc,cscale_rifenc,c_rifenc,skip_rifenc,tta_rifenc,uhd_rifenc,static_rifenc)

        gmf_model=self.cb_model_gmfss.currentText()
        usecs_gmf = self.rb_usecs_gmfss.isChecked()
        usec_gmf = self.rb_usec_gmfss.isChecked()
        cscale_gmf = self.sb_cscale_gmfss.text()
        c_gmf = self.sb_c_gmfss.text()
        scale_gmf = self.cb_scale_gmfss.currentText()
        sct_gmf = self.db_sct_gmfss.text()
        use_smooth_gmf = self.rb_smooth_gmfss.isChecked()
        gmf_set=gmfss_setting(gmf_model,usecs_gmf,usec_gmf,cscale_gmf,c_gmf,scale_gmf,sct_gmf,use_smooth_gmf)

        gmftrt_model=self.cb_model_gmfsstrt.currentText()
        usecs_gmftrt = self.rb_usecs_gmfsstrt.isChecked()
        usec_gmftrt = self.rb_usec_gmfsstrt.isChecked()
        cscale_gmftrt = self.sb_cscale_gmfsstrt.text()
        c_gmftrt = self.sb_c_gmfsstrt.text()
        scale_gmftrt = self.cb_scale_gmfsstrt.currentText()
        sct_gmftrt = self.db_sct_gmfsstrt.text()
        use_smooth_gmftrt = self.rb_smooth_gmfsstrt.isChecked()
        gmftrt_set=gmfsstrt_setting(gmftrt_model,usecs_gmftrt,usec_gmftrt,cscale_gmftrt,c_gmftrt,scale_gmftrt,sct_gmftrt,use_smooth_gmftrt)

        vfi_set = rife_ml_set
        vfi_method = self.cb_VFI.currentText()
        if vfi_method == 'rife_mlrt':
            vfi_set = rife_ml_set
        elif vfi_method == 'rife':
            vfi_set = rife_set
        elif vfi_method == 'rife_ncnn':
            vfi_set = rifenc_set
        elif vfi_method == 'rife_trt':
            vfi_set = rifetrt_set
        elif vfi_method == 'gmfss':
            vfi_set = gmf_set
        elif vfi_method == 'gmfss_trt':
            vfi_set = gmftrt_set

        use_qtgmc=self.rb_qtgmc.isChecked()
        use_deband=self.rb_deband.isChecked()
        use_taa=self.rb_taa.isChecked()

        is_rs_bef=self.rb_resize_bef.isChecked()

        is_rs_aft=self.rb_resize_aft.isChecked()

        rs_bef_w=self.sb_rsbef_w.text()
        rs_bef_h=self.sb_rsbef_h.text()
        rs_aft_w=self.sb_rsaft_w.text()
        rs_aft_h=self.sb_rsaft_h.text()
        #encode setting
        encoder=self.cb_encode.currentText()
        preset=self.cb_preset.currentText()
        eformat=self.cb_eformat.currentText()
        vformat=self.cb_vformat.currentText()
        use_crf=self.rb_crf.isChecked()
        use_bit=self.rb_bit.isChecked()
        crf=self.sb_crf.text()
        bit=self.sb_bit.text()
        use_encode_audio=self.rb_audio.isChecked()
        use_source_audio=self.rb_save_source_audio.isChecked()
        audio_format=self.cb_aformat.currentText()
        customization_encode=self.te_customization_encode.toPlainText()
        use_customization_encode=self.rb_customization_encode.isChecked()

        return every_set_object(videos,outfolder,
                                use_sr,sr_gpu,sr_gpu_id,sr_method,sr_set,use_vfi,vfi_gpu,vfi_gpu_id,vfi_method,vfi_set,use_qtgmc,use_deband,use_taa,is_rs_bef,is_rs_aft,rs_bef_w,rs_bef_h,rs_aft_w,rs_aft_h,
                                encoder,preset,eformat,vformat,use_crf,use_bit,crf,bit,use_encode_audio,use_source_audio,audio_format,customization_encode,use_customization_encode)

    def save_conf_set(self):
        conf = ConfigParser()
        every_setting = self.every_set()

        conf.add_section('sr')
        conf.set('sr', 'use_sr', str(every_setting.use_sr))
        conf.set('sr', 'sr_gpu', str(every_setting.sr_gpu))
        conf.set('sr', 'sr_gpu_id', str(every_setting.sr_gpu_id))

        conf.set('sr', 'sr_method', str(every_setting.sr_method))

        if every_setting.sr_method == 'Real_cugan_mlrt':
            conf.set('sr', 'device', str(every_setting.sr_set.device))
            conf.set('sr', 'half', str(every_setting.sr_set.half))
            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'tile', str(every_setting.sr_set.tile))
            conf.set('sr', 'alpha', str(every_setting.sr_set.alpha))
        elif every_setting.sr_method == 'Real_esrgan_mlrt':
            conf.set('sr', 'device', str(every_setting.sr_set.device))
            conf.set('sr', 'half', str(every_setting.sr_set.half))
            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'tile', str(every_setting.sr_set.tile))
            conf.set('sr', 'scale', str(every_setting.sr_set.scale))
        elif every_setting.sr_method == 'Waifu2x_mlrt':
            conf.set('sr', 'device', str(every_setting.sr_set.device))
            conf.set('sr', 'half', str(every_setting.sr_set.half))
            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'tile', str(every_setting.sr_set.tile))
        elif every_setting.sr_method == 'Basicvsrpp':
            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'interval', str(every_setting.sr_set.interval))
        elif every_setting.sr_method == 'Basicvsr':
            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'radius', str(every_setting.sr_set.radius))
        elif every_setting.sr_method == 'Real_esrgan':
            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'tile', str(every_setting.sr_set.tile))
        elif every_setting.sr_method == 'Real_esrgan_trt':
            conf.set('sr', 'model', str(every_setting.sr_set.model))
        elif every_setting.sr_method == 'AnimeSR':
            conf.set('sr', 'model', str(every_setting.sr_set.model))
        elif every_setting.sr_method == 'AnimeSR_trt':
            conf.set('sr', 'model', str(every_setting.sr_set.model))

        conf.add_section('vfi')
        conf.set('vfi', 'use_vfi', str(every_setting.use_vfi))
        conf.set('vfi', 'vfi_gpu', str(every_setting.vfi_gpu))
        conf.set('vfi', 'vfi_gpu_id', str(every_setting.vfi_gpu_id))

        conf.set('vfi', 'vfi_method', str(every_setting.vfi_method))

        if every_setting.vfi_method == 'rife_mlrt':
            conf.set('vfi', 'model', str(every_setting.vfi_set.model))
            conf.set('vfi', 'device', str(every_setting.vfi_set.device))
            conf.set('vfi', 'half', str(every_setting.vfi_set.half))
            conf.set('vfi', 'cscale', str(every_setting.vfi_set.cscale))
            conf.set('vfi', 'scale', str(every_setting.vfi_set.scale))
        elif every_setting.vfi_method == 'rife':
            conf.set('vfi', 'model', str(every_setting.vfi_set.model))
            conf.set('vfi', 'usecs', str(every_setting.vfi_set.usecs))
            conf.set('vfi', 'usec', str(every_setting.vfi_set.usec))
            conf.set('vfi', 'cscale', str(every_setting.vfi_set.cscale))
            conf.set('vfi', 'clips', str(every_setting.vfi_set.clips))
            conf.set('vfi', 'scale', str(every_setting.vfi_set.scale))
            conf.set('vfi', 'sct', str(every_setting.vfi_set.sct))
            conf.set('vfi', 'smooth', str(every_setting.vfi_set.use_smooth))
        elif every_setting.vfi_method == 'rife_trt':
            conf.set('vfi', 'model', str(every_setting.vfi_set.model))
            conf.set('vfi', 'usecs', str(every_setting.vfi_set.usecs))
            conf.set('vfi', 'usec', str(every_setting.vfi_set.usec))
            conf.set('vfi', 'cscale', str(every_setting.vfi_set.cscale))
            conf.set('vfi', 'clips', str(every_setting.vfi_set.clips))
            conf.set('vfi', 'scale', str(every_setting.vfi_set.scale))
            conf.set('vfi', 'sct', str(every_setting.vfi_set.sct))
            conf.set('vfi', 'smooth', str(every_setting.vfi_set.use_smooth))
        elif every_setting.vfi_method == 'rife_ncnn':
            conf.set('vfi', 'model', str(every_setting.vfi_set.model))
            conf.set('vfi', 'usecs', str(every_setting.vfi_set.usecs))
            conf.set('vfi', 'usec', str(every_setting.vfi_set.usec))
            conf.set('vfi', 'cscale', str(every_setting.vfi_set.cscale))
            conf.set('vfi', 'clips', str(every_setting.vfi_set.clips))
            conf.set('vfi', 'skip', str(every_setting.vfi_set.skip))
            conf.set('vfi', 'tta', str(every_setting.vfi_set.tta))
            conf.set('vfi', 'uhd', str(every_setting.vfi_set.uhd))
            conf.set('vfi', 'static', str(every_setting.vfi_set.static))
        elif every_setting.vfi_method == 'gmfss':
            conf.set('vfi', 'model', str(every_setting.vfi_set.model))
            conf.set('vfi', 'usecs', str(every_setting.vfi_set.usecs))
            conf.set('vfi', 'usec', str(every_setting.vfi_set.usec))
            conf.set('vfi', 'cscale', str(every_setting.vfi_set.cscale))
            conf.set('vfi', 'clips', str(every_setting.vfi_set.clips))
            conf.set('vfi', 'scale', str(every_setting.vfi_set.scale))
            conf.set('vfi', 'sct', str(every_setting.vfi_set.sct))
            conf.set('vfi', 'smooth', str(every_setting.vfi_set.use_smooth))
        elif every_setting.vfi_method == 'gmfss_trt':
            conf.set('vfi', 'model', str(every_setting.vfi_set.model))
            conf.set('vfi', 'usecs', str(every_setting.vfi_set.usecs))
            conf.set('vfi', 'usec', str(every_setting.vfi_set.usec))
            conf.set('vfi', 'cscale', str(every_setting.vfi_set.cscale))
            conf.set('vfi', 'clips', str(every_setting.vfi_set.clips))
            conf.set('vfi', 'scale', str(every_setting.vfi_set.scale))
            conf.set('vfi', 'sct', str(every_setting.vfi_set.sct))
            conf.set('vfi', 'smooth', str(every_setting.vfi_set.use_smooth))


        conf.add_section('fix')
        conf.set('fix', 'use_qtgmc ', str(every_setting.use_qtgmc))
        conf.set('fix', 'use_deband', str(every_setting.use_deband))
        conf.set('fix', 'use_taa', str(every_setting.use_taa))
        conf.set('fix', 'is_rs_bef ', str(every_setting.is_rs_bef))
        conf.set('fix', 'is_rs_aft', str(every_setting.is_rs_aft))
        conf.set('fix', 'rs_bef_w', str(every_setting.rs_bef_w))
        conf.set('fix', 'rs_bef_h', str(every_setting.rs_bef_h))
        conf.set('fix', 'rs_aft_w', str(every_setting.rs_aft_w))
        conf.set('fix', 'rs_aft_h', str(every_setting.rs_aft_h))

        conf.add_section('encode')
        conf.set('encode', 'encoder', str(every_setting.encoder))
        conf.set('encode', 'preset', str(every_setting.preset))
        conf.set('encode', 'eformat', str(every_setting.eformat))
        conf.set('encode', 'vformat', str(every_setting.vformat))
        conf.set('encode', 'use_crf', str(every_setting.use_crf))
        conf.set('encode', 'use_bit', str(every_setting.use_bit))
        conf.set('encode', 'crf', str(every_setting.crf))
        conf.set('encode', 'bit', str(every_setting.bit))
        conf.set('encode', 'use_encode_audio', str(every_setting.use_encode_audio))
        conf.set('encode', 'use_source_audio', str(every_setting.use_source_audio))
        conf.set('encode', 'audio_format', str(every_setting.audio_format))
        conf.set('encode', 'customization_encode', str(every_setting.customization_encode))
        conf.set('encode', 'use_customization_encode', str(every_setting.use_customization_encode))

        conf.add_section('else_set')
        conf.set('else_set', 'out_folder', str(every_setting.outfolder))
        conf.set('else_set', 'videos', str(every_setting.videos))
        return conf

    def load_conf_set(self,conf):

        self.rb_SR.setChecked(conf['sr'].getboolean('use_sr'))
        self.cb_SR.setCurrentText(conf['sr']['sr_method'])

        if conf['sr']['sr_method'] == 'Real_cugan_mlrt':
            self.cb_device_mlrt_cg.setCurrentText(conf['sr']['device'])
            self.rb_half_mlrt_cg.setChecked(conf['sr'].getboolean('half'))
            self.cb_model_mlrt_cg.setCurrentText(conf['sr']['model'])
            self.cb_tile_mlrt_cg.setCurrentText(conf['sr']['tile'])
            self.db_alpha_mlrt_cg.setValue(conf['sr'].getfloat('alpha'))

        elif conf['sr']['sr_method'] == 'Real_esrgan_mlrt':
            self.cb_device_mlrt_eg.setCurrentText(conf['sr']['device'])
            self.rb_half_mlrt_eg.setChecked(conf['sr'].getboolean('half'))
            self.cb_model_mlrt_eg.setCurrentText(conf['sr']['model'])
            self.cb_tile_mlrt_eg.setCurrentText(conf['sr']['tile'])
            self.cb_scale_mlrt_eg.setCurrentText(conf['sr']['scale'])

        elif conf['sr']['sr_method'] == 'Waifu2x_mlrt':
            self.cb_device_mlrt_wf.setCurrentText(conf['sr']['device'])
            self.rb_half_mlrt_wf.setChecked(conf['sr'].getboolean('half'))
            self.cb_model_mlrt_wf.setCurrentText(conf['sr']['model'])
            self.cb_tile_mlrt_wf.setCurrentText(conf['sr']['tile'])

        elif conf['sr']['sr_method'] == 'Basicvsrpp':
            self.cb_model_vsrpp.setCurrentText(conf['sr']['model'])
            self.sb_interval_vsrpp.setValue(conf['sr'].getint('interval'))

        elif conf['sr']['sr_method'] == 'Basicvsr':
            self.cb_model_vsr.setCurrentText(conf['sr']['model'])
            self.sb_radius_vsr.setValue(conf['sr'].getint('radius'))

        elif conf['sr']['sr_method'] == 'Real_esrgan':
            self.cb_model_eg.setCurrentText(conf['sr']['model'])
            self.cb_tile_eg.setCurrentText(conf['sr']['tile'])

        elif conf['sr']['sr_method'] == 'Real_esrgan_trt':
            self.cb_model_egtrt.setCurrentText(conf['sr']['model'])

        elif conf['sr']['sr_method'] == 'AnimeSR':
            self.cb_model_as.setCurrentText(conf['sr']['model'])

        elif conf['sr']['sr_method'] == 'AnimeSR_trt':
            self.cb_model_astrt.setCurrentText(conf['sr']['model'])

        self.rb_VFI.setChecked(conf['vfi'].getboolean('use_vfi'))
        self.cb_VFI.setCurrentText(conf['vfi']['vfi_method'])

        if conf['vfi']['vfi_method'] == 'rife_mlrt':
            self.cb_model_mlrt_rife.setCurrentText(conf['vfi']['model'])
            self.cb_device_mlrt_rife.setCurrentText(conf['vfi']['device'])
            self.rb_half_mlrt_rife.setChecked(conf['vfi'].getboolean('half'))
            self.sb_cscale_mlrt_rife.setValue(conf['vfi'].getint('cscale'))
            self.cb_scale_mlrt_rife.setCurrentText(conf['vfi']['scale'])

        elif conf['vfi']['vfi_method'] == 'rife':
            self.cb_model_rife.setCurrentText(conf['vfi']['model'])
            self.rb_usecs_rife.setChecked(conf['vfi'].getboolean('usecs'))
            self.rb_usec_rife.setChecked(conf['vfi'].getboolean('usec'))
            self.sb_cscale_rife.setValue(conf['vfi'].getint('cscale'))
            self.sb_c_rife.setValue(conf['vfi'].getint('clips'))
            self.cb_scale_rife.setCurrentText(conf['vfi']['scale'])
            self.db_sct_rife.setValue(conf['vfi'].getfloat('sct'))
            self.rb_smooth_rife.setChecked(conf['vfi'].getboolean('smooth'))

        elif conf['vfi']['vfi_method'] == 'rife_trt':
            self.cb_model_rifetrt.setCurrentText(conf['vfi']['model'])
            self.rb_usecs_rifetrt.setChecked(conf['vfi'].getboolean('usecs'))
            self.rb_usec_rifetrt.setChecked(conf['vfi'].getboolean('usec'))
            self.sb_cscale_rifetrt.setValue(conf['vfi'].getint('cscale'))
            self.sb_c_rifetrt.setValue(conf['vfi'].getint('clips'))
            self.cb_scale_rifetrt.setCurrentText(conf['vfi']['scale'])
            self.db_sct_rifetrt.setValue(conf['vfi'].getfloat('sct'))
            self.rb_smooth_rifetrt.setChecked(conf['vfi'].getboolean('smooth'))

        elif conf['vfi']['vfi_method'] == 'rife_ncnn':
            self.cb_model_rifenc.setCurrentText(conf['vfi']['model'])
            self.rb_usecs_rifenc.setChecked(conf['vfi'].getboolean('usecs'))
            self.rb_usec_rifenc.setChecked(conf['vfi'].getboolean('usec'))
            self.sb_cscale_rifenc.setValue(conf['vfi'].getint('cscale'))
            self.sb_c_rifenc.setValue(conf['vfi'].getint('clips'))
            self.rb_skip_rifenc.setChecked(conf['vfi'].getboolean('skip'))
            self.rb_tta_rifenc.setChecked(conf['vfi'].getboolean('tta'))
            self.rb_uhd_rifenc.setChecked(conf['vfi'].getboolean('uhd'))
            self.sb_static_rifenc.setValue(conf['vfi'].getint('static'))

        elif conf['vfi']['vfi_method'] == 'gmfss':
            self.cb_model_gmfss.setCurrentText(conf['vfi']['model'])
            self.rb_usecs_gmfss.setChecked(conf['vfi'].getboolean('usecs'))
            self.rb_usec_gmfss.setChecked(conf['vfi'].getboolean('usec'))
            self.sb_cscale_gmfss.setValue(conf['vfi'].getint('cscale'))
            self.sb_c_gmfss.setValue(conf['vfi'].getint('clips'))
            self.cb_scale_gmfss.setCurrentText(conf['vfi']['scale'])
            self.db_sct_gmfss.setValue(conf['vfi'].getfloat('sct'))
            self.rb_smooth_gmfss.setChecked(conf['vfi'].getboolean('smooth'))

        elif conf['vfi']['vfi_method'] == 'gmfss_trt':
            self.cb_model_gmfsstrt.setCurrentText(conf['vfi']['model'])
            self.rb_usecs_gmfsstrt.setChecked(conf['vfi'].getboolean('usecs'))
            self.rb_usec_gmfsstrt.setChecked(conf['vfi'].getboolean('usec'))
            self.sb_cscale_gmfsstrt.setValue(conf['vfi'].getint('cscale'))
            self.sb_c_gmfsstrt.setValue(conf['vfi'].getint('clips'))
            self.cb_scale_gmfsstrt.setCurrentText(conf['vfi']['scale'])
            self.db_sct_gmfsstrt.setValue(conf['vfi'].getfloat('sct'))
            self.rb_smooth_gmfsstrt.setChecked(conf['vfi'].getboolean('smooth'))

        self.rb_qtgmc.setChecked(conf['fix'].getboolean('use_qtgmc'))
        self.rb_deband.setChecked(conf['fix'].getboolean('use_deband'))
        self.rb_taa.setChecked(conf['fix'].getboolean('use_taa'))
        self.rb_resize_bef.setChecked(conf['fix'].getboolean('is_rs_bef'))
        self.rb_resize_aft.setChecked(conf['fix'].getboolean('is_rs_aft'))
        self.sb_rsbef_w.setValue(conf['fix'].getint('rs_bef_w'))
        self.sb_rsbef_h.setValue(conf['fix'].getint('rs_bef_h'))
        self.sb_rsaft_w.setValue(conf['fix'].getint('rs_aft_w'))
        self.sb_rsaft_h.setValue(conf['fix'].getint('rs_aft_h'))

        self.cb_encode.setCurrentText(conf['encode']['encoder'])
        self.cb_eformat.setCurrentText(conf['encode']['eformat'])
        self.cb_preset.setCurrentText(conf['encode']['preset'])
        self.cb_vformat.setCurrentText(conf['encode']['vformat'])

        self.rb_bit.setChecked(conf['encode'].getboolean('use_bit'))
        self.rb_crf.setChecked(conf['encode'].getboolean('use_crf'))
        self.sb_bit.setValue(conf['encode'].getint('bit'))
        self.sb_crf.setValue(conf['encode'].getint('crf'))

        self.rb_audio.setChecked(conf['encode'].getboolean('use_encode_audio'))
        self.rb_save_source_audio.setChecked(conf['encode'].getboolean('use_source_audio'))
        self.cb_aformat.setCurrentText(conf['encode']['audio_format'])

        self.rb_customization_encode.setChecked(conf['encode'].getboolean('use_customization_encode'))
        self.te_customization_encode.setText(conf['encode']['customization_encode'])

    def save_conf_Manual(self):
        self.save_config.setEnabled(False)
        self.save_config.setText('保存ing')

        with open(self.real_path+'/config.ini', 'w', encoding='utf-8') as f:
            (self.save_conf_set()).write(f)

        QMessageBox.information(self, "提示信息", "已保存当前自定义预设")
        self.save_config.setEnabled(True)
        self.save_config.setText('保存预设')#conf['url']['smms_pic_url']

    def load_conf_Manual(self):
        self.load_config.setEnabled(False)
        self.load_config.setText('加载ing')
        if not os.path.exists(self.real_path+"/config.ini"):
            QMessageBox.information(self, "提示信息", "自定义预设文件不存在")
        else:
            conf = ConfigParser()
            conf.read(self.real_path+"/config.ini", encoding="utf-8")
            self.load_conf_set(conf)
            print("已加载保存的自定义预设")

        self.load_config.setEnabled(True)
        self.load_config.setText('加载预设')

    def save_conf_auto(self):
        with open(self.real_path+'/config_auto.ini', 'w', encoding='utf-8') as f:
            (self.save_conf_set()).write(f)
        print("已自动保存当前设置，下次启动软件时自动加载")

    def load_conf_auto(self):
        if os.path.exists(self.real_path+"/config_auto.ini"):
            conf = ConfigParser()
            conf.read(self.real_path+"/config_auto.ini", encoding="utf-8")
            self.load_conf_set(conf)
            print("已自动加载上一次软件运行设置")

    def closeEvent(self, event):
        self.save_conf_auto()
        super().closeEvent(event)

    def auto_run(self):
        self.pb_autorun.setEnabled(False)
        self.pb_autorun.setText('渲染压制ing')

        self.pb_debug.setEnabled(False)
        self.pb_debug.setText('Debug模式')

        every_setting=self.every_set()
        allow_autorun=True

        if every_setting.use_sr == True and every_setting.use_vfi == True:
            if 'mlrt' in every_setting.sr_method and 'mlrt' not in every_setting.vfi_method:
                allow_autorun = False
                QMessageBox.information(self, "提示信息", "vsmlrt的运行库不能vsmlrt以外的运行库混用")
            if 'mlrt' not in every_setting.sr_method and 'mlrt' in every_setting.vfi_method:
                allow_autorun = False
                QMessageBox.information(self, "提示信息", "vsmlrt的运行库不能vsmlrt以外的运行库混用")

        if every_setting.use_sr == False and every_setting.use_vfi == False:
            allow_autorun = False
            QMessageBox.information(self, "提示信息", "请至少开启超分或补帧一个渲染流程")

        if every_setting.outfolder == '':
            allow_autorun=False
            QMessageBox.information(self, "提示信息", "输出文件夹为空，请选择输出文件夹")

        for _char in every_setting.videos:
            if ' ' in _char:
                allow_autorun = False
                QMessageBox.information(self, "提示信息", "输入视频文件不能含有空格，请规范文件名")
                break

        if allow_autorun == True:
            self.autorun_Thread = autorun(every_setting, 'start')
            self.autorun_Thread.signal.connect(self.set_btn_auto_run)
            self.autorun_Thread.start()
        else:
            self.pb_autorun.setEnabled(True)
            self.pb_debug.setEnabled(True)
            self.pb_autorun.setText('一键启动模式')

    def debug_run(self):
        self.pb_autorun.setEnabled(False)
        self.pb_autorun.setText('一键启动模式')

        self.pb_debug.setEnabled(False)
        self.pb_debug.setText('Debug运行ing')

        every_setting=self.every_set()
        allow_debug=True

        if every_setting.use_sr == True and every_setting.use_vfi == True:
            if 'mlrt' in every_setting.sr_method and 'mlrt' not in every_setting.vfi_method:
                allow_debug = False
                QMessageBox.information(self, "提示信息", "vsmlrt的运行库不能vsmlrt以外的运行库混用")
            if 'mlrt' not in every_setting.sr_method and 'mlrt' in every_setting.vfi_method:
                allow_debug = False
                QMessageBox.information(self, "提示信息", "vsmlrt的运行库不能vsmlrt以外的运行库混用")

        if every_setting.use_sr == False and every_setting.use_vfi == False:
            allow_debug = False
            QMessageBox.information(self, "提示信息", "请至少开启超分或补帧一个渲染流程")

        if every_setting.outfolder == '':
            allow_debug=False
            QMessageBox.information(self, "提示信息", "输出文件夹为空，请选择输出文件夹")

        for _char in every_setting.videos:
            if ' ' in _char:
                allow_debug = False
                QMessageBox.information(self, "提示信息", "输入视频文件不能含有空格，请规范文件名")
                break

        if allow_debug == True:
            self.debugrun_Thread = autorun(every_setting, 'debug')
            self.debugrun_Thread.signal.connect(self.set_btn_auto_run)
            self.debugrun_Thread.start()
        else:
            self.pb_autorun.setEnabled(True)
            self.pb_autorun.setText('一键启动模式')
            self.pb_debug.setEnabled(True)
            self.pb_debug.setText('Debug模式')

    def set_btn_auto_run(self):#一键运行开关控制
        self.pb_autorun.setEnabled(True)
        self.pb_autorun.setText('一键启动模式')
        self.pb_debug.setEnabled(True)
        self.pb_debug.setText('Debug模式')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('logo.png'))
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())