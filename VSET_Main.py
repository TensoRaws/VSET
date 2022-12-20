import sys
import os
import subprocess as sp
import webbrowser

from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from VSET import Ui_MainWindow

class Signal(QObject):
    text_update = pyqtSignal(str)

    def write(self, text):
        self.text_update.emit(str(text))
        QApplication.processEvents()

class cugan_setting(QObject):
    def __init__(self,model,tile,alpha):
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
    def __init__(self,model,tile,scale):
        self.model = model
        self.tile = tile
        self.scale = scale

    def return_model(self):
        return self.model

    def return_tile(self):
        return self.tile

    def return_scale(self):
        return self.scale

class diy_setting(QObject):
    def __init__(self,videos,vpy):
        self.videos = videos
        self.vpy = vpy

    def return_videos(self):
        return self.videos

    def return_vpy(self):
        return self.vpy


class sr_auto_setting(QObject):
    def __init__(self,videos,device,half,sr_method,cugan_setting,esrgan_setting,is_rs_bef,is_rs_aft,rs_bef_w,rs_bef_h,rs_aft_w,rs_aft_h):
        self.videos = videos
        self.device = device
        self.half = half
        self.sr_method = sr_method
        self.cugan_setting = cugan_setting
        self.esrgan_setting = esrgan_setting
        self.is_rs_bef = is_rs_bef
        self.is_rs_aft = is_rs_aft
        self.rs_bef_w = rs_bef_w
        self.rs_bef_h = rs_bef_h
        self.rs_aft_w = rs_aft_w
        self.rs_aft_h = rs_aft_h

    def return_videos(self):
        return self.videos

    def return_device(self):
        return self.device

    def return_half(self):
        return self.half

    def return_sr_method(self):
        return self.sr_method

    def return_cugan_setting(self):
        return self.cugan_setting

    def return_esrgan_setting(self):
        return self.esrgan_setting

    def return_is_rs_bef(self):
        return self.is_rs_bef

    def return_is_rs_aft(self):
        return self.is_rs_aft

    def return_rs_bef_w(self):
        return self.rs_bef_w

    def return_rs_bef_h(self):
        return self.rs_bef_h

    def return_rs_aft_w(self):
        return self.rs_aft_w

    def return_rs_aft_h(self):
        return self.rs_aft_h

class encode_setting(QObject):
    def __init__(self,outfolder,encoder,preset,eformat,vformat,use_crf,use_bit,crf,bit,encode_diy,use_sr_auto,use_diy,use_encode_diy):
        self.outfolder = outfolder
        self.encoder = encoder
        self.preset = preset
        self.eformat = eformat
        self.vformat = vformat
        self.use_crf = use_crf
        self.use_bit = use_bit
        self.crf = crf
        self.bit = bit
        self.encode_diy = encode_diy
        self.use_sr_auto = use_sr_auto
        self.use_diy = use_diy
        self.use_encode_diy = use_encode_diy

    def return_outfolder(self):
        return self.outfolder

    def return_encoder(self):
        return self.encoder

    def return_use_crf(self):
        return self.use_crf

    def return_use_bit(self):
        return self.use_bit

    def return_preset(self):
        return self.preset

    def return_eformat(self):
        return self.eformat

    def return_vformat(self):
        return self.vformat

    def return_crf(self):
        return self.crf

    def return_bit(self):
        return self.bit

    def return_encode_diy(self):
        return self.encode_diy

    def return_use_sr_auto(self):
        return self.use_sr_auto

    def return_use_diy(self):
        return self.use_diy

    def return_use_encode_diy(self):
        return self.use_encode_diy


