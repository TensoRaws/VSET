import time
from PyQt5.QtCore import *

from PyQt5.QtCore import QThread
import os
import re
import sys
import subprocess as sp
from ffprobe import get_video_info
from ffmpeg import ffmpeg_info

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
        self.directory = (os.path.dirname(os.path.realpath(sys.argv[0]))).replace('\\','/')
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
    def vs_preview_sr(self):
        vs_previewer_bin=''
        if self.every_setting.sr_method == 'Real_cugan_mlrt':
            vs_previewer_bin = self.directory + '/vs_vsmlrt/vsedit-previewer.exe'

        if self.every_setting.sr_method == 'Real_esrgan_mlrt':
            vs_previewer_bin = self.directory + '/vs_vsmlrt/vsedit-previewer.exe'

        if self.every_setting.sr_method == 'Waifu2x_mlrt':
            vs_previewer_bin = self.directory + '/vs_vsmlrt/vsedit-previewer.exe'

        if self.every_setting.sr_method == 'Basicvsrpp':
            vs_previewer_bin = self.directory + '/vs_pytorch/vsedit-previewer.exe'

        if self.every_setting.sr_method == 'swinir':
            vs_previewer_bin = self.directory + '/vs_pytorch/vsedit-previewer.exe'

        if self.every_setting.sr_method == 'Real_esrgan':
            vs_previewer_bin = self.directory + '/vs_pytorch/vsedit-previewer.exe'

        if self.every_setting.sr_method == 'codeformer':
            vs_previewer_bin = self.directory + '/vs_pytorch/vsedit-previewer.exe'

        return vs_previewer_bin

    def vs_preview_vfi(self):
        vs_previewer_bin = ''
        if self.every_setting.vfi_method == 'rife_mlrt':
            vs_previewer_bin = self.directory + '/vs_vsmlrt/vsedit-previewer.exe'
        elif self.every_setting.vfi_method == 'rife_ncnn':
            vs_previewer_bin = self.directory + '/vs_pytorch/vsedit-previewer.exe'
        return vs_previewer_bin

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

        if self.every_setting.sr_method == 'swinir':
            vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

        if self.every_setting.sr_method == 'Real_esrgan':
            vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

        if self.every_setting.sr_method == 'codeformer':
            vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'

        return vspipe_bin

    def vspipe_vfi(self):
        vspipe_bin = ''
        if self.every_setting.vfi_method == 'rife_mlrt':
            vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'
        elif self.every_setting.vfi_method == 'rife_ncnn':
            vspipe_bin = self.directory + '/vs_pytorch/VSPipe.exe'
        return vspipe_bin


    def vpy_generate(self,vpy,video,num):
        vpy.write('import vapoursynth as vs\n')
        vpy.write('core = vs.core\n')

        vpy.write('res = core.lsmas.LWLibavSource(r"' + video + '")\n')
        if self.every_setting.is_rs_bef == True:
            vpy.write(
                'res = core.resize.Bicubic(clip=res,width=' + self.every_setting.rs_bef_w + ',height=' + self.every_setting.rs_bef_h + ',format=vs.YUV420P16)\n')
        else:
            vpy.write('res = core.resize.Bicubic(clip=res,format=vs.YUV420P16)\n')

        if self.every_setting.use_qtgmc == True:
            vpy.write('import havsfunc as haf\n')
            if self.every_setting.qtgmcFps == '保留原帧数':
                vpy.write('res = haf.QTGMC(res, Preset="' + 'Slower' + '", TFF=True, FPSDivisor=2)\n')
            else:
                vpy.write('res = haf.QTGMC(res, Preset="' + 'Slower' + '", TFF=True, FPSDivisor=1)\n')

        if self.every_setting.use_taa_bef == True:
            vpy.write('import vsTAAmbk as taa\n')
            vpy.write(
                'res  = taa.TAAmbk(res, aatype=-3, preaa=-1, strength=0.1, mtype=2, aapair=1, cycle=5, sharp=0)\n')

        if self.every_setting.use_deband == True:
            vpy.write('res  = core.neo_f3kdb.Deband(res,preset="medium",output_depth=16)\n')

        if self.every_setting.priority == '先超后补':
            if self.every_setting.use_sr == True:
                if 'mlrt' in self.every_setting.sr_method:
                    vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n')
                    vpy.write('res=core.fmtc.bitdepth(res, bits=32)\n')
                elif self.every_setting.sr_method == 'codeformer':
                    vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB24)\n')
                else:
                    if self.every_setting.use_half_sr == True:
                        vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGBH)\n')
                    else:
                        vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGBS)\n')
                for str_ in self.every_setting.sr_set.sr_vpy():
                    vpy.write(str_)

            if self.every_setting.use_vfi == True:
                vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n')
                vpy.write('res=core.fmtc.bitdepth(res, bits=32)\n')
                for str_ in self.every_setting.vfi_set.vfi_vpy():
                    vpy.write(str_)
        else:
            if self.every_setting.use_vfi == True:
                vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n')
                vpy.write('res=core.fmtc.bitdepth(res, bits=32)\n')
                for str_ in self.every_setting.vfi_set.vfi_vpy():
                    vpy.write(str_)
            if self.every_setting.use_sr == True:
                if 'mlrt' in self.every_setting.sr_method:
                    vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n')
                    vpy.write('res=core.fmtc.bitdepth(res, bits=32)\n')
                elif self.every_setting.sr_method == 'codeformer':
                    vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB24)\n')
                else:
                    if self.every_setting.use_half_sr == True:
                        vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGBH)\n')
                    else:
                        vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGBS)\n')
                for str_ in self.every_setting.sr_set.sr_vpy():
                    vpy.write(str_)

        if self.every_setting.is_rs_aft == True:
            vpy.write(
                'res = core.resize.Bicubic(clip=res,matrix_s="709",width=' + self.every_setting.rs_aft_w + ',height=' + self.every_setting.rs_aft_h + ',format=vs.YUV420P16)\n')
        else:
            vpy.write('res = core.resize.Bicubic(clip=res,matrix_s="709",format=vs.YUV420P16)\n')

        if self.every_setting.use_cas_aft == True:
            vpy.write('res=core.cas.CAS(res, sharpness=1)\n')
        if self.every_setting.use_taa_aft == True:
            vpy.write('import vsTAAmbk as taa\n')
            vpy.write(
                'res  = taa.TAAmbk(res, aatype=-3, preaa=-1, strength=0.1, mtype=2, aapair=1, cycle=5, sharp=0)\n')
        if self.every_setting.add_noise == True:  # 添加噪点
            vpy.write('from adptvgrnMod import adptvgrnMod\n')
            vpy.write(
                'res = adptvgrnMod(res, size=3, strength=[10,10], sharp=33, luma_scaling=50, seed=3, show_mask=0)\n')

        if self.every_setting.embed_input_sub == True:
            vpy.write('res = core.vsfm.TextSubMod(res,file="' + self.every_setting.subs[num - 1] + '")\n')

        vpy.write('res.set_output()\n')
        vpy.close()

    def run(self):

        vpy_folder = self.every_setting.outfolder + '/vpys'

        if self.run_mode == 'debug':

            bat_file = open(self.every_setting.outfolder + '/run.bat', 'w', encoding='ansi')

        if not os.path.exists(vpy_folder):
            os.makedirs(vpy_folder)#存放配置文件vpy的文件夹

        video_folder = self.every_setting.outfolder
        if not os.path.exists(video_folder):
            os.makedirs(video_folder)
        num = 1

        if self.run_mode=='preview':

            video=self.every_setting.video_select
            video=(self.every_setting.videos)[video]

            video_name = (video.rsplit("/", 1))[-1]
            video_name = (video_name.rsplit(".", 1))[0]  # 只保留文件名的参数

            vpy_place = vpy_folder + '/' + video_name + '.vpy'
            print(vpy_place)

            vpy = open(vpy_place, 'w', encoding='utf-8')

            self.vpy_generate(vpy, video,num)

            print('生成第' + str(num) + '个vpy脚本文件，对应视频文件：' + video + '\n')

            # vspipe默认路径
            vs_previewer_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'
            # 判断vspipe路径类型

            if self.every_setting.use_vfi == True:
                vs_previewer_bin = self.vs_preview_vfi()
            if self.every_setting.use_sr == True:
                vs_previewer_bin = self.vs_preview_sr()

            command_preview=[]
            command_preview.append(vs_previewer_bin)
            command_preview.append(vpy_place)
            print(command_preview)

            startupinfo = sp.STARTUPINFO(dwFlags=sp.STARTF_USESHOWWINDOW)
            print('建议不要在TRT引擎未渲染之前使用预览功能，不然加载时间会很漫长，且没有报错提示\n')
            print('预览加载ing，如果长时间不响应请关闭重试')
            self.pipi_preview=sp.Popen(command_preview, encoding='utf-8')

            self.pipi_preview.wait()
            print('预览完毕\n')

        else:
            for video in self.every_setting.videos:

                print('正在运行队列中第'+str(num)+'个视频，视频文件名: '+video)
                print(' ')

                ffmpeg_code = self.ffmpeg_()#压制参数之一

                ffprobe = get_video_info(video)#视频的各个参数


                video_name = (video.rsplit("/", 1))[-1]
                video_name = (video_name.rsplit(".", 1))[0]  # 只保留文件名的参数

                # video_frames = ffprobe.frames()#原视频帧数

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
                    if self.every_setting.use_encode_audio == True:
                        audio_info.append('-c:a')
                        audio_info.append(self.every_setting.audio_format)
                    else:#无论使用原音频还是外挂新音频，都是copy
                        audio_info.append('-c:a')
                        audio_info.append('copy')
                    print(video+' 有音频，默认使用-map 1:a对此视频所有的音频进行处理')
                else:
                    if self.every_setting.use_input_audio == True:
                        audio_info.append('-c:a')
                        audio_info.append('copy')
                    print(video+' 无音频')

                print(' ')

                sub_info=[]
                have_sub=ffprobe.is_HaveSubtitle()

                if have_sub == True:
                    if self.every_setting.use_source_sub == True or self.every_setting.attach_input_sub==True:
                        sub_info.append('-c:s')
                        sub_info.append('copy')
                    print(video+' 有外挂字幕')
                else:
                    if self.every_setting.attach_input_sub == True:
                        sub_info.append('-c:s')
                        sub_info.append('copy')
                    print(video+' 无外挂字幕')
                print(' ')

                FFMPEG_BIN = self.directory + '/ffmpeg.exe'
                #输入处理

                input_info=[FFMPEG_BIN]
                input_info.append('-hide_banner')
                input_info.append('-y')
                input_info.append('-i')
                input_info.append('pipe:')
                input_info.append('-i')
                input_info.append(video)

                if self.every_setting.use_input_audio==True:
                    input_info.append('-i')
                    input_info.append(self.every_setting.audios[num-1])

                if self.every_setting.attach_input_sub==True:
                    input_info.append('-i')
                    input_info.append(self.every_setting.subs[num - 1])

                #0是管道流，1是源视频流，2是音频流，3是字幕流
                #音频

                input_info.append('-map')
                input_info.append('0:v:0')
                if have_audio == True and self.every_setting.use_input_audio==False:
                    input_info.append('-map')
                    input_info.append('1:a')
                #字幕
                if have_sub == True and self.every_setting.use_source_sub == True:
                    input_info.append('-map')
                    input_info.append('1:s')

                if self.every_setting.use_input_audio==True:
                    input_info.append('-map')
                    input_info.append('2:a')

                if self.every_setting.attach_input_sub==True:
                    input_info.append('-map')
                    if self.every_setting.use_input_audio == True:
                        input_info.append('3')
                    else:
                        input_info.append('2')

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

                self.vpy_generate(vpy,video,num)
                print('生成第' + str(num) + '个vpy脚本文件，对应视频文件：'+video+'\n')

                # vspipe默认路径
                vspipe_bin = self.directory + '/vs_vsmlrt/VSPipe.exe'
                # 判断vspipe路径类型

                if self.every_setting.use_vfi == True:
                    vspipe_bin = self.vspipe_vfi()
                if self.every_setting.use_sr == True:
                    vspipe_bin = self.vspipe_sr()

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
                print('')
                print(command_in)
                print('')
                if self.run_mode=='start':
                    startupinfo = sp.STARTUPINFO(dwFlags=sp.STARTF_USESHOWWINDOW)
                    #vspipe debug信息
                    self.pipe_test = sp.Popen(command_test, stdout=sp.PIPE, stderr=sp.PIPE, shell=False,
                                              startupinfo=startupinfo,encoding='utf-8')
                    for line in self.pipe_test.stderr:
                        print(str(line).replace("\n",""))
                    self.pipe_test.wait()
                    #vspipe的视频信息
                    self.pipe_test = sp.Popen(command_test, stdout=sp.PIPE, stderr=sp.PIPE, shell=False,
                                              startupinfo=startupinfo,encoding='utf-8')
                    info_dict = {}
                    for line in self.pipe_test.stdout:
                        key, value = (str(line).replace("\n", "")).strip().split(':')
                        info_dict[key.strip()] = value.strip()

                    self.pipe_test.wait()
                    print('以下是渲染的视频'+video+'的视频预览信息')
                    print('Width:', info_dict['Width'])
                    print('Height:', info_dict['Height'])
                    print('Frames:', info_dict['Frames'])
                    print('FPS:', info_dict['FPS'])
                    print('已输出 ' + video + ' 的相关运行前信息')
                    print(' ')
                    #运行
                    self.pipe_out = sp.Popen(command_out, stdout=sp.PIPE, shell=False,startupinfo=startupinfo)
                    self.pipe_in = sp.Popen(command_in, stdin=self.pipe_out.stdout, stdout=sp.PIPE, stderr=sp.STDOUT, shell=False,startupinfo=startupinfo,
                                       encoding="utf-8", text=True)


                    # for line in self.pipe_test.stderr:
                    #     print(str(line,encoding='utf-8').replace("\n",""))

                    pattern =r"frame=\s*(-?\d+)\s+fps=\s*([\d.]+).+time=\s*(-?[\d:.]+)\s+bitrate=\s*(-?[\w/.-]+)"
                    video_render_frames=int(info_dict['Frames'])
                    while self.pipe_in.poll() is None:
                        line = self.pipe_in.stdout.readline()
                        line = line.strip()
                        if line:
                            match = re.search(pattern, format(line))
                            if match:
                                frame = int(match.group(1)) if match.group(1) else None
                                fps = float(match.group(2)) if match.group(2) else None
                                time = match.group(3) if match.group(3) else None
                                bitrate = match.group(4) if match.group(4) else None
                                if fps != 0:
                                    print('已渲染/总帧数: '+ str(frame)+' / '+str(video_render_frames)+' '
                                          +'速度(FPS): '+str(fps)
                                          +' '+'预计剩余时间：'+str(
                                            int(((video_render_frames - frame) / fps) / 3600)) + 'h ' + str(
                                            int((((video_render_frames - frame) / fps) % 3600) / 60)) + 'min ' + str(
                                            int(((video_render_frames - frame) / fps) % 60)) + 'sec'+' '+
                                        '已渲染的时间长度: '+ time +' '+
                                        '比特率: '+bitrate)
                                # else:
                                # print(frame, fps, time, bitrate)
                            else:
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