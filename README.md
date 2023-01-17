# VSET（VapourSynth Encode Tool）
基于Vapoursynth的图形化视频批量压制处理工具,集成了Real-cugan,Real-esrgan,Waifu2x的二次元超分算法，以及适用于三次元超分辨率的算法BasicVSRpp。
现阶段已经初步测试完毕。开源2.0版本正在公测中，欢迎各位大佬帮忙测试。
## 20230117更新
-集成了BasicVSRpp算法，支持6个常用模型   
-集成了Waifu2x算法，支持将近30个模型   
-软件目前解决了AMD CPU的压制问题，用户可以使用AMD CPU压制视频   
-更新了vs-mlrt至v13版本

## 相关地址
[百度网盘下载地址](https://pan.baidu.com/s/1Lq1frEIHFmN-mJlWsmmX6g?pwd=Nang)

[爱发电](https://afdian.net/a/NangInShell)   
如果您觉得软件还可以，且有经济能力的话，可以稍微爱发电平台支持一下软件的开发。

[BiliBili:NangInShell](https://space.bilibili.com/335908558)   

**软件QQ交流群：711185279**
## 安装方法
整合包下载解压后即可使用，更新包用于debug，一般用不到。
![image](https://user-images.githubusercontent.com/72263191/212929996-4cf59811-faef-4b57-b3a7-543986414e5a.png)

## 使用步骤   
1，输入输出页面导入视频文件队列和设置输出文件夹   
2，超分设置里设置好相关参数   
3，压制设置里设置好压制参数   
4，交付页面点击交互。   
（注意：如果出现错误请使用交付页面的debug模型运行，会在输出文件夹生成相关批处理文件，文件内容截图发给开发）   
## 软件界面
![image](https://user-images.githubusercontent.com/72263191/212924504-eebf637b-c327-4b33-bcfb-e4dbe00e5862.png "软件主界面")
![image](https://user-images.githubusercontent.com/72263191/212927595-b094dfcb-ccde-4c7f-b37a-53dd921e1605.png)
![image](https://user-images.githubusercontent.com/72263191/212927649-bd8afe86-3e64-410f-9237-34ddd9093d2f.png)
![image](https://user-images.githubusercontent.com/72263191/212927683-23b31165-a1a3-4bac-bc36-838fab097004.png)
![image](https://user-images.githubusercontent.com/72263191/212927706-d8b9b500-6c46-4b37-a7f0-23afb50e66df.png)

## 其他链接（感谢大佬们的付出）
[（BasicVSRpp vs接口支持）https://github.com/HolyWu/vs-basicvsrpp](https://github.com/HolyWu/vs-basicvsrpp)

[（vs-mlrt vs接口支持）https://github.com/AmusementClub/vs-mlrt](https://github.com/AmusementClub/vs-mlrt)

[（vs-Editor）https://github.com/YomikoR/VapourSynth-Editor](https://github.com/YomikoR/VapourSynth-Editor)

[（vapoursynth）https://github.com/vapoursynth/vapoursynth](https://github.com/vapoursynth/vapoursynth)

[（ffmpeg）https://github.com/FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg)