class sr_auto(QThread):
    signal = pyqtSignal()
    def __init__(self, sr_auto_setting,encode_setting,run_mode):
        super().__init__()

        self.directory=os.path.dirname(os.path.realpath(sys.argv[0]))

        self.run_mode=run_mode
        self.videos = sr_auto_setting.return_videos()
        self.device = sr_auto_setting.return_device()
        self.half = sr_auto_setting.return_half()
        if self.half == 'True':
            self.half=True
        else:
            self.half=False

        self.sr_method = sr_auto_setting.return_sr_method()
        self.cugan_setting = sr_auto_setting.return_cugan_setting()
        self.esrgan_setting=sr_auto_setting.return_esrgan_setting()
        self.is_rs_bef = sr_auto_setting.return_is_rs_bef()

        self.is_rs_aft = sr_auto_setting.return_is_rs_aft()
        self.rs_bef_w = sr_auto_setting.return_rs_bef_w()
        self.rs_bef_h = sr_auto_setting.return_rs_bef_h()
        self.rs_aft_w = sr_auto_setting.return_rs_aft_w()
        self.rs_aft_h = sr_auto_setting.return_rs_aft_w()


        self.outfolder = encode_setting.return_outfolder()
        self.encoder = encode_setting.return_encoder()
        self.preset = encode_setting.return_preset()
        self.eformat = encode_setting.return_eformat()
        self.vformat = encode_setting.return_vformat()
        self.use_crf = encode_setting.return_use_crf()
        self.use_bit = encode_setting.return_use_bit()
        self.crf = encode_setting.return_crf()
        self.bit = encode_setting.return_bit()
        self.encode_diy = encode_setting.return_encode_diy()
        self.use_sr_auto = encode_setting.return_use_sr_auto()
        self.use_diy = encode_setting.return_use_diy()
        self.use_encode_diy = encode_setting.return_use_encode_diy()
    def cugan_(self):
        noise = 0
        scale = 2
        version = 2

        if self.cugan_setting.return_model() == 'pro-conservative-up2x':
            noise = 0
            scale = 2
            version = 2
        elif self.cugan_setting.return_model() == 'pro-conservative-up3x':
            noise = 0
            scale = 3
            version = 2
        elif self.cugan_setting.return_model() == 'pro-denoise3x-up2x':
            noise = 3
            scale = 2
            version = 2
        elif self.cugan_setting.return_model() == 'pro-denoise3x-up3x':
            noise = 3
            scale = 3
            version = 2
        elif self.cugan_setting.return_model() == 'pro-no-denoise3x-up2x':
            noise = -1
            scale = 2
            version = 2
        elif self.cugan_setting.return_model() == 'pro-no-denoise3x-up3x':
            noise = -1
            scale = 3
            version = 2
        elif self.cugan_setting.return_model() == 'up2x-latest-conservative':
            noise = 0
            scale = 2
            version = 1
        elif self.cugan_setting.return_model() == 'up2x-latest-denoise1x':
            noise = 1
            scale = 2
            version = 1
        elif self.cugan_setting.return_model() == 'up2x-latest-denoise2x':
            noise = 2
            scale = 2
            version = 1
        elif self.cugan_setting.return_model() == 'up2x-latest-denoise3x':
            noise = 3
            scale = 2
            version = 1
        elif self.cugan_setting.return_model() == 'up2x-latest-no-denoise':
            noise = -1
            scale = 2
            version = 1
        elif self.cugan_setting.return_model() == 'up3x-latest-conservative':
            noise = 0
            scale = 3
            version = 1
        elif self.cugan_setting.return_model() == 'up3x-latest-denoise3x':
            noise = 3
            scale = 3
            version = 1
        elif self.cugan_setting.return_model() == 'up3x-latest-no-denoise':
            noise = -1
            scale = 3
            version = 1
        elif self.cugan_setting.return_model() == 'up4x-latest-conservative':
            noise = 0
            scale = 4
            version = 1
        elif self.cugan_setting.return_model() == 'up4x-latest-denoise3x':
            noise = 3
            scale = 4
            version = 1
        elif self.cugan_setting.return_model() == 'up4x-latest-no-denoise':
            noise = -1
            scale = 4
            version = 1

        return('res = CUGAN(res, noise='+str(noise)+', scale='+str(scale)+', tiles='+str(self.cugan_setting.return_tile())+',version='+str(version)+',alpha='+str(self.cugan_setting.return_alpha())+', backend=device)\n')

    def esrgan_(self):
        model=0
        if self.esrgan_setting.return_model()=='animevideov3':
            model=0
        elif self.esrgan_setting.return_model()=='animevideo-xsx2':
            model = 1
        elif self.esrgan_setting.return_model()=='animevideo-xsx4':
            model = 2

        return ('res = RealESRGAN(res, scale='+str(self.esrgan_setting.return_scale())+',tiles='+str(self.esrgan_setting.return_tile())+',model='+str(model)+', backend=device)')

    def ffmpeg_(self):
        vcodec = 'libx265'
        profile = 'main10'
        yuv = 'yuv420p10le'

        if self.encoder == 'cpu(i)' and self.eformat == 'H265':
            vcodec = 'libx265'
            yuv = 'yuv420p10le'
            profile = 'main10'
        elif self.encoder == 'cpu(i)' and self.eformat == 'H264':
            vcodec = 'libx264'
            yuv = 'yuv420p'
            profile = 'main'
        elif self.encoder == 'nvenc' and self.eformat == 'H264':
            vcodec = 'h264_nvenc'
            yuv = 'yuv420p'
            profile = 'main'
        elif self.encoder == 'nvenc' and self.eformat == 'H265':
            vcodec = 'hevc_nvenc'
            yuv = 'yuv420p10le'
            profile = 'main10'
        ffmpeg_set = ' -y -map 0:v:0 -map 1:a -c:v ' + vcodec + ' -pix_fmt ' + yuv + ' -profile:v ' + profile + ' -preset ' + self.preset

        if self.eformat == 'H265':
            ffmpeg_set = ffmpeg_set + ' -vtag hvc1'

        if self.use_crf == True:
            ffmpeg_set = ffmpeg_set + ' -crf ' + self.crf
        else:
            ffmpeg_set = ffmpeg_set + ' -b:v ' + self.bit + 'm '

        ffmpeg_set = ffmpeg_set + ' -c:a aac '
        return ffmpeg_set

    def run(self):
        vpy_folder=self.outfolder+'/vpys'
        if not os.path.exists(vpy_folder):
            os.makedirs(vpy_folder)#存放配置文件vpy的文件夹

        video_folder=self.outfolder+'/out_videos'
        if not os.path.exists(video_folder):
            os.makedirs(video_folder)

        #ORT_CPU,ORT_CUDA,OV_CPU,TRT,OV_GPU,NCNN_VK
        if self.device =='GPU_nvidia':
            use_device='ORT_CUDA()'
        elif self.device=='GPU_nvidia_trt':
            use_device = 'TRT()'
        elif self.device=='GPU_amd':
            use_device = 'OV_GPU()'
        elif self.device=='NCNN':
            use_device = 'NCNN_VK()'
        elif self.device=='CPU_intel':
            use_device = 'ORT_CPU()'
        elif self.device=='CPU_amd':
            use_device = 'OV_CPU()'

        cugan_code=self.cugan_()
        esrgan_code=self.esrgan_()
        ffmpeg_code=self.ffmpeg_()


        if self.run_mode=='getbat':
            num = 1
            bat_file = open(self.outfolder + '/run.bat', 'w', encoding='ansi')
            for video in self.videos:
                print('生成第' + str(num) + '个vpy脚本文件')

                video_name=(video.rsplit("/",1))[-1]
                video_name=(video_name.rsplit(".",1))[0]#只保留文件名的参数
                vpy_place=vpy_folder+'/'+video_name+'.vpy'
                vpy=open(vpy_place,'w',encoding='utf-8')
                vpy.write('import vapoursynth as vs\n')
                vpy.write('from vsmlrt import CUGAN,RealESRGAN,Backend\n')
                vpy.write('core = vs.core\n')

                vpy.write('device=Backend.'+use_device+'\n')
                vpy.write('device.device_id=0\n')
                vpy.write('device.fp16='+str(self.half)+'\n')

                vpy.write('res = core.lsmas.LWLibavSource(r"'+video+'")\n')


                if self.is_rs_bef==True:
                    vpy.write('res = core.resize.Bicubic(clip=res,width='+self.rs_bef_w+',height='+self.rs_bef_h+',format=vs.YUV444P16)\n')
                else:
                    vpy.write('res = core.resize.Bicubic(clip=res,format=vs.YUV444P16)\n')

                vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n')
                vpy.write('res=core.fmtc.bitdepth(res, bits=32)\n')

                if self.sr_method=='Real_cugan':
                    vpy.write(cugan_code)
                if self.sr_method=='Real_esrgan':
                    vpy.write(esrgan_code)

                if self.is_rs_aft == True:
                    vpy.write('res = core.resize.Bicubic(clip=res,width=' + self.rs_aft_w + ',height=' + self.rs_aft_h + ',format=vs.YUV444P16)\n')
                else:
                    vpy.write('res = core.resize.Bicubic(clip=res,matrix_s="709",format=vs.YUV444P16)\n')
                vpy.write('res.set_output()\n')
                vpy.close()
                print("生成第"+str(num)+"个批处理命令行，并写入bat")
                if self.use_encode_diy==False:
                    bat_file.write(
                        '"'+self.directory+'\\vapoursynth\\VSPipe.exe"' + ' -c y4m ' + vpy_place + ' - | "'+self.directory+'\\vapoursynth\\ffmpeg.exe" -i pipe: -i ' + video + ffmpeg_code +video_folder+'/'+video_name+'.'+self.vformat+'\n')
                else:
                    bat_file.write(
                        '"'+self.directory+'\\vapoursynth\\VSPipe.exe"' + ' -c y4m ' + vpy_place + ' - | "'+self.directory+'\\vapoursynth\\ffmpeg.exe" '+self.encode_diy)

                print("完成第" + str(num) + "个视频的相关配置")
                num = num + 1
            bat_file.close()
            print('bat文件已在输出文件夹里生成')

        elif self.run_mode=='start':
            num = 1
            for video in self.videos:
                print('生成第' + str(num) + '个vpy脚本文件')

                video_name = (video.rsplit("/", 1))[-1]
                video_name = (video_name.rsplit(".", 1))[0]  # 只保留文件名的参数
                vpy_place = vpy_folder + '/' + video_name + '.vpy'
                vpy = open(vpy_place, 'w', encoding='utf-8')
                vpy.write('import vapoursynth as vs\n')
                vpy.write('from vsmlrt import CUGAN,RealESRGAN,Backend\n')
                vpy.write('core = vs.core\n')

                vpy.write('device=Backend.' + use_device + '\n')
                vpy.write('device.device_id=0\n')
                vpy.write('device.fp16=' + str(self.half) + '\n')

                vpy.write('res = core.lsmas.LWLibavSource(r"' + video + '")\n')

                if self.is_rs_bef == True:
                    vpy.write(
                        'res = core.resize.Bicubic(clip=res,width=' + self.rs_bef_w + ',height=' + self.rs_bef_h + ',format=vs.YUV444P16)\n')
                else:
                    vpy.write('res = core.resize.Bicubic(clip=res,format=vs.YUV444P16)\n')

                vpy.write('res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n')
                vpy.write('res=core.fmtc.bitdepth(res, bits=32)\n')

                if self.sr_method == 'Real_cugan':
                    vpy.write(cugan_code)
                if self.sr_method == 'Real_esrgan':
                    vpy.write(esrgan_code)

                if self.is_rs_aft == True:
                    vpy.write(
                        'res = core.resize.Bicubic(clip=res,width=' + self.rs_aft_w + ',height=' + self.rs_aft_h + ',format=vs.YUV444P16)\n')
                else:
                    vpy.write('res = core.resize.Bicubic(clip=res,matrix_s="709",format=vs.YUV444P16)\n')
                vpy.write('res.set_output()\n')
                vpy.close()

                command_out=self.directory+'\\vapoursynth\\VSPipe.exe -c y4m '+vpy_place+' -'
                if self.use_encode_diy==False:
                    command_in=self.directory+'\\vapoursynth\\ffmpeg.exe -i pipe: -i ' + video + ffmpeg_code +video_folder+'/'+video_name+'.'+self.vformat
                else:
                    command_in=self.directory+'\\vapoursynth\\ffmpeg.exe '+self.encode_diy
                pipe_out= sp.Popen(command_out, stdout=sp.PIPE,shell=True)
                pipe_in=sp.Popen(command_in, stdin=pipe_out.stdout, stdout=sp.PIPE,stderr=sp.STDOUT, shell=True,encoding="utf-8",text=True)

                for line in pipe_in.stdout:
                    print(line)
                num = num + 1
        self.signal.emit()

