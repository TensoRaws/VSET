import vapoursynth as vs
core = vs.core
res = core.lsmas.LWLibavSource(r"D:/code/VSET_Vue/video/test2.mp4")
res = core.resize.Bicubic(clip=res,format=vs.YUV420P16)
res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)
res=core.fmtc.bitdepth(res, bits=32)
from vsmlrt import CUGAN,RealESRGAN,Waifu2x,RIFE,Backend
device_sr=Backend.ORT_CUDA()
device_sr.device_id=0
device_sr.fp16=True
res = RealESRGAN(res, scale=2,tiles=1,model=5005, backend=device_sr)
res = core.resize.Bicubic(clip=res,matrix_s="709",format=vs.YUV420P16)
res.set_output()
