import sys
import os
import subprocess as sp
import json
import time
from configparser import ConfigParser

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
                [self.directory + '/vs_pytorch/ffprobe', '-i', self.filepath, '-print_format', 'json', '-show_format',
                 '-show_streams', '-v',
                 'quiet'], shell=True)
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
            color_space = stream[0]['color_space']
        else:
            color_space = 2
        if 'color_transfer' in stream[0]:
            color_transfer = stream[0]['color_transfer']
        else:
            color_transfer = 2
        if 'color_primaries' in stream[0]:
            color_primaries = stream[0]['color_primaries']
        else:
            color_primaries = 2

        item = {
            'color_space': color_space,
            'color_transfer': color_transfer,
            'color_primaries': color_primaries
        }
        return item


class Signal(QObject):
    text_update = pyqtSignal(str)

    def write(self, text):
        self.text_update.emit(str(text))
        QApplication.processEvents()

    def flush(self):
        pass


class cugan_setting(QObject):
    def __init__(self, model, tile, alpha):
        self.model = model
        self.tile = tile
        self.alpha = alpha

    def return_model(self):
        return self.model

    def return_tile(self):
        return self.tile

    def return_alpha(self):
        return self.alpha


class esrgan_setting(QObject):
    def __init__(self, model, tile, scale):
        self.model = model
        self.tile = tile
        self.scale = scale

    def return_model(self):
        return self.model

    def return_tile(self):
        return self.tile

    def return_scale(self):
        return self.scale


class waifu2x_setting(QObject):
    def __init__(self, model, tile):
        self.model = model
        self.tile = tile

    def return_model(self):
        return self.model

    def return_tile(self):
        return self.tile


class vsrpp_setting(QObject):
    def __init__(self, model, interval):
        self.model = model
        self.interval = interval

    def return_model(self):
        return self.model

    def return_interval(self):
        return self.interval


