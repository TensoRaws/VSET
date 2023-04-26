import time
from PyQt5.QtCore import *

from PyQt5.QtCore import QThread
import os
import sys
import subprocess as sp
from src.ffprobe import get_video_info
from src.ffmpeg import ffmpeg_info

class autorun_test(QThread):
    def __init__(self):
        super().__init__()
        self.test=True

    def run(self):
        print('test\n')

class autorun(QThread):
    signal = pyqtSignal()
    def __init__(self, every_setting, run_mode):
        super().__init__()
        self.every_setting=every_setting
        self.run_mode=run_mode
        self.directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.ffmpeg_=ffmpeg_info(every_setting).return_ffmpeg
        self.pipe_out=None
        self.pipe_in=None
        self.pipe_test=None
        self.is_running=True

    def stop_(self):
        self.is_running = False
        if self.pipe_in !=None:
            try:
                self.pipe_in.kill()
            except:
                print('中止失败')
        if self.pipe_out !=None:
            try:
                self.pipe_out.kill()
            except:
                print('中止失败')
        if self.pipe_test !=None:
            try:
                self.pipe_test.kill()
            except:
                print('中止失败')

    def vspipe_sr(self):
        vspipe_bin=''
        if self.every_setting.sr_method == 'Real_cugan_mlrt':
            vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'

        if self.every_setting.sr_method == 'Real_esrgan_mlrt':
            vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'

        if self.every_setting.sr_method == 'Waifu2x_mlrt':
            vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'

        if self.every_setting.sr_method == 'Basicvsrpp':
            vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

        if self.every_setting.sr_method == 'Basicvsr':
            vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

        if self.every_setting.sr_method == 'Swinir':
            vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

        if self.every_setting.sr_method == 'Real_esrgan':
            vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

        if self.every_setting.sr_method == 'AnimeSR':
            vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

        return vspipe_bin

    def vspipe_vfi(self):
        vspipe_bin = ''
        if self.every_setting.vfi_method == 'rife_mlrt':
            vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'
        elif self.every_setting.vfi_method == 'rife_ncnn':
            vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'
        return vspipe_bin

    def run(self):
        vpy_folder = self.every_setting.outfolder + '/vpys'
        if self.run_mode == 'debug':
            bat_file = open(self.every_setting.outfolder + '/run.bat', 'w', encoding='ansi')
        if not os.path.exists(vpy_folder):
            os.makedirs(vpy_folder)#存放配置文件vpy的文件夹
        video_folder = self.every_setting.outfolder
        if not os.path.exists(video_folder):
            os.makedirs(video_folder)

        #实测路径
        #FFMPEG_BIN=self.directory + '\\vapoursynth\\ffmpeg.exe'
        #测试路径
        #FFMPEG_BIN = 'ffmpeg.exe'
        num = 1

        for video in self.every_setting.videos:

            print('正在运行队列中第'+str(num)+'个视频，视频文件名: '+video)

            ffmpeg_code = self.ffmpeg_()#压制参数之一

            ffprobe = get_video_info(video)#视频的各个参数


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
            have_audio = ffprobe.is_HaveAudio()

            if have_audio == True:
                print(video+' 有音频，默认使用-map 1:a对此视频所有的音频进行处理')
            else:
                print(video+' 无音频，将跳过加载音频处理的参数')


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
            sub_info=[]
            have_sub=ffprobe.is_HaveSubtitle()

            if have_sub == True:
                    sub_info.append('-c:s')
                    sub_info.append('copy')

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
            if have_sub == True:
                input_info.append('-map')
                input_info.append('1:s')
            #输出处理

            output_info=[]
            output_info.append(video_folder+'/'+video_name+'.'+self.every_setting.vformat)
            if self.every_setting.use_customization_encode == False:#自定义压制参数
                # ffmpeg_code = input_info + ffmpeg_code + color_info + audio_info + output_info
                ffmpeg_code = input_info + ffmpeg_code + audio_info + sub_info + output_info
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
                if self.every_setting.qtgmcFps=='保留原帧数':
                    vpy.write('res = haf.QTGMC(res, Preset="'+'Slower'+'", TFF=True, FPSDivisor=2)\n')
                else:
                    vpy.write('res = haf.QTGMC(res, Preset="' + 'Slower' + '", TFF=True, FPSDivisor=1)\n')
            if self.every_setting.use_deband == True:
                vpy.write('res  = core.neo_f3kdb.Deband(res,preset="medium",output_depth=16)\n')

            vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n')
            vpy.write('res=core.fmtc.bitdepth(res, bits=32)\n')
            #vspipe默认路径
            vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'
            # 判断vspipe路径类型

            if self.every_setting.use_vfi==True:
                vspipe_bin = self.vspipe_vfi()
            if self.every_setting.use_sr==True:
                vspipe_bin=self.vspipe_sr()

            if self.every_setting.use_sr == True:
                for str_ in self.every_setting.sr_set.sr_vpy():
                    vpy.write(str_)
            if self.every_setting.use_vfi == True:
                for str_ in self.every_setting.vfi_set.vfi_vpy():
                    vpy.write(str_)
            if self.every_setting.is_rs_aft == True:
                vpy.write(
                    'res = core.resize.Bicubic(clip=res,matrix_s="709",width=' + self.every_setting.rs_aft_w + ',height=' + self.every_setting.rs_aft_h + ',format=vs.YUV444P16)\n')
            else:
                vpy.write('res = core.resize.Bicubic(clip=res,matrix_s="709",format=vs.YUV444P16)\n')

            if self.every_setting.add_noise == True:#添加噪点
                vpy.write('from adptvgrnMod import adptvgrnMod\n')
                vpy.write('res = adptvgrnMod(res, size=3, strength=[10,10], sharp=33, luma_scaling=50, seed=3, show_mask=0)\n')

            vpy.write('res.set_output()\n')
            vpy.close()
            print('生成第' + str(num) + '个vpy脚本文件，对应视频文件：'+video+'')

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

            if self.run_mode=='start':
                startupinfo = sp.STARTUPINFO(dwFlags=sp.STARTF_USESHOWWINDOW)

                self.pipe_test = sp.Popen(command_test, stdout=sp.PIPE, stderr=sp.PIPE, shell=False,
                                          startupinfo=startupinfo)
                for line in self.pipe_test.stderr:
                    print(str(line,encoding='utf-8').replace("\n",""))
                self.pipe_test.wait()

                self.pipe_out = sp.Popen(command_out, stdout=sp.PIPE, shell=False,startupinfo=startupinfo)
                self.pipe_in = sp.Popen(command_in, stdin=self.pipe_out.stdout, stdout=sp.PIPE, stderr=sp.STDOUT, shell=False,startupinfo=startupinfo,
                                   encoding="utf-8", text=True)


                # for line in self.pipe_test.stderr:
                #     print(str(line,encoding='utf-8').replace("\n",""))

                print('已输出 '+video+' 的debug信息')
                print(' ')

                while self.pipe_in.poll() is None:
                    line = self.pipe_in.stdout.readline()
                    line = line.strip()
                    if line:
                        print(format(line))

                if self.is_running==False:
                    break

                print(video+" 已经渲染完成，这是队列中第"+str(num)+'个视频。')

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
        #回归None
        self.pipe_out = None
        self.pipe_in = None
        self.pipe_test = None

        self.signal.emit()