class diy_encode(QThread):
    signal = pyqtSignal()
    def __init__(self, diy_setting,encode_setting,run_mode):
        super().__init__()
        self.directory = os.path.dirname(os.path.realpath(sys.argv[0]))

        self.videos=diy_setting.return_videos()
        self.vpy=diy_setting.return_vpy()

        self.outfolder = encode_setting.return_outfolder()
        self.encoder = encode_setting.return_encoder()
        self.preset = encode_setting.return_preset()
        self.eformat = encode_setting.return_eformat()
        self.vformat = encode_setting.return_vformat()
        self.use_crf = encode_setting.return_use_crf()
        self.use_bit = encode_setting.return_use_bit()
        self.crf = encode_setting.return_crf()
        self.bit = encode_setting.return_bit()
        self.encode_diy = encode_setting.return_encode_diy()
        self.use_sr_auto = encode_setting.return_use_sr_auto()
        self.use_diy = encode_setting.return_use_diy()
        self.use_encode_diy = encode_setting.return_use_encode_diy()

        self.run_mode=run_mode

    def ffmpeg_(self):
        vcodec = 'libx265'
        profile = 'main10'
        yuv = 'yuv420p10le'

        if self.encoder == 'cpu(i)' and self.eformat == 'H265':
            vcodec = 'libx265'
            yuv = 'yuv420p10le'
            profile = 'main10'
        elif self.encoder == 'cpu(i)' and self.eformat == 'H264':
            vcodec = 'libx264'
            yuv = 'yuv420p'
            profile = 'main'
        elif self.encoder == 'nvenc' and self.eformat == 'H264':
            vcodec = 'h264_nvenc'
            yuv = 'yuv420p'
            profile = 'main'
        elif self.encoder == 'nvenc' and self.eformat == 'H265':
            vcodec = 'hevc_nvenc'
            yuv = 'yuv420p10le'
            profile = 'main10'
        ffmpeg_set = ' -y -map 0:v:0 -map 1:a -c:v ' + vcodec + ' -pix_fmt ' + yuv + ' -profile:v ' + profile + ' -preset ' + self.preset

        if self.eformat == 'H265':
            ffmpeg_set = ffmpeg_set + ' -vtag hvc1'

        if self.use_crf == True:
            ffmpeg_set = ffmpeg_set + ' -crf ' + self.crf
        else:
            ffmpeg_set = ffmpeg_set + ' -b:v ' + self.bit + 'm '

        ffmpeg_set = ffmpeg_set + ' -c:a aac '
        return ffmpeg_set

    def run(self):
        vpy_folder = self.outfolder + '/vpys'
        if not os.path.exists(vpy_folder):
            os.makedirs(vpy_folder)  # 存放配置文件vpy的文件夹

        video_folder = self.outfolder + '/out_videos'
        if not os.path.exists(video_folder):
            os.makedirs(video_folder)

        ffmpeg_code = self.ffmpeg_()
        vpy_data = open(self.vpy, 'r', encoding='utf-8')
        if self.run_mode == 'getbat':
            num = 1
            bat_file = open(self.outfolder + '/run.bat', 'w', encoding='ansi')
            for video in self.videos:
                print('生成第' + str(num) + '个vpy脚本文件')
                video_name = (video.rsplit("/", 1))[-1]
                video_name = (video_name.rsplit(".", 1))[0]  # 只保留文件名的参数
                vpy_place = vpy_folder + '/' + video_name + '.vpy'
                vpy_target=open(vpy_place,'w',encoding='utf-8')

                for data in vpy_data:
                    if 'core.lsmas.LWLibavSource' in data:
                      data_=data.split('core.lsmas.LWLibavSource',1)[0]
                      data_=data_+'core.lsmas.LWLibavSource(r"'+video+'")'
                      vpy_target.write(data_+'\n')
                    else:
                        vpy_target.write(data)
                if self.use_encode_diy == False:
                    bat_file.write(
                        '"' + self.directory + '\\vapoursynth\\VSPipe.exe"' + ' -c y4m ' + vpy_place + ' - | "' + self.directory + '\\vapoursynth\\ffmpeg.exe" -i pipe: -i ' + video + ffmpeg_code + video_folder + '/' + video_name + '.' + self.vformat + '\n')
                else:
                    bat_file.write(
                        '"' + self.directory + '\\vapoursynth\\VSPipe.exe"' + ' -c y4m ' + vpy_place + ' - | "' + self.directory + '\\vapoursynth\\ffmpeg.exe" ' + self.encode_diy)
            bat_file.close()
        elif self.run_mode=='start':
            num = 1
            for video in self.videos:
                print('生成第' + str(num) + '个vpy脚本文件')
                video_name = (video.rsplit("/", 1))[-1]
                video_name = (video_name.rsplit(".", 1))[0]  # 只保留文件名的参数
                vpy_place = vpy_folder + '/' + video_name + '.vpy'
                vpy_target = open(vpy_place, 'w', encoding='utf-8')

                for data in vpy_data:
                    if 'core.lsmas.LWLibavSource' in data:
                      data_=data.split('core.lsmas.LWLibavSource',1)[0]
                      data_=data_+'core.lsmas.LWLibavSource(r"'+video+'")'
                      vpy_target.write(data_+'\n')
                    else:
                        vpy_target.write(data)
                vpy_target.close()

                command_out = self.directory + '\\vapoursynth\\VSPipe.exe -c y4m ' + vpy_place + ' -'
                if self.use_encode_diy == False:
                    command_in = self.directory + '\\vapoursynth\\ffmpeg.exe -i pipe: -i ' + video + ffmpeg_code + video_folder + '/' + video_name + '.' + self.vformat
                else:
                    command_in = self.directory + '\\vapoursynth\\ffmpeg.exe ' + self.encode_diy
                pipe_out = sp.Popen(command_out, stdout=sp.PIPE, shell=True)
                pipe_in = sp.Popen(command_in, stdin=pipe_out.stdout, stdout=sp.PIPE, stderr=sp.STDOUT, shell=True,
                                   encoding="utf-8", text=True)
                for line in pipe_in.stdout:
                    print(line)
                num = num + 1
        self.signal.emit()