class every_set_object(QObject):
    def __init__(self, videos, outfolder,
                 device, gpu_id, half, sr_method, sr_set, is_rs_bef, is_rs_aft, rs_bef_w, rs_bef_h, rs_aft_w, rs_aft_h,
                 encoder, preset, eformat, vformat, use_crf, use_bit, crf, bit, use_encode_audio, use_source_audio,
                 audio_format, customization_encode, use_customization_encode):
        self.videos = videos
        self.outfolder = outfolder

        self.device = device
        self.gpu_id = gpu_id
        self.half = half
        self.sr_method = sr_method
        self.sr_set = sr_set
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
        self.every_setting = every_setting
        self.run_mode = run_mode
        self.directory = os.path.dirname(os.path.realpath(sys.argv[0]))

    def cugan_(self):
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
            'up4x-latest-no-denoise': [-1, 4, 1],
        }
        noise, scale, version = model_switch[self.every_setting.sr_set.model] \
            if self.every_setting.sr_set.model in model_switch else [0, 2, 2]

        return ('res = CUGAN(res, noise=' + str(noise) + ', scale=' + str(scale) + ', tiles=' + str(
            self.every_setting.sr_set.tile) + ',version=' + str(version) + ',alpha=' + str(
            self.every_setting.sr_set.alpha) + ', backend=device)\n')

    def esrgan_(self):
        model_switch = {
            'animevideov3': 0,
            'animevideo-xsx2': 1,
            'animevideo-xsx4': 2
        }
        model = model_switch[self.every_setting.sr_set.model] \
            if self.every_setting.sr_set.model in model_switch else 0
        return ('res = RealESRGAN(res, scale=' + str(self.every_setting.sr_set.scale) + ',tiles=' + str(
            self.every_setting.sr_set.tile) + ',model=' + str(model) + ', backend=device)\n')

    def waifu2x_(self):
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
        }
        noise, scale, model = model_switch[self.every_setting.sr_set.model] \
            if self.every_setting.sr_set.model in model_switch else [1, 1, 1]

        return ('res = Waifu2x(res, noise=' + str(noise) + ',scale=' + str(scale) + ',tiles=' + str(
            self.every_setting.sr_set.tile) + ',model=' + str(model) + ', backend=device)\n')

    def vsrpp_(self):
        model_switch = {
            'reds4': 0,
            'vimeo90k_bi': 1,
            'vimeo90k_bd': 2,
            'ntire_decompress_track1': 3,
            'ntire_decompress_track2': 4,
            'ntire_decompress_track3': 5
        }
        model = model_switch[self.every_setting.sr_set.model] \
            if self.every_setting.sr_set.model in model_switch else 0

        return ('res = BasicVSRPP(res,model=' + str(model) + ',interval=' + str(
            self.every_setting.sr_set.interval) + ',device_index=' + str(self.every_setting.gpu_id) + ',fp16=' + str(
            self.every_setting.half) + ')\n')

    def ffmpeg_(self):
        ffmpeg_set = []
        if self.every_setting.use_customization_encode == True:
            ffmpeg_set_customizatio = str(self.every_setting.customization_encode)
            for str_ in ffmpeg_set_customizatio.split():
                ffmpeg_set.append(str_)
        else:
            if self.every_setting.encoder == 'cpu(i)' and self.every_setting.eformat == 'H265':
                ffmpeg_set.append('-c:v')
                ffmpeg_set.append('libx265')
                ffmpeg_set.append('-pix_fmt')
                ffmpeg_set.append('yuv420p10le')
                ffmpeg_set.append('-profile:v')
                ffmpeg_set.append('main10')
            elif self.every_setting.encoder == 'cpu(i)' and self.every_setting.eformat == 'H264':
                ffmpeg_set.append('-c:v')
                ffmpeg_set.append('libx264')
                ffmpeg_set.append('-pix_fmt')
                ffmpeg_set.append('yuv420p')
                ffmpeg_set.append('-profile:v')
                ffmpeg_set.append('main')
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

        return ffmpeg_set

    def run(self):

        vpy_folder = self.every_setting.outfolder + '/vpys'
        if self.run_mode == 'debug':
            bat_file = open(self.every_setting.outfolder + '/run.bat', 'w', encoding='ansi')
        if not os.path.exists(vpy_folder):
            os.makedirs(vpy_folder)  # 存放配置文件vpy的文件夹
        video_folder = self.every_setting.outfolder + '/out_videos'
        if not os.path.exists(video_folder):
            os.makedirs(video_folder)

        use_device_switch = {
            'GPU_nvidia': 'ORT_CUDA()',
            'GPU_nvidia_trt': 'TRT()',
            'GPU_amd': 'OV_GPU()',
            'NCNN': 'NCNN_VK()'
        }
        use_device = use_device_switch[self.every_setting.device] \
            if self.every_setting.device in use_device_switch else 'ORT_CUDA()'
        # 实测路径
        # FFMPEG_BIN=self.directory + '\\vapoursynth\\ffmpeg.exe'
        # 测试路径
        # FFMPEG_BIN = 'ffmpeg.exe'
        num = 1
        for video in self.every_setting.videos:
            print('正在运行队列中第' + str(num) + '个视频')

            ffmpeg_code = self.ffmpeg_()
            ffprobe = FFprobe()
            ffprobe.parse(video)

            video_name = (video.rsplit("/", 1))[-1]
            video_name = (video_name.rsplit(".", 1))[0]  # 只保留文件名的参数

            # 色彩处理
            color_info = []
            v_info = ffprobe.video_info()
            if v_info['color_space'] != 2:
                color_info.append('-vf')
                color_info.append('scale=out_color_matrix=' + v_info['color_space'])
                color_info.append('-colorspace')
                color_info.append(v_info['color_space'])

            if v_info['color_transfer'] != 2:
                color_info.append('-color_trc')
                color_info.append(v_info['color_transfer'])

            if v_info['color_primaries'] != 2:
                color_info.append('-color_primaries')
                color_info.append(v_info['color_primaries'])

            # 音频处理
            audio_info = []
            have_audio = False
            for i in ffprobe._video_info['streams']:
                if i['codec_type'] == 'audio':
                    have_audio = True
                    break
            if have_audio == True:
                print(video + ' 有音频')
            else:
                print(video + ' 无音频')

            if have_audio == True:
                if self.every_setting.use_encode_audio == True:
                    audio_info.append('-c:a')
                    audio_info.append(self.every_setting.audio_format)
                    if self.every_setting.audio_format == 'flac':
                        audio_info.append('-strict')
                        audio_info.append('-2')
                else:
                    audio_info.append('-c:a')
                    audio_info.append('copy')
            # 实测路径
            # FFMPEG_BIN=self.directory + '/vs_pytorch/ffmpeg.exe'
            # 测试路径
            # FFMPEG_BIN = 'ffmpeg.exe'
            FFMPEG_BIN = self.directory + '/vs_pytorch/ffmpeg.exe'
            # 输入处理
            input_info = [FFMPEG_BIN]
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

            # 输出处理
            output_info = []

            output_info.append(video_folder + '/' + video_name + '.' + self.every_setting.vformat)
            if self.every_setting.use_customization_encode == False:
                ffmpeg_code = input_info + ffmpeg_code + color_info + audio_info + output_info
            else:
                ffmpeg_code = input_info + ffmpeg_code + audio_info + output_info

            # vpy配置文件生成
            vpy_place = vpy_folder + '/' + video_name + '.vpy'
            vpy = open(vpy_place, 'w', encoding='utf-8')
            vpy.write('import vapoursynth as vs\n')
            vpy.write('core = vs.core\n')

            vpy.write('res = core.lsmas.LWLibavSource(r"' + video + '")\n')

            if self.every_setting.is_rs_bef == True:
                vpy.write(
                    'res = core.resize.Bicubic(clip=res,matrix_s="709",width=' + self.every_setting.rs_bef_w + ',height=' + self.every_setting.rs_bef_h + ',format=vs.YUV444P16)\n')
            else:
                vpy.write('res = core.resize.Bicubic(clip=res,format=vs.YUV444P16)\n')

            vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n')
            vpy.write('res=core.fmtc.bitdepth(res, bits=32)\n')

            if self.every_setting.sr_method == 'Real_cugan':
                vpy.write('from vsmlrt import CUGAN,Waifu2x,RealESRGAN,Backend\n')
                vpy.write('device=Backend.' + use_device + '\n')
                vpy.write('device.device_id=' + str(self.every_setting.gpu_id) + '\n')
                vpy.write('device.fp16=' + str(self.every_setting.half) + '\n')
                vpy.write(self.cugan_())
                vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'
            if self.every_setting.sr_method == 'Real_esrgan':
                vpy.write('from vsmlrt import CUGAN,Waifu2x,RealESRGAN,Backend\n')
                vpy.write('device=Backend.' + use_device + '\n')
                vpy.write('device.device_id=' + str(self.every_setting.gpu_id) + '\n')
                vpy.write('device.fp16=' + str(self.every_setting.half) + '\n')
                vpy.write(self.esrgan_())
                vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'
            if self.every_setting.sr_method == 'Waifu2x':
                vpy.write('from vsmlrt import CUGAN,Waifu2x,RealESRGAN,Backend\n')
                vpy.write('device=Backend.' + use_device + '\n')
                vpy.write('device.device_id=' + str(self.every_setting.gpu_id) + '\n')
                vpy.write('device.fp16=' + str(self.every_setting.half) + '\n')
                vpy.write(self.waifu2x_())
                vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'
            if self.every_setting.sr_method == 'BasicVSRpp':
                vpy.write('from vsbasicvsrpp import BasicVSRPP\n')
                vpy.write(self.vsrpp_())
                vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

            if self.every_setting.is_rs_aft == True:
                vpy.write(
                    'res = core.resize.Bicubic(clip=res,matrix_s="709",width=' + self.every_setting.rs_aft_w + ',height=' + self.every_setting.rs_aft_h + ',format=vs.YUV444P16)\n')
            else:
                vpy.write('res = core.resize.Bicubic(clip=res,matrix_s="709",format=vs.YUV444P16)\n')

            vpy.write('res.set_output()\n')
            vpy.close()
            print('生成第' + str(num) + '个vpy脚本文件')

            vspipe_code = []
            # 实测路径
            # vspipe_bin=self.directory + '/vapoursynth/VSPipe.exe'
            # 测试路径
            # vspipe_bin = 'D:/VS_NangInShell/VS_Nang/package/VSPipe.exe'
            vspipe_code.append(vspipe_bin)
            vspipe_code.append('-c')
            vspipe_code.append('y4m')
            vspipe_code.append(vpy_place)
            vspipe_code.append('-')
            command_out = vspipe_code
            command_in = ffmpeg_code
            print(command_out)
            print(command_in)
            print('\n')
            if self.run_mode == 'start':
                pipe_out = sp.Popen(command_out, stdout=sp.PIPE, shell=True)
                pipe_in = sp.Popen(command_in, stdin=pipe_out.stdout, stdout=sp.PIPE, stderr=sp.STDOUT, shell=True,
                                   encoding="utf-8", text=True)
                while pipe_in.poll() is None:
                    line = pipe_in.stdout.readline()
                    line = line.strip()
                    if line:
                        print(format(line))
                print(video + " 已经渲染完成，这是队列中第" + str(num) + '个视频。')
            # for line in pipe_in.stdout:
            #     print(line)
            elif self.run_mode == 'debug':
                for str_ in command_out:
                    bat_file.write('\"' + str_ + '\"' + ' ')
                bat_file.write('| ')
                for str_ in command_in:
                    bat_file.write('\"' + str_ + '\"' + ' ')
                bat_file.write('\n')
                print('队列中第' + str(
                    num) + '个视频：' + video + ' 的配置文件已经生成，相关配置信息已经写入输出文件夹的run.bat文件')
            num = num + 1
            print('\n')
        if self.run_mode == 'debug':
            bat_file.write('pause')
        self.signal.emit()


