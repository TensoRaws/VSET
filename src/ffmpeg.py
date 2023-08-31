from PyQt5.QtCore import  QObject

class ffmpeg_info(QObject):
    def __init__(self,every_set):
        self.ffmpeg_set = every_set
                
    def return_ffmpeg(self):
        ffmpeg_code=[]
        if self.ffmpeg_set.use_customization_encode == True:
            self.ffmpeg_code_customizatio = str(self.ffmpeg_set.customization_encode)
            for str_ in self.ffmpeg_code_customizatio.split():
                ffmpeg_code.append(str_)
        else:
            if self.ffmpeg_set.encoder == 'cpu_H265':
                ffmpeg_code.append('-c:v')
                ffmpeg_code.append('libx265')
                ffmpeg_code.append('-pix_fmt')
                ffmpeg_code.append('yuv420p10le')
                ffmpeg_code.append('-profile:v')
                ffmpeg_code.append('main10')
                ffmpeg_code.append('-vtag')
                ffmpeg_code.append('hvc1')
            elif self.ffmpeg_set.encoder == 'cpu_H264':
                ffmpeg_code.append('-c:v')
                ffmpeg_code.append('libx264')
                ffmpeg_code.append('-pix_fmt')
                ffmpeg_code.append('yuv420p')
                ffmpeg_code.append('-profile:v')
                ffmpeg_code.append('main')
            elif self.ffmpeg_set.encoder == 'cpu_Av1':
                ffmpeg_code.append('-c:v')
                ffmpeg_code.append('libaom-av1')
                ffmpeg_code.append('-pix_fmt')
                ffmpeg_code.append('yuv420p10le')
            elif self.ffmpeg_set.encoder == 'nvenc_H264':
                ffmpeg_code.append('-c:v')
                ffmpeg_code.append('h264_nvenc')
                ffmpeg_code.append('-pix_fmt')
                ffmpeg_code.append('yuv420p')
            elif self.ffmpeg_set.encoder == 'nvenc_H265':
                ffmpeg_code.append('-c:v')
                ffmpeg_code.append('hevc_nvenc')
                ffmpeg_code.append('-pix_fmt')
                ffmpeg_code.append('p010le')
                ffmpeg_code.append('-profile:v')
                ffmpeg_code.append('main10')
                ffmpeg_code.append('-vtag')
                ffmpeg_code.append('hvc1')
            elif self.ffmpeg_set.encoder == 'nvenc_Av1':
                ffmpeg_code.append('-c:v')
                ffmpeg_code.append('av1_nvenc')
                ffmpeg_code.append('-pix_fmt')
                ffmpeg_code.append('p010le')
                ffmpeg_code.append('-profile:v')
                ffmpeg_code.append('main10')
            elif self.ffmpeg_set.encoder == 'qsv_H264':
                ffmpeg_code.append('-c:v')
                ffmpeg_code.append('h264_qsv')
                ffmpeg_code.append('-pix_fmt')
                ffmpeg_code.append('p010le')
            elif self.ffmpeg_set.encoder == 'qsv_H265':
                ffmpeg_code.append('-c:v')
                ffmpeg_code.append('hevc_qsv')
                ffmpeg_code.append('-pix_fmt')
                ffmpeg_code.append('p010le')
                ffmpeg_code.append('-profile:v')
                ffmpeg_code.append('main10')
                ffmpeg_code.append('-vtag')
                ffmpeg_code.append('hvc1')
            elif self.ffmpeg_set.encoder == 'qsv_Av1':
                ffmpeg_code.append('-c:v')
                ffmpeg_code.append('av1_qsv')
                ffmpeg_code.append('-pix_fmt')
                ffmpeg_code.append('p010le')

            ffmpeg_code.append('-preset')
            ffmpeg_code.append(self.ffmpeg_set.preset)

            if self.ffmpeg_set.use_crf == True:
                if 'nvenc' not in self.ffmpeg_set.encoder:
                    ffmpeg_code.append('-crf')
                    ffmpeg_code.append(self.ffmpeg_set.crf)
                else:
                    ffmpeg_code.append('-cq')
                    ffmpeg_code.append(self.ffmpeg_set.crf)
            else:
                ffmpeg_code.append('-b:v')
                ffmpeg_code.append(self.ffmpeg_set.bit + 'M')

        return ffmpeg_code