class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        sys.stdout = Signal()
        sys.stdout.text_update.connect(self.updatetext)

        self.pb_github.clicked.connect(self.open_github)
        self.pb_afd.clicked.connect(self.open_afd)
        self.pb_bili.clicked.connect(self.open_bili)

        self.pb_clear_auto.clicked.connect(self.clear_auto)
        self.pb_clearall_auto.clicked.connect(self.clearall_auto)
        self.pb_input_auto.clicked.connect(self.input_auto)

        self.pb_input_diy.clicked.connect(self.input_diy)
        self.pb_clear_diy.clicked.connect(self.clear_diy)
        self.pb_clearall_diy.clicked.connect(self.clearall_diy)

        self.pb_vpyin_diy.clicked.connect(self.vpyin)
        self.pb_readvpy_diy.clicked.connect(self.readvpy)
        self.pb_clearvpy_diy.clicked.connect(self.clearvpy)
        self.pb_debugvpy_diy.clicked.connect(self.debugvpy)

        self.pb_outfolder.clicked.connect(self.outfolder)

        self.pb_getbat.clicked.connect(self.getbat)
        self.pb_start.clicked.connect(self.start)

    def updatetext(self, text):
        """
            更新textBrowser
        """
        cursor = self.tb_show.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.tb_show.append(text)
        self.tb_show.setTextCursor(cursor)
        self.tb_show.ensureCursorVisible()

    def open_github(self):
        github_url = 'https://github.com/NangInShell'
        webbrowser.open(github_url)

    def open_afd(self):
        afd_url = 'https://afdian.net/a/NangInShell'
        webbrowser.open(afd_url)

    def open_bili(self):
        bili_url = 'https://space.bilibili.com/335908558'
        webbrowser.open(bili_url)

    def clear_auto(self):
        self.lw_input_auto.takeItem(self.lw_input_auto.row(self.lw_input_auto.currentItem()))

    def clearall_auto(self):
        self.lw_input_auto.clear()

    def input_auto(self):
        files = QFileDialog.getOpenFileNames(self,
                                             "多文件选择",
                                             "./",
                                             "videos (*.mp4 *.mkv *.mov *.m2ts *.avi *.ts *.flv *.rmvb *.m4v)")

        print(files[0])
        for file in files[0]:
            self.lw_input_auto.addItem(file)

    def clear_diy(self):
        self.lw_input_diy.takeItem(self.lw_input_diy.row(self.lw_input_diy.currentItem()))

    def clearall_diy(self):
        self.lw_input_diy.clear()

    def input_diy(self):
        files = QFileDialog.getOpenFileNames(self,
                                             "多文件选择",
                                             "./",
                                             "videos (*.mp4 *.mkv *.mov *.m2ts *.avi *.ts *.flv *.rmvb *.m4v)")
        print(files[0])
        for file in files[0]:
            self.lw_input_diy.addItem(file)

    def vpyin(self):
        fname,ftype= QFileDialog.getOpenFileName(self, "打开文件", "/", "*.vpy")
        self.le_vpy_loc.setText(fname)
        print(fname)

    def clearvpy(self):
        self.le_vpy_loc.clear()

    def debugvpy(self):
        QMessageBox.information(self, "提示信息", "别点这个按钮，暂时没用，请使用vseditor来debug")

    def readvpy(self):
        if os.path.exists(self.le_vpy_loc.text()):
            vpy=self.le_vpy_loc.text()
            #print(vpy)
            file=open(vpy,'r',encoding='UTF-8')
            data=file.read()
            self.te_readvpy.setText(data)
            print("读取vpy文件:"+vpy)
        else:
            QMessageBox.information(self, "提示信息", "文件类型错误或无法读取文件")
            print("文件类型错误或无法读取文件")
        # print(data)

    def outfolder(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      "./")  # 起始路径
        self.le_outfile.setText(directory)
    def getbat(self):
        self.pb_getbat.setEnabled(False)
        self.pb_getbat.setText('正在生成')
        #auto_sr
        videos=[]
        if self.rb_auto.isChecked()==True:
            video_num=self.lw_input_auto.count()
            for i in range(video_num):
                videos.append(self.lw_input_auto.item(i).text())
        elif self.r_diy.isChecked()==True:
            video_num = self.lw_input_diy.count()
            for i in range(video_num):
                videos.append(self.lw_input_diy.item(i).text())

        device=self.cb_device.currentText()
        half='True'
        if self.rb_half.isChecked()==False:
            half='False'
        sr_method='Real_cugan'
        if self.toolBox.currentIndex()==0:
            sr_method = 'Real_cugan'
        elif self.toolBox.currentIndex()==1:
            sr_method = 'Real_esrgan'
        cugan_model=self.cb_cg_model.currentText()
        cugan_tile=self.cb_cg_tile.currentText()
        cugan_alpha=self.db_cg_alpha.text()
        cugan_set=cugan_setting(cugan_model,cugan_tile,cugan_alpha)

        esrgan_model=self.cb_eg_model.currentText()
        esrgan_tile=self.cb_eg_tile.currentText()
        esrgan_scale=self.cb_eg_scale.currentText()
        esrgan_set=esrgan_setting(esrgan_model,esrgan_tile,esrgan_scale)

        is_rs_bef=self.rb_resize_bef.isChecked()
        is_rs_aft=self.rb_resize_aft.isChecked()

        rs_bef_w=self.sb_rsbef_w.text()
        rs_bef_h=self.sb_rsbef_h.text()
        rs_aft_w=self.sb_rsaft_w.text()
        rs_aft_h=self.sb_rsaft_h.text()

        #encode setting
        outfolder=self.le_outfile.text()
        encoder=self.cb_encode.currentText()
        preset=self.cb_preset.currentText()
        eformat=self.cb_eformat.currentText()
        vformat=self.cb_vformat.currentText()
        use_crf=self.rb_crf.isChecked()
        use_bit=self.rb_bit.isChecked()
        crf=self.sb_crf.text()
        bit=self.sb_bit.text()
        encode_diy=self.te_encode.toPlainText()
        use_sr_auto=self.rb_auto.isChecked()
        use_diy=self.rb_diy.isChecked()
        use_encode_diy=self.rb_encode.isChecked()

        sr_auto_set=sr_auto_setting(videos,device,half,sr_method,cugan_set,esrgan_set,is_rs_bef,is_rs_aft,rs_bef_w,rs_bef_h,rs_aft_w,rs_aft_h)
        encode_set=encode_setting(outfolder,encoder,preset,eformat,vformat,use_crf,use_bit,crf,bit,encode_diy,use_sr_auto,use_diy,use_encode_diy)

        if use_sr_auto == True:
            if outfolder =='':
                QMessageBox.information(self, "提示信息", "请选择输出文件夹")
            else:
                self.sr_Thread=sr_auto(sr_auto_set,encode_set,'getbat')
                self.sr_Thread.signal.connect(self.set_btn_bat)
                self.sr_Thread.setDaemon(True)
                self.sr_Thread.start()

        vpy=self.le_vpy_loc.text()
        diy_set=diy_setting(videos,vpy)
        if use_diy==True:
            if outfolder == '':
                QMessageBox.information(self, "提示信息", "请选择输出文件夹")
            else:
                self.diy_Thread=diy_encode(diy_set,encode_set,'getbat')
                self.diy_Thread.signal.connect(self.set_btn_bat)
                self.diy_Thread.setDaemon(True)
                self.diy_Thread.start()

        # if use_diy == True:

    def set_btn_bat(self):#生成bat开关控制
        self.pb_getbat.setText('生成bat')
        self.pb_getbat.setEnabled(True)

    def start(self):
        self.pb_start.setEnabled(False)
        self.pb_start.setText('运行ing')

        videos = []
        if self.rb_auto.isChecked() == True:
            video_num = self.lw_input_auto.count()
            for i in range(video_num):
                videos.append(self.lw_input_auto.item(i).text())
        elif self.r_diy.isChecked() == True:
            video_num = self.lw_input_diy.count()
            for i in range(video_num):
                videos.append(self.lw_input_diy.item(i).text())

        device=self.cb_device.currentText()
        half='True'
        if self.rb_half.isChecked()==False:
            half='False'
        sr_method='Real_cugan'
        if self.toolBox.currentIndex()==0:
            sr_method = 'Real_cugan'
        elif self.toolBox.currentIndex()==1:
            sr_method = 'Real_esrgan'
        cugan_model=self.cb_cg_model.currentText()
        cugan_tile=self.cb_cg_tile.currentText()
        cugan_alpha=self.db_cg_alpha.text()
        cugan_set=cugan_setting(cugan_model,cugan_tile,cugan_alpha)

        esrgan_model=self.cb_eg_model.currentText()
        esrgan_tile=self.cb_eg_tile.currentText()
        esrgan_scale=self.cb_eg_scale.currentText()
        esrgan_set=esrgan_setting(esrgan_model,esrgan_tile,esrgan_scale)

        is_rs_bef=self.rb_resize_bef.isChecked()
        is_rs_aft=self.rb_resize_aft.isChecked()

        rs_bef_w=self.sb_rsbef_w.text()
        rs_bef_h=self.sb_rsbef_h.text()
        rs_aft_w=self.sb_rsaft_w.text()
        rs_aft_h=self.sb_rsaft_h.text()

        #encode setting
        outfolder=self.le_outfile.text()
        encoder=self.cb_encode.currentText()
        preset=self.cb_preset.currentText()
        eformat=self.cb_eformat.currentText()
        vformat=self.cb_vformat.currentText()
        use_crf=self.rb_crf.isChecked()
        use_bit=self.rb_bit.isChecked()
        crf=self.sb_crf.text()
        bit=self.sb_bit.text()
        encode_diy=self.te_encode.toPlainText()
        use_sr_auto=self.rb_auto.isChecked()
        use_diy=self.rb_diy.isChecked()
        use_encode_diy=self.rb_encode.isChecked()

        sr_auto_set=sr_auto_setting(videos,device,half,sr_method,cugan_set,esrgan_set,is_rs_bef,is_rs_aft,rs_bef_w,rs_bef_h,rs_aft_w,rs_aft_h)
        encode_set=encode_setting(outfolder,encoder,preset,eformat,vformat,use_crf,use_bit,crf,bit,encode_diy,use_sr_auto,use_diy,use_encode_diy)

        if use_sr_auto == True:
            if outfolder == '':
                QMessageBox.information(self, "提示信息", "请选择输出文件夹")
            else:
                self.sr_Thread=sr_auto(sr_auto_set,encode_set,'start')
                self.sr_Thread.signal.connect(self.set_btn_start)
                self.sr_Thread.setDaemon(True)
                self.sr_Thread.start()

        vpy = self.le_vpy_loc.text()
        diy_set = diy_setting(videos, vpy)

        if use_diy == True:
            if outfolder == '':
                QMessageBox.information(self, "提示信息", "请选择输出文件夹")
            else:
                self.diy_Thread = diy_encode(diy_set, encode_set, 'start')
                self.diy_Thread.signal.connect(self.set_btn_start)
                self.diy_Thread.setDaemon(True)
                self.diy_Thread.start()

    def set_btn_start(self):#一键运行开关控制
        self.pb_start.setEnabled(True)
        self.pb_start.setText('一键启动')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('logo.png'))
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())