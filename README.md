# VSET --VapourSynth Encode Tool
基于*Vapoursynth*的图形化视频批量压制处理图形化工具，现阶段已经初步测试完毕

开源2.0版本正在公测中，欢迎大家使用   

<img src="https://user-images.githubusercontent.com/72263191/212935212-516e32a0-5171-4dc0-907e-d5162af4ce2d.png" alt="Anime!" width="250"/>

## 简介
VSET是一款可以提升视频分辨率(Super-Resolution)的工具   

#### 特性  
&#x2705; **动漫**视频超分辨率  
&#x2705; 实拍视频超分辨率   
&#x2705; **自定义参数压制**   
&#x2705; 支持队列**批量处理**   
&#x2705; 支持**多开**，吃满显卡CPU   
&#x2705; **开源、免费**   

## 更新进度
### 2023-01-17更新
- 集成了BasicVSRpp算法，支持6个常用模型   
- 集成了Waifu2x算法，支持将近30个模型   
- 软件目前解决了AMD CPU的压制问题，用户可以使用AMD CPU压制视频   
- 更新了vs-mlrt至v13版本

## 安装
*注意：第一次使用时不要运行update.exe*
### 方法一 - 在线安装
[Online Installer](https://github.com/NangInShell/VSET/releases/tag/v.2.0.0-installer)

**请保证网络稳定，建议开启tun/tap代理模式**

### 方法二 - 离线下载
[VSET](https://github.com/NangInShell/VSET/releases/latest) 
[vs_vsmlrt环境包](https://github.com/Tohrusky/vs_vsmlrt/releases/latest)
[vs_pytorch环境包](https://github.com/Tohrusky/vs_pytorch/releases/latest)

下载完环境包和主程序后，将两个环境包直接解压到*VSET*的根目录即可
```
$ ls
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         1/18/2023   9:44 PM                vs_pytorch
d-----         1/18/2023   9:22 PM                vs_vsmlrt
-a----         1/18/2023   9:09 PM       38856845 VSET.exe
-a----         1/18/2023   9:09 PM       13664459 update.exe
```

### 方法三 - 国内网盘
[百度网盘](https://pan.baidu.com/s/1Lq1frEIHFmN-mJlWsmmX6g?pwd=Nang)

整合包下载解压后即可使用
![image](https://user-images.githubusercontent.com/72263191/212929996-4cf59811-faef-4b57-b3a7-543986414e5a.png)

## 使用步骤   
1. 输入输出页面导入视频文件队列并设置输出文件夹   
2. 超分设置页面设置好相关参数   
3. 压制设置页面设置好压制参数   
4. 交付页面点击一键启动

*注意：如果出现错误，请使用交付页面的debug模式运行，会在输出文件夹生成相关批处理(.bat)文件，将文件内容截图反馈给开发*

## 软件界面
![image](https://user-images.githubusercontent.com/72263191/212924504-eebf637b-c327-4b33-bcfb-e4dbe00e5862.png "软件主界面")
![image](https://user-images.githubusercontent.com/72263191/212927595-b094dfcb-ccde-4c7f-b37a-53dd921e1605.png)
![image](https://user-images.githubusercontent.com/72263191/212927649-bd8afe86-3e64-410f-9237-34ddd9093d2f.png)
![image](https://user-images.githubusercontent.com/72263191/212927683-23b31165-a1a3-4bac-bc36-838fab097004.png)
![image](https://user-images.githubusercontent.com/72263191/212927706-d8b9b500-6c46-4b37-a7f0-23afb50e66df.png)

## 相关链接
[爱发电](https://afdian.net/a/NangInShell)   
如果您觉得软件使用体验不错，且**自身经济条件尚可**，可以在爱发电平台支持一下

[BiliBili: NangInShell](https://space.bilibili.com/335908558)   

[QQ交流群：711185279]

## 参考
[BasicVSRpp vs接口支持](https://github.com/HolyWu/vs-basicvsrpp)

[vs-mlrt vs接口支持](https://github.com/AmusementClub/vs-mlrt)

[vs-Editor](https://github.com/YomikoR/VapourSynth-Editor)

[vapoursynth](https://github.com/vapoursynth/vapoursynth)

[ffmpeg](https://github.com/FFmpeg/FFmpeg)
