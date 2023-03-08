# VSET --Video SuperResolution Encode Tool
基于*Vapoursynth*的图形化视频批量压制处理工具，现阶段已经初步测试完毕

开源3.1版本正在公测中，欢迎大家使用、反馈

<img src="https://user-images.githubusercontent.com/72263191/212935212-516e32a0-5171-4dc0-907e-d5162af4ce2d.png" alt="Anime!" width="250"/>

## 简介
VSET是一款可以提升视频分辨率(Super-Resolution)的工具，**在Windows环境下使用**

#### 特性  
&#x2705; **动漫**视频超分辨率  
&#x2705; 实拍视频超分辨率   
&#x2705; 流行的补帧算法rife  
&#x2705; **自定义参数压制**   
&#x2705; 支持队列**批量处理**   
&#x2705; 支持**多开**，支持高性能处理（提高高性能显卡的cuda占用）   
&#x2705; **开源**   

## 更新进度
### 2023-01-17更新
- 新增了Swinir算法，适用于三次元超分辨率
- 新增了Waifu2x算法的新模型，新增后waifu2x模型数量超过30个模型   
- 所有算法除了ncnn模式外均支持半精度推理
- 使用cuda或ncnn时任务可终止，TRT模式的在生成引擎时终止的话需要去任务管理器终止，其他情况下可以直接终止。
- 去掉了抗锯齿滤镜，新增了添加噪点的滤镜
- QTGMC滤镜支持隔行扫描视频倍帧
- 更新补帧算法rife，vsmlrt版本。支持TRT，cuda，ncnn推理，转场识别。
- 新增可自定义的后端推理参数设置，可提高显卡的占用，用尽显卡的所有性能。
- UI优化和其他已知BUG修复
- 可能解决了AMD显卡的使用问题，AMD显卡用户默认只可使用ncnn推理，且不支持多卡。但由于开发没有AMD显卡测试，所以用户得自己测试能否使用。


## 安装
方法一：[百度网盘](https://pan.baidu.com/s/1M6KIbEBRi35SZtOtd1zVjQ?pwd=Nang)

整合包下载解压后即可使用
![image](https://user-images.githubusercontent.com/72263191/223602793-365fc17b-b3dd-4369-9eba-c5239f13e872.png)

方法二：steam在线更新

**因为国内网盘下载的局限性，为了照顾没有网盘的小伙伴，后期考虑上传软件到steam在线平台，如果你想在steam上获得及时的更新,而不用每次都重复下载网盘的重复文件的话可以联系开发者索要序列码。在测试开发阶段的版本和网盘版本同步更新，不收费，谨防上当受骗。以后steam上线正式版本也会同步更新网盘离线版。不想用steam的玩家可以在github或B站获得与最新版本一样的网盘离线版的更新内容。**

**测试要求：使用过VSET 3.0及之后的版本一段时间，有显存大于等于6G的20，30，40系列的显卡，有一颗能与人平等交流的心和一定的测试时间。**

**steam开发测试群请联系下面QQ群的管理员**

## 使用步骤   
1. 输入输出页面导入视频文件队列并设置输出文件夹   
2. 超分设置页面设置好相关参数   
3. 压制设置页面设置好压制参数   
4. 交付页面点击一键启动

*注意：如果出现错误，请使用交付页面的debug模式运行，会在输出文件夹生成相关批处理(.bat)文件，将文件内容截图反馈给开发*

## 软件界面
![image](https://user-images.githubusercontent.com/72263191/223601902-b4312dc5-4124-4077-b753-54e4f2214f3b.png) "软件主界面")
![image](https://user-images.githubusercontent.com/72263191/223601936-038a9cf6-0e74-4162-bfd6-27f21cb8cc2c.png))
![image](https://user-images.githubusercontent.com/72263191/223601954-cc2fee41-336c-4109-a0a8-1b57b364a65e.png))
![image](https://user-images.githubusercontent.com/72263191/223602057-a378275c-478d-4a2c-ba67-98ada39b970e.png))
![image](https://user-images.githubusercontent.com/72263191/223602086-768c989c-ae79-4549-b4cb-48ceab31ce8b.png))
![image]((https://user-images.githubusercontent.com/72263191/223602166-60ae7692-d0b8-4413-ab7b-58ca37928c4b.png)
![image](https://user-images.githubusercontent.com/72263191/223602286-a78aa928-187b-40ef-8ced-e0f3bfabf591.png)

## 相关链接
[爱发电](https://afdian.net/a/NangInShell)   
如果您觉得软件使用体验不错，且**自身经济条件尚可**，可以在爱发电平台支持一下

[BiliBili: NangInShell](https://space.bilibili.com/335908558)   

[QQ交流群：711185279]

## 参考
[超分算法](https://github.com/HolyWu)

[rife ncnn](https://github.com/styler00dollar)

[vs-mlrt vs接口支持](https://github.com/AmusementClub/vs-mlrt)

[vs-Editor](https://github.com/YomikoR/VapourSynth-Editor)

[vapoursynth](https://github.com/vapoursynth/vapoursynth)

[ffmpeg](https://github.com/FFmpeg/FFmpeg)
