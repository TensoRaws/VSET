import subprocess as sp
import os
import sys
import json
from PyQt5.QtCore import  QObject

class FFprobe():
    def __init__(self):
        self.filepath = ''
        self.video_info = {}
        self.directory = os.path.dirname(os.path.realpath(sys.argv[0]))

    def parse(self, filepath):
        self.filepath = filepath
        try:
            res = sp.check_output(
                [self.directory + '/ffprobe', '-i', self.filepath, '-print_format', 'json', '-show_format',
                 '-show_streams', '-v',
                 'quiet'], shell=True)

            res = res.decode('utf8')
            self.video_info = json.loads(res)
            # print('_video_info ',self._video_info)
        except Exception as e:
            print(e)
            raise Exception('获取视频信息失败')


    def video_full_frame(self):
        stream = self._video_info['streams'][0]
        return stream['nb_frames']

    def color_info(self):

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

class get_video_info(QObject):
    def __init__(self,filename):

        self.video_info=filename
        self.ffprobe = FFprobe()
        self.ffprobe.parse(self.video_info)

    #判断可变帧率
    def is_Vfr(self):
        # extract the video stream information
        for item in self.ffprobe.video_info['streams']:
            if item['codec_type'] == 'video':
                avg_frame_rate = item['avg_frame_rate']
                r_frame_rate = item['r_frame_rate']
                return avg_frame_rate != r_frame_rate
        else:
            return None#不存在视频流

    def is_HaveAudio(self):
        for item in self.ffprobe.video_info['streams']:
            if item['codec_type'] == 'audio':
                return True
        return False

    def is_HaveSubtitle(self):
        for item in self.ffprobe.video_info['streams']:
            if item['codec_type'] == 'subtitle':
                return True
        return False

#print(get_video_info(r'M:\code\VSET_os\video_test\10秒内封字幕.mkv').is_HaveSubtitle())



