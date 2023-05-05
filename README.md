# VSET --Video SuperResolution Encode Tool
基于*Vapoursynth*的图形化视频批量压制处理工具，现阶段已经初步测试完毕

开源3.2版本已更新，欢迎大家使用、反馈

## 特别注意
**网络上出现一些未经允许私自搬运VSET压缩包到收费下载网站的行为，遂特此说明，VSET目前没有任何第三方下载方式，也没有任何第三方收费服务，请只认准本项目github的下载方式。**

**同时本项目的所有源代码，程序和附带的自建环境禁止用于任何第三方未经许可的商业用途。可在遵守开源协议下的条件下二次分发。**

<img src="https://user-images.githubusercontent.com/72263191/212935212-516e32a0-5171-4dc0-907e-d5162af4ce2d.png" alt="Anime!" width="250"/>

## [💬 感谢发电名单](https://github.com/NangInShell/VSET/blob/main/Thanks.md)
感谢发电大佬们对本项目的支持以及所有测试用户的测试支持。以上链接包含了发电者名单和项目支出详情。

&#x2705; **发电大佬可联系开发者优先加入专门的debug群**

&#x2705; **QQ交流群：711185279**

发电地址:[**爱发电**](https://afdian.net/a/NangInShell)  

## 简介
VSET是一款可以提升视频分辨率(Super-Resolution)的工具，**在Windows环境下使用**

#### 特性  
&#x2705; **动漫**视频超分辨率  
&#x2705; **实拍**视频超分辨率  
&#x2705; 流行的**补帧**算法rife  
&#x2705; QTGMC，deband等常用**vs滤镜**  
&#x2705; **16bit**高精度处理   
&#x2705; **预览**  
&#x2705; 完整的**字幕**，**音频**处理流程  
&#x2705; **自定义**参数压制**   
&#x2705; 支持队列**批量处理**   
&#x2705; 支持**多开**，支持高性能处理（提高高性能显卡的占用）   
&#x2705; **开源**   

## 更新进度
### 2023-04-27更新

- **新增预览功能，可在渲染前预览任意设置下任何时间点（任何一帧）的画面。**
- **优化输出信息，可获取输出视频的目标分辨率，帧数，当前运行进度，码率，速率，预计剩余时间。**
- **新增对Intel显卡的支持，现在软件对A卡，I卡，N卡全面支持。**
- **Basicvsrpp新增至十个模型，移除老版本的basicvsr算法。**
- **新增codeformat人脸修复算法。**
- **修复Swinir,Realesrgan算法显存占用过大的问题。**
- **新增多个滤镜设置。**
- **修复nvenc硬件编码的cq参数问题，修了hevc-qsv,h264-qsv压制不能运行的问题。**
- **新增多个可选编码器，新增多个压制预设。**
- **新增字幕外部导入外挂或内嵌，音频外部导入。**
- **修复mp4封装flac音频的问题。**
- **新增设置“先超后补”，“先补后超”。**


## 安装
方法一：[百度网盘](https://pan.baidu.com/s/1oilF8cgjdiN6D_0ZQz1sLw?pwd=Nang)

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

![image](https://user-images.githubusercontent.com/72263191/234762202-da7eb2e2-9fec-447e-9730-c71dbb453e7f.png)
![image](https://user-images.githubusercontent.com/72263191/234762228-ec8daaa3-6cc8-4942-985a-570dfec088a0.png)
![image](https://user-images.githubusercontent.com/72263191/234762234-c4162dd5-29d9-4fff-8bb0-ecce47ed8884.png)
![image](https://user-images.githubusercontent.com/72263191/234762242-234e47d0-01af-4722-8528-47841e22e3f4.png)
![image](https://user-images.githubusercontent.com/72263191/234762250-94963d6e-ce69-4513-ab4f-33aabeb26846.png)
![image](https://user-images.githubusercontent.com/72263191/234762266-854fd9f6-6d18-462f-8dd1-7baf8bea0daf.png)
![image](https://user-images.githubusercontent.com/72263191/234762275-cd32511c-9ab1-48d8-a4f8-41d69df1a443.png)

## 相关链接
[爱发电](https://afdian.net/a/NangInShell)  

[BiliBili: NangInShell](https://space.bilibili.com/335908558)   

[QQ交流群：711185279]

## 参考
[超分算法](https://github.com/HolyWu)

[rife ncnn](https://github.com/styler00dollar)

[vs-mlrt vs接口支持](https://github.com/AmusementClub/vs-mlrt)

[vs-Editor](https://github.com/YomikoR/VapourSynth-Editor)

[vapoursynth](https://github.com/vapoursynth/vapoursynth)

[ffmpeg](https://github.com/FFmpeg/FFmpeg)