class MyMainWindow(QMainWindow, Ui_mainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        sys.stdout = Signal()
        sys.stdout.text_update.connect(self.updatetext)

        self.real_path = os.path.dirname(os.path.realpath(sys.argv[0]))

        self.video_clear.clicked.connect(self.clear_video_list)
        self.video_clearall.clicked.connect(self.clear_all_video_list)
        self.video_input.clicked.connect(self.input_video_list)

        self.select_of.clicked.connect(self.outfolder)

        self.save_config.clicked.connect(self.save_conf_Manual)
        self.load_config.clicked.connect(self.load_conf_Manual)

        self.pb_autorun.clicked.connect(self.auto_run)
        self.pb_debug.clicked.connect(self.debug_run)
        self.load_conf_auto()
        if ' ' in self.real_path:
            QMessageBox.information(self, "提示信息",
                                    "你的软件存放路径不符合规范，建议把软件存放到英文的路径下,不要有空格")

        for _char in self.real_path:
            if '\u4e00' <= _char <= '\u9fa5':
                QMessageBox.information(self, "提示信息",
                                        "你的软件存放路径不符合规范，建议把软件存放到英文的路径下,不要有空格")
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
        valid_out_folder = True
        for file in files[0]:
            if ' ' in file:
                valid_out_folder = False
                break

        if valid_out_folder == True:
            for file in files[0]:
                self.video_list.addItem(file)
        else:
            QMessageBox.information(self, "提示信息", "视频文件名不能有空格字符，请重新选择。")

    def outfolder(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                     "选取文件夹",
                                                     "./")  # 起始路径
        valid_out_folder = True
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

        device = self.cb_device.currentText()
        gpu_id = self.cb_gpu.currentIndex()
        half = 'True'
        if self.rb_half.isChecked() == False:
            half = 'False'

        cugan_model = self.cb_cg_model.currentText()
        cugan_tile = self.cb_cg_tile.currentText()
        cugan_alpha = self.db_cg_alpha.text()
        cugan_set = cugan_setting(cugan_model, cugan_tile, cugan_alpha)

        esrgan_model = self.cb_eg_model.currentText()
        esrgan_tile = self.cb_eg_tile.currentText()
        esrgan_scale = self.cb_eg_scale.currentText()
        esrgan_set = esrgan_setting(esrgan_model, esrgan_tile, esrgan_scale)

        waifu_model = self.cb_wf_model.currentText()
        waifu_tile = self.cb_wf_tile.currentText()
        waifu_set = waifu2x_setting(waifu_model, waifu_tile)

        vsrpp_model = self.cb_vsrpp_model.currentText()
        vsrpp_interval = self.sb_interval.text()
        vsrpp_set = vsrpp_setting(vsrpp_model, vsrpp_interval)

        sr_set = cugan_set
        sr_method = ''
        if self.cb_SR.currentIndex() == 0:
            sr_method = 'Real_cugan'
            sr_set = cugan_set
        elif self.cb_SR.currentIndex() == 1:
            sr_method = 'Real_esrgan'
            sr_set = esrgan_set
        elif self.cb_SR.currentIndex() == 2:
            sr_method = 'Waifu2x'
            sr_set = waifu_set
        elif self.cb_SR.currentIndex() == 3:
            sr_method = 'BasicVSRpp'
            sr_set = vsrpp_set

        is_rs_bef = self.rb_resize_bef.isChecked()
        is_rs_aft = self.rb_resize_aft.isChecked()

        rs_bef_w = self.sb_rsbef_w.text()
        rs_bef_h = self.sb_rsbef_h.text()
        rs_aft_w = self.sb_rsaft_w.text()
        rs_aft_h = self.sb_rsaft_h.text()

        # encode setting
        encoder = self.cb_encode.currentText()
        preset = self.cb_preset.currentText()
        eformat = self.cb_eformat.currentText()
        vformat = self.cb_vformat.currentText()
        use_crf = self.rb_crf.isChecked()
        use_bit = self.rb_bit.isChecked()
        crf = self.sb_crf.text()
        bit = self.sb_bit.text()
        use_encode_audio = self.rb_audio.isChecked()
        use_source_audio = self.rb_save_source_audio.isChecked()
        audio_format = self.cb_aformat.currentText()
        customization_encode = self.te_customization_encode.toPlainText()
        use_customization_encode = self.rb_customization_encode.isChecked()

        return every_set_object(videos, outfolder,
                                device, gpu_id, half, sr_method, sr_set, is_rs_bef, is_rs_aft, rs_bef_w, rs_bef_h,
                                rs_aft_w, rs_aft_h,
                                encoder, preset, eformat, vformat, use_crf, use_bit, crf, bit, use_encode_audio,
                                use_source_audio, audio_format, customization_encode, use_customization_encode)

    def save_conf_set(self):
        conf = ConfigParser()
        every_setting = self.every_set()

        conf.add_section('sr')
        conf.set('sr', 'device', str(every_setting.device))
        conf.set('sr', 'gpu_id', str(every_setting.gpu_id))
        conf.set('sr', 'half', str(every_setting.half))

        conf.set('sr', 'sr_method', str(every_setting.sr_method))

        if every_setting.sr_method == 'Real_cugan':
            conf.set('sr', 'cugan_model', str(every_setting.sr_set.model))
            conf.set('sr', 'cugan_tile', str(every_setting.sr_set.tile))
            conf.set('sr', 'cugan_alpha', str(every_setting.sr_set.alpha))
        elif every_setting.sr_method == 'Real_esrgan':
            conf.set('sr', 'esrgan_model', str(every_setting.sr_set.model))
            conf.set('sr', 'esrgan_tile', str(every_setting.sr_set.tile))
            conf.set('sr', 'esrgan_scale', str(every_setting.sr_set.scale))
        elif every_setting.sr_method == 'Waifu2x':
            conf.set('sr', 'waifu_model', str(every_setting.sr_set.model))
            conf.set('sr', 'waifu_tile', str(every_setting.sr_set.tile))
        elif every_setting.sr_method == 'BasicVSRpp':
            conf.set('sr', 'vsrpp_model', str(every_setting.sr_set.model))
            conf.set('sr', 'vsrpp_interval', str(every_setting.sr_set.interval))

        conf.set('sr', 'is_rs_bef ', str(every_setting.is_rs_bef))
        conf.set('sr', 'is_rs_aft', str(every_setting.is_rs_aft))
        conf.set('sr', 'rs_bef_w', str(every_setting.rs_bef_w))
        conf.set('sr', 'rs_bef_h', str(every_setting.rs_bef_h))
        conf.set('sr', 'rs_aft_w', str(every_setting.rs_aft_w))
        conf.set('sr', 'rs_aft_h', str(every_setting.rs_aft_h))

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
        conf.set('else_set', 'gpu_id', (str(self.cb_gpu.currentText()))[4:-1])

        return conf

    def load_conf_set(self, conf):

        self.cb_device.setCurrentText(conf['sr']['device'])
        self.rb_half.setChecked(conf['sr'].getboolean('half'))
        self.rb_resize_bef.setChecked(conf['sr'].getboolean('is_rs_bef'))
        self.rb_resize_aft.setChecked(conf['sr'].getboolean('is_rs_aft'))
        self.sb_rsbef_w.setValue(conf['sr'].getint('rs_bef_w'))
        self.sb_rsbef_h.setValue(conf['sr'].getint('rs_bef_h'))
        self.sb_rsaft_w.setValue(conf['sr'].getint('rs_aft_w'))
        self.sb_rsaft_h.setValue(conf['sr'].getint('rs_aft_h'))

        if conf['sr']['sr_method'] == 'Real_cugan':
            self.cb_SR.setCurrentText(conf['sr']['sr_method'])
            self.cb_cg_model.setCurrentText(conf['sr']['cugan_model'])
            self.cb_cg_tile.setCurrentText(conf['sr']['cugan_tile'])
            self.db_cg_alpha.setValue(conf['sr'].getfloat('cugan_alpha'))

        elif conf['sr']['sr_method'] == 'Real_esrgan':
            self.cb_SR.setCurrentText(conf['sr']['sr_method'])
            self.cb_eg_model.setCurrentText(conf['sr']['esrgan_model'])
            self.cb_eg_tile.setCurrentText(conf['sr']['esrgan_tile'])
            self.cb_eg_scale.setCurrentText(conf['sr']['esrgan_scale'])

        elif conf['sr']['sr_method'] == 'Waifu2x':
            self.cb_SR.setCurrentText(conf['sr']['sr_method'])
            self.cb_wf_model.setCurrentText(conf['sr']['waifu_model'])
            self.cb_wf_tile.setCurrentText(conf['sr']['waifu_tile'])

        elif conf['sr']['sr_method'] == 'BasicVSRpp':
            self.cb_SR.setCurrentText(conf['sr']['sr_method'])
            self.cb_vsrpp_model.setCurrentText(conf['sr']['vsrpp_model'])
            self.sb_interval.setValue(conf['sr'].getint('vsrpp_interval'))

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

        with open(self.real_path + '/config.ini', 'w', encoding='utf-8') as f:
            (self.save_conf_set()).write(f)

        QMessageBox.information(self, "提示信息", "已保存当前自定义预设")
        self.save_config.setEnabled(True)
        self.save_config.setText('保存预设')  # conf['url']['smms_pic_url']

    def load_conf_Manual(self):
        self.load_config.setEnabled(False)
        self.load_config.setText('加载ing')
        if not os.path.exists(self.real_path + "/config.ini"):
            QMessageBox.information(self, "提示信息", "自定义预设文件不存在")
        else:
            conf = ConfigParser()
            conf.read(self.real_path + "/config.ini", encoding="utf-8")
            self.load_conf_set(conf)
            print("已加载保存的自定义预设")

        self.load_config.setEnabled(True)
        self.load_config.setText('加载预设')

    def save_conf_auto(self):
        with open(self.real_path + '/config_auto.ini', 'w', encoding='utf-8') as f:
            (self.save_conf_set()).write(f)
        print("已自动保存当前设置，下次启动软件时自动加载")

    def load_conf_auto(self):
        if os.path.exists(self.real_path + "/config_auto.ini"):
            conf = ConfigParser()
            conf.read(self.real_path + "/config_auto.ini", encoding="utf-8")
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

        every_setting = self.every_set()
        allow_autorun = True

        if every_setting.outfolder == '':
            allow_autorun = False
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

        every_setting = self.every_set()
        allow_debug = True

        if every_setting.outfolder == '':
            allow_debug = False
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

    def set_btn_auto_run(self):  # 一键运行开关控制
        self.pb_autorun.setEnabled(True)
        self.pb_autorun.setText('一键启动模式')
        self.pb_debug.setEnabled(True)
        self.pb_debug.setText('Debug模式')


def check_update() -> None:
    if os.path.exists('update.exe'):
        if os.path.exists('VSET_update.exe'):
            os.remove('VSET_update.exe')
        # 删除之前的更新脚本，改名
        os.rename('update.exe', 'VSET_update.exe')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('logo.png'))
    myWin = MyMainWindow()
    myWin.show()

    check_update()

    sys.exit(app.exec_())
