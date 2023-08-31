import os
import subprocess as sp
import json
import time
from configparser import ConfigParser
from pynvml import *
from Signal import Signal

from PyQt5.QtGui import QTextCursor,QIcon
from PyQt5.QtCore import *
import cpuinfo

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from VSET_UI import Ui_MainWindow

#参数
from method import cugan_ml_setting,esrgan_ml_setting,waifu2x_ml_setting,vsrpp_setting,swinir_setting
from method import esrgan_setting,codeformer_setting,rife_ml_setting,rifenc_setting,every_set_object,mlrt_setting
#推理
from render import autorun,autorun_test


class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        #绑定信息框
        sys.stdout = Signal()
        sys.stdout.text_update.connect(self.updatetext)

        self.real_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #加载显卡
        try:
            nvmlInit()
            deviceCount = nvmlDeviceGetCount()

            for i in range(deviceCount):
                handle = nvmlDeviceGetHandleByIndex(i)
                device = (str(i) + ":" + str(nvmlDeviceGetName(handle),'utf8'))
                self.cb_gpu.addItem(device)
        except:
            print("加载N卡失败，负载显卡强制设置为0,不存在N卡或显卡驱动太陈旧。")


        self.video_clear.clicked.connect(self.clear_video_list)
        self.video_clearall.clicked.connect(self.clear_all_video_list)
        self.video_input.clicked.connect(self.input_video_list)

        self.select_of.clicked.connect(self.outfolder)

        self.save_config.clicked.connect(self.save_conf_Manual)
        self.load_config.clicked.connect(self.load_conf_Manual)

        self.autorun_Thread=None#预加载线程
        self.debugrun_Thread=None#预加载线程
        self.previewrun_Thread = None  # 预加载线程

        self.load_conf_auto()
      # self.setWindowFlags(Qt.FramelessWindowHint)#隐藏窗口
        self.render.clicked.connect(self.auto_run)
        self.debug.clicked.connect(self.debug_run)
        self.stop_render.clicked.connect(self.quit_thread)
        self.video_preview.clicked.connect(self.preview_run)

        for _char in self.real_path:
            if '\u4e00' <= _char <= '\u9fa5' or _char == ' ':
                QMessageBox.information(self, "提示信息", "你的软件存放路径不符合规范，建议把软件存放到只有英文/数字的路径下,不要有空格")
                break

    def updatetext(self, text):
        """
            更新textEdit
        """
        cursor = self.te_show.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.te_show.insertPlainText(text)
        self.te_show.setTextCursor(cursor)
        self.te_show.ensureCursorVisible()

        # cursor = self.te_show.textCursor()
        # cursor.movePosition(QTextCursor.End)
        # progress_start = self.te_show.toPlainText().rfind("frame=")  # 查找最近的 "progress:" 标记
        # if progress_start == -1:  # 如果没有找到，则将新的进度信息附加到文本的末尾
        #     self.te_show.insertPlainText(text)
        # else:  # 如果找到了，则将新的进度信息替换旧的进度信息
        #     cursor.setPosition(progress_start)
        #     cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        #     # QTimer.singleShot(1000, lambda: cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor))
        #     cursor.insertText(text)
        #     self.te_show.setTextCursor(cursor)
        # self.te_show.ensureCursorVisible()

    def clear_video_list(self):
        self.video_list.takeItem(self.video_list.row(self.video_list.currentItem()))

    def clear_all_video_list(self):
        self.video_list.clear()
        self.out_folder.clear()

    def input_video_list(self):
        files = QFileDialog.getOpenFileNames(self,
                                             "多文件选择",
                                             "./",
                                             "videos (*.mp4 *.mkv *.mov *.m2ts *.avi *.ts *.flv *.rmvb *.m4v)")
        for file in files[0]:
            self.video_list.addItem(file)

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
        gpu=self.cb_gpu.currentText()

        videos = []
        video_num = self.video_list.count()
        for i in range(video_num):
            videos.append(self.video_list.item(i).text())

        video_select = self.video_list.row(self.video_list.currentItem())

        audios =[]
        audio_num = self.audio_list.count()
        for i in range(audio_num):
            audios.append(self.audio_list.item(i).text())

        subs=[]
        sub_num = self.sub_list.count()
        for i in range(sub_num):
            subs.append(self.sub_list.item(i).text())

        outfolder = self.out_folder.text()

        # 其他参数设置
        cm_numstream =self.sb_ns_cm.text()
        cm_gragh = self.rb_gragh_cm.isChecked()

        tm_numstream = self.sb_ns_tm.text()
        trt_output = self.cb_output_tm.currentText()
        trt_force16 = self.rb_force16_tm.isChecked()
        trt_graph = self.rb_graph_tm.isChecked()
        trt_cublas = self.rb_cublas_tm.isChecked()
        trt_heuristic = self.rb_heuristic_tm.isChecked()
        om_numstream = self.sb_ns_om.text()

        nm_numstream =self.sb_ns_nm.text()

        qtgmcFps = self.cb_qtgmcFps.currentText()

        priority = self.cb_Priority.currentText()
        use_sr = self.rb_SR.isChecked()
        sr_gpu_id = self.cb_gpuid_sr.currentText()
        use_half_sr=self.rb_half_sr.isChecked()
        #是否使用超分use_sr，负载显卡sr_gpu_id，半精度use_half,已经选择

        cugan_ml_device = self.cb_device_mlrt_cg.currentText()
        cugan_ml_model = self.cb_model_mlrt_cg.currentText()
        cugan_ml_tile = self.cb_tile_mlrt_cg.currentText()
        cugan_ml_alpha = self.db_alpha_mlrt_cg.text()
        mlrt_sr_set=mlrt_setting(cugan_ml_device,cm_numstream,cm_gragh,tm_numstream,trt_output,trt_force16,
                                 trt_graph,trt_cublas,trt_heuristic,om_numstream,nm_numstream,use_half_sr,sr_gpu_id)
        cugan_ml_set = cugan_ml_setting(mlrt_sr_set, cugan_ml_model, cugan_ml_tile, cugan_ml_alpha)

        esrgan_ml_device = self.cb_device_mlrt_eg.currentText()
        esrgan_ml_model = self.cb_model_mlrt_eg.currentText()
        esrgan_ml_tile = self.cb_tile_mlrt_eg.currentText()
        esrgan_ml_scale = self.cb_scale_mlrt_eg.currentText()
        mlrt_sr_set=mlrt_setting(esrgan_ml_device,cm_numstream,cm_gragh,tm_numstream,trt_output,trt_force16,
                                 trt_graph,trt_cublas,trt_heuristic,om_numstream,nm_numstream,use_half_sr,sr_gpu_id)
        esrgan_ml_set = esrgan_ml_setting(mlrt_sr_set, esrgan_ml_model, esrgan_ml_tile,
                                          esrgan_ml_scale)

        waifu_ml_device = self.cb_device_mlrt_wf.currentText()
        waifu_ml_model = self.cb_model_mlrt_wf.currentText()
        waifu_ml_tile = self.cb_tile_mlrt_wf.currentText()
        mlrt_sr_set=mlrt_setting(waifu_ml_device,cm_numstream,cm_gragh,tm_numstream,trt_output,trt_force16,
                                 trt_graph,trt_cublas,trt_heuristic,om_numstream,nm_numstream,use_half_sr,sr_gpu_id)
        waifu_ml_set = waifu2x_ml_setting(mlrt_sr_set, waifu_ml_model, waifu_ml_tile)

        vsrpp_model = self.cb_model_vsrpp.currentText()
        vsrpp_length = self.sb_length_vsrpp.text()
        vsrpp_half=use_half_sr#半精度
        vsrpp_gpu_id=sr_gpu_id#设备编号
        vsrpp_set = vsrpp_setting(vsrpp_model, vsrpp_length,vsrpp_half,vsrpp_gpu_id)

        swinir_model = self.cb_model_sw.currentText()
        swinir_tile = self.cb_tile_sw.currentText()
        swinir_half = use_half_sr  # 半精度
        swinir_gpu_id = sr_gpu_id  # 设备编号
        swinir_set = swinir_setting(swinir_model, swinir_tile,swinir_half,swinir_gpu_id)

        esrgan_model = self.cb_model_eg.currentText()
        esrgan_tile = self.cb_tile_eg.currentText()
        esrgan_half = use_half_sr  # 半精度
        esrgan_gpu_id = sr_gpu_id  # 设备编号
        esrgan_set = esrgan_setting(esrgan_model, esrgan_tile,esrgan_half,esrgan_gpu_id)

        former_model = self.cb_model_cf.currentText()
        former_scale = self.cb_scale_cf.currentText()
        former_weight = self.db_weigh_cf.text()
        former_ocf = self.rb_centerface_cf.isChecked()
        former_gpu_id = sr_gpu_id  # 设备编号
        codeformer_set = codeformer_setting(former_model, former_scale, former_weight, former_ocf,former_gpu_id)

        sr_method = self.cb_SR.currentText()  # 算法名称
        if sr_method == 'Real_cugan_mlrt':
            sr_set = cugan_ml_set
        elif sr_method == 'Real_esrgan_mlrt':
            sr_set = esrgan_ml_set
        elif sr_method == 'Waifu2x_mlrt':
            sr_set = waifu_ml_set
        elif sr_method == 'Basicvsrpp':
            sr_set = vsrpp_set
        elif sr_method == 'swinir':
            sr_set = swinir_set
        elif sr_method == 'Real_esrgan':
            sr_set = esrgan_set
        elif sr_method == 'codeformer':
            sr_set = codeformer_set

        use_vfi = self.rb_VFI.isChecked()
        vfi_gpu_id = self.cb_gpuid_vfi.currentText()
        use_half_vfi = self.rb_half_vfi.isChecked()
        # 是否使用补帧use_vfi，负载显卡vfi_gpu_id，半精度use_half_vfi,已经选择

        rife_ml_device = self.cb_device_mlrt_rife.currentText()
        rife_ml_model = self.cb_model_mlrt_rife.currentText()
        rife_ml_cscale = self.sb_cscale_mlrt_rife.text()
        rife_ml_scale = self.cb_scale_mlrt_rife.currentText()
        rife_ml_change=self.db_change_mlrt_rife.text()
        rife_ml_debef=self.cb_debef_mlrt_rife.currentText()
        rife_ml_deaft=self.cb_deaft_mlrt_rife.currentText()
        mlrt_vfi_set = mlrt_setting(rife_ml_device,cm_numstream,cm_gragh,tm_numstream,trt_output,trt_force16,
                                 trt_graph,trt_cublas,trt_heuristic,om_numstream,nm_numstream,use_half_sr,sr_gpu_id)
        rife_ml_set = rife_ml_setting(mlrt_vfi_set, rife_ml_model, rife_ml_cscale, rife_ml_scale,rife_ml_change,rife_ml_debef,rife_ml_deaft)

        rifenc_model = self.cb_model_rifenc.currentText()
        usecs_rifenc = self.rb_usecs_rifenc.isChecked()#使用补帧倍数
        usec_rifenc = self.rb_usec_rifenc.isChecked()#使用补帧帧数
        cscale_rifenc = self.sb_cscale_rifenc.text()#倍数
        c_rifenc = self.sb_c_rifenc.text()#帧数
        skip_rifenc = self.rb_skip_rifenc.isChecked()
        tta_rifenc = self.rb_tta_rifenc.isChecked()
        uhd_rifenc = self.rb_uhd_rifenc.isChecked()
        static_rifenc = self.sb_static_rifenc.text()
        rifenc_set = rifenc_setting(rifenc_model, usecs_rifenc, usec_rifenc, cscale_rifenc, c_rifenc, skip_rifenc,
                                    tta_rifenc, uhd_rifenc, static_rifenc,vfi_gpu_id)

        vfi_method = self.cb_VFI.currentText()
        if vfi_method == 'rife_mlrt':
            vfi_set = rife_ml_set
        elif vfi_method == 'rife_ncnn':
            vfi_set = rifenc_set

        #预处理参数设置
        use_qtgmc = self.rb_qtgmc.isChecked()
        use_deband = self.rb_deband.isChecked()
        use_taa_bef = self.rb_taa_bef.isChecked()
        is_rs_bef = self.rb_resize_bef.isChecked()
        rs_bef_w = self.sb_rsbef_w.text()
        rs_bef_h = self.sb_rsbef_h.text()

        #后处理
        use_cas_aft=self.rb_cas_aft.isChecked()
        use_taa_aft=self.rb_taa_aft.isChecked()
        add_noise=self.rb_addnoise.isChecked()
        is_rs_aft = self.rb_resize_aft.isChecked()
        rs_aft_w = self.sb_rsaft_w.text()
        rs_aft_h = self.sb_rsaft_h.text()

        # encode setting
        encoder = self.cb_encoder.currentText()
        preset_switch = {
            'cpu_H265': self.cb_preset_h265c.currentText(),
            'cpu_H264': self.cb_preset_h264c.currentText(),
            'cpu_Av1': self.cb_preset_av1c.currentText(),
            'nvenc_H265': self.cb_preset_h265g.currentText(),
            'nvenc_H264': self.cb_preset_h264g.currentText(),
            'nvenc_Av1': self.cb_preset_av1g.currentText(),
            'qsv_H265': self.cb_preset_h265q.currentText(),
            'qsv_H264': self.cb_preset_h264q.currentText(),
            'qsv_Av1': self.cb_preset_av1q.currentText()
        }
        preset = preset_switch[encoder] \
            if encoder in preset_switch else 'medium'
        vformat = self.cb_vformat.currentText()
        use_crf = self.rb_crf.isChecked()
        use_bit = self.rb_bit.isChecked()
        crf = self.sb_crf.text()
        bit = self.sb_bit.text()

        use_encode_audio = self.rb_audiotrans.isChecked()
        audio_format = self.cb_aformat.currentText()
        use_source_audio = self.rb_save_source_audio.isChecked()
        use_input_audio = self.rb_input_audio.isChecked()

        use_source_sub=self.rb_save_source_sub.isChecked()
        attach_input_sub = self.rb_attach_sub.isChecked()
        embed_input_sub =self.rb_embed_sub.isChecked()

        customization_encode = self.te_customization_encode.toPlainText()
        use_customization_encode = self.rb_customization_encode.isChecked()


        return every_set_object(gpu,videos,video_select, audios,subs,outfolder,
                                use_sr, sr_gpu_id, use_half_sr,sr_method, sr_set, use_vfi, vfi_gpu_id,use_half_vfi, vfi_method,vfi_set,
                                use_qtgmc, use_deband, use_taa_bef,use_cas_aft,use_taa_aft,add_noise,
                                is_rs_bef, is_rs_aft, rs_bef_w, rs_bef_h, rs_aft_w, rs_aft_h,
                                encoder, preset, vformat, use_crf, use_bit, crf, bit,
                                use_encode_audio,use_source_audio, use_input_audio,audio_format,
                                use_source_sub, attach_input_sub, embed_input_sub,
                                customization_encode, use_customization_encode,
                                cm_numstream,cm_gragh,tm_numstream,trt_output,trt_force16,trt_graph,trt_cublas,trt_heuristic,om_numstream,nm_numstream,
                                qtgmcFps,priority)

    def save_conf_set(self):
        conf = ConfigParser()
        every_setting = self.every_set()
        conf.add_section('sr')
        conf.set('sr', 'use_sr', str(every_setting.use_sr))
        conf.set('sr', 'sr_gpu_id', str(every_setting.sr_gpu_id))
        conf.set('sr', 'use_half_sr', str(every_setting.use_half_sr))

        conf.set('sr', 'sr_method', str(every_setting.sr_method))

        if every_setting.sr_method == 'Real_cugan_mlrt':
            conf.set('sr', 'device', str(every_setting.sr_set.mlrt_set.device))
            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'tile', str(every_setting.sr_set.tile))
            conf.set('sr', 'alpha', str(every_setting.sr_set.alpha))
        elif every_setting.sr_method == 'Real_esrgan_mlrt':
            conf.set('sr', 'device', str(every_setting.sr_set.mlrt_set.device))
            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'tile', str(every_setting.sr_set.tile))
            conf.set('sr', 'scale', str(every_setting.sr_set.scale))
        elif every_setting.sr_method == 'Waifu2x_mlrt':
            conf.set('sr', 'device', str(every_setting.sr_set.mlrt_set.device))
            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'tile', str(every_setting.sr_set.tile))
        elif every_setting.sr_method == 'Basicvsrpp':
            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'length', str(every_setting.sr_set.length))
        elif every_setting.sr_method == 'swinir':
            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'tile', str(every_setting.sr_set.tile))
        elif every_setting.sr_method == 'Real_esrgan':


            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'tile', str(every_setting.sr_set.tile))
        elif every_setting.sr_method == 'codeformer':
            conf.set('sr', 'model', str(every_setting.sr_set.model))
            conf.set('sr', 'scale', str(every_setting.sr_set.scale))
            conf.set('sr', 'weight', str(every_setting.sr_set.weight))
            conf.set('sr', 'ocf', str(every_setting.sr_set.ocf))

        conf.add_section('vfi')
        conf.set('vfi', 'use_vfi', str(every_setting.use_vfi))
        conf.set('vfi', 'vfi_gpu_id', str(every_setting.vfi_gpu_id))
        conf.set('vfi', 'rb_half_vfi', str(every_setting.use_half_vfi))
        conf.set('vfi', 'vfi_method', str(every_setting.vfi_method))
        if every_setting.vfi_method == 'rife_mlrt':
            conf.set('vfi', 'device', str(every_setting.vfi_set.mlrt_set.device))
            conf.set('vfi', 'model', str(every_setting.vfi_set.model))
            conf.set('vfi', 'cscale', str(every_setting.vfi_set.cscale))
            conf.set('vfi', 'scale', str(every_setting.vfi_set.scale))
            conf.set('vfi', 'change', str(every_setting.vfi_set.change))
            conf.set('vfi', 'debef', str(every_setting.vfi_set.debef))
            conf.set('vfi', 'deaft', str(every_setting.vfi_set.deaft))
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
        conf.add_section('fix')
        conf.set('fix', 'use_qtgmc ', str(every_setting.use_qtgmc))
        conf.set('fix', 'use_deband', str(every_setting.use_deband))
        conf.set('fix', 'use_taa_bef', str(every_setting.use_taa_bef))

        conf.set('fix', 'use_cas_aft ', str(every_setting.use_cas_aft))
        conf.set('fix', 'use_taa_aft', str(every_setting.use_taa_aft))
        conf.set('fix', 'add_noise', str(every_setting.add_noise))

        conf.set('fix', 'is_rs_bef ', str(every_setting.is_rs_bef))
        conf.set('fix', 'is_rs_aft', str(every_setting.is_rs_aft))
        conf.set('fix', 'rs_bef_w', str(every_setting.rs_bef_w))
        conf.set('fix', 'rs_bef_h', str(every_setting.rs_bef_h))
        conf.set('fix', 'rs_aft_w', str(every_setting.rs_aft_w))
        conf.set('fix', 'rs_aft_h', str(every_setting.rs_aft_h))
        conf.add_section('encode')
        conf.set('encode', 'encoder', str(every_setting.encoder))
        conf.set('encode', 'preset', str(every_setting.preset))
        conf.set('encode', 'vformat', str(every_setting.vformat))
        conf.set('encode', 'use_crf', str(every_setting.use_crf))
        conf.set('encode', 'use_bit', str(every_setting.use_bit))
        conf.set('encode', 'crf', str(every_setting.crf))
        conf.set('encode', 'bit', str(every_setting.bit))

        conf.set('encode', 'use_encode_audio', str(every_setting.use_encode_audio))
        conf.set('encode', 'use_source_audio', str(every_setting.use_source_audio))
        conf.set('encode', 'audio_format', str(every_setting.audio_format))
        conf.set('encode', 'use_input_audio', str(every_setting.use_input_audio))

        conf.set('encode', 'use_source_sub', str(every_setting.use_source_sub))
        conf.set('encode', 'attach_input_sub', str(every_setting.attach_input_sub))
        conf.set('encode', 'embed_input_sub', str(every_setting.embed_input_sub))

        conf.set('encode', 'customization_encode', str(every_setting.customization_encode))
        conf.set('encode', 'use_customization_encode', str(every_setting.use_customization_encode))
        conf.add_section('else_set')

        conf.set('else_set', 'out_folder', str(every_setting.outfolder))
        conf.set('else_set', 'videos', str(every_setting.videos))
        conf.set('else_set', 'audios', str(every_setting.audios))
        conf.set('else_set', 'subs', str(every_setting.subs))

        conf.set('else_set', 'cm_numstream', str(every_setting.cm_numstream))
        conf.set('else_set', 'cm_gragh', str(every_setting.cm_gragh))

        conf.set('else_set', 'tm_numstream', str(every_setting.tm_numstream))
        conf.set('else_set', 'trt_output', str(every_setting.mlrt_trt_output))
        conf.set('else_set', 'trt_force16', str(every_setting.mlrt_trt_force16))
        conf.set('else_set', 'trt_graph', str(every_setting.mlrt_trt_graph))
        conf.set('else_set', 'trt_cublas', str(every_setting.mlrt_trt_cublas))
        conf.set('else_set', 'trt_heuristic', str(every_setting.mlrt_trt_heuristic))

        conf.set('else_set', 'om_numstream', str(every_setting.om_numstream))

        conf.set('else_set', 'nm_numstream', str(every_setting.nm_numstream))

        conf.set('else_set', 'qtgmcFps', str(every_setting.qtgmcFps))
        conf.set('else_set', 'priority', str(every_setting.priority))
        return conf

    def load_conf_set(self,conf):
        self.rb_SR.setChecked(conf['sr'].getboolean('use_sr'))
        self.cb_gpuid_sr.setCurrentText(conf['sr']['sr_gpu_id'])
        self.rb_half_sr.setChecked(conf['sr'].getboolean('use_half_sr'))
        self.cb_SR.setCurrentText(conf['sr']['sr_method'])
        if conf['sr']['sr_method'] == 'Real_cugan_mlrt':
            self.cb_device_mlrt_cg.setCurrentText(conf['sr']['device'])
            self.cb_model_mlrt_cg.setCurrentText(conf['sr']['model'])
            self.cb_tile_mlrt_cg.setCurrentText(conf['sr']['tile'])
            self.db_alpha_mlrt_cg.setValue(conf['sr'].getfloat('alpha'))

        elif conf['sr']['sr_method'] == 'Real_esrgan_mlrt':
            self.cb_device_mlrt_eg.setCurrentText(conf['sr']['device'])
            self.cb_model_mlrt_eg.setCurrentText(conf['sr']['model'])
            self.cb_tile_mlrt_eg.setCurrentText(conf['sr']['tile'])
            self.cb_scale_mlrt_eg.setCurrentText(conf['sr']['scale'])

        elif conf['sr']['sr_method'] == 'Waifu2x_mlrt':
            self.cb_device_mlrt_wf.setCurrentText(conf['sr']['device'])
            self.cb_model_mlrt_wf.setCurrentText(conf['sr']['model'])
            self.cb_tile_mlrt_wf.setCurrentText(conf['sr']['tile'])

        elif conf['sr']['sr_method'] == 'Basicvsrpp':
            self.cb_model_vsrpp.setCurrentText(conf['sr']['model'])
            self.sb_length_vsrpp.setValue(conf['sr'].getint('length'))

        elif conf['sr']['sr_method'] == 'swinir':
            self.cb_model_sw.setCurrentText(conf['sr']['model'])
            self.cb_tile_sw.setCurrentText(conf['sr']['tile'])

        elif conf['sr']['sr_method'] == 'Real_esrgan':
            self.cb_model_eg.setCurrentText(conf['sr']['model'])
            self.cb_tile_eg.setCurrentText(conf['sr']['tile'])

        elif conf['sr']['sr_method'] == 'codeformer':
            self.cb_model_cf.setCurrentText(conf['sr']['model'])
            self.cb_scale_cf.setCurrentText(conf['sr']['scale'])
            self.db_weigh_cf.setValue(conf['sr'].getfloat('weight'))
            self.rb_centerface_cf.setChecked(conf['sr'].getboolean('ocf'))

        self.rb_VFI.setChecked(conf['vfi'].getboolean('use_vfi'))
        self.rb_half_vfi.setChecked(conf['vfi'].getboolean('rb_half_vfi'))
        self.cb_gpuid_vfi.setCurrentText(conf['vfi']['vfi_gpu_id'])
        self.cb_VFI.setCurrentText(conf['vfi']['vfi_method'])
        if conf['vfi']['vfi_method'] == 'rife_mlrt':
            self.cb_model_mlrt_rife.setCurrentText(conf['vfi']['model'])
            self.cb_device_mlrt_rife.setCurrentText(conf['vfi']['device'])
            self.sb_cscale_mlrt_rife.setValue(conf['vfi'].getint('cscale'))
            self.cb_scale_mlrt_rife.setCurrentText(conf['vfi']['scale'])
            self.db_change_mlrt_rife.setValue(conf['vfi'].getfloat('change'))
            self.cb_debef_mlrt_rife.setCurrentText(conf['vfi']['debef'])
            self.cb_deaft_mlrt_rife.setCurrentText(conf['vfi']['deaft'])
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
        self.rb_qtgmc.setChecked(conf['fix'].getboolean('use_qtgmc'))
        self.rb_deband.setChecked(conf['fix'].getboolean('use_deband'))
        self.rb_taa_bef.setChecked(conf['fix'].getboolean('use_taa_bef'))

        self.rb_cas_aft.setChecked(conf['fix'].getboolean('use_cas_aft'))
        self.rb_taa_aft.setChecked(conf['fix'].getboolean('use_taa_aft'))
        self.rb_addnoise.setChecked(conf['fix'].getboolean('add_noise'))

        self.rb_resize_bef.setChecked(conf['fix'].getboolean('is_rs_bef'))
        self.rb_resize_aft.setChecked(conf['fix'].getboolean('is_rs_aft'))
        self.sb_rsbef_w.setValue(conf['fix'].getint('rs_bef_w'))
        self.sb_rsbef_h.setValue(conf['fix'].getint('rs_bef_h'))
        self.sb_rsaft_w.setValue(conf['fix'].getint('rs_aft_w'))
        self.sb_rsaft_h.setValue(conf['fix'].getint('rs_aft_h'))
        self.cb_encoder.setCurrentText(conf['encode']['encoder'])
        preset_switch = {
            'cpu_H265': self.cb_preset_h265c,
            'cpu_H264': self.cb_preset_h264c,
            'cpu_Av1': self.cb_preset_av1c,
            'nvenc_H265': self.cb_preset_h265g,
            'nvenc_H264': self.cb_preset_h264g,
            'nvenc_Av1': self.cb_preset_av1g,
            'qsv_H265': self.cb_preset_h265q,
            'qsv_H264': self.cb_preset_h264q,
            'qsv_Av1': self.cb_preset_av1q
        }
        preset = preset_switch[conf['encode']['encoder']]
        if conf['encode']['encoder'] in preset_switch:
            preset = preset_switch[conf['encode']['encoder']]
            preset.setCurrentText(conf['encode']['preset'])
        self.cb_vformat.setCurrentText(conf['encode']['vformat'])
        self.rb_bit.setChecked(conf['encode'].getboolean('use_bit'))
        self.rb_crf.setChecked(conf['encode'].getboolean('use_crf'))
        self.sb_bit.setValue(conf['encode'].getint('bit'))
        self.sb_crf.setValue(conf['encode'].getint('crf'))

        self.rb_audiotrans.setChecked(conf['encode'].getboolean('use_encode_audio'))
        self.rb_save_source_audio.setChecked(conf['encode'].getboolean('use_source_audio'))
        self.cb_aformat.setCurrentText(conf['encode']['audio_format'])
        self.rb_input_audio.setChecked(conf['encode'].getboolean('use_input_audio'))

        self.rb_save_source_sub.setChecked(conf['encode'].getboolean('use_source_sub'))
        self.rb_attach_sub.setChecked(conf['encode'].getboolean('attach_input_sub'))
        self.rb_embed_sub.setChecked(conf['encode'].getboolean('embed_input_sub'))

        self.rb_customization_encode.setChecked(conf['encode'].getboolean('use_customization_encode'))
        self.te_customization_encode.setText(conf['encode']['customization_encode'])

        self.out_folder.setText(conf['else_set']['out_folder'])

        self.sb_ns_cm.setValue(conf['else_set'].getint('cm_numstream'))
        self.rb_gragh_cm.setChecked(conf['else_set'].getboolean('cm_gragh'))

        self.sb_ns_tm.setValue(conf['else_set'].getint('tm_numstream'))
        self.cb_output_tm.setCurrentText(conf['else_set']['trt_output'])
        self.rb_force16_tm.setChecked(conf['else_set'].getboolean('trt_force16'))
        self.rb_graph_tm.setChecked(conf['else_set'].getboolean('trt_graph'))
        self.rb_cublas_tm.setChecked(conf['else_set'].getboolean('trt_cublas'))
        self.rb_heuristic_tm.setChecked(conf['else_set'].getboolean('trt_heuristic'))
        self.sb_ns_om.setValue(conf['else_set'].getint('om_numstream'))

        self.sb_ns_nm.setValue(conf['else_set'].getint('nm_numstream'))

        self.cb_qtgmcFps.setCurrentText(conf['else_set']['qtgmcFps'])
        self.cb_Priority.setCurrentText(conf['else_set']['priority'])

    def save_conf_Manual(self):
        self.save_config.setEnabled(False)
        self.save_config.setText('保存ing')
        print(self.real_path+'/config.ini')
        with open(self.real_path+'/config.ini', 'w', encoding='utf-8') as f:
            (self.save_conf_set()).write(f)
        QMessageBox.information(self, "提示信息", "已保存当前自定义预设")
        self.save_config.setEnabled(True)
        self.save_config.setText('保存预设')

    def load_conf_Manual(self):
        self.load_config.setEnabled(False)
        self.load_config.setText('加载ing')
        print(self.real_path+"\config.ini")
        if not os.path.exists(self.real_path+"/config.ini"):
            QMessageBox.information(self, "提示信息", "自定义预设文件不存在")
        else:
            conf = ConfigParser()
            conf.read(self.real_path+"\config.ini", encoding="utf-8")
            self.load_conf_set(conf)
            print("已加载保存的自定义预设")
            print(' ')

        self.load_config.setEnabled(True)
        self.load_config.setText('加载预设')

    def save_conf_auto(self):
        with open(self.real_path+'\config_auto.ini', 'w', encoding='utf-8') as f:
            conf=self.save_conf_set()
            conf.write(f)
        print("已自动保存当前设置，下次启动软件时自动加载")

    def load_conf_auto(self):
        if os.path.exists(self.real_path+"/config_auto.ini"):
            conf = ConfigParser()
            conf.read(self.real_path+"/config_auto.ini", encoding="utf-8")
            try:
                self.load_conf_set(conf)
                print("已自动加载上一次软件运行设置")
            except:
                print('加载失败，配置文件出错，请重新保存配置')
            print(' ')

    def closeEvent(self, event):
        self.quit_thread()
        self.save_conf_auto()
        time.sleep(1)
        super().closeEvent(event)

    def is_allowRun(self):
        every_setting = self.every_set()
        allowRun = True

        if every_setting.use_sr == True and every_setting.use_vfi == True:
            if 'mlrt' in every_setting.sr_method and 'mlrt' not in every_setting.vfi_method:
                allowRun = False
                QMessageBox.information(self, "提示信息",
                                        "vsmlrt的超分库不能vsmlrt以外的补帧库混用，请取消选择一个补帧或超分的启动开关")
            if 'mlrt' not in every_setting.sr_method and 'mlrt' in every_setting.vfi_method:
                allowRun = False
                QMessageBox.information(self, "提示信息",
                                        "vsmlrt的补帧库不能vsmlrt以外的超分库混用，请取消选择一个补帧或超分的启动开关")

        if every_setting.use_input_audio == True:
            if len(every_setting.videos) != len(every_setting.audios):
                allowRun = False
                QMessageBox.information(self, "提示信息",
                                        "输入的音频和输入视频数量不一致，终止启动进程")

        if every_setting.attach_input_sub == True or every_setting.embed_input_sub == True:
            if len(every_setting.videos) != len(every_setting.subs):
                allowRun = False
                QMessageBox.information(self, "提示信息",
                                        "输入的字幕和输入视频数量不一致，终止启动进程")

        for video_name in every_setting.videos:
            if os.path.dirname(video_name) == every_setting.outfolder:
                allowRun = False
                print('输出文件夹不能与输入视频的文件夹同目录,已自动终止运行')
                QMessageBox.information(self, "提示信息", "输出文件夹不能与输入视频的文件夹同目录")
                break

        if every_setting.outfolder == '':
            allowRun = False
            QMessageBox.information(self, "提示信息", "输出文件夹为空，请选择输出文件夹")
        return allowRun

    def auto_run(self):
        self.stackedWidget.setCurrentIndex(4)
        self.list_main.setCurrentRow(4)
        # self.list_main.setCurrentIndex(4)
        self.render.setEnabled(False)
        self.render.setText('渲染压制ing')

        self.debug.setEnabled(False)
        self.debug.setText('Debug')

        self.video_preview.setEnabled(False)
        self.video_preview.setText('预览')

        allow_autorun=self.is_allowRun()
        every_setting = self.every_set()

        if allow_autorun == True:
            self.autorun_Thread = autorun(every_setting, 'start')
            self.autorun_Thread.signal.connect(self.set_btn_auto_run)
            self.autorun_Thread.start()
        else:
            self.set_btn_auto_run()

    def debug_run(self):
        self.stackedWidget.setCurrentIndex(4)
        self.list_main.setCurrentRow(4)

        self.render.setEnabled(False)
        self.render.setText('启动渲染')
        self.debug.setEnabled(False)
        self.debug.setText('Debug运行ing')
        self.video_preview.setEnabled(False)
        self.video_preview.setText('预览')

        every_setting=self.every_set()
        allow_debug=self.is_allowRun()

        if allow_debug == True:
            self.debugrun_Thread = autorun(every_setting, 'debug')
            self.debugrun_Thread.signal.connect(self.set_btn_auto_run)
            self.debugrun_Thread.start()
        else:
            self.set_btn_auto_run()

    def preview_run(self):
        self.stackedWidget.setCurrentIndex(4)
        self.list_main.setCurrentRow(4)
        self.render.setEnabled(False)
        self.render.setText('启动渲染')
        self.debug.setEnabled(False)
        self.debug.setText('Debug')
        self.video_preview.setEnabled(False)
        self.video_preview.setText('预览')

        every_setting = self.every_set()
        allow_debug = self.is_allowRun()

        video = every_setting.video_select
        if video == -1:
            QMessageBox.information(self, "提示信息",
                                    "未选择目标视频")
            print('未选择目标视频')
            allow_debug = False
        else:
            video = (every_setting.videos)[video]
            for _char in video:
                if '\u4e00' <= _char <= '\u9fa5':
                    QMessageBox.information(self, "提示信息", "预览路径不符合规范，预览文件名和路径名只有英文/英文符号/数字的路径下")
                    print('预览路径不符合规范，预览文件名和路径名只有英文/英文符号/数字的路径下')
                    allow_debug=False
                    break
        if allow_debug == True:
            self.previewrun_Thread = autorun(every_setting, 'preview')
            self.previewrun_Thread.signal.connect(self.set_btn_auto_run)
            self.previewrun_Thread.start()
        else:
            self.set_btn_auto_run()

    def quit_thread(self):
          if self.autorun_Thread!= None:
              self.autorun_Thread.stop_()

          self.render.setEnabled(True)
          self.render.setText('启动渲染')
          self.debug.setEnabled(True)
          self.debug.setText('Debug')
          print('已终止当前任务，如果程序还在运行（高占用）的话请检查任务管理器后台')

    def set_btn_auto_run(self):#一键运行开关控制
        self.render.setEnabled(True)
        self.render.setText('启动渲染')
        self.debug.setEnabled(True)
        self.debug.setText('Debug')
        self.video_preview.setEnabled(True)
        self.video_preview.setText('预览')


if __name__ == "__main__":

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('logo.png'))
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